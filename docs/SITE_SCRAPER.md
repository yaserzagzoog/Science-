# Website scraper — full-site archive you can search and query

Two standard-library Python scripts (no `pip install`, Python 3.9+):

| Script | Purpose |
| --- | --- |
| `scripts/scrape_site.py` | Crawl a whole site into a local corpus |
| `scripts/ingest_fetched.py` | Build the same corpus from pages fetched elsewhere |
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
| `--products [QUERY]` | the extracted product catalog, optionally filtered |

Pages can be addressed by list index, full URL, or any unique substring of a
URL. Add `--json` to `--list` and `--search` for machine-readable output.

## Re-crawling

`--resume` continues an interrupted crawl in the same directory. To take a
fresh snapshot instead, crawl into a new dated directory
(`--out data/zagzoog-2026-08-19`) and keep the old one for comparison.

## When the crawler cannot reach the site

Crawling needs outbound HTTPS to the target host. In sandboxed environments
(including Claude Code on the web) egress may be blocked by policy, and the
request fails before it leaves the machine. It is also of no use against a
JavaScript app that renders its content client-side — `scrape_site.py` reads
HTML, it does not run scripts.

For both cases `scripts/ingest_fetched.py` separates *fetching* from
*parsing*. Fetch the pages by whatever means works — a hosted extraction
service, a headless browser, a colleague running `curl` — save each one as a
JSON file shaped like

```json
{"url": "https://example.com/page", "content": "<html>…</html>",
 "title": "optional", "description": "optional"}
```

then build the normal corpus from that directory:

```bash
scripts/ingest_fetched.py --results-dir ./fetched --out data/example
scripts/query_site.py --data data/example --stats   # identical from here on
```

`content` may be HTML, Markdown or plain text; the format is detected. The
same URL captured several times keeps the richest copy. Beyond parsing, the
ingest does three things worth knowing about:

- **Noise removal** — inlined CSS and framework bootstrap payloads (React
  Server Component streams, i18n dictionaries) are dropped. Left in, they can
  outweigh the real text by five to one and wreck search ranking.
- **Boilerplate removal** — lines appearing on more than
  `--boilerplate-threshold` of pages (default 0.6) are site chrome, not
  content. They are removed from the searchable text and listed in
  `boilerplate.txt`.
- **Product extraction** — e-commerce cards are distilled into
  `products.jsonl` with sku, name, price, previous price, brand and category,
  queryable via `query_site.py --products`.

## The zagzoog.com archive

`data/zagzoog/` holds an archive of zagzoog.com (Zagzoog for Home Appliances)
built through this path, because the domain is blocked by the egress policy of
the environment it was built in.

The site is a Next.js storefront with `/en/` and `/ar/` locales over a Magento
catalog. Two properties shaped the capture:

- Content is rendered client-side, so pages had to be fetched with a
  JavaScript-capable browser, not plain HTTP.
- The shop listing renders **12 product cards per view** and loads the rest on
  scroll. Category and brand filters are URL parameters
  (`/en/shop/?category_id=NNN&brand=NN`), so the catalog was captured by
  slicing it into filtered views small enough to render whole.

That yields 217 of the 230 products the site advertises (94%), each with its
own detail page captured. Four categories are complete: Cooking Appliances
47/47, Small Appliances 36/36, Dishwashers 7/7, Screens 5/5.

Finding the last of those 217 needed two things beyond the obvious slicing:

- **Category IDs run past the navigation.** The mega-menu exposes ids 422-450,
  but 451-456 also hold products and appear in no menu. Probing found them;
  457 onward are empty, so the range ends at 456.
- **Subcategory x brand.** A category filtered to one brand usually falls
  under the 12-card render cap even when the category alone does not.

The remaining 13 (Air Conditioners 47/56, Laundry 29/32, Refrigeration 46/47)
sit behind three slices that stay capped at 12 with no finer filter to apply:
duct AC by O General, and the Z Trust refrigeration and laundry subcategories.
Everything else was tried and ruled out rather than assumed: the `page`
parameter is ignored, sort and price filters are client-side state, search is
an inline XHR with no URL route, the Arabic locale returns the identical 12,
related-product links surface nothing new, and Floor Standing AC (`425`)
returns zero products for every brand. Those 13 need a scrolling browser
session.

One limit worth stating plainly: the **specification table is not captured**.
On a product page "Product Details" and "Specifications" are collapsed
accordions whose contents are not in the DOM until a user clicks them, so no
amount of rendering reaches them. The per-product spec sheet PDF carries those
numbers — `products.jsonl` records its URL for 134 of the 203 (the other 69
publish no sheet). Downloading and parsing those PDFs is the remaining step to
a complete specification database.

To refresh the archive, re-fetch the URLs in `data/zagzoog/pages.jsonl` and
re-run `ingest_fetched.py` over the results.

## Courtesy and legality

Scrape sites you own or have permission to archive. The defaults — obeying
`robots.txt`, one request per second, an identifying User-Agent — are there to
keep the crawl from burdening the target server. Raising `--concurrency` or
lowering `--delay` on someone else's site is impolite and may get you blocked.
