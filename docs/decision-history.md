# Left-only Sofle: current setup and decision history

This is the durable record of the decisions made while adapting the Sofle and the surrounding macOS tools for a programmer who uses only the left hand. It records the current saved design, why it exists, what was superseded, what is known to be physically flashed, and what remains unresolved. Keymap snapshot updated on 2026-09-26.

## Accessibility goal and design rules

- The right hand is not usable. Every required action must be possible with the left hand alone.
- All left-hand fingers are usable. The user confirmed Y and Z are pinky-operated; the previous ring-finger description of Y was incorrect. K is an index-finger key, and O was chosen for index-finger Backspace. Other finger assignments have not been measured.
- The right Sofle half is disconnected and can remain disconnected.
- Preserve the familiar Base letters. Moving frequently used letters to make a theoretically tidy layer is not worth relearning the keyboard.
- Optimize for low fatigue, predictable behavior, recovery from mistakes, and low memory load.
- Prefer holding one key and tapping another over simultaneous multi-key combos.
- Ctrl, Command, and digits 1-6 are especially important for macOS Spaces, Ghostty, and development work.
- Avoid F1-F12 as user-facing keys. F13-F19 are allowed only as internal ZMK-to-Karabiner bridge signals.
- Do not fill empty positions merely because they exist. A sparse layer is safer than an unmemorable layer.

## Hardware and build source of truth

