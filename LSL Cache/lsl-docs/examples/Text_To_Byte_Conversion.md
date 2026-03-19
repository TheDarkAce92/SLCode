---
name: "Text To Byte Conversion"
category: "example"
type: "example"
language: "LSL"
description: "Here's a function to pass a string of text and receive a list of bytes. A second function is provided to work in reverse. These methods are especially useful for working with encryption."
wiki_url: "https://wiki.secondlife.com/wiki/Text_To_Byte_Conversion"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Here's a function to pass a string of text and receive a list of bytes. A second function is provided to work in reverse. These methods are especially useful for working with encryption.

## Text2Bytes.lsl

```lsl
list text2bytes(string text)
{
    string base64 = llStringToBase64(text);
    list bytes;
    integer i;
    integer n = llStringLength(base64);
    integer dword;
    for(i = 0; i < n; i += 4)
        bytes += [  ((dword = ((llBase64ToInteger(llGetSubString(base64, i, i + 3) + "==") >>  8) & 0xFFffFF)) >> 16),
                    ((dword >> 8) & 0xFF), (dword & 0xFF) ];
    return llList2List(bytes, 0, (-3 >> !!(dword & 0xFF00)) | !!(dword & 0xFF));
}

string bytes2text(list bytes)
{
    string text = "";
    integer i = -1;
    integer b = 0;
    while((b = (llList2Integer(bytes, ++i) & 0xFF)))
    {
        integer A = (b << 22) & 0x3C000000;
        integer B = (b << 20) & 0x00F00000;
        text += "%" + llGetSubString(llIntegerToBase64(
                        A + B + 0xD3400000
                        - (0xF8000000 * (A / 0x28000000))//lowercase=0x90000000, uppercase=0xF8000000
                        - (0x03E00000 * (B / 0x00A00000))//lowercase=0x02400000, uppercase=0x03E00000
                      ), 0, 1);
    }
    return llUnescapeURL(text);
}

default
{
    state_entry()
    {
        list bytes = text2bytes("Hello, Avatar!");
        llSay(0, llList2CSV(bytes));

        string text = bytes2text(bytes);
        llSay(0, text);
    }

    touch_start(integer total_number)
    {
        list bytes = text2bytes("Touched.");
        llSay(0, llList2CSV(bytes));

        string text = bytes2text(bytes);
        llSay(0, text);
    }
}
```