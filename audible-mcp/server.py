"""Audible MCP server.

Exposes your personal Audible account — the titles in your library
(purchased/downloaded) and your wish list — as MCP tools.

Requires a one-time login via authenticate.py, which stores device
credentials in an auth file (default: ~/.audible-mcp/auth.json).

Environment variables:
    AUDIBLE_AUTH_FILE      Path to the auth file (default above).
    AUDIBLE_AUTH_PASSWORD  Password for the auth file, if you encrypted it.
"""

import os
from pathlib import Path
from typing import Any

import audible
from mcp.server.fastmcp import FastMCP

DEFAULT_AUTH_FILE = Path.home() / ".audible-mcp" / "auth.json"

RESPONSE_GROUPS = "product_desc,product_attrs,contributors,series"
PAGE_SIZE = 500  # max the Audible API allows per page

mcp = FastMCP("audible")

_client: audible.Client | None = None


def _get_client() -> audible.Client:
    global _client
    if _client is None:
        auth_file = Path(os.environ.get("AUDIBLE_AUTH_FILE", DEFAULT_AUTH_FILE))
        if not auth_file.exists():
            raise RuntimeError(
                f"Auth file not found at {auth_file}. "
                "Run `python authenticate.py` first (see README.md)."
            )
        password = os.environ.get("AUDIBLE_AUTH_PASSWORD")
        auth = audible.Authenticator.from_file(auth_file, password=password)
        _client = audible.Client(auth=auth)
    return _client


def _format_item(product: dict[str, Any]) -> dict[str, Any]:
    """Reduce a raw Audible product record to the fields that matter."""
    authors = [a["name"] for a in product.get("authors") or []]
    narrators = [n["name"] for n in product.get("narrators") or []]
    series = [
        {"title": s.get("title"), "sequence": s.get("sequence")}
        for s in product.get("series") or []
    ]
    minutes = product.get("runtime_length_min")
    return {
        "title": product.get("title"),
        "subtitle": product.get("subtitle"),
        "authors": authors,
        "narrators": narrators,
        "series": series or None,
        "runtime_hours": round(minutes / 60, 1) if minutes else None,
        "release_date": product.get("release_date"),
        "asin": product.get("asin"),
    }


def _fetch_all_pages(path: str, items_key: str, **params: Any) -> list[dict[str, Any]]:
    """Page through an Audible API endpoint until it runs dry."""
    client = _get_client()
    items: list[dict[str, Any]] = []
    page = 0
    while True:
        response = client.get(
            path,
            num_results=PAGE_SIZE,
            page=page,
            response_groups=RESPONSE_GROUPS,
            **params,
        )
        batch = response.get(items_key) or []
        items.extend(batch)
        if len(batch) < PAGE_SIZE:
            return items
        page += 1


@mcp.tool()
def get_library() -> list[dict[str, Any]]:
    """List every title in the user's Audible library (all purchased and
    downloaded audiobooks), newest purchases first."""
    raw = _fetch_all_pages("1.0/library", "items", sort_by="-PurchaseDate")
    return [_format_item(item) for item in raw]


@mcp.tool()
def get_wishlist() -> list[dict[str, Any]]:
    """List every title on the user's Audible wish list, newest first."""
    raw = _fetch_all_pages("1.0/wishlist", "products", sort_by="-DateAdded")
    return [_format_item(item) for item in raw]


@mcp.tool()
def search_library(query: str) -> list[dict[str, Any]]:
    """Search the user's Audible library by title, author, or narrator.

    Args:
        query: Case-insensitive text to match against title, subtitle,
            author names, and narrator names.
    """
    needle = query.lower()
    results = []
    for item in get_library():
        haystack = " ".join(
            filter(
                None,
                [
                    item["title"],
                    item["subtitle"],
                    *item["authors"],
                    *item["narrators"],
                ],
            )
        ).lower()
        if needle in haystack:
            results.append(item)
    return results


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
