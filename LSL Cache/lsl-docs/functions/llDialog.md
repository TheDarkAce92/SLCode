---
name: "llDialog"
category: "function"
type: "function"
language: "LSL"
description: "Shows a dialog box with buttons to an avatar; button presses are sent as chat on the specified channel"
wiki_url: "https://wiki.secondlife.com/wiki/llDialog"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "void llDialog(key avatar, string message, list buttons, integer channel)"
parameters:
  - name: "avatar"
    type: "key"
    description: "UUID of the avatar to show the dialog to (must be in the same region)"
  - name: "message"
    type: "string"
    description: "Text to display in the dialog (max 512 bytes, non-empty)"
  - name: "buttons"
    type: "list"
    description: "List of button label strings (max 12 buttons, each 1-24 UTF-8 bytes)"
  - name: "channel"
    type: "integer"
    description: "Chat channel on which button presses are spoken"
return_type: "void"
energy_cost: "10.0"
sleep_time: "1.0"
patterns: ["lldialog"]
deprecated: "false"
---

# llDialog

```lsl
void llDialog(key avatar, string message, list buttons, integer channel)
```

Displays a dialog box in the lower-right corner of `avatar`'s screen. When a button is pressed, the avatar speaks that button's label text on `channel`. A `llListen` on the same channel is required to receive the response.

Causes a 1.0-second forced delay.

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `avatar` | key | Target avatar UUID |
| `message` | string | Dialog message (max 512 bytes) |
| `buttons` | list | Button labels (max 12) |
| `channel` | integer | Response channel |

## Button Layout (3×4 grid, bottom-to-top, left-to-right)

```
[ 9] [10] [11]
[ 6] [ 7] [ 8]
[ 3] [ 4] [ 5]
[ 0] [ 1] [ 2]
```

To reorder buttons for display, use:

```lsl
list order_buttons(list buttons)
{
    return llList2List(buttons, -3, -1) + llList2List(buttons, -6, -4)
         + llList2List(buttons, -9, -7) + llList2List(buttons, -12, -10);
}
```

## Caveats

- **Message:** Must be fewer than 512 bytes and non-empty. Workaround for empty-looking message: `" \n"`.
- **Buttons:** Max 12. Empty list defaults to `["OK"]`. Each label: 1–24 UTF-8 bytes.
- **Listener required:** Must call `llListen` on the same `channel` before or after `llDialog` to receive responses.
- **No built-in close:** The dialog cannot be closed programmatically. Always set a timeout via `llSetTimerEvent`.
- **Distance restriction:** If the listener is in a different script/object from the `llDialog` call, the response is only heard within 20m of the listener's prim.
- **Ignore button:** Clicking Ignore generates no chat output.

## Channel Best Practices

Use a random negative channel to avoid collisions:

```lsl
integer dialogChannel = (integer)(llFrand(-1000000000.0) - 1000000000.0);
```

Or derive from object key (consistent across rezzes):

```lsl
integer dialogChannel = (integer)("0x" + llGetSubString((string)llGetKey(), -8, -1));
```

## Examples

```lsl
// Basic dialog with cleanup
integer gListener;

default
{
    touch_start(integer num_detected)
    {
        llListenRemove(gListener);
        key user = llDetectedKey(0);
        gListener = llListen(-99, "", user, "");
        llDialog(user, "\nDo you want this object to self-destruct?",
                 ["Yes", "No"], -99);
        llSetTimerEvent(60.0);
    }

    listen(integer chan, string name, key id, string msg)
    {
        if (msg == "Yes") llDie();
        llListenRemove(gListener);
        llSetTimerEvent(0.0);
    }

    timer()
    {
        llListenRemove(gListener);
        llSetTimerEvent(0.0);
    }
}
```

```lsl
// Reusable menu opener function
integer dialogChannel;
integer dialogHandle;

open_menu(key inputKey, string inputString, list inputList)
{
    dialogChannel = (integer)(llFrand(-1000000000.0) - 1000000000.0);
    dialogHandle = llListen(dialogChannel, "", inputKey, "");
    llDialog(inputKey, inputString, inputList, dialogChannel);
    llSetTimerEvent(30.0);
}

close_menu()
{
    llSetTimerEvent(0.0);
    llListenRemove(dialogHandle);
}
```

## See Also

- `llTextBox` — show a text input box instead of buttons
- `llListen` — required to receive dialog responses
- `llListenRemove` — clean up listener after response or timeout
- `llSetTimerEvent` — implement dialog timeout


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llDialog) — scraped 2026-03-18_