- Keyboard: left half of a Sofle
- Controller: nice!nano v2, built as `nice_nano//zmk` (named `nice_nano_v2` before the Zephyr 4.1 upgrade)
- Firmware: ZMK
- Shield: `sofle_left`
- Saved ZMK revision: `9ebbeff0a8b69a42f14aec022cdf16c7a107b9e0` (Zephyr 4.1, saved on branch `zmk-zephyr-4.1`, not flashed). Both keyboards were built on `abb64ba316c29caddc49727ca2cac2f0ed5970c7` (Zephyr 3.5).
- Build matrix: left shield only; the earlier right-shield build was removed
- OLED: enabled. Saved, not flashed: a custom status screen (`src/status_screen.c`, loaded through `zephyr/module.yml` and `CMakeLists.txt`) with ZMK's built-in layout, but the layer name is plain UNSCII 8 text without the keyboard icon. The top-row icons are ZMK's own widgets in Montserrat 16.
- RGB and encoders: disabled
- Bluetooth profiles: only ZMK profiles 0 and 1 are exposed (previously labeled BT1/BT2)
- Baseline before the flattened-modifier safety change: `362f3bff9ba0c4503625a8daa77b474c61dfec60`
- Last successful build before that safety change: [GitHub Actions run 34733958813](https://github.com/tqmark/sofli/actions/runs/34733958813)
- Firmware name after the safety change: `SofleL-FlatMT`
- One firmware for both keyboards (saved, not flashed): `build.yaml` builds a single `sofle` artifact, and both Sofles advertise `SofleL-FlatMT` over USB and Bluetooth. The old Sofle (`2707E`) still runs the earlier `darksofle` build until it is flashed again. Each keyboard keeps its own Bluetooth address and pairings. macOS keeps the name recorded when a keyboard was paired (or a name set in Bluetooth settings), so a new advertised name may appear only after pairing again. Flash each keyboard with its own artifact.

The full Sofle matrix still appears in `config/sofle.keymap`; the right-side entries are inactive placeholders required by the shield. The layouts below show only the physical left half.

### Automatic power saving

- The OLED blanks after about 30 seconds without activity and turns back on when typing resumes.
- Deep sleep is enabled after 15 minutes of inactivity on battery (`CONFIG_ZMK_SLEEP=y`, `CONFIG_ZMK_IDLE_SLEEP_TIMEOUT=900000`).
- ZMK's activity handler (unchanged by the Zephyr 4.1 upgrade) prevents deep sleep while USB power is present, including USB charging while using Bluetooth.
- On battery, deep sleep disconnects Bluetooth; a matrix key press wakes the keyboard and it reconnects. The wake press may not be typed, and a reboot returns to Base. Saved Bluetooth pairings are retained.
- These settings take effect separately on each keyboard after it is flashed. Real battery sleep/wake behavior still needs a physical test.

### Saved versus flashed

“Saved” means present in Git. “Confirmed flashed” means explicitly verified on the physical board. These are not interchangeable.

Serial transfer and USB reboot were verified separately for both keyboards:

- Old Sofle (serial ending `2707E`): `b246979`, flashed on 2026-09-19 at 13:37 Asia/Ho_Chi_Minh. Serial DFU reported `Device programmed.` and the same serial returned as `SofleL-FlatMT` (USB `1d50:615e`). This replaces `e9f4de5`, changing Lower+E from comma to Backspace while retaining Lower+G Backspace, Raise+Y browser brief, Navigation/Media, all timing, and 15-minute battery sleep.
- New Sofle (serial ending `33F97`): `b246979`, flashed on 2026-09-19 at 13:39 Asia/Ho_Chi_Minh. Serial DFU reported `Device programmed.` and the same serial returned as `SofleL-FlatMT` (USB `1d50:615e`). This replaces `e9f4de5`, adding Lower+E Backspace while retaining all other bindings and timing.
- Old Sofle (serial ending `2707E`): `a6ecdd8`, flashed on 2026-09-26, confirmed at 10:27 Asia/Ho_Chi_Minh, by copying `darksofle.uf2` onto the bootloader volume. It returned as `SofleL-FlatMT` with the same serial (USB `1d50:615e`). This is the first keyboard carrying the hold-based recovery, the faster Navigation/Media, the double-tap modifier toggles and the `darksofle` Bluetooth name. The earlier same-day flash of `2fb9e4d` is superseded.
- The two keyboards no longer run the same firmware: the old Sofle is on `a6ecdd8`, the new Sofle (`33F97`) is still on `b246979`. Their bootloader gestures therefore differ. Physical typing/comfort testing remains separate from transfer verification.
- Lower+E Backspace is merged into main and flashed to both Sofles. Comma remains on the Base comma/Command thumb.
- The native/Sofle Karabiner handlers and browser helper are installed on this Mac. The user confirmed the shortcut worked after enabling System Events Automation permission for the current `Karabiner-Console-User-Server` entry; the separately listed lowercase entry was already enabled but did not authorize the running app. Full-brief mode was not separately confirmed.
- **The bootloader gesture differs per keyboard.** Old Sofle (`2707E`, on `a6ecdd8`): hold K for Raise, then hold D for one second. New Sofle (`33F97`, on `b246979`): hold K for Raise, then press X+G together. Use the gesture for the firmware actually on that board.
- Hardware fallback: double-tap the controller reset button.

## Current saved keymap

### Base

```text
Q        P            F  M  L  J
B        Y/Nav+Media  U  R  S  O
C        D            T  H  E  A
X/Lower  G            V  W  N  I  K/Raise

         Z   /-Option   Esc-Control   comma-Command   Space-Shift
```

- Tap X for `x`; hold X for temporary Lower.
- Tap K for `k`; hold K for temporary Raise.
- Tap Y for `y`. Hold Y and tap a Navigation/Media key for that action immediately, or hold Y alone for 200 ms. Release Y to leave it. Y pressed within 150 ms of typing is always `y`.
- Hold X or K and tap Z to lock that layer. Tap Z while locked to return to Base.
- Tap `/` for slash; hold it for Left Option.
- Tap Esc for Escape; hold it for Left Control.
- Tap the comma thumb for comma; hold it for Left Command.
- Tap Space for Space; hold it for Left Shift.
- Enter is X+Space through Lower. Period is X+comma through Lower; the old duplicate Lower+I period is now right bracket (`]`).
- Hold-tap timing is 200 ms. No tap dances remain on any layer.
- X and K use hold-preferred layer-taps so a following key selects the layer immediately instead of waiting 200 ms.

### Lower

Hold X for temporary access. Hold X, tap Z, and release X to lock it.

```text
1          2          3  4       5          6
7          8          9  0       -          =
'          unused     ;  Tab     Backspace  Ctrl+A
\ / Base   Backspace  \  unused  [          ]       `

           Z-toggle   /-Option   Esc-Control   Period-Command   Enter-Shift
```

- Digits are arranged in reading order, making Ctrl+1 through Ctrl+5 and Cmd+1 through Cmd+6 available from one hand.
- Lower+E and Lower+G are Backspace: from Base, hold X first and tap E or G. X resolves to Lower as soon as the following key is pressed. With Lower locked, E or G alone is Backspace. Lower+D remains unused and L+J remains removed. Navigation/Media+O is also Backspace from Base; Y directly on Lower still types `8`.
- The bootloader is no longer a combo, so the X-then-G deletion gesture cannot enter it even if Raise is locked by mistake.
- The physical X position taps backslash. While Lower is locked, holding it temporarily reveals Base; release it to return to Lower. This is the route to Base letters and a normal Space without unlocking.
- The comma thumb taps period and holds Command on Lower. The Space thumb taps Enter and holds Shift. A direct Lower Space was removed.
- Apostrophe, semicolon, brackets, backslash, slash, period, and grave are directly available on Lower. Comma remains on the Base Command thumb: release momentary Lower first, or use X's Base peek when Lower is locked. Add Shift on Base for `<`.
- Shift-generated variants such as `+`, `_`, colon, double quote, braces, question mark, and tilde are not duplicated as dedicated keys.
- Lower+H is Tab. Add the Shift thumb for Shift+Tab; the dedicated Lower+W Shift+Tab was removed and W is unused.
- Lower+A sends Ctrl+A, matching the physical A position. In Ghostty, hold X, tap A and then Q/P/F for leader 1/2/3. For pane movement, hold X, tap A, release X, then tap Base H/J/K/L. Outside Ghostty this sends ordinary Ctrl+A and follows the active application's binding.
- Lower+V is backslash; Shift gives pipe. It is reachable while X remains held, unlike the backslash on the X position itself. Slash remains on the Option thumb. Lower+N/I supply adjacent brackets (`[` and `]`); Shift gives `{` and `}`. Lower+E supplies Backspace, and Lower+K retains backtick.

For Ctrl+1, hold X, hold the Esc/Control thumb, and tap physical Q. Ctrl+2 through Ctrl+6 use P, F, M, L, and J. The same positions work with the Command thumb.

### Raise

Hold K for temporary access. Hold K, tap Z, and release K to lock it.

```text
BT0       BT1          Finder   unused       unused    unused
Browser   Brief        unused   unused       Settings  unused
Chat      Bootloader*  Ghostty  unused       unused    unused
unused    unused       unused   Clear BT*    Notes     OLED on   Esc

* hold for one second; a tap does nothing

          Z-toggle  /-Option  Esc-Control  comma-Command  Space-Shift
```

- Q/P select ZMK Bluetooth profiles 0/1, respectively. These are the same physical positions that produce 1/2 on Lower, and the same saved profiles previously labeled BT1/BT2. Individual V/W bindings are now unused.
- Hold K+B/T/C/F/N/S to open Browser, Ghostty, the Telegram/Slack toggle, Finder, Notes, or Settings. F still emits the existing Finder bridge F19, so Karabiner needs no change.
- Hold K and tap Y for the active browser's YouTube transcript. Add the Shift thumb for the full brief. Y emits F18 on Raise; Karabiner handles F18/Shift+F18 only from the Sofle and only in supported browsers. Base Y Navigation/Media is unchanged. This bridge needs the newly built firmware, not just the Karabiner update.
- Duplicate arrows, Shift+arrow selection, Backspace, and forward Delete were removed from Raise. Navigation and Backspace now belong to Y; use its Shift thumb for selection in supporting apps. Forward Delete was explicitly rejected. The earlier Home/End and direct Ghostty layout macros remain removed. Freed positions stay unused.
- Raise+I turns external power on to recover the OLED.
- Physical K on Raise taps Escape immediately. Z is the only Raise exit.
- The Esc/Control thumb on Raise is a plain mod-tap so Ctrl chords are not delayed. Z is the reliable return to Base.
- Base V+W gives one-shot Raise for one command.
- Hold Raise+W for one second to clear the selected Bluetooth profile; hold Raise+D for one second to enter the bootloader. Tapping either does nothing. W and D are unused on Lower and Navigation/Media, so neither is reached by Lower muscle memory, and neither is a combo.

### Navigation/Media

Hold Y with the pinky and tap:

```text
P/F/M    Volume Down / Volume Up / Mute
H/J/K/L  Left / Down / Up / Right
O        Backspace
C / S    double-tap within 300 ms: hold Command / Shift (double-tap to release)
```

- This reuses the existing fourth layer; there is no fifth layer or new letter hold-tap. The internal `MEDIA` index and `ymedia` behavior remain unchanged; the OLED label is `Nav/media`.
- The user confirmed Y is a pinky key, leaving physical H/J/K/L available as arrows. Holding K cannot offer K/Up; Y avoids that physical conflict. O is index-finger Backspace, alongside Lower+E/G.
- P/F/M keep the three volume actions together. L is now Right and J is Down. A is unused: there is no forward Delete on the active left half.
- C and S are double-tap key toggles for Command and Shift, for Cmd+click, Shift+click and similar trackpad use with one hand. Hold Y, tap C twice within 300 ms, use the trackpad, then double-tap again to release. A single tap emits nothing, so a stray Y+C cannot strand a modifier. This is firmware-only; macOS Sticky Keys stays off. Releasing Y between the two taps types an ordinary `c`/`s`. The OLED does not show held modifiers, so a forgotten toggle shows up as modified typing: nothing else clears it, because ZMK counts modifier presses and the Command thumb's own press/release leaves the count above zero.
- Slash/Option, Escape/Control, comma/Command, and Space/Shift are direct mod-taps matching Base. Shift+arrows selects in supporting apps; Option or Command modifies movement according to the application. These are not Vim Visual-mode macros.
- Y is a balanced hold-tap with three guards instead of a mandatory 200 ms dwell. Y pressed within 150 ms of another key is always `y` (mid-word rolls such as `days`). Navigation/Media engages only if the first key after Y is a Navigation/Media key or modifier thumb; most Y-initial words (`yes`, `yet`, `year`) continue on E/A/U/I, so they always type. And that key must be released while Y is still held, so a rolled Y+key stays two letters.
- Known risk: O is a trigger for Backspace, so `you`/`your` at the start of a line after a pause sends Backspace if O is released while the pinky still holds Y. Mid-sentence `you` is protected by the 150 ms rule; an ordinary roll releases Y first. Holding Y alone for 200 ms still selects the layer.
- Consequence: after typing, pause about 150 ms before holding Y for arrows. The first arrow fires on its release, not its press; holding it for repeat starts once Y has been held 200 ms.
- Unused left positions, including X and Z, do nothing. Physical K sends Up, not Raise. There is no lock; releasing Y removes only this layer and normally returns to Base. Leave Lower/Raise first to reach the Base Y leader.

### Combos

- Base Q+P: grave accent
- Base B+Y: Tab
- Base V+W: one-shot Raise

There are no destructive combos. Raise V+W (clear Bluetooth) and Raise X+G (bootloader) were removed on 2026-09-26; see the chronology.

The benign combos are scoped to Base because ZMK combos follow physical positions, not letters. Without scoping, Q+P would overlap Lower 1+2 and Raise BT0+BT1, and B+Y would overlap Lower 7+8. L+J no longer triggers a combo on any layer: on Base it sends the normal letters. Caps Lock and Caps Word were removed because they were not needed.

## macOS integration decisions

The complete personal configuration files are intentionally not copied into this firmware repository. The reusable browser-brief rule fragment and wrapper are versioned under `macos/karabiner/`; this section records their contract and the other integrations with ZMK.

### Karabiner-Elements

Live configuration: `~/.config/karabiner/karabiner.json`; launcher script: `~/.config/karabiner/open_apps.sh`.

- On the native Mac keyboard, Caps Lock taps Escape and holds Control with a 200 ms alone timeout.
- Right Option maps to Left Control.
- Native Space+B/T/N/C/S/F simultaneous chords open Browser, terminal, Notes, the Slack/Telegram toggle, Settings, and Finder. Space+M remains normal typing. The chords use a 30 ms window and exclude only the Sofle device (VID `0x1d50`, PID `0x615e`); they work in terminals too. When Vivaldi is frontmost, Space+B searches its open tabs instead of launching.
- The Sofle emits F13-F17 and F19 from Raise. Karabiner maps them to Browser, Ghostty/Terminal, Notes, the Slack/Telegram toggle, Settings, and Finder. Raise+Y now emits F18 for the browser transcript action; Shift+F18 requests a full brief. These internal bridges keep actions away from user-facing F1-F12 and avoid Space/Shift ambiguity on the Sofle.
- Native Space+Y / Shift+Space+Y run transcript / full brief in Vivaldi, the only browser in the Brewfile. They use a 30 ms simultaneous window like the existing native app launchers and exclude the Sofle; F18 handlers require the Sofle device. No global Space hold behavior was added.
- Both brief front-ends call `~/.config/karabiner/browser_brief.py`, which reads the active supported browser tab via AppleScript and passes an explicit validated YouTube URL to the existing `~/.local/bin/brief` (`-t` for transcript). It does not type `yy` or read the clipboard. The existing brief tool writes its result to the clipboard. macOS Automation approval may be required on first deliberate use.
- C is the only chat shortcut. When Slack is frontmost, it opens Telegram; when Telegram is frontmost, it opens Slack; when neither is frontmost, it opens Telegram if installed and otherwise Slack. K+C uses it on the Sofle and native Space+C uses it on the Mac keyboard. Apple Messages is not used.
- Ctrl+N/P becomes Down/Up outside Ghostty and Apple Terminal.
- Left Option+H/L focuses the previous/next macOS window in the current Space.
- Cmd+Tab and Cmd+Shift+Tab are disabled globally. No general replacement for selecting an arbitrary running application has been chosen; this is a gap.
- Holding Right Command+Space for 150 ms temporarily reveals the menu bar and sends Escape on release.

### Rectangle

Rectangle remains configured on macOS, but the Sofle no longer dedicates keys to it. Lower+H is Tab; the former almost-maximize and restore positions G/W are unused. Ctrl+A uses physical A. No Rectangle or native-keyboard settings were changed by this firmware redesign.

### Ghostty

Live configuration: `~/.config/ghostty/config`; layout helper: `~/.config/ghostty/ghostty-layout`.

- Ctrl+A is a one-shot leader.
- Leader then H/J/K/L moves between splits; N/P changes tabs; R reloads the config; S enters persistent resize mode.
- Ctrl+A twice sends a literal Ctrl+A. Escape cancels the leader.
- Resize mode uses H/J/K/L or arrows and exits with Escape or Q.
- Leader then 1/2/3 creates a two-thirds split, equal halves, or a six-pane grid.
- The three direct Raise layout macros were removed. Lower+A now provides Ctrl+A without automatically sending a following command.
- Window, tab, and split state is restored on launch.

Ghostty has no action for running the layout helper directly, so its binding types a shell command. It is safe only at a shell prompt; invoking it while Neovim, Claude, or another interactive program owns the pane can type unwanted text. That risk is accepted for now and should remain visible.

### Neovim

Live configuration: `~/.config/nvim`. Space is the Neovim leader.

- `[b`/`]b`: previous/next buffer; Space+B,D deletes a buffer.
- Space+W saves.
- Escape clears search highlighting.
- Ctrl+D/U scrolls half a page and recenters.
- Space+F,F/F,G/F,B/F,H/F,R/F,S opens file, grep, buffer, help, recent-file, and symbol searches; Space+/ searches the current buffer.
- `[d`/`]d` moves between diagnostics; `[h`/`]h` moves between Git hunks.
- Space+Y/P uses the macOS clipboard.
- Alt+J/K moves lines or selections.
- Ctrl+arrows resizes Neovim windows.

The firmware preserves quick Escape, Control, Space, and movement access because these mappings make them more valuable than isolated shortcut keys. Y+H/J/K/L send standard arrows; use the Shift thumb for applications that select with Shift+arrows. Use normal Base H/J/K/L and Vim Visual mode for Vim-native movement/selection unless the editor is explicitly configured otherwise.

## Decision chronology

### 2025: establish the personal layout

- `8a7763e` created the standard Sofle ZMK repository, including Base, Lower, Raise, Adjust, both halves, RGB-era bindings, and the original build workflow.
- `653aa6e` installed the familiar Q/P/F/M/L/J letter layout, added Q+P grave, L+J Delete, B+Y Tab, and began experimenting with multi-role thumb keys.
- `9102619` changed L+J from forward Delete to Backspace, matching the more frequent editing need.
- `2a0d91a` and `3047bf7` enabled and corrected the OLED setting.
- `00799d9` through `7c04858` iterated on comma, slash/Option, Enter/Command, Space/Shift/period, I/K/Z tap dances, number placement, and ways to enter or leave Lower and Raise. These were exploratory and are superseded by the current bindings.
- `bad25d5` established the reading-order 1-6 / 7-0 number rows and moved slash onto the Option thumb. This became the basis of the current Lower layer.
- `67e795b` and `7c04858` continued layer-transition and slash experiments. Direct layer jumps and letter tap dances from this period were later removed.

### 2026-09-07: make left-only use the governing constraint

- `87ad78c` explicitly redesigned the left half as the whole usable keyboard. It added a one-shot app layer, left-side navigation/editing, sticky modifiers, Caps Word, and F13-F19 app bridge keys.
- `825f311` tried the board naming required by then-current ZMK main.
- `1b43206` removed the right-shield build, Adjust, and the separate app layer to keep only three learnable layers. App bridge keys moved into Raise.
- `7a2dcef` made layer access available by holding letter keys as well as locking them.
- `91216d7` through `6e15438` explored Z as Lower and K as Raise, including double-tap locking. The goal was temporary access by hold and persistent access by deliberate repetition.
- `f1efe42` through `b94f869` refined Lower: underscore was tried, Base-like thumbs were restored, and redundant shifted symbols were replaced with editing actions because Shift can already produce them.

### 2026-09-08: integrate the coding desktop and recovery path

- `bf0829d` placed four Rectangle commands on Lower for one-handed window control.
- `1e00336` added firmware macros for Ghostty's Ctrl+A then 1/2/3 layouts.
- `f8440b2` and `128001d` rearranged Raise application/Bluetooth functions, restored Base-like Raise thumbs, and added direct external-power/OLED recovery.
- `e1e5fa1` and `cb62760` temporarily returned to a legacy ZMK revision and matching workflow so `nice_nano_v2` would build.
- `6abbfae`, `424283c`, and `851697a` temporarily reset stored settings to recover a blank OLED, then restored normal persistence so Bluetooth and settings would not be erased on every boot.
- `3c2c185` and `6e14cb2` made Z and K layer-lock controls and established Z as the universal way back to Base.
- `93b9af0` moved Lower from Z to X. This preserved Z as a simple emergency exit and allowed X to own typing/numbers while K owned commands/navigation.
- `c900027` through `43e832d` tested faster hold and double-tap windows: 150 ms holds, 125 ms double taps, then 175/150 ms. The final design later settled at 200 ms holds and 175 ms tap dances after real use.
- `027283f` briefly made hold-Z a special Control-plus-number workflow for macOS Spaces. `a49b107` removed it because Z was more valuable as a simple Base key and reliable layer exit; Ctrl+numbers remain reachable through Lower and the Control thumb.

### 2026-09-09: settle punctuation, editing, arrows, and applications

- `7ae4301` made comma the primary thumb tap and Enter its double tap, reversing an earlier Enter-first design.
- `848ac33` set 200 ms holds and 175 ms double taps, the present timing.
- `b685354` added direct Enter access on Lower and moved forward Delete to a safer Raise location.
- `bea1f04` made the Lower Space-position thumb Enter when tapped and Shift when held. Lower no longer needs a duplicate direct Space.
- `522cf5c` made Raise+J Backspace, following the preference for holding a leader and tapping J.
- `9467728` moved arrows to Q/P/F/M so their physical arrangement reads Left/Down/Up/Right like Vim movement.
- `aeb1509` placed Messages on Raise+X and Finder on Raise+G.

### 2026-09-10: improve thumb familiarity and locked-Lower recovery

- `beb4a1e` swapped the Option and Control thumb positions without changing their behaviors. The current order is slash/Option then Escape/Control.
- `076a61a` added the locked-Lower Base peek on physical X so Space and Base letters remain reachable without fully leaving Lower.
- `e7c3e87`, `1570365`, and `28b2d85` fixed the ZMK encoding of that behavior for the pinned schema. `28b2d85` is the last firmware revision explicitly reported as physically present.
- `c3a42b1` simplified Bluetooth to the two profiles actually used and tried easier X double-tap Lower locking.
- `a8fc23d` restored its 175 ms double-tap window.

### 2026-09-11: remove unreliable nested tap dances

- `a357671` removed X/K double-tap layer locking. A tap-dance wrapped around a layer-tap first waited for the dance, then for the hold-tap, and could leak the following Base letter before the layer became active. X and K became plain hold-preferred layer-taps; locking moved to “hold leader, tap Z.”
- The same change scoped harmless combos to Base, added dedicated Lower+D Backspace, moved Bluetooth clear and bootloader away from editing keys, and removed obsolete slash and I tap dances.
- `9a521cc` pinned the last suitable pre-Zephyr-4.1 ZMK revision: new enough for locking, old enough for `nice_nano_v2` and `sofle_left`.
- `82ad09a` simplified the saved bootloader chord to Raise X+G.
- `743fc85` tried balanced modifier hold-taps to improve modifier chords. This was later reverted because balanced waits for the other key's release and made held Ctrl+Space slower rather than faster.

### 2026-09-13: add focused media access

- `c16618c` first placed volume controls on Raise, but they displaced more valuable Raise functions.
- `362f3bf` created the fourth sparse Media layer: Q+F/M/L/J for volume down, mute, volume up, and Backspace. Positional hold triggers protect normal Q typing, the layer is momentary only, and Raise stays intact.
- The same change restored modifier hold-taps to hold-preferred so modifiers resolve when the next key goes down. Space retains its tap-dance because Ctrl+Shift worked in use and double-tap period remained useful.

### 2026-09-14: flatten modifier thumbs after the hold-tap audit

- A source-level audit of the pinned ZMK revision showed that a tap dance creates its nested mod-tap only when the dance resolves. The interrupting key has already passed the hold-tap listener, so fast Shift+letter could remain lowercase and a following hold-tap could be lost.
- Space/Shift, comma/Command, and Raise Escape/Control became direct `&mt` bindings. Double-tap period, Enter, and Raise-to-Base were removed from those positions.
- Enter remains readily available as X+Space. Period is X+comma, matching the preferred hold-then-tap gesture; Lower+I remains a duplicate period for now. Z remains the Raise recovery key.
- The firmware name became `SofleL-FlatMT`, and CI gained a structural check that rejects any future custom behavior wrapping `&mt`.
- The final K tap dance on Raise was also removed. K now sends immediate Escape, Z remains the exit, and CI rejects every tap dance on every layer.
- The shared Karabiner chat launcher became a Slack/Telegram toggle based on the frontmost app. A separate direct-Telegram action was rejected: C is the only chat shortcut, K+X is unused, and native Space+M remains normal typing.
- The Media leader moved from top-row Q to second-row Y for an easier hold. It was initially documented as ring-finger-operated; the user corrected this to pinky on 2026-09-18. Unlike the former instant positional trigger, Y requires a deliberate 200 ms hold so quick Y rolls cannot trigger commands.

### 2026-09-17: automatic battery sleep

- Enabled the pinned ZMK deep-sleep support after 15 minutes idle so an unused keyboard consumes less battery overnight. The existing 30-second OLED blanking remains; USB power prevents deep sleep. The firmware must be flashed to each Sofle separately.

### 2026-09-18: simplify Lower and Raise around daily actions

- The user confirmed Browser, Ghostty, Telegram/Slack, Finder, Notes, and Settings on B/T/C/F/N/S, and requested both easier Tab/Ghostty leader access and movement/selection.
- Lower's three unused Rectangle keys initially became Tab, Ctrl+A, and Shift+Tab. The user then requested Ctrl+A on physical A: it moved from G to A, right bracket moved from A to I, and G became unused. V became backslash to solve the X-held reach conflict; slash remains on its thumb. The duplicate Lower+I period was removed.
- The user requested brackets next to each other: left bracket moved from Lower+E to Lower+N beside right bracket on I, and comma moved from N to E. Ctrl+A remains on A.
- Finder moved from Raise+G to Raise+F; Up moved from F to U while Left/Down/Right stayed on Q/P/M. Raise+D/H became Shift+Left/Right. The three Ghostty layout macros and Home/End were removed.
- Base, numbers, thumb behaviors, Media, layer locking, Bluetooth profiles, recovery combos, and deep sleep are unchanged. Remaining empty positions are deliberate.

### 2026-09-18: pinky-held Navigation/Media and leaner Lower/Raise

- The user confirmed Y is a pinky key, chose O for index-finger Backspace, and requested P/F/M as Volume Down/Up/Mute. The existing Y-held fourth layer now also puts arrows on physical H/J/K/L. No new leader, fifth layer, forward Delete, or tap dance was added.
- Navigation/Media gained the four Base modifier thumbs for selection and modified movement. Y retains its deliberate 200 ms tap-preferred hold; X/K and modifier timing are unchanged. Z remains the Lower/Raise lock/exit key and is inactive on Navigation/Media.
- Removed Lower+D Backspace and Lower+W Shift+Tab. Tab remains H; Shift+Tab uses the Shift thumb. Removing Lower Backspace means leaving Lower (or using Base peek) before Y+O.
- Raise keeps the six app bridges, OLED recovery, Escape, and its existing thumb/lock behaviors. The two existing Bluetooth selectors moved from V/W to Q/P and are now explicitly labeled BT0/BT1. Removed duplicate arrows, selection, Backspace, and forward Delete. V+W still clears the selected Bluetooth profile; X+G still enters the bootloader, only on Raise.
- Numbers, adjacent Lower brackets N/I, Lower+A Ctrl+A, Lower+E comma, Base typing/combos, right-half placeholders, and battery sleep remain unchanged. The new Sofle is still confirmed on c3b6c26; this newer design requires a separate flash.
- The user then requested removal of the Base L+J Backspace combo. It was removed without changing any layer bindings or other combos; Y+O is now the only Backspace binding on the active left half. Base L/J are ordinary letters, including when pressed together.
- At the user's request, main was fast-forwarded to the tested `9b9d69e` revision and that exact firmware was flashed to the new Sofle (`277D64B1BE733F97`) at 15:12. Build [35319954561](https://github.com/tqmark/soflone/actions/runs/35319954561) passed. The application-only serial DFU package matched UF2 SHA-256 `217d716493dcacf6eb1d9d6b786efa61444227ce4a9ed7f20917b00b4fcaa056`; successful transfer and USB restart were verified. The old Sofle was not connected or updated.
- At 15:15, the user connected the old Sofle (`7DF33F115102707E`) in bootloader mode and requested the same firmware. The identical `9b9d69e` application was programmed over `/dev/cu.usbmodem1101`; `Device programmed.` and the return of the same serial as `SofleL-FlatMT` were verified. Both keyboards now have the same tested firmware; no pairings were cleared or bootloader updates requested.

### 2026-09-19: add Backspace to the familiar X-held layer

- The user reported not getting used to Y+O. After discussing E/A alternatives and X+K, the user chose X+G: Lower+G was unused, so no punctuation or other action needed moving.
- Lower+G now sends Backspace. The gesture is hold X first, then tap G, using the existing hold-preferred Lower behavior. This also makes deletion available while typing numbers without leaving Lower. In locked Lower, G alone deletes backward.
- Y+O remains available, L+J remains removed, Lower+K remains backtick, and all other layers, timing, thumb modifiers, Bluetooth actions, and recovery combos remain unchanged. In particular, X+G on Raise is still bootloader, not Backspace.
- At the user's request, main was fast-forwarded to tested revision `7a9de84` and the exact application was flashed to the new Sofle (`277D64B1BE733F97`) at 12:15. Build [35423210707](https://github.com/tqmark/soflone/actions/runs/35423210707) passed; UF2 SHA-256 is `ae23ec460b9c13e5510929d524907fb137406004e7751ae4af655dbb71bc6f68`. Serial DFU reported `Device programmed.` and the same serial returned as `SofleL-FlatMT`. The old Sofle was not updated and remains on `9b9d69e`.

### 2026-09-19: restore browser brief on native and Sofle keyboards

- The user identified a missing Space+Y shortcut. The active Karabiner profile contained no Y/brief action and Raise+Y was unused. Older backups documented transcript mode on Space+Y and full brief on Shift+Space+Y. The `brief` helper was still installed.
- Added Raise+Y F18 and browser/device-scoped Karabiner rules for F18/Shift+F18 plus native Space+Y/Shift+Space+Y. All other firmware bindings, hold timing, recovery gestures, app bridges, and existing Karabiner rules were preserved.
- Replaced the old Vimium `yy` plus clipboard-delay sequence with a small wrapper that reads the active browser URL, validates a YouTube host, and invokes the existing brief tool with an explicit URL. This avoids typing into the page and stale clipboard fallback. The existing transcript-fetching tool was not modified or executed during testing.
- Added a cross-configuration regression check, mocked helper tests, and CI coverage. The live missing-rule check first failed with `Expected 4 browser brief handlers, got 0`, then passed after installation. Karabiner lint and AppleScript compilation passed; live browser/transcript behavior remains untested. The original personal config was backed up as `karabiner_20260919_before_browser_brief.json` before adding the two rule groups.
- Mac-side changes are installed. At the user's request, main was fast-forwarded to tested revision `e9f4de5` on 2026-09-19. Build [35424169390](https://github.com/tqmark/soflone/actions/runs/35424169390) passed. UF2 SHA-256: `2dc0a8ec2a730ca161fb3e79a046c451f3b196e8ed7eec0c5bff503c71b13984`.
- At 12:55 Asia/Ho_Chi_Minh, the application-only serial DFU package was flashed to the new Sofle (`277D64B1BE733F97`) on `/dev/cu.usbmodem1101`. The updater reported `Device programmed.` and the same serial returned as `SofleL-FlatMT` (USB `1d50:615e`). No bootloader or SoftDevice replacement was performed. The old Sofle remains on `9b9d69e`; actual K+Y/Shift+K+Y browser output remains a user test.
- Subsequent live attempts reached the helper but failed at System Events access. The screenshot showed the current `Karabiner-Console-User-Server` Automation entry disabled, unlike the separate lowercase entry. After enabling the current entry, the user reported success. This was a Mac permission issue, not a firmware defect; static/mocked tests had not exercised the actual Karabiner permission context.
- At the user's request, the same verified package was reflashed to the new Sofle at 13:27, then flashed to the old Sofle (`7DF33F115102707E`) at 13:29. For each transfer, SHA-256 verification passed, serial DFU reported `Device programmed.`, and the same serial returned as `SofleL-FlatMT`. Both now run `e9f4de5`; the old keyboard also gains the earlier Lower+G Backspace change.

### 2026-09-19: add Backspace on Lower E

- After confirming Lower+E was comma, the user requested Backspace there. Hold X, then tap E to delete backward; in locked Lower, E alone deletes backward. Holding E on Lower can repeat deletion according to the host settings.
- Lower+G and Navigation/Media+O Backspace remain available. Base E, the Base comma/Command thumb, all timings, modifiers, other bindings, and Raise X+G bootloader are unchanged. Comma and `<` now require Base rather than a direct Lower key.
- The layout regression check failed with `lower_layer physical E: expected &kp BACKSPACE, got &kp COMMA` before the binding change, then passed. Build [35426918202](https://github.com/tqmark/soflone/actions/runs/35426918202) passed; a normalized comparison confirmed this was the only functional firmware change.
- At the user's request, main was fast-forwarded to `b246979` and its application-only package was flashed to the old Sofle (`7DF33F115102707E`) at 13:37 Asia/Ho_Chi_Minh on `/dev/cu.usbmodem1101`. UF2 SHA-256: `7bc02cc6d42e7aaf8031363a716d3d4ea9dc33b6df0af3b466ad1abd9000bab9`. The updater reported `Device programmed.` and the same serial returned as `SofleL-FlatMT` (`1d50:615e`). The new Sofle remains on `e9f4de5`.
- At 13:39, the user connected the new Sofle (`277D64B1BE733F97`) in bootloader mode and requested the same update. The identical application-only package passed SHA-256 checks, serial DFU reported `Device programmed.`, and the same serial returned as `SofleL-FlatMT` (`1d50:615e`). Both keyboards now have `b246979`; no bootloader or settings-reset image was used.

### 2026-09-26: remove destructive combos, faster Navigation/Media, trackpad modifier toggles

- A source review of the pinned ZMK found that pressing Base V+W twice within about a second cleared the selected Bluetooth pairing. The first V+W starts one-shot Raise, which stays active until a key sends a keycode or 1000 ms pass; combos match against the highest active layer (`combo.c`), so the second V+W matched Raise's `clear_bluetooth`. Retrying a chord that seemed not to work was enough. Raise X+G bootloader shared the same weakness and also collided with the Lower X-then-G Backspace habit when Raise was locked by mistake.
- Both combos were removed. Clear Bluetooth is now a one-second hold on Raise+W and the bootloader a one-second hold on Raise+D: tap-preferred hold-taps with `&none` as the tap, on positions unused on Lower and Navigation/Media. CI now rejects any destructive combo.
- The user could not get used to Y+O Backspace behind the mandatory 200 ms dwell and wanted faster Navigation/Media. Y became balanced with `require-prior-idle-ms = 150` and `hold-trigger-key-positions` limited to the Navigation/Media keys and modifier thumbs. O Backspace was briefly removed to make `you` unconditionally safe, then restored at the user's request, accepting the start-of-line `you` risk described under Navigation/Media.
- The user uses Command and Shift with the trackpad on the native keyboard, which one hand cannot do while holding a key. Navigation/Media C and S now toggle Command and Shift. They sit on Navigation/Media because it cannot be locked; on Raise a mistaken Lower-habit tap could leave Command held.
- Thumb-roll misfires under `hold-preferred` were tested by the user and occur only at very high speed, so the thumb mod-taps were left unchanged.
- Not yet flashed. Both Sofles remain on `b246979`, whose bootloader is still Raise X+G.

### 2026-09-26: flash the old Sofle, then require a double tap for the modifier toggles

- The user flashed the `darksofle` artifact from build [36213670628](https://github.com/tqmark/soflone/actions/runs/36213670628) (revision `2fb9e4d`) to the old Sofle (`7DF33F115102707E`) by copying the UF2 to the bootloader volume, and reported it working. Before flashing, both UF2 files were verified: correct magic numbers, the `0xADA52840` family, load address `0x26000`, and the expected name in each image. This keyboard therefore runs the hold-based recovery, faster Navigation/Media, and Y+O Backspace. The new Sofle (`277D64B1BE733F97`) remains on `b246979`, whose bootloader is still Raise X+G. Physical typing tests remain separate from installation verification.
- That build set `CONFIG_ZMK_KEYBOARD_NAME`, which feeds the USB product name, the Bluetooth name and the device model at once. The user wanted only the Bluetooth name changed, so `build.yaml` now overrides `CONFIG_BT_DEVICE_NAME` alone; build [36214036089](https://github.com/tqmark/soflone/actions/runs/36214036089) passed but is not flashed. macOS keeps the name recorded at pairing time, so the old Sofle still shows as its paired name until it is paired again.
- The user judged the single-tap modifier toggles too powerful to leave on one tap. Navigation/Media C and S became tap dances: a single tap emits nothing, a double tap within 300 ms flips Command or Shift. This is the first tap dance since the 2026-09-14 audit removed them all. It is admissible because the audit's failure needs a hold-tap nested in the dance: the dance creates the mod-tap only after it resolves, by which time the interrupting key has passed the hold-tap listener. These dances wrap `&none` and `&kt`, so no hold-tap is created and a single tap has nothing to leak. Both checks were narrowed from "no tap dances at all" to "no tap dance may wrap anything but `&none`/`&kt`, and it must start with `&none`", and were confirmed to reject a mod-tap, a hold-tap and a reordered dance.
- Flashed to the old Sofle (`2707E`) as revision `a6ecdd8` from build [36214470304](https://github.com/tqmark/soflone/actions/runs/36214470304), by copying the UF2 to the bootloader volume. Both images were verified first: UF2 magic and final magic on every block, family `0xADA52840`, load address `0x26000`, and `darksofle` present once against `SofleL-FlatMT` twice, confirming the Bluetooth-only rename. macOS reported the keyboard back as `SofleL-FlatMT` on serial `7DF33F115102707E`. Bluetooth still lists the previously paired name until the keyboard is paired again.

### 2026-09-26: upgrade ZMK to Zephyr 4.1

- The user asked for the latest ZMK with the same setup. ZMK is pinned to main at `9ebbeff` (Zephyr v4.1.0+zmk-fixes, Hardware Model V2) instead of `abb64ba`, and the reusable build workflow moves to the same commit. No ZMK release carries Zephyr 4.1 yet. See [ADR 0003](adr/0003-pin-zmk-on-zephyr-4-1.md).
- The board is renamed from `nice_nano_v2` to `nice_nano//zmk` (default revision 2.0.0, the same hardware). The `sofle_left` shield, keymap, `sofle.conf` options and every binding are unchanged. The unused, deprecated `label` was removed from `lower_bslash_base`.
- A source diff between the two ZMK commits found no change to hold-tap, tap dance, combos, macros, sticky layer, key toggle, `&tog` layer locking, or the USB-powered sleep exception. `&bootloader` now enters the UF2 bootloader through Zephyr's retention boot mode on the `zmk` board variant, so Raise+D needs a physical test after flashing.
- Per-keyboard names were briefly `darksofle`/`lightsofle`. A byte comparison of the two images showed they differed only in the name string and the one-byte shift it causes. ZMK compiles the Bluetooth name into the firmware, so different names require different files. The user chose one file for both keyboards instead: a single `sofle` artifact, both named `SofleL-FlatMT`. This also replaces the automatic `sofle_left-nice_nano__zmk-zmk` file name.
- Saved on a branch, not flashed. The old Sofle stays on `a6ecdd8` and the new Sofle on `b246979`, both on Zephyr 3.5, until the user flashes the upgrade.
- The user found the OLED layer name too bold and wanted only its first letter capitalised. The layer name font changed from Montserrat 12 to UNSCII 8 (`CONFIG_ZMK_LV_FONT_DEFAULT_SMALL_UNSCII_8`), whose strokes are one pixel wide. The names are now `Default`, `Lower`, `Raise` and `Nav/media`. The top-row icons stay in Montserrat 16, because the built-in status screen draws them from that font and UNSCII has none of them. A bold or custom font would need a custom status screen and was not pursued.
- The user then asked to remove the keyboard icon in front of the layer name. ZMK hard-codes it in its layer widget, and UNSCII 8 has no glyph for it, so it would have drawn as a placeholder box. The repository now provides its own status screen: the same layout and ZMK's own battery and output widgets, with a plain-text layer name. The settings the built-in screen used to switch on (icon widgets, mono theme, Montserrat 16 default font, 4096-byte LVGL pool) are restated in `config/sofle.conf`. This is the repository's first C code; a ZMK upgrade must check it still builds against the display API.

## Decisions deliberately rejected or superseded

- Reconnecting or depending on the right half: conflicts with the physical requirement.
- A full Adjust layer: unnecessary complexity for the currently enabled hardware.
- A separate full Apps layer: merged into Raise to reduce layer count.
- Caps Lock or Caps Word: not needed; X+G is no longer assigned to capitalization.
- User-facing F1-F12: conflicts with the preference to preserve them and avoid function-row semantics.
- Dedicated shifted symbols already produced by Shift: uses scarce positions without adding capability.
- Z as the Lower leader or special Ctrl+number leader: overloaded the universal recovery key and the pinky.
- X/K double-tap locks: unreliable and slow when implemented as tap-dance around layer-tap.
- Lower direct Space: replaced by two useful Enter positions plus the locked-Lower Base peek.
- Bootloader on L+J: too close to the well-trained Backspace chord and could unexpectedly remove HID service.
- Bluetooth clear beside arrow and deletion keys: too destructive for an editing cluster.
- Destructive combos of any kind: a Base combo's one-shot Raise turns a repeated chord into a Raise combo. Destructive actions are one-second holds instead.
- ZMK main (superseded 2026-09-26): once rejected because it forced the Zephyr/board-model migration. That migration is now done on purpose, pinned to one commit. Tracking `revision: main` itself remains rejected.
- Global balanced modifier hold-taps: delayed held multi-modifier chords until another key was released.
- Mod-taps nested inside tap dances: delayed the modifier until after the outer dance resolved and could lose fast chords. Tap dances around `&none`/`&kt` are permitted because they create no nested hold-tap and emit nothing on a single tap.
- Five exposed Bluetooth profiles: only two are needed.

## Known issues and unresolved decisions

1. **Space hold on the new Mac**: the earlier nested tap dance was removed and the direct Space/Shift mod-tap has been flashed on both keyboards. Physical comfort and normal-speed typing still need user testing. Hold Sofle Space, keep holding it, tap A, and expect `A`.
2. **Firmware identity**: the old Sofle (`2707E`) is verified on `a6ecdd8`; the new Sofle (`33F97`) is still on `b246979`. Physical typing tests remain separate from installation verification. Do not infer future installations merely from a successful CI build or the presence of a UF2 file.
3. **Redesign ergonomics**: confirm pinky-held Y with H/J/K/L, P/F/M volume, and thumb-modified movement. Also test Lower Tab plus Shift, the Ctrl+A workflow, and the new X-then-G deletion gesture.
4. **Arbitrary app switching**: Cmd+Tab is disabled, and named launchers do not select every running application. A dependable one-handed general switcher has not been chosen.
5. **Deletion comfort**: Lower+E/G Backspace is flashed on both Sofles. Both X+E and X+G need comparative reach/repeated-deletion testing. Y+O is retained, now without the 200 ms dwell in the saved firmware; L+J stays removed and Raise has no dedicated Backspace.
6. **Combo accidents**: Q+P and B+Y need normal-speed typing tests for false activation. Verify L/J together now type letters instead of deleting.
7. **USB wake repeat**: an older report said the first key after about 30 seconds over USB could repeat. Cause and current status are unknown.
8. **OLED**: it was blank during setup and recovered after settings/power experiments. Raise+I exists as a safe power-on path; continued reliability is unconfirmed.
9. **Physical ergonomics**: finger assignments, reach, fatigue, accidental locks, missing spaces, unexpected capitals, and multi-modifier comfort need observation rather than assumption.
10. **Browser brief**: native rules and the helper are installed, and both Sofles have the K+Y firmware bridge. The user confirmed the shortcut worked after correcting the current Karabiner app's System Events Automation permission. Full-brief mode and operation on another Mac remain separate tests.
11. **Faster Navigation/Media (saved, not flashed)**: verify Y-initial words and fast Y rolls never trigger arrows, volume or Backspace (watch `you`/`your` at the start of a line), and that the 150 ms idle rule is not annoying when reaching for arrows right after typing. If it is, lower it rather than restoring the dwell.
12. **Modifier toggles**: verify Cmd+click and Shift+click with the trackpad, that a single Y+C or Y+S does nothing, and that a forgotten toggle is noticed quickly.
13. **Zephyr 4.1 firmware (saved, not flashed)**: after the first flash, run the full regression test. In particular check the Raise+D bootloader hold (it uses a new boot-mode mechanism), hold-tap timing, battery sleep and wake, and the OLED. Flash one keyboard first and keep the other on Zephyr 3.5 as a fallback.

## Flashing decision and recovery

The nice!nano UF2 volume appeared as “Adafruit nRF UF2” but was not reliably accessible in Finder on this Mac. Raw disk copying failed with macOS “Operation not permitted.” The successful route was serial DFU from Ghostty using `adafruit-nrfutil` and the current `/dev/cu.usbmodem…` port.

The repeatable workflow is:

1. Download the left-side firmware artifact from the successful GitHub Actions build.
2. Enter the bootloader using the combo that belongs to the firmware already on the board, or double-tap reset.
3. Identify the current `usbmodem` serial port; its number can change.
4. Run serial DFU with the matching DFU zip, port, and 115200 baud.
5. Confirm the board leaves the `nice!nano` bootloader and reappears as `Sofle` before testing keys.

Never copy a personal SSH private key into this repository or into firmware artifacts. Git publication uses the existing local SSH configuration; firmware flashing does not require Git credentials.

## Regression test after flashing the saved firmware

1. Confirm macOS sees the USB keyboard name `SofleL-FlatMT` on both Sofles, and over Bluetooth (macOS keeps the name from pairing, e.g. `darksofle`, until the keyboard is paired again or renamed in Bluetooth settings). Tap Z to ensure Base, then type ordinary Q/U, X, K, comma, and Space at normal speed.
2. Hold X and immediately tap Q: expect `1`, with no leaked `x` or `q`.
3. Hold X, tap Z, release X, tap Q: expect `1`. Tap Z and then Q: expect `q`.
4. Lock Lower, hold physical X for Base peek, tap Space, release X: expect one Space and return to Lower.
5. Pause, hold Y and tap H/J/K/L without waiting: expect Left/Down/Up/Right. Release Y and verify the same keys work as Base letters (K still holds Raise). K+F should open Finder.
6. Lock Raise with K+Z and leave with Z. Verify physical K and the Esc thumb both send Escape without delay.
7. Test Ctrl+1 through Ctrl+5, Cmd+1 through Cmd+6, Ctrl+Shift, Space-as-Shift, X+Space Enter, and X+comma period.
8. Hold X first, tap E or G: expect Backspace, with no leaked `x`, `e`, or `g`. Keep X held and hold E/G to test repeat. Lock Lower, then tap E/G: expect Backspace; unlock and verify E/G type their Base letters. Hold Y and tap O: expect Backspace; roll Y then O: expect `yo`. Base L/J together should type letters, never Backspace. Lower+D/W and Raise+J/A should do nothing. Raise+X+G must do nothing. Tap Raise+D and Raise+W: nothing. Only hold Raise+D when ready to enter the bootloader.
9. Type Y rolls, including `yo`, `yp`, `yf`, `ym`, `yh`, `yj`, `yk`, `yl`, `yc` and `ys`, both mid-word and at the start of a line after a pause, plus `you`, `yes`, `yet`, `year` and `days`: expect letters, never commands or toggles. Then hold Y and test P/F/M for Volume Down/Up/Mute.
10. Test Q+P, B+Y, and V+W deliberately and during fast ordinary typing. Press V+W twice quickly: expect one-shot Raise only, with the Bluetooth connection intact.
11. Hold K and test Q/P for BT0/BT1 selection (the same saved profiles, now on Lower's 1/2 positions). V/W alone should do nothing. Test USB wake, OLED power-on, and all six app bridge keys.
12. Test Bluetooth clear (hold Raise+W one second) and bootloader (hold Raise+D one second) only when prepared for their destructive or disruptive effects.
13. On battery, leave the keyboard untouched for just over 15 minutes, then press a matrix key and confirm Bluetooth reconnects and normal typing resumes. Separately confirm USB-powered operation stays awake past the same timeout.
14. Hold X and test H for Tab, Shift thumb+H for Shift+Tab, and V for backslash (Shift+V gives pipe). Test A then Q/P/F at a clean Ghostty shell prompt for leader 1/2/3; do not invoke those layouts inside Neovim. Verify N/I send `[`/`]` (Shift gives `{`/`}`), E/G send Backspace, K sends backtick, and D/W send nothing. Release X to type comma with the Base Command thumb; add Shift for `<`.
15. In a normal macOS text field, hold Y for 200 ms, hold the Shift thumb, and tap/repeat H/J/K/L to select in each direction. Test Option/Command modified movement separately and release all keys to check for stuck modifiers. Verify the four modifier thumbs retain Base tap outputs. Test Neovim separately, where behavior is editor-dependent.
16. With a public YouTube video open in a supported browser, test native Space+Y and Shift+Space+Y, then Sofle K+Y and K+Shift+Y after flashing. Expect transcript/full-brief output on the clipboard, no typed `yy`, no trigger outside the supported browsers, and normal Base Y/navigation behavior. Grant macOS Automation access only when deliberately invoking the shortcut.
17. Hold Y and tap C once, release Y, then type: expect plain letters, no Command. Then hold Y, tap C twice, release Y, and Cmd+click two Finder items with the trackpad: both should be selected. Hold Y and double-tap C again, then type a letter: expect a plain letter. Repeat with S and Shift+click to select a range.
