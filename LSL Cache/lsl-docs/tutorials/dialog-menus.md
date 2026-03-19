---
name: "Dialog Menus"
category: "tutorial"
type: "reference"
language: "LSL"
description: "Step-by-step tutorial for creating interactive dialog menu systems with llDialog, llListen, and cleanup patterns"
wiki_url: "https://wiki.secondlife.com/wiki/Dialog_Menus"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
---

# Dialog Menus

A dialog menu presents a popup box with button choices to an avatar. When a button is pressed, the avatar speaks that button's text on a specified channel, which a `llListen` handler picks up.

## Nine Required Elements

1. A message (< 512 bytes, non-empty)
2. A list of button strings (max 12)
3. A communication channel (ideally unique negative integer)
4. User detection via `llDetectedKey()`
5. Dialog display with `llDialog()`
6. Listener registration with `llListen()`
7. A `listen` event handler
8. Listener removal with `llListenRemove()`
9. A timer for timeout cleanup

## Message Requirements

- Must be fewer than 512 bytes
- Must not be empty (workaround: use `" \n"`)
- Supports `\n` (newline) and `\t` (tab) formatting
- No font styling available
- More than 8 lines triggers a scrollbar

## Button List

- Maximum 12 buttons
- All elements must be strings
- Empty string `""` fails — use `" "` (single space) if needed
- Empty list defaults to `["OK"]`

## Channel Selection

Use a formula based on the object's key for a stable, collision-resistant channel:

```lsl
integer dialogChannel = -1 - (integer)("0x" + llGetSubString((string)llGetKey(), -7, -1));
```

Or use a random channel:

```lsl
integer dialogChannel = (integer)(llFrand(-1000000000.0) - 1000000000.0);
```

## Complete Example

```lsl
list buttons = ["-", "Red", "Green", "Yellow"];
string dialogInfo = "\nPlease make a choice.";

key toucherID;
integer dialogChannel;
integer listenHandle;

default
{
    state_entry()
    {
        dialogChannel = -1 - (integer)("0x" + llGetSubString((string)llGetKey(), -7, -1));
    }

    touch_start(integer num_detected)
    {
        toucherID = llDetectedKey(0);
        llListenRemove(listenHandle);  // Remove any previous listener
        listenHandle = llListen(dialogChannel, "", toucherID, "");
        llDialog(toucherID, dialogInfo, buttons, dialogChannel);
        llSetTimerEvent(60.0);  // 60-second timeout
    }

    listen(integer channel, string name, key id, string message)
    {
        if (message == "-")
        {
            // Re-show menu (back button)
            llDialog(toucherID, dialogInfo, buttons, dialogChannel);
            return;
        }

        // Clean up listener and timer
        llListenRemove(listenHandle);
        llSetTimerEvent(0.0);

        if (message == "Red")
            llSetColor(<1.0, 0.0, 0.0>, ALL_SIDES);
        else if (message == "Green")
            llSetColor(<0.0, 1.0, 0.0>, ALL_SIDES);
        else if (message == "Yellow")
            llSetColor(<1.0, 1.0, 0.0>, ALL_SIDES);
    }

    timer()
    {
        // Timeout — clean up
        llSetTimerEvent(0.0);
        llListenRemove(listenHandle);
        llWhisper(0, "Menu timed out.");
    }
}
```

## Button Layout in Dialog

Buttons appear in a 3×4 grid, filled bottom-to-top, left-to-right:

```
[ 9] [10] [11]
[ 6] [ 7] [ 8]
[ 3] [ 4] [ 5]
[ 0] [ 1] [ 2]
```

To order buttons visually from top-left to bottom-right, pre-sort the list. This helper assumes exactly 12 buttons (a full grid); it will produce incorrect output for fewer:

```lsl
list order_buttons(list buttons)
{
    return llList2List(buttons, -3, -1) + llList2List(buttons, -6, -4)
         + llList2List(buttons, -9, -7) + llList2List(buttons, -12, -10);
}
```

## Critical Rules

- Use `==` for comparison, never `=` (assignment).
- Register the listener **before** calling `llDialog`.
- Always remove listeners when done to prevent accumulation.
- Always set a timer to handle users who ignore or dismiss the dialog.

## Limitations

- No way to force-close a dialog box.
- No notification when the user clicks Ignore.
- Cannot change the dialog box size or colour.
- Dialog responses are heard sim-wide if listener is in same script as `llDialog`; otherwise only within 20m.

## See Also

- `llDialog` — function reference
- `llTextBox` — text input field dialog
- `llListen` — listener setup
- `llListenRemove` — listener cleanup
