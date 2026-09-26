#!/bin/sh

set -eu

keymap_path="${1:-config/sofle.keymap}"

if grep -nE '^[[:space:]]*bindings[[:space:]]*=[[:space:]]*<&mt([[:space:]]|$)' "$keymap_path"; then
    echo "FAIL: a tap dance or custom behavior wraps an undecided mod-tap"
    exit 1
fi

# Tap dances are allowed only around &none/&kt. The 2026-09-14 audit banned
# them outright because one wrapped around a mod-tap creates the mod-tap only
# after the dance resolves, by which time the interrupting key has passed the
# hold-tap listener. That needs a nested hold-tap, so the narrower rule keeps
# the safety property and still permits the Nav/Media modifier dances.
if sed -n '/compatible = "zmk,behavior-tap-dance"/,/};/p' "$keymap_path" \
    | grep -E '^[[:space:]]*bindings[[:space:]]*=' \
    | grep -oE '&[a-zA-Z_][a-zA-Z0-9_]*' \
    | grep -vE '^&(none|kt)$'; then
    echo "FAIL: a tap dance wraps something other than &none/&kt"
    exit 1
fi

echo "PASS: no custom behavior wraps a mod-tap and no tap dance wraps a hold-tap"
