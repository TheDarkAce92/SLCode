---
name: "Seedable PRNG"
category: "example"
type: "example"
language: "LSL"
description: "See also: llFrand, llListRandomize, Pseudo-random_Number_Generator"
wiki_url: "https://wiki.secondlife.com/wiki/Seedable_PRNG"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

See also: llFrand, llListRandomize, Pseudo-random_Number_Generator

Note: The 32bit_Hash example presents just the conversion to integer from llMD5String.

## md5 based seedable PRNG

It's not the fastest thing but it doesn't seem to have much if any output skew, and I couldn't detect any periodicity in the first 100,000 cycles.

```lsl
//new md5 based seedable PRNG
//By: Gigs Taggart
//Released under BSD License.
//http://www.opensource.org/licenses/bsd-license.php

integer gSeed=0;
string gLastHash;

prng_seed(integer seed)
{
    gSeed=seed;
}

integer prng_get()
{
    gLastHash=llMD5String(gLastHash, gSeed);
    //the bitwise thingy gets rid of negative numbers
    return (integer)("0x" + llGetSubString(gLastHash, 0, 7)) & 0x7FFFFFFF;
}

default
{
    state_entry()
    {
        prng_seed(2007031901);

        string line;
        integer index;

        line = "";
        for (index = 0; index < 9; ++index)
        {
           line += " " + (string) prng_get();
        }
        llOwnerSay(line);

        line = "";
        for (index = 0; index < 30; ++index)
        {
           line += " " + (string) (1 + (prng_get() % 6));
        }
        llOwnerSay(line);

        llOwnerSay("OK");
    }
}
```