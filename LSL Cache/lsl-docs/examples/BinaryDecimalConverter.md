---
name: "BinaryDecimalConverter"
category: "example"
type: "example"
language: "LSL"
description: "The next function converts a binary value to a decimal number. Works +/- 5 times faster than Base2Dec :"
wiki_url: "https://wiki.secondlife.com/wiki/BinaryDecimalConverter"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

The next function converts a binary value to a decimal number. Works +/- 5 times faster than Base2Dec :

```lsl
integer binToDec(string val)
{
    integer dec = 0;
    integer i = ~llStringLength(val);
    while(++i)
        dec = (dec << 1) + (integer)llGetSubString(val, i, i);
    return dec;
}
```

This one converts a decimal to a binary value:

```lsl
string decToBin(integer val)
{
    string binary = (string)(val & 1);
    for(val = ((val >> 1) & 0x7FFFffff); val; val = (val >> 1))
    {
        if (val & 1)
            binary = "1" + binary;
        else
            binary = "0" + binary;
    }
    return binary;
}
```

Greets from Soundless :)

This version of decToBin doesn't crash on negatives, is shorter source code and about 50 bytes shorter in Mono bytecode than the original, but sadly about 50% slower. << and >> are expensive on bytecode.

```lsl
string decToBin(integer val)
{
    string binary;
    do
        binary = (string) (val & 1) + binary;
    while (val /= 2);
    return binary;
}
```

((Omei))