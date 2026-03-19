---
name: "String Compare"
category: "example"
type: "example"
language: "LSL"
description: "Created by Xaviar Czervik. Do whatever you wish with this function: Sell it (good luck), use it, or modify it."
wiki_url: "https://wiki.secondlife.com/wiki/String_Compare"
author: "Xaviar Czervik"
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

### String compare

Created by Xaviar Czervik. Do whatever you wish with this function: Sell it (good luck), use it, or modify it.

The following code returns 1, -1 or 0. The 1 and -1 are essentially random, however it will return the same value every time the script is executed. 0 Is returned when, and only when, the strings are exactly equal. Completely re-designed to use a few tricks I learned in the past months. Also much easier to read now.

I have used this script for comparing the Keys of two objects in a dynamic set of sensors, to decide which one should be the "Master" in the region to tell me information. I'm sure there can be more uses to this...

```lsl
integer compare(string s1, string s2)
{
    if (s1 == s2)
        return FALSE;

    else if (llStringLength(s1) < llStringLength(s2))
        return TRUE;

    else if (llStringLength(s1) > llStringLength(s2))
        return -1;

    else
    {
        list testList = [s1, s2];

        testList = llListSort(testList, 0, TRUE);

        if (s1 == llList2String(testList, 0))
            return TRUE;

        return -1;
    }
}
```

### Notes:

I'm not sure why the string length comparison is in above function, it is not needed for string comparison functions where you rely on alphabetical order. The concept is nice though. I've modified this function. Given strings s1 and s2, it'l return 1 if s1>s2, -1 if s1<s2 and 0 if they are equal:

```lsl
integer compare(string s1, string s2)
{
   if (s1 == s2)
        return FALSE;

    else
    {
        list testList = [s1, s2];
        testList = llListSort(testList, 1, 0);

        // s2 < s1
        if (s1 == llList2String(testList, 0))
            return TRUE;

        return -1;
    }
}
```

Above function not extensively tested, but it seems to suit my purpose (having users enter a set of characters within certain range, filter out anything else since it will be submitted to a webpage).
If only linden would give us 'normal' string comparison functions like any other language, instead of spending expensive cpu cycles to validate user input.

This can be further reduced to the following:

```lsl
integer compare(string s1, string s2)
{
    if (s1 == s2)
        return FALSE;

    if (s1 == llList2String(llListSort([s1, s2], 1, TRUE), 0))
        return -1;

    return TRUE;
}
```