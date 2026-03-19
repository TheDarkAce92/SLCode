---
name: "llDialog"
category: "example"
type: "example"
language: "LSL"
description: "Shows a dialog box in the lower right corner of the avatar's screen (upper right in Viewer 1.x) with a message and choice buttons, as well as an ignore button. This has many uses ranging from simple message delivery to complex menu systems."
wiki_url: "https://wiki.secondlife.com/wiki/LlDialog"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL


DialogllDialog

- 1 Summary
- 2 Caveats

  - 2.1 message limits
  - 2.2 buttons limits
- 3 Examples
- 4 Useful Snippets

  - 4.1 Helper Functions
- 5 Notes

  - 5.1 Tips
  - 5.2 Appearance
  - 5.3 Limits
- 6 See Also

  - 6.1 Events
  - 6.2 Functions
  - 6.3 Articles
- 7 Deep Notes

  - 7.1 Footnotes
  - 7.2 Signature
  - 7.3 Haiku

## Summary

1/4 Bugs Function: **llDialog**( key avatar, string message, list buttons, integer channel ); 1.0 Forced Delay 10.0 Energy Shows a dialog box in the lower right corner of the avatar's screen (upper right in Viewer 1.x) with a message and choice buttons, as well as an ignore button. This has many uses ranging from simple message delivery to complex menu systems. • key avatar – avatar UUID that is in the same region • string message – message to be displayed in the dialog box • list buttons – button labels • integer channel – output chat channel, any integer value When a button is pressed, the avatar says the text of the button label on channel.The position where the chat is generated is where the root prim of the dialog generating object was when the dialog button was pressed. Button Order 9   10 11 6 7 8   3 4 5 0 1 2 ## Caveats - This function causes the script to sleep for 1.0 seconds. - This function **only** opens a dialog box. The script must then also register a listener on the same *channel* using llListen and have a listen event handler to receive the response. - There is no way by script to kill a dialog box. - There is no way for the script to detect if the user clicked the small `["Ignore"]` button (no chat is generated as a result of pressing this button). - There is no way to distinguish the input from a dialog box and regular chat made by the same user. - It is important to expect that the response may not be one of the buttons. - In most cases, the listener will be in the same script as the llDialog, however if not, the distance between the root prim of the listening object and the dialog generating prim becomes a factor. If this distance is greater than 20 meters when a button is pressed, the response will not be heard. See #Limits. - This limitation affects attachments too if the wearer moves more than 20 meters from where the listener is located. See #Limits. - If the listener resides in the same script that created the dialog, then the dialog button is heard sim-wide. - By default, only one dialog can be displayed per object in the Second Life Viewer. This can be overridden by the ScriptDialogLimitations debug setting in the Viewer. - The **dialog response** (the generated chat) has its in world location at the **root prim's global position**. It can generate a listen event within 20 meters from that position. - The listening location for a child prim in the object is either at the child prim's location or at the root prim's location see bugtrace JIRA SCR-43 ### message limits - message must be fewer than 512 bytes in length and be not empty. If it is empty, llDialog will shout `"llDialog: must supply a message"` on the DEBUG_CHANNEL. If you want to create an empty message, however, you can do it legally by using a line feed as your message, as in ```lsl llDialog(avatar_key," \n",button_list,dialog_channel); ``` If the message length is greater than or equal to 512 bytes, it shouts (again on the debug channel): `"llDialog: message too long, must be less than 512 characters"`; in both instances, the dialog box will not be created for avatar. - The client only displays 20 lines of message at a time, not counting the top line containing the owner and name of the object. If there are more than 20 lines the dialog displays a scroll bar. See #Appearance. ### buttons limits - If buttons is an empty list, it will default to as if it were `["OK"]` - Buttons named "Client_Side_Mute" or "Client_Side_Ignore" will be interpreted by the viewer as if the user click the special "Mute" or "Ignore" buttons, respectively. - Prior to SL viewer 3.3.1 (released in 2012) the viewer treated the buttons with values of "Mute" and "Ignore" as being equivalent to the dialogs special buttons "Mute" and "Ignore". This was changed as a result of [STORM-1718](https://jira.secondlife.com/browse/STORM-1718). Some very old versions of some viewer, especially those with a V1-style interface, could still have this old behavior and should be tested. - If you need a button in your menu that will collide with one of these special values, please consider adding spaces in the button name (e.g. `[" Ignore "]`). - An error will be shouted on DEBUG_CHANNEL, if... - there are more than 12 buttons. - any list item is not a string. - any list item string length (measured in bytes, using UTF-8 encoding) is zero or greater than 24. - In other words, a button's text when encoded as UTF-8 cannot be longer than 24 bytes or a empty string. - The following function can be used to truncate the string without giving an error: ```lsl string buttonLabel(string label) { //crop to valid UTF-8 of at most 24 bytes string encoded = llStringToBase64(label); if (llStringLength(encoded) > 8; } return llBase64ToString(llGetSubString(encoded, 0, end)); } ``` - The client will not display all the characters of a button if the text is wider than the text space of the button. See #Appearance. - If the script generates button labels from outside sources like inventory or object names, take care to avoid the special string `"!!llTextBox!!"`. This text, used as any button label, will cause llDialog to behave as llTextBox instead. ## Examples The following is a simple example that displays a dialog menu for the owner of the object when the script starts. The script will also listen for messages (the selected button, which is spoken by the avatar) and repeat it in chat. The example uses PUBLIC_CHANNEL to illustrate the avatar's behavior, but generally you'd want to use a private channel instead. ```lsl default { state_entry() { integer dialog_channel = PUBLIC_CHANNEL; llDialog(llGetOwner(), "This is a message", ["A", "B", "C", "D"], dialog_channel); llListen(dialog_channel, "", llGetOwner(), ""); } listen(integer channel, string name, key id, string message) { llOwnerSay("Heard: " + message); } } ``` The following example shows how you might offer a menu to any user interacting with an object, one user at a time, as well as timing-out if that user doesn't use the menu (by closing it instead). ```lsl // When the prim is touched, give the toucher the option of killing the prim. integer gListener; // Identity of the listener associated with the dialog, so we can clean up when not needed default { touch_start(integer total_number) { // Kill off any outstanding listener, to avoid any chance of multiple listeners being active llListenRemove(gListener); // get the UUID of the person touching this prim key user = llDetectedKey(0); // Listen to any reply from that user only, and only on the same channel to be used by llDialog // It's best to set up the listener before issuing the dialog gListener = llListen(-99, "", user, ""); // Send a dialog to that person. We'll use a fixed negative channel number for simplicity llDialog(user, "\nDo you wish for this prim to die?", ["Yes", "No"] , -99); // Start a one-minute timer, after which we will stop listening for responses llSetTimerEvent(60.0); } listen(integer chan, string name, key id, string msg) { // If the user clicked the "Yes" button, kill this prim. if (msg == "Yes") llDie(); // The user did not click "Yes" ... // Make the timer fire immediately, to do clean-up actions llSetTimerEvent(0.1); } timer() { // Stop listening. It's wise to do this to reduce lag llListenRemove(gListener); // Stop the timer now that its job is done llSetTimerEvent(0); } } ``` Important: Please make sure that you close open listeners where possible. You'll make the Second Life experience so much better when paying attention to details here. **Important:** There are no built-in submenus nor pagination (like in a list with "previous" and "next") when using llDialog. You simply get one page with a max of 12 buttons, that's it. If you want a different dialog menu layout (other info and/or other buttons), you'll have to build that functionality into your script as the example below demonstrates. ```lsl string mainMenuDialog = "\nWhich settings would you like to access?\nClick \"Close\" to close the menu.\n\nYou are here:\nMainmenu"; list mainMenuButtons = ["sub 01", "sub 02", "Close"]; string subMenu_01_Dialog = "\nClick \"Close\" to close the menu.\nClick \"-Main-\" to return to the main menu.\n\nYou are here:\nMainmenu > sub 01"; list subMenu_01_Buttons = ["action 01a", "action 01b", "Close", "-Main-"]; string subMenu_02_Dialog = "\nClick \"Close\" to close the menu.\nClick \"-Main-\" to return to the main menu.\n\nYou are here:\nMainmenu > sub 02"; list subMenu_02_Buttons = ["action 02a", "action 02b", "Close", "-Main-"]; integer dialogChannel; integer dialogHandle; open_menu(key inputKey, string inputString, list inputList) { dialogChannel = (integer)llFrand(DEBUG_CHANNEL)*-1; dialogHandle = llListen(dialogChannel, "", inputKey, ""); llDialog(inputKey, inputString, inputList, dialogChannel); llSetTimerEvent(30.0); } close_menu() { llSetTimerEvent(0.0);// you can use 0 as well to save memory llListenRemove(dialogHandle); } default { on_rez(integer start_param) { llResetScript(); } touch_start(integer total_number) { key id = llDetectedKey(0); // Ensure any outstanding listener is removed before creating a new one close_menu(); open_menu(id, mainMenuDialog, mainMenuButtons); } listen(integer channel, string name, key id, string message) { if(channel != dialogChannel) return; close_menu(); if(message == "-Main-") open_menu(id, mainMenuDialog, mainMenuButtons); else if(message == "sub 01") open_menu(id, subMenu_01_Dialog, subMenu_01_Buttons); else if(message == "sub 02") open_menu(id, subMenu_02_Dialog, subMenu_02_Buttons); else if (message == "action 01a") { //do something open_menu(id, subMenu_01_Dialog, subMenu_01_Buttons); } else if (message == "action 01b") { //do something else //maybe not re-open the menu for this option? //open_menu(id, subMenu_01_Dialog, subMenu_01_Buttons); } else if (message == "action 02a") { //do something open_menu(id, subMenu_02_Dialog, subMenu_02_Buttons); } else if (message == "action 02b") { //do something else open_menu(id, subMenu_02_Dialog, subMenu_02_Buttons); } } timer() { close_menu(); } } ``` ## Useful Snippets ```lsl // Compact function to put buttons in "correct" human-readable order integer channel; list order_buttons(list buttons) { return llList2List(buttons, -3, -1) + llList2List(buttons, -6, -4) + llList2List(buttons, -9, -7) + llList2List(buttons, -12, -10); } default { state_entry() { // Create random channel within range [-1000000000,-2000000000] channel = (integer)(llFrand(-1000000000.0) - 1000000000.0); llListen(channel,"", "",""); } touch_start(integer total_number) { llDialog(llDetectedKey(0),"\nPlease choose an option:\n", order_buttons(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]),channel); } listen(integer _chan, string _name, key _id, string _option) { llSay(0, _name + " selected option " + _option); } } ``` ```lsl list make_ordered_buttons(integer input) { string output; if (input == 12) output = "10, 11, 12, 7, 8, 9, 4, 5, 6, 1, 2, 3"; else if (input == 11) output = "10, 11, 7, 8, 9, 4, 5, 6, 1, 2, 3"; else if (input == 10) output = "10, 7, 8, 9, 4, 5, 6, 1, 2, 3"; else if (input == 9) output = "7, 8, 9, 4, 5, 6, 1, 2, 3"; else if (input == 8) output = "7, 8, 4, 5, 6, 1, 2, 3"; else if (input == 7) output = "7, 4, 5, 6, 1, 2, 3"; else if (input == 6) output = "4, 5, 6, 1, 2, 3"; else if (input == 5) output = "4, 5, 1, 2, 3"; else if (input == 4) output = "4, 1, 2, 3"; else if (input == 3) output = "1, 2, 3"; else if (input == 2) output = "1, 2"; else if (input == 1) output = "1"; // when we want to return [] avoid returning [""] here if (output == "") return []; /* else convert output */ return llCSV2List(output); } // Usage: llDialog(id, "dialog message", make_ordered_buttons(5), -37812); // Output: // - - - // - - - // - [ 4 ] [ 5 ] // [ 1 ] [ 2 ] [ 3 ] ``` ### Helper Functions •  uDlgBtnPagList – Compact Pagination for llDialog lists, remenu, and multi-user support ## Notes To use dialog boxes to make menu systems, see Dialog Menus: A step by step guide (aimed at learners). ### Tips It is a good idea to use a very negative channel (if never more negative than the most negative 32-bit integer that is -2,147,483,648), e.g.,

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

•

listen

### Functions

•

llListen

•

llTextBox

•

llRegionSay

•

llWhisper

–

Sends chat limited to 10 meters

•

llSay

–

Sends chat limited to 20 meters

•

llShout

–

Sends chat limited to 100 meters

•

llInstantMessage

–

Sends chat to the specified user

•

llOwnerSay

–

Sends chat to the owner only

### Articles

•

Dialog Menus: A step by step guide

–

A walk through of the entire dialog menu process (aimed at learners).

## Deep Notes

#### Footnotes

1. **^** Channel zero is also known as: PUBLIC_CHANNEL, open chat, local chat and public chat

#### Signature

```lsl
function void llDialog( key avatar, string message, list buttons, integer channel );
```

#### Haiku

click here click there. But,


read the options carefully


you might get a shock.