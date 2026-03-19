---
name: "NexiiText2"
category: "example"
type: "example"
language: "LSL"
description: "Second generation of my prim text renderer. It's meant to be easy, compact, efficient and high performance. The new design utilises PRIM_LINK_TARGET and a dynamic prim allocation architecture."
wiki_url: "https://wiki.secondlife.com/wiki/NexiiText2"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 Non-License
- 2 Intro

  - 2.1 Note on Colour
  - 2.2 Note on Setup
- 3 Text Prim
- 4 Fonts
- 5 Colours
- 6 Core
- 7 Complete Script

## Non-License

```lsl
//===================================================//
//                    NexiiText.8                    //
//       "20 September 2011", "06:15:00 GMT-0"       //
//                  By Nexii Malthus                 //
//                   Public Domain                   //
//===================================================//
```

## Intro

Second generation of my prim text renderer. It's meant to be easy, compact, efficient and high performance.
The new design utilises PRIM_LINK_TARGET and a dynamic prim allocation architecture.

While you do not have the precise control of prim positioning that static text displays have, on the other hand you can very easily scale font size and create text boxes.

This library is excellent for use in the dynamic environment of HUDs. You can allocate a reserve of prims for use of the text library and use them up as you wish.
The renderer is extremely efficient in prim usage as empty areas are completely void of prims. Prims are only used where text is visible.
This also supports newlines (\n) and tabs (\t).

### Note on Colour

It makes more sense for a rotation type to transport colours in a compact format (rotation RGBA), rather than multiple vars (vector RGB + float Alpha).

The compact format is <Red [0,1], Green [0,1], Blue [0,1], Alpha [0,1]>



### Note on Setup

Your "Text" named objects need to have specific parameters to work with this script, use the following:

Use the LSL script below this note to create your Text Prim, just drop it into a prim and it'll create it automatically for you.

Also, create any prim and name it "A", that will be your cursor for positioning the text.

Overall, setup will be:

- 1. Create your root prim (name can be anything)
- 2. Create any number of "Text" named prims, to be used for writing text to
- 3. Create an "A" named prim to act as the cursor.
- 4. Link it all up, put the script in the root prim. Also might want to recolor the background black to make it easier to see the text. :)

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
        llSetObjectName("Text");
        llRemoveInventory(llGetScriptName());
    }
}
```



## Fonts

Some fonts I created.

```lsl
key Normal          = "0967db80-5132-d6dc-f37c-4f9cc1196983";// Normal Font
key Bold            = "48de7a07-1641-3d26-2bca-9773a20d2adf";// Be Bold!
key Lined           = "35399d2f-e35f-5100-179a-f3a119b1cdf7";// URLy Underline!
key Italic          = "1bb8a1f9-87cb-4946-afc6-b1856bc9b752";// Iffy Italics!
key Stroked         = "a2d5149e-d018-3ddd-202d-3432605c8084";// Edgy Edge!
key Shadowed        = "347ff828-9cef-31e5-a792-1bfdd2a1cea0";// Silly Shadow!
```

## Colours

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

```lsl
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// NexiiText2
list     TextLinkset; // Link numbers of all text prims
integer  TextPrim;    // Running pointer of above
integer  TextPrims;   // Total of text prims
list     TextRender;  // Running list of prim params, for PRIM_LINK_TARGET good-ness
integer  TextRenders; // Keeps track of how many prims have been rendered so far. So we don't stack heap.

integer  TextLength;  // Amount of chars to print out per line
vector   TextPos;     // Origin Position of text area
rotation TextRot;     // Rotation to put prims at
float    TextHeight;  // Printing height factor
integer  TextLineX;   // Printing line X position
integer  TextLineY;   // Printing line Y position

