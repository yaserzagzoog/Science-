#!/usr/bin/env python3
"""Search and read a corpus produced by scripts/scrape_site.py.

Standard library only. Reads <data>/pages.jsonl and gives you a few ways to
interact with the scraped site:

    --stats                overview: pages, words, languages, depth, top pages
    --list                 every page as "url  <tab>  title"
    --tree                 the site's URL structure as a tree
    --search "terms"       TF-IDF ranked full-text search with snippets
    --show URL|N           print one page (text by default, --markdown for md)
    --links URL|N          inbound and outbound links for one page
    --export FILE.md       whole site as one markdown file (e.g. for NotebookLM)
    --broken               pages that link to URLs the crawl never captured

Examples
--------
    scripts/query_site.py --data data/zagzoog --stats
    scripts/query_site.py --data data/zagzoog --search "contact address"
    scripts/query_site.py --data data/zagzoog --show 3 --markdown
    scripts/query_site.py --data data/zagzoog --export zagzoog-corpus.md
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import signal
import sys
import urllib.parse
from collections import Counter, defaultdict

WORD_RE = re.compile(r"[\w؀-ۿ]+", re.UNICODE)
# Very common words carry no signal; dropping them sharpens ranking. Arabic
# stop words are included because the site may be bilingual.
STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has", "have",
    "he", "in", "is", "it", "its", "of", "on", "or", "that", "the", "this", "to",
    "was", "were", "will", "with", "you", "your", "we", "our",
    "في", "من", "على", "الى", "إلى", "عن", "مع", "هذا", "هذه", "التي", "الذي", "و",
}


def tokenize(text: str) -> list[str]:
    return [w for w in (m.group(0).lower() for m in WORD_RE.finditer(text)) if w]


def load_pages(data_dir: str) -> list[dict]:
    path = os.path.join(data_dir, "pages.jsonl")
    if not os.path.exists(path):
        raise SystemExit(
            f"No corpus at {path}\n"
            f"Run: scripts/scrape_site.py <url> --out {data_dir}"
        )
    pages = []
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                pages.append(json.loads(line))
    pages.sort(key=lambda p: (p.get("depth", 0), p["url"]))
    return pages


def split_aliases(pages: list[dict]) -> tuple[list[dict], list[dict]]:
    """Separate real documents from URLs that duplicate another page's bytes."""
    unique = [p for p in pages if not p.get("duplicate_of")]
    aliases = [p for p in pages if p.get("duplicate_of")]
    return unique, aliases


def resolve(pages: list[dict], target: str) -> dict:
    """Accept a list index, a full URL, or a unique substring of a URL."""
    if target.isdigit():
        index = int(target)
        if 0 <= index < len(pages):
            return pages[index]
        raise SystemExit(f"Index {index} out of range (0-{len(pages) - 1})")
    for page in pages:
        if page["url"] == target or page["url"].rstrip("/") == target.rstrip("/"):
            return page
    matches = [p for p in pages if target.lower() in p["url"].lower()]
    if len(matches) == 1:
        return matches[0]
    if not matches:
        raise SystemExit(f"No page matching {target!r}")
    listing = "\n".join(f"  {p['url']}" for p in matches[:10])
    raise SystemExit(f"{len(matches)} pages match {target!r}:\n{listing}")


# --------------------------------------------------------------------------
# Commands
# --------------------------------------------------------------------------

