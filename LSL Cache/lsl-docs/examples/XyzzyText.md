---
name: "XyzzyText"
category: "example"
type: "example"
language: "LSL"
description: "Scripting tools to allow display of text on a prim: XyText 1.5 , XyzzyText, XyyyyzText, XyText-UTF8, XyzzyText-UTF8, ZZText, VariText"
wiki_url: "https://wiki.secondlife.com/wiki/XyzzyText"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 Copyright & Licensing
- 2 XyzzyText - 5 Character

  - 2.1 Main Script
  - 2.2 Slave Script
  - 2.3 Prim Setup
- 3 How to produce textures with alternative fonts for 5 character version (Photoshop VBscript version)
- 4 How to produce textures with alternative fonts for 5 character version (GIMP script-fu version)
- 5 XyzzyText - 10 Character

  - 5.1 Master Script
  - 5.2 Slave Script
  - 5.3 10-Char Prim Setup
- 6 XyzzyText - 16 Character MESH PLANE (Modification by Traven Sachs)

  - 6.1 Master Script
  - 6.2 Slave Script
  - 6.3 16-Char MESH Prim Setup

Scripting tools to allow display of text on a prim: XyText 1.5 , XyzzyText, XyyyyzText, XyText-UTF8, XyzzyText-UTF8, ZZText, VariText

**XyzzyText** is a new version of XyText 1.5 with some advanced features:

- Efficiency!  You can now control an entire linkset with just one script.
- Flexible Speed vs Lag.  Just drop in plug-and-play slave scripts to increase rendering speed.  (More than 4-5 slaves not recommended, there is diminishing returns)
- Ease of use.  There is no need to know link numbers.  Simply name the child prims xyzzytext-banknumber-cellnumber.
- To use, pass the bank number to use in the "key" field of the link message of DISPLAY_STRING/EXTENDED.

Copyright & Licensing

- Traven Sachs hereby releases his contributions to this under the MIT license (16 Char MESH Prim Mod).
- Gigs Taggart hereby releases his contributions to this under the MIT license.
- Thraxis Epsilon hereby releases his contributions to this under the MIT license.
- Strife Onizuka hereby releases his contributions to this under the MIT license.
- Huney Jewell hereby releases her contributions to this under the MIT license.
- Salahzar Stenvaag hereby releases his contributions to this under the MIT license. (photoshop/GIMP vbs script for alternative fonts plus ZZText)
- Ruud Lathrop hereby releases her contributions to this under the MIT license.
- Joel Cloquet hereby releases his contributions to this under the MIT license.

XyzzyText - 5 Character

Example:

```lsl
Display Prims named:
xyzzytext-0-0 xyzzytext-0-1
xyzzytext-1-0 xyzzytext-1-1
```

Quickstart:

```lsl
* Store all scripts in your inventory
* Rez a box
* Drop the prim setup script in it (You now have one unit, name it xyzzytext-0-0)
* Make a row of four of these prims (xyzzytext-0-0 xyzzytext-0-1,xyzzytext-0-2,xyzzytext-0-3)
* Move a copy of this row a little down, and rename the new row(xyzzytext-1-0 xyzzytext-1-1,xyzzytext-1-2,xyzzytext-1-3)
* Do this for every row you make
* Create a big box that serves as the board-background(mainprim)
* Link all prims with the mainprim(selected last), so the mainprim keeps yellow after linking(root-prim)
* Copy the main script and usage script into the root prim
* Type something, and check if it all works
* Flatten the prims, so the text looks straight
* Consider adding slave scripts to the root prim if you have a lot of rows
```

Usage:

```lsl
integer DISPLAY_STRING      = 204000;
integer DISPLAY_EXTENDED    = 204001;
integer REMAP_INDICES       = 204002;
integer RESET_INDICES       = 204003;
integer SET_FADE_OPTIONS    = 204004;
integer SET_FONT_TEXTURE    = 204005;
integer SET_LINE_COLOR      = 204006;
integer SET_COLOR           = 204007;
integer RESCAN_LINKSET      = 204008;

integer gToggle;

default
{
    state_entry()
    {
        llListen(0,"",NULL_KEY,"");

    }


    listen(integer channel,string name, key id, string message)
    {
        if (gToggle)
            llMessageLinked(LINK_THIS,DISPLAY_STRING,name + ":"+ message,"0");
        else
            llMessageLinked(LINK_THIS,DISPLAY_STRING,name + ":"+ message,"1");

        gToggle=!gToggle;

    }
}
```

## Main Script

```lsl
////////////////////////////////////////////
// XyzzyText v2.1 Script (Set Line Color) by Huney Jewell
// XyzzyText v2.0 Script (5 Face, Single Texture)
//
//
// Edited trivially by Joel Cloquet on 1/2011 to use the (relatively)
// new llSetLinkPrimitiveParamsFast function, thereby removing the need in
// some cases to use the slave script.
//
// Heavily Modified by Thraxis Epsilon, Gigs Taggart 5/2007 and Strife Onizuka 8/2007
// Rewrite to allow one-script-per-object operation w/ optional slaves
// Enable prim-label functionality
// Enabled Banking
//
// Modified by Kermitt Quirk 19/01/2006
// To add support for 5 face prim instead of 3
//
// Core XyText Originally Written by Xylor Baysklef
//
//
////////////////////////////////////////////

/////////////// CONSTANTS ///////////////////
// XyText Message Map.
integer DISPLAY_STRING      = 204000;
integer DISPLAY_EXTENDED    = 204001;
integer REMAP_INDICES       = 204002;
integer RESET_INDICES       = 204003;
integer SET_FADE_OPTIONS    = 204004;
integer SET_FONT_TEXTURE    = 204005;
integer SET_LINE_COLOR      = 204006;
integer SET_COLOR           = 204007;
integer RESCAN_LINKSET      = 204008;

//internal API
integer REGISTER_SLAVE      = 205000;
integer SLAVE_RECOGNIZED    = 205001;
integer SLAVE_DISPLAY       = 205003;
integer SLAVE_DISPLAY_EXTENDED = 205004;
integer SLAVE_RESET = 205005;

// This is an extended character escape sequence.
string  ESCAPE_SEQUENCE = "\\e";

// This is used to get an index for the extended character.
string  EXTENDED_INDEX  = "12345";

// Face numbers.
integer FACE_1          = 3;
integer FACE_2          = 7;
integer FACE_3          = 4;
integer FACE_4          = 6;
integer FACE_5          = 1;

// Used to hide the text after a fade-out.
key     TRANSPARENT     = "701917a8-d614-471f-13dd-5f4644e36e3c";
key     null_key        = NULL_KEY;
///////////// END CONSTANTS ////////////////

///////////// GLOBAL VARIABLES ///////////////
// This is the key of the font we are displaying.
key     gFontTexture        = "b2e7394f-5e54-aa12-6e1c-ef327b6bed9e";
// All displayable characters.  Default to ASCII order.
string gCharIndex;

// This is whether or not to use the fade in/out special effect.
integer gCellUseFading      = FALSE;
// This is how long to display the text before fading out (if using
// fading special effect).
// Note: < 0  means don't fade out.
float   gCellHoldDelay      = 1.0;

integer gSlaveRegistered;
list gSlaveNames;

integer BANK_STRIDE=3; //offset, length, highest_dirty
list gBankingData;

/////////// END GLOBAL VARIABLES ////////////

ResetCharIndex() {
   gCharIndex  = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`";
   gCharIndex += "abcdefghijklmnopqrstuvwxyz{|}~";
   gCharIndex += "\n\n\n\n\n";
}

vector GetGridOffset(integer index) {
   // Calculate the offset needed to display this character.
   integer Row = index / 10;
   integer Col = index % 10;

   // Return the offset in the texture.
   return <-0.45 + 0.1 * Col, 0.45 - 0.1 * Row, 0.0>;
}

ShowChars(integer link,vector grid_offset1, vector grid_offset2, vector grid_offset3, vector grid_offset4, vector grid_offset5) {
   // Set the primitive textures directly.

   // <-0.256, 0, 0>
   // <0, 0, 0>
   // <0.130, 0, 0>
   // <0, 0, 0>
   // <-0.74, 0, 0>

   llSetLinkPrimitiveParamsFast( link,[
        PRIM_TEXTURE, FACE_1, (string)gFontTexture, <0.126, 0.1, 0>, grid_offset1 + <0.037, 0, 0>, 0.0,
        PRIM_TEXTURE, FACE_2, (string)gFontTexture, <0.05, 0.1, 0>, grid_offset2, 0.0,
        PRIM_TEXTURE, FACE_3, (string)gFontTexture, <-0.74, 0.1, 0>, grid_offset3 - <0.244, 0, 0>, 0.0,
        PRIM_TEXTURE, FACE_4, (string)gFontTexture, <0.05, 0.1, 0>, grid_offset4, 0.0,
        PRIM_TEXTURE, FACE_5, (string)gFontTexture, <0.126, 0.1, 0>, grid_offset5 - <0.037, 0, 0>, 0.0
        ]);
}

RenderString(integer link, string str) {
   // Get the grid positions for each pair of characters.
   vector GridOffset1 = GetGridOffset( llSubStringIndex(gCharIndex, llGetSubString(str, 0, 0)) );
   vector GridOffset2 = GetGridOffset( llSubStringIndex(gCharIndex, llGetSubString(str, 1, 1)) );
   vector GridOffset3 = GetGridOffset( llSubStringIndex(gCharIndex, llGetSubString(str, 2, 2)) );
   vector GridOffset4 = GetGridOffset( llSubStringIndex(gCharIndex, llGetSubString(str, 3, 3)) );
   vector GridOffset5 = GetGridOffset( llSubStringIndex(gCharIndex, llGetSubString(str, 4, 4)) );

   // Use these grid positions to display the correct textures/offsets.
   ShowChars(link,GridOffset1, GridOffset2, GridOffset3, GridOffset4, GridOffset5);
}

RenderWithEffects(integer link, string str) {
   // Get the grid positions for each pair of characters.
   vector GridOffset1 = GetGridOffset( llSubStringIndex(gCharIndex, llGetSubString(str, 0, 0)) );
   vector GridOffset2 = GetGridOffset( llSubStringIndex(gCharIndex, llGetSubString(str, 1, 1)) );
   vector GridOffset3 = GetGridOffset( llSubStringIndex(gCharIndex, llGetSubString(str, 2, 2)) );
   vector GridOffset4 = GetGridOffset( llSubStringIndex(gCharIndex, llGetSubString(str, 3, 3)) );
   vector GridOffset5 = GetGridOffset( llSubStringIndex(gCharIndex, llGetSubString(str, 4, 4)) );

   // First set the alpha to the lowest possible.
   llSetLinkAlpha(link,0.05, ALL_SIDES);

   // Use these grid positions to display the correct textures/offsets.
   ShowChars(link,GridOffset1, GridOffset2, GridOffset3, GridOffset4, GridOffset5);          // Now turn up the alpha until it is at full strength.
    float Alpha = 0.10;
    for (; Alpha <= 1.0; Alpha += 0.05)
       llSetLinkAlpha(link,Alpha, ALL_SIDES);
          // See if we want to fade out as well.
   if (gCellHoldDelay < 0.0)
       // No, bail out. (Just keep showing the string at full strength).
       return;
          // Hold the text for a while.
   llSleep(gCellHoldDelay);
      // Now fade out.
   for (Alpha = 0.95; Alpha >= 0.05; Alpha -= 0.05)
       llSetLinkAlpha(link,Alpha, ALL_SIDES);
          // Make the text transparent to fully hide it.
   llSetLinkTexture(link,TRANSPARENT, ALL_SIDES);
}

integer RenderExtended(integer link, string str, integer render) {
   // Look for escape sequences.
   integer length = 0;
   list Parsed       = llParseString2List(str, [], (list)ESCAPE_SEQUENCE);
   integer ParsedLen = llGetListLength(Parsed);

   // Create a list of index values to work with.
   list Indices;
   // We start with room for 5 indices.
   integer IndicesLeft = 5;

   string Token;
   integer Clipped;
   integer LastWasEscapeSequence = FALSE;
   // Work from left to right.
   integer i = 0;
   for (; i < ParsedLen && IndicesLeft > 0; ++i) {
       Token = llList2String(Parsed, i);

       // If this is an escape sequence, just set the flag and move on.
       if (Token == ESCAPE_SEQUENCE) {
           LastWasEscapeSequence = TRUE;
       }
       else { // Token != ESCAPE_SEQUENCE
           // Otherwise this is a normal token.  Check its length.
           Clipped = FALSE;
           integer TokenLength = llStringLength(Token);
           // Clip if necessary.
           if (TokenLength > IndicesLeft) {
               TokenLength = llStringLength(Token = llGetSubString(Token, 0, IndicesLeft - 1));
               IndicesLeft = 0;
               Clipped = TRUE;
           }
           else
               IndicesLeft -= TokenLength;

           // Was the previous token an escape sequence?
           if (LastWasEscapeSequence) {
               // Yes, the first character is an escape character, the rest are normal.
               length += 2 + TokenLength;
               if(render)
               {
                    // This is the extended character.
                    Indices += (llSubStringIndex(EXTENDED_INDEX, llGetSubString(Token, 0, 0)) + 95);

                    // These are the normal characters.
                    integer j = 1;
                    for (; j < TokenLength; ++j)
                    {
                       Indices += llSubStringIndex(gCharIndex, llGetSubString(Token, j, j));
                    }
                }
           }
           else { // Normal string.
               // Just add the characters normally.
               length += TokenLength;
               if(render)
               {
                   integer j = 0;
                   for (; j < TokenLength; ++j)
                   {
                       Indices += llSubStringIndex(gCharIndex, llGetSubString(Token, j, j));
                   }
                }
           }

           // Unset this flag, since this was not an escape sequence.
           LastWasEscapeSequence = FALSE;
       }
   }

   // Use the indices to create grid positions.
  if(render)
  {
       vector GridOffset1 = GetGridOffset( llList2Integer(Indices, 0) );
       vector GridOffset2 = GetGridOffset( llList2Integer(Indices, 1) );
       vector GridOffset3 = GetGridOffset( llList2Integer(Indices, 2) );
       vector GridOffset4 = GetGridOffset( llList2Integer(Indices, 3) );
       vector GridOffset5 = GetGridOffset( llList2Integer(Indices, 4) );

       // Use these grid positions to display the correct textures/offsets.
       ShowChars(link,GridOffset1, GridOffset2, GridOffset3, GridOffset4, GridOffset5);
   }
   return length;
}

integer ConvertIndex(integer index) {
   // This converts from an ASCII based index to our indexing scheme.
   if (index >= 32) // ' ' or higher
       index -= 32;
   else { // index < 32
       // Quick bounds check.
       if (index > 15)
           index = 15;

       index += 94; // extended characters
   }

   return index;
}

PassToRender(integer render,string message, integer bank)
{
//    float time;
    integer extendedlen = 0;
    integer link;
    integer i = 0;
    integer msgLen = llStringLength(message);
    string TextToRender;
    integer num_slaves=llGetListLength(gSlaveNames);
    string slave_name; //avoids unnecessary casts, keeping it as a string


    //get the bank offset and length
    integer bank_offset=llList2Integer(gBankingData, (bank * BANK_STRIDE));
    integer bank_length=llList2Integer(gBankingData, (bank * BANK_STRIDE) + 1);
    integer bank_highest_dirty=llList2Integer(gBankingData, (bank * BANK_STRIDE) + 2);

    integer x = 0;
    for (;x < msgLen;x = x + 5)
    {

        if (i >= bank_length)  //we don't want to run off the end of the bank
        {
            //set the dirty to max, and bail out, we're done
            gBankingData=llListReplaceList(gBankingData, (list)bank_length, (bank * BANK_STRIDE) + 2, (bank * BANK_STRIDE) + 2);
            return;
        }

        link = unpack(gXyTextPrims,(i + bank_offset));
        TextToRender = llGetSubString(message, x, x + 15);

        if(gSlaveRegistered && (link % (num_slaves + 1)))
        {
            slave_name=llList2String(gSlaveNames, (link % (num_slaves + 1)) - 1);
            if (render == 1)
               llMessageLinked(LINK_THIS, SLAVE_DISPLAY, TextToRender, (key)((string)link + "," + slave_name));
            if (render == 2)
            {
                //time = llGetAndResetTime();
                if(llSubStringIndex(TextToRender,"\e") > x)
                    extendedlen = 5;
                else
                    extendedlen = RenderExtended(link,TextToRender,0);
                if (extendedlen > 5)
                {
                    x += extendedlen - 5;
                }
               llMessageLinked(LINK_THIS, SLAVE_DISPLAY_EXTENDED, TextToRender, (key)((string)link + "," + slave_name));
              // llOwnerSay((string)llGetAndResetTime());
            }
               //sorry, no fade effect with slave
        }
        else
        {
            if (render == 1)
                RenderString(link,TextToRender);
            if (render == 2)
            {
                extendedlen = RenderExtended(link,TextToRender,1);
                if (extendedlen > 5)
                {
                    x += extendedlen - 5;
                }

            }
            if (render == 3)
                RenderWithEffects(link,TextToRender);
        }
        ++i;
    }

    if (bank_highest_dirty==0)
        bank_highest_dirty=bank_length;

    integer current_highest_dirty=i;
    while (i < bank_highest_dirty)
    {
        link = unpack(gXyTextPrims,(i + bank_offset));

        if(gSlaveRegistered && (link % (num_slaves+1) != 0))
        {
            slave_name=llList2String(gSlaveNames, (link % (num_slaves + 1)) - 1);
            llMessageLinked(LINK_THIS, SLAVE_DISPLAY, "     ", (key)((string)link + "," + slave_name));
            //sorry, no fade effect with slave
        }
        else
        {
            RenderString(link,"     ");
        }
        ++i;
    }
    gBankingData=llListReplaceList(gBankingData, (list)current_highest_dirty, (bank * BANK_STRIDE) + 2, (bank * BANK_STRIDE) + 2);
}

