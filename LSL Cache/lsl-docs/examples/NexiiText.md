---
name: "NexiiText"
category: "example"
type: "example"
language: "LSL"
description: "The idea of this text renderer is to be easy, compact, efficient and fast performing. It uses a simple design where the system is initialised txtInit(). A board selected txtSelect(\"My-Fav-Board\") a..."
wiki_url: "https://wiki.secondlife.com/wiki/NexiiText"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 Non-License
- 2 Intro

  - 2.1 Note on Colour
- 3 Text Prim
- 4 Fonts

  - 4.1 Colours
- 5 Core
- 6 Advanced
- 7 Abstract
- 8 Complete Script

## Non-License

```lsl
//===================================================//
//                    NexiiText.8                    //
//       "14 September 2011", "23:19:00 GMT-0"       //
//                  By Nexii Malthus                 //
//                   Public Domain                   //
//===================================================//
```

## Intro

The idea of this text renderer is to be easy, compact, efficient and fast performing.
It uses a simple design where the system is initialised txtInit().
A board selected txtSelect("My-Fav-Board") and instructions pushed through txtPush("Text on my fav board!",Colour,Font).

It gives you a ton of control in how every single character can be rendered, switching colours and texture as you go.
You can always just push through a single massive string though Text("Board","Text",Colour,Font). It adapts to you.

### Note on Colour

It makes more sense for a rotation type to transport colours in a compact format (rotation RGBA), rather than multiple vars (vector RGB + float Alpha).

The compact format is <Red [0,1], Green [0,1], Blue [0,1], Alpha [0,1]>



## Text Prim

```lsl
default {
    state_entry() {
        llSetPrimitiveParams([
            PRIM_TYPE,
                PRIM_TYPE_PRISM,
                PRIM_HOLE_SQUARE,
                <0.199, 0.8, 0>,
                0.306,
                <0, 0, 0>,
                <1, 1, 0>,
                <0, 0, 0>,
            PRIM_SIZE,
                <0.01, 0.58, 0.18>,
            PRIM_TEXTURE,
                ALL_SIDES,
                "180d23df-62b6-8608-0535-03413ddf3805",
                <1, 1, 0>,
                <0, 0, 0>,
                0.0
        ]);
    }
}
```

## Fonts

```lsl
    // Fonts, 10x10 grid.
key Normal          = "0967db80-5132-d6dc-f37c-4f9cc1196983";// Normal Font
key Bold            = "48de7a07-1641-3d26-2bca-9773a20d2adf";// Be Bold!
key Lined           = "35399d2f-e35f-5100-179a-f3a119b1cdf7";// URLy Underline!
key Italic          = "1bb8a1f9-87cb-4946-afc6-b1856bc9b752";// Iffy Italics!
key Stroked         = "a2d5149e-d018-3ddd-202d-3432605c8084";// Edgy Edge!
key Shadowed        = "347ff828-9cef-31e5-a792-1bfdd2a1cea0";// Silly Shadow!

    // These are the printable characters:
string txtChars     = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~";

    // Icons
  // Icons are stretched two glyphs long compared to fonts
  // for optimal sharpness and occupy two prim faces as a result.
key Icon            = "db7db103-0994-c55e-9740-6fb43e4f1dc9";
```

### Colours

Here's an extra snippet for use alongside, instead of writing down the colours all the time. For quick reference and convenience.

```lsl
rotation White  = <.99,.99,.99, 1.0>;
rotation Black  = <.00,.00,.00, 1.0>;
rotation Red    = <.99,.00,.00, 1.0>;
rotation Green  = <.00,.99,.50, 1.0>;
rotation Blue   = <.00,.40,.90, 1.0>;
rotation Orange = <.99,.50,.00, 1.0>;
rotation LSL    = <.00,.99,.50, 1.0>;
rotation URL    = <.20,.40,.70, 1.0>;
```

## Core

You do not to use these directly, just in the same LSL script.
See Abstracts and Advanced for simplifying use of this library.

