---
name: "Notecard Configuration Reader by Maddox Deluxe"
category: "example"
type: "example"
language: "LSL"
description: "Read the script comments to have better understanding of the codes. [v1.6 Video]"
wiki_url: "https://wiki.secondlife.com/wiki/Notecard_Configuration_Reader_by_Maddox_Deluxe"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

## This new update has been tested and works great

Read the script comments to have better understanding of the codes. [[v1.6 Video](http://youtu.be/f9hRGWNW7a4)]

**Fixes in v1.6**

- Backdrop uuid now checks for NULL KEY
- Checks the notecard for saved data
- Clean up the script

**Fixes in v1.5**

- New uuid Key checking function

**Fixes in v1.4**

- Themes list format adding

**Fixes in v1.3**

- Empty notecard data error checking
- Spaces error checking
- Add few more comments to some codes

**Fixes in v1.2**

- Key names error checking
- Other fixes that are not listed

**Useful Functions - (See main script comments)**

- DumpListFind(list db, string name)
- integer IsElement(list db, string search)
- integer KeyNameCheck(list db, string search)
- integer isKey(key uuid)




First make a notecard called (Category Theme).Fantasy and copy the data of this one into it. The 00000000-0000-0000-0000-000000000000 just means no floor drop, but holds the key format still for error checking. The notecard format can not have line spaces and need to be done just how you see the notecard settings here, the error checking works great for the script.

```lsl
// our test notecard
[Author Name] = Maddox Deluxe
// Theme [1]
[Menu Button Name] = Fantasy Tiger
[BackDrop Texture UUID] = 8f304cf2-7120-24e2-d1f1-db6b31bd6f6c
[FloorDrop Texture UUID] = 00000000-0000-0000-0000-000000000000
// Theme [2]
[Menu Button Name] = Fantasy Car
[BackDrop Texture UUID] = 517b2288-67ca-b14c-1de2-c5f5fdf5291f
[FloorDrop Texture UUID] = 00000000-0000-0000-0000-000000000000
// Theme [3]
[Menu Button Name] = Fantasy Tree
[BackDrop Texture UUID] = f6321118-cc24-6230-78a5-a257a3e33378
[FloorDrop Texture UUID] = 00000000-0000-0000-0000-000000000000
```

Or with out the comments.

```lsl
[Author Name] = Maddox Deluxe
[Menu Button Name] = Fantasy Tiger
[BackDrop Texture UUID] = 8f304cf2-7120-24e2-d1f1-db6b31bd6f6c
[FloorDrop Texture UUID] = 00000000-0000-0000-0000-000000000000
[Menu Button Name] = Fantasy Car
[BackDrop Texture UUID] = 517b2288-67ca-b14c-1de2-c5f5fdf5291f
[FloorDrop Texture UUID] = 00000000-0000-0000-0000-000000000000
[Menu Button Name] = Fantasy Tree
[BackDrop Texture UUID] = f6321118-cc24-6230-78a5-a257a3e33378
[FloorDrop Texture UUID] = 00000000-0000-0000-0000-000000000000
```

Our main script called (CODE).Notecard.Reader

```lsl
// Notecard Multi-line Entries Configuration Reader v1.6 by Maddox Deluxe
// Error Checking for: Key Names, values, Empty Notecard Data, Line Spaces
// This script is free; you can redistribute it and/or modify it
// Just read the comments on the script

key NotecardQueryId;          // key name of the notecard
key LineRequestID;            // notecard line count
integer LineTotal;            // The number of lines in the notecard
integer LineIndex;            // index for data read requests

string Author_Name = "";      // variable for setting author name
string Menu_Button_Name = ""; // variable for setting menu button name to the themes list
string Back_Drop_UUID = "";   // variable for setting backdrop uuid key to the themes list
string Floor_Drop_UUID = "";  // variable for setting floor drop uuid key to the themes list

string data;                  // notecard data
string GetNoteName;           // notecard name

list Themes;                  // our list database for testing
list KeyNames;                // our list database for the key names: [Author Name]. [Menu Button Name], ect..

integer ThemesCount;          // counts how many themes they are in the notecard configuration

key User;                     // user tracker key

// function by Maddox Deluxe
// test to dump all 3 elements in the list that goes with each other
DumpListFind(list db, string name)
{
 integer index = llListFindList(db, [name]);
        if (~index)
        {
            list Found = llList2List(db, index, index + 2);

            string BN = llList2String(Found,0);
            string BD = llList2String(Found,1);
            string FD = llList2String(Found,2);

            llOwnerSay("Dump testing for list database search.\nAuthor Name: "+(string)Author_Name+ "\nButton Name: "+(string)BN+ "\nBackdrop Texture: "+(string)BD+ "\nFloor drop Texture: "+(string)FD);

    llOwnerSay("List Dump Found Test: "+llDumpList2String(Found, ","));

  //  llMessageLinked(LINK_SET, 0,"SET BACKDROP TEXTURE",(string)BD);
            if(FD != (key)"00000000-0000-0000-0000-000000000000")
            {
 //    llMessageLinked(LINK_SET, 0,"SET FLOOR DROP TEXTURE",(string)FD);
            }

        }
}
// function by Maddox Deluxe
// looks for 3 elements and the search string is the first element of the set
integer IsElement(list db, string search)
{
 integer index = llListFindList(db, [search]);
        if (~index)
        {
            list Found = llList2List(db, index, index + 2);

            string str = llList2String(Found,0);
            if (str == search)
            return TRUE; // was found
        }
        return FALSE; // was not found
 }
// function by Maddox Deluxe
// checks the key names making sure they match what is setup in the notecard
integer KeyNameCheck(list db, string search)
{
    integer i;
    for (i=0;i