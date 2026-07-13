# Audible MCP Server

An MCP (Model Context Protocol) server that gives Claude access to **your
personal Audible account**: the titles in your library (everything you've
purchased/downloaded) and your wish list.

The stock Audible connector on claude.ai can only search the public catalog —
it has no login to your account. This server fills that gap. It uses the
community [`audible`](https://github.com/mkb79/Audible) API client, which
registers itself as a device on your account (the same way the Audible app
does), since Audible has no official public API.

## Tools

| Tool | What it returns |
|---|---|
| `get_library` | Every title you own, newest purchases first |
| `get_wishlist` | Every title on your wish list, newest first |
| `search_library` | Titles you own matching a title/author/narrator query |

Each item includes title, subtitle, authors, narrators, series info, runtime,
release date, and ASIN.

## No-terminal option: the Windows app

If you don't want to touch a shell at all, use the prebuilt Windows app
instead. Every push to this folder triggers the *Build Audible Exporter*
GitHub Actions workflow, which compiles everything into a single
`AudibleExporter.exe` published on the repo's **Releases** page.

1. Download `AudibleExporter.exe` from Releases and double-click it.
2. Click **Sign in to Audible** — your browser opens Amazon's sign-in page
   (the app never sees your password); after signing in, copy the final
   page's address and paste it into the app.
3. Click **Fetch & save my titles** — it saves `audible_library.csv` and
   `audible_wishlist.csv` wherever you choose and shows both lists.

To also use it as an MCP server for Claude Desktop (still no shell — the
config file opens in Notepad via Settings → Developer → Edit Config):

```json
{
  "mcpServers": {
    "audible": {
      "command": "C:\\path\\to\\AudibleExporter.exe",
      "args": ["--mcp"]
    }
  }
}
```

## Setup from source (terminal route)

Requires Python 3.10+ on the machine where the server will run (your own
computer — your credentials stay local).

```bash
cd audible-mcp
pip install .
```

### 1. Authenticate (one time)

```bash
python authenticate.py
```

Pick your marketplace (e.g. `us`), open the Amazon URL it prints in your
browser, sign in there, and paste the final redirect URL back into the
terminal. Your password is only ever typed into Amazon's own page. The
resulting device credentials are saved to `~/.audible-mcp/auth.json`
(optionally encrypted with a password of your choosing).

### 2. Connect to Claude

**Claude Code:**

```bash
claude mcp add audible -- python /path/to/audible-mcp/server.py
```

**Claude Desktop** — add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "audible": {
      "command": "python",
      "args": ["/path/to/audible-mcp/server.py"]
    }
  }
}
```

If you encrypted the auth file or moved it, set `AUDIBLE_AUTH_PASSWORD` /
`AUDIBLE_AUTH_FILE` in the server's `env` block.

### 3. Use it

Ask Claude things like:

- "Pull all the titles I've downloaded on Audible and my wish list."
- "Which books on my Audible wish list are by authors I already own?"
- "Do I own anything narrated by Ray Porter?"

## Notes

- Registering creates a device on your Amazon account (visible under
  *Manage Your Content and Devices*); you can deregister it there any time.
- The auth file grants access to your Audible account — treat it like a
  password. Encrypting it during `authenticate.py` is recommended.
- This uses an unofficial API client. It is stable and widely used, but it is
  not endorsed by Audible/Amazon.