```lsl
    // Global stack
list txtBoards;// Format is [str Board: "A", int Prims: 8, int txtLinks Pointer: 0];
list txtLinks;// Format is [2,3,4,5,6,7,8,9]; (All link numbers)

    // Internal stack
integer txtBoard;
integer txtPtr;

    // Initializes Text Render system by searching all boards.
txtInit() {
    integer Prim = 1; integer Prims = llGetNumberOfPrims();
    for(; Prim <= Prims; ++Prim ) { string Name = llGetLinkName(Prim);
        if(llGetSubString(Name,0,4) == "ntxt.") {
            list t = llParseString2List(Name,["."],[]);
            string B = llList2String(t,1);
            integer i = llListFindList(txtBoards,[B]);
            if(!~i) {
                integer x; integer y; list z; @again; y = Linked("ntxt."+B+"."+(string)x);
                if(y) { z += y; x++; jump again; }
                txtBoards += [B,x,llGetListLength(txtLinks)]; txtLinks += z;
}   }   }   }

    // Helps return the needed prim params for a single prim face.
list txtFace( integer Face, string Char, rotation Color, key Texture, integer Index ) {
    integer i = llSubStringIndex(txtChars,Char);
    float W = 1.0;// Glyph Width
    float H = 1.0;// Glyph Height
    float X = 0.0;// Glyph X Offset

    ////
    // Special Cases

        // For dual-width glyphs (Icon)
    if(Index == -1) X = -.05; else if(Index == 1) X = .05;

        // Adjust glyph sizes to taste.
    if(Texture == Normal ) { W = .6; H = .98; } else
    if(Texture == Bold) { W = .6; H = .98; } else
    if(Texture == Lined) { W = .6; H = .98; } else
    if(Texture == Italic) { W = .7; H = .98; } else
    if(Texture == Stroked) { W = .7; H = .98; } else
    if(Texture == Shadowed) { W = .6; H = .98; } else
    if(Texture == Icon ) { W = .475; H = .98; }
    if(Char == "W") W = .8;

    // Special Cases
    ////

    list Out;
    if(Face == 0) Out =
        [PRIM_TEXTURE, 3, Texture, <.25*W,.1*H,0>, <((-.45+.1*(i%10)) + (.0745*W)) + (X*W), .45-(.1*(i/10)), 0>, 0,
         PRIM_COLOR, 3, , Color.s];
    else if(Face == 1) Out =
        [PRIM_TEXTURE, 7, Texture,<.1*W,.1*H,0>, <((-.45+.1*(i%10))) + (X*W), .45-(.1*(i/10)), 0>, .0,
         PRIM_COLOR, 7, , Color.s];
    else if(Face == 2) {
        float x = ((-.45+.1*(i%10)) - (.69*W)) + (X*W);
        if(x < -1) x = 2 + x;
        Out = [PRIM_TEXTURE, 4, Texture, <-1.635*W,.1*H,0>, , .0,
                PRIM_COLOR, 4, , Color.s];
    } else if(Face == 3) Out =
        [PRIM_TEXTURE, 6, Texture, <.1*W,.1*H,0>, <((-.45+.1*(i%10))) + (X*W), .45-(.1*(i/10)), 0>, .0,
         PRIM_COLOR, 6, , Color.s];
    else /*Face == 4*/ Out =
        [PRIM_TEXTURE, 1, Texture, <.25*W,.1*H,0>, <((-.45+.1*(i%10)) - (.0745*W)) + (X*W), .45-(.1*(i/10)), 0>, .0,
         PRIM_COLOR, 1, , Color.s];
    return Out;
}
```

## Advanced

```lsl
    // Begin text rendering, we select a board first.
TextSelect(string Board) {
    if(txtBoards == []) txtInit();
    txtBoard = llListFindList(txtBoards,[Board]);
    txtPtr = 0;
}

    // With board selected, we can push individual strings to be rendered with colour and texture.
TextPush(string Text, rotation Colour, key Texture) {
    integer BoardsLen = llList2Integer(txtBoards,txtBoard+1)*5;
    integer LinksPtr = llList2Integer(txtBoards,txtBoard+2);
    integer x; integer y = llStringLength(Text); if(y+txtPtr > BoardsLen) y = BoardsLen-1;
    while(x,Normal);
    }
}
```

## Abstract

```lsl
    // For ease of use, select board, input text, colour and font. Also fills the end.
Text(string Board, string Text, rotation Colour, key Texture) {
    TextSelect(Board);
    TextPush(Text,Colour,Texture);
    TextFill();
}

    // If you want to clear a board, such as on a reset, you can use this.
TextClear(string Board) {
    TextSelect(Board);
    TextFill();
}
```



## Complete Script

