---
status: superseded by 0003
---

# Pin ZMK after layer locking but before Zephyr 4.1

Layer locking is required for the low-effort “hold X or K, tap Z” workflow, but ZMK main moved to Zephyr 4.1 and Hardware Model V2 soon afterward. The repository pins ZMK at `abb64ba316c29caddc49727ca2cac2f0ed5970c7`: it includes layer locking while retaining the known `nice_nano_v2` board and `sofle_left` shield names. This is the smallest compatible change and avoids an unrelated board-model migration.

## Considered options

- The old pin built with familiar names but lacked layer locking.
- ZMK main had locking but changed the board to `nice_nano//zmk`, causing the existing build to fail with `Invalid BOARD`.
- The selected pre-Zephyr-4.1 revision provides both locking and the established build target.

## Consequences

The GitHub Actions workflow must use a ZMK build image compatible with the pinned revision. Upgrading ZMK is a deliberate migration, not a routine version bump.
