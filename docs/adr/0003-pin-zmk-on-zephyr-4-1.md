---
status: accepted
---

# Pin ZMK on Zephyr 4.1

Supersedes [0002](0002-pin-zmk-before-zephyr-4-1.md). The user asked for the latest ZMK with the same setup. The repository now pins ZMK at `9ebbeff0a8b69a42f14aec022cdf16c7a107b9e0`, ZMK main on 2026-09-26, which runs Zephyr 4.1 and Hardware Model V2. The board becomes `nice_nano//zmk` (default revision 2.0.0, the nice!nano v2); the `sofle_left` shield is unchanged.

A source comparison against the previous pin `abb64ba` found no change in the keymap behaviors this layout relies on: hold-tap, tap dance, combos, macros, sticky layer, key toggle, and `&tog` layer locking. The one runtime difference is `&bootloader`, which on the `zmk` board variant now enters the UF2 bootloader through Zephyr's retention boot mode instead of the Adafruit magic reboot value.

## Considered options

- Stay on `abb64ba`: known-good, but frozen before eleven months of fixes.
- Track `revision: main`: any rebuild could pull a breaking change, which ZMK itself warns against.
- Pin the current main commit: latest code, and upgrading remains a deliberate edit. No ZMK release carries Zephyr 4.1 yet (latest is `v0.3`); move to `v0.4` once it exists.

## Consequences

`config/west.yml` and the reusable-workflow ref in `.github/workflows/build.yml` must name the same commit, since the workflow chooses the build image. The single build has an explicit artifact name, `sofle`, instead of the automatic `sofle_left-nice_nano__zmk-zmk`. The Raise+D bootloader hold must be tested on the keyboard after the first flash, with the reset-button double tap as the fallback.