```lsl
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Lib.Linkset

// These are some helper functions for identifying linked prims by name.

    // Searches for Needle(s) and returns a list of link number(s).
list LinkedList( string Needle ) {
    list Needles; integer Hay = 1; integer Stacks = llGetNumberOfPrims();
    for(; Hay <= Stacks; ++Hay ) if(llGetLinkName(Hay) == Needle) Needles += Hay;
return Needles; }

    // Searches for single Needle prim and returns a link number.
integer Linked( string Needle ) {
    integer Prims = llGetNumberOfPrims()+1;
    while(--Prims) if(llGetLinkName(Prims) == Needle) return Prims;
return 0; }

    // Searches & Replaces Needle(s) with link numbers and returns modified list.
list ListLinked( list Needles ) {
    integer Prims = llGetNumberOfPrims()+1;
    while(--Prims) {
        integer Ptr = llListFindList(Needles,[llGetLinkName(Prims)]);
        if(~Ptr) Needles = llListReplaceList(Needles,[Prims],Ptr,Ptr);
} return Needles; }

// Lib.Linkset
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Lib.NexiiText

// by Nexii Malthus, released into Public Domain.

// The idea of this text renderer is to be easy, compact, efficient and fast performing.
// It uses a simple design where the system is initialised txtInit().
// A board selected txtSelect("My Fav Board") and instructions pushed through txtPush("My Fav board!,Colour,Font).
// It gives you a ton of control in how every single character can be rendered, switching colours and texture as you go.
// You can always just push through a single massive string though txt("Board","Text",Colour,Font). It adapts to you.

//// Note on Colour
// It makes more sense for a rotation type to transport colours in a compact format, rather than multiple vars.
// The compact format is  (w/ Range Notation)

    // Fonts, 10x10 grid.
key Normal          = "0967db80-5132-d6dc-f37c-4f9cc1196983";// Normal Font
key Bold            = "48de7a07-1641-3d26-2bca-9773a20d2adf";// Be Bold!
key Lined           = "35399d2f-e35f-5100-179a-f3a119b1cdf7";// URLy Underline!
key Italic          = "1bb8a1f9-87cb-4946-afc6-b1856bc9b752";// Iffy Italics!
key Stroked         = "a2d5149e-d018-3ddd-202d-3432605c8084";// Edgy Edge!
key Shadowed        = "347ff828-9cef-31e5-a792-1bfdd2a1cea0";// Silly Shadow!

    // These are the printable characters:
string txtChars     = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~";

    // Icons
  // Icons are stretched two glyphs long compared to fonts
  // for optimal sharpness and occupy two prim faces as a result.
key Icon            = "db7db103-0994-c55e-9740-6fb43e4f1dc9";

    // These are the printable icons:  (Ordered with character and representation)
/*//  Empty             ! ->                " >                 # Home              $ (i)
    % (?)               & L$                ' RSS Feed          ( Ext. Link         ) Avatar
    * General           + Mature            , Adult             - Headshot          . C7 (Gun)
    / Forboda (Gun)     0 Explosion         1 Knife
/*/

//////////////////////////////
// Public Functions

///////////////
// Simple text rendering vv

    // For ease of use, select board, input text, colour and font. Also fills the end.
Text(string Board, string Text, rotation Colour, key Texture) {
    TextSelect(Board);
    TextPush(Text,Colour,Texture);
    TextFill();
}

    // If you want to clear a board, such as on a reset, you can use this.
TextClear(string Board) {
    TextSelect(Board);
    TextFill();
}

// Simple text rendering ^^
///////////////

///////////////
// Advanced Text Rendering

    // Begin text rendering, we select a board first.
TextSelect(string Board) {
    if(txtBoards == []) txtInit();
    txtBoard = llListFindList(txtBoards,[Board]);
    txtPtr = 0;
}

    // With board selected, we can push individual strings to be rendered with colour and texture.
TextPush(string Text, rotation Colour, key Texture) {
    integer BoardsLen = llList2Integer(txtBoards,txtBoard+1)*5;
    integer LinksPtr = llList2Integer(txtBoards,txtBoard+2);
    integer x; integer y = llStringLength(Text); if(y+txtPtr > BoardsLen) y = BoardsLen-1;
    while(x BoardsLen) y = (BoardsLen-1)/2;
    while(x,Normal);
    }
}

// Advanced text rendering ^^
///////////////

// Public Functions
//////////////////////////////

//////////////////////////////
// Raw Library stuff
// Don't touch unless you know what your doing.

    // Global stack
list txtBoards;// Format is [str Board: "A", int Prims: 8, int txtLinks Pointer: 0];
list txtLinks;// Format is [2,3,4,5,6,7,8,9]; (All link numbers)

    // Internal stack
integer txtBoard;
integer txtPtr;

    // Initializes Text Render system by searching all boards.
txtInit() {
    integer Prim = 1; integer Prims = llGetNumberOfPrims();
    for(; Prim <= Prims; ++Prim ) { string Name = llGetLinkName(Prim);
        if(llGetSubString(Name,0,4) == "ntxt.") {
            list t = llParseString2List(Name,["."],[]);
            string B = llList2String(t,1);
            integer i = llListFindList(txtBoards,[B]);
            if(!~i) {
                integer x; integer y; list z; @again; y = Linked("ntxt."+B+"."+(string)x);
                if(y) { z += y; x++; jump again; }
                txtBoards += [B,x,llGetListLength(txtLinks)]; txtLinks += z;
}   }   }   }

    // Helps return the needed prim params for a single prim face.
list txtFace( integer Face, string Char, rotation Color, key Texture, integer Index ) {
    integer i = llSubStringIndex(txtChars,Char);
    float W = 1.0;// Glyph Width
    float H = 1.0;// Glyph Height
    float X = 0.0;// Glyph X Offset

    ////
    // Special Cases

        // For dual-width glyphs (Icon)
    if(Index == -1) X = -.05; else if(Index == 1) X = .05;

        // Adjust glyph sizes to taste.
    if(Texture == Normal ) { W = .6; H = .98; } else
    if(Texture == Bold) { W = .6; H = .98; } else
    if(Texture == Lined) { W = .6; H = .98; } else
    if(Texture == Italic) { W = .7; H = .98; } else
    if(Texture == Stroked) { W = .7; H = .98; } else
    if(Texture == Shadowed) { W = .6; H = .98; } else
    if(Texture == Icon ) { W = .475; H = .98; }
    if(Char == "W") W = .8;

    // Special Cases
    ////

    list Out;
    if(Face == 0) Out =
        [PRIM_TEXTURE, 3, Texture, <.25*W,.1*H,0>, <((-.45+.1*(i%10)) + (.0745*W)) + (X*W), .45-(.1*(i/10)), 0>, 0,
         PRIM_COLOR, 3, , Color.s];
    else if(Face == 1) Out =
        [PRIM_TEXTURE, 7, Texture,<.1*W,.1*H,0>, <((-.45+.1*(i%10))) + (X*W), .45-(.1*(i/10)), 0>, .0,
         PRIM_COLOR, 7, , Color.s];
    else if(Face == 2) {
        float x = ((-.45+.1*(i%10)) - (.69*W)) + (X*W);
        if(x < -1) x = 2 + x;
        Out = [PRIM_TEXTURE, 4, Texture, <-1.635*W,.1*H,0>, , .0,
                PRIM_COLOR, 4, , Color.s];
    } else if(Face == 3) Out =
        [PRIM_TEXTURE, 6, Texture, <.1*W,.1*H,0>, <((-.45+.1*(i%10))) + (X*W), .45-(.1*(i/10)), 0>, .0,
         PRIM_COLOR, 6, , Color.s];
    else /*Face == 4*/ Out =
        [PRIM_TEXTURE, 1, Texture, <.25*W,.1*H,0>, <((-.45+.1*(i%10)) - (.0745*W)) + (X*W), .45-(.1*(i/10)), 0>, .0,
         PRIM_COLOR, 1, , Color.s];
    return Out;
}
// Raw Library stuff
//////////////////////////////

// Lib.NexiiText
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

///////////////////
// Font Colours!
// Didn't want to keep rewriting them.
rotation White  = <.99,.99,.99, 1.0>;
rotation Black  = <.00,.00,.00, 1.0>;
rotation Red    = <.99,.00,.00, 1.0>;
rotation Green  = <.00,.99,.50, 1.0>;
rotation Blue   = <.00,.40,.90, 1.0>;
rotation Orange = <.99,.50,.00, 1.0>;
rotation LSL    = <.00,.99,.50, 1.0>;
rotation URL    = <.20,.40,.70, 1.0>;
///////////////////

///////////////////
// Example Code
default {
    state_entry() {



        // Example 1
        // The simplest way is to use the one-shot Text(..) function
        Text("Board 1", "NexiiText.7", LSL, Bold);




        ////
        // Example 2

        // More advanced is to render string by string. Which allows rich text.

        // We select a board
        TextSelect("Board 2");

        // Then push strings to render, in different colours and fonts.
        TextPush("OpenSource. ", Orange, Stroked);
        TextPush("By ", White, Normal);
        TextPush("Nexii", White, Italic);

        // If we didn't fill the end, a previous render
        // could have left junk text in the final visual.
        TextFill();

        // Example 2
        ////






        ////
        // Example 3

        // We can also render font textures in brilliant ways, such as icons.

        TextSelect("Board 3");
        TextPush("Nexii ",Blue,Normal);
        TextIcon(".",White,Icon);
        TextPush(" XyText",Red,Normal);
        TextFill();

        // Example 3
        ////



        ////
        // Example 4
        llSetTimerEvent(.98);
    }

    timer() {
        string Time = llGetTimestamp();
               Time = llGetSubString(Time, 11,18);
        TextSelect("Time");
        TextPush(Time, White, Normal);
        TextFill();
        // Example 4
        ////
    }
}//////////////////
```