Shows a dialog box in the lower right corner of the avatar's screen (upper right in Viewer 1.x) with a message and choice buttons, as well as an ignore button. This has many uses ranging from simple message delivery to complex menu systems.

## Caveats

- This function causes the script to sleep for 1.0 seconds.
- This function **only** opens a dialog box. The script must then also register a listener on the same *channel* using llListen and have a listen event handler to receive the response.
- There is no way by script to kill a dialog box.
- There is no way for the script to detect if the user clicked the small `["Ignore"]` button (no chat is generated as a result of pressing this button).
- There is no way to distinguish the input from a dialog box and regular chat made by the same user.

  - It is important to expect that the response may not be one of the buttons.
- In most cases, the listener will be in the same script as the llDialog, however if not, the distance between the root prim of the listening object and the dialog generating prim becomes a factor. If this distance is greater than 20 meters when a button is pressed, the response will not be heard. See #Limits.

  - This limitation affects attachments too if the wearer moves more than 20 meters from where the listener is located. See #Limits.
  - If the listener resides in the same script that created the dialog, then the dialog button is heard sim-wide.
- By default, only one dialog can be displayed per object in the Second Life Viewer.  This can be overridden by the ScriptDialogLimitations debug setting in the Viewer.

- The **dialog response** (the generated chat) has its in world location at the **root prim's global position**.

It can generate a listen event within 20 meters from that position.

- The listening location for a child prim in the object is either at the child prim's location or at the root prim's location

