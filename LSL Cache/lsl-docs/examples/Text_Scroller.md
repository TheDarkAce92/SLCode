---
name: "Text Scroller"
category: "example"
type: "example"
language: "LSL"
description: "Updated: 24 April 2010 by The Creator Fred Gandt"
wiki_url: "https://wiki.secondlife.com/wiki/Text_Scroller"
author: "link_message"
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 Text Scroller ( V1 )

  - 1.1 Create The Object
  - 1.2 Display Script
  - 1.3 Control Script
  - 1.4 The Charsheet Texture
  - 1.5 Functions Used
  - 1.6 Events Used

Text Scroller ( V1 )

Updated: 24 April 2010 by The Creator Fred Gandt

**All these scripts should be compiled as MONO**

A simple text display object that scrolls text (applied as a texture) from right to left (like *those* LED signs) in a continuous loop.

- Touch start/stop.

## Create The Object

- Create a fresh new prim and drop this script onto/into it. The prim will form the shape needed plus change the texturing etc. (you can do what you like to the texturing afterwards)

```lsl
default
{
    state_entry()
    {
        llSetPrimitiveParams([7, <0.5, 0.01, 0.25>, // Set the size
                              8, <0.0, 0.0, 0.0, 1.0>, // Set to ZERO_ROTATION
                              9, 0, 0, <0.375, 0.875, 0.0>, 0.0, <0.0, 0.0, 0.0>, <1.0, 1.0, 0.0>, <0.0, 0.0, 0.0>, // Shape the prim
                              17, -1, "5748decc-f629-461c-9a36-a35a221fe21f", <1.0, 1.0, 0.0>, <0.0, 0.0, 0.0>, 0.0, // Apply the blank texture
                              18, -1, <1.0, 0.65, 0.1>, 1.0, // Color the prim (kinda orange)
                              20, -1, 1, // Make fullbright
                              25, -1, 0.05]); // Slight glow
        llRemoveInventory(llGetScriptName()); // Remove the script when done
    }
}
```

- When the script has worked its magic, Snap the prim to the grid with a grid size of .5 meters.
- Shift-Drag-Copy the prim, snapping each to the grid positively along the X axis until you have 10 prims in a continuous strip.
- You can actually make the object as long or short as you like. 1 prim will work. 100 prims will work (although large linksets have been a problem for link_messages in the past). Just follow the same basic build plan.
- Select each of the prims from the end that has the greatest X axis position, one at a time (negatively along the X axis) until ALL are selected.

- Link the set.
- **DO NOT LINK THE OBJECT TO ANYTHING ELSE. IT MUST BE A STAND ALONE OBJECT** (unless you feel like editing the scripts to compensate)

## Display Script

- Check "Edit Linked parts" and select one prim at a time, dropping this script in each.
- **DO NOT CREATE A FRESH SCRIPT IN EACH PRIM. DROP THE SAME SCRIPT FROM YOUR INVENTORY INTO EACH PRIM.**

```lsl
string font = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890(){}[]<>|\\/.,;:'!?\"£$%^&*_+-=~#@ ";
// A accurate representation of the characters featured on the texture used to display the text.

vector GetOffset(string s)
{
    if(s == "") // If there is no text
        s = " "; // Use a space
    integer i = llSubStringIndex(font, s); // Find the character
    if(i == -1) // If we can't find it
        i = 94; // Use a space
    return <(-0.45 + ((i % 10) * 0.1)), (0.45 - (llRound(i / 10) * 0.1)), 0.0>;
} // Return the offset needed to display the correct section of the texture by doing the mathematics *coughs*

integer me; // Used to store the Link number

integer my_ss_5; // Used to store the index of the feed text we display on face 5

integer my_ss_6; // Used to store the index of the feed text we display on face 6

default
{
    state_entry()
    {
        me = llGetLinkNumber();
        my_ss_6 = ((me - 1) * 2); // Whatever link we are (in a correctly built object) establish the index to grab
        my_ss_5 = (my_ss_6 + 1); // And also grab the next
    }
    link_message(integer sender, integer num, string msg, key id)
    {
        llSetLinkPrimitiveParamsFast(me, [17, 5, id, <0.1, 0.1, 0.0>, GetOffset(llGetSubString(msg, my_ss_5, my_ss_5)), 0.0,
                                          17, 6, id, <0.1, 0.1, 0.0>, GetOffset(llGetSubString(msg, my_ss_6, my_ss_6)), 0.0]);
    } // Set the texture to the correct offset to display the correct characters
}
```

## Control Script

- One possible way amongst many to feed the text to the script is by notecard. That is the way I set this script. As such, you need a notecard in the root containing the text you wish to display. Only one notecard will be read. If you add more notecards (without altering the script) it will read the first it finds alphabetically.
- There is a caveat regarding the length of the lines of text in the notecard. If the line is longer then 255 bytes the dataserver will return the first 255 bytes of the line.
- This example - taken from one of Shakespeare's Hamlet's soliloques (To be, or not to be?...) is too long by the bold lettering -

  - "For who would bear the whips and scorns of time, th'oppressor's wrong, the proud man's contumely, the pangs of despised love, the law's delay, the insolence of office, and the spurns that patient merit of th'unworthy takes, when he himself might his quiet**us make with a bare bodkin?**"
