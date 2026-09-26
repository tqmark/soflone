"""Static regression checks for the agreed left-only layout; no ZMK dependencies."""

from pathlib import Path
import re
import sys


POSITIONS = dict(zip(
    "Q P F M L J B Y U R S O C D T H E A X G V W N I K Z slash esc comma space".split(),
    [*range(0, 6), *range(12, 18), *range(24, 30), *range(36, 43), *range(50, 55)],
))
THUMBS = {
    "slash": "&mt LEFT_ALT SLASH",
    "esc": "&mt LEFT_CONTROL ESC",
    "comma": "&mt LEFT_COMMAND COMMA",
    "space": "&mt LEFT_SHIFT SPACE",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate(source):
    source = re.sub(r"/\*.*?\*/|//[^\n]*", "", source, flags=re.S)
    matches = re.findall(
        r'(\w+)\s*\{\s*display-name\s*=\s*"[^"]*";\s*bindings\s*=\s*<([^>]*)>',
        source,
    )
    require(len(matches) == 4, "Expected exactly four layers")
    layers = {
        name: [" ".join(binding.split()) for binding in re.findall(r"&[^&]+", body)]
        for name, body in matches
    }
    require(list(layers) == ["default_layer", "lower_layer", "raise_layer", "media_layer"],
            "Unexpected layer names or order")
    for index, name in enumerate(("BASE", "LOWER", "RAISE", "MEDIA")):
        require(re.search(r"#define\s+" + name + r"\s+" + str(index) + r"\b", source),
                f"{name}: layer index changed")
    for name, bindings in layers.items():
        require(len(bindings) == 60, f"{name}: expected 60 matrix bindings")
        # BT_CLR and BT_CLR_ALL expand to two cells, so only &bt, which takes
        # exactly two, may use them. Anywhere else the extra cell shifts every
        # later binding and the build fails far from the cause.
        for binding in bindings:
            require(not re.search(r"\bBT_CLR(_ALL)?\b", binding) or binding.startswith("&bt "),
                    f"{name}: {binding}: use BT_CLR_CMD outside &bt")

    base = {key: f"&kp {key}" for key in POSITIONS if len(key) == 1}
    base.update(THUMBS)
    base.update(X="&lt LOWER X", K="&lt RAISE K", Y="&ymedia MEDIA Y")

    lower = dict(zip(
        "Q P F M L J B Y U R S O".split(),
        [f"&kp {key}" for key in
         "NUMBER_1 NUMBER_2 NUMBER_3 NUMBER_4 N5 NUMBER_6 N7 N8 N9 N0 MINUS EQUAL".split()],
    ))
    lower.update(THUMBS)
    lower.update({
        "C": "&kp SQT", "T": "&kp SEMI", "H": "&kp TAB", "E": "&kp BACKSPACE",
        "A": "&kp LC(A)", "X": "&lower_bslash_base 0 0", "G": "&kp BACKSPACE", "V": "&kp BSLH",
        "N": "&kp LEFT_BRACKET", "I": "&kp RIGHT_BRACKET", "K": "&kp GRAVE",
        "Z": "&tog LOWER", "esc": "&trans", "comma": "&mt LEFT_COMMAND DOT",
        "space": "&mt LEFT_SHIFT ENTER",
    })

    raise_keys = dict(THUMBS)
    raise_keys.update({
        "Q": "&bt BT_SEL 0", "P": "&bt BT_SEL 1", "B": "&kp F13", "T": "&kp F14",
        "N": "&kp F15", "C": "&kp F16", "S": "&kp F17", "F": "&kp F19", "Y": "&kp F18",
        "I": "&ext_power EP_ON", "K": "&kp ESC", "Z": "&tog RAISE",
        "D": "&hold_bootloader 0 0", "W": "&hold_bt_clear BT_CLR_CMD 0",
    })

    nav_media = dict(THUMBS)
    nav_media.update({
        "P": "&kp C_VOL_DN", "F": "&kp C_VOL_UP", "M": "&kp C_MUTE",
        "H": "&kp LEFT", "J": "&kp DOWN", "K": "&kp UP", "L": "&kp RIGHT",
        "O": "&kp BACKSPACE", "C": "&td_command", "S": "&td_shift",
    })

    for name, expected in zip(
        ("default_layer", "lower_layer", "raise_layer", "media_layer"),
        (base, lower, raise_keys, nav_media),
    ):
        for key, position in POSITIONS.items():
            wanted = expected.get(key, "&none")
            require(layers[name][position] == wanted,
                    f"{name} physical {key}: expected {wanted}, got {layers[name][position]}")

    # Benign combos stay scoped to Base. No combo may be destructive: a Base
    # combo's one-shot Raise makes a second press of the same chord a Raise combo.
    expected_combos = {
        "grave": ("0 1", "BASE", "&kp GRAVE", None),
        "tab": ("12 13", "BASE", "&kp TAB", None),
        "raise_once": ("38 39", "BASE", "&sl RAISE", None),
    }
    require(len(re.findall(r"(?<![-\w])key-positions\s*=", source)) == len(expected_combos),
            "Unexpected combo count")
    for name, (positions, layer, binding, timeout) in expected_combos.items():
        match = re.search(r"\b" + name + r"\s*\{([^}]*)\}", source)
        require(match is not None, f"Missing combo {name}")
        body = match.group(1)
        for prop, value in {"key-positions": positions, "layers": layer, "bindings": binding}.items():
            actual = re.search(re.escape(prop) + r"\s*=\s*<([^>]*)>", body)
            require(actual is not None and " ".join(actual.group(1).split()) == value,
                    f"{name}: unexpected {prop}")
        if timeout:
            require(re.search(r"timeout-ms\s*=\s*<" + timeout + r">", body),
                    f"{name}: timeout changed")

    for name, pattern, flavor in (
        ("mt", r"&mt\s*\{([^}]*)\}", "hold-preferred"),
        ("lt", r"&lt\s*\{([^}]*)\}", "hold-preferred"),
        ("ymedia", r"ymedia:\s*ymedia\s*\{([^}]*)\}", "balanced"),
    ):
        match = re.search(pattern, source)
        require(match is not None, f"Missing hold behavior {name}")
        body = match.group(1)
        require(re.search(r'flavor\s*=\s*"' + flavor + '"', body), f"{name}: flavor changed")
        require(re.search(r"tapping-term-ms\s*=\s*<200>", body), f"{name}: timing changed")
        if name == "ymedia":
            require(re.search(r"bindings\s*=\s*<&mo>\s*,\s*<&kp>", body),
                    "Y must hold a momentary layer and tap a key")
            require(re.search(r"require-prior-idle-ms\s*=\s*<150>", body),
                    "ymedia: Y typed within 150 ms of another key must stay a letter")
            triggers = re.search(r"hold-trigger-key-positions\s*=\s*<([^>]*)>", body)
            wanted = sorted(POSITIONS[k] for k in "P F M L J S O C H K slash esc comma space".split())
            require(triggers is not None and sorted(map(int, triggers.group(1).split())) == wanted,
                    "ymedia: hold triggers must be exactly the Nav keys and modifier thumbs")

    # Destructive actions: one-second hold, tap does nothing.
    for name, hold in (("hold_bt_clear", "&bt"), ("hold_bootloader", "&bootloader")):
        match = re.search(name + r":\s*" + name + r"\s*\{([^}]*)\}", source)
        require(match is not None, f"Missing {name}")
        body = match.group(1)
        require(re.search(r'flavor\s*=\s*"tap-preferred"', body), f"{name}: must fire only on the timer")
        require(re.search(r"tapping-term-ms\s*=\s*<1000>", body), f"{name}: hold must be one second")
        require(re.search(r"bindings\s*=\s*<" + hold + r">\s*,\s*<&none>", body),
                f"{name}: tap must do nothing")
    # Tap dances are allowed only where they cannot reproduce the 2026-09-14
    # failure: one wrapped around a mod-tap resolves late and leaks the tap key.
    # So every tap dance must wrap only &none/&kt, and must start with &none so
    # a single tap emits nothing.
    dances = re.findall(r'(\w+):\s*\w+\s*\{([^}]*compatible\s*=\s*"zmk,behavior-tap-dance"[^}]*)\}',
                        source)
    require(len(dances) == source.count('"zmk,behavior-tap-dance"'),
            "Could not parse every tap dance")
    for name, body in dances:
        bindings = re.findall(r"&[\w]+", re.search(r"bindings\s*=\s*<([^;]*)>;", body).group(1))
        require(bindings[0] == "&none", f"{name}: a single tap must emit nothing")
        require(all(b in ("&none", "&kt") for b in bindings),
                f"{name}: a tap dance may only wrap &none and &kt, never a hold-tap")
        require(re.search(r"tapping-term-ms\s*=\s*<300>", body), f"{name}: timing changed")
    require({n for n, _ in dances} == {"td_command", "td_shift"}, "Unexpected tap dances")


if __name__ == "__main__":
    try:
        validate(Path(sys.argv[1] if len(sys.argv) > 1 else "config/sofle.keymap").read_text())
    except ValueError as error:
        sys.exit(f"FAIL: {error}")
    print("PASS: four 60-position layers; left bindings, modifiers, timing, combos and recovery holds match")