def cmd_stats(pages: list[dict], aliases: list[dict], data_dir: str) -> None:
    words = sum(p.get("word_count", 0) for p in pages)
    langs = Counter(p.get("lang", "").split("-")[0] or "?" for p in pages)
    depths = Counter(p.get("depth", 0) for p in pages)
    hosts = Counter(urllib.parse.urlsplit(p["url"]).netloc for p in pages)
    external = Counter()
    for page in pages:
        for link in page.get("links_external", []):
            external[urllib.parse.urlsplit(link).netloc] += 1

    report_path = os.path.join(data_dir, "crawl_report.json")
    report = {}
    if os.path.exists(report_path):
        with open(report_path, encoding="utf-8") as handle:
            report = json.load(handle)

    print(f"corpus:      {os.path.abspath(data_dir)}")
    if report:
        print(f"crawled:     {report.get('finished_at', '?')} "
              f"in {report.get('elapsed_seconds', '?')}s")
        print(f"start url:   {report.get('start_url', '?')}")
        if report.get("queued_remaining"):
            print(f"UNFINISHED:  {report['queued_remaining']} URLs still queued "
                  f"(re-run with --resume)")
    print(f"pages:       {len(pages)} unique"
          + (f" (+{len(aliases)} duplicate URLs)" if aliases else ""))
    print(f"words:       {words:,}")
    print(f"assets:      {report.get('assets', '?')}   errors: {report.get('errors', '?')}")
    print(f"hosts:       " + ", ".join(f"{h} ({n})" for h, n in hosts.most_common()))
    print(f"languages:   " + ", ".join(f"{k} ({v})" for k, v in langs.most_common()))
    print(f"depth:       " + ", ".join(f"d{k}={v}" for k, v in sorted(depths.items())))
    if external:
        print("top outbound domains:")
        for host, count in external.most_common(10):
            print(f"  {count:>4}  {host}")
    print("\nlargest pages:")
    for page in sorted(pages, key=lambda p: -p.get("word_count", 0))[:10]:
        print(f"  {page.get('word_count', 0):>6}w  {page['url']}")


def cmd_list(pages: list[dict], limit: int, as_json: bool) -> None:
    limit = limit or len(pages)
    selected = pages[:limit] if limit else pages
    if as_json:
        print(json.dumps(
            [{"index": pages.index(p), "url": p["url"], "title": p.get("title", ""),
              "words": p.get("word_count", 0)} for p in selected],
            ensure_ascii=False, indent=2))
        return
    for index, page in enumerate(selected):
        print(f"{index:>4}  {page['url']}\t{page.get('title', '')}")


def cmd_tree(pages: list[dict]) -> None:
    tree: dict = {}
    for page in pages:
        parts = urllib.parse.urlsplit(page["url"])
        node = tree.setdefault(parts.netloc, {})
        for segment in [s for s in parts.path.split("/") if s] or ["/"]:
            node = node.setdefault(segment, {})
        node["__url__"] = page["url"]

    def walk(node: dict, prefix: str = "") -> None:
        keys = [k for k in node if k != "__url__"]
        for position, key in enumerate(sorted(keys)):
            last = position == len(keys) - 1
            print(f"{prefix}{'└── ' if last else '├── '}{key}")
            walk(node[key], prefix + ("    " if last else "│   "))

    walk(tree)


def build_index(pages: list[dict]) -> tuple[list[Counter], dict[str, float]]:
    """Term frequencies per page plus inverse document frequency per term."""
    term_freqs = []
    doc_freq: Counter = Counter()
    for page in pages:
        blob = " ".join([
            page.get("title", ""),
            page.get("description", ""),
            " ".join(h["text"] for h in page.get("headings", [])),
            page.get("text", ""),
        ])
        counts = Counter(tokenize(blob))
        term_freqs.append(counts)
        doc_freq.update(counts.keys())
    total = max(len(pages), 1)
    idf = {
        term: math.log(1 + (total - freq + 0.5) / (freq + 0.5))
        for term, freq in doc_freq.items()
    }
    return term_freqs, idf


