# Website scraper — full-site archive you can search and query

Two standard-library Python scripts (no `pip install`, Python 3.9+):

| Script | Purpose |
| --- | --- |
| `scripts/scrape_site.py` | Crawl a whole site into a local corpus |
| `scripts/query_site.py`  | Search, read and export that corpus |

## Quick start

```bash
# 1. Crawl the site (polite defaults: 1 request/second, obeys robots.txt)
scripts/scrape_site.py https://www.zagzoog.com --out data/zagzoog

# 2. See what you got
scripts/query_site.py --data data/zagzoog --stats
scripts/query_site.py --data data/zagzoog --tree

# 3. Interact with it
scripts/query_site.py --data data/zagzoog --search "contact address"
scripts/query_site.py --data data/zagzoog --show 4 --markdown
scripts/query_site.py --data data/zagzoog --links https://www.zagzoog.com/about

# 4. Turn the whole site into one document (e.g. to upload to NotebookLM)
scripts/query_site.py --data data/zagzoog --export zagzoog-corpus.md
```

## What the crawl produces

```
data/zagzoog/
├── pages.jsonl        one JSON record per page — the searchable corpus
├── assets.jsonl       every non-HTML resource seen (PDFs, images, ...)
├── raw/               byte-for-byte HTML mirror
├── text/              extracted plain text (scripts, styles and SVG removed)
├── markdown/          markdown rendering of each page
├── crawl_state.json   visited set + frontier, so --resume can continue
└── crawl_report.json  summary of the last run
```

Each record in `pages.jsonl` carries: `url`, `title`, `description`, `lang`,
`canonical`, `depth`, `discovered_from`, `headings`, `meta`, `text`,
`word_count`, `links_internal`, `links_external`, `status`, `content_sha256`,
`fetched_at`, and the paths of the raw/text/markdown files.

## How the crawler behaves

- **Scope** — stays on the start host, treating `example.com` and
  `www.example.com` as one site. Add more with `--allow-host`, or narrow with
  `--include` / `--exclude` regexes.
- **Discovery** — breadth-first from the start URL, plus every URL in
  `robots.txt` `Sitemap:` entries and `/sitemap.xml` (sitemap indexes are
  followed one level, which finds pages nothing links to).
- **robots.txt** — obeyed by default, including `Crawl-delay`. `--ignore-robots`
  exists for sites you own; the default stays polite.
- **Politeness** — `--delay` (default 1.0s) is a hard minimum between requests
  across all threads, so `--concurrency` only overlaps latency, never the rate.
- **Duplicates** — pages with identical bytes under different URLs (`/` and
  `/index.html`) are stored once; the other URL is kept as an alias.
- **Resilience** — retries 429/5xx with backoff, resumable via `--resume`, and
  Ctrl-C saves state before exiting.
- **Encoding** — honours the HTTP charset, then the `<meta>` charset, so Arabic
  and other non-Latin pages come out correctly.

Useful flags: `--max-pages` (default 1000, `0` = unlimited), `--max-depth`,
`--include-assets` to also download PDFs and images, `--no-sitemap`,
`--user-agent`. Run `scripts/scrape_site.py --help` for the full list.

## Querying the corpus

| Command | What it does |
| --- | --- |
| `--stats` | pages, words, languages, depth spread, top outbound domains |
| `--list` | every page as `url <tab> title` |
| `--tree` | the URL structure as a tree |
| `--search "terms"` | BM25-ranked full-text search with snippets (English + Arabic) |
| `--show URL\|N` | print one page; add `--markdown` for the markdown version |
| `--links URL\|N` | inbound and outbound links for one page |
| `--broken` | internal links that were never captured, split into failed / policy-skipped / not-crawled |
| `--export FILE.md` | the whole site as a single markdown document |

Pages can be addressed by list index, full URL, or any unique substring of a
URL. Add `--json` to `--list` and `--search` for machine-readable output.

## Re-crawling

`--resume` continues an interrupted crawl in the same directory. To take a
fresh snapshot instead, crawl into a new dated directory
(`--out data/zagzoog-2026-08-19`) and keep the old one for comparison.

## Network access note

Crawling requires outbound HTTPS to the target host. In sandboxed environments
(including Claude Code on the web) egress may be restricted by policy, in which
case requests fail before they leave the machine. Run the scraper from a
machine with normal internet access, or have the target domain allowed in the
environment's egress policy.

## Courtesy and legality

Scrape sites you own or have permission to archive. The defaults — obeying
`robots.txt`, one request per second, an identifying User-Agent — are there to
keep the crawl from burdening the target server. Raising `--concurrency` or
lowering `--delay` on someone else's site is impolite and may get you blocked.
