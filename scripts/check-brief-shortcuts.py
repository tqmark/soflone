"""Check the native/Sofle browser-brief contract without invoking any action."""

import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
BROWSERS = {r"^com\.vivaldi\.Vivaldi$"}
DEVICE = {"vendor_id": 7504, "product_id": 24926}
PREFIX = 'PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin" python3 ~/.config/karabiner/browser_brief.py '


def validate(config, keymap):
    if "profiles" in config:
        profiles = [p for p in config["profiles"] if p.get("selected")]
        assert len(profiles) == 1, "Expected one selected Karabiner profile"
        rules = profiles[0].get("complex_modifications", {}).get("rules", [])
    else:
        rules = config["rules"]
    handlers = [m for r in rules for m in r.get("manipulators", [])
                if any("browser_brief.py" in t.get("shell_command", "") for t in m.get("to", []))]
    assert len(handlers) == 4, f"Expected 4 browser brief handlers, got {len(handlers)}"
    seen = set()
    for m in handlers:
        assert m["type"] == "basic"
        source = m["from"]
        native = "simultaneous" in source
        shifted = source.get("modifiers", {}).get("mandatory", []) == ["shift"]
        assert source.get("modifiers", {}) == ({"mandatory": ["shift"]} if shifted else {})
        mode = "full" if shifted else "transcript"
        assert m["to"] == [{"shell_command": PREFIX + mode}], "Unexpected action or typed keys"
        conditions = m["conditions"]
        browser = [c for c in conditions if c["type"] == "frontmost_application_if"]
        assert len(browser) == 1 and set(browser[0]["bundle_identifiers"]) == BROWSERS
        device = [c for c in conditions if c["type"] == ("device_unless" if native else "device_if")]
        assert len(conditions) == 2 and len(device) == 1 and device[0]["identifiers"] == [DEVICE]
        if native:
            assert source["simultaneous"] == [{"key_code": "spacebar"}, {"key_code": "y"}]
            assert m["parameters"] == {"basic.simultaneous_threshold_milliseconds": 30}
            assert source["simultaneous_options"] == {
                "detect_key_down_uninterruptedly": True,
                "key_down_order": "insensitive", "key_up_order": "insensitive", "key_up_when": "any",
            }
        else:
            assert source["key_code"] == "f18"
        pair = (native, shifted)
        assert pair not in seen, "Duplicate shortcut"
        seen.add(pair)
    assert len(seen) == 4
    text = re.sub(r"/\*.*?\*/|//[^\n]*", "", keymap, flags=re.S)
    body = re.search(r"raise_layer\s*\{.*?bindings\s*=\s*<([^>]*)>", text, re.S).group(1)
    bindings = [" ".join(b.split()) for b in re.findall(r"&[^&]+", body)]
    assert bindings[13] == "&kp F18", "Raise physical Y must emit F18"


if __name__ == "__main__":
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "macos/karabiner/brief-shortcuts.json"
    try:
        validate(json.loads(path.read_text()), (ROOT / "config/sofle.keymap").read_text())
    except (AssertionError, ValueError, KeyError) as error:
        sys.exit(f"FAIL: {error}")
    print("PASS: native Space+Y/Shift+Y and Sofle F18/Shift+F18, scopes, actions and firmware bridge match")