see bugtrace JIRA [SCR-43](https://jira.secondlife.com/browse/SCR-43)

### message limits

- message must be fewer than 512 bytes in length and be not empty. If it is empty, llDialog will shout `"llDialog: must supply a message"` on the DEBUG_CHANNEL. If you want to create an empty message, however, you can do it legally by using a line feed as your message, as in

```lsl
llDialog(avatar_key," \n",button_list,dialog_channel);
```

 If the message length is greater than or equal to 512 bytes, it shouts (again on the debug channel): `"llDialog: message too long, must be less than 512 characters"`; in both instances, the dialog box will not be created for avatar.
- The client only displays 20 lines of message at a time, not counting the top line containing the owner and name of the object. If there are more than 20 lines the dialog displays a scroll bar. See #Appearance.



### buttons limits

- If buttons is an empty list, it will default to as if it were `["OK"]`
- Buttons named "Client_Side_Mute" or "Client_Side_Ignore" will be interpreted by the viewer as if the user click the special "Mute" or "Ignore" buttons, respectively.

  - Prior to SL viewer 3.3.1 (released in 2012) the viewer treated the buttons with values of "Mute" and "Ignore" as being equivalent to the dialogs special buttons "Mute" and "Ignore". This was changed as a result of [STORM-1718](https://jira.secondlife.com/browse/STORM-1718). Some very old versions of some viewer, especially those with a V1-style interface, could still have this old behavior and should be tested.
  - If you need a button in your menu that will collide with one of these special values, please consider adding spaces in the button name (e.g. `[" Ignore "]`).
- An error will be shouted on DEBUG_CHANNEL, if...

  - there are more than 12 buttons.
  - any list item is not a string.
  - any list item string length (measured in bytes, using UTF-8 encoding) is zero or greater than 24.

  - In other words, a button's text when encoded as UTF-8 cannot be longer than 24 bytes or a empty string.
  - The following function can be used to truncate the string without giving an error:

```lsl
string buttonLabel(string label) { //crop to valid UTF-8 of at most 24 bytes
    string  encoded = llStringToBase64(label);
    if (llStringLength(encoded) <= 32) {
        return label; }
    integer end = 31;
    //note: if we don't do this, llBase64ToString might add a "?" for the character we cut in half
    string  tailEnc = llGetSubString(encoded, 28, 33);
    integer tail    = llBase64ToInteger(tailEnc);
    while ((tail & 0xc0) == 0x80) {
        if (end % 4 == 1) {
            end -= 2; }
        else {
            end--; }
        tail = tail >> 8; }
    return llBase64ToString(llGetSubString(encoded, 0, end)); }
```
- The client will not display all the characters of a button if the text is wider than the text space of the button. See #Appearance.
- If the script generates button labels from outside sources like inventory or object names, take care to avoid the special string `"!!llTextBox!!"`. This text, used as any button label, will cause llDialog to behave as llTextBox instead.

## Examples

The following is a simple example that displays a dialog menu for the owner of the object when the script starts. The script will also listen for messages (the selected button, which is spoken by the avatar) and repeat it in chat. The example uses PUBLIC_CHANNEL to illustrate the avatar's behavior, but generally you'd want to use a private channel instead.

```lsl
default
{
    state_entry()
    {
        integer dialog_channel = PUBLIC_CHANNEL;

        llDialog(llGetOwner(), "This is a message", ["A", "B", "C", "D"], dialog_channel);

        llListen(dialog_channel, "", llGetOwner(), "");
    }

    listen(integer channel, string name, key id, string message)
    {
        llOwnerSay("Heard: " + message);
    }
}
```

The following example shows how you might offer a menu to any user interacting with an object, one user at a time, as well as timing-out if that user doesn't use the menu (by closing it instead).

```lsl
// When the prim is touched, give the toucher the option of killing the prim.

integer gListener; // Identity of the listener associated with the dialog, so we can clean up when not needed

default
{
    touch_start(integer total_number)
    {
        // Kill off any outstanding listener, to avoid any chance of multiple listeners being active
        llListenRemove(gListener);

        // get the UUID of the person touching this prim
        key user = llDetectedKey(0);

        // Listen to any reply from that user only, and only on the same channel to be used by llDialog
        // It's best to set up the listener before issuing the dialog
        gListener = llListen(-99, "", user, "");

        // Send a dialog to that person. We'll use a fixed negative channel number for simplicity
        llDialog(user, "\nDo you wish for this prim to die?", ["Yes", "No"] , -99);

        // Start a one-minute timer, after which we will stop listening for responses
        llSetTimerEvent(60.0);
    }

    listen(integer chan, string name, key id, string msg)
    {
        // If the user clicked the "Yes" button, kill this prim.
        if (msg == "Yes")
            llDie();

        // The user did not click "Yes" ...
        // Make the timer fire immediately, to do clean-up actions
        llSetTimerEvent(0.1);
    }

    timer()
    {
        // Stop listening. It's wise to do this to reduce lag
        llListenRemove(gListener);
        // Stop the timer now that its job is done
        llSetTimerEvent(0);
    }
}
```

|  | Important: Please make sure that you close open listeners where possible. You'll make the Second Life experience so much better when paying attention to details here. |
| --- | --- |

|  | Important: There are no built-in submenus nor pagination (like in a list with "previous" and "next") when using llDialog. You simply get one page with a max of 12 buttons, that's it. If you want a different dialog menu layout (other info and/or other buttons), you'll have to build that functionality into your script as the example below demonstrates. |
| --- | --- |

```lsl
string mainMenuDialog = "\nWhich settings would you like to access?\nClick \"Close\" to close the menu.\n\nYou are here:\nMainmenu";
list mainMenuButtons = ["sub 01", "sub 02", "Close"];

string subMenu_01_Dialog = "\nClick \"Close\" to close the menu.\nClick \"-Main-\" to return to the main menu.\n\nYou are here:\nMainmenu > sub 01";
list subMenu_01_Buttons = ["action 01a", "action 01b", "Close", "-Main-"];

string subMenu_02_Dialog = "\nClick \"Close\" to close the menu.\nClick \"-Main-\" to return to the main menu.\n\nYou are here:\nMainmenu > sub 02";

list subMenu_02_Buttons = ["action 02a", "action 02b", "Close", "-Main-"];

integer dialogChannel;
integer dialogHandle;

open_menu(key inputKey, string inputString, list inputList)
{
    dialogChannel = (integer)llFrand(DEBUG_CHANNEL)*-1;
    dialogHandle = llListen(dialogChannel, "", inputKey, "");
    llDialog(inputKey, inputString, inputList, dialogChannel);
    llSetTimerEvent(30.0);
}

close_menu()
{
    llSetTimerEvent(0.0);// you can use 0 as well to save memory
    llListenRemove(dialogHandle);
}

default
{
    on_rez(integer start_param)
    {
        llResetScript();
    }

    touch_start(integer total_number)
    {
        key id = llDetectedKey(0);
        // Ensure any outstanding listener is removed before creating a new one
        close_menu();
        open_menu(id, mainMenuDialog, mainMenuButtons);
    }

    listen(integer channel, string name, key id, string message)
    {
        if(channel != dialogChannel)
            return;

        close_menu();

        if(message == "-Main-")
            open_menu(id, mainMenuDialog, mainMenuButtons);

        else if(message == "sub 01")
            open_menu(id, subMenu_01_Dialog, subMenu_01_Buttons);

        else if(message == "sub 02")
            open_menu(id, subMenu_02_Dialog, subMenu_02_Buttons);

        else if (message == "action 01a")
        {
            //do something
            open_menu(id, subMenu_01_Dialog, subMenu_01_Buttons);
        }
        else if (message == "action 01b")
        {
            //do something else

            //maybe not re-open the menu for this option?
            //open_menu(id, subMenu_01_Dialog, subMenu_01_Buttons);
        }
        else if (message == "action 02a")
        {
            //do something
            open_menu(id, subMenu_02_Dialog, subMenu_02_Buttons);
        }
        else if (message == "action 02b")
        {
            //do something else
            open_menu(id, subMenu_02_Dialog, subMenu_02_Buttons);
        }
    }

    timer()
    {
        close_menu();
    }
}
```

## Notes

To use dialog boxes to make menu systems, see Dialog Menus: A step by step guide (aimed at learners).

### Tips

It is a good idea to use a very negative channel (if never more negative than the most negative 32-bit integer that is -2,147,483,648), *e.g.*,

```lsl
// Create random channel within range [-1000000000,-2000000000]
integer channel = (integer)(llFrand(-1000000000.0) - 1000000000.0);

llDialog(llDetectedKey(0), "Please choose one of the below options:",
    ["Yes", "No", "0", "1"], channel);
```

Negative channels are popular for script communications because for years the standard SL client was unable to chat directly on those channels. However, since late 2016 both third party and the Linden Lab viewer can use negative channels from the chat bar. Previously, the only way for viewers to use negative channels prior to llTextBox was to use llDialog, which was limited to 24 bytes.

You can be reasonably confident that all of your scripted objects have a unique chat channel with this small function:

```lsl
integer dialog_channel; // top of script in variables

integer channel() { // top of script in functions
    return (integer)("0x"+llGetSubString((string)llGetKey(),-8,-1));
}

dialog_channel = channel(); // somewhere in actual script execution, such as state_entry()
```

**Note:** Since this function uses public information to generate the channel number it should by no means considered secret.

The preceding code can produce both positive and negative channels, depending on the 8th to last character of the key.
The following examples will always produce negative channels:-

```lsl
    gChannel = 0x80000000 | (integer)("0x"+(string)llGetKey());
    gChannel = 0x80000000 | (integer)("0x"+(string)llGetOwner());
```



This next version returns a channel number between -1073741823 (0xBFFFFFFF) and -2147483648 (0x80000000).  It is also only one line of code.

```lsl
privchan = ((integer)("0x"+llGetSubString((string)llGetKey(),-8,-1)) & 0x3FFFFFFF) ^ 0xBFFFFFFF;
```

### Appearance

If message requires more than 8 lines, a vertical scroll bar will appear in the dialog.

In viewer 3 there is no scroll bar, only the 512 chars message limit is effective, so you may show more than 40 short lines in the message
Too many lines will hide some of the buttons or all of them outside the window though

The message text can be formatted somewhat using "\n" (for newline) and "\t" (for tab). If URLs are in the text, they will appear as clickable links, and some viewer application URLs will receive special formatting. (Clickable links were not available before Viewer 2.) You can do nothing though to influence the font face, size or weight.

There is no way to change the actual size of the dialog, nor change its color.

The average number of characters that can be displayed on a dialog line is about 35 characters per line in ASCII7 characters. It depends upon the width of the characters, the viewer version, and font settings.

The number of characters that can be displayed in a button depends upon the width of the characters. You should expect around 10 chars, give or take, not the full 24 in the button definition. The full button definition IS said, up to 24 chars, into the chat channel even though fewer characters may be displayed in the button itself.

### Limits

My testing shows the a Dialog box now works anywhere in the same Region as the object OR any region it hands you off to (e.g. the region you teleport to). It will not work for any subsequent hand offs. I have tested this with teleport only, I haven't tested it walking between regions.

I've tested from the next SIM with an Alt, and from 2 SIMs away myself. Both worked without restriction apart from some lag on the messages. (OQ).

## See Also

### Events

- listen

### Functions

- llListen
- llTextBox
- llRegionSay
- **llWhisper** — Sends chat limited to 10 meters
- **llSay** — Sends chat limited to 20 meters
- **llShout** — Sends chat limited to 100 meters
- **llInstantMessage** — Sends chat to the specified user
- **llOwnerSay** — Sends chat to the owner only

### Articles

- **Dialog Menus: A step by step guide** — A walk through of the entire dialog menu process (aimed at learners).

<!-- /wiki-source -->
