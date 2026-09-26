# Left-only Sofle input system

This context names the parts of a one-handed coding input system built around one physical Sofle half, ZMK, and macOS automation.

## Language

**Base**:
The normal typing layer containing the familiar letter arrangement and five active thumb keys.
_Avoid_: Default layer, layer 0

**Lower**:
The number, punctuation, and editing layer reached by holding X. It can be locked with Z for longer work.
_Avoid_: Number layer, symbol layer, layer 1

**Raise**:
The application, Bluetooth, and recovery layer reached by holding K. It can be locked with Z for longer work.
_Avoid_: Command layer, navigation layer, layer 2

**Navigation/Media**:
The sparse momentary layer reached by holding Y with the pinky: H/J/K/L arrows, O Backspace, P/F/M volume, C/S Command and Shift toggles, and the four Base modifier thumbs. Holding Y and tapping one of these keys selects it at once; holding Y alone selects it after 200 ms. It reuses the internal MEDIA layer and cannot be locked.
_Avoid_: Function layer, layer 3

**Layer leader**:
The Base key held to reach another layer: X for Lower, K for Raise, or Y for Navigation/Media.
_Avoid_: Mode key

**Layer lock**:
A deliberate transition that keeps Lower or Raise active after its leader is released. Hold the leader, tap Z, then release the leader.
_Avoid_: Double-tap mode

**Base peek**:
A temporary return from locked Lower to Base while the physical X position is held. It makes Base letters and Space available without unlocking Lower.
_Avoid_: Temporary unlock

**Bridge key**:
An F13-F19 key emitted by ZMK and consumed by Karabiner to open a macOS application or run a browser action. F18 carries the browser transcript/full-brief action. It is an internal signal, not a user-facing function key.
_Avoid_: Function key shortcut

**Saved firmware**:
The configuration at the Git branch tip, whether or not it has been installed on the keyboard.
_Avoid_: Current firmware

**Confirmed flashed firmware**:
The last revision whose installation on the physical keyboard was explicitly verified.
_Avoid_: Latest firmware
