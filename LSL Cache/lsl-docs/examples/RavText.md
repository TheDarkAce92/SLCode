---
name: "RavText"
category: "example"
type: "example"
language: "LSL"
description: "RavText A lightweight, multi font, text-on-a-prim display system Version 1.0(3)"
wiki_url: "https://wiki.secondlife.com/wiki/RavText"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

RavText
A lightweight, multi font, text-on-a-prim display system
Version 1.0(3)

License:  This is licensed under the terms of the Lesser GPL (LGPL).

This is yet another 10 character display using a 5 faced prim. It does not, however, use any part of the popular XyText series of scripts.  It is 100% home grown.  It is meant for specialized usage: specifically when one desires a very lightweight script for displaying 10 character basic alphanumeric text.  While it could be expanded to accommodate more characters rather easily, at the moment it just does uppercase alphanumeric plus a few special characters.

The functionality of RavText is limited compared to other text systems, but does have some advantages.  it is definitely not suitable for every application.  Here are the advantages and drawbacks of RavText compared to other systems:

DISADVANTAGES:

1. Limited character set.  Uppercase alphanumeric characters and a few special characters (namely " !@#$%&()") are supported.  (However, it could easily be expanded to use larger character sets with a few minor modifications and the right texture maps).

2. Lack of special effects or a robust display system.  There are no fade in / fade out effects or any sort of color control, although there is nothing preventing someone from adding them.

3. Currently, the textures can give an annoying flicker under some circumstances when viewed at certain angles on certain displays.

4. Needs some manual configuration when using more than one 5 prim display.  There is no link scanner or any other utility built in.  Individual prims must have their own script and that script must be preconfigured by hand (although it does not take much effort to do so).

5. Not very well commented or documented.  Meh, I'm lazy.

ADVANTAGES:

1. Very lightweight & efficient.  The script is relatively simple, and fast.  It attempts to keep CPU usage to a minimum.

2. "Rezzes" faster.  Partly because of the limited character set, RavText only uses 8 textures per character map, as opposed to the 60+ textures used by XyText derivitives. This tends to result in textures rezzing much faster, and staying in the cache more frequently.  NOTE:  If RavText supported 128 characters instead of the current 45, it would require 64 textures.  This is one of the main reasons I decided to go with uppercase only. I wanted quick rendering basic text.

3. Flexible.  While this version is configured for the standard 5 face configuration, it can be modified to accommodate almost any primface configuration by just editing a few lists.

3. Supports multiple fonts.  Due to the low number of textures required to map the limited RavText character set, it was easy to generate additional display fonts.  Currently, there are 6 possible fonts.

BASIC CONFIGURATION AND CONCEPTS:

RavText uses the variables "panelnum"  and "subpanel" to tell it where it is in your display system.  Each panel is considered to be its own unit and is composed of subpanels. For example, if you wanted to have two blocks of text, each 20 characters long, you would have two panels, each with two subpanels.  Subpanels should be numbered left to right starting with 0.  So text block #1 would be panel 0, with subpanel 0 and 1.  text block 2 would be panel 1, with subpanels 0 and 1 as well.

To set the text on a specific panel, you set the key attribute of a linked message to be "7A", set the string attribute to be whatever string you want to display.  You would set the number to be 2 raised to the power of the panel number.  You can use -1 to display on all panels.

To change the font, set the key attribute of the link message to be "7F", set the integer value to be 2 raised to the panel number (or -1 for all panels) and the string to be the font number you want to use (fonts are numbered 0 to 5).



BASIC USAGE:

1. Make a 5 face prim, just like the ones used with current XyText versions. Instructions detailed below.

2. Put the RavText script in the prim.

3. To display text, send a link message to the prim thusly:

```lsl
llMessageLinked(LINK_SET, -1, "TEST MSG!", "7A");
```

The value "7A" is the command to display a string of text.  The value -1 basically means all panels.

OK, next lets make a two panel display.  It will display up to 20 characters.

1. make two 5 faced prims. Instructions for a 5 faced prim that works for this are given below.

2. Put RavText scripts in each prim

3. Set the subpanel variable on the rightmost display prim to be 1.  Leave the other subpanel value at 0.

4. Once again, send the link message:

```lsl
llMessageLinked(LINK_SET, -1, "TEST MSG! EXPANDED!", "7A");
```

To change the font, send the following link message:

```lsl
llMessageLinked(LINK_SET, -1, "3", "7F");
```

There are a lot more examples I could give, but for now I will leave it as is.  I will try to update this page as I can.

AND NOW, THE CODE:

