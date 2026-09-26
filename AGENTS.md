# Soflone

ZMK firmware for a left-half-only Sofle, used by a programmer with only the left hand. Read `CONTEXT.md` for terms, then `docs/decision-history.md` before changing any binding; `docs/adr/` explains the two fixed constraints.

- Every action must remain reachable with the left hand. Do not move letters, fill unused positions, or add F1-F12, tap dances, or a fifth layer without being asked.
- `config/west.yml` is pinned before Zephyr 4.1 on purpose. Do not bump ZMK or rename `nice_nano_v2`.
- Saved firmware is not flashed firmware. Record a flash only after the user or the DFU output confirms it; a green CI build proves nothing about the keyboard.
- A binding change also updates the keymap comments, the decision history (current keymap, chronology, regression test) and `scripts/check-keymap-layout.py`.
- Treat Raise V+W (clear Bluetooth) and Raise X+G (bootloader) as destructive; never trigger or move them casually.

Checks (CI runs the same, then builds):

```sh
scripts/check-hold-tap-safety.sh
python3 scripts/check-keymap-layout.py
python3 scripts/check-brief-shortcuts.py
python3 -m unittest discover -s tests
```