// Bitwise Voodoo by Gigs Taggart and optimized by Strife Onizuka
list gXyTextPrims;

integer get_number_of_prims()
{//ignores avatars.
    integer a = llGetNumberOfPrims();
    //Mono tweak
    vector size = llGetAgentSize(llGetLinkKey(a));
    while(size.z > 0)
    {
        --a;
        size = llGetAgentSize(llGetLinkKey(a));
    }
    return a;
}

//functions to pack 8-bit shorts into ints
list pack_and_insert(list in_list, integer pos, integer value)
{
//    //figure out the bitpack position
//    integer pack = pos & 3; //4 bytes per int
//    pos=pos >> 2;
//    integer shifted = value << (pack << 3);
//    integer old_value = llList2Integer(in_list, pos);
//    shifted = old_value | shifted;
//    in_list = llListReplaceList(in_list, (list)shifted, pos, pos);
//    return in_list;
    //Safe optimized version
    integer index = pos >> 2;
    return llListReplaceList(in_list, (list)(llList2Integer(in_list, index) | (value << ((pos & 3) << 3))), index, index);
}

integer unpack(list in_list, integer pos)
{
    return (llList2Integer(in_list, pos >> 2) >> ((pos & 3) << 3)) & 0x000000FF;//unsigned
//    return (llList2Integer(in_list, pos >> 2) << (((~pos) & 3) << 3)) >> 24;//signed
}

change_color(vector color)
{
    integer num_prims=llGetListLength(gXyTextPrims) << 2;

    integer i = 0;

    for (; i<=num_prims; ++i)
    {
        integer link = unpack(gXyTextPrims,i);
        if (!link)
            return;

        llSetLinkPrimitiveParamsFast( link,[
            PRIM_COLOR, FACE_1, color, 1.0,
            PRIM_COLOR, FACE_2, color, 1.0,
            PRIM_COLOR, FACE_3, color, 1.0,
            PRIM_COLOR, FACE_4, color, 1.0,
            PRIM_COLOR, FACE_5, color, 1.0
        ]);
    }
}

change_line_color(integer bank, vector color)
{

    //get the bank offset and length
    integer i = llList2Integer(gBankingData, (bank * BANK_STRIDE));
    integer bank_end = i + llList2Integer(gBankingData, (bank * BANK_STRIDE) + 1);

    for (; i < bank_end; ++i)
    {
        integer link = unpack(gXyTextPrims,i);
        if (!link)
            return;

        llSetLinkPrimitiveParamsFast( link,[
            PRIM_COLOR, FACE_1, color, 1.0,
            PRIM_COLOR, FACE_2, color, 1.0,
            PRIM_COLOR, FACE_3, color, 1.0,
            PRIM_COLOR, FACE_4, color, 1.0,
            PRIM_COLOR, FACE_5, color, 1.0
        ]);
    }
}

init()
{
    integer num_prims=get_number_of_prims();
    string link_name;
    integer bank=0;
    integer prims_pointer=0; //"pointer" to the next entry to be used in the gXyTextPrims list.

    list temp_bank = [];
    integer temp_bank_stride=2;

    //FIXME: font texture might should be per-bank
    llMessageLinked(LINK_THIS, SET_FONT_TEXTURE, "", gFontTexture);

    // moving this before the prim scan so that the slaves properly configure themseves before
    // any requests to display
    llMessageLinked(LINK_THIS, SLAVE_RESET, "" , null_key);

    gXyTextPrims=[];
    integer x=0;
    for (;x<64;++x)
    {
        gXyTextPrims = (gXyTextPrims = []) + gXyTextPrims + 0;  //we need to pad out the list to make it easier to add things in any order later
    }

    gBankingData = [];
    @loop;
    {
        //loop over all prims, looking for ones in the current bank
        for(x=0;x<=num_prims;++x)
        {
            link_name=llGetLinkName(x);
            list tmp = llParseString2List(link_name, (list)"-", []);
            if(llList2String(tmp,0) == "xyzzytext")
            {
                if (llList2Integer(tmp,1) == bank)
                {
                    temp_bank += llList2Integer(tmp,2) + (list)x;
                }
            }

        }

        if (temp_bank != [])
        {
            //sort the current bank
            temp_bank = llListSort(temp_bank, temp_bank_stride, TRUE);

            integer temp_len = llGetListLength(temp_bank);

            //store metadata
            gBankingData += [prims_pointer, temp_len/temp_bank_stride, 0];

            //repack the bank into the prim list
            for (x = 0; x < temp_len; x += temp_bank_stride)
            {
                gXyTextPrims = pack_and_insert(gXyTextPrims, prims_pointer, llList2Integer(temp_bank, x + 1));
                ++prims_pointer;
            }
            ++bank;
            temp_bank=[];
            jump loop;
        }
    }

    //llOwnerSay((string)llGetFreeMemory());
}

default {
   state_entry() {
       // Initialize the character index.
       ResetCharIndex();
       init();
   }

   on_rez(integer num)
   {
      llResetScript();
   }

   link_message(integer sender, integer channel, string data, key id) {
        if (id==null_key)
            id="0";

        if (channel == DISPLAY_STRING) {
            PassToRender(1,data, (integer)((string)id));
        }
        else if (channel == DISPLAY_EXTENDED) {
            PassToRender(2,data, (integer)((string)id));
        }
        else if (channel == REMAP_INDICES) {
            // Parse the message, splitting it up into index values.
            list Parsed = llCSV2List(data);
            integer i = 0;
            // Go through the list and swap each pair of indices.
            for (; i < llGetListLength(Parsed); i += 2) {
                integer Index1 = ConvertIndex( llList2Integer(Parsed, i) );
                integer Index2 = ConvertIndex( llList2Integer(Parsed, i + 1) );

                // Swap these index values.
                string Value1 = llGetSubString(gCharIndex, Index1, Index1);
                string Value2 = llGetSubString(gCharIndex, Index2, Index2);

                gCharIndex = llDeleteSubString(gCharIndex, Index1, Index1);
                gCharIndex = llInsertString(gCharIndex, Index1, Value2);

                gCharIndex = llDeleteSubString(gCharIndex, Index2, Index2);
                gCharIndex = llInsertString(gCharIndex, Index2, Value1);
            }
        }
        else if (channel == RESCAN_LINKSET)
        {
            init();
        }
        else if (channel == RESET_INDICES) {
            // Restore the character index back to default settings.
            ResetCharIndex();
        }
        else if (channel == SET_FADE_OPTIONS) {
            // Change the channel we listen to for cell commands, the
            // starting character position to extract from, and
            // special effect attributes.
            list Parsed = llCSV2List(data);
            gCellUseFading      = (integer) llList2String(Parsed, 0);
            gCellHoldDelay      = (float)   llList2String(Parsed, 1);
        }
        else if (channel == SET_FONT_TEXTURE) {
            // Use the new texture instead of the current one.
            gFontTexture = id;
        }
        else if (channel == SET_COLOR) {
            change_color((vector)data);
        }
        else if (channel == SET_LINE_COLOR) {
            change_line_color((integer)((string)id), (vector)data);
        }
        else if (channel == REGISTER_SLAVE)
        {
            if(!~llListFindList(gSlaveNames, (list)data))
            {//isn't registered yet
                gSlaveNames += data;
                gSlaveRegistered=TRUE;
                //llOwnerSay((string)llGetListLength(gSlaveNames) + " Slave(s) Recognized: " + data);
            }
//            else
//            {//it already exists
//                llOwnerSay((string)llGetListLength(gSlaveNames) + " Slave, Existing Slave Recognized: " + data);
//            }
            llMessageLinked(LINK_THIS, SLAVE_RECOGNIZED, data , null_key);
        }
    }


    changed(integer change)
    {
        if(change&CHANGED_INVENTORY)
        {
            if(gSlaveRegistered)
            {
                //by using negative indexes they don't need to be adjusted when an entry is deleted.
                integer x = ~llGetListLength(gSlaveNames);
                while(++x)
                {
                    if (!~llGetInventoryType(llList2String(gSlaveNames, x)))
                    {
                        //llOwnerSay("Slave Removed: " + llList2String(gSlaveNames, x));
                        gSlaveNames = llDeleteSubList(gSlaveNames, x, x);
                    }
                }
                gSlaveRegistered = !(gSlaveNames == []);
            }
        }
    }
}
```

## Slave Script

```lsl
////////////////////////////////////////////
// XyText v2.0 SLAVE Script (5 Face, Single Texture)
//
// Modified by Thraxis Epsilon and Gigs Taggart 5/2007
// Rewrite to allow one-script-per-object operation
//
// Modified by Kermitt Quirk 19/01/2006
// To add support for 5 face prim instead of 3
//
// Originally Written by Xylor Baysklef
//
//
////////////////////////////////////////////

integer REMAP_INDICES       = 204002;
integer RESET_INDICES       = 204003;

//internal API
integer REGISTER_SLAVE      = 205000;
integer SLAVE_RECOGNIZED    = 205001;
integer SLAVE_DISPLAY       = 205003;
integer SET_FONT_TEXTURE    = 204005;

integer SLAVE_DISPLAY_EXTENDED = 205004;
integer SLAVE_RESET = 205005;

// This is an extended character escape sequence.
string  ESCAPE_SEQUENCE = "\\e";

// This is used to get an index for the extended character.
string  EXTENDED_INDEX  = "12345";

// Face numbers.
integer FACE_1          = 3;
integer FACE_2          = 7;
integer FACE_3          = 4;
integer FACE_4          = 6;
integer FACE_5          = 1;

///////////// GLOBAL VARIABLES ///////////////
// This is the key of the font we are displaying.
key     gFontTexture        = "b2e7394f-5e54-aa12-6e1c-ef327b6bed9e";
// All displayable characters.  Default to ASCII order.
string gCharIndex;

integer gActive; //if we are recognized, this is true
/////////// END GLOBAL VARIABLES ////////////

ResetCharIndex() {
   gCharIndex  = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`";
   gCharIndex += "abcdefghijklmnopqrstuvwxyz{|}~";
   gCharIndex += "\n\n\n\n\n";
}

vector GetGridOffset(integer index) {
   // Calculate the offset needed to display this character.
   integer Row = index / 10;
   integer Col = index % 10;

   // Return the offset in the texture.
   return <-0.45 + 0.1 * Col, 0.45 - 0.1 * Row, 0.0>;
}

ShowChars(integer link,vector grid_offset1, vector grid_offset2, vector grid_offset3, vector grid_offset4, vector grid_offset5) {
   // Set the primitive textures directly.

   // <-0.256, 0, 0>
   // <0, 0, 0>
   // <0.130, 0, 0>
   // <0, 0, 0>
   // <-0.74, 0, 0>

   llSetLinkPrimitiveParamsFast( link,[
        PRIM_TEXTURE, FACE_1, (string)gFontTexture, <0.126, 0.1, 0>, grid_offset1 + <0.037, 0, 0>, 0.0,
        PRIM_TEXTURE, FACE_2, (string)gFontTexture, <0.05, 0.1, 0>, grid_offset2, 0.0,
        PRIM_TEXTURE, FACE_3, (string)gFontTexture, <-0.74, 0.1, 0>, grid_offset3 - <0.244, 0, 0>, 0.0,
        PRIM_TEXTURE, FACE_4, (string)gFontTexture, <0.05, 0.1, 0>, grid_offset4, 0.0,
        PRIM_TEXTURE, FACE_5, (string)gFontTexture, <0.126, 0.1, 0>, grid_offset5 - <0.037, 0, 0>, 0.0
        ]);
}

RenderString(integer link, string str) {
   // Get the grid positions for each pair of characters.
   vector GridOffset1 = GetGridOffset( llSubStringIndex(gCharIndex, llGetSubString(str, 0, 0)) );
   vector GridOffset2 = GetGridOffset( llSubStringIndex(gCharIndex, llGetSubString(str, 1, 1)) );
   vector GridOffset3 = GetGridOffset( llSubStringIndex(gCharIndex, llGetSubString(str, 2, 2)) );
   vector GridOffset4 = GetGridOffset( llSubStringIndex(gCharIndex, llGetSubString(str, 3, 3)) );
   vector GridOffset5 = GetGridOffset( llSubStringIndex(gCharIndex, llGetSubString(str, 4, 4)) );

   // Use these grid positions to display the correct textures/offsets.
   ShowChars(link,GridOffset1, GridOffset2, GridOffset3, GridOffset4, GridOffset5);
}

RenderExtended(integer link, string str) {
   // Look for escape sequences.
   list Parsed       = llParseString2List(str, [], [ESCAPE_SEQUENCE]);
   integer ParsedLen = llGetListLength(Parsed);

   // Create a list of index values to work with.
   list Indices;
   // We start with room for 5 indices.
   integer IndicesLeft = 5;

   integer i = 0;
   string Token;
   integer Clipped;
   integer LastWasEscapeSequence = FALSE;
   // Work from left to right.
   for (; i < ParsedLen && IndicesLeft > 0; ++i) {
       Token = llList2String(Parsed, i);

       // If this is an escape sequence, just set the flag and move on.
       if (Token == ESCAPE_SEQUENCE) {
           LastWasEscapeSequence = TRUE;
       }
       else { // Token != ESCAPE_SEQUENCE
           // Otherwise this is a normal token.  Check its length.
           Clipped = FALSE;
           integer TokenLength = llStringLength(Token);
           // Clip if necessary.
           if (TokenLength > IndicesLeft) {
               Token = llGetSubString(Token, 0, IndicesLeft - 1);
               TokenLength = llStringLength(Token);
               IndicesLeft = 0;
               Clipped = TRUE;
           }
           else
               IndicesLeft -= TokenLength;

           // Was the previous token an escape sequence?
           if (LastWasEscapeSequence) {
               // Yes, the first character is an escape character, the rest are normal.

               // This is the extended character.
               Indices += (llSubStringIndex(EXTENDED_INDEX, llGetSubString(Token, 0, 0)) + 95);

               // These are the normal characters.
               integer j = 1;
               for (; j < TokenLength; ++j)
                   Indices += llSubStringIndex(gCharIndex, llGetSubString(Token, j, j));
           }
           else { // Normal string.
               // Just add the characters normally.
               integer j;
               for (j = 0; j < TokenLength; ++j)
                   Indices += llSubStringIndex(gCharIndex, llGetSubString(Token, j, j));
           }

           // Unset this flag, since this was not an escape sequence.
           LastWasEscapeSequence = FALSE;
       }
   }

   // Use the indices to create grid positions.
   vector GridOffset1 = GetGridOffset( llList2Integer(Indices, 0) );
   vector GridOffset2 = GetGridOffset( llList2Integer(Indices, 1) );
   vector GridOffset3 = GetGridOffset( llList2Integer(Indices, 2) );
   vector GridOffset4 = GetGridOffset( llList2Integer(Indices, 3) );
   vector GridOffset5 = GetGridOffset( llList2Integer(Indices, 4) );

   // Use these grid positions to display the correct textures/offsets.
   ShowChars(link,GridOffset1, GridOffset2, GridOffset3, GridOffset4, GridOffset5);
}

integer ConvertIndex(integer index) {
   // This converts from an ASCII based index to our indexing scheme.
   if (index >= 32) // ' ' or higher
       index -= 32;
   else { // index < 32
       // Quick bounds check.
       if (index > 15)
           index = 15;

       index += 94; // extended characters
   }

   return index;
}

default
{
    state_entry()
    {
        // Initialize the character index.
        ResetCharIndex();
        llMessageLinked(LINK_THIS, REGISTER_SLAVE, llGetScriptName() , NULL_KEY);
    }

    on_rez(integer num)
    {
        llResetScript();
    }

    link_message(integer sender, integer channel, string data, key id)
    {

        if (channel == SLAVE_RECOGNIZED)
        {
            if (data == llGetScriptName())
            {
                gActive=TRUE;
            }
            return;
        }

        if (channel == SLAVE_DISPLAY)
        {
            if (!gActive)
                return;

            list params=llCSV2List((string)id);
            if (llList2String(params, 1) != llGetScriptName())
                return;


            RenderString(llList2Integer(params, 0),data);
            return;
        }

       if (channel == SLAVE_DISPLAY_EXTENDED)
       {
            if (!gActive)
                return;

            list params=llCSV2List((string)id);
            if (llList2String(params, 1) != llGetScriptName())
                return;

            RenderExtended(llList2Integer(params, 0),data);
       }

        if (channel == SET_FONT_TEXTURE)
        {
           gFontTexture = id;
           return;
        }

        if (channel == REMAP_INDICES) {
           // Parse the message, splitting it up into index values.
           list Parsed = llCSV2List(data);
           integer i;
           // Go through the list and swap each pair of indices.
           for (i = 0; i < llGetListLength(Parsed); i += 2) {
               integer Index1 = ConvertIndex( llList2Integer(Parsed, i) );
               integer Index2 = ConvertIndex( llList2Integer(Parsed, i + 1) );

               // Swap these index values.
               string Value1 = llGetSubString(gCharIndex, Index1, Index1);
               string Value2 = llGetSubString(gCharIndex, Index2, Index2);

               gCharIndex = llDeleteSubString(gCharIndex, Index1, Index1);
               gCharIndex = llInsertString(gCharIndex, Index1, Value2);

               gCharIndex = llDeleteSubString(gCharIndex, Index2, Index2);
               gCharIndex = llInsertString(gCharIndex, Index2, Value1);
           }
           return;
        }
        if (channel == RESET_INDICES) {
           // Restore the character index back to default settings.
           ResetCharIndex();
           return;
        }


        if (channel == SLAVE_RESET)
        {
            ResetCharIndex();
            gActive=FALSE;
            llMessageLinked(LINK_THIS, REGISTER_SLAVE, llGetScriptName() , NULL_KEY);
        }

    }


}
```

## Prim Setup

**(Caution! Not compatible with 5 face double texture Xytext)**

```lsl
////////////////////////////////////////////
// XyzzyText Prim Setup Script (5 Face)
//
// Modified by Thraxis Epsilon
//
////////////////////////////////////////////

default
{
    state_entry()
    {

        llSetPrimitiveParams([
                    PRIM_TYPE, PRIM_TYPE_PRISM, PRIM_HOLE_DEFAULT, <0.199, 0.8, 0.0>, 0.68, <0.0, 0.0, 0.0>, <1.0, 1.0, 0.0>, <0.0, 0.0, 0.0>,
                    PRIM_SIZE, <0.03, 2.89, 0.5>,
                    PRIM_TEXTURE, 1, "09b04244-9569-d21f-6de0-4bbcf5552222", <0.126, 0.10, 0.0>, <-0.740013, 0.0, 0.0>, 0.0,
                    PRIM_TEXTURE, 6, "09b04244-9569-d21f-6de0-4bbcf5552222", <0.050, 0.100, 0.00>, <0.0, 0.0, 0.0>, 0.0,
                    PRIM_TEXTURE, 4, "09b04244-9569-d21f-6de0-4bbcf5552222", <-0.740, 0.10, 0.00>, <0.130009, 0.0, 0.0>, 0.0,
                    PRIM_TEXTURE, 7, "09b04244-9569-d21f-6de0-4bbcf5552222", <0.050, 0.100, 0.00>, <0.0, 0.0, 0.0>, 0.0,
                    PRIM_TEXTURE, 3, "09b04244-9569-d21f-6de0-4bbcf5552222", <0.126, 0.10, 0.0>, <-0.255989, 0.0, 0.0>, 0.0]);

        llRemoveInventory(llGetScriptName());
    }
}
```



How to produce textures with alternative fonts for 5 character version (Photoshop VBscript version)

Note: If you need to use XyzzyText for European or UTF-8 other languages, please see the following link: XyzzyText-UTF8
Use the following section for GIMP script-fu if you prefer opensource alternative. Use the following link: ZZText for an alternative international solution (still based on xytext and xyzzytext) using even fewer textures and lag than the xytext solution.

If you need to display with another font, italics or other characters, you can do the following :)

