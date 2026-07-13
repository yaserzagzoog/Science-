"""Point-and-click Audible exporter.

Double-click the packaged .exe (no terminal needed) to:
  1. Sign in to Audible via your own browser (one time).
  2. Fetch your full library (downloaded/purchased titles) and wish list.
  3. Save both as CSV files and view them in the window.

Run with --mcp to act as the MCP server for Claude Desktop instead
(same executable, same saved sign-in).
"""

import csv
import io
import os
import sys
import threading
import webbrowser
from pathlib import Path

# In a windowed (no-console) exe there is no stdio; give the logging and
# MCP machinery something safe to write to so imports don't crash.
if sys.stdout is None:
    sys.stdout = io.TextIOWrapper(io.BytesIO(), encoding="utf-8")
if sys.stderr is None:
    sys.stderr = io.TextIOWrapper(io.BytesIO(), encoding="utf-8")

import audible

import server


def run_gui() -> None:
    import tkinter as tk
    from tkinter import filedialog, messagebox, scrolledtext, simpledialog, ttk

    root = tk.Tk()
    root.title("Audible Library & Wish List Exporter")
    root.geometry("720x560")

    frame = ttk.Frame(root, padding=12)
    frame.pack(fill="both", expand=True)

    auth_file = Path(os.environ.get("AUDIBLE_AUTH_FILE", server.DEFAULT_AUTH_FILE))
    signed_in = auth_file.exists()

    status = tk.StringVar(
        value="Signed in — ready to fetch." if signed_in else "Not signed in yet."
    )

    top = ttk.Frame(frame)
    top.pack(fill="x")
    ttk.Label(top, text="Marketplace:").pack(side="left")
    country = tk.StringVar(value="us")
    ttk.Combobox(
        top,
        textvariable=country,
        values=["us", "ca", "uk", "au", "fr", "de", "es", "it", "in", "jp", "br"],
        width=5,
        state="readonly",
    ).pack(side="left", padx=(4, 16))

    sign_in_btn = ttk.Button(top, text="1. Sign in to Audible")
    sign_in_btn.pack(side="left", padx=4)
    fetch_btn = ttk.Button(top, text="2. Fetch & save my titles")
    fetch_btn.pack(side="left", padx=4)

    ttk.Label(frame, textvariable=status, foreground="#555").pack(
        anchor="w", pady=(8, 4)
    )

    output = scrolledtext.ScrolledText(frame, wrap="word")
    output.pack(fill="both", expand=True)

    def set_busy(busy: bool) -> None:
        state = "disabled" if busy else "normal"
        sign_in_btn.config(state=state)
        fetch_btn.config(state=state)

    def login_url_callback(login_url: str) -> str:
        webbrowser.open(login_url)
        return simpledialog.askstring(
            "Finish signing in",
            "Your browser has opened an Amazon sign-in page.\n"
            "Sign in there (the final page will LOOK like an error — that's\n"
            "normal), then copy that page's full address and paste it here:",
            parent=root,
        ) or ""

    def sign_in() -> None:
        def work() -> None:
            try:
                auth = audible.Authenticator.from_login_external(
                    locale=country.get(), login_url_callback=login_url_callback
                )
                auth_file.parent.mkdir(parents=True, exist_ok=True)
                auth.to_file(auth_file)
                status.set("Signed in — ready to fetch.")
            except Exception as exc:
                messagebox.showerror("Sign-in failed", str(exc))
                status.set("Sign-in failed — try again.")
            finally:
                set_busy(False)

        set_busy(True)
        status.set("Waiting for browser sign-in...")
        # The paste dialog must run on the UI thread, so no worker thread here.
        work()

    def write_csv(path: Path, items: list[dict]) -> None:
        with open(path, "w", newline="", encoding="utf-8-sig") as fh:
            writer = csv.writer(fh)
            writer.writerow(
                ["Title", "Subtitle", "Authors", "Narrators", "Series",
                 "Runtime (hours)", "Release date", "ASIN"]
            )
            for it in items:
                series = "; ".join(
                    f"{s['title']} #{s['sequence']}" if s.get("sequence") else s["title"]
                    for s in it["series"] or []
                )
                writer.writerow(
                    [it["title"], it["subtitle"] or "",
                     ", ".join(it["authors"]), ", ".join(it["narrators"]),
                     series, it["runtime_hours"] or "",
                     it["release_date"] or "", it["asin"]]
                )

    def show(items: list[dict], heading: str) -> None:
        output.insert("end", f"\n=== {heading} ({len(items)}) ===\n")
        for it in items:
            authors = ", ".join(it["authors"])
            output.insert("end", f"  • {it['title']}" + (f" — {authors}\n" if authors else "\n"))
        output.see("end")

    def fetch() -> None:
        if not auth_file.exists():
            messagebox.showinfo("Sign in first", "Please click 'Sign in to Audible' first.")
            return
        folder = filedialog.askdirectory(title="Where should the CSV files be saved?")
        if not folder:
            return

        def work() -> None:
            try:
                status.set("Fetching your library...")
                library = server.get_library()
                status.set("Fetching your wish list...")
                wishlist = server.get_wishlist()
                lib_path = Path(folder) / "audible_library.csv"
                wish_path = Path(folder) / "audible_wishlist.csv"
                write_csv(lib_path, library)
                write_csv(wish_path, wishlist)

                def done() -> None:
                    show(library, "LIBRARY — downloaded/purchased titles")
                    show(wishlist, "WISH LIST")
                    status.set(f"Done. Saved {lib_path.name} and {wish_path.name} to {folder}")
                    set_busy(False)

                root.after(0, done)
            except Exception as exc:
                root.after(0, lambda: (
                    messagebox.showerror("Fetch failed", str(exc)),
                    status.set("Fetch failed."),
                    set_busy(False),
                ))

        set_busy(True)
        threading.Thread(target=work, daemon=True).start()

    sign_in_btn.config(command=sign_in)
    fetch_btn.config(command=fetch)
    root.mainloop()


def main() -> None:
    if "--mcp" in sys.argv:
        server.main()
    else:
        run_gui()


if __name__ == "__main__":
    main()