float    TextRatio = 3.2222;  // Ratio between Height:Width of a text prim
float    TextOffset = 0.57;   // Length of a character in meters
string   TextChars = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~";
```

There are five functions:

- TextInit

  - Initializes the text renderer. This must be run once on script startup in default state on state_entry. It looks for all the prims named "Text".

```lsl
TextInit() {
    integer Hay = 1; integer Stacks = llGetNumberOfPrims();
    for(; Hay <= Stacks; ++Hay ) if(llGetLinkName(Hay) == "Text") TextLinkset += Hay;
    TextPrims = llGetListLength(TextLinkset);
}
```



- TextCursor

  - Sets a location where to push text into.
  - Position is a vector of a location in the linkset. It defines the top left most corner of a text area.
  - Direction is a vector of where the text should face.
  - FontHeight is the height of text prims in meters
  - MaxCharsPerLine defines how long a line is allowed to be in characters before moving onto the next line.

```lsl
TextCursor(vector Position, vector Direction, float FontHeight, integer MaxCharsPerLine) {
    TextPos = Position;
    TextRot = llRotBetween(<1,0,0>, Direction);
    TextLength = MaxCharsPerLine;
    TextHeight = FontHeight;
    TextLineX = TextLineY = 0;
}
```

- TextPush

  - Virtually draws string characters with colour and font.
  - Text is the characters to send. Empty white space is optimised out and \n's are accepted for starting new lines.
  - Colour is 4 floats that specify  in a [0,1] range. (See Colour note above)
  - Font is a texture of a 10x10 grid of characters that are printable in the TextChars list. (See Fonts above)

```lsl
TextPush(string Text, rotation Colour, key Font) {
    integer x; integer y = llStringLength(Text);
    for(; x < y && TextPrim < TextPrims; ++TextPrim) {
        while(llGetSubString(Text,x,x) == "\n") { ++x; ++TextLineY; TextLineX = 0; }
        while(llGetSubString(Text,x,x) == " ") {
            ++TextLineX; x += 1;
            if(TextLineX >= TextLength) {
                TextLineX = 0; ++TextLineY;
            }
        }

        vector Pos;
        Pos.x = 0.0025;
        Pos.y = TextHeight * TextOffset*2.5;
        Pos.z = TextHeight*-.5;
        Pos.y += TextHeight * TextOffset * TextLineX;
        Pos.z -= TextHeight * TextLineY;

        TextRender += [
            PRIM_LINK_TARGET, llList2Integer(TextLinkset,TextPrim),
            PRIM_SIZE, <0.01, TextHeight*TextRatio, TextHeight>,
            PRIM_ROT_LOCAL, TextRot,
            PRIM_POS_LOCAL, TextPos + Pos*TextRot
        ];

        integer Face;
        @Consume;
        string Char = llGetSubString(Text,x,x);
        if(Char != "\n" && x < y && Face < 5) {
            TextRender += TextFace(Face, Char, Colour, Font);
            ++x; ++Face;
            if(++TextLineX < TextLength) jump Consume;
            else {
                TextLineX = 0; ++TextLineY;
            }
        }

        if(++TextRenders > 9) {
            TextRenders = 0;
            llSetLinkPrimitiveParamsFast(llList2Integer(TextRender,1), llList2List(TextRender,2,-1));
            TextRender = [];
        }
    }
}
```

- TextFace

  - Private internal function -- returns a prim parameters list for drawing a character on a prim face.

```lsl
list TextFace(integer Face, string Char, rotation Colour, key Font) {
    integer i = llSubStringIndex(TextChars, Char);
    float W = 0.60; float X = 0.0;
    float H = 0.98;
    if(Face == 0) return [
        PRIM_TEXTURE, 3, Font, <.25*W,.1*H,0>, <((-.45+.1*(i%10)) + (.0745*W)) + (X*W), .45-(.1*(i/10)), 0>, 0,
        PRIM_COLOR, 3, , Colour.s];
    else if(Face == 1) return [
        PRIM_TEXTURE, 7, Font, <.1*W,.1*H,0>, <((-.45+.1*(i%10))) + (X*W), .45-(.1*(i/10)), 0>, .0,
        PRIM_COLOR, 7, , Colour.s];
    else if(Face == 2) {
        float x = ((-.45+.1*(i%10)) - (.69*W)) + (X*W); if(x < -1) x = 2 + x;
        return [PRIM_TEXTURE, 4, Font, <-1.635*W,.1*H,0>, , .0,
                PRIM_COLOR, 4, , Colour.s];
    } else if(Face == 3) return [
        PRIM_TEXTURE, 6, Font, <.1*W,.1*H,0>, <((-.45+.1*(i%10))) + (X*W), .45-(.1*(i/10)), 0>, .0,
        PRIM_COLOR, 6, , Colour.s];
    /*/ Face == 4 /*/ return [
        PRIM_TEXTURE, 1, Font, <.25*W,.1*H,0>, <((-.45+.1*(i%10)) - (.0745*W)) + (X*W), .45-(.1*(i/10)), 0>, .0,
        PRIM_COLOR, 1, , Colour.s];
}
```

- TextFrameEnd

  - Finishes text input and starts actual rendering.

```lsl
TextFrameEnd() {
    for(; TextPrim < TextPrims; ++TextPrim) TextRender += [
        PRIM_LINK_TARGET, llList2Integer(TextLinkset, TextPrim),
        PRIM_POS_LOCAL, ZERO_VECTOR,
        PRIM_ROT_LOCAL, ZERO_ROTATION,
        PRIM_SIZE, <0.01, 0.01, 0.01>,
        PRIM_COLOR, ALL_SIDES, ZERO_VECTOR, 0.0
    ];
    llSetLinkPrimitiveParamsFast(llList2Integer(TextRender,1), llList2List(TextRender,2,-1));
    TextRender = [];
    TextRenders = TextPrim = 0;
}
```

```lsl
// NexiiText2
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
```

## Complete Script

```lsl
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// NexiiText2
list     TextLinkset;
integer  TextPrim;
integer  TextPrims;
list     TextRender;
integer  TextRenders;

