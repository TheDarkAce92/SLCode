---
name: "HexText"
category: "example"
type: "example"
language: "LSL"
description: "HexText is an LSL script to display Unicode text on 8 faced prims within Second Life. Support is included for Japanese/Chinese, as well as many other languages and symbols. It is not all-inclusive. There are some code pages that are missing. It does cover the majority of characters that avatars use in Unicode enhanced display names."
wiki_url: "https://wiki.secondlife.com/wiki/HexText"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 About
- 2 Acknowledgments
- 3 Setup

  - 3.1 Creating displays
  - 3.2 Setup and initialization
  - 3.3 LSL Script
- 4 Reference Manual

  - 4.1 Commands

  - 4.1.1 fw_data
  - 4.1.2 fw_direct
  - 4.1.3 fw_conf & fw_defaultconf
  - 4.1.4 fw_notify
  - 4.1.5 fw_memory
  - 4.1.6 fw_reset
  - 4.2 Style settings
  - 4.3 Predefined colors
- 5 Version History

  - 5.1 Version 1.0
  - 5.2 Version 1.1
- 6 Bugs

## About

HexText is an LSL script to display Unicode text on 8 faced prims within Second Life. Support is included for Japanese/Chinese, as well as many other languages  and symbols. It is not all-inclusive. There are some code pages that are missing. It does cover the majority of characters that avatars use in Unicode enhanced display names.

The primary font used is Google's Noto Monospace (Bold & Regular), supplemented with other open source or public domain fonts for code pages not covered by Noto.

The character set is broken up into ~113 individual textures for each supported Unicode code page, covering roughly 28,000 characters. Each texture is a 16 x 16 matrix of characters. To minimize texture memory usage, the majority of textures are rendered at 512 x 256 pixels. Kanji is rendered at 512 x 384 which gets reduced to 512 x 256 at upload. As the textures are 512 x 256, it takes 8 of them to equal the amount of GPU texture memory used by a single 1024 x 1024 texture. I have found that unless you are displaying Kanji, it is rare to use more memory than 2 - 1024 x 1024 textures.

## Acknowledgments

Thanks go to Ochi Wolfe for his excellent FURWARE_text display sytem and documentation. Without his, and his contributors efforts, HexText would have been significantly more difficult to create.

HexText is released under the MIT license.

HexText uses a subset of the FURWARE_text/Reference command set. HexText does not support virtual text boxes, inline styles or touch queries.

HexText can use displays set up by the FURWARE_text/Tutorial#Creating_displays, however it can only use the 8 faced prim displays. HexText uses display prims with the same description format used by FURWARE text. HexText only supports a single display set per linkset, unlike FURWARE text that can handle multiple displays per linkset.

The HexText texture set was created with FURWARE_text/TextureCreator.

Use of both HexText and the FURWARE text scripts in the same linkset is not recommended.

Although it is technically possible to combine the FURWARE text engine, and HexText to create a Unicode display system with the features of both, I was concerned that it would not fit in a single script, and would therefore suffer performance issues.

## Setup

The following was taken from the FURWARE text manual, edited to remove limitations imposed by HexText. All credit for FURWARE text tools to Ochi Wolfe and his contributors. Hexadeci Mole is only responsible for the alternative HexText Unicode display script, textures and its documentation.

### Creating displays

