# H/J/K/L arrow strategy for the left-only Sofle

Research date: 2026-09-14

Historical proposal, not implemented. The final 2026-09-18 redesign instead reuses the Y-held fourth layer for H/J/K/L arrows, O Backspace, P/F/M volume, and Base modifier thumbs. The user confirmed Y is pinky-operated. Raise now holds applications, Bluetooth, and recovery rather than arrows. Base H/J/K/L typing and the K layer leader remain unchanged. See `../decision-history.md` for the current saved layout; the comparisons below describe the earlier design.

## Question

How should the physical Base `H`, `J`, `K`, and `L` keys also produce Left, Down, Up, and Right without making ordinary typing less reliable for a one-left-hand user?

This note evaluates the saved keymap at `11ccab3`. It recommends a design but does not change the firmware.

## Recommendation

Keep Base `H`, `J`, `K`, and `L` exactly as they are. Add Left, Down, Up, and Right to those same physical positions on the existing Raise layer:

```text
physical key   H      J       K     L
Base           h      j       k     l
Raise          Left   Down    Up    Right
```

Use two navigation paths:

1. For repeated Vim-style movement, hold Base `K`, tap `Z`, release `K`, then use `H/J/K/L`. Tap `Z` to return to Base.
2. For quick movement while `K` remains held, keep the current `Q/P/F/M` arrows. They remain Left/Down/Up/Right and avoid the impossible `K`-while-holding-`K` case.

This works because ZMK resolves a position from the highest active layer; after Raise is locked and the original Base `K` is released, pressing physical `K` uses Raise's `Up` binding rather than Base's `K`/Raise layer-tap. [ZMK's layer model](https://zmk.dev/docs/keymaps#layers) defines this binding precedence. The current pinned ZMK revision also documents that `&tog` locks an already momentarily active layer so releasing its `&mo`/layer-tap activator does not turn it off; a later `&tog` turns it off. [Official layer-locking documentation at the pinned revision](https://github.com/zmkfirmware/zmk/blob/9ebbeff0a8b69a42f14aec022cdf16c7a107b9e0/docs/docs/keymaps/behaviors/layers.md#layer-locking).

### Exact impact on the saved Raise layer

| Physical position | Current Raise action | Proposed action | Resolution |
| --- | --- | --- | --- |
| `H` | Ghostty layout 2 | Left | Move layout 2 to one of the unused Raise positions, preferably physical `U` |
| `J` | Backspace | Down | Remove this duplicate; Backspace remains available through Base `L+J`, Lower `D`, and Media `Y+J` |
| `K` | Escape / Raise-off tap dance | Up | Use `Z` as the existing reliable layer exit; the Escape/Control thumb still supplies Escape |
| `L` | Unused | Right | No displacement |

The current bindings and their physical positions are visible in [`config/sofle.keymap`](../../config/sofle.keymap).

## Why this is the best first change

- **No Base typing risk.** Base `H/J/K/L` remain their current bindings, so there is no new hold threshold, delayed letter, or accidental arrow decision during ordinary prose, code, or Neovim use. ZMK hold-taps necessarily decide between two outcomes using a tapping term and interruption rules; avoiding four new hold-taps avoids that ambiguity entirely. [Official hold-tap summary and interrupt-flavor definitions](https://zmk.dev/docs/keymaps/behaviors/hold-tap#interrupt-flavors).
- **It uses an already learned gesture.** `K+Z` already locks Raise, and `Z` already exits it. ZMK explicitly supports locking a momentarily activated layer with `&tog`. [Official layer-locking documentation](https://zmk.dev/docs/keymaps/behaviors/layers#layer-locking).
- **It solves K's physical conflict honestly.** One physical switch cannot remain depressed as the Raise activator and also be pressed again as Up. Locking Raise, releasing K, and then using K as Up removes the conflict without moving the familiar Base letter.
- **It adds no fifth layer and no new leader.** The only required firmware changes would be four Raise bindings and relocating one Ghostty layout command.
- **It preserves the fastest temporary path.** ZMK's momentary layer behavior is active only while its activator is held. That is ideal for `K+Q/P/F/M`, where the leader is not itself one of the four targets. [Official momentary-layer behavior](https://zmk.dev/docs/keymaps/behaviors/layers#momentary-layer).

## One-arrow alternative already present

Base `V+W` currently invokes `&sl RAISE`. Once H/J/K/L are placed on Raise, the sequence `V+W`, release, then tap one of `H/J/K/L` can produce one Vim-style arrow, including `K` for Up. ZMK sticky layers are one-shot layers and quick-release on the next key press. [Official sticky-layer behavior](https://zmk.dev/docs/keymaps/behaviors/sticky-layer).

This is technically clean but is secondary here: ZMK combos require every member to be pressed inside `timeout-ms`, which favors a near-simultaneous chord, while the user's more comfortable motion is holding a leader and then tapping a target. [Official combo timing and layer scoping](https://zmk.dev/docs/keymaps/combos#configuration).

## Alternatives considered

### 1. A dedicated Nav layer held by Z

A fifth sparse layer could put arrows on physical H/J/K/L and make Base Z a custom `tap Z / hold Nav` behavior. A positional hold-tap could list only H/J/K/L as hold triggers: an intended `Z+H/J/K/L` would select Nav immediately under `hold-preferred`, while another key pressed before the tapping term would force Z to tap. ZMK documents both the immediate interrupt behavior of `hold-preferred` and the way unlisted positions force a positional hold-tap to tap. [Interrupt flavors](https://zmk.dev/docs/keymaps/behaviors/hold-tap#interrupt-flavors); [positional hold-taps](https://zmk.dev/docs/keymaps/behaviors/hold-tap#positional-hold-tap-and-hold-trigger-key-positions).

This is the best option only if the user requires the exact gesture “hold one leader, tap any H/J/K/L” for all four arrows without locking first. It is not the first recommendation because Z is operated by the pinky, sustained pinky holds may be tiring, Z is the established universal layer exit, and it adds a fifth layer.

`require-prior-idle-ms` can force a recently typed dual-role key to tap immediately and reduce fast-typing misfires, but a larger value also makes the hold behavior harder to invoke soon after typing. [Official `require-prior-idle-ms` behavior and trade-off](https://zmk.dev/docs/keymaps/behaviors/hold-tap#require-prior-idle-ms).

### 2. Hold each letter for its arrow

Custom hold-taps could make quick `H/J/K/L` presses type letters and long presses send arrows. With `tap-preferred`, an interrupt does not choose hold, but the arrow is not selected until the tapping term expires. With `hold-preferred`, another key press selects hold immediately, which is risky for rolled same-hand typing. [Official interrupt-flavor definitions](https://zmk.dev/docs/keymaps/behaviors/hold-tap#interrupt-flavors).

This option also cannot preserve K's existing hold-to-Raise behavior: one hold-tap has one hold outcome, so K's hold would have to mean either Raise or Up. ZMK custom hold-taps combine one hold behavior and one tap behavior. [Official custom hold-tap model](https://zmk.dev/docs/keymaps/behaviors/hold-tap#custom-hold-tap-configuration).

For this layout, direct letter hold-taps therefore add latency and typing risk while still forcing Raise to move. They are not recommended.

### 3. Use Shift, Control, Command, or Option with H/J/K/L

A mod-morph can make a key choose another binding when a specified modifier is held; by default, the triggering modifier is not sent with the morphed key. [Official mod-morph behavior](https://zmk.dev/docs/keymaps/behaviors/mod-morph).

This would consume valuable existing chords. Shift is needed for uppercase and symbols, Control for terminal/Neovim commands, Command for macOS shortcuts, and Option for window or editor actions. In particular, using Space/Shift+H/J/K/L for arrows would remove the only direct Base route to uppercase H/J/K/L. It is not recommended.

### 4. Double-tap the letters

Tap dance can assign another action to a second tap, but it waits for its tapping term unless interrupted, and a second tap selects the second binding. [Official tap-dance resolution](https://zmk.dev/docs/keymaps/behaviors/tap-dance).

That makes ordinary repeated letters such as `ll` semantically ambiguous and repeats the timing complexity previously removed from X and K. It is not recommended.

### 5. Toggle or sticky navigation modes

A dedicated `&tog NAV` would allow repeated arrows after the activator is released, but it creates another persistent mode that must be explicitly turned off. ZMK's toggle behavior stays enabled until toggled again. [Official toggle-layer behavior](https://zmk.dev/docs/keymaps/behaviors/layers#toggle-layer).

A dedicated `&sl NAV` would avoid holding and would expose K/Up, but it releases on the next key, so every additional arrow needs another activation. [Official sticky-layer behavior](https://zmk.dev/docs/keymaps/behaviors/sticky-layer). The existing Raise lock and one-shot paths already provide both patterns without adding a new mode.

### 6. Other ZMK mechanisms

- Key toggle holds an individual key down until toggled or otherwise released; using it for an arrow risks continued cursor movement and does not create an H/J/K/L navigation map. [Official key-toggle behavior](https://zmk.dev/docs/keymaps/behaviors/key-toggle).
- Conditional layers activate a layer only when all configured prerequisite layers are active. That is useful for tri-layer designs, not for this single-leader navigation problem. [Official conditional-layer behavior](https://zmk.dev/docs/keymaps/conditional-layers).
- Sticky keys are intended to keep a key—commonly a modifier—pressed until another key is pressed. A sticky **layer**, not a sticky key, is the relevant one-shot navigation mechanism. [Official sticky-key behavior](https://zmk.dev/docs/keymaps/behaviors/sticky-key); [official sticky-layer behavior](https://zmk.dev/docs/keymaps/behaviors/sticky-layer).

## Proposed validation if implemented later

Do not judge the design only inside Neovim, where Base H/J/K/L already move. Test it in Finder, a browser text field, Ghostty's shell, and Neovim insert mode:

1. Type prose and code containing `h`, `j`, `k`, `l`, and `ll`; Base output must be unchanged.
2. Hold K, tap Z, release K; verify H/J/K/L produce Left/Down/Up/Right repeatedly.
3. Tap Z; verify all four positions immediately return to letters.
4. Hold K and verify Q/P/F/M still provide quick temporary arrows.
5. Invoke Ghostty layout 2 from its relocated Raise position.
6. Verify Escape and every retained Backspace route before flashing becomes the new confirmed physical state.

## Decision

Adopt **dual arrow clusters on Raise** as the next design: retain Q/P/F/M for temporary K-held movement and add physical H/J/K/L for locked, Vim-familiar movement. Do not put hold-taps or tap dances on Base H/J/K/L. Revisit a dedicated Z-held Nav layer only if the K+Z lock gesture proves too costly in daily use.