Using Photoshop VB Scripting on windows, just open up Photoshop CS3, and create with notepad the following MakeFonts.vbs:

```lsl
Dim appRef
Set appRef = CreateObject( "Photoshop.Application" )
' Remember current unit settings and then set units to
' the value expected by this script
Dim originalRulerUnits
originalRulerUnits = appRef.Preferences.RulerUnits
appRef.Preferences.RulerUnits = 1 ' psPixels
' Create a new 512*512 pixel document and assign it to a variable.
Dim docRef
Dim artLayerRef
Dim textItemRef
dim rows(10)
rows(1)=" !""#$%&'()"
rows(2)="*+,-./0123"
rows(3)="456789:;<="
rows(4)=">?@ABCDEFG"
rows(5)="HIJKLMNOPQ"
rows(6)="RSTUVWXYZ["
rows(7)="\]^_`abcde"
rows(8)="fghijklmno"
rows(9)="pqrstuvwxy"
rows(10)="z{|}~·ΘΩ√"

dim fontname
fontname="Courier"

Set docRef = appRef.Documents.Add(512, 512, 72, "Table for font " & fontname, 2, 3, 1)
' Create a new art layer containing text
Dim colorObj
Set colorObj=CreateObject("Photoshop.SolidColor")
colorObj.RGB.Red=255
colorObj.RGB.Green=255
colorObj.RGB.Blue=255
' Set the contents of the text layer.
for i=1 to 10
   for j=1 to 10
     Set artLayerRef = docRef.ArtLayers.Add
     artLayerRef.Kind = 2
     Set textItemRef = artLayerRef.TextItem
     ' textItemRef.Font = fontname
     textItemRef.Color=colorObj
     textItemRef.Justification = 2
     textItemRef.Font = "A Charming Font"
     textItemRef.Size = 38
     textItemRef.Contents = mid(rows(i),j,1)
     textItemRef.Position = Array((j-1)*51.2+25,i*51.2-7)
   next
