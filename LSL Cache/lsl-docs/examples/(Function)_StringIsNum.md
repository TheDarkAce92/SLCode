---
name: "(Function) StringIsNum"
category: "example"
type: "example"
language: "LSL"
description: "Due to my need of wanting a nice clean function to test an input and check if it consists entirely of numbers, I decided to write one myself, and share with the community."
wiki_url: "https://wiki.secondlife.com/wiki/StringIsNum"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Due to my need of wanting a nice clean function to test an input and check if it consists entirely of numbers, I decided to write one myself, and share with the community.

This snippet is a fully working User Made Function. It is designed to be inserted into existing scripts to check if an input consists entirely of numbers, and will reject inputs that contain letters or symbols.

Note: This is a very inefficient technique. See later better examples.

```lsl
// this function will return TRUE if the entire string consists of number characters only
integer string_is_num(string input)
{
    list numberCharacters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"];
    integer stringLength = llStringLength(input);

    integer index;
    do
    {
        string character = llGetSubString(input, index, index);

        if (llListFindList(numberCharacters, [character]) == -1)
            return FALSE;

        ++index;
    }
    while (index < stringLength);

    return TRUE;
}

default
{
    state_entry()
    {
        key owner = llGetOwner();
        llListen(0, "", owner, "");
    }

    listen(integer channel, string name, key id, string message)
    {
        //Respond if the string is a number
        if( StringIsNum(message) )
            llOwnerSay("'" + message + "' consists of numbers only.");
        else
            llOwnerSay("'" + message + "' does not consist of numbers only.");
    }
}
```

## Better Methods

Here's a simpler solution for strings containing integer values from −2147483648 and 2147483647 written without + sign, leading zeros, or thousands separators ','  (Omei Qunhua)

```lsl
    if ( (string) ( (integer) data) == data)
        llOwnerSay("'" + data + "' contains a valid integer");
```

The following examples will validate that a string contains only the characters 0 though 9. (Omei Qunhua)

a) Example for a string of length 5

```lsl
    StringOf5Dec(string test)
    {
        return ( (integer) ("1" + test) >= 100000);
    }
```

b) Example for a string of length 1 through 9

```lsl
    VarStringIsDecimal(string test)
    {
        integer limit = (integer) llPow(10.0, llStringLength(test) );
        return ( (integer) ("1" + test) >= limit);
    }
```