# Browser transcript / full-brief shortcuts

These files restore the browser action that existed in older Karabiner backups but was missing from both the active profile and the Sofle's Raise layer.

| Keyboard | Transcript only | Full brief |
| --- | --- | --- |
| Native / non-Sofle | Space+Y | Shift+Space+Y |
| Sofle | Hold K, tap Y | Hold K and the Shift thumb, tap Y |

The native version uses the same 30 ms simultaneous-chord window as the existing Space app launchers, not a global Space hold layer. Hold Shift first for the shifted variant. Native rules exclude the Sofle; Sofle F18 rules require its VID/PID (`1d50:615e`). Both are restricted to Vivaldi. Holding Base Y still opens Navigation/Media, unchanged.

## Files and installation

- `brief-shortcuts.json`: two importable Karabiner rules, with four manipulators. This is a rule fragment, **not** a replacement for the full personal `karabiner.json`.
- `browser_brief.py`: install at `~/.config/karabiner/browser_brief.py`. Rules invoke it through Homebrew/system `python3` with mode `transcript` or `full`.
- Requires the existing executable `~/.local/bin/brief` and its existing dependencies, including `yt-dlp`, Python, and macOS clipboard utilities. This repository does not copy or modify that separate tool.
- Sofle Raise+Y must emit F18; Shift is handled by the existing Shift thumb. Each Sofle needs its new firmware flashed separately.

Back up the personal Karabiner configuration before adding these rules to the active profile. Preserve all unrelated rules and profiles. The current Mac's pre-install backup is `~/.config/karabiner/automatic_backups/karabiner_20260919_before_browser_brief.json`.

## Runtime behavior

The wrapper reads the URL from the frontmost supported browser using AppleScript, checks that it is an HTTP(S) YouTube URL, and passes it as an explicit argument to the existing `brief` tool. Transcript mode adds `-t`; full mode does not. The existing tool copies the result to the clipboard. The wrapper never reads the clipboard, types Vimium `yy`, launches a browser, or selects a fallback tab. Unsupported URLs and browser-read failures do not invoke `brief`.

This intentionally replaces the old Vimium/clipboard timing dependency while restoring the original user-facing actions. Vivaldi's installed AppleScript dictionary is used to compile the URL query, so Vivaldi must be installed for the script to compile. macOS may ask for Automation access to System Events and the chosen browser on first use; grant it only when you deliberately trigger this shortcut.

## Checks

Run from the repository root:

```sh
python3 scripts/check-brief-shortcuts.py
python3 -B -m unittest discover -s tests -p test_browser_brief.py
python3 scripts/check-brief-shortcuts.py "$HOME/.config/karabiner/karabiner.json"
```

The configuration check covers all four actions, exact modifier matching, browser/device scopes, and Raise+Y's F18 binding. The helper tests mock all subprocesses: they do not read a browser or clipboard, run `brief`, fetch transcripts, or access the network. Karabiner's own `--lint-complex-modifications` validates the rule file. AppleScript was compiled, not executed, during installation checks.

After flashing, test on a public YouTube video: transcript mode should copy only transcript output; Shift mode should copy the full brief. Also check ordinary Space/Y typing, native app chords, Sofle Y navigation, and X+G Backspace. Runtime permissions and the existing transcript tool's network behavior are not established by static/mocked tests.
