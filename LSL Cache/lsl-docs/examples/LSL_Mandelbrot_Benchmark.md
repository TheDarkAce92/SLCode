---
name: "LSL Mandelbrot Benchmark"
category: "example"
type: "example"
language: "LSL"
description: "string hexc=\"0123456789ABCDEF\";"
wiki_url: "https://wiki.secondlife.com/wiki/LSL_Mandelbrot_Benchmark"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

```lsl
//
// The Great Computer Language Shootout
// http://shootout.alioth.debian.org/
//
// contributed by Isaac Gouy
// modified by Babbage Linden, Oct 10 2007
//

string hexc="0123456789ABCDEF";

string byte2hex(integer byte)
{
    integer highBits = (byte & 0xF0) >> 4;
    integer lowBits = byte & 0x0F;
    return llGetSubString(hexc, highBits, highBits) + llGetSubString(hexc, lowBits, lowBits);
}

mandlebrot(integer width)
{
    integer height = width;
    integer i;
    integer m = 50;
    integer bits = 0;
    integer bitnum = 0;
    integer isOverLimit = FALSE;
    float Zr = 0.0;
    float Zi = 0.0;
    float Cr = 0.0;
    float Ci = 0.0;
    float Tr;
    float Ti;
    float limit2 = 4.0;

    llSay(0, "P4");
    llSay(0, (string)width + " " + (string)height);

    string hexBytes = "";

    integer y;
    for(y = 0; y < height; y++)
    {
        integer x;
     for(x = 0; x < width; x++)
     {

        Zr = 0.0; Zi = 0.0;
        Cr = 2.0*x / width - 1.5;
        Ci = 2.0*y / height - 1.0;

        i = 0;
        do {
           Tr = Zr*Zr - Zi*Zi + Cr;
           Ti = 2.0*Zr*Zi + Ci;
           Zr = Tr; Zi = Ti;
           isOverLimit = Zr*Zr + Zi*Zi > limit2;
        } while (!isOverLimit && (++i < m));

        bits = bits << 1;
        if (!isOverLimit) bits++;
        bitnum++;

        if (x == width - 1) {
           bits = bits << (8 - bitnum);
           bitnum = 8;
        }

        if (bitnum == 8)
        {
           hexBytes += byte2hex(bits);
           bits = 0; bitnum = 0;
        }
     }
    }
    llSay(0, "0x" + hexBytes);
}

test()
{
    mandlebrot(10);
}

time()
{
    llResetTime();
    llSay(0, "Starting tests...");
    test();
    llSay(0, "Finished tests in " + (string)llGetTime() + "s");

}

default
{
    state_entry()
    {
        time();
    }

    touch_start(integer num)
    {
        time();
    }
}
```

## LSL2 Optimized

This version was optimized for the LSL2 VM, it might run faster under Mono then the unoptimized version.

```lsl
//
// The Great Computer Language Shootout
// http://shootout.alioth.debian.org/
//
// contributed by Isaac Gouy
// modified by Babbage Linden, Oct 10 2007
// optimized for LSL2 by Strife Onizuka, Apr 14 2008
//

string hexc="0123456789ABCDEF";

string byte2hex(integer byte)
{
    integer highBits = (byte & 0xF0) >> 4;
    integer lowBits = byte & 0x0F;
    return llGetSubString(hexc, highBits, highBits) + llGetSubString(hexc, lowBits, lowBits);
}

mandlebrot(integer width)
{
    integer height = width;
    integer m = 50;
    integer bits = 0;
    integer bitnum = 0;
    integer isNotOverLimit = TRUE;
    float limit2 = 4.0;

    llSay(0, "P4");
    llSay(0, (string)width + " " + (string)height);

    string hexBytes = "";

    integer y = 0;
    for(; y < height; ++y)
    {
        integer x = 0;
        for(; x < width; ++x)
        {

           float Zr = 0.0;
           float Zi = 0.0;
           float Cr = 2.0*x / width - 1.5;
           float Ci = 2.0*y / height - 1.0;

           integer i = 0;
           do {
              float Tr = Zr*Zr - Zi*Zi + Cr;
              Zi = 2.0*Zr*Zi + Ci;
              Zr = Tr;
           } while ((isNotOverLimit = (Zr*Zr + Zi*Zi <= limit2)) && (++i < m));

           bits = (bits << 1) + isNotOverLimit;
           ++bitnum;

           if (x == width - 1) {
              bits = bits << (8 - bitnum);
              bitnum = 8;
           }

           if (bitnum == 8)
           {
              hexBytes += byte2hex(bits);
              bits = 0; bitnum = 0;
           }
        }
    }
    llSay(0, "0x" + hexBytes);
}

test()
{
    mandlebrot(10);
}

time()
{
    llResetTime();
    llSay(0, "Starting tests...");
    test();
    llSay(0, "Finished tests in " + (string)llGetTime() + "s");

}

default
{
    state_entry()
    {
        time();
    }

    touch_start(integer num)
    {
        time();
    }
}
```