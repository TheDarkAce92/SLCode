---
name: "LSL NSieve Benchmark"
category: "example"
type: "example"
language: "LSL"
description: "string setByteArray(integer numbytes) { string result = \"\"; integer i; for(i = 0; i < numbytes; ++i) { result += \"1\"; } result += \"1\"; return result; }"
wiki_url: "https://wiki.secondlife.com/wiki/LSL_NSieve_Benchmark"
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

string setByteArray(integer numbytes)
{
    string result = "";
    integer i;
    for(i = 0; i < numbytes; ++i)
    {
        result += "1";
    }
    result += "1";
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
    return llGetSubString(s, index, index) == "1";
}

string set(string s, integer index)
{
    return replace(s, index, "1");
}

string unset(string s, integer index)
{
    return replace(s, index, "0");
}

test()
{
    integer m = 128;
    string bytes = setByteArray(m);
    integer count = 0;

    integer i;
    for (i=2; i <= m; i++)
    {
         if(get(bytes, i))
         {
            integer k;
            for(k=i+i; k <= m; k+=i)
            {
                bytes = unset(bytes, k);
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

## LSL2 Optimized

This version was optimized for the LSL2 VM, it might run faster under Mono then the unoptimized version. In LSLEditor, it runs about 20% faster.

```lsl
//
// The Great Computer Language Shootout
// http://shootout.alioth.debian.org/
//
// contributed by Isaac Gouy
// modified by Babbage Linden
// optimized for LSL2 by Strife Onizuka, Apr 14 2008
//

test()
{
    integer m = 128;

    string bytes = "11";
    integer i = 2;
    for(; i <= m; i = i << 1)
    {
        bytes += bytes;
    }
    bytes = llGetSubString(bytes , 0, m);
    integer count = 0;

    for (i = 2; i <= m; ++i)
    {
        if(llGetSubString(bytes, i, i) == "1")
        {
            integer k = i;
            while((k += i) <= m)
            {
                bytes = llInsertString(llDeleteSubString(bytes, k, k), k, "0");
            }
            ++count;
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