"""One-time Audible authentication.

Creates the encrypted auth file the MCP server uses. Run this once on the
machine where the server will run:

    python authenticate.py

You will be given an Amazon URL to open in your browser. Sign in there
(password, 2FA, CAPTCHA all happen in the browser — this script never sees
your password), then paste the final redirect URL back here.
"""

import getpass
import os
from pathlib import Path

import audible

DEFAULT_AUTH_FILE = Path.home() / ".audible-mcp" / "auth.json"

COUNTRY_CODES = ["us", "ca", "uk", "au", "fr", "de", "es", "it", "in", "jp", "br"]


def main() -> None:
    auth_file = Path(os.environ.get("AUDIBLE_AUTH_FILE", DEFAULT_AUTH_FILE))
    if auth_file.exists():
        answer = input(f"{auth_file} already exists. Overwrite? [y/N] ")
        if answer.strip().lower() != "y":
            print("Aborted.")
            return

    print("Audible marketplaces:", ", ".join(COUNTRY_CODES))
    country = input("Your marketplace country code [us]: ").strip().lower() or "us"
    if country not in COUNTRY_CODES:
        print(f"Unknown country code {country!r}. Aborted.")
        return

    print(
        "\nA login URL will be shown next. Open it in your browser, sign in to\n"
        "Amazon/Audible, and when the browser lands on an error-looking page\n"
        "(that's expected), copy its full URL and paste it here.\n"
    )

    auth = audible.Authenticator.from_login_external(locale=country)

    password = getpass.getpass(
        "Password to encrypt the auth file (press Enter for none): "
    )

    auth_file.parent.mkdir(parents=True, exist_ok=True)
    if password:
        auth.to_file(auth_file, password=password, encryption="json")
    else:
        auth.to_file(auth_file)

    print(f"\nDone. Credentials saved to {auth_file}")
    if password:
        print("Set AUDIBLE_AUTH_PASSWORD to this password when running the server.")
    print("Set AUDIBLE_AUTH_FILE to this path if you move the file elsewhere.")


if __name__ == "__main__":
    main()
