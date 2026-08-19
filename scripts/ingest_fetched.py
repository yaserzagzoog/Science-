#!/usr/bin/env python3
"""Build a scrape_site.py-compatible corpus from externally fetched pages.

`scripts/scrape_site.py` fetches and parses in one pass. When the network path
has to be something else — a hosted extraction/crawl service, a browser export,
a colleague's `curl` dump — this script takes over from the fetch step: it reads
the fetched payloads, parses them with the same parser, and writes the same
corpus layout, so `scripts/query_site.py` works identically either way.

Input is a directory of JSON files shaped like

    {"content": "...", "title": "...", "description": "...", "url": "..."}

where `content` is HTML, Markdown, or plain text (auto-detected). Files that
are not JSON, or that carry no URL, are skipped and reported.

    scripts/ingest_fetched.py --results-dir ./fetched --out data/zagzoog

Two things it does that a plain converter would not:

* **Boilerplate removal.** Site chrome (nav, mega-menu, footer) repeats on
  every page and swamps full-text search. Lines appearing on more than
  `--boilerplate-threshold` of pages are dropped from the searchable text and
  kept in `boilerplate.txt` for inspection.
* **Product extraction.** E-commerce listing and product pages are also
  distilled into `products.jsonl` (sku, name, url, price, currency, category).
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import importlib.util
import json
import os
import re
import sys
import time
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))


def load_scraper_module():
    """Reuse the parser from scrape_site.py rather than duplicating it."""
    path = os.path.join(HERE, "scrape_site.py")
    spec = importlib.util.spec_from_file_location("scrape_site", path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["scrape_site"] = module
    spec.loader.exec_module(module)
    return module


SCRAPER = load_scraper_module()
PageParser = SCRAPER.PageParser
collapse = SCRAPER.collapse
normalize_url = SCRAPER.normalize_url
url_to_path = SCRAPER.url_to_path
registrable = SCRAPER.registrable

PRICE_RE = re.compile(r"([\d][\d,]*(?:\.\d+)?)")

# Fetched payloads often carry inlined CSS and framework bootstrap data (React
# Server Component streams, i18n dictionaries). It is not page content, and it
# swamps full-text search, so it is dropped before indexing.
# Swatch filenames spell brands inconsistently (ZTRUST, samsung-log, GlemGas).
BRAND_NAMES = {
    "ztrust": "Z Trust", "samsung": "Samsung", "lg": "LG", "ogeneral": "O General",
    "glemgas": "Glem Gas", "glem builtin": "Glem Builtin", "hisense": "Hisense",
    "hitachi": "Hitachi", "mabe": "Mabe", "philips": "Philips",
    "whirlpool": "Whirlpool",
}

NOISE_MARKERS = ("__next_f", "self.__next", "window.__NUXT", "__NEXT_DATA__",
                 "@font-face", "!function", "webpackChunk")


def denoise(text: str) -> str:
    """Drop inlined script/style payloads, keeping human-readable lines."""
    kept = []
    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped:
            kept.append(line)
            continue
        if any(marker in stripped for marker in NOISE_MARKERS):
            continue
        if stripped.count('\\"') > 2 or stripped.count('":"') > 2:
            continue
        # A CSS rule or minified blob: mostly punctuation, not prose.
        symbols = sum(1 for ch in stripped if not (ch.isalnum() or ch.isspace()))
        if len(stripped) > 120 and symbols / len(stripped) > 0.18:
            continue
        if re.match(r"^[.#:@\[][A-Za-z0-9_.\-\[\]()=\"\'\s,>:*]*\{", stripped):
            continue
        kept.append(line)
    return collapse("\n".join(kept))


def looks_like_html(text: str) -> bool:
    head = text[:4000].lower()
    return any(tag in head for tag in ("<div", "<p", "<html", "<body", "<a ", "<span"))


def read_payloads(results_dir: str) -> tuple[list[dict], list[str]]:
    """Load every JSON payload, keeping the largest capture per URL."""
    best: dict[str, dict] = {}
    skipped: list[str] = []
    for name in sorted(os.listdir(results_dir)):
        path = os.path.join(results_dir, name)
        if not os.path.isfile(path):
            continue
        try:
            with open(path, encoding="utf-8") as handle:
                payload = json.load(handle)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            skipped.append(f"{name}: not JSON ({exc.__class__.__name__})")
            continue
        if not isinstance(payload, dict):
            skipped.append(f"{name}: JSON is not an object")
            continue
        url = normalize_url(payload.get("url", ""))
        content = payload.get("content") or ""
        if not url:
            skipped.append(f"{name}: no usable url field")
            continue
        if not content.strip():
            skipped.append(f"{name}: empty content for {url}")
            continue
        payload["_source_file"] = name
        # The same URL may be captured several times (different drivers or
        # render waits); the richest capture wins.
        if url not in best or len(content) > len(best[url].get("content", "")):
            payload["url"] = url
            best[url] = payload
    return list(best.values()), skipped


def parse_payload(payload: dict) -> dict:
    """Turn one fetched payload into text, markdown, links and headings."""
    url = payload["url"]
    content = payload["content"]
    if looks_like_html(content):
        parser = PageParser()
        try:
            parser.feed(content)
            parser.close()
        except Exception:  # noqa: BLE001 - malformed markup still yields text
            pass
        text = collapse("".join(parser._chunks))
        markdown = collapse("".join(parser._md))
        title = " ".join(parser.title.split()) or payload.get("title", "")
        description = parser.meta.get("description") or payload.get("description", "")
        headings = parser.headings
        raw_links = [link["href"] for link in parser.links if link["rel"] != "img"]
        lang = parser.lang
    else:
        text = collapse(content)
        markdown = content.strip()
        title = payload.get("title", "")
        description = payload.get("description", "")
        headings = [
            {"level": f"h{min(len(m.group(1)), 6)}", "text": m.group(2).strip()}
            for m in re.finditer(r"(?m)^(#{1,6})\s+(.+)$", markdown)
        ]
        raw_links = re.findall(r"\]\((https?://[^)\s]+)\)", markdown)
        lang = ""

    if not title:
        for heading in headings:
            if heading["level"] in ("h1", "h2"):
                title = heading["text"]
                break

    return {
        "url": url,
        "title": title,
        "description": description,
        "lang": lang,
        "headings": headings,
        "text": text,
        "markdown": markdown,
        "raw_links": raw_links,
        "source_file": payload.get("_source_file", ""),
    }


def strip_boilerplate(parsed: list[dict], threshold: float) -> tuple[list[str], int]:
    """Drop lines that appear on most pages — nav, mega-menu, footer."""
    if len(parsed) < 3:
        return [], 0
    counts: collections.Counter = collections.Counter()
    for page in parsed:
        for line in set(page["text"].split("\n")):
            line = line.strip()
            if line:
                counts[line] += 1
    cutoff = max(2, int(len(parsed) * threshold))
    boilerplate = {line for line, count in counts.items() if count >= cutoff}
    removed = 0
    for page in parsed:
        kept = []
        for line in page["text"].split("\n"):
            if line.strip() in boilerplate:
                removed += 1
                continue
            kept.append(line)
        page["text"] = collapse("\n".join(kept))
    return sorted(boilerplate), removed


def extract_products(parsed: list[dict]) -> list[dict]:
    """Pull product records out of listing and detail pages.

    Cards render as an image link, then a category heading, a brand swatch and
    the titled product link, then the price block:

        [![Product](img)](/en/product-page/SKU/)
        ###### Air Conditioners
        ![Brand](.../swatch/ZTRUST.svg)
        ##### [Cool Window 21800 Btu](/en/product-page/SKU/)
        ![SAR](...)1,799Incl. VAT 2,600Save...
    """
    link_re = re.compile(
        r"\[([^\]\n]{0,140})\]\((?:https?://[^)\s]*)?(/(?:en|ar)/product-page/"
        r"([A-Za-z0-9._-]+)/?)\)"
    )
    products: dict[str, dict] = {}
    for page in parsed:
        markdown = page["markdown"]
        host = urllib.parse.urlsplit(page["url"]).netloc
        locale = "ar" if "/ar/" in page["url"] else "en"
        for match in link_re.finditer(markdown):
            label, path, sku = match.group(1).strip(), match.group(2), match.group(3)
            record = products.setdefault(sku, {
                "sku": sku, "name": "", "name_ar": "", "url": f"https://{host}{path}",
                "price_sar": "", "was_price_sar": "", "brand": "", "category": "",
                "seen_on": [],
            })
            # Image-only links carry no name; the titled link a few lines later
            # does. Keep the longest real label seen for this SKU.
            name = "" if label.startswith("!") else label
            key = "name_ar" if locale == "ar" else "name"
            if name and len(name) > len(record[key]) and not name.endswith("..."):
                record[key] = name
            elif name and not record[key]:
                record[key] = name

            window = markdown[match.end(): match.end() + 260]
            price = re.search(r"\)([\d][\d,]*)\s*Incl", window)
            if price and not record["price_sar"]:
                record["price_sar"] = price.group(1).replace(",", "")
            was = re.search(r"Incl\.\s*VAT\s*([\d][\d,]*)\s*Save", window)
            if was and not record["was_price_sar"]:
                record["was_price_sar"] = was.group(1).replace(",", "")

            before = markdown[max(0, match.start() - 420): match.start()]
            # Swatches are usually /media/attribute/swatch/NAME.svg, but some
            # are PNGs behind an image proxy with the path percent-encoded.
            brand = re.findall(
                r"swatch(?:/|%2F)(?:[^/%\s)]*(?:/|%2F))*?([A-Za-z0-9_.-]+?)"
                r"(?:-log[a-z]*)?\.(?:svg|png)", before, re.I)
            if brand and not record["brand"]:
                raw = brand[-1].replace("_", " ").strip()
                record["brand"] = BRAND_NAMES.get(raw.lower(), raw)
            cat = re.findall(r"#{4,6}\s*\[?\s*([A-Za-z][A-Za-z &/]{2,40}?)\s*\]?\s*\n",
                             before)
            if cat and not record["category"]:
                record["category"] = cat[-1].strip()
            if page["url"] not in record["seen_on"]:
                record["seen_on"].append(page["url"])
    return sorted(products.values(), key=lambda p: p["sku"])


def write_corpus(parsed: list[dict], out: str, source_note: str) -> dict:
    for sub in ("raw", "text", "markdown"):
        os.makedirs(os.path.join(out, sub), exist_ok=True)

    used: dict[str, str] = {}
    records = []
    seen_hashes: dict[str, str] = {}
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    for page in sorted(parsed, key=lambda p: p["url"]):
        url = page["url"]
        digest = hashlib.sha256(page["text"].encode("utf-8")).hexdigest()
        duplicate_of = ""
        if page["text"] and digest in seen_hashes and seen_hashes[digest] != url:
            duplicate_of = seen_hashes[digest]
        else:
            seen_hashes.setdefault(digest, url)

        candidate = url_to_path(url, ".html")
        if used.get(candidate, url) != url:
            candidate = (candidate[: -len(".html")]
                         + "__" + hashlib.sha1(url.encode()).hexdigest()[:8] + ".html")
        used[candidate] = url
        stem = candidate[: -len(".html")]
        text_rel, md_rel = stem + ".txt", stem + ".md"

        internal, external = [], []
        for href in page["raw_links"]:
            target = normalize_url(href, url)
            if not target:
                continue
            same = registrable(urllib.parse.urlsplit(target).hostname or "") == \
                registrable(urllib.parse.urlsplit(url).hostname or "")
            (internal if same else external).append(target)

        if not duplicate_of:
            for rel, body in ((text_rel, page["text"]),
                              (md_rel, page["markdown"])):
                dest = os.path.join(out, "text" if rel.endswith(".txt") else "markdown", rel)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                with open(dest, "w", encoding="utf-8") as handle:
                    handle.write(body)

        records.append({
            "url": url,
            "status": 200,
            "title": page["title"],
            "description": page["description"],
            "lang": page["lang"],
            "canonical": "",
            "depth": 0,
            "discovered_from": source_note,
            "headings": page["headings"],
            "meta": {},
            "text": "" if duplicate_of else page["text"],
            "word_count": 0 if duplicate_of else len(page["text"].split()),
            "links_internal": sorted(set(internal)),
            "links_external": sorted(set(external)),
            "noindex": False,
            "content_type": "text/html",
            "content_sha256": digest,
            "duplicate_of": duplicate_of,
            "bytes": len(page["markdown"].encode("utf-8")),
            "raw_path": "",
            "text_path": "" if duplicate_of else os.path.join("text", text_rel),
            "markdown_path": "" if duplicate_of else os.path.join("markdown", md_rel),
            "fetched_at": now,
            "source_file": page["source_file"],
        })

    with open(os.path.join(out, "pages.jsonl"), "w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    unique = [r for r in records if not r["duplicate_of"]]
    report = {
        "start_url": unique[0]["url"] if unique else "",
        "site": registrable(urllib.parse.urlsplit(unique[0]["url"]).hostname or "")
        if unique else "",
        "pages": len(unique),
        "duplicates": len(records) - len(unique),
        "assets": 0,
        "errors": 0,
        "queued_remaining": 0,
        "total_words": sum(r["word_count"] for r in records),
        "elapsed_seconds": 0,
        "finished_at": now,
        "output_dir": os.path.abspath(out),
        "ingested_from": source_note,
    }
    with open(os.path.join(out, "crawl_report.json"), "w", encoding="utf-8") as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2)
    # query_site.py --broken reads this file; write a minimal, honest one.
    with open(os.path.join(out, "crawl_state.json"), "w", encoding="utf-8") as handle:
        json.dump({"seen": [r["url"] for r in records], "queue": [],
                   "errors": [], "skipped": {}}, handle, ensure_ascii=False, indent=2)
    open(os.path.join(out, "assets.jsonl"), "a", encoding="utf-8").close()
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build a corpus from externally fetched page payloads.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--results-dir", required=True,
                        help="directory of JSON payloads to ingest")
    parser.add_argument("--out", default="data/site", help="corpus directory to write")
    parser.add_argument("--source-note", default="external-fetch",
                        help="recorded as discovered_from on every page")
    parser.add_argument("--boilerplate-threshold", type=float, default=0.6,
                        help="drop lines appearing on this fraction of pages (0 disables)")
    args = parser.parse_args(argv)

    payloads, skipped = read_payloads(args.results_dir)
    if not payloads:
        raise SystemExit(f"No usable payloads in {args.results_dir}")
    parsed = [parse_payload(p) for p in payloads]
    for page in parsed:
        page["text"] = denoise(page["text"])
        page["markdown"] = denoise(page["markdown"])

    boilerplate, removed = ([], 0)
    if args.boilerplate_threshold > 0:
        boilerplate, removed = strip_boilerplate(parsed, args.boilerplate_threshold)

    products = extract_products(parsed)
    os.makedirs(args.out, exist_ok=True)
    if boilerplate:
        with open(os.path.join(args.out, "boilerplate.txt"), "w", encoding="utf-8") as h:
            h.write("\n".join(boilerplate))
    if products:
        with open(os.path.join(args.out, "products.jsonl"), "w", encoding="utf-8") as h:
            for product in products:
                h.write(json.dumps(product, ensure_ascii=False) + "\n")

    report = write_corpus(parsed, args.out, args.source_note)

    print(f"ingested {len(payloads)} payloads -> {report['pages']} pages "
          f"({report['duplicates']} duplicates), {report['total_words']:,} words")
    if boilerplate:
        print(f"boilerplate: {len(boilerplate)} repeated lines removed "
              f"({removed} line instances) -> {args.out}/boilerplate.txt")
    if products:
        priced = sum(1 for p in products if p["price_sar"])
        print(f"products:    {len(products)} distinct SKUs ({priced} with a price) "
              f"-> {args.out}/products.jsonl")
    for note in skipped:
        print(f"skipped {note}", file=sys.stderr)
    print(f"corpus:      {report['output_dir']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