next
' Restore unit settingPhotoshop CS3
appRef.Preferences.RulerUnits = originalRulerUnits
```

Just click on the file in internet explorer and it will start working with your photoshop (I'll take a bit to display all the 100 characters, maybe around 1 sec for character).

This will layout the 100 characters in photoshop on 100 different layers. Then do the following:

- select all the layers with text and go to Text tool and change to whatever font (size etc) you want
- maybe need to add a black layer to see your fonts :) (after you have to hid or delete this)
- merge all the layers in just one
- add an alpha channel for transparency (all black)
- select all in the merged text layer and copy it to alpha channel
- enable the alpha channel and the RGB channel so that you see your font set and the transparent red
- save the font as TGA preserving alpha channel
- upload it to SecondLife 10 L$
- get the UUID from the inventory and specify it instead of the standard template.

How to produce textures with alternative fonts for 5 character version (GIMP script-fu version)

Use the following script for generating characters with GIMP:

To use it you must put under the $HOME/.gimpXXX/scripts directory and name it something.scm.
Then you will find it under gimp <Toolbox>/Xtns/Script-Fu/Text. Clicking on it you are prompted for font to use (use monospaced fonts Andale Mono for instance). (Change only font and fontsize 50 should be ok, others are hard-coded in the script). Adapt with new unicode characters if you need them.

Note: If you need to use XyzzyText for European or UTF-8 other languages, please see the following link: XyzzyText-UTF8
Use the following section for GIMP script-fu if you prefer opensource alternative. Use the following link: ZZText for an alternative international solution (still based on xytext and xyzzytext) using even fewer textures and lag than the xytext solution.



```lsl
(define (script-fu-xytext-simple inText inFont inFontSize inTextColor)
   (let*
       (
       ; define our local variables
       ; create a new image:
       (theImageWidth  512)
       (theImageHeight 512)
       (theImage)
       (theLayer )
       (x 0)
       (y 0)
       (p 32)
       (theText)
       (rows #(
               " !\"#$%&'()"
               "*+,-./0123"
               "456789:;<="
               ">?@ABCDEFG"
               "HIJKLMNOPQ"
               "RSTUVWXYZ["
               "\\]^_`abcde"
               "fghijklmno"
               "pqrstuvwxy"

               ;"z{|}~·thetaOmegaRadix.o "
               (list #\z #\{ #\| #\} #\~ #x387 #x3F4 #x3A9r #x221A #x387 )
              )
       )
       (el 0)
       (ch 0)
       ) ;end of our local variables

  ; builds image
  (set! theImage (car    (gimp-image-new theImageWidth theImageHeight RGB)))
  ; builds layer
  (set! theLayer (car (gimp-layer-new theImage theImageWidth theImageHeight RGB-IMAGE "layer 1" 100 NORMAL) ) )
  ; add layer to image
  (gimp-image-add-layer theImage theLayer 0)

  ; add alpha and set foreground
  (gimp-layer-add-alpha theLayer)
  (gimp-palette-set-foreground inTextColor)

  ; clear all the image and remove selection
  (gimp-selection-all theImage)
  (gimp-edit-clear theLayer)
  (gimp-selection-none theImage)

  ; do actual plot of characters
  (while (< x 10)
    (while (< y 10)
      (set! el (vector-ref rows x))
      (set! ch (if (string? el) (substring el y (+ y 1)) (list-ref el (+ y 1))))
      (if (integer? ch) (set! ch (integer->char ch)))
      (if (char? ch)(set! ch (string ch)))
      (set! p ch)
      (set! theText (car (gimp-text-fontname theImage theLayer
          (+ (* y 51.2) 12) (- (* x 51.2) 7)
          p    0    TRUE
          inFontSize PIXELS
          inFont)))

        ; go on next char
        ;(set! p (+ p 1))
        (set! y (+ y 1))
      )

    (set! y 0)
    (set! x (+ x 1))
  )

  ; apply the layers (apply transparence
  (gimp-image-merge-visible-layers theImage 0)

  (gimp-display-new theImage)
  )
)

(script-fu-register
  "script-fu-xytext-simple"           ;func name
  "XYText-simple"                     ;menu label
  "Generate font for xytext-simple"   ;description
  "Salahzar Stenvaag"                 ;author
  "copyright 2008, Salahzar Stenvaag" ;copyright notice
  "October 27, 1997"                  ;date created
  ""                                  ;image type that the script works on
  SF-STRING      "Text:"         "Text Box"           ;a string variable
  SF-FONT        "Font:"         "Andale Mono"        ;a fixed font variable
  SF-ADJUSTMENT  "Font size"     '(50 1 1000 1 10 0 1);a spin-button
  SF-COLOR       "Color:"        '(255 255 255)       ;color variable
)

(script-fu-menu-register "script-fu-xytext-simple" "/Xtns/Text")
```

XyzzyText - 10 Character

## Master Script

```lsl
////////////////////////////////////////////
// XyzzyText v2.1(10-Char) by Thraxis Epsilon
// XyzzyText v2.1 Script (Set Line Color) by Huney Jewell
// XyzzyText v2.0 Script (5 Face, Single Texture)
//
// Edited trivially by Joel Cloquet on 1/2011 to use the (relatively)
// new llSetLinkPrimitiveParamsFast function, thereby removing the need in
// some cases to use the slave script.
//
// Heavily Modified by Thraxis Epsilon, Gigs Taggart 5/2007 and Strife Onizuka 8/2007
// Rewrite to allow one-script-per-object operation w/ optional slaves
// Enable prim-label functionality
// Enabled Banking
// Enabled 10-char per prim
//
// Modified by Kermitt Quirk 19/01/2006
// To add support for 5 face prim instead of 3
//
// Core XyText Originally Written by Xylor Baysklef
//
//
////////////////////////////////////////////

/////////////// CONSTANTS ///////////////////
// XyText Message Map.
integer DISPLAY_STRING      = 204000;
integer DISPLAY_EXTENDED    = 204001;
integer REMAP_INDICES       = 204002;
integer RESET_INDICES       = 204003;
integer SET_FADE_OPTIONS    = 204004;
integer SET_FONT_TEXTURE    = 204005;
integer SET_LINE_COLOR      = 204006;
integer SET_COLOR           = 204007;
integer RESCAN_LINKSET      = 204008;

//internal API
integer REGISTER_SLAVE      = 205000;
integer SLAVE_RECOGNIZED    = 205001;
integer SLAVE_DISPLAY       = 205003;
integer SLAVE_DISPLAY_EXTENDED = 205004;
integer SLAVE_RESET         = 205005;

// This is an extended character escape sequence.
string  ESCAPE_SEQUENCE = "\\e";

// This is used to get an index for the extended character.
string  EXTENDED_INDEX  = "123456789abcdef";

// Face numbers.
integer FACE_1          = 3;
integer FACE_2          = 7;
integer FACE_3          = 4;
integer FACE_4          = 6;
integer FACE_5          = 1;

// Used to hide the text after a fade-out.
key     TRANSPARENT     = "701917a8-d614-471f-13dd-5f4644e36e3c";
key     null_key        = NULL_KEY;

// This is a list of textures for all 2-character combinations.
list    CHARACTER_GRID  = [
        "00e9f9f7-0669-181c-c192-7f8e67678c8d",
        "347a5cb6-0031-7ec0-2fcf-f298eebf3c0e",
        "4e7e689e-37f1-9eca-8596-a958bbd23963",
        "19ea9c21-67ba-8f6f-99db-573b1b877eb1",
        "dde7b412-cda1-652f-6fc2-73f4641f96e1",
        "af6fa3bb-3a6c-9c4f-4bf5-d1c126c830da",
        "a201d3a2-364b-43b6-8686-5881c0f82a94",
        "b674dec8-fead-99e5-c28d-2db8e4c51540",
        "366e05f3-be6b-e5cf-c33b-731dff649caa",
        "75c4925c-0427-dc0c-c71c-e28674ff4d27",
        "dcbe166b-6a97-efb2-fc8e-e5bc6a8b1be6",
        "0dca2feb-fc66-a762-db85-89026a4ecd68",
        "a0fca76f-503a-946b-9336-0a918e886f7a",
        "67fb375d-89a1-5a4f-8c7a-0cd1c066ffc4",
        "300470b2-da34-5470-074c-1b8464ca050c",
        "d1f8e91c-ce2b-d85e-2120-930d3b630946",
        "2a190e44-7b29-dadb-0bff-c31adaf5a170",
        "75d55e71-f6f8-9835-e746-a45f189f30a1",
        "300fac33-2b30-3da3-26bc-e2d70428ec19",
        "0747c776-011a-53ce-13ee-8b5bb9e87c1e",
        "85a855c3-a94f-01ca-33e0-7dde92e727e2",
        "cbc1dab2-2d61-2986-1949-7a5235c954e1",
        "f7aef047-f266-9596-16df-641010edd8e1",
        "4c34ebf7-e5e1-2e1a-579f-e224d9d5e71b",
        "4a69e98c-26a5-ad05-e92e-b5b906ad9ef9",
        "462a9226-2a97-91ac-2d89-57ab33334b78",
        "20b24b3a-8c57-82ee-c6ed-555003f5dbcd",
        "9b481daa-9ea8-a9fa-1ee4-ab9a0d38e217",
        "c231dbdc-c842-15b0-7aa6-6da14745cfdc",
        "c97e3cbb-c9a3-45df-a0ae-955c1f4bf9cf",
        "f1e7d030-ff80-a242-cb69-f6951d4eae3b",
        "ed32d6c4-d733-c0f1-f242-6df1d222220d",
        "88f96a30-dccf-9b20-31ef-da0dfeb23c72",
        "252f2595-58b8-4bcc-6515-fa274d0cfb65",
        "f2838c4f-de80-cced-dff8-195dfdf36b2c",
        "cc2594fe-add2-a3df-cdb3-a61711badf53",
        "e0ce2972-da00-955c-129e-3289b3676776",
        "3e0d336d-321f-ddfa-5c1b-e26131766f6a",
        "d43b1dc4-6b51-76a7-8b90-38865b82bf06",
        "06d16cbb-1868-fd1d-5c93-eae42164a37d",
        "dd5d98cf-273e-3fd0-f030-48be58ee3a0b",
        "0e47c89e-de4a-6233-a2da-cb852aad1b00",
        "fb9c4a55-0e13-495b-25c4-f0b459dc06de",
        "e3ce8def-312c-735b-0e48-018b6799c883",
        "2f713216-4e71-d123-03ed-9c8554710c6b",
        "4a417d8a-1f4f-404b-9783-6672f8527911",
        "ca5e21ec-5b20-5909-4c31-3f90d7316b33",
        "06a4fcc3-e1c4-296d-8817-01f88fbd7367",
        "130ac084-6f3c-95de-b5b6-d25c80703474",
        "59d540a0-ae9d-3606-5ae0-4f2842b64cfa",
        "8612ae9a-f53c-5bf4-2899-8174d7abc4fd",
        "12467401-e979-2c49-34e0-6ac761542797",
        "d53c3eaa-0404-3860-0675-3e375596c3e3",
        "9f5b26bd-81d3-b25e-62fe-5b671d1e3e79",
        "f57f0b64-a050-d617-ee00-c8e9e3adc9cb",
        "beff166a-f5f3-f05e-e020-98f2b00e27ed",
        "02278a65-94ba-6d5e-0d2b-93f2e4f4bf70",
        "a707197d-449e-5b58-846c-0c850c61f9d6",
        "021d4b1a-9503-a44f-ee2b-976eb5d80e68",
        "0ae2ffae-7265-524d-cb76-c2b691992706"];
list    CHARACTER_GRID2  = [
        "f6e41cf2-1104-bd0b-0190-dffad1bac813",
        "2b4bb15e-956d-56ae-69f5-d26a20de0ce7",
        "f816da2c-51f1-612a-2029-a542db7db882",
        "345fea05-c7be-465c-409f-9dcb3bd2aa07",
        "b3017e02-c063-5185-acd5-1ef5f9d79b89",
        "4dcff365-1971-3c2b-d73c-77e1dc54242a"
          ];

///////////// END CONSTANTS ////////////////

///////////// GLOBAL VARIABLES ///////////////
// All displayable characters.  Default to ASCII order.
string gCharIndex;
// This is the channel to listen on while acting
// as a cell in a larger display.
integer gCellChannel      = -1;
// This is the starting character position in the cell channel message
// to render.
integer gCellCharPosition = 0;
// This is whether or not to use the fade in/out special effect.
integer gCellUseFading      = FALSE;
// This is how long to display the text before fading out (if using
// fading special effect).
// Note: < 0  means don't fade out.
float   gCellHoldDelay      = 1.0;

integer gSlaveRegistered;
list gSlaveNames;

integer BANK_STRIDE=3; //offset, length, highest_dirty
list gBankingData;

/////////// END GLOBAL VARIABLES ////////////

ResetCharIndex() {
    gCharIndex  = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`";
    // \" <-- Fixes LSL syntax highlighting bug.
    gCharIndex += "abcdefghijklmnopqrstuvwxyz{|}~";
    gCharIndex += "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n";
}

vector GetGridPos(integer index1, integer index2) {
    // There are two ways to use the lookup table...
    integer Col;
    integer Row;
    if (index1 >= index2) {
        // In this case, the row is the index of the first character:
        Row = index1;
        // And the col is the index of the second character (x2)
        Col = index2 * 2;
    }
    else { // Index1 < Index2
        // In this case, the row is the index of the second character:
        Row = index2;
        // And the col is the index of the first character, x2, offset by 1.
        Col = index1 * 2 + 1;
    }
    return ;
}

string GetGridTexture(vector grid_pos) {
    // Calculate the texture in the grid to use.
    integer GridCol = llRound(grid_pos.x) / 20;
    integer GridRow = llRound(grid_pos.y) / 10;

    // Lookup the texture.
    key Texture = llList2Key(CHARACTER_GRID, GridRow * (GridRow + 1) / 2 + GridCol);
    return Texture;
}

vector GetGridOffset(vector grid_pos) {
    // Zoom in on the texture showing our character pair.
    integer Col = llRound(grid_pos.x) % 20;
    integer Row = llRound(grid_pos.y) % 10;

    // Return the offset in the texture.
    return <-0.45 + 0.05 * Col, 0.45 - 0.1 * Row, 0.0>;
}

ShowChars(integer link,vector grid_pos1, vector grid_pos2, vector grid_pos3, vector grid_pos4, vector grid_pos5) {
   // Set the primitive textures directly.


   llSetLinkPrimitiveParamsFast( link , [
        PRIM_TEXTURE, FACE_1, GetGridTexture(grid_pos1), <0.25, 0.1, 0>, GetGridOffset(grid_pos1) + <0.075, 0, 0>, 0.0,
        PRIM_TEXTURE, FACE_2, GetGridTexture(grid_pos2), <0.1, 0.1, 0>, GetGridOffset(grid_pos2), 0.0,
        PRIM_TEXTURE, FACE_3, GetGridTexture(grid_pos3), <-1.48, 0.1, 0>, GetGridOffset(grid_pos3)+ <0.37, 0, 0>, 0.0,
        PRIM_TEXTURE, FACE_4, GetGridTexture(grid_pos4), <0.1, 0.1, 0>, GetGridOffset(grid_pos4), 0.0,
        PRIM_TEXTURE, FACE_5, GetGridTexture(grid_pos5), <0.25, 0.1, 0>, GetGridOffset(grid_pos5) - <0.075, 0, 0>, 0.0
        ]);
}

RenderString(integer link, string str) {
    // Get the grid positions for each pair of characters.
    vector GridPos1 = GetGridPos( llSubStringIndex(gCharIndex, llGetSubString(str, 0, 0)),
                                  llSubStringIndex(gCharIndex, llGetSubString(str, 1, 1)) );
    vector GridPos2 = GetGridPos( llSubStringIndex(gCharIndex, llGetSubString(str, 2, 2)),
                                  llSubStringIndex(gCharIndex, llGetSubString(str, 3, 3)) );
    vector GridPos3 = GetGridPos( llSubStringIndex(gCharIndex, llGetSubString(str, 4, 4)),
                                  llSubStringIndex(gCharIndex, llGetSubString(str, 5, 5)) );
    vector GridPos4 = GetGridPos( llSubStringIndex(gCharIndex, llGetSubString(str, 6, 6)),
                                  llSubStringIndex(gCharIndex, llGetSubString(str, 7, 7)) );
    vector GridPos5 = GetGridPos( llSubStringIndex(gCharIndex, llGetSubString(str, 8, 8)),
                                  llSubStringIndex(gCharIndex, llGetSubString(str, 9, 9)) );

    // Use these grid positions to display the correct textures/offsets.
    ShowChars(link,GridPos1, GridPos2, GridPos3, GridPos4, GridPos5);
}

//RenderWithEffects(integer link, string str) {
//    // Get the grid positions for each pair of characters.
//    vector GridPos1 = GetGridPos( llSubStringIndex(gCharIndex, llGetSubString(str, 0, 0)),
//                                  llSubStringIndex(gCharIndex, llGetSubString(str, 1, 1)) );
//    vector GridPos2 = GetGridPos( llSubStringIndex(gCharIndex, llGetSubString(str, 2, 2)),
//                                  llSubStringIndex(gCharIndex, llGetSubString(str, 3, 3)) );
//    vector GridPos3 = GetGridPos( llSubStringIndex(gCharIndex, llGetSubString(str, 4, 4)),
//                                  llSubStringIndex(gCharIndex, llGetSubString(str, 5, 5)) );
//    vector GridPos4 = GetGridPos( llSubStringIndex(gCharIndex, llGetSubString(str, 6, 6)),
//                                  llSubStringIndex(gCharIndex, llGetSubString(str, 7, 7)) );
//    vector GridPos5 = GetGridPos( llSubStringIndex(gCharIndex, llGetSubString(str, 8, 8)),
//                                  llSubStringIndex(gCharIndex, llGetSubString(str, 9, 9)) );                          //
//
//      // First set the alpha to the lowest possible.
//   llSetAlpha(0.05, ALL_SIDES);
//
//    // Use these grid positions to display the correct textures/offsets.
//    ShowChars(link,GridPos1, GridPos2, GridPos3, GridPos4, GridPos5);
//
//    float Alpha = 0.10;
//    for (; Alpha <= 1.0; Alpha += 0.05)
//       llSetAlpha(Alpha, ALL_SIDES);
//          // See if we want to fade out as well.
//   if (gCellHoldDelay < 0.0)
//       // No, bail out. (Just keep showing the string at full strength).
//       return;
//          // Hold the text for a while.
//   llSleep(gCellHoldDelay);
//      // Now fade out.
//   for (Alpha = 0.95; Alpha >= 0.05; Alpha -= 0.05)
//       llSetAlpha(Alpha, ALL_SIDES);
//          // Make the text transparent to fully hide it.
//   llSetTexture(TRANSPARENT, ALL_SIDES);
//}

integer RenderExtended(integer link, string str,integer render) {
    // Look for escape sequences.
    integer length = 0;
    list Parsed       = llParseString2List(str, [], (list)ESCAPE_SEQUENCE);
    integer ParsedLen = llGetListLength(Parsed);

    // Create a list of index values to work with.
    list Indices;
    // We start with room for 6 indices.
    integer IndicesLeft = 10;

    string Token;
    integer Clipped;
    integer LastWasEscapeSequence = FALSE;
    // Work from left to right.
    integer i=0;
    for (; i < ParsedLen && IndicesLeft > 0; ++i) {
        Token = llList2String(Parsed, i);

        // If this is an escape sequence, just set the flag and move on.
        if (Token == ESCAPE_SEQUENCE) {
            LastWasEscapeSequence = TRUE;
        }
        else { // Token != ESCAPE_SEQUENCE
            // Otherwise this is a normal token.  Check its length.
            Clipped = FALSE;
            integer TokenLength = llStringLength(Token);
            // Clip if necessary.
            if (TokenLength > IndicesLeft) {
                TokenLength = llStringLength(Token = llGetSubString(Token, 0, IndicesLeft - 1));
                IndicesLeft = 0;
                Clipped = TRUE;
            }
            else
                IndicesLeft -= TokenLength;

            // Was the previous token an escape sequence?
            if (LastWasEscapeSequence) {
                // Yes, the first character is an escape character, the rest are normal.
                length += 2 + TokenLength;
                if (render)
                {
                    // This is the extended character.
                    Indices += [llSubStringIndex(EXTENDED_INDEX, llGetSubString(Token, 0, 0)) + 95];

                    // These are the normal characters.
                    integer j=1;
                    for (; j < TokenLength; ++j)
                    {
                        Indices += [llSubStringIndex(gCharIndex, llGetSubString(Token, j, j))];
                    }
                }
            }
            else { // Normal string.
                // Just add the characters normally.
                length += TokenLength;
                if(render)
                {
                    integer j=0;
                    for (; j < TokenLength; ++j)
                    {
                        Indices += [llSubStringIndex(gCharIndex, llGetSubString(Token, j, j))];
                    }
                }
            }

            // Unset this flag, since this was not an escape sequence.
            LastWasEscapeSequence = FALSE;
        }
    }

    if(render)
    {
        // Use the indices to create grid positions.
        vector GridPos1 = GetGridPos( llList2Integer(Indices, 0), llList2Integer(Indices, 1) );
        vector GridPos2 = GetGridPos( llList2Integer(Indices, 2), llList2Integer(Indices, 3) );
        vector GridPos3 = GetGridPos( llList2Integer(Indices, 4), llList2Integer(Indices, 5) );
        vector GridPos4 = GetGridPos( llList2Integer(Indices, 6), llList2Integer(Indices, 7) );
        vector GridPos5 = GetGridPos( llList2Integer(Indices, 8), llList2Integer(Indices, 9) );

        // Use these grid positions to display the correct textures/offsets.
        ShowChars(link,GridPos1, GridPos2, GridPos3, GridPos4, GridPos5);
    }
    return length;
}

integer ConvertIndex(integer index) {
    // This converts from an ASCII based index to our indexing scheme.
    if (index >= 32) // ' ' or higher
        index -= 32;
    else { // index < 32
        // Quick bounds check.
        if (index > 15)
            index = 15;

        index += 94; // extended characters
    }

    return index;
}

PassToRender(integer render,string message, integer bank)
{
    float time;
    integer extendedlen = 0;
    integer link;

    integer i = 0;
    integer msgLen = llStringLength(message);
    string TextToRender;
    integer num_slaves=llGetListLength(gSlaveNames);
    string slave_name; //avoids unnecessary casts, keeping it as a string


    //get the bank offset and length
    integer bank_offset=llList2Integer(gBankingData, (bank * BANK_STRIDE));
    integer bank_length=llList2Integer(gBankingData, (bank * BANK_STRIDE) + 1);
    integer bank_highest_dirty=llList2Integer(gBankingData, (bank * BANK_STRIDE) + 2);

    integer x=0;
    for (;x < msgLen;x = x + 10)
    {

        if (i >= bank_length)  //we don't want to run off the end of the bank
        {
            //set the dirty to max, and bail out, we're done
            gBankingData=llListReplaceList(gBankingData, [bank_length], (bank * BANK_STRIDE) + 2, (bank * BANK_STRIDE) + 2);
            return;
        }

        link = unpack(gXyTextPrims,(i + bank_offset));
        TextToRender = llGetSubString(message, x, x + 20);

        if(gSlaveRegistered && (link % (num_slaves +1)))
        {
            slave_name=llList2String(gSlaveNames, (link % (num_slaves + 1)) - 1);
            if (render == 1)
                llMessageLinked(LINK_THIS, SLAVE_DISPLAY, TextToRender, (key)((string)link + "," + slave_name));
            if (render == 2)
            {
                if(llSubStringIndex(TextToRender,"\e")>x+10)
                {
                    extendedlen = 10;
                }
                else
                {
                    extendedlen = RenderExtended(link,TextToRender,0);
                }

                if(extendedlen>10)
                {
                    x += extendedlen-10;
                }

                llMessageLinked(LINK_THIS,SLAVE_DISPLAY_EXTENDED,TextToRender,(key)((string)link+","+slave_name));
            }
        }
        else
        {
            if (render == 1)
                RenderString(link,TextToRender);
            if (render == 2)
            {
                extendedlen = RenderExtended(link,TextToRender,1);
                if(extendedlen>10)
                {
                    x += extendedlen-10;
                }
            }

//            if (render == 3)
//                RenderWithEffects(link,TextToRender);
        }
        ++i;
    }

    if (bank_highest_dirty==0)
        bank_highest_dirty=bank_length;

    integer current_highest_dirty=i;
    while (i < bank_highest_dirty)
    {
        link = unpack(gXyTextPrims,(i + bank_offset));

        if(gSlaveRegistered && (link % (num_slaves+1) != 0))
        {
            slave_name=llList2String(gSlaveNames, (link % (num_slaves + 1)) - 1);
            llMessageLinked(LINK_THIS, SLAVE_DISPLAY, "     ", (key)((string)link + "," + slave_name));
            //sorry, no fade effect with slave
        }
        else
        {
            RenderString(link,"          ");
        }
        ++i;
    }
    gBankingData=llListReplaceList(gBankingData, [current_highest_dirty], (bank * BANK_STRIDE) + 2, (bank * BANK_STRIDE) + 2);
}

// Bitwise Voodoo by Gigs Taggart and optimized by Strife Onizuka
list gXyTextPrims;

integer get_number_of_prims()
{//ignores avatars.
    integer a = llGetNumberOfPrims();
    while(llGetAgentSize(llGetLinkKey(a)))
        --a;
    return a;
}

//functions to pack 8-bit shorts into ints
list pack_and_insert(list in_list, integer pos, integer value)
{
//    //figure out the bitpack position
//    integer pack = pos & 3; //4 bytes per int
//    pos=pos >> 2;
//    integer shifted = value << (pack << 3);
//    integer old_value = llList2Integer(in_list, pos);
//    shifted = old_value | shifted;
//    in_list = llListReplaceList(in_list, (list)shifted, pos, pos);
//    return in_list;
    //Safe optimized version
    integer index = pos >> 2;
    return llListReplaceList(in_list, (list)(llList2Integer(in_list, index) | (value << ((pos & 3) << 3))), index, index);
}

integer unpack(list in_list, integer pos)
{
    return (llList2Integer(in_list, pos >> 2) >> ((pos & 3) << 3)) & 0x000000FF;//unsigned
//    return (llList2Integer(in_list, pos >> 2) << (((~pos) & 3) << 3)) >> 24;//signed
}

change_color(vector color)
{
    integer num_prims=llGetListLength(gXyTextPrims) << 2;

    integer i = 0;

    for (; i<=num_prims; ++i)
    {
        integer link = unpack(gXyTextPrims,i);
        if (!link)
            return;

        llSetLinkPrimitiveParamsFast( link,[
            PRIM_COLOR, FACE_1, color, 1.0,
            PRIM_COLOR, FACE_2, color, 1.0,
            PRIM_COLOR, FACE_3, color, 1.0,
            PRIM_COLOR, FACE_4, color, 1.0,
            PRIM_COLOR, FACE_5, color, 1.0
        ]);
    }
}

change_line_color(integer bank, vector color)
{

    //get the bank offset and length
    integer i = llList2Integer(gBankingData, (bank * BANK_STRIDE));
    integer bank_end = i + llList2Integer(gBankingData, (bank * BANK_STRIDE) + 1);

    for (; i < bank_end; ++i)
    {
        integer link = unpack(gXyTextPrims,i);
        if (!link)
            return;

        llSetLinkPrimitiveParamsFast( link,[
            PRIM_COLOR, FACE_1, color, 1.0,
            PRIM_COLOR, FACE_2, color, 1.0,
            PRIM_COLOR, FACE_3, color, 1.0,
            PRIM_COLOR, FACE_4, color, 1.0,
            PRIM_COLOR, FACE_5, color, 1.0
        ]);
    }
}

init()
{
    integer num_prims=get_number_of_prims();

    string link_name;
    integer bank=0;
    integer bank_empty=FALSE;
    integer prims_pointer=0; //"pointer" to the next entry to be used in the gXyTextPrims list.

    list temp_bank=[];
    integer temp_bank_stride=2;

    // moving this before the prim scan so that the slaves properly configure themseves before
    // any requests to display
    llMessageLinked(LINK_THIS, SLAVE_RESET, "" , null_key);

    gXyTextPrims=[];
    integer x=0;
    for (;x<64;++x)
    {
        gXyTextPrims= (gXyTextPrims = []) + gXyTextPrims + [0];  //we need to pad out the list to make it easier to add things in any order later
    }

    gBankingData = [];
    @loop;
    {
        //loop over all prims, looking for ones in the current bank
        for(x=0;x<=num_prims;++x)
        {
            link_name=llGetLinkName(x);
            list tmp = llParseString2List(link_name, ["-"], []);
            if(llList2String(tmp,0)== "xyzzytext")
            {
                integer prims_bank=llList2Integer(tmp,1);
                if (llList2Integer(tmp,1)==bank)
                {
                    temp_bank+=llList2Integer(tmp,2) + (list)x;
                }
            }

        }


        if (temp_bank!=[])
        {
            //sort the current bank
            temp_bank=llListSort(temp_bank, temp_bank_stride, TRUE);

            integer temp_len=llGetListLength(temp_bank);

            //store metadata
            gBankingData+=[prims_pointer,temp_len/temp_bank_stride,0];

            //repack the bank into the prim list
            for (x=0; x < temp_len; x+=temp_bank_stride)
            {
                gXyTextPrims = pack_and_insert(gXyTextPrims, prims_pointer, llList2Integer(temp_bank, x+1));
                ++prims_pointer;
            }
            ++bank;
            temp_bank=[];
            jump loop;
        }
    }
}

default {
    state_entry() {
        // Initialize the character index.
        ResetCharIndex();
        init();
    }

   on_rez(integer num)
   {
      llResetScript();
   }

    link_message(integer sender, integer channel, string data, key id) {
        if(id == null_key)
            id="0";

        if (channel == DISPLAY_STRING) {
            PassToRender(1,data, (integer)((string)id));
            return;
        }
        else if (channel == DISPLAY_EXTENDED) {
             PassToRender(2,data, (integer)((string)id));
            return;
        }
        else if (channel == REMAP_INDICES) {
            // Parse the message, splitting it up into index values.
            list Parsed = llCSV2List(data);
            integer i;
            // Go through the list and swap each pair of indices.
            for (i = 0; i < llGetListLength(Parsed); i += 2) {
                integer Index1 = ConvertIndex( llList2Integer(Parsed, i) );
                integer Index2 = ConvertIndex( llList2Integer(Parsed, i + 1) );

                // Swap these index values.
                string Value1 = llGetSubString(gCharIndex, Index1, Index1);
                string Value2 = llGetSubString(gCharIndex, Index2, Index2);

                gCharIndex = llDeleteSubString(gCharIndex, Index1, Index1);
                gCharIndex = llInsertString(gCharIndex, Index1, Value2);

                gCharIndex = llDeleteSubString(gCharIndex, Index2, Index2);
                gCharIndex = llInsertString(gCharIndex, Index2, Value1);
            }
            return;
        }
        else if (channel == RESET_INDICES) {
            // Restore the character index back to default settings.
            ResetCharIndex();
            return;
        }
        else if (channel == RESCAN_LINKSET)
        {
            init();
        }
        else if (channel == SET_COLOR) {
            change_color((vector)data);
        }
        else if (channel == SET_LINE_COLOR) {
            change_line_color((integer)((string)id), (vector)data);
        }
        else if (channel == REGISTER_SLAVE)
        {
            if(!~llListFindList(gSlaveNames, (list)data))
            {//isn't registered yet
                gSlaveNames += data;
                gSlaveRegistered=TRUE;
                //llOwnerSay((string)llGetListLength(gSlaveNames) + " Slave(s) Recognized: " + data);
            }
//            else
//            {//it already exists
//                llOwnerSay((string)llGetListLength(gSlaveNames) + " Slave, Existing Slave Recognized: " + data);
//            }
            llMessageLinked(LINK_THIS, SLAVE_RECOGNIZED, data , null_key);
        }
    }

    changed(integer change)
    {
        if(change&CHANGED_INVENTORY)
        {
            if(gSlaveRegistered)
            {
                //by using negative indexes they don't need to be adjusted when an entry is deleted.
                integer x = ~llGetListLength(gSlaveNames);
                while(++x)
                {
                    if (!~llGetInventoryType(llList2String(gSlaveNames, x)))
                    {
                        //llOwnerSay("Slave Removed: " + llList2String(gSlaveNames, x));
                        gSlaveNames = llDeleteSubList(gSlaveNames, x, x);
                    }
                }
                gSlaveRegistered = !(gSlaveNames == []);
            }
        }
    }
}
```

## Slave Script

```lsl
////////////////////////////////////////////
// XyzzyText v2.1(10-Char) by Thraxis Epsilon
// XyText v2.0 SLAVE Script (5 Face, Single Texture)
//
// Heavily Modified by Thraxis Epsilon, Gigs Taggart 5/2007 and Strife Onizuka 8/2007
// Rewrite to allow one-script-per-object operation w/ optional slaves
// Enable prim-label functionality
// Enabled Banking
// Enabled 10-char per prim
//
// Modified by Kermitt Quirk 19/01/2006
// To add support for 5 face prim instead of 3
//
// Originally Written by Xylor Baysklef
//
//
////////////////////////////////////////////

integer REMAP_INDICES       = 204002;
integer RESET_INDICES       = 204003;

//internal API
integer REGISTER_SLAVE      = 205000;
integer SLAVE_RECOGNIZED    = 205001;
integer SLAVE_DISPLAY       = 205003;
integer SET_FONT_TEXTURE    = 204005;

integer SLAVE_DISPLAY_EXTENDED = 205004;
integer SLAVE_RESET = 205005;

// This is an extended character escape sequence.
string  ESCAPE_SEQUENCE = "\\e";

// This is used to get an index for the extended character.
string  EXTENDED_INDEX  = "123456789abcdef";

// Face numbers.
integer FACE_1          = 3;
integer FACE_2          = 7;
integer FACE_3          = 4;
integer FACE_4          = 6;
integer FACE_5          = 1;

// This is a list of textures for all 2-character combinations.
list    CHARACTER_GRID  = [
        "00e9f9f7-0669-181c-c192-7f8e67678c8d",
        "347a5cb6-0031-7ec0-2fcf-f298eebf3c0e",
        "4e7e689e-37f1-9eca-8596-a958bbd23963",
        "19ea9c21-67ba-8f6f-99db-573b1b877eb1",
        "dde7b412-cda1-652f-6fc2-73f4641f96e1",
        "af6fa3bb-3a6c-9c4f-4bf5-d1c126c830da",
        "a201d3a2-364b-43b6-8686-5881c0f82a94",
        "b674dec8-fead-99e5-c28d-2db8e4c51540",
        "366e05f3-be6b-e5cf-c33b-731dff649caa",
        "75c4925c-0427-dc0c-c71c-e28674ff4d27",
        "dcbe166b-6a97-efb2-fc8e-e5bc6a8b1be6",
        "0dca2feb-fc66-a762-db85-89026a4ecd68",
        "a0fca76f-503a-946b-9336-0a918e886f7a",
        "67fb375d-89a1-5a4f-8c7a-0cd1c066ffc4",
        "300470b2-da34-5470-074c-1b8464ca050c",
        "d1f8e91c-ce2b-d85e-2120-930d3b630946",
        "2a190e44-7b29-dadb-0bff-c31adaf5a170",
        "75d55e71-f6f8-9835-e746-a45f189f30a1",
        "300fac33-2b30-3da3-26bc-e2d70428ec19",
        "0747c776-011a-53ce-13ee-8b5bb9e87c1e",
        "85a855c3-a94f-01ca-33e0-7dde92e727e2",
        "cbc1dab2-2d61-2986-1949-7a5235c954e1",
        "f7aef047-f266-9596-16df-641010edd8e1",
        "4c34ebf7-e5e1-2e1a-579f-e224d9d5e71b",
        "4a69e98c-26a5-ad05-e92e-b5b906ad9ef9",
        "462a9226-2a97-91ac-2d89-57ab33334b78",
        "20b24b3a-8c57-82ee-c6ed-555003f5dbcd",
        "9b481daa-9ea8-a9fa-1ee4-ab9a0d38e217",
        "c231dbdc-c842-15b0-7aa6-6da14745cfdc",
        "c97e3cbb-c9a3-45df-a0ae-955c1f4bf9cf",
        "f1e7d030-ff80-a242-cb69-f6951d4eae3b",
        "ed32d6c4-d733-c0f1-f242-6df1d222220d",
        "88f96a30-dccf-9b20-31ef-da0dfeb23c72",
        "252f2595-58b8-4bcc-6515-fa274d0cfb65",
        "f2838c4f-de80-cced-dff8-195dfdf36b2c",
        "cc2594fe-add2-a3df-cdb3-a61711badf53",
        "e0ce2972-da00-955c-129e-3289b3676776",
        "3e0d336d-321f-ddfa-5c1b-e26131766f6a",
        "d43b1dc4-6b51-76a7-8b90-38865b82bf06",
        "06d16cbb-1868-fd1d-5c93-eae42164a37d",
        "dd5d98cf-273e-3fd0-f030-48be58ee3a0b",
        "0e47c89e-de4a-6233-a2da-cb852aad1b00",
        "fb9c4a55-0e13-495b-25c4-f0b459dc06de",
        "e3ce8def-312c-735b-0e48-018b6799c883",
        "2f713216-4e71-d123-03ed-9c8554710c6b",
        "4a417d8a-1f4f-404b-9783-6672f8527911",
        "ca5e21ec-5b20-5909-4c31-3f90d7316b33",
        "06a4fcc3-e1c4-296d-8817-01f88fbd7367",
        "130ac084-6f3c-95de-b5b6-d25c80703474",
        "59d540a0-ae9d-3606-5ae0-4f2842b64cfa",
        "8612ae9a-f53c-5bf4-2899-8174d7abc4fd",
        "12467401-e979-2c49-34e0-6ac761542797",
        "d53c3eaa-0404-3860-0675-3e375596c3e3",
        "9f5b26bd-81d3-b25e-62fe-5b671d1e3e79",
        "f57f0b64-a050-d617-ee00-c8e9e3adc9cb",
        "beff166a-f5f3-f05e-e020-98f2b00e27ed",
        "02278a65-94ba-6d5e-0d2b-93f2e4f4bf70",
        "a707197d-449e-5b58-846c-0c850c61f9d6",
        "021d4b1a-9503-a44f-ee2b-976eb5d80e68",
        "0ae2ffae-7265-524d-cb76-c2b691992706",
        "f6e41cf2-1104-bd0b-0190-dffad1bac813",
        "2b4bb15e-956d-56ae-69f5-d26a20de0ce7",
        "f816da2c-51f1-612a-2029-a542db7db882",
        "345fea05-c7be-465c-409f-9dcb3bd2aa07"];
list    CHARACTER_GRID2  = [
        "b3017e02-c063-5185-acd5-1ef5f9d79b89",
        "4dcff365-1971-3c2b-d73c-77e1dc54242a"
          ];

///////////// END CONSTANTS ////////////////
string gCharIndex;

integer gActive; //if we are recognized, this is true
/////////// END GLOBAL VARIABLES ////////////
ResetCharIndex() {
    gCharIndex  = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`";
    // \" <-- Fixes LSL syntax highlighting bug.
    gCharIndex += "abcdefghijklmnopqrstuvwxyz{|}~";
    gCharIndex += "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n";
}

vector GetGridPos(integer index1, integer index2) {
    // There are two ways to use the lookup table...
    integer Col;
    integer Row;
    if (index1 >= index2) {
        // In this case, the row is the index of the first character:
        Row = index1;
        // And the col is the index of the second character (x2)
        Col = index2 * 2;
    }
    else { // Index1 < Index2
        // In this case, the row is the index of the second character:
        Row = index2;
        // And the col is the index of the first character, x2, offset by 1.
        Col = index1 * 2 + 1;
    }
    return ;
}

string GetGridTexture(vector grid_pos) {
    // Calculate the texture in the grid to use.
    integer GridCol = llRound(grid_pos.x) / 20;
    integer GridRow = llRound(grid_pos.y) / 10;

    // Lookup the texture.
    key Texture = llList2Key(CHARACTER_GRID, GridRow * (GridRow + 1) / 2 + GridCol);
    return Texture;
}

vector GetGridOffset(vector grid_pos) {
    // Zoom in on the texture showing our character pair.
    integer Col = llRound(grid_pos.x) % 20;
    integer Row = llRound(grid_pos.y) % 10;

    // Return the offset in the texture.
    return <-0.45 + 0.05 * Col, 0.45 - 0.1 * Row, 0.0>;
}

ShowChars(integer link,vector grid_pos1, vector grid_pos2, vector grid_pos3, vector grid_pos4, vector grid_pos5) {
   // Set the primitive textures directly.


   llSetLinkPrimitiveParamsFast( link , [
        PRIM_TEXTURE, FACE_1, GetGridTexture(grid_pos1), <0.25, 0.1, 0>, GetGridOffset(grid_pos1) + <0.075, 0, 0>, 0.0,
        PRIM_TEXTURE, FACE_2, GetGridTexture(grid_pos2), <0.1, 0.1, 0>, GetGridOffset(grid_pos2), 0.0,
        PRIM_TEXTURE, FACE_3, GetGridTexture(grid_pos3), <-1.48, 0.1, 0>, GetGridOffset(grid_pos3)+ <0.37, 0, 0>, 0.0,
        PRIM_TEXTURE, FACE_4, GetGridTexture(grid_pos4), <0.1, 0.1, 0>, GetGridOffset(grid_pos4), 0.0,
        PRIM_TEXTURE, FACE_5, GetGridTexture(grid_pos5), <0.25, 0.1, 0>, GetGridOffset(grid_pos5) - <0.075, 0, 0>, 0.0
        ]);
}

RenderString(integer link, string str) {
    // Get the grid positions for each pair of characters.
    vector GridPos1 = GetGridPos( llSubStringIndex(gCharIndex, llGetSubString(str, 0, 0)),
                                  llSubStringIndex(gCharIndex, llGetSubString(str, 1, 1)) );
    vector GridPos2 = GetGridPos( llSubStringIndex(gCharIndex, llGetSubString(str, 2, 2)),
                                  llSubStringIndex(gCharIndex, llGetSubString(str, 3, 3)) );
    vector GridPos3 = GetGridPos( llSubStringIndex(gCharIndex, llGetSubString(str, 4, 4)),
                                  llSubStringIndex(gCharIndex, llGetSubString(str, 5, 5)) );
    vector GridPos4 = GetGridPos( llSubStringIndex(gCharIndex, llGetSubString(str, 6, 6)),
                                  llSubStringIndex(gCharIndex, llGetSubString(str, 7, 7)) );
    vector GridPos5 = GetGridPos( llSubStringIndex(gCharIndex, llGetSubString(str, 8, 8)),
                                  llSubStringIndex(gCharIndex, llGetSubString(str, 9, 9)) );

    // Use these grid positions to display the correct textures/offsets.
    ShowChars(link,GridPos1, GridPos2, GridPos3, GridPos4, GridPos5);
}

RenderExtended(integer link, string str) {
    // Look for escape sequences.
    list Parsed       = llParseString2List(str, [], (list)ESCAPE_SEQUENCE);
    integer ParsedLen = llGetListLength(Parsed);

    // Create a list of index values to work with.
    list Indices;
    // We start with room for 6 indices.
    integer IndicesLeft = 10;

    string Token;
    integer Clipped;
    integer LastWasEscapeSequence = FALSE;
    // Work from left to right.
    integer i=0;
    for (; i < ParsedLen && IndicesLeft > 0; ++i) {
        Token = llList2String(Parsed, i);

        // If this is an escape sequence, just set the flag and move on.
        if (Token == ESCAPE_SEQUENCE) {
            LastWasEscapeSequence = TRUE;
        }
        else { // Token != ESCAPE_SEQUENCE
            // Otherwise this is a normal token.  Check its length.
            Clipped = FALSE;
            integer TokenLength = llStringLength(Token);
            // Clip if necessary.
            if (TokenLength > IndicesLeft) {
                TokenLength = llStringLength(Token = llGetSubString(Token, 0, IndicesLeft - 1));
                IndicesLeft = 0;
                Clipped = TRUE;
            }
            else
                IndicesLeft -= TokenLength;

            // Was the previous token an escape sequence?
            if (LastWasEscapeSequence) {
                // Yes, the first character is an escape character, the rest are normal.
                // This is the extended character.
                Indices += [llSubStringIndex(EXTENDED_INDEX, llGetSubString(Token, 0, 0)) + 95];

                // These are the normal characters.
                integer j=1;
                for (; j < TokenLength; ++j)
                {
                    Indices += [llSubStringIndex(gCharIndex, llGetSubString(Token, j, j))];
                }
            }
            else { // Normal string.
                // Just add the characters normally.
                integer j=0;
                for (; j < TokenLength; ++j)
                {
                    Indices += [llSubStringIndex(gCharIndex, llGetSubString(Token, j, j))];
                }
            }

            // Unset this flag, since this was not an escape sequence.
            LastWasEscapeSequence = FALSE;
        }
    }

    // Use the indices to create grid positions.
    vector GridPos1 = GetGridPos( llList2Integer(Indices, 0), llList2Integer(Indices, 1) );
    vector GridPos2 = GetGridPos( llList2Integer(Indices, 2), llList2Integer(Indices, 3) );
    vector GridPos3 = GetGridPos( llList2Integer(Indices, 4), llList2Integer(Indices, 5) );
    vector GridPos4 = GetGridPos( llList2Integer(Indices, 6), llList2Integer(Indices, 7) );
    vector GridPos5 = GetGridPos( llList2Integer(Indices, 8), llList2Integer(Indices, 9) );

    // Use these grid positions to display the correct textures/offsets.
    ShowChars(link,GridPos1, GridPos2, GridPos3, GridPos4, GridPos5);
}

integer ConvertIndex(integer index) {
    // This converts from an ASCII based index to our indexing scheme.
    if (index >= 32) // ' ' or higher
        index -= 32;
    else { // index < 32
        // Quick bounds check.
        if (index > 15)
            index = 15;

        index += 94; // extended characters
    }

    return index;
}

default {
    state_entry()
    {
        // Initialize the character index.
        ResetCharIndex();
        llMessageLinked(LINK_THIS, REGISTER_SLAVE, llGetScriptName() , NULL_KEY);
    }

   on_rez(integer num)
   {
      llResetScript();
   }

    link_message(integer sender, integer channel, string data, key id) {
        if (channel == SLAVE_RECOGNIZED)
        {
            if (data == llGetScriptName())
            {
                gActive=TRUE;
            }
            return;
        }

        else if (channel == SLAVE_DISPLAY)
        {
            if (!gActive)
                return;

            list params=llCSV2List((string)id);
            if (llList2String(params, 1) != llGetScriptName())
                return;


            RenderString(llList2Integer(params, 0),data);
            return;
        }

       else if (channel == SLAVE_DISPLAY_EXTENDED)
       {
            if (!gActive)
                return;

            list params=llCSV2List((string)id);
            if (llList2String(params, 1) != llGetScriptName())
                return;

            RenderExtended(llList2Integer(params, 0),data);
    }
        else if (channel == REMAP_INDICES) {
            // Parse the message, splitting it up into index values.
            list Parsed = llCSV2List(data);
            integer i;
            // Go through the list and swap each pair of indices.
            for (i = 0; i < llGetListLength(Parsed); i += 2) {
                integer Index1 = ConvertIndex( llList2Integer(Parsed, i) );
                integer Index2 = ConvertIndex( llList2Integer(Parsed, i + 1) );

                // Swap these index values.
                string Value1 = llGetSubString(gCharIndex, Index1, Index1);
                string Value2 = llGetSubString(gCharIndex, Index2, Index2);

                gCharIndex = llDeleteSubString(gCharIndex, Index1, Index1);
                gCharIndex = llInsertString(gCharIndex, Index1, Value2);

                gCharIndex = llDeleteSubString(gCharIndex, Index2, Index2);
                gCharIndex = llInsertString(gCharIndex, Index2, Value1);
            }
            return;
        }
        else if (channel == RESET_INDICES) {
            // Restore the character index back to default settings.
            ResetCharIndex();
            return;
        }
       else if (channel == SLAVE_RESET)
        {
            ResetCharIndex();
            gActive=FALSE;
            llMessageLinked(LINK_THIS, REGISTER_SLAVE, llGetScriptName() , NULL_KEY);
        }
    }
}
```

## 10-Char Prim Setup

```lsl
////////////////////////////////////////////
// XyzzyText Prim Setup Script (5 Face)
//
// Modified by Thraxis Epsilon
//
////////////////////////////////////////////

default
{
    state_entry()
    {

        llSetPrimitiveParams([
                    PRIM_TYPE, PRIM_TYPE_PRISM, 32, <0.199, 0.8, 0.0>, 0.30, <0.0, 0.0, 0.0>, <1.0, 1.0, 0.0>, <0.0, 0.0, 0.0>,
                    PRIM_SIZE, <0.03, 2.89, 0.5>,
                    PRIM_TEXTURE, 1, "09b04244-9569-d21f-6de0-4bbcf5552222", <2.48, 1.0, 0.0>, <-0.74, 0.0, 0.0>, 0.0,
                    PRIM_TEXTURE, 6, "09b04244-9569-d21f-6de0-4bbcf5552222", <1.0, 1.0, 0.0>, <0.0, 0.0, 0.0>, 0.0,
                    PRIM_TEXTURE, 4, "09b04244-9569-d21f-6de0-4bbcf5552222", <14.75, 1.0, 0.0>, <0.27, 0.0, 0.0>, 0.0,
                    PRIM_TEXTURE, 7, "09b04244-9569-d21f-6de0-4bbcf5552222", <1.0, 1.0, 0.0>, <0.0, 0.0, 0.0>, 0.0,
                    PRIM_TEXTURE, 3, "09b04244-9569-d21f-6de0-4bbcf5552222", <2.48, 1.0, 0.0>, <-0.25, 0.0, 0.0>, 0.0]);

        llRemoveInventory(llGetScriptName());
    }
}
```

XyzzyText - 16 Character MESH PLANE (Modification by Traven Sachs)

## Master Script

```lsl
////////////////////////////////////////////
// XyzzyText v2.1m (16-Char MESH) by Traven Sachs 29-November-2012
// XyzzyText v2.1(10-Char) by Thraxis Epsilon
// XyzzyText v2.1 Script (Set Line Color) by Huney Jewell
// XyzzyText v2.0 Script (5 Face, Single Texture)
//
// Heavily Modified by Thraxis Epsilon, Gigs Taggart 5/2007 and Strife Onizuka 8/2007
// Rewrite to allow one-script-per-object operation w/ optional slaves
// Enable prim-label functionality
// Enabled Banking
// Enabled 10-char per prim
// Enabled 16-Char on an 8 Face Mesh Plane Prim
//
// Modified by Kermitt Quirk 19/01/2006
// To add support for 5 face prim instead of 3
//
// Core XyText Originally Written by Xylor Baysklef
//
////////////////////////////////////////////

/////////////// CONSTANTS ///////////////////
// XyText Message Map.
integer DISPLAY_STRING      = 204000;
integer DISPLAY_EXTENDED    = 204001;
integer REMAP_INDICES       = 204002;
integer RESET_INDICES       = 204003;
integer SET_FADE_OPTIONS    = 204004;
integer SET_FONT_TEXTURE    = 204005;
integer SET_LINE_COLOR      = 204006;
integer SET_COLOR           = 204007;
integer RESCAN_LINKSET      = 204008;

//internal API
integer REGISTER_SLAVE      = 205000;
integer SLAVE_RECOGNIZED    = 205001;
integer SLAVE_DISPLAY       = 205003;
integer SLAVE_DISPLAY_EXTENDED = 205004;
integer SLAVE_RESET         = 205005;

// This is an extended character escape sequence.
string  ESCAPE_SEQUENCE = "\\e";

// This is used to get an index for the extended character.
string  EXTENDED_INDEX  = "123456789abcdef";

// Face numbers.
integer FACE_1          = 0;
integer FACE_2          = 1;
integer FACE_3          = 2;
integer FACE_4          = 3;
integer FACE_5          = 4;
integer FACE_6          = 5;
integer FACE_7          = 6;
integer FACE_8          = 7;

// Used to hide the text after a fade-out.
key     TRANSPARENT     = "f54a0c32-3cd1-d49a-5b4f-7b792bebc204";
key     null_key        = NULL_KEY;

// This is a list of textures for all 2-character combinations.
list    CHARACTER_GRID  = [
        "00e9f9f7-0669-181c-c192-7f8e67678c8d",
        "347a5cb6-0031-7ec0-2fcf-f298eebf3c0e",
        "4e7e689e-37f1-9eca-8596-a958bbd23963",
        "19ea9c21-67ba-8f6f-99db-573b1b877eb1",
        "dde7b412-cda1-652f-6fc2-73f4641f96e1",
        "af6fa3bb-3a6c-9c4f-4bf5-d1c126c830da",
        "a201d3a2-364b-43b6-8686-5881c0f82a94",
        "b674dec8-fead-99e5-c28d-2db8e4c51540",
        "366e05f3-be6b-e5cf-c33b-731dff649caa",
        "75c4925c-0427-dc0c-c71c-e28674ff4d27",
        "dcbe166b-6a97-efb2-fc8e-e5bc6a8b1be6",
        "0dca2feb-fc66-a762-db85-89026a4ecd68",
        "a0fca76f-503a-946b-9336-0a918e886f7a",
        "67fb375d-89a1-5a4f-8c7a-0cd1c066ffc4",
        "300470b2-da34-5470-074c-1b8464ca050c",
        "d1f8e91c-ce2b-d85e-2120-930d3b630946",
        "2a190e44-7b29-dadb-0bff-c31adaf5a170",
        "75d55e71-f6f8-9835-e746-a45f189f30a1",
        "300fac33-2b30-3da3-26bc-e2d70428ec19",
        "0747c776-011a-53ce-13ee-8b5bb9e87c1e",
        "85a855c3-a94f-01ca-33e0-7dde92e727e2",
        "cbc1dab2-2d61-2986-1949-7a5235c954e1",
        "f7aef047-f266-9596-16df-641010edd8e1",
        "4c34ebf7-e5e1-2e1a-579f-e224d9d5e71b",
        "4a69e98c-26a5-ad05-e92e-b5b906ad9ef9",
        "462a9226-2a97-91ac-2d89-57ab33334b78",
        "20b24b3a-8c57-82ee-c6ed-555003f5dbcd",
        "9b481daa-9ea8-a9fa-1ee4-ab9a0d38e217",
        "c231dbdc-c842-15b0-7aa6-6da14745cfdc",
        "c97e3cbb-c9a3-45df-a0ae-955c1f4bf9cf",
        "f1e7d030-ff80-a242-cb69-f6951d4eae3b",
        "ed32d6c4-d733-c0f1-f242-6df1d222220d",
        "88f96a30-dccf-9b20-31ef-da0dfeb23c72",
        "252f2595-58b8-4bcc-6515-fa274d0cfb65",
        "f2838c4f-de80-cced-dff8-195dfdf36b2c",
        "cc2594fe-add2-a3df-cdb3-a61711badf53",
        "e0ce2972-da00-955c-129e-3289b3676776",
        "3e0d336d-321f-ddfa-5c1b-e26131766f6a",
        "d43b1dc4-6b51-76a7-8b90-38865b82bf06",
        "06d16cbb-1868-fd1d-5c93-eae42164a37d",
        "dd5d98cf-273e-3fd0-f030-48be58ee3a0b",
        "0e47c89e-de4a-6233-a2da-cb852aad1b00",
        "fb9c4a55-0e13-495b-25c4-f0b459dc06de",
        "e3ce8def-312c-735b-0e48-018b6799c883",
        "2f713216-4e71-d123-03ed-9c8554710c6b",
        "4a417d8a-1f4f-404b-9783-6672f8527911",
        "ca5e21ec-5b20-5909-4c31-3f90d7316b33",
        "06a4fcc3-e1c4-296d-8817-01f88fbd7367",
        "130ac084-6f3c-95de-b5b6-d25c80703474",
        "59d540a0-ae9d-3606-5ae0-4f2842b64cfa",
        "8612ae9a-f53c-5bf4-2899-8174d7abc4fd",
        "12467401-e979-2c49-34e0-6ac761542797",
        "d53c3eaa-0404-3860-0675-3e375596c3e3",
        "9f5b26bd-81d3-b25e-62fe-5b671d1e3e79",
        "f57f0b64-a050-d617-ee00-c8e9e3adc9cb",
        "beff166a-f5f3-f05e-e020-98f2b00e27ed",
        "02278a65-94ba-6d5e-0d2b-93f2e4f4bf70",
        "a707197d-449e-5b58-846c-0c850c61f9d6",
        "021d4b1a-9503-a44f-ee2b-976eb5d80e68",
        "0ae2ffae-7265-524d-cb76-c2b691992706"];
list    CHARACTER_GRID2  = [
        "f6e41cf2-1104-bd0b-0190-dffad1bac813",
        "2b4bb15e-956d-56ae-69f5-d26a20de0ce7",
        "f816da2c-51f1-612a-2029-a542db7db882",
        "345fea05-c7be-465c-409f-9dcb3bd2aa07",
        "b3017e02-c063-5185-acd5-1ef5f9d79b89",
        "4dcff365-1971-3c2b-d73c-77e1dc54242a"
          ];

///////////// END CONSTANTS ////////////////

///////////// GLOBAL VARIABLES ///////////////
// All displayable characters.  Default to ASCII order.
string gCharIndex;
// This is the channel to listen on while acting
// as a cell in a larger display.
integer gCellChannel      = -1;
// This is the starting character position in the cell channel message
// to render.
integer gCellCharPosition = 0;
// This is whether or not to use the fade in/out special effect.
integer gCellUseFading      = FALSE;
// This is how long to display the text before fading out (if using
// fading special effect).
// Note: < 0  means don't fade out.
float   gCellHoldDelay      = 1.0;

integer gSlaveRegistered;
list gSlaveNames;

integer BANK_STRIDE = 3; //offset, length, highest_dirty
list gBankingData;

/////////// END GLOBAL VARIABLES ////////////

ResetCharIndex() {
    gCharIndex  = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`";
    // \" <-- Fixes LSL syntax highlighting bug.
    gCharIndex += "abcdefghijklmnopqrstuvwxyz{|}~";
    gCharIndex += "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n";
}

vector GetGridPos(integer index1, integer index2) {
    // There are two ways to use the lookup table...
    integer Col;
    integer Row;
    if (index1 >= index2) {
        // In this case, the row is the index of the first character:
        Row = index1;
        // And the col is the index of the second character (x2)
        Col = index2 * 2;
    }
    else { // Index1 < Index2
        // In this case, the row is the index of the second character:
        Row = index2;
        // And the col is the index of the first character, x2, offset by 1.
        Col = index1 * 2 + 1;
    }
    return ;
}

string GetGridTexture(vector grid_pos) {
    // Calculate the texture in the grid to use.
    integer GridCol = llRound(grid_pos.x) / 20;
    integer GridRow = llRound(grid_pos.y) / 10;

    // Lookup the texture.
    key Texture = llList2Key(CHARACTER_GRID, GridRow * (GridRow + 1) / 2 + GridCol);
    return Texture;
}

vector GetGridOffset(vector grid_pos) {
    // Zoom in on the texture showing our character pair.
    integer Col = llRound(grid_pos.x) % 20;
    integer Row = llRound(grid_pos.y) % 10;

    // Return the offset in the texture.
    return <-0.45 + 0.05 * Col, 0.45 - 0.1 * Row, 0.0>;
}

ShowChars(integer link,vector grid_pos1, vector grid_pos2, vector grid_pos3, vector grid_pos4, vector grid_pos5, vector grid_pos6, vector grid_pos7, vector grid_pos8) {
   // Set the primitive textures directly.

//integer face, string name, vector repeats, vector offsets, float rotation
   llSetLinkPrimitiveParamsFast( link , [
        PRIM_TEXTURE, FACE_1, GetGridTexture(grid_pos1), <0.1, 0.1, 0>, GetGridOffset(grid_pos1), 0.0,
        PRIM_TEXTURE, FACE_2, GetGridTexture(grid_pos2), <0.1, 0.1, 0>, GetGridOffset(grid_pos2), 0.0,
        PRIM_TEXTURE, FACE_3, GetGridTexture(grid_pos3), <0.1, 0.1, 0>, GetGridOffset(grid_pos3), 0.0,
        PRIM_TEXTURE, FACE_4, GetGridTexture(grid_pos4), <0.1, 0.1, 0>, GetGridOffset(grid_pos4), 0.0,
        PRIM_TEXTURE, FACE_5, GetGridTexture(grid_pos5), <0.1, 0.1, 0>, GetGridOffset(grid_pos5), 0.0,
        PRIM_TEXTURE, FACE_6, GetGridTexture(grid_pos6), <0.1, 0.1, 0>, GetGridOffset(grid_pos6), 0.0,
        PRIM_TEXTURE, FACE_7, GetGridTexture(grid_pos7), <0.1, 0.1, 0>, GetGridOffset(grid_pos7), 0.0,
        PRIM_TEXTURE, FACE_8, GetGridTexture(grid_pos8), <0.1, 0.1, 0>, GetGridOffset(grid_pos8), 0.0
        ]);
}

RenderString(integer link, string str) {
    // Get the grid positions for each pair of characters.
    vector GridPos1 = GetGridPos( llSubStringIndex(gCharIndex, llGetSubString(str, 0, 0)),
                                  llSubStringIndex(gCharIndex, llGetSubString(str, 1, 1)) );
    vector GridPos2 = GetGridPos( llSubStringIndex(gCharIndex, llGetSubString(str, 2, 2)),
                                  llSubStringIndex(gCharIndex, llGetSubString(str, 3, 3)) );
    vector GridPos3 = GetGridPos( llSubStringIndex(gCharIndex, llGetSubString(str, 4, 4)),
                                  llSubStringIndex(gCharIndex, llGetSubString(str, 5, 5)) );
    vector GridPos4 = GetGridPos( llSubStringIndex(gCharIndex, llGetSubString(str, 6, 6)),
                                  llSubStringIndex(gCharIndex, llGetSubString(str, 7, 7)) );
    vector GridPos5 = GetGridPos( llSubStringIndex(gCharIndex, llGetSubString(str, 8, 8)),
                                  llSubStringIndex(gCharIndex, llGetSubString(str, 9, 9)) );
    vector GridPos6 = GetGridPos( llSubStringIndex(gCharIndex, llGetSubString(str, 10, 10)),
                                  llSubStringIndex(gCharIndex, llGetSubString(str, 11, 11)) );
    vector GridPos7 = GetGridPos( llSubStringIndex(gCharIndex, llGetSubString(str, 12, 12)),
                                  llSubStringIndex(gCharIndex, llGetSubString(str, 13, 13)) );
    vector GridPos8 = GetGridPos( llSubStringIndex(gCharIndex, llGetSubString(str, 14, 14)),
                                  llSubStringIndex(gCharIndex, llGetSubString(str, 15, 15)) );

    // Use these grid positions to display the correct textures/offsets.
    ShowChars(link,GridPos1, GridPos2, GridPos3, GridPos4, GridPos5, GridPos6, GridPos7, GridPos8);
}

//RenderWithEffects(integer link, string str) {
//    // Get the grid positions for each pair of characters.
//    vector GridPos1 = GetGridPos( llSubStringIndex(gCharIndex, llGetSubString(str, 0, 0)),
//                                  llSubStringIndex(gCharIndex, llGetSubString(str, 1, 1)) );
//    vector GridPos2 = GetGridPos( llSubStringIndex(gCharIndex, llGetSubString(str, 2, 2)),
//                                  llSubStringIndex(gCharIndex, llGetSubString(str, 3, 3)) );
//    vector GridPos3 = GetGridPos( llSubStringIndex(gCharIndex, llGetSubString(str, 4, 4)),
//                                  llSubStringIndex(gCharIndex, llGetSubString(str, 5, 5)) );
//    vector GridPos4 = GetGridPos( llSubStringIndex(gCharIndex, llGetSubString(str, 6, 6)),
//                                  llSubStringIndex(gCharIndex, llGetSubString(str, 7, 7)) );
//    vector GridPos5 = GetGridPos( llSubStringIndex(gCharIndex, llGetSubString(str, 8, 8)),
//                                  llSubStringIndex(gCharIndex, llGetSubString(str, 9, 9)) );                          //
//
//      // First set the alpha to the lowest possible.
//   llSetAlpha(0.05, ALL_SIDES);
//
//    // Use these grid positions to display the correct textures/offsets.
//    ShowChars(link,GridPos1, GridPos2, GridPos3, GridPos4, GridPos5);
//
//    float Alpha = 0.10;
//    for (; Alpha <= 1.0; Alpha += 0.05)
//       llSetAlpha(Alpha, ALL_SIDES);
//          // See if we want to fade out as well.
//   if (gCellHoldDelay < 0.0)
//       // No, bail out. (Just keep showing the string at full strength).
//       return;
//          // Hold the text for a while.
//   llSleep(gCellHoldDelay);
//      // Now fade out.
//   for (Alpha = 0.95; Alpha >= 0.05; Alpha -= 0.05)
//       llSetAlpha(Alpha, ALL_SIDES);
//          // Make the text transparent to fully hide it.
//   llSetTexture(TRANSPARENT, ALL_SIDES);
//}

integer RenderExtended(integer link, string str,integer render) {
    // Look for escape sequences.
    integer length = 0;
    list Parsed       = llParseString2List(str, [], (list)ESCAPE_SEQUENCE);
    integer ParsedLen = llGetListLength(Parsed);

    // Create a list of index values to work with.
    list Indices;
    // We start with room for 6 indices.
    integer IndicesLeft = 16;

    string Token;
    integer Clipped;
    integer LastWasEscapeSequence = FALSE;
    // Work from left to right.
    integer i=0;
    for (; i < ParsedLen && IndicesLeft > 0; ++i) {
        Token = llList2String(Parsed, i);

        // If this is an escape sequence, just set the flag and move on.
        if (Token == ESCAPE_SEQUENCE) {
            LastWasEscapeSequence = TRUE;
        }
        else { // Token != ESCAPE_SEQUENCE
            // Otherwise this is a normal token.  Check its length.
            Clipped = FALSE;
            integer TokenLength = llStringLength(Token);
            // Clip if necessary.
            if (TokenLength > IndicesLeft) {
                TokenLength = llStringLength(Token = llGetSubString(Token, 0, IndicesLeft - 1));
                IndicesLeft = 0;
                Clipped = TRUE;
            }
            else
                IndicesLeft -= TokenLength;

            // Was the previous token an escape sequence?
            if (LastWasEscapeSequence) {
                // Yes, the first character is an escape character, the rest are normal.
                length += 2 + TokenLength;
                if (render)
                {
                    // This is the extended character.
                    Indices += [llSubStringIndex(EXTENDED_INDEX, llGetSubString(Token, 0, 0)) + 95];

                    // These are the normal characters.
                    integer j=1;
                    for (; j < TokenLength; ++j)
                    {
                        Indices += [llSubStringIndex(gCharIndex, llGetSubString(Token, j, j))];
                    }
                }
            }
            else { // Normal string.
                // Just add the characters normally.
                length += TokenLength;
                if(render)
                {
                    integer j=0;
                    for (; j < TokenLength; ++j)
                    {
                        Indices += [llSubStringIndex(gCharIndex, llGetSubString(Token, j, j))];
                    }
                }
            }

            // Unset this flag, since this was not an escape sequence.
            LastWasEscapeSequence = FALSE;
        }
    }

    if(render)
    {
        // Use the indices to create grid positions.
        vector GridPos1 = GetGridPos( llList2Integer(Indices, 0), llList2Integer(Indices, 1) );
        vector GridPos2 = GetGridPos( llList2Integer(Indices, 2), llList2Integer(Indices, 3) );
        vector GridPos3 = GetGridPos( llList2Integer(Indices, 4), llList2Integer(Indices, 5) );
        vector GridPos4 = GetGridPos( llList2Integer(Indices, 6), llList2Integer(Indices, 7) );
        vector GridPos5 = GetGridPos( llList2Integer(Indices, 8), llList2Integer(Indices, 9) );
        vector GridPos6 = GetGridPos( llList2Integer(Indices, 10), llList2Integer(Indices, 11) );
        vector GridPos7 = GetGridPos( llList2Integer(Indices, 12), llList2Integer(Indices, 13) );
        vector GridPos8 = GetGridPos( llList2Integer(Indices, 14), llList2Integer(Indices, 15) );

        // Use these grid positions to display the correct textures/offsets.
        ShowChars(link, GridPos1, GridPos2, GridPos3, GridPos4, GridPos5, GridPos6, GridPos7, GridPos8);
    }
    return length;
}

integer ConvertIndex(integer index) {
    // This converts from an ASCII based index to our indexing scheme.
    if (index >= 32) // ' ' or higher
        index -= 32;
    else { // index < 32
        // Quick bounds check.
        if (index > 15)
            index = 15;

        index += 94; // extended characters
    }

    return index;
}

PassToRender(integer render,string message, integer bank)
{
    float time;
    integer extendedlen = 0;
    integer link;

    integer i = 0;
    integer msgLen = llStringLength(message);
    string TextToRender;
    integer num_slaves=llGetListLength(gSlaveNames);
    string slave_name; //avoids unnecessary casts, keeping it as a string


    //get the bank offset and length
    integer bank_offset=llList2Integer(gBankingData, (bank * BANK_STRIDE));
    integer bank_length=llList2Integer(gBankingData, (bank * BANK_STRIDE) + 1);
    integer bank_highest_dirty=llList2Integer(gBankingData, (bank * BANK_STRIDE) + 2);

    integer x=0;
    for (;x < msgLen;x = x + 16)
    {

        if (i >= bank_length)  //we don't want to run off the end of the bank
        {
            //set the dirty to max, and bail out, we're done
            gBankingData=llListReplaceList(gBankingData, [bank_length], (bank * BANK_STRIDE) + 2, (bank * BANK_STRIDE) + 2);
            return;
        }

        link = unpack(gXyTextPrims,(i + bank_offset));
        TextToRender = llGetSubString(message, x, x + 32);

        if(gSlaveRegistered && (link % (num_slaves +1)))
        {
            slave_name=llList2String(gSlaveNames, (link % (num_slaves + 1)) - 1);
            if (render == 1)
                llMessageLinked(LINK_THIS, SLAVE_DISPLAY, TextToRender, (key)((string)link + "," + slave_name));
            if (render == 2)
            {
                if(llSubStringIndex(TextToRender,"\e")>x+16)
                {
                    extendedlen = 16;
                }
                else
                {
                    extendedlen = RenderExtended(link,TextToRender,0);
                }

                if(extendedlen>16)
                {
                    x += extendedlen-16;
                }

                llMessageLinked(LINK_THIS,SLAVE_DISPLAY_EXTENDED,TextToRender,(key)((string)link+","+slave_name));
            }
        }
        else
        {
            if (render == 1)
                RenderString(link,TextToRender);
            if (render == 2)
            {
                extendedlen = RenderExtended(link,TextToRender,1);
                if(extendedlen>16)
                {
                    x += extendedlen-16;
                }
            }

//            if (render == 3)
//                RenderWithEffects(link,TextToRender);
        }
        ++i;
    }

    if (bank_highest_dirty==0)
        bank_highest_dirty=bank_length;

    integer current_highest_dirty=i;
    while (i < bank_highest_dirty)
    {
        link = unpack(gXyTextPrims,(i + bank_offset));

        if(gSlaveRegistered && (link % (num_slaves+1) != 0))
        {
            slave_name=llList2String(gSlaveNames, (link % (num_slaves + 1)) - 1);
            llMessageLinked(LINK_THIS, SLAVE_DISPLAY, "     ", (key)((string)link + "," + slave_name));
            //sorry, no fade effect with slave
        }
        else
        {
            RenderString(link,"          ");
        }
        ++i;
    }
    gBankingData=llListReplaceList(gBankingData, [current_highest_dirty], (bank * BANK_STRIDE) + 2, (bank * BANK_STRIDE) + 2);
}

// Bitwise Voodoo by Gigs Taggart and optimized by Strife Onizuka
list gXyTextPrims;

integer get_number_of_prims()
{//ignores avatars.
    integer a = llGetNumberOfPrims();
    while(llGetAgentSize(llGetLinkKey(a)))
        --a;
    return a;
}

//functions to pack 8-bit shorts into ints
list pack_and_insert(list in_list, integer pos, integer value)
{
//    //figure out the bitpack position
//    integer pack = pos & 3; //4 bytes per int
//    pos=pos >> 2;
//    integer shifted = value << (pack << 3);
//    integer old_value = llList2Integer(in_list, pos);
//    shifted = old_value | shifted;
//    in_list = llListReplaceList(in_list, (list)shifted, pos, pos);
//    return in_list;
    //Safe optimized version
    integer index = pos >> 2;
    return llListReplaceList(in_list, (list)(llList2Integer(in_list, index) | (value << ((pos & 3) << 3))), index, index);
}

integer unpack(list in_list, integer pos)
{
    return (llList2Integer(in_list, pos >> 2) >> ((pos & 3) << 3)) & 0x000000FF;//unsigned
//    return (llList2Integer(in_list, pos >> 2) << (((~pos) & 3) << 3)) >> 24;//signed
}

change_color(vector color)
{
    integer num_prims=llGetListLength(gXyTextPrims) << 2;

    integer i = 0;

    for (; i<=num_prims; ++i)
    {
        integer link = unpack(gXyTextPrims,i);
        if (!link)
            return;

        llSetLinkPrimitiveParamsFast( link,[
            PRIM_COLOR, FACE_1, color, 1.0,
            PRIM_COLOR, FACE_2, color, 1.0,
            PRIM_COLOR, FACE_3, color, 1.0,
            PRIM_COLOR, FACE_4, color, 1.0,
            PRIM_COLOR, FACE_5, color, 1.0,
            PRIM_COLOR, FACE_6, color, 1.0,
            PRIM_COLOR, FACE_7, color, 1.0,
            PRIM_COLOR, FACE_8, color, 1.0
        ]);
    }
}

change_line_color(integer bank, vector color)
{

    //get the bank offset and length
    integer i = llList2Integer(gBankingData, (bank * BANK_STRIDE));
    integer bank_end = i + llList2Integer(gBankingData, (bank * BANK_STRIDE) + 1);

    for (; i < bank_end; ++i)
    {
        integer link = unpack(gXyTextPrims,i);
        if (!link)
            return;

        llSetLinkPrimitiveParamsFast( link,[
            PRIM_COLOR, FACE_1, color, 1.0,
            PRIM_COLOR, FACE_2, color, 1.0,
            PRIM_COLOR, FACE_3, color, 1.0,
            PRIM_COLOR, FACE_4, color, 1.0,
            PRIM_COLOR, FACE_5, color, 1.0,
            PRIM_COLOR, FACE_6, color, 1.0,
            PRIM_COLOR, FACE_7, color, 1.0,
            PRIM_COLOR, FACE_8, color, 1.0
        ]);
    }
}

init()
{
    integer num_prims=get_number_of_prims();

    string link_name;
    integer bank=0;
    integer bank_empty=FALSE;
    integer prims_pointer=0; //"pointer" to the next entry to be used in the gXyTextPrims list.

    list temp_bank=[];
    integer temp_bank_stride=2;


    gXyTextPrims=[];
    integer x=0;
    for (;x<64;++x)
    {
        gXyTextPrims= (gXyTextPrims = []) + gXyTextPrims + [0];  //we need to pad out the list to make it easier to add things in any order later
    }

    @loop;

    {

        //loop over all prims, looking for ones in the current bank
        for(x=0;x<=num_prims;++x)
        {
            link_name=llGetLinkName(x);
            list tmp = llParseString2List(link_name, ["-"], []);
            if(llList2String(tmp,0)== "xyzzytext")
            {
                integer prims_bank=llList2Integer(tmp,1);
                if (llList2Integer(tmp,1)==bank)
                {
                    temp_bank+=llList2Integer(tmp,2) + (list)x;
                }
            }

        }


        if (temp_bank!=[])
        {
            //sort the current bank
            temp_bank=llListSort(temp_bank, temp_bank_stride, TRUE);

            integer temp_len=llGetListLength(temp_bank);

            //store metadata
            gBankingData+=[prims_pointer,temp_len/temp_bank_stride,0];

            //repack the bank into the prim list
            for (x=0; x < temp_len; x+=temp_bank_stride)
            {
                gXyTextPrims = pack_and_insert(gXyTextPrims, prims_pointer, llList2Integer(temp_bank, x+1));
                ++prims_pointer;
            }
            ++bank;
            temp_bank=[];
            jump loop;
        }
    }

    llMessageLinked(LINK_THIS, SLAVE_RESET, "" , null_key);
}

default {
    state_entry() {
        // Initialize the character index.
        ResetCharIndex();
        init();
    }

   on_rez(integer num)
   {
      llResetScript();
   }

    link_message(integer sender, integer channel, string data, key id) {
        if(id == null_key)
            id="0";

        if (channel == DISPLAY_STRING) {
            PassToRender(1,data, (integer)((string)id));
            return;
        }
        else if (channel == DISPLAY_EXTENDED) {
             PassToRender(2,data, (integer)((string)id));
            return;
        }
        else if (channel == REMAP_INDICES) {
            // Parse the message, splitting it up into index values.
            list Parsed = llCSV2List(data);
            integer i;
            // Go through the list and swap each pair of indices.
            for (i = 0; i < llGetListLength(Parsed); i += 2) {
                integer Index1 = ConvertIndex( llList2Integer(Parsed, i) );
                integer Index2 = ConvertIndex( llList2Integer(Parsed, i + 1) );

                // Swap these index values.
                string Value1 = llGetSubString(gCharIndex, Index1, Index1);
                string Value2 = llGetSubString(gCharIndex, Index2, Index2);

                gCharIndex = llDeleteSubString(gCharIndex, Index1, Index1);
                gCharIndex = llInsertString(gCharIndex, Index1, Value2);

                gCharIndex = llDeleteSubString(gCharIndex, Index2, Index2);
                gCharIndex = llInsertString(gCharIndex, Index2, Value1);
            }
            return;
        }
        else if (channel == RESET_INDICES) {
            // Restore the character index back to default settings.
            ResetCharIndex();
            return;
        }
        else if (channel == RESCAN_LINKSET)
        {
            init();
        }
        else if (channel == SET_COLOR) {
            change_color((vector)data);
        }
        else if (channel == SET_LINE_COLOR) {
            change_line_color((integer)((string)id), (vector)data);
        }
        else if (channel == REGISTER_SLAVE)
        {
            if(!~llListFindList(gSlaveNames, (list)data))
            {//isn't registered yet
                gSlaveNames += data;
                gSlaveRegistered=TRUE;
                //llOwnerSay((string)llGetListLength(gSlaveNames) + " Slave(s) Recognized: " + data);
            }
//            else
//            {//it already exists
//                llOwnerSay((string)llGetListLength(gSlaveNames) + " Slave, Existing Slave Recognized: " + data);
//            }
            llMessageLinked(LINK_THIS, SLAVE_RECOGNIZED, data , null_key);
        }
    }

    changed(integer change)
    {
        if(change&CHANGED_INVENTORY)
        {
            if(gSlaveRegistered)
            {
                //by using negative indexes they don't need to be adjusted when an entry is deleted.
                integer x = ~llGetListLength(gSlaveNames);
                while(++x)
                {
                    if (!~llGetInventoryType(llList2String(gSlaveNames, x)))
                    {
                        //llOwnerSay("Slave Removed: " + llList2String(gSlaveNames, x));
                        gSlaveNames = llDeleteSubList(gSlaveNames, x, x);
                    }
                }
                gSlaveRegistered = !(gSlaveNames == []);
            }
        }
    }
}
```

## Slave Script

```lsl
////////////////////////////////////////////
// XyzzyText v2.1m (16-Char MESH) by Traven Sachs 29-November-2012
// XyzzyText v2.1(10-Char) by Thraxis Epsilon
// XyText v2.0 SLAVE Script (5 Face, Single Texture)
//
// Heavily Modified by Thraxis Epsilon, Gigs Taggart 5/2007 and Strife Onizuka 8/2007
// Rewrite to allow one-script-per-object operation w/ optional slaves
// Enable prim-label functionality
// Enabled Banking
// Enabled 10-char per prim
// Enabled 16-Char on an 8 Face Mesh Plane Prim
//
// Modified by Kermitt Quirk 19/01/2006
// To add support for 5 face prim instead of 3
//
// Originally Written by Xylor Baysklef
//
//
////////////////////////////////////////////

integer REMAP_INDICES       = 204002;
integer RESET_INDICES       = 204003;

//internal API
integer REGISTER_SLAVE      = 205000;
integer SLAVE_RECOGNIZED    = 205001;
integer SLAVE_DISPLAY       = 205003;
integer SET_FONT_TEXTURE    = 204005;

integer SLAVE_DISPLAY_EXTENDED = 205004;
integer SLAVE_RESET = 205005;

// This is an extended character escape sequence.
string  ESCAPE_SEQUENCE = "\\e";

// This is used to get an index for the extended character.
string  EXTENDED_INDEX  = "123456789abcdef";

// Face numbers.
integer FACE_1          = 0;
integer FACE_2          = 1;
integer FACE_3          = 2;
integer FACE_4          = 3;
integer FACE_5          = 4;
integer FACE_6          = 5;
integer FACE_7          = 6;
integer FACE_8          = 7;

// This is a list of textures for all 2-character combinations.
list    CHARACTER_GRID  = [
        "00e9f9f7-0669-181c-c192-7f8e67678c8d",
        "347a5cb6-0031-7ec0-2fcf-f298eebf3c0e",
        "4e7e689e-37f1-9eca-8596-a958bbd23963",
        "19ea9c21-67ba-8f6f-99db-573b1b877eb1",
        "dde7b412-cda1-652f-6fc2-73f4641f96e1",
        "af6fa3bb-3a6c-9c4f-4bf5-d1c126c830da",
        "a201d3a2-364b-43b6-8686-5881c0f82a94",
        "b674dec8-fead-99e5-c28d-2db8e4c51540",
        "366e05f3-be6b-e5cf-c33b-731dff649caa",
        "75c4925c-0427-dc0c-c71c-e28674ff4d27",
        "dcbe166b-6a97-efb2-fc8e-e5bc6a8b1be6",
        "0dca2feb-fc66-a762-db85-89026a4ecd68",
        "a0fca76f-503a-946b-9336-0a918e886f7a",
        "67fb375d-89a1-5a4f-8c7a-0cd1c066ffc4",
        "300470b2-da34-5470-074c-1b8464ca050c",
        "d1f8e91c-ce2b-d85e-2120-930d3b630946",
        "2a190e44-7b29-dadb-0bff-c31adaf5a170",
        "75d55e71-f6f8-9835-e746-a45f189f30a1",
        "300fac33-2b30-3da3-26bc-e2d70428ec19",
        "0747c776-011a-53ce-13ee-8b5bb9e87c1e",
        "85a855c3-a94f-01ca-33e0-7dde92e727e2",
        "cbc1dab2-2d61-2986-1949-7a5235c954e1",
        "f7aef047-f266-9596-16df-641010edd8e1",
        "4c34ebf7-e5e1-2e1a-579f-e224d9d5e71b",
        "4a69e98c-26a5-ad05-e92e-b5b906ad9ef9",
        "462a9226-2a97-91ac-2d89-57ab33334b78",
        "20b24b3a-8c57-82ee-c6ed-555003f5dbcd",
        "9b481daa-9ea8-a9fa-1ee4-ab9a0d38e217",
        "c231dbdc-c842-15b0-7aa6-6da14745cfdc",
        "c97e3cbb-c9a3-45df-a0ae-955c1f4bf9cf",
        "f1e7d030-ff80-a242-cb69-f6951d4eae3b",
        "ed32d6c4-d733-c0f1-f242-6df1d222220d",
        "88f96a30-dccf-9b20-31ef-da0dfeb23c72",
        "252f2595-58b8-4bcc-6515-fa274d0cfb65",
        "f2838c4f-de80-cced-dff8-195dfdf36b2c",
        "cc2594fe-add2-a3df-cdb3-a61711badf53",
        "e0ce2972-da00-955c-129e-3289b3676776",
        "3e0d336d-321f-ddfa-5c1b-e26131766f6a",
        "d43b1dc4-6b51-76a7-8b90-38865b82bf06",
        "06d16cbb-1868-fd1d-5c93-eae42164a37d",
        "dd5d98cf-273e-3fd0-f030-48be58ee3a0b",
        "0e47c89e-de4a-6233-a2da-cb852aad1b00",
        "fb9c4a55-0e13-495b-25c4-f0b459dc06de",
        "e3ce8def-312c-735b-0e48-018b6799c883",
        "2f713216-4e71-d123-03ed-9c8554710c6b",
        "4a417d8a-1f4f-404b-9783-6672f8527911",
        "ca5e21ec-5b20-5909-4c31-3f90d7316b33",
        "06a4fcc3-e1c4-296d-8817-01f88fbd7367",
        "130ac084-6f3c-95de-b5b6-d25c80703474",
        "59d540a0-ae9d-3606-5ae0-4f2842b64cfa",
        "8612ae9a-f53c-5bf4-2899-8174d7abc4fd",
        "12467401-e979-2c49-34e0-6ac761542797",
        "d53c3eaa-0404-3860-0675-3e375596c3e3",
        "9f5b26bd-81d3-b25e-62fe-5b671d1e3e79",
        "f57f0b64-a050-d617-ee00-c8e9e3adc9cb",
        "beff166a-f5f3-f05e-e020-98f2b00e27ed",
        "02278a65-94ba-6d5e-0d2b-93f2e4f4bf70",
        "a707197d-449e-5b58-846c-0c850c61f9d6",
        "021d4b1a-9503-a44f-ee2b-976eb5d80e68",
        "0ae2ffae-7265-524d-cb76-c2b691992706",
        "f6e41cf2-1104-bd0b-0190-dffad1bac813",
        "2b4bb15e-956d-56ae-69f5-d26a20de0ce7",
        "f816da2c-51f1-612a-2029-a542db7db882",
        "345fea05-c7be-465c-409f-9dcb3bd2aa07"];
list    CHARACTER_GRID2  = [
        "b3017e02-c063-5185-acd5-1ef5f9d79b89",
        "4dcff365-1971-3c2b-d73c-77e1dc54242a"
          ];

///////////// END CONSTANTS ////////////////
string gCharIndex;

integer gActive; //if we are recognized, this is true
/////////// END GLOBAL VARIABLES ////////////
ResetCharIndex() {
    gCharIndex  = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`";
    // \" <-- Fixes LSL syntax highlighting bug.
    gCharIndex += "abcdefghijklmnopqrstuvwxyz{|}~";
    gCharIndex += "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n";
}

vector GetGridPos(integer index1, integer index2) {
    // There are two ways to use the lookup table...
    integer Col;
    integer Row;
    if (index1 >= index2) {
        // In this case, the row is the index of the first character:
        Row = index1;
        // And the col is the index of the second character (x2)
        Col = index2 * 2;
    }
    else { // Index1 < Index2
        // In this case, the row is the index of the second character:
        Row = index2;
        // And the col is the index of the first character, x2, offset by 1.
        Col = index1 * 2 + 1;
    }
    return ;
}

string GetGridTexture(vector grid_pos) {
    // Calculate the texture in the grid to use.
    integer GridCol = llRound(grid_pos.x) / 20;
    integer GridRow = llRound(grid_pos.y) / 10;

    // Lookup the texture.
    key Texture = llList2Key(CHARACTER_GRID, GridRow * (GridRow + 1) / 2 + GridCol);
    return Texture;
}

vector GetGridOffset(vector grid_pos) {
    // Zoom in on the texture showing our character pair.
    integer Col = llRound(grid_pos.x) % 20;
    integer Row = llRound(grid_pos.y) % 10;

    // Return the offset in the texture.
    return <-0.45 + 0.05 * Col, 0.45 - 0.1 * Row, 0.0>;
}

ShowChars(integer link,vector grid_pos1, vector grid_pos2, vector grid_pos3, vector grid_pos4, vector grid_pos5, vector grid_pos6, vector grid_pos7, vector grid_pos8) {
   // Set the primitive textures directly.


   llSetLinkPrimitiveParamsFast( link , [
        PRIM_TEXTURE, FACE_1, GetGridTexture(grid_pos1), <0.1, 0.1, 0>, GetGridOffset(grid_pos1), 0.0,
        PRIM_TEXTURE, FACE_2, GetGridTexture(grid_pos2), <0.1, 0.1, 0>, GetGridOffset(grid_pos2), 0.0,
        PRIM_TEXTURE, FACE_3, GetGridTexture(grid_pos3), <0.1, 0.1, 0>, GetGridOffset(grid_pos3), 0.0,
        PRIM_TEXTURE, FACE_4, GetGridTexture(grid_pos4), <0.1, 0.1, 0>, GetGridOffset(grid_pos4), 0.0,
        PRIM_TEXTURE, FACE_5, GetGridTexture(grid_pos5), <0.1, 0.1, 0>, GetGridOffset(grid_pos5), 0.0,
        PRIM_TEXTURE, FACE_6, GetGridTexture(grid_pos6), <0.1, 0.1, 0>, GetGridOffset(grid_pos6), 0.0,
        PRIM_TEXTURE, FACE_7, GetGridTexture(grid_pos7), <0.1, 0.1, 0>, GetGridOffset(grid_pos7), 0.0,
        PRIM_TEXTURE, FACE_8, GetGridTexture(grid_pos8), <0.1, 0.1, 0>, GetGridOffset(grid_pos8), 0.0
        ]);
}

RenderString(integer link, string str) {
    // Get the grid positions for each pair of characters.
    vector GridPos1 = GetGridPos( llSubStringIndex(gCharIndex, llGetSubString(str, 0, 0)),
                                  llSubStringIndex(gCharIndex, llGetSubString(str, 1, 1)) );
    vector GridPos2 = GetGridPos( llSubStringIndex(gCharIndex, llGetSubString(str, 2, 2)),
                                  llSubStringIndex(gCharIndex, llGetSubString(str, 3, 3)) );
    vector GridPos3 = GetGridPos( llSubStringIndex(gCharIndex, llGetSubString(str, 4, 4)),
                                  llSubStringIndex(gCharIndex, llGetSubString(str, 5, 5)) );
    vector GridPos4 = GetGridPos( llSubStringIndex(gCharIndex, llGetSubString(str, 6, 6)),
                                  llSubStringIndex(gCharIndex, llGetSubString(str, 7, 7)) );
    vector GridPos5 = GetGridPos( llSubStringIndex(gCharIndex, llGetSubString(str, 8, 8)),
                                  llSubStringIndex(gCharIndex, llGetSubString(str, 9, 9)) );
    vector GridPos6 = GetGridPos( llSubStringIndex(gCharIndex, llGetSubString(str, 10, 10)),
                                  llSubStringIndex(gCharIndex, llGetSubString(str, 11, 11)) );
    vector GridPos7 = GetGridPos( llSubStringIndex(gCharIndex, llGetSubString(str, 12, 12)),
                                  llSubStringIndex(gCharIndex, llGetSubString(str, 13, 13)) );
    vector GridPos8 = GetGridPos( llSubStringIndex(gCharIndex, llGetSubString(str, 14, 14)),
                                  llSubStringIndex(gCharIndex, llGetSubString(str, 15, 15)) );

    // Use these grid positions to display the correct textures/offsets.
    ShowChars(link,GridPos1, GridPos2, GridPos3, GridPos4, GridPos5, GridPos6, GridPos7, GridPos8);
}

RenderExtended(integer link, string str) {
    // Look for escape sequences.
    list Parsed       = llParseString2List(str, [], (list)ESCAPE_SEQUENCE);
    integer ParsedLen = llGetListLength(Parsed);

    // Create a list of index values to work with.
    list Indices;
    // We start with room for 16 indices.
    integer IndicesLeft = 16;

    string Token;
    integer Clipped;
    integer LastWasEscapeSequence = FALSE;
    // Work from left to right.
    integer i=0;
    for (; i < ParsedLen && IndicesLeft > 0; ++i) {
        Token = llList2String(Parsed, i);

        // If this is an escape sequence, just set the flag and move on.
        if (Token == ESCAPE_SEQUENCE) {
            LastWasEscapeSequence = TRUE;
        }
        else { // Token != ESCAPE_SEQUENCE
            // Otherwise this is a normal token.  Check its length.
            Clipped = FALSE;
            integer TokenLength = llStringLength(Token);
            // Clip if necessary.
            if (TokenLength > IndicesLeft) {
                TokenLength = llStringLength(Token = llGetSubString(Token, 0, IndicesLeft - 1));
                IndicesLeft = 0;
                Clipped = TRUE;
            }
            else
                IndicesLeft -= TokenLength;

            // Was the previous token an escape sequence?
            if (LastWasEscapeSequence) {
                // Yes, the first character is an escape character, the rest are normal.
                // This is the extended character.
                Indices += [llSubStringIndex(EXTENDED_INDEX, llGetSubString(Token, 0, 0)) + 95];

                // These are the normal characters.
                integer j=1;
                for (; j < TokenLength; ++j)
                {
                    Indices += [llSubStringIndex(gCharIndex, llGetSubString(Token, j, j))];
                }
            }
            else { // Normal string.
                // Just add the characters normally.
                integer j=0;
                for (; j < TokenLength; ++j)
                {
                    Indices += [llSubStringIndex(gCharIndex, llGetSubString(Token, j, j))];
                }
            }

            // Unset this flag, since this was not an escape sequence.
            LastWasEscapeSequence = FALSE;
        }
    }

    // Use the indices to create grid positions.
    vector GridPos1 = GetGridPos( llList2Integer(Indices, 0), llList2Integer(Indices, 1) );
    vector GridPos2 = GetGridPos( llList2Integer(Indices, 2), llList2Integer(Indices, 3) );
    vector GridPos3 = GetGridPos( llList2Integer(Indices, 4), llList2Integer(Indices, 5) );
    vector GridPos4 = GetGridPos( llList2Integer(Indices, 6), llList2Integer(Indices, 7) );
    vector GridPos5 = GetGridPos( llList2Integer(Indices, 8), llList2Integer(Indices, 9) );
    vector GridPos6 = GetGridPos( llList2Integer(Indices, 10), llList2Integer(Indices, 11) );
    vector GridPos7 = GetGridPos( llList2Integer(Indices, 12), llList2Integer(Indices, 13) );
    vector GridPos8 = GetGridPos( llList2Integer(Indices, 14), llList2Integer(Indices, 15) );

    // Use these grid positions to display the correct textures/offsets.
    ShowChars(link,GridPos1, GridPos2, GridPos3, GridPos4, GridPos5, GridPos6, GridPos7, GridPos8);
}

integer ConvertIndex(integer index) {
    // This converts from an ASCII based index to our indexing scheme.
    if (index >= 32) // ' ' or higher
        index -= 32;
    else { // index < 32
        // Quick bounds check.
        if (index > 15)
            index = 15;

        index += 94; // extended characters
    }

    return index;
}

default {
    state_entry()
    {
        // Initialize the character index.
        ResetCharIndex();
        llMessageLinked(LINK_THIS, REGISTER_SLAVE, llGetScriptName() , NULL_KEY);
    }

   on_rez(integer num)
   {
      llResetScript();
   }

    link_message(integer sender, integer channel, string data, key id) {
        if (channel == SLAVE_RECOGNIZED)
        {
            if (data == llGetScriptName())
            {
                gActive=TRUE;
            }
            return;
        }

        else if (channel == SLAVE_DISPLAY)
        {
            if (!gActive)
                return;

            list params=llCSV2List((string)id);
            if (llList2String(params, 1) != llGetScriptName())
                return;


            RenderString(llList2Integer(params, 0),data);
            return;
        }

       else if (channel == SLAVE_DISPLAY_EXTENDED)
       {
            if (!gActive)
                return;

            list params=llCSV2List((string)id);
            if (llList2String(params, 1) != llGetScriptName())
                return;

            RenderExtended(llList2Integer(params, 0),data);
    }
        else if (channel == REMAP_INDICES) {
            // Parse the message, splitting it up into index values.
            list Parsed = llCSV2List(data);
            integer i;
            // Go through the list and swap each pair of indices.
            for (i = 0; i < llGetListLength(Parsed); i += 2) {
                integer Index1 = ConvertIndex( llList2Integer(Parsed, i) );
                integer Index2 = ConvertIndex( llList2Integer(Parsed, i + 1) );

                // Swap these index values.
                string Value1 = llGetSubString(gCharIndex, Index1, Index1);
                string Value2 = llGetSubString(gCharIndex, Index2, Index2);

                gCharIndex = llDeleteSubString(gCharIndex, Index1, Index1);
                gCharIndex = llInsertString(gCharIndex, Index1, Value2);

                gCharIndex = llDeleteSubString(gCharIndex, Index2, Index2);
                gCharIndex = llInsertString(gCharIndex, Index2, Value1);
            }
            return;
        }
        else if (channel == RESET_INDICES) {
            // Restore the character index back to default settings.
            ResetCharIndex();
            return;
        }
       else if (channel == SLAVE_RESET)
        {
            ResetCharIndex();
            gActive=FALSE;
            llMessageLinked(LINK_THIS, REGISTER_SLAVE, llGetScriptName() , NULL_KEY);
        }
    }
}
```

## 16-Char MESH Prim Setup

```lsl
//There really isn't a Prim Setup for these
//You can get a full perm 8 face plane mesh here for L$10
//https://marketplace.secondlife.com/p/Mesh-8-Faces-8x1/3014457 [1]
// Or for completely FREE here
//https://marketplace.secondlife.com/p/FREE-8-faced-mesh-prim-xytext-v2-16-characters-per-half-a-prim/3312172 [2]
```

8x1, high LOD, land impact 0.5: [https://marketplace.secondlife.com/p/Free-full-perm-8-face-mesh-panel/4172861](https://marketplace.secondlife.com/p/Free-full-perm-8-face-mesh-panel/4172861)

[https://marketplace.secondlife.com/p/Mesh-8-Faces-8x1/3014457](https://marketplace.secondlife.com/p/Mesh-8-Faces-8x1/3014457)

[https://marketplace.secondlife.com/p/FREE-8-faced-mesh-prim-xytext-v2-16-characters-per-half-a-prim/3312172](https://marketplace.secondlife.com/p/FREE-8-faced-mesh-prim-xytext-v2-16-characters-per-half-a-prim/3312172)