```lsl
// RavText
// Version 1.0(3)
// Created 2008-09-18
// A lightweight 10 char / prim text generation system with multiple font support
// Created by Ravenous Dingo
// Copyright 2008 owned by the person controlling the Second Life avatar named Ravenous Dingo
// This code is hereby released under the terms of the LGPL (Lesser GPL) license
// Associated textures are hereby released to the public domain

float panelnum=0.; // Panels are groups of prims that work as one block of text

integer subpanel=0; // sub panel is the position within the panel block

integer default_font=0;

list fontmap=[

                ];

list corner_map=[
                    <-0.4225, 0.4675, 0>,
                    <-0.4675, 0.4675, 0>,
                    <-0.807, 0.4675, 0>,
                    <-0.4675, 0.4675, 0>,
                    <-0.515, 0.4675, 0>
                    ];
list rep_map=[
                <0.1525, 0.0625, 0>,
                <0.0625, 0.0625, 0>,
                <-1.0, 0.0625, 0>,
                <0.0625, 0.0625, 0>,
                <0.155, 0.0625, 0>
                ];

list face_map=[ 3, 7, 4, 6, 1 ];

list cur_texmap=[];

integer numfaces=0;

integer start_idx=0;

string alphamap=" 1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%&()";

integer bitmask=0;
key kravtext_cmd="7A";
key ksetfont_cmd="7F";

vector base_offset=<-0.4675, 0.4675, 0>;
float increment=0.0625;

integer mod=0;
integer curfont=-1;
list param=[];

integer indexAlpha(string str)
{
    integer idx=llSubStringIndex(alphamap, str);
    if (idx == -1)
    {
        idx=0;
    }
    return idx;
}

init()
{
    composeFonts();
    mod=llStringLength(alphamap);
    numfaces=llGetListLength(face_map);
    bitmask=llRound(llPow(2.,panelnum));
    start_idx=subpanel * numfaces * 2;
    loadFont(default_font);
}

loadFont(integer fontnum)
{
    if (fontnum == curfont)
    {
        return;
    }
    list tmp_font=llList2List(fontmap, fontnum * 8, (fontnum * 8) + 7);

    integer i=0;
    string tfont="";
    integer tfnum=0;
    integer tidx=0;
    if (llGetListLength(param) != 0)
    {
        for (i=0; i < numfaces; i++)
        {
            tidx=(i * 6) + 2;
            tfont=llList2String(param, tidx);
            // now find the font index;
            tfnum=llListFindList(cur_texmap, [tfont]);
            // get the new font
            tfont=llList2String(tmp_font, tfnum);
            // and replace it
            param=llListReplaceList(param,  [tfont], tidx, tidx);
        }
    }
    curfont=fontnum;
    cur_texmap=tmp_font;
    llSetPrimitiveParams(param);
}

composeFonts()
{
    list sysfixed=[
                "df574f09-061c-d3fe-07eb-3d0008271bc4",
                "ace8bde9-b93e-d667-c03c-45ce826c955d",
                "f7c99d89-ff0b-059e-3e3b-625d71799f19",
                "eb3e7fea-60f6-6335-a7da-5d0e7dbed0bf",
                "627a4675-4db8-f473-b16a-27aeb42e2b6f",
                "aa14726b-fab8-7802-cc23-f118455f4354",
                "d7808242-a2da-e144-3338-6b005671e6e6",
                "60d062d7-b60f-220d-f9dd-189596a796d2"
                ];

    list OCR_A=[
                "6d788259-709e-cc72-98b4-4ec56986a958",
                "c74622f7-5740-1e5f-2a64-69060bf2742e",
                "ffa88837-7f13-dbb3-e28c-2e969b9b4737",
                "9127b5d8-459f-7d2c-2b3b-2b6c740de94a",
                "894d4fc7-6c3c-954c-e7c9-94c687a1ac62",
                "f529f498-be68-f5bd-2464-34e5bb4a8cdb",
                "b645eb2c-57eb-a420-afbe-cba49bd298d8",
                "bf8541e1-d875-96a6-adc3-fbdd38c41f2a"
                ];

    list profont=[
                "9e83c094-58b1-8375-192f-2e0ef0f06d91",
                "fcd34765-3c58-c1df-2c5e-5e96d1491c0c",
                "fd232e50-9ed5-3cc0-345e-b08154b9bf97",
                "10c5ab5f-49cb-ff40-3023-029caa4a4ff1",
                "2956334f-79f3-010b-9be7-fc4811d2adae",
                "b0277b5b-dfbf-27c3-47c9-3a120881fe64",
                "969a1eb3-acbf-8425-1ddd-4f6a81bdbd58",
                "409d587d-a374-4a1b-16d5-9c19a9baf83a"
                ];
    list cour_new=[
                "e60aa9ab-7f1c-33ec-3408-37c20cce3c76",
                "93eb9bef-dafa-9980-5d25-5adb5614ccc3",
                "dd584fae-63e2-6f50-4811-a5b14989020a",
                "cf4c4265-64a9-fa64-b18e-47c11fc18aa2",
                "1c63839f-ebfa-c9e9-2391-98faa059c7a3",
                "533279c5-cd44-daa4-b010-cd7c99e48c72",
                "c1731907-6627-7463-2cff-dfa4499559bb",
                "88e2bd5c-5c6f-6103-c2fb-db958e31d026"
                ];
    list bs_vera=[
                "f88d322e-2f8d-c5d9-544c-293e0c5647c1",
                "91546531-86b9-87ec-3dec-2072ebb012ad",
                "1a545d8d-f14f-32aa-ad96-1abca948a662",
                "d78fa62c-301d-fa10-188a-ee5f6ad87777",
                "69e53076-8083-975b-31c0-420f1f5658dc",
                "1b5ffc88-96e6-03c0-39c0-e38a6fad981a",
                "a1511389-1b45-b7fb-1961-fd02ee57e26d",
                "474e449e-f2f3-d5ac-1c63-1be922b3b434"
                ];
    list sheldon=[
                "2958c0ac-cba6-a02b-da3e-aec050e3714f",
                "cb8faeb7-c87e-c57c-448a-53a718adb3c8",
                "572ff18e-d319-6213-ca28-202aeb7dc2e8",
                "0bfc28e2-788d-035d-1ac1-ce752d90f89c",
                "1fe4af1d-d99b-fe28-fba8-0006527c4c5f",
                "f7fb5f59-0275-3ee7-9b54-e9a1ae61b76c",
                "5e52d02e-edae-bf73-da61-9e1fe4e1801b",
                "ff54400e-050c-7f87-cefd-a396c86d24d6"
                ];
    fontmap=sysfixed + OCR_A + profont + cour_new + bs_vera + sheldon;
}

default
{
    state_entry()
    {
        init();
    }

    link_message(integer sender, integer num, string msg, key id)
    {
        if ((id == kravtext_cmd) && (num & bitmask))
        {
            param=[]; // create our primitive param list
            msg=llToUpper(msg); // make everything upper case
            integer i=0;
            integer this_idx=0;
            integer frame=0;
            integer tnum=0;
            integer xinc=0;
            integer yinc=0;
            integer fx=0;
            integer fy=0;
            float xpos=0.;
            float ypos=0.;

            integer thisface=0;
            string thistex=NULL_KEY;
            vector this_rep=<0.,0.,0.>;
            for (i=0; i < numfaces; i++)
            {
                this_idx = start_idx + (i * 2);
                frame = ( mod * indexAlpha( llGetSubString( msg, this_idx, this_idx ) ) )
                        + indexAlpha( llGetSubString( msg, this_idx+ 1, this_idx +1 ) );
                base_offset=llList2Vector(corner_map, i);
                this_rep=llList2Vector(rep_map, i);
                thisface=llList2Integer(face_map, i);
                xinc = frame % 32;
                yinc = frame / 32;
                fx = xinc / 16;
                fy = yinc / 16;
                tnum=(fy * 2) + fx;
                thistex=llList2String(cur_texmap, tnum);
                xinc = xinc - ( 16 * fx );
                yinc = yinc - ( 16 * fy );
                xpos=base_offset.x + (increment * (float)xinc);
                ypos=base_offset.y - (increment * (float)yinc);

                param += [
                            PRIM_TEXTURE,
                            thisface,
                            thistex,
                            this_rep,
                            ,
                            0.
                            ];
            }
            llSetPrimitiveParams(param);
        }
        else if ((id == ksetfont_cmd) && (num & bitmask))
        {
            integer fnum=(integer)msg;
            loadFont(fnum);
        }
    }
}
```

Because everyone seems to have a slightly different set of settings for their 5 faced prim, and because we don't have the description of the exact one that was being used in the original script, I have altered the offsets in the script to match with the 5 faced prim detailed below:

1.   Rez a Prism (I used X=0.01,Y=2.5,Z=1.5. Obviously adjust to taste.)

2.   Path cut: Begin 0.2, End 0.8.

3.   Hollow 65, default shape.

4.   Twist, Taper, Top Shear are all default 0.

5.   Slice Begin and end are default 0, and 1.



RESPONSE TO NOTE: Its not the speed of rendering the text itself - its the speed at which the client renders the textures.  As I mentioned in the advantages / disadvantages, that's the man reason for using it.  The very fact that it uses fewer characters means it has a smaller texture "footprint" and renders faster overall in clients due to much fewer textures to load.  I think Jor3l Boa is confusing client rendering with script execution time.  Not an uncommon mistake, but it totally misses the entire point of this script lol.  -Rav

RESPONSE TO RESPONSE NOTE: Yes lol, about the font, is there any script to make it or some files to edit?, would be cool if we can make fonts. And yes, is faster to render but less chars, anyway is good :P (noob note removed) -Jor3l