integer  TextLength;
vector   TextPos;
rotation TextRot;
float    TextHeight;
integer  TextLineX;
integer  TextLineY;

float    TextRatio = 3.2222;
float    TextOffset = 0.57;
string   TextChars = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~";

TextInit() {
    integer Hay = 1; integer Stacks = llGetNumberOfPrims();
    for(; Hay <= Stacks; ++Hay ) if(llGetLinkName(Hay) == "Text") TextLinkset += Hay;
    TextPrims = llGetListLength(TextLinkset);
}

TextCursor(vector Position, vector Direction, float FontHeight, integer MaxCharsPerLine) {
    TextPos = Position;
    TextRot = llRotBetween(<1,0,0>, Direction);
    TextLength = MaxCharsPerLine;
    TextHeight = FontHeight;
    TextLineX = TextLineY = 0;
}

TextPush(string Text, rotation Colour, key Font) {
    integer x; integer y = llStringLength(Text);
    for(; x < y && TextPrim < TextPrims; ++TextPrim) {
        while(llGetSubString(Text,x,x) == "\n") { ++x; ++TextLineY; TextLineX = 0; }
        while(llGetSubString(Text,x,x) == " ") {
            ++TextLineX; x += 1;
            if(TextLineX >= TextLength) {
                TextLineX = 0; ++TextLineY;
            }
        }

        vector Pos;
        Pos.x = 0.0025;
        Pos.y = TextHeight * TextOffset*2.5;
        Pos.z = TextHeight*-.5;
        Pos.y += TextHeight * TextOffset * TextLineX;
        Pos.z -= TextHeight * TextLineY;

        TextRender += [
            PRIM_LINK_TARGET, llList2Integer(TextLinkset,TextPrim),
            PRIM_SIZE, <0.01, TextHeight*TextRatio, TextHeight>,
            PRIM_ROT_LOCAL, TextRot,
            PRIM_POS_LOCAL, TextPos + Pos*TextRot
        ];

        integer Face;
        @Consume;
        string Char = llGetSubString(Text,x,x);
        if(Char != "\n" && x < y && Face < 5) {
            TextRender += TextFace(Face, Char, Colour, Font);
            ++x; ++Face;
            if(++TextLineX < TextLength) jump Consume;
            else {
                TextLineX = 0; ++TextLineY;
            }
        }

        if(++TextRenders > 9) {
            TextRenders = 0;
            llSetLinkPrimitiveParamsFast(llList2Integer(TextRender,1), llList2List(TextRender,2,-1));
            TextRender = [];
        }
    }
}

