---
name: "LSL NSieve Bits Benchmark"
category: "example"
type: "example"
language: "LSL"
description: "string hexc=\"0123456789ABCDEF\";"
wiki_url: "https://wiki.secondlife.com/wiki/LSL_NSieve_Bits_Benchmark"
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
// modified by Babbage Linden
//

string hexc="0123456789ABCDEF";

string setBitArray(integer numbits)
{
    string result = "";
    integer i;
    for(i = 0; i < numbits; i += 4)
    {
        result += "F";
    }
    result += "F";
    return result;
}

string replace(string s, integer index, string char)
{
    string result = "";
    if(index >= 1)
    {
        result += llGetSubString(s, 0, index - 1);
    }
    result += char;
    if(index < (llStringLength(s) - 1))
    {
        result += llGetSubString(s, index + 1, -1);
    }
    return result;
}

integer get(string s, integer index)
{
    integer charIndex = index / 4;
    integer bitIndex = index % 4;
    integer bits = (integer)("0x" + llGetSubString(s, charIndex, charIndex));
    return (bits & (1 << bitIndex));
}

string set(string s, integer index)
{
    integer charIndex = index / 4;
    integer bitIndex = index % 4;
    integer bits = (integer)("0x" + llGetSubString(s, charIndex, charIndex));
    bits = bits | (1 << bitIndex);
    return replace(s, charIndex, llGetSubString(hexc, bits, bits));
}

string unset(string s, integer index)
{
    integer charIndex = index / 4;
    integer bitIndex = index % 4;
    integer bits = (integer)("0x" + llGetSubString(s, charIndex, charIndex));
    integer mask = 0xF & ~(1 << bitIndex);
    bits = bits & mask;
    return replace(s, charIndex, llGetSubString(hexc, bits, bits));
}

test()
{
    integer m = 128;
    string bits = setBitArray(m);
    integer count = 0;

    integer i;
    for (i=2; i <= m; i++)
    {
         if(get(bits, i))
         {
            integer k;
            for(k=i+i; k <= m; k+=i)
            {
                bits = unset(bits, k);
            }
            count++;
         }
    }
    llSay(0, "Primes up to " + (string)m + " " + (string)count);
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