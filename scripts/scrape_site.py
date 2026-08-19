#!/usr/bin/env python3
"""Full-site crawler that mirrors a website into a queryable local corpus.

Standard library only, so it runs anywhere Python 3.9+ is installed with no
`pip install` step. Crawls one site breadth-first, obeys robots.txt, and writes

    <out>/pages.jsonl        one JSON record per HTML page (the search corpus)
    <out>/assets.jsonl       one JSON record per non-HTML resource that was seen
    <out>/raw/...            byte-for-byte HTML mirror
    <out>/text/...           extracted plain text
    <out>/markdown/...       markdown rendering of each page
    <out>/crawl_state.json   visited set + frontier, so a crawl can be resumed
    <out>/crawl_report.json  summary of the last run

Use scripts/query_site.py to search and read the result.

Examples
--------
    scripts/scrape_site.py https://www.zagzoog.com
    scripts/scrape_site.py https://www.zagzoog.com --out data/zagzoog --delay 1.5
    scripts/scrape_site.py https://www.zagzoog.com --resume --max-pages 2000
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import re
import signal
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
import xml.etree.ElementTree as ET
import zlib
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from typing import Iterable

DEFAULT_UA = (
    "Mozilla/5.0 (compatible; SiteArchiveBot/1.0; "
    "+https://github.com/yaserzagzoog/Science-)"
)
HTML_TYPES = ("text/html", "application/xhtml+xml")
XML_TYPES = ("text/xml", "application/xml", "application/rss+xml", "application/atom+xml")
# Query parameters that only carry campaign/session noise and would otherwise
# multiply the same page into many "distinct" URLs.
TRACKING_PARAMS = re.compile(
    r"^(utm_[a-z_]+|gclid|fbclid|msclkid|mc_cid|mc_eid|_ga|ref|referrer|"
    r"igshid|yclid|s_kwcid|ttclid)$",
    re.I,
)
SKIP_SCHEMES = {"mailto", "tel", "javascript", "data", "sms", "ftp", "file", "about"}
BLOCK_TAGS = {
    "address", "article", "aside", "blockquote", "br", "div", "dd", "dl", "dt",
    "fieldset", "figcaption", "figure", "footer", "form", "h1", "h2", "h3", "h4",
    "h5", "h6", "header", "hr", "li", "main", "nav", "ol", "p", "pre", "section",
    "table", "tbody", "td", "tfoot", "th", "thead", "tr", "ul",
}
INVISIBLE_TAGS = {"script", "style", "noscript", "template", "svg", "canvas", "iframe"}


# --------------------------------------------------------------------------
# URL helpers
# --------------------------------------------------------------------------

def normalize_url(url: str, base: str | None = None) -> str | None:
    """Absolutize, strip fragments and tracking params, canonicalize the host.

    Returns None for anything that is not a crawlable http(s) URL.
    """
    if not url:
        return None
    url = url.strip()
    if not url or url.startswith("#"):
        return None
    scheme = url.split(":", 1)[0].lower() if ":" in url[:12] else ""
    if scheme in SKIP_SCHEMES:
        return None
    if base:
        url = urllib.parse.urljoin(base, url)
    parts = urllib.parse.urlsplit(url)
    if parts.scheme not in ("http", "https"):
        return None
    host = parts.hostname or ""
    if not host:
        return None
    netloc = host.lower()
    if parts.port and not (
        (parts.scheme == "http" and parts.port == 80)
        or (parts.scheme == "https" and parts.port == 443)
    ):
        netloc = f"{netloc}:{parts.port}"
    query = urllib.parse.urlencode(
        [
            (k, v)
            for k, v in urllib.parse.parse_qsl(parts.query, keep_blank_values=True)
            if not TRACKING_PARAMS.match(k)
        ]
    )
    path = re.sub(r"/{2,}", "/", parts.path) or "/"
    return urllib.parse.urlunsplit((parts.scheme, netloc, path, query, ""))


def registrable(host: str) -> str:
    """Drop a leading 'www.' so example.com and www.example.com are one site."""
    host = host.lower()
    return host[4:] if host.startswith("www.") else host


def url_to_path(url: str, extension: str) -> str:
    """Map a URL onto a stable, filesystem-safe relative path."""
    parts = urllib.parse.urlsplit(url)
    path = parts.path
    if path.endswith("/") or not path:
        path += "index"
    segments = [re.sub(r"[^A-Za-z0-9._-]", "_", s) for s in path.split("/") if s]
    if parts.query:
        digest = hashlib.sha1(parts.query.encode()).hexdigest()[:10]
        segments[-1] = f"{segments[-1]}__q{digest}"
    # Keep individual segments short enough for every common filesystem.
    segments = [s[:100] for s in segments]
    root, dot_ext = os.path.splitext(segments[-1])
    if dot_ext.lower() in (".html", ".htm", ".php", ".asp", ".aspx", ".jsp"):
        segments[-1] = root
    return os.path.join(parts.netloc.replace(":", "_"), *segments) + extension


# --------------------------------------------------------------------------
# HTML parsing
# --------------------------------------------------------------------------

class PageParser(HTMLParser):
    """Extracts title, metadata, links, headings, text and markdown in one pass."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.lang = ""
        self.canonical = ""
        self.meta: dict[str, str] = {}
        self.links: list[dict[str, str]] = []
        self.headings: list[dict[str, str]] = []
        self.robots_noindex = False
        self.robots_nofollow = False
        self._chunks: list[str] = []
        self._md: list[str] = []
        self._skip_depth = 0
        self._in_title = False
        self._heading: str | None = None
        self._heading_text: list[str] = []
        self._href_stack: list[str] = []
        self._link_text: list[str] = []
        self._list_stack: list[str] = []
        self._pre_depth = 0

    # -- helpers ---------------------------------------------------------
    def _emit(self, text: str) -> None:
        self._chunks.append(text)
        self._md.append(text)

    def _newline(self, count: int = 1) -> None:
        self._chunks.append("\n" * count)
        self._md.append("\n" * count)

    # -- HTMLParser hooks ------------------------------------------------
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attr = {k.lower(): (v or "") for k, v in attrs}
        if tag in INVISIBLE_TAGS:
            self._skip_depth += 1
            return
        if self._skip_depth:
            return

        if tag == "html" and attr.get("lang"):
            self.lang = attr["lang"]
        elif tag == "title":
            self._in_title = True
        elif tag == "meta":
            name = (attr.get("name") or attr.get("property") or "").lower()
            content = attr.get("content", "")
            if name and content:
                self.meta.setdefault(name, content)
                if name == "robots":
                    lowered = content.lower()
                    self.robots_noindex = "noindex" in lowered
                    self.robots_nofollow = "nofollow" in lowered
        elif tag == "link":
            rel = (attr.get("rel") or "").lower()
            if "canonical" in rel and attr.get("href"):
                self.canonical = attr["href"]
        elif tag == "a":
            href = attr.get("href", "")
            self._href_stack.append(href)
            self._link_text = []
            if href:
                self._md.append("[")
            if href:
                self.links.append(
                    {"href": href, "rel": (attr.get("rel") or "").lower(), "text": ""}
                )
        elif tag == "img":
            alt = attr.get("alt", "").strip()
            src = attr.get("src") or attr.get("data-src") or ""
            if src:
                self.links.append({"href": src, "rel": "img", "text": alt})
            if alt:
                self._md.append(f"![{alt}]({src})")
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._heading = tag
            self._heading_text = []
            self._newline(2)
            self._md.append("#" * int(tag[1]) + " ")
        elif tag == "pre":
            self._pre_depth += 1
            self._newline(2)
            self._md.append("```\n")
        elif tag in ("strong", "b"):
            self._md.append("**")
        elif tag in ("em", "i"):
            self._md.append("*")
        elif tag == "code" and not self._pre_depth:
            self._md.append("`")
        elif tag in ("ul", "ol"):
            self._list_stack.append(tag)
            self._newline(2)
        elif tag == "li":
            self._newline()
            depth = max(len(self._list_stack) - 1, 0)
            bullet = "1. " if (self._list_stack or ["ul"])[-1] == "ol" else "- "
            self._chunks.append("  " * depth)
            self._md.append("  " * depth + bullet)
        elif tag == "br":
            self._newline()
        elif tag == "hr":
            self._newline(2)
            self._md.append("---")
            self._newline(2)
        elif tag in BLOCK_TAGS:
            self._newline(2)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in INVISIBLE_TAGS:
            self._skip_depth = max(0, self._skip_depth - 1)
            return
        if self._skip_depth:
            return

        if tag == "title":
            self._in_title = False
        elif tag == "a":
            href = self._href_stack.pop() if self._href_stack else ""
            if href:
                # Keeping the target in the markdown makes the export usable as
                # a link graph, not just prose.
                self._md.append(f"]({href})")
            text = "".join(self._link_text).strip()
            if self.links and text and not self.links[-1]["text"]:
                self.links[-1]["text"] = " ".join(text.split())[:200]
            self._link_text = []
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            text = " ".join("".join(self._heading_text).split())
            if text:
                self.headings.append({"level": tag, "text": text[:300]})
            self._heading = None
            self._heading_text = []
            self._newline(2)
        elif tag == "pre":
            self._pre_depth = max(0, self._pre_depth - 1)
            self._md.append("\n```")
            self._newline(2)
        elif tag in ("strong", "b"):
            self._md.append("**")
        elif tag in ("em", "i"):
            self._md.append("*")
        elif tag == "code" and not self._pre_depth:
            self._md.append("`")
        elif tag in ("ul", "ol"):
            if self._list_stack:
                self._list_stack.pop()
            self._newline(2)
        elif tag in BLOCK_TAGS:
            self._newline(2)

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        if self._in_title:
            self.title += data
            return
        if not data.strip() and "\n" in data:
            data = " "
        if self._heading is not None:
            self._heading_text.append(data)
        if self._href_stack:
            self._link_text.append(data)
        self._emit(data)


def collapse(text: str) -> str:
    """Collapse runaway whitespace while keeping paragraph breaks."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t\f\v]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def decode_body(body: bytes, content_type: str) -> str:
    """Decode using the charset from the header, then a meta tag, then UTF-8."""
    charset = ""
    match = re.search(r"charset=([\w.:+-]+)", content_type, re.I)
    if match:
        charset = match.group(1).strip("\"'")
    if not charset:
        match = re.search(rb"charset=[\"']?([\w.:+-]+)", body[:4096], re.I)
        if match:
            charset = match.group(1).decode("ascii", "ignore")
    for candidate in (charset, "utf-8", "cp1256", "latin-1"):
        if not candidate:
            continue
        try:
            return body.decode(candidate)
        except (LookupError, UnicodeDecodeError):
            continue
    return body.decode("utf-8", "replace")


# --------------------------------------------------------------------------
# Crawler
# --------------------------------------------------------------------------

class RateLimiter:
    """Enforces a minimum interval between requests across all worker threads."""

    def __init__(self, delay: float) -> None:
        self.delay = delay
        self._lock = threading.Lock()
        self._next = 0.0

    def wait(self) -> None:
        if self.delay <= 0:
            return
        with self._lock:
            now = time.monotonic()
            sleep_for = max(0.0, self._next - now)
            self._next = max(now, self._next) + self.delay
        if sleep_for:
            time.sleep(sleep_for)


class Crawler:
    def __init__(self, args: argparse.Namespace) -> None:
        start = normalize_url(args.start_url)
        if not start:
            raise SystemExit(f"Not a crawlable http(s) URL: {args.start_url}")
        self.start_url = start
        self.args = args
        self.out = os.path.abspath(args.out)
        self.site = registrable(urllib.parse.urlsplit(start).hostname or "")
        self.extra_hosts = {registrable(h) for h in args.allow_host}
        self.limiter = RateLimiter(args.delay)
        self.lock = threading.Lock()
        self.queue: deque[tuple[str, int, str]] = deque()
        self.seen: set[str] = set()
        self.pages: dict[str, dict] = {}
        self.assets: dict[str, dict] = {}
        self.errors: list[dict] = []
        self.used_paths: dict[str, str] = {}
        self.skipped: dict[str, str] = {}
        self.content_hashes: dict[str, str] = {}
        self.stop = threading.Event()
        self.robots: urllib.robotparser.RobotFileParser | None = None
        self.include_re = re.compile(args.include) if args.include else None
        self.exclude_re = re.compile(args.exclude) if args.exclude else None
        for sub in ("raw", "text", "markdown"):
            os.makedirs(os.path.join(self.out, sub), exist_ok=True)

    # -- persistence -----------------------------------------------------
    @property
    def state_path(self) -> str:
        return os.path.join(self.out, "crawl_state.json")

    def load_state(self) -> bool:
        for name, target in (("pages.jsonl", self.pages), ("assets.jsonl", self.assets)):
            path = os.path.join(self.out, name)
            if os.path.exists(path):
                with open(path, encoding="utf-8") as handle:
                    for line in handle:
                        line = line.strip()
                        if line:
                            record = json.loads(line)
                            target[record["url"]] = record
        for record in self.pages.values():
            self.used_paths[record["raw_path"]] = record["url"]
            if not record.get("duplicate_of"):
                self.content_hashes.setdefault(record["content_sha256"], record["url"])
        if not os.path.exists(self.state_path):
            return False
        with open(self.state_path, encoding="utf-8") as handle:
            state = json.load(handle)
        self.seen = set(state.get("seen", []))
        self.skipped = state.get("skipped", {})
        self.queue = deque(tuple(item) for item in state.get("queue", []))
        self.errors = state.get("errors", [])
        return True

    def save_state(self) -> None:
        with self.lock:
            state = {
                "start_url": self.start_url,
                "site": self.site,
                "seen": sorted(self.seen),
                "queue": [list(item) for item in self.queue],
                "errors": self.errors[-500:],
                "skipped": dict(self.skipped),
                "saved_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            }
            pages = list(self.pages.values())
            assets = list(self.assets.values())
        self._write_json(self.state_path, state)
        self._write_jsonl(os.path.join(self.out, "pages.jsonl"), pages)
        self._write_jsonl(os.path.join(self.out, "assets.jsonl"), assets)

    @staticmethod
    def _write_json(path: str, payload: object) -> None:
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
        os.replace(tmp, path)

    @staticmethod
    def _write_jsonl(path: str, records: Iterable[dict]) -> None:
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as handle:
            for record in records:
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        os.replace(tmp, path)

    # -- policy ----------------------------------------------------------
    def in_scope(self, url: str) -> bool:
        host = registrable(urllib.parse.urlsplit(url).hostname or "")
        if host != self.site and host not in self.extra_hosts:
            return False
        if self.include_re and not self.include_re.search(url):
            return False
        if self.exclude_re and self.exclude_re.search(url):
            return False
        return True

    def allowed_by_robots(self, url: str) -> bool:
        if self.args.ignore_robots or self.robots is None:
            return True
        try:
            return self.robots.can_fetch(self.args.user_agent, url)
        except Exception:
            return True

    def load_robots(self) -> list[str]:
        """Read robots.txt for crawl rules and sitemap hints."""
        parts = urllib.parse.urlsplit(self.start_url)
        robots_url = f"{parts.scheme}://{parts.netloc}/robots.txt"
        parser = urllib.robotparser.RobotFileParser()
        parser.set_url(robots_url)
        try:
            body, _, _, _ = self.fetch(robots_url)
            text = body.decode("utf-8", "replace")
            parser.parse(text.splitlines())
            self.robots = parser
            delay = None
            try:
                delay = parser.crawl_delay(self.args.user_agent)
            except Exception:
                delay = None
            if delay and float(delay) > self.limiter.delay:
                self.limiter.delay = float(delay)
                log(f"robots.txt requests Crawl-delay {delay}s; honoring it")
            sitemaps = re.findall(r"(?im)^\s*sitemap:\s*(\S+)", text)
            log(f"robots.txt loaded ({len(text.splitlines())} lines, "
                f"{len(sitemaps)} sitemap hints)")
            return sitemaps
        except Exception as exc:  # noqa: BLE001 - a missing robots.txt is normal
            log(f"robots.txt unavailable ({exc}); proceeding without crawl rules")
            return []

    def discover_sitemaps(self, hints: list[str]) -> list[str]:
        """Expand sitemap(s), following sitemap-index files one level deep."""
        parts = urllib.parse.urlsplit(self.start_url)
        root = f"{parts.scheme}://{parts.netloc}"
        pending = deque(hints or [])
        for guess in ("/sitemap.xml", "/sitemap_index.xml", "/sitemap-index.xml"):
            pending.append(root + guess)
        found: list[str] = []
        visited: set[str] = set()
        while pending and len(visited) < 50:
            sitemap_url = normalize_url(pending.popleft())
            if not sitemap_url or sitemap_url in visited:
                continue
            visited.add(sitemap_url)
            try:
                body, _, ctype, status = self.fetch(sitemap_url)
                if status != 200 or not body:
                    continue
                if sitemap_url.endswith(".gz"):
                    body = gzip.decompress(body)
                root_el = ET.fromstring(body)
            except Exception:
                continue
            tag = root_el.tag.split("}")[-1]
            locs = [
                (el.text or "").strip()
                for el in root_el.iter()
                if el.tag.split("}")[-1] == "loc" and el.text
            ]
            if tag == "sitemapindex":
                pending.extend(locs)
            else:
                found.extend(locs)
            log(f"sitemap {sitemap_url}: {len(locs)} entries ({tag})")
        return found

    # -- network ---------------------------------------------------------
    def fetch(self, url: str) -> tuple[bytes, dict, str, int]:
        """Fetch a URL, returning (body, headers, content_type, status)."""
        self.limiter.wait()
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": self.args.user_agent,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": self.args.accept_language,
                "Accept-Encoding": "gzip, deflate",
            },
        )
        last_error: Exception | None = None
        for attempt in range(self.args.retries + 1):
            try:
                with urllib.request.urlopen(request, timeout=self.args.timeout) as resp:
                    raw = resp.read(self.args.max_bytes + 1)
                    headers = {k.lower(): v for k, v in resp.headers.items()}
                    encoding = headers.get("content-encoding", "").lower()
                    if encoding == "gzip":
                        raw = gzip.decompress(raw)
                    elif encoding == "deflate":
                        raw = zlib.decompress(raw, -zlib.MAX_WBITS)
                    return (
                        raw,
                        headers,
                        headers.get("content-type", ""),
                        resp.status,
                    )
            except urllib.error.HTTPError as exc:
                # 4xx are final; 429/5xx are worth a backoff retry.
                if exc.code not in (429, 500, 502, 503, 504) or attempt == self.args.retries:
                    raise
                last_error = exc
            except Exception as exc:  # noqa: BLE001 - transient network failures
                if attempt == self.args.retries:
                    raise
                last_error = exc
            time.sleep(min(2 ** attempt, 10))
        raise last_error or RuntimeError("fetch failed")

    # -- crawl -----------------------------------------------------------
    def enqueue(self, url: str, depth: int, source: str) -> None:
        with self.lock:
            if url in self.seen:
                return
            self.seen.add(url)
            self.queue.append((url, depth, source))

    def process(self, url: str, depth: int, source: str) -> None:
        if self.stop.is_set():
            return
        if not self.allowed_by_robots(url):
            with self.lock:
                self.skipped[url] = "disallowed by robots.txt"
            log(f"skip (robots.txt) {url}")
            return
        try:
            body, headers, content_type, status = self.fetch(url)
        except urllib.error.HTTPError as exc:
            self.record_error(url, source, f"HTTP {exc.code} {exc.reason}")
            return
        except Exception as exc:  # noqa: BLE001
            self.record_error(url, source, f"{type(exc).__name__}: {exc}")
            return

        base_type = content_type.split(";")[0].strip().lower()
        if base_type not in HTML_TYPES:
            self.record_asset(url, source, base_type, len(body), headers)
            if self.args.include_assets:
                path = os.path.join(self.out, "raw", url_to_path(url, ""))
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "wb") as handle:
                    handle.write(body)
            return

        html = decode_body(body, content_type)
        parser = PageParser()
        try:
            parser.feed(html)
            parser.close()
        except Exception as exc:  # noqa: BLE001 - malformed markup still yields text
            log(f"parse warning for {url}: {exc}")

        text = collapse("".join(parser._chunks))
        markdown = collapse("".join(parser._md))
        title = " ".join(parser.title.split())

        digest = hashlib.sha256(body).hexdigest()
        with self.lock:
            original = self.content_hashes.get(digest)
            if original is None:
                self.content_hashes[digest] = url
        if original is not None and original != url:
            # Same bytes under another URL (e.g. "/" and "/index.html"). Record
            # the alias, but do not duplicate files or re-walk identical links.
            with self.lock:
                self.pages[url] = {
                    "url": url,
                    "status": status,
                    "title": title,
                    "duplicate_of": original,
                    "depth": depth,
                    "discovered_from": source,
                    "content_sha256": digest,
                    "word_count": 0,
                    "text": "",
                    "links_internal": [],
                    "links_external": [],
                    "raw_path": "",
                    "text_path": "",
                    "markdown_path": "",
                    "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                }
            log(f"duplicate of {original}  {url}")
            return

        raw_rel, text_rel, md_rel = self.reserve_paths(url)
        header = f"<!-- source: {url} -->\n\n"
        if title and not markdown.lstrip().startswith("#"):
            header += f"# {title}\n\n"
        self.write_file(os.path.join(self.out, "raw", raw_rel), html)
        self.write_file(os.path.join(self.out, "text", text_rel), text)
        self.write_file(os.path.join(self.out, "markdown", md_rel), header + markdown + "\n")

        internal: list[str] = []
        external: list[str] = []
        for link in parser.links:
            if link["rel"] == "img":
                continue
            target = normalize_url(link["href"], url)
            if not target:
                continue
            (internal if self.in_scope(target) else external).append(target)

        record = {
            "url": url,
            "final_url": url,
            "status": status,
            "title": title,
            "description": parser.meta.get("description")
            or parser.meta.get("og:description", ""),
            "lang": parser.lang or parser.meta.get("og:locale", ""),
            "canonical": normalize_url(parser.canonical, url) if parser.canonical else "",
            "depth": depth,
            "discovered_from": source,
            "headings": parser.headings,
            "meta": parser.meta,
            "text": text,
            "word_count": len(text.split()),
            "links_internal": sorted(set(internal)),
            "links_external": sorted(set(external)),
            "noindex": parser.robots_noindex,
            "content_type": base_type,
            "content_sha256": digest,
            "duplicate_of": "",
            "bytes": len(body),
            "raw_path": os.path.join("raw", raw_rel),
            "text_path": os.path.join("text", text_rel),
            "markdown_path": os.path.join("markdown", md_rel),
            "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        with self.lock:
            self.pages[url] = record
            count = len(self.pages)
        log(f"[{count}] {status} d{depth} {record['word_count']:>5}w  {url}")

        if self.args.max_pages and count >= self.args.max_pages:
            self.stop.set()
            return
        if depth >= self.args.max_depth or parser.robots_nofollow:
            return
        for target in internal:
            self.enqueue(target, depth + 1, url)

    def record_error(self, url: str, source: str, message: str) -> None:
        with self.lock:
            self.errors.append(
                {"url": url, "discovered_from": source, "error": message}
            )
        log(f"error {message}  {url}")

    def record_asset(
        self, url: str, source: str, content_type: str, size: int, headers: dict
    ) -> None:
        with self.lock:
            self.assets[url] = {
                "url": url,
                "discovered_from": source,
                "content_type": content_type,
                "bytes": size,
                "last_modified": headers.get("last-modified", ""),
                "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            }

    def reserve_paths(self, url: str) -> tuple[str, str, str]:
        """Claim raw/text/markdown paths for a URL, disambiguating collisions.

        Distinct URLs can map to the same natural path (``/foo`` and
        ``/foo.html``), which would otherwise silently overwrite each other.
        """
        with self.lock:
            candidate = url_to_path(url, ".html")
            owner = self.used_paths.get(candidate)
            if owner is not None and owner != url:
                digest = hashlib.sha1(url.encode()).hexdigest()[:8]
                stem = candidate[: -len(".html")]
                candidate = f"{stem}__{digest}.html"
            self.used_paths[candidate] = url
        stem = candidate[: -len(".html")]
        return candidate, stem + ".txt", stem + ".md"

    @staticmethod
    def write_file(path: str, content: str) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(content)

    def run(self) -> dict:
        started = time.time()
        resumed = self.args.resume and self.load_state()
        sitemap_hints = [] if self.args.ignore_robots else self.load_robots()
        if resumed:
            log(f"resuming: {len(self.pages)} pages already stored, "
                f"{len(self.queue)} URLs queued")
        else:
            self.enqueue(self.start_url, 0, "seed")
            if not self.args.no_sitemap:
                for loc in self.discover_sitemaps(sitemap_hints):
                    target = normalize_url(loc)
                    if target and self.in_scope(target):
                        self.enqueue(target, 0, "sitemap")
            log(f"frontier seeded with {len(self.queue)} URLs")

        def worker() -> None:
            while not self.stop.is_set():
                with self.lock:
                    if not self.queue:
                        break
                    url, depth, source = self.queue.popleft()
                self.process(url, depth, source)

        try:
            while not self.stop.is_set():
                with self.lock:
                    pending = len(self.queue)
                if not pending:
                    break
                with ThreadPoolExecutor(max_workers=self.args.concurrency) as pool:
                    futures = [pool.submit(worker) for _ in range(self.args.concurrency)]
                    for future in futures:
                        future.result()
                self.save_state()
        except KeyboardInterrupt:
            self.stop.set()
            log("interrupted — saving state so --resume can continue")

        self.save_state()
        report = {
            "start_url": self.start_url,
            "site": self.site,
            "pages": len(self.pages),
            "assets": len(self.assets),
            "errors": len(self.errors),
            "queued_remaining": len(self.queue),
            "total_words": sum(p["word_count"] for p in self.pages.values()),
            "elapsed_seconds": round(time.time() - started, 1),
            "finished_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "output_dir": self.out,
        }
        self._write_json(os.path.join(self.out, "crawl_report.json"), report)
        return report


def _allow_broken_pipe() -> None:
    """Exit quietly when output is piped into head, less, and friends."""
    try:
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (AttributeError, ValueError):  # not POSIX, or not main thread
        pass


def log(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Crawl a website into a local, queryable corpus.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("start_url", help="URL to start from, e.g. https://www.example.com")
    parser.add_argument("--out", default="data/site", help="output directory")
    parser.add_argument("--max-pages", type=int, default=1000, help="0 for no limit")
    parser.add_argument("--max-depth", type=int, default=10, help="link depth from seed")
    parser.add_argument("--delay", type=float, default=1.0,
                        help="minimum seconds between requests (politeness)")
    parser.add_argument("--concurrency", type=int, default=4, help="worker threads")
    parser.add_argument("--timeout", type=float, default=30.0, help="per-request timeout")
    parser.add_argument("--retries", type=int, default=2,
                        help="retries for 429/5xx and network errors")
    parser.add_argument("--max-bytes", type=int, default=10_000_000,
                        help="maximum response size to read")
    parser.add_argument("--user-agent", default=DEFAULT_UA)
    parser.add_argument("--accept-language", default="en,ar;q=0.9")
    parser.add_argument("--allow-host", action="append", default=[],
                        help="extra host to treat as in-scope (repeatable)")
    parser.add_argument("--include", help="only crawl URLs matching this regex")
    parser.add_argument("--exclude", help="skip URLs matching this regex")
    parser.add_argument("--include-assets", action="store_true",
                        help="also download non-HTML files (PDFs, images, ...)")
    parser.add_argument("--no-sitemap", action="store_true",
                        help="do not seed the frontier from sitemap.xml")
    parser.add_argument("--ignore-robots", action="store_true",
                        help="do not apply robots.txt rules (only for sites you own)")
    parser.add_argument("--resume", action="store_true",
                        help="continue a previous crawl in --out")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    _allow_broken_pipe()
    crawler = Crawler(args)

    def handle_signal(signum, frame):  # noqa: ANN001, ARG001
        crawler.stop.set()

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            signal.signal(sig, handle_signal)
        except ValueError:
            pass

    report = crawler.run()
    log("")
    log(f"done: {report['pages']} pages, {report['assets']} assets, "
        f"{report['errors']} errors, {report['total_words']} words "
        f"in {report['elapsed_seconds']}s")
    log(f"corpus: {report['output_dir']}")
    log(f"query it: scripts/query_site.py --data {report['output_dir']} --stats")
    return 0 if report["pages"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