list TextFace(integer Face, string Char, rotation Colour, key Font) {
    integer i = llSubStringIndex(TextChars, Char);
    float W = 0.60; float X = 0.0;
    float H = 0.98;
    if(Face == 0) return [
        PRIM_TEXTURE, 3, Font, <.25*W,.1*H,0>, <((-.45+.1*(i%10)) + (.0745*W)) + (X*W), .45-(.1*(i/10)), 0>, 0,
        PRIM_COLOR, 3, , Colour.s];
    else if(Face == 1) return [
        PRIM_TEXTURE, 7, Font, <.1*W,.1*H,0>, <((-.45+.1*(i%10))) + (X*W), .45-(.1*(i/10)), 0>, .0,
        PRIM_COLOR, 7, , Colour.s];
    else if(Face == 2) {
        float x = ((-.45+.1*(i%10)) - (.69*W)) + (X*W); if(x < -1) x = 2 + x;
        return [PRIM_TEXTURE, 4, Font, <-1.635*W,.1*H,0>, , .0,
                PRIM_COLOR, 4, , Colour.s];
    } else if(Face == 3) return [
        PRIM_TEXTURE, 6, Font, <.1*W,.1*H,0>, <((-.45+.1*(i%10))) + (X*W), .45-(.1*(i/10)), 0>, .0,
        PRIM_COLOR, 6, , Colour.s];
    /*/ Face == 4 /*/ return [
        PRIM_TEXTURE, 1, Font, <.25*W,.1*H,0>, <((-.45+.1*(i%10)) - (.0745*W)) + (X*W), .45-(.1*(i/10)), 0>, .0,
        PRIM_COLOR, 1, , Colour.s];
}

TextFrameEnd() {
    for(; TextPrim < TextPrims; ++TextPrim) TextRender += [
        PRIM_LINK_TARGET, llList2Integer(TextLinkset, TextPrim),
        PRIM_POS_LOCAL, ZERO_VECTOR,
        PRIM_ROT_LOCAL, ZERO_ROTATION,
        PRIM_SIZE, <0.01, 0.01, 0.01>,
        PRIM_COLOR, ALL_SIDES, ZERO_VECTOR, 0.0
    ];
    llSetLinkPrimitiveParamsFast(llList2Integer(TextRender,1), llList2List(TextRender,2,-1));
    TextRender = [];
    TextRenders = TextPrim = 0;
}
// NexiiText2
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Styles
key Normal      = "0967db80-5132-d6dc-f37c-4f9cc1196983";// Normal Font
key Bold        = "48de7a07-1641-3d26-2bca-9773a20d2adf";// Be Bold!
key Lined       = "35399d2f-e35f-5100-179a-f3a119b1cdf7";// URLy Underline!
key Italic      = "1bb8a1f9-87cb-4946-afc6-b1856bc9b752";// Iffy Italics!
key Stroked     = "a2d5149e-d018-3ddd-202d-3432605c8084";// Edgy Edge!
key Shadowed    = "347ff828-9cef-31e5-a792-1bfdd2a1cea0";// Silly Shadow!

rotation White  = <.99,.99,.99, 1.0>;
rotation Black  = <.00,.00,.00, 1.0>;
rotation Red    = <.99,.00,.00, 1.0>;
rotation Green  = <.00,.99,.50, 1.0>;
rotation Blue   = <.00,.40,.90, 1.0>;
rotation Orange = <.99,.50,.00, 1.0>;
rotation LSL    = <.00,.99,.50, 1.0>;
rotation URL    = <.20,.40,.70, 1.0>;
// Styles
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Linkset Indexing
list LinkedList(string Needle) {
    list Needles;
    integer Hay = 1;
    integer Stacks = llGetNumberOfPrims();
    for(; Hay <= Stacks; ++Hay ) if(llGetLinkName(Hay) == Needle) Needles += Hay;
    return Needles;
}
integer Linked(string Needle) {
    integer Prims = llGetNumberOfPrims()+1;
    while(--Prims) if(llGetLinkName(Prims) == Needle) return Prims;
    return 0;
}
// Linkset Indexing
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Application
default {
    state_entry() {
        TextInit();
        TextFrameEnd();

        integer primA = Linked("A"); // I often use linked prims for testing different position input.
        vector vA = llList2Vector(llGetLinkPrimitiveParams(primA, [PRIM_POS_LOCAL]),0);

        TextCursor(vA, <1,0,0>, 0.1, 25);
        TextPush("Awesome!", White, Italic);
        TextPush("\n\nNexiiText", Orange, Lined);
        TextPush("\n\tA Prim Text Renderer", White, Normal);
        TextPush("\n\n...with dynamic\n\t\tprim allocation", White, Normal);
        TextFrameEnd();
    }
}
```