- Add your text notecard to the root.
- Drop this script into the root.

```lsl
integer count; // Used to keep track of itterations

integer length; // A measure of string length

string text = "                   "; // Adding this creates a gap between beginning and end of text

integer NCC; // NoteCardCount for tracking which line to read

string NC; // NoteCard name

integer on; // Are we on or off?

default
{
    state_entry()
    {
        NC = llGetInventoryName(INVENTORY_NOTECARD, 0); // Establish the name of our NC
        llGetNotecardLine(NC, NCC); // Ask for the first line
    }
    dataserver(key q, string data)
    {
        if(data != EOF) // If the data is useful
        {
            text += (data + " "); // Store it
            llGetNotecardLine(NC, (++NCC)); // And get the next line
        }
        else // If not useful we are at the end of the NC
        {
            length = llStringLength(text); // Establish the length of our text
            // The number 19 is 1 less than the number of faces (2 per prim) that display text. Change that number accordingly if...
            // ...you have a larger or smaller number of prims in your object.
            llMessageLinked(-1, 0, llGetSubString("Touch start scroll.", count, (count + 19)), "b6349d2d-56bf-4c18-4859-7db0771990a5");
        } // Message the display scripts that we are ready to function
    }
    timer()
    {
        if(count == length) // If we have gone full circle
        count = 0; // Start again
        llMessageLinked(-1, 0, llGetSubString(text, count, (count + 19)), "b6349d2d-56bf-4c18-4859-7db0771990a5");
        ++count; // Message the display scripts with a chunk of text
    }
    touch_end(integer nd)
    {
        if(on) // Are we running?
        llSetTimerEvent(0.0); // Stop the timer
        else // No?
        llSetTimerEvent(0.15); // Start the timer
        on = (!on); // Remember what we did
    }
    changed(integer change)
    {
        if(change & CHANGED_INVENTORY) // If the inventory has changed the NC may have
        llResetScript(); // So reset the script to read the new card
    }
}
```

- The object should be set with the text "Touch Start Scroll.". If you get something else, you haven't followed these instructions.

## The Charsheet Texture

- I am a scriptor, not a texturizerer. I created a very simple Charsheet (Character Sheet) to get you going but, it isn't very good *grins*. You will probably want to replace it.

- The texture MUST be 10 characters by 10 characters (you may have empty spaces so, 56 chars is fine so long as the grid is the full 100 spaces).
- Unlike the texture I have supplied...ALL the chars should be perfectly evenly spaced and not spreading into the neighboring spaces.
- This is the texture supplied. You don't need to copy this. The script already has the UUID in it.

- The display scripts contain a string that is in the exact same order the chars are read from top left to bottom right (row by row, not column by column).
- **HAVING THE SAME ORDER OF CHARS IN THE TEXTURE AND STRING IS VITAL.**
- The order you choose is entirely up to you as long as the strings in ALL the display scripts match the order of chars in the texture.
- Don't forget to include a blank grid space on your 10 x 10 texture for a space "character". There also needs to be an empty space (in the correct place) in the scripts.
- In the display script strings there are two characters that must be treated unusually. The \ and the " must have a \ placed before them.

  - Example "ABCabc123.,:\"\\/| " Note the included space and the way the \ and " have a \ before them.

## Functions Used

1. llSetPrimitiveParams - Set shapes, colors, textures and other parameters of the prim the script is in.
1. llRemoveInventory - Remove the named inventory from the prim contents.
1. llGetScriptName - Returns the name of the script that calls the function.
1. llSubStringIndex - Searches a string for a test and returns the index (or -1 if not found)
1. llRound - Returns a classically rounded (up or down; whichever is closest) float as an integer.
1. llGetLinkNumber - Establish the link number of the prim the script is in.
1. llGetSubString - Returns the part of the source string specified.
1. llSetLinkPrimitiveParamsFast - Set parameters in any prim in a link-set without enforced delay.
1. llGetInventoryName - Returns the name of the specified inventory type at index.
1. llStringLength - Establish how many characters make up the source string.
1. llGetNotecardLine - Requests the string data on line of named notecard and (if successful) dataserver returns the result.
1. llMessageLinked - Send a message to defined links (or self) which are picked up by link_message
1. llSetTimerEvent - Establish a repeating time frame that on each pass will trigger timer
1. llResetScript - Wipe the memory and start from the word "default".

## Events Used

1. state_entry - Triggered when entering the state this event is in.
1. link_message - Triggered if llMessageLinked sends a message to the link containing this event.
1. dataserver - Triggered with responses to requests for data made by various functions.
1. timer - Triggered if a set time has elapsed then again after that time elapses again ad infinitum until the set time is zero.
1. touch_end - Triggered by an agent left clicking the object containing the script.
1. changed - Triggered by various changes that the script can sense.