def snippet(text: str, terms: list[str], width: int = 220) -> str:
    lowered = text.lower()
    best = -1
    for term in terms:
        position = lowered.find(term)
        if position != -1 and (best == -1 or position < best):
            best = position
    if best == -1:
        return " ".join(text.split())[:width]
    start = max(0, best - width // 3)
    excerpt = " ".join(text[start:start + width].split())
    prefix = "…" if start else ""
    return f"{prefix}{excerpt}…"


def cmd_search(pages: list[dict], query: str, limit: int, as_json: bool) -> None:
    terms = [t for t in tokenize(query) if t not in STOP_WORDS] or tokenize(query)
    if not terms:
        raise SystemExit("Empty query")
    term_freqs, idf = build_index(pages)
    lengths = [max(sum(tf.values()), 1) for tf in term_freqs]
    average = sum(lengths) / max(len(lengths), 1)

    scored = []
    for index, page in enumerate(pages):
        tf = term_freqs[index]
        score = 0.0
        matched = 0
        for term in terms:
            count = tf.get(term, 0)
            if not count:
                continue
            matched += 1
            # BM25 saturation so one long page cannot dominate on repetition.
            norm = count * 2.5 / (count + 1.5 * (0.25 + 0.75 * lengths[index] / average))
            score += idf.get(term, 0.0) * norm
        if not matched:
            continue
        title_terms = set(tokenize(page.get("title", "")))
        score *= 1 + 0.5 * len(title_terms & set(terms))  # title hits matter more
        score *= 1 + 0.25 * (matched / len(terms))        # reward covering the query
        scored.append((score, index, page))

    scored.sort(key=lambda item: -item[0])
    results = scored[:limit] if limit else scored

    if as_json:
        print(json.dumps(
            [{"score": round(s, 3), "index": i, "url": p["url"],
              "title": p.get("title", ""),
              "snippet": snippet(p.get("text", ""), terms)}
             for s, i, p in results],
            ensure_ascii=False, indent=2))
        return

    if not results:
        print(f"No matches for {query!r} across {len(pages)} pages.")
        return
    print(f"{len(scored)} matching pages for {query!r} (showing {len(results)})\n")
    for score, index, page in results:
        print(f"[{index}] {page.get('title') or '(untitled)'}   score={score:.2f}")
        print(f"     {page['url']}")
        print(f"     {snippet(page.get('text', ''), terms)}\n")


def cmd_show(pages: list[dict], target: str, data_dir: str, markdown: bool) -> None:
    page = resolve(pages, target)
    if page.get("duplicate_of"):
        print(f"# (duplicate of {page['duplicate_of']})")
        page = resolve(pages, page["duplicate_of"])
    key = "markdown_path" if markdown else "text_path"
    path = os.path.join(data_dir, page.get(key, ""))
    print(f"# {page.get('title', '')}")
    print(f"url:     {page['url']}")
    print(f"fetched: {page.get('fetched_at', '?')}   words: {page.get('word_count', 0)}")
    if page.get("description"):
        print(f"desc:    {page['description']}")
    print("-" * 78)
    if os.path.exists(path):
        with open(path, encoding="utf-8") as handle:
            print(handle.read())
    else:
        print(page.get("text", ""))


def cmd_links(pages: list[dict], target: str) -> None:
    page = resolve(pages, target)
    inbound = [p["url"] for p in pages if page["url"] in p.get("links_internal", [])]
    print(f"{page['url']}\n")
    print(f"inbound ({len(inbound)}):")
    for url in sorted(inbound):
        print(f"  <- {url}")
    print(f"\noutbound internal ({len(page.get('links_internal', []))}):")
    for url in page.get("links_internal", []):
        print(f"  -> {url}")
    print(f"\noutbound external ({len(page.get('links_external', []))}):")
    for url in page.get("links_external", []):
        print(f"  => {url}")


def cmd_broken(pages: list[dict], aliases: list[dict], data_dir: str) -> None:
    # A link counts as captured if it produced a page, a duplicate alias, or a
    # downloaded asset. Anything else is either an error or a deliberate skip.
    captured = {p["url"] for p in pages} | {p["url"] for p in aliases}
    assets_path = os.path.join(data_dir, "assets.jsonl")
    if os.path.exists(assets_path):
        with open(assets_path, encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    captured.add(json.loads(line)["url"])

    failed: dict[str, str] = {}
    skipped: dict[str, str] = {}
    state_path = os.path.join(data_dir, "crawl_state.json")
    if os.path.exists(state_path):
        with open(state_path, encoding="utf-8") as handle:
            state = json.load(handle)
        for entry in state.get("errors", []):
            failed[entry["url"]] = entry["error"]
        skipped = state.get("skipped", {})

    referrers: dict[str, list[str]] = defaultdict(list)
    for page in pages:
        for link in page.get("links_internal", []):
            if link not in captured:
                referrers[link].append(page["url"])
    if not referrers:
        print("Every internal link resolves to a captured page or asset.")
        return

    broken = {u: r for u, r in referrers.items() if u in failed}
    blocked = {u: r for u, r in referrers.items() if u in skipped}
    uncrawled = {u: r for u, r in referrers.items()
                 if u not in failed and u not in skipped}

    def report(title: str, group: dict[str, list[str]], reason) -> None:
        if not group:
            return
        print(f"{title} ({len(group)}):\n")
        for url, sources in sorted(group.items()):
            print(f"{url}\n    reason: {reason(url)}")
            for source in sources[:5]:
                print(f"    linked from: {source}")
            if len(sources) > 5:
                print(f"    ... and {len(sources) - 5} more")
            print()

    report("BROKEN — request failed", broken, lambda u: failed[u])
    report("SKIPPED — excluded by crawl policy", blocked, lambda u: skipped[u])
    report("NOT CRAWLED — still queued, or cut off by a limit/filter", uncrawled,
           lambda u: "not fetched (page limit, depth limit, or --include/--exclude)")


def cmd_export(pages: list[dict], data_dir: str, out_path: str) -> None:
    with open(out_path, "w", encoding="utf-8") as handle:
        host = urllib.parse.urlsplit(pages[0]["url"]).netloc if pages else "site"
        handle.write(f"# {host} — full site archive\n\n")
        handle.write(f"{len(pages)} pages, "
                     f"{sum(p.get('word_count', 0) for p in pages):,} words.\n\n")
        handle.write("## Contents\n\n")
        for index, page in enumerate(pages):
            handle.write(f"{index + 1}. {page.get('title') or page['url']}\n")
        handle.write("\n---\n\n")
        for page in pages:
            handle.write(f"## {page.get('title') or page['url']}\n\n")
            handle.write(f"Source: {page['url']}\n\n")
            md_path = os.path.join(data_dir, page.get("markdown_path", ""))
            if os.path.exists(md_path):
                with open(md_path, encoding="utf-8") as source:
                    body = source.read()
                # The per-page file repeats the title as an H1; drop it here.
                body = re.sub(r"\A(<!-- source:.*?-->\s*)?(# .*?\n)?\s*", "", body,
                              count=1, flags=re.S)
                handle.write(body.strip() + "\n\n")
            else:
                handle.write(page.get("text", "").strip() + "\n\n")
            handle.write("---\n\n")
    size = os.path.getsize(out_path)
    print(f"Wrote {out_path} ({size:,} bytes, {len(pages)} pages)")


def _allow_broken_pipe() -> None:
    """Exit quietly when output is piped into head, less, and friends."""
    try:
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (AttributeError, ValueError):  # not POSIX, or not main thread
        pass


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Search and read a scraped site corpus.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--data", default="data/site", help="corpus directory")
    parser.add_argument("--limit", type=int, default=20,
                        help="max results to show; 0 for all")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument("--markdown", action="store_true",
                        help="with --show, print the markdown rendering")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--stats", action="store_true")
    group.add_argument("--list", action="store_true")
    group.add_argument("--tree", action="store_true")
    group.add_argument("--search", metavar="QUERY")
    group.add_argument("--show", metavar="URL|INDEX")
    group.add_argument("--links", metavar="URL|INDEX")
    group.add_argument("--broken", action="store_true")
    group.add_argument("--export", metavar="FILE.md")
    args = parser.parse_args(argv)
    _allow_broken_pipe()

    pages, aliases = split_aliases(load_pages(args.data))
    if args.stats:
        cmd_stats(pages, aliases, args.data)
    elif args.list:
        cmd_list(pages, args.limit, args.json)
    elif args.tree:
        cmd_tree(pages)
    elif args.search:
        cmd_search(pages, args.search, args.limit, args.json)
    elif args.show:
        cmd_show(pages + aliases, args.show, args.data, args.markdown)
    elif args.links:
        cmd_links(pages + aliases, args.links)
    elif args.broken:
        cmd_broken(pages, aliases, args.data)
    elif args.export:
        cmd_export(pages, args.data, args.export)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