HexText uses displays created with the FURWARE text display creator available here: [https://marketplace.secondlife.com/p/FURWARE-text/141379](https://marketplace.secondlife.com/p/FURWARE-text/141379)

You may (and should) use the "**FURWARE display creator**" to have a perfectly aligned grid of display prims automatically created for you. Every prim will be automatically assigned a special object name that is used internally by the text script so that it knows how to order them correctly, independently of the link order.

Creating a display is simple:

- Rez the display creator on a parcel where you have sufficient permissions.
- Touch the creator object. A dialog appears where you can set some parameters of the new display:

  - A **name** for the display. You will use this name to identify which display you wish to manipulate when using multiple displays within one linkset.
  - The number of **rows and columns** of the display (the columns are counted in prims here, not in characters).
  - The number of **faces per prim**. There are mesh prims from 1 to 8 faces available. HexText can only use the 8 face display prims.
- When you're happy with the settings, click "Create" to start rezzing the prims. Link them to your creation as appropriate. (I would not recommend that any display prim be link #1 in a linkset)

### Setup and initialization

When you have created your display and linked it together with your creation,  put **a single copy** of the HexText Script (listed below) into the linkset instead of the FURWARE text script. The script does **not** have to be in the root prim.

**Important hint:**

You may wish to send some initial commands to the text script as soon as its initialization is done. A reset of the text script may happen in a number of cases:

- The script was just put into the object.
- The object in which the script resides was shift-copied.
- The linkset has changed (then the script needs to search for display prims again).
- The script was reset manually (for instance using the "fw_reset" command).

In order to know when exactly the script is ready to take commands, it sends a link message to the whole set with the "id" parameter set to "fw_ready". It is **good practice** to watch for these messages and send your initialization commands when receiving this message. Your code could look something like this:

```lsl link_message(integer sender, integer num, string str, key id) { if (id == "fw_ready") { // Set your default color, alignment, wrapping, trim, etc. llMessageLinked(sender, 0, "c=red;a=center;w=word", "fw_conf"); // If your default display is not blank, send the default text llMessageLinked(sender, 0, "Default text", "fw_data"); // ... } } ``` ### LSL Script Previously, there were 2 variations of the script. One that rendered Kanji characters on 2 prim faces, and another version that used 1 face for all characters. They have been combined, and one script can do both. In the combined version of the script, the k configuration option can be used to switch between 1 face and 2 face Kanji rendering.

Do not use the FURWARE text script in the same linkset that this script occupies.

- 2XKanji Script (LSL Mono): HexText/HexText_2XKanji

## Reference Manual

Commands supported in HexText (a subset of the FURWARE text command set.)

### Commands

The following commands can be issued from other scripts in your linkset to control HexText.

#### fw_data

Display a string on the screen. The entire screen is overwritten with the text message. If you wish to only overwrite a portion of the display, consider fw_direct.

```lsl
llMessageLinked(LINK_SET, 0, "Some text to draw.", "fw_data");
```

#### fw_direct

This command is not supported by FURWARE text. It is unique to HexText to display text at specific display coordinates. It does not erase the display when called, instead, it overwrites existing characters in the display. Trim is ignored with fw_direct.

```lsl
llMessageLinked(LINK_SET, 0, "Some text to draw.", "fw_direct:10:2");
```

Display the string "Some text to draw." starting at the 11th column, 3rd row (Column/Row numbering starts at 0.)

#### fw_conf & fw_defaultconf

Sets the global style preference for the display. Unlike FURWARE text, fw_conf is treated the same as fw_defaultconf.

```lsl
llMessageLinked(LINK_SET, 0, "c=red; a=center", "fw_conf");
llMessageLinked(LINK_SET, 0, "c=red; a=center", "fw_defaultconf");
```

#### fw_notify

Enable or disable link message notifications when the script has completed rendering. Off by default.

```lsl
llMessageLinked(LINK_SET, 0, "on", "fw_notify");
llMessageLinked(LINK_SET, 0, "off", "fw_notify");
```

A link message will be sent to the linkset after rendering is complete with the key value of "fw_done"

#### fw_memory

Tells the owner how much memory is available.

```lsl
llMessageLinked(LINK_SET, 0, "", "fw_memory");
```

#### fw_reset

Performs a full reset on the text script.

```lsl
llMessageLinked(LINK_SET, 0, "", "fw_reset");
```

A link message will be sent to the linkset after reset is complete with the key value of "fw_ready"

### Style settings

Text styles and format settings are specified using special strings. They are used for global settings ("fw_conf").

A single setting is given as a **key=value** pair, for example **c=red**.

Multiple settings are separated by "**;**", for example **c=red; a=center; w=none**.

In the following table: **Bold** = Default

Setting

Key

Values

Description

Font color

c

R,G,B

Font color as red, green, blue (each in range 0.0-1.0)

R,G,B,A

Font color as red, green, blue, alpha (each in range 0.0-1.0)

rand

Random color (with alpha = 1)

(predefined)

Predefined color, see table below (default is White)

Alignment

a

**left**

Alignment left

center

Alignment centered

right

Alignment right

Wrapping

w

**word**

Wrap after words, if possible

char

Wrap at any position

none

No wrapping; cuts overlong lines

Trimming

t

**on**

Trims whitespace from beginning and end of lines

off

Keeps whitespace

2X Kanji

k

on

Use 2 prim faces for Kanji characters

**off**

Use 1 prim face for all characters

Force refresh

force

on

Enables forced refresh of all faces (disables optimizations!)

**off**

Disables forced refresh of all faces (enables optimizations)

### Predefined colors

You may use the following names in place of color vectors in styles.



red
green
blue
cyan
magenta
yellow
white
silver

darkred
darkgreen
darkblue
darkcyan
darkmagenta
darkyellow
black
gray

## Version History

### Version 1.0

- Initial release.

### Version 1.1

- Switched to the easier to follow version of Strife's unicode decoder.
- Combined the General and 2XKanji versions of the script into a single script.
- Added the option of turning 2XKanji on and off with fw_conf.
- Memory optimizations to try and prevent stack-heap collisions with long paragraphs.
- Many small optimizations to improve rendering speed.

## Bugs

Probably a lot. Let Hexadeci Mole know.

---

## Subpage: HexText_2XKanji

HexText Unicode Display (2XKanji). Two prim faces for Kanji/Katakana, 1 prim face for all other characters.

```lsl
////////// DESCRIPTION /////////////////////////////////////
//                                                        //
//  HexText 1.1 Unicode Display System by Hexadeci Mole   //
//  Optionally uses 2 faces for Kanji characters          //
//  Thanks to Ochi Wolfe for the FURWARE text toolset     //
//                                                        //
////////////////////////////////////////////////////////////

////////// DOCUMENTATION ///////////////////////////////////
//                                                        //
//  Documentation is available at:                        //
//  http://wiki.secondlife.com/wiki/HexText               //
//                                                        //
////////////////////////////////////////////////////////////

////////// LICENSE /////////////////////////////////////////

/*
MIT License
Copyright (c) 2018-2020 Hexadeci Mole, HexText
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
*/

////////// CONSTANTS ///////////////////////////////////////

// Numerically accurate for Furware faces, but there can be a bit of character cell bleed
vector  gOffset = <.53125, .0123, 0>;
vector  gCellSize = <.0625, .0625, 0>;
vector  gOffsetLeft = <.015625, .0123, 0>;
vector  gOffsetRight = <-.015625, .0123, 0>;
vector  gCellSizeHalf = <.03125, .0625, 0>;

// Numerically accurate for normal UV faces, but there can be a bit of character cell bleed
//vector  gOffset = <.46875, .46875, 0>;
//vector  gCellSize = <.0625, .0625, 0>;
//vector  gOffsetLeft = <.484375, .46875, 0>;
//vector  gOffsetRight = <.453125, .46875, 0>;
//vector  gCellSizeHalf = <.03125, .0625, 0>;

////////// DEFAULTS ////////////////////////////////////////

integer gAlign = 0;         // Alignment: 0 = Left, 1 = Center, 2 = Right
integer gTrim = TRUE;       // Trim whitespace from lines
integer gWrap = 2;          // Wrapping: 0 = None, 1 = Char, 2 = Word
float   gWrapLimit = 0.75;  // Percentage of display width before which word wrap is cancelled.
integer g2XKanji = FALSE;   // Use 2 faces for Kanji characters if TRUE, else just one.
integer gForce = FALSE;     // Ignore optimizations for drawing
integer gNotify = FALSE;    // Notify when drawing is complete
vector  gColor = <1, 1, 1>; //
float   gAlpha = 1;

////////// END USER CONFIG /////////////////////////////////

integer gPrimCount;
integer gCols;
integer gColPrims;
integer gRows;
integer gPos;
vector  gSpaceOffset;

list    gTextLinks;
list    gRowLengths;

list    gColors = [
            "rand",         < 0,  0,  0>,
            "white",        < 1,  1,  1>,
            "black",        < 0,  0,  0>,
            "darkred",      <.5,  0,  0>,
            "darkgreen",    < 0, .5,  0>,
            "darkblue",     < 0,  0, .5>,
            "darkcyan",     < 0, .5, .5>,
            "darkmagenta",  <.5,  0, .5>,
            "darkyellow",   <.5, .5,  0>,
            "gray",         <.5, .5, .5>,
            "red",          < 1,  0,  0>,
            "green",        < 0,  1,  0>,
            "blue",         < 0,  0,  1>,
            "cyan",         < 0,  1,  1>,
            "magenta",      < 1,  0,  1>,
            "yellow",       < 1,  1,  0>,
            "silver",       <.75, .75, .75>];

string  gBlankUUID = "a2d3fdcf-febe-1481-09c7-a662f352f15e"; // Used for unrendered Unicode blocks.
string  gASCII_UUID; // Used to speed up rendering for ASCII, set to 0x00 code page below.
list    gCodePages;
list    gCodePageUUIDs = [
            0x00, "27e9e604-b315-454f-770e-cf5dc6333879",
            0x01, "fdcf478b-302d-70f8-fb72-c2cbf403d242",
            0x02, "10b6e068-571f-c912-1177-c25533b5350b",
            0x03, "ed4b350a-d0cb-68fa-e01c-7a4662837ad6",
            0x04, "090834da-5503-aeb9-8f42-f979c76a0f35",
            0x05, "d2378c82-ce3a-19c2-a25c-ea84b5d87b39",
            0x06, "93917f55-2427-365b-6d81-46871d3eb8d7",
            0x0E, "deadeda9-4676-9f75-b11d-0c1c4cc320af",
            0x10, "03088af6-b6e2-7a93-3ac4-b275b650a12b",
            0x14, "92c4d466-02c3-6063-440d-686a17287ef3",
            0x15, "96424a86-271d-2d64-4807-d6710e27afd8",
            0x16, "b7f7a0e7-e528-a504-2c52-171ea216982b",
            0x1D, "756ad03c-2e87-1bd2-8265-edf77f9493e6",
            0x1E, "6ba77713-1017-72d5-96c0-9b9305659e1e",
            0x1F, "047f7d75-cfcd-5515-227f-668554d7427d",
            0x20, "f40f5d7d-58e5-68e3-5c21-ba2a0f18e0a9",
            0x21, "6fce7405-d606-bb55-8ddd-f32f444b78da",
            0x22, "bb7bea3c-9044-e505-41d6-afafd6a9f5de",
            0x23, "5ca29772-2722-011f-8e04-3bfe1e713864",
            0x24, "0dede3b3-e632-8059-1a33-125f3e100e52",
            0x25, "87a27d99-2e97-2613-c47b-63806981b6e5",
            0x26, "8c382389-5701-4d3a-62d2-6e8720dc665f",
            0x27, "c76498fc-03a3-f598-fa7d-24b4876f0c26",
            0x2C, "7a702e38-9304-cbde-e5ab-a60a020f1d1d",
            0x30, "bbed1e3f-f89b-49c4-999c-80cc352189f6",
            0x31, "504c15c1-e9b5-8691-8b9a-574b0eb16633",
            0x32, "3f47af69-cb2e-8e85-d2d9-09c869822419",
            0x33, "eb7c701e-ac4a-9c2b-19a9-afc7f08c4675",
            0x34, "2cf174bd-0deb-2970-d63d-e359f7512521",
            0x35, "1f9bb5a7-2f4a-15e3-8d6d-504cd0d250de",
            0x36, "99d49a10-42bb-45a9-03ed-c81dea3f2d12",
            0x37, "441e23c4-0608-59fe-7e56-99e53f1c71ba",
            0x38, "9582249b-5370-dd77-0925-c97e72f6d8e9",
            0x39, "3c79958e-bdf2-73cd-2e6c-f2acc297bfcd",
            0x3A, "2286bbb7-f805-690f-0b0b-0593c12e2f2a",
            0x3B, "a2e5a0d0-f5aa-913f-1c00-f641f2ca5091",
            0x3C, "955e9609-afde-ebb7-a5e1-ddae46455090",
            0x3D, "431e9f87-41a2-a7f3-22ad-c17b4ec5a237",
            0x3E, "b5db2e3b-2271-a0bd-00d6-8b40812097ac",
            0x3F, "76f2d1fe-826d-f30a-c1af-1b09387c2936",
            0x40, "f90e3a5e-9404-0729-0ddc-46f52fc8e919",
            0x41, "70a5bc82-7abb-763b-fd46-12c9e4c60a84",
            0x42, "1b4af3ed-1ca2-54da-2f13-2c378476c50b",
            0x43, "33c44a35-5bdd-3cf0-9e20-bbebc4390ae7",
            0x44, "78468268-b9dc-57f4-554a-097341f9e37f",
            0x45, "be4f77d7-e86d-9c19-50f4-ff70fa0bbcdd",
            0x46, "cecc557a-e740-3468-787a-a8efc50afb82",
            0x47, "04d78b83-693d-8c16-4a1f-634c5dd6615a",
            0x48, "7e01d0db-b456-3cb8-b97c-f688dc27f705",
            0x49, "55d04868-f003-4de0-5237-a04862cc4697",
            0x4A, "afa697ab-2885-8d7c-f59b-b0f48b94941f",
            0x4B, "07f7427f-fc20-9d10-7ffd-556fb3c480a9",
            0x4C, "ff6b4d03-ca92-e7d4-46e9-9121352dec6e",
            0x4D, "c41ac88b-4e71-d997-cd33-fd1d81ca992c",
            0x4E, "c2309d45-43b7-15f4-e482-886dbf9b8419",
            0x4F, "3190730d-de06-ea8a-3a5d-757b5ef9c04d",
            0x50, "dcdf69a0-83c0-68d3-7883-9d6b142ab522",
            0x51, "8214ba5e-af73-0ed3-84f6-1251d668ce09",
            0x52, "0aa80f45-305c-a8b7-fdc5-c49cdb837d43",
            0x53, "261cb0e8-a2d7-b90d-734f-409064920bec",
            0x54, "0ad4e700-c8db-dc9f-6dea-45d126ce1781",
            0x55, "81f351a3-4a90-e052-22d7-daa869ee3656",
            0x56, "7df297e5-79cd-7036-9443-f0f8a9fa7e8f",
            0x57, "e06b0624-4363-2202-96b9-47b1321abafe",
            0x58, "9dfa4ed2-5146-0c20-4c1b-d67611591a2d",
            0x59, "7a0d489d-bf9c-4e76-bc30-65f9606a77a9",
            0x5A, "ab196901-2d9c-23d5-a10a-e28fd7b784a9",
            0x5B, "c569ab67-1c18-307a-0d57-bafa4e0320e7",
            0x5C, "cc92b193-1ed3-72ed-428f-de27c971e53e",
            0x5D, "3d9233a1-acbf-e28b-bfd9-db9d080daaaf",
            0x5E, "7da71ac2-af51-48b8-5207-70991b2b172b",
            0x5F, "cf34309e-b3e7-9777-6b04-2a64893ccc83",
            0x60, "6a449a86-c107-d264-ff67-8241347d865d",
            0x61, "e4f9c21d-8508-e64b-d390-3c85f06dea17",
            0x62, "c3a3ce13-6dec-8e81-d2a4-3125559bb782",
            0x63, "52bff60e-65c7-a540-ff35-95c5a8220f81",
            0x64, "9aeca54a-3ed9-6692-098b-2ec3da979cb3",
            0x65, "20c82000-a1d8-9cc3-bf40-e4b4e2472018",
            0x66, "58ae46d4-2e5b-cacb-101a-6cef0987d75a",
            0x67, "cf8f267d-6b6f-fd88-8588-48e886dc3010",
            0x68, "e603db4d-1e85-516a-b612-4b1b748fc3e2",
            0x69, "4122d3ed-68b9-2eba-dd7d-b8a0f59126a2",
            0x6A, "6a4425cf-46c7-1dd3-1e15-bc58b6e63522",
            0x6B, "3402c9d6-b776-2f3f-7d8d-855cd9a7f7e7",
            0x6C, "09710c77-9db2-65ff-db0b-400f42b55671",
            0x6D, "b0fca79a-5060-324f-f4f5-71cffac18e1f",
            0x6E, "cd8d52f4-32d1-4ea3-6908-8ed9204d4f8f",
            0x6F, "90e38c28-d6a9-fca4-0e39-b24adf825ba8",
            0x70, "b25aadb4-f64a-6420-b479-277edea2a169",
            0x71, "ced5dcf5-58a8-d7b3-0da8-cb10f9b708f8",
            0x72, "515461e6-1aca-5056-d289-705a1c070ef4",
            0x73, "226100cc-10ce-8cb7-f7a8-d13873493374",
            0x74, "37d54277-71b2-dd6f-ebff-666aa4c6efd0",
            0x75, "38b2a124-4ef3-9dc0-e4c4-b4d1ee25811a",
            0x76, "d8c218ff-97b0-f320-7f2e-ba74fcd3e19c",
            0x77, "8d68593e-90fb-c442-b320-c6e99cd831b2",
            0x78, "a1b3619d-eb8f-03c2-e219-375ab2e978c3",
            0x79, "b25f989c-ea35-3398-7809-d0e47415e1ec",
            0x7A, "b3d35e10-70f0-4004-3d4f-8987e77c3ce6",
            0x7B, "6ff601ba-64fb-f61b-c11a-95c4e26cc3b5",
            0x7C, "5c5508de-ca4a-1a85-3662-7767af1d45f1",
            0x7D, "f334c84a-8a89-4dca-1a0a-3f57869b383a",
            0x7E, "6d4992fc-1891-7bb8-e8c8-080b0c7f0f53",
            0x7F, "1c087c0c-2f44-70c6-f386-9fff328645af",
            0x80, "ae6217d8-a650-393d-4c12-244924e50091",
            0x81, "5bac0887-f686-1486-123d-c9cc203a97d7",
            0x82, "4c00bbf3-25d7-c781-ad69-f2c8b151844d",
            0x83, "02146f13-b5a4-34d4-eae3-b87e8a622446",
            0x84, "149a8ebe-fa15-b985-b6ca-4b4f8c8dcbc6",
            0x85, "899f9215-92ca-39bc-b157-46b4e56ffee2",
            0x86, "07c72032-8ba0-58b5-7dbb-1e26d4a9c29d",
            0x87, "021ca04d-5893-f615-9357-5ec1fd1e0985",
            0x88, "f13f10ab-8526-a061-b90e-38b0f13876a9",
            0x89, "9d8895f4-1080-69f7-0f78-cc7c42068402",
            0x8A, "35363fbc-f952-3833-f2b8-ac1685decb41",
            0x8B, "ece7161f-2360-e294-55f8-18593cfe268e",
            0x8C, "b199f897-ce70-3715-05e0-a58c234e21e7",
            0x8D, "066676e6-5640-399e-0191-b061e56a9277",
            0x8E, "b5e67788-bd9b-9603-9f5f-8c8fc90dbcdf",
            0x8F, "180bb534-f8fb-b8cd-fcb9-938eb41876f6",
            0x90, "42d6a5c7-3537-0e6a-ceb1-c7ec1408843e",
            0x91, "28d50a1f-aae9-e9ae-df70-dad6d0dd494b",
            0x92, "4638765a-bf63-95fb-dfef-df43e3fd6b0e",
            0x93, "c183e0ac-c3bf-cbcc-79d8-2877e5aeaa87",
            0x94, "db5df7a0-b48e-28ac-e24a-0222a3cda022",
            0x95, "3f5e9f00-86bc-b5a4-8930-61a8c2f94dbc",
            0x96, "d92d47bf-0582-fa1c-5e62-3ef591f2a12b",
            0x97, "a2603a86-209d-d36c-2df8-03ad69418439",
            0x98, "d1b3c91d-3d5a-53f8-9fdc-149fb77cfdfc",
            0x99, "c4a69385-91f1-375c-b9d6-86eb1b8ed537",
            0x9A, "4c9dd325-deb5-b5b3-7b94-c6dd0aec5a99",
            0x9B, "8ba75a75-1421-bc42-6a41-3cef5ff131ad",
            0x9C, "33aecc7d-ab14-c2d8-1428-1379a73a69a2",
            0x9D, "dbb8d20e-e182-67ec-955d-33de256e6241",
            0x9E, "9dd876bf-f802-4cd6-5395-ba00d5e1b3b2",
            0x9F, "a60a2bea-4e28-78a1-d9da-887b60a219ef",
            0xA6, "24f26d30-c396-b3fb-42b6-f3ba01b7ed87",
            0xA7, "39102d6d-227b-86f1-e44b-324a7bf58bf4",
            0xF8, "21ad1fb8-214f-c9db-74d5-317e692d7bb7",
            0xFE, "33d6e3ce-e1bb-816a-6133-1af0077a67b5",
            0xFF, "5709c611-6a62-244f-5963-dda110a59f04"];

Flush()
{
    integer i;
    gRowLengths = [];

    while (i++ < gRows) gRowLengths += 0xFFFF;
}

Render(list chars, integer col, integer row, integer direct)
{
    if (col < 0 || col >= gCols || row < 0 || row >= gRows) return;

    integer len = llGetListLength(chars);
    integer cursor;
    integer unicode;
    integer i;
    integer face;
    integer row_index = row * gColPrims;
    integer clear = (gForce || len < llList2Integer(gRowLengths, row)) && !direct; // Never clear if using direct access
    list    params;

    if      (direct)        cursor =  col;
    else if (gAlign == 0 || len == 0) cursor =  0;
    else if (gAlign == 1)   cursor = (gCols - len) / 2;
    else                    cursor =  gCols - len;

    if (cursor + len > gCols) len = gCols - cursor;

    // Using direct invalidates optimization for this row.
    if (direct) gRowLengths = llListReplaceList(gRowLengths, [0xFFFF], row, row);
    else        gRowLengths = llListReplaceList(gRowLengths, [len], row, row);

    // Clear out everything before first char
    if (cursor > 0 && clear)
    {
        while (i < cursor)
        {
            face = i & 7;

            if (face) ++i;
            else
            {
                // If this is a new prim, set the target link #.
                params += [ PRIM_LINK_TARGET, llList2Integer(gTextLinks, row_index + (i >> 3)) ];

                // If the whole prim is to be blanked, do it with a single command
                if (i + 7 < cursor)
                {
                    face = ALL_SIDES;
                    i += 8;
                }
                else ++i;
            }

            params += [ PRIM_TEXTURE, face, gASCII_UUID, gCellSize, gSpaceOffset, 0 ]; //, PRIM_COLOR, face, <1, 1, 1>, 0 ];
        }

        // Specify the first column position prim as the default.
        llSetLinkPrimitiveParamsFast(llList2Integer(gTextLinks, row_index), params);
        params = [];
    }

    // Draw the line, making sure any fw_direct calls don't draw off the end.
    i = 0;

    while (i < len)
    {
        unicode = llList2Integer(chars, i);

        if (unicode > 0)
        {
            // Single cell mode
            params += [ PRIM_TEXTURE, cursor & 7, llList2String(gCodePages, unicode >> 8 & 0xFF),
                        gCellSize, <(unicode & 0xF) * .0625 - gOffset.x, gOffset.y - (unicode >> 4 & 0xF) * .0625, 0>, 0,
                        PRIM_COLOR, cursor & 7, gColor, gAlpha ];
        }
        else if (unicode & 0x10000000)
        {
            // 2XKanji Left Half
            params += [ PRIM_TEXTURE, cursor & 7, llList2String(gCodePages, unicode >> 8 & 0xFF),
                        gCellSizeHalf, <(unicode & 0xF) * .0625 - gOffsetLeft.x, gOffsetLeft.y - (unicode >> 4 & 0xF) * .0625, 0>, 0,
                        PRIM_COLOR, cursor & 7, gColor, gAlpha ];
        }
        else // if (unicode & 0x20000000)
        {
            // 2XKanji Right Half
            params += [ PRIM_TEXTURE, cursor & 7, llList2String(gCodePages, unicode >> 8 & 0xFF),
                        gCellSizeHalf, <(unicode & 0xF) * .0625 - gOffsetRight.x, gOffsetRight.y - (unicode >> 4 & 0xF) * .0625, 0>, 0,
                        PRIM_COLOR, cursor & 7, gColor, gAlpha ];
        }

        // Last face of the prim, or end of line, draw the faces. (End of row would fall on 7th face)
        if (cursor & 7 == 7 || ++i == len)
        {
            llSetLinkPrimitiveParamsFast(llList2Integer(gTextLinks, row_index + (cursor >> 3)), params);
            params = [];
        }

        ++cursor;
        // Note the ++i is in the test above.
    }

    // Clear out everything after last char
    if (cursor < gCols && clear)
    {
        i = cursor;

        while (i < gCols)
        {
            face = i & 7;

            if (face) ++i;
            else
            {
                // If this is a new prim, set the target link #.
                params += [ PRIM_LINK_TARGET, llList2Integer(gTextLinks, row_index + (i >> 3)) ];

                // If the whole prim is to be blanked, do it with a single command
                if (i + 7 < cursor)
                {
                    face = ALL_SIDES;
                    i += 8;
                }
                else ++i;
            }

            params += [ PRIM_TEXTURE, face, gASCII_UUID, gCellSize, gSpaceOffset, 0 ]; //, PRIM_COLOR, face, <1, 1, 1>, 0 ];
        }

        // Specify the cursor position prim as the default.
        llSetLinkPrimitiveParamsFast(llList2Integer(gTextLinks, row_index + (cursor >> 3)), params);
   }
}

// If line is one long paragraph to be displayed, break it up into row size chunks
// so we don't have to decode the whole paragraph before starting to render.
// This is slower than decoding the entire line in one pass, but uses less memory.
// Pad it a bit, so we don't end up with an empty chars list before the line is truly done rendering.
list UTFtoInt(list chars, string line, integer pos)
{
    integer len = llStringLength(line);
    string  input;
    //integer long1;
    integer long2;
    integer char;
    integer colmax = gCols + 2;

    while (pos < len && llGetListLength(chars) < colmax)
    {
        // Unicode Decoder: http://wiki.secondlife.com/wiki/UTF-8
        char = llBase64ToInteger(llStringToBase64(input = llGetSubString(line, pos, pos)));

        if (char > 0) chars += char >> 24;
        else
        {
            // Multibyte, use smart shifting. Skip decoding unicode greater than 0x3FFFF for speed
            long2 =   (integer)("0x"+llGetSubString(input = (string)llParseString2List(llEscapeURL(input),(list)"%",[]),-8,-1));
            //long1 = (integer)("0x"+llDeleteSubString(input,-8,-1));
            char =  (   (  0x0000003f & long2       )
                      | (( 0x00003f00 & long2) >> 2 )
                      | (( 0x003f0000 & long2) >> 4 )
                    //| (( 0x3f000000 & long2) >> 6 )
                    //| (( 0x0000003f & long1) << 24)
                    //| (( 0x00000100 & long1) << 22)
                    ) & (0x7FFFFFFF >> (5 * ((integer)(llLog(~char) / 0.69314718055994530941723212145818) - 25)));

            // Mark 2x characters as negative by setting top bit. Also set a bit to indicate left/right part of char.
            if (g2XKanji && char > 0x2FFF && char < 0xA000) chars += [char | 0x90000000, char | 0xA0000000];
            else chars += char;
        }

        ++pos;
    }

    gPos =  pos;
    return chars;
}

Draw(string text)
{
    integer total_lines = llGetListLength(llParseStringKeepNulls(text, (list)"\n", []));
    string  line;
    integer row = 0;
    integer line_num = 0;
    list    chars;
    integer char;
    integer pos_end;
    integer pos_out;

    do
    {
        // Re-parsing the text for each line is a tradeoff between speed and memory usage.
        if (gTrim)  line = llStringTrim(llList2String(llParseStringKeepNulls(text, (list)"\n", []), line_num), STRING_TRIM);
        else        line =              llList2String(llParseStringKeepNulls(text, (list)"\n", []), line_num);

        chars = [];
        gPos = 0;

        do
        {
            chars = UTFtoInt(chars, line, gPos);

            if (llGetListLength(chars) <= gCols || gWrap == 0)
            {
                Render(chars, 0, row, FALSE);

                // Done with this line.
                chars = [];
            }
            else if (llList2Integer(chars, gCols) == 32 || gWrap == 1)
            {
                Render(llList2List(chars, 0, gCols - 1), 0, row, FALSE);

                // If we got here with gWrap = 2, then skip the space
                chars = llDeleteSubList(chars, 0, gCols - (gWrap == 1));
            }
            else
            {
                // Handle finding a word wrap location.
                pos_end = gCols - 1;
                pos_out = 0;

                do
                {
                    char = llList2Integer(chars, pos_end);

                    // Test for space
                    if      (char == 32) pos_out = pos_end - 1;
                    // Test for hyphen. Could also test for Japanese: "、" and "。", Hebrew: "־‬", Armenian: "֊"
                    else if (char == 45) pos_out = pos_end;
                    // Test for falling below wrap limit.
                    else if (pos_end < gCols * gWrapLimit)
                    {
                        // Test to see if last char is first half of split Kanji char.
                        if (llList2Integer(chars, gCols - 1) & 0x10000000) pos_out = gCols - 2;
                        else pos_out = gCols - 1;
                    }
                }
                while (!pos_out && --pos_end >= 0);

                Render(llList2List(chars, 0, pos_out), 0, row, FALSE);

                // If we wrapped on a space, delete it too, so it doesn't render on next line.
                chars = llDeleteSubList(chars, 0, pos_out + (char == 32));
            }
        }
        while (llGetListLength(chars) && ++row < gRows);
    }
    while (++line_num < total_lines && row < gRows);

    // Blank out any remaining display lines
    while (row < gRows)
    {
        Render([], 0, row, FALSE);
        ++row;
    }

    if (gNotify) llMessageLinked(LINK_SET, 0, "", "fw_done");
}

default
{
    state_entry()
    {
        gPrimCount = llGetObjectPrimCount(llGetKey())+llGetNumberOfPrims()*!!llGetAttached();

        integer link = gPrimCount;
        integer col = -1;
        integer row = -1;
        integer i;
        integer j;
        list    items;

        do
        {
            items = llParseString2List(llGetLinkName(link), (list)":", []);
            if (llList2String(items, 0) == "FURWARE text mesh")
            {
                if (llGetLinkNumberOfSides(link) == 8)
                {
                    if (llList2Integer(items, 2) > row) row = llList2Integer(items, 2);
                    if (llList2Integer(items, 3) > col) col = llList2Integer(items, 3);
                }
                else
                {
                    llOwnerSay("Only 8 face text prims supported");
                    return;
                }
            }
        }
        while (--link > 0);

        if (col < 0 || row < 0)
        {
            llOwnerSay("No text prims found");
            return;
        }

        gCols = ++col * 8;
        gColPrims = col;
        gRows = ++row;
        gTextLinks = [];
        link = gPrimCount;

        for (i = 0; i < row * col; ++i) gTextLinks += 0;

        do
        {
            items = llParseString2List(llGetLinkName(link), (list)":", []);
            if (llList2String(items, 0) == "FURWARE text mesh")
            {
                i = llList2Integer(items, 2) * col + llList2Integer(items, 3);
                gTextLinks = llListReplaceList(gTextLinks, (list)link, i, i);
            }
        }
        while (--link >= 0);

        for (i = 0; i < 256; ++i)
        {
            j = llListFindList(gCodePageUUIDs, (list)i);
            if (~j) gCodePages += llList2String(gCodePageUUIDs, j + 1);
            else    gCodePages += gBlankUUID;
        }

        gCodePageUUIDs = []; // No longer needed, empty it to free up memory?
        gASCII_UUID = llList2String(gCodePages, 0);
        gSpaceOffset = <-gOffset.x, gOffset.y - 2 * .0625, 0>;

        Flush(); // Invalidate the whole display
        Draw("");

        llMessageLinked(LINK_SET, 0, "", "fw_ready");
    }

    link_message(integer source, integer num, string str, key id)
    {
        if (llGetSubString(id, 0, 2) != "fw_") return;

        list    commands = llParseString2List(llToLower(id), (list)":", []);
        string  command  = llStringTrim(llList2String(commands, 0), STRING_TRIM);
        list    options;
        list    params;
        string  param;
        string  value_lc;
        integer i;
        integer pos;

        if      (command == "fw_data")
        {
            Draw(str);
        }
        else if (command == "fw_direct")
        {
            Render(UTFtoInt([], str, 0), llList2Integer(commands, 1), llList2Integer(commands, 2), TRUE);
        }
        else if (command == "fw_conf" || command == "fw_defaultconf")
        {
            options = llParseString2List(llToLower(str), (list)";", []);

            for(i = 0; i < llGetListLength(options); ++i)
            {
                params = llParseString2List(llList2String(options, i), (list)"=", []);

                if (llGetListLength(params) > 1)
                {
                    param =    llStringTrim(llList2String(params, 0), STRING_TRIM);
                    value_lc = llStringTrim(llList2String(params, 1), STRING_TRIM);

                    if (param == "c")
                    {
                        pos = llListFindList(gColors, (list)value_lc);
                        gAlpha = 1;

                        if      (pos == 0)
                        {
                            gColor = ;
                        }
                        else if (pos > 0)
                        {
                            gColor = llList2Vector(gColors, pos + 1);
                        }
                        else
                        {
                            value_lc = "<" + value_lc + ">";
                            rotation color = (rotation)value_lc;

                            if (color == ZERO_ROTATION)
                            {
                                gColor = (vector)value_lc;
                                gAlpha = 1;
                            }
                            else
                            {
                                gColor = ;
                                gAlpha = color.s;
                            }
                        }
                    }
                    else if (param == "a")
                    {
                        pos = llListFindList([ "left", "center", "right" ], (list)value_lc);
                        if (~pos)
                        {
                            if (gAlign != pos) Flush();
                            gAlign = pos;
                        }
                    }
                    else if (param == "w")
                    {
                        pos = llListFindList([ "none", "char", "word" ], (list)value_lc);
                        if (~pos) gWrap = pos;
                    }
                    else if (param == "t")
                    {
                        gTrim = (value_lc == "on");
                    }
                    else if (param == "k")
                    {
                        g2XKanji = (value_lc == "on");
                    }
                    else if (param == "force")
                    {
                        gForce = (value_lc == "on");
                    }
                } // more than 1 param
            } // iterate options
        }
        else if (command == "fw_memory")
        {
            llOwnerSay("HexText Free Mem: " + (string)llGetFreeMemory());
        }
        else if (command == "fw_notify")
        {
            gNotify = (llToLower(llStringTrim(str, STRING_TRIM)) == "on");
        }
        else if (command == "fw_reset")
        {
            llResetScript();
        }
    }

    changed(integer change)
    {
        // Must reset, only time we search for link names.
        if (change & CHANGED_LINK &&
            gPrimCount != llGetObjectPrimCount(llGetKey())+llGetNumberOfPrims()*!!llGetAttached())
        {
            llResetScript();
        }
    }
}
```