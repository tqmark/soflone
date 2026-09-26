# Left-only Sofle configuration

This repository contains the ZMK firmware for Mark's left-half-only Sofle and the design record for the surrounding macOS coding setup.

- [Current setup and complete decision history](docs/decision-history.md)
- [Project language](CONTEXT.md)
- [Why the whole system is left-half-only](docs/adr/0001-design-for-one-left-hand.md)
- [Why ZMK is pinned on Zephyr 4.1](docs/adr/0003-pin-zmk-on-zephyr-4-1.md) (supersedes [the pre-4.1 pin](docs/adr/0002-pin-zmk-before-zephyr-4-1.md))
- [Research: H/J/K/L arrow strategy](docs/research/hjkl-arrow-strategy.md)

The source of truth for the saved firmware is [config/sofle.keymap](config/sofle.keymap). The firmware saved in Git can be newer than the firmware physically flashed on the keyboard; the distinction is recorded in the decision history.
