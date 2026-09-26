#!/usr/bin/env python3
"""Run the existing brief tool for the active browser's YouTube tab."""

from pathlib import Path
import subprocess
import sys
from urllib.parse import urlsplit


# Only Vivaldi is named here, and that is deliberate -- `using terms from`
# resolves the dictionary at *compile* time, so naming a browser that is not
# installed fails the whole script rather than just that branch. Vivaldi is the
# only browser in the Brewfile, so it is the only one guaranteed to be there.
# Choose only the frontmost app. No synthetic keystrokes, clipboard reads,
# cookies, or network calls here.
BROWSER_URL_SCRIPT = '''
tell application "System Events"
    set browserID to bundle identifier of first application process whose frontmost is true
end tell
if browserID is not in {"com.vivaldi.Vivaldi"} then
    error "Use Vivaldi"
end if
using terms from application "Vivaldi"
    tell application id browserID
        if (count of windows) is 0 then error "No browser window"
        return URL of active tab of front window
    end tell
end using terms from
'''


def youtube_url(value):
    try:
        url = urlsplit(value)
        return (
            url.scheme in ("https", "http")
            and url.hostname in {"youtube.com", "www.youtube.com", "m.youtube.com",
                                 "music.youtube.com", "youtu.be", "www.youtu.be"}
            and url.username is None and url.password is None
            and url.port in (None, 80, 443)
            and not any(c.isspace() for c in value)
        )
    except ValueError:
        return False


def main(argv=None, *, run=subprocess.run, brief_path=None):
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1 or args[0] not in ("transcript", "full"):
        print("Usage: browser_brief.py {transcript|full}", file=sys.stderr)
        return 2
    try:
        result = run(["/usr/bin/osascript", "-e", BROWSER_URL_SCRIPT],
                     capture_output=True, text=True, check=True, timeout=10)
        url = result.stdout.strip()
        if not youtube_url(url):
            print("Open a YouTube video in Vivaldi first.", file=sys.stderr)
            return 1
        command = [str(brief_path or Path.home() / ".local/bin/brief")]
        if args[0] == "transcript":
            command.append("-t")
        command.append(url)
        # Pass an explicit, validated URL so brief cannot fall back to clipboard.
        return run(command, check=False).returncode
    except (OSError, subprocess.SubprocessError):
        print("Could not run browser brief. Check the helper and macOS Automation permissions.",
              file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
