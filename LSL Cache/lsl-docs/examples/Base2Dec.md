---
name: "Base2Dec"
category: "example"
type: "example"
language: "LSL"
description: "This function converts a number to decimal from any base (up to 16). Its parameters are the number to be converted, and the base to convert from."
wiki_url: "https://wiki.secondlife.com/wiki/Base2Dec"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

This function converts a number to decimal from any base (up to 16). Its parameters are the number to be converted, and the base to convert from.

```lsl
integer sbBase2Dec(string strNumber, integer intBase) {
    string  strDigits = "0123456789abcdef";
    integer intDigit  = -llStringLength(strNumber);
    integer intReturn = 0;

    while(intDigit)
        intReturn = (intReturn * intBase) + llSubStringIndex(strDigits, llGetSubString(strNumber, intDigit, intDigit++));
    return intReturn;
}
```