---
name: "List2CSV"
category: "example"
type: "example"
language: "LSL"
description: "Includes escaping all characters, including commas and spaces, so the list that comes out should be just like the list that is sent in. Feedback is greatly appericated."
wiki_url: "https://wiki.secondlife.com/wiki/List2CSV"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

## List2CSV and CSV2List

Includes escaping all characters, including commas and spaces, so the list that comes out should be just like the list that is sent in.  Feedback is greatly appericated.

```lsl
//Thanks to:
//    http://lslwiki.net/lslwiki/wakka.php?wakka=llCSV2List (viewed Nov 12, 2008)
//    https://wiki.secondlife.com/wiki/Library_Combined_Library (viewed Nov 12, 2008)

string strReplace(string str, string search, string replace) {
    return llDumpList2String(llParseStringKeepNulls((str = "") + str, [search], []), replace);
}

string escapeString(string s)
{
    //I'm using forward slashes because backslashes are special chars in LSL
    //    so reading this would be a pain.
    //escape / to /b
    //escape , to /c
    //escape < to /l
    //escape > to /r
    //escape space to /s
    string final = s;
    //backslash must be first when escaping
    final = strReplace(final, "/", "/b");

    final = strReplace(final, ",", "/c");
    final = strReplace(final, "<", "/l");
    final = strReplace(final, ">", "/r");
    final = strReplace(final, " ", "/s");
    return final;
}

string unescapeString(string s)
{
    string final = s;
    final = strReplace(final, "/c", ",");
    final = strReplace(final, "/l", "<");
    final = strReplace(final, "/r", ">");
    final = strReplace(final, "/s", " ");

    //backslash must be last when unescaping
    final = strReplace(final, "/b", "/");
    return final;
}

string List2TypeCSV(list input) { // converts a list to a CSV string with type information prepended to each item
    integer     i;
    list        output;
    integer     len;

    len=llGetListLength(input); //this can shave seconds off long lists
    for (i = 0; i < len; i++) {
        output += [llGetListEntryType(input, i)] + escapeString((string)llList2List(input, i, i));
    }

    return llList2CSV(output);
}

list TypeCSV2List(string inputstring) { // converts a CSV string created with List2TypeCSV back to a list with the correct type information
    integer     i;
    list        input;
    list        output;
    integer     len;

    input = llCSV2List(inputstring);

    len=llGetListLength(input);
    for (i = 0; i < len; i += 2) {
        string value = unescapeString(llList2String(input, i + 1));
        if (llList2Integer(input, i) == TYPE_INTEGER) output += (integer)value;
        else if (llList2Integer(input, i) == TYPE_FLOAT) output += (float)value;
        else if (llList2Integer(input, i) == TYPE_STRING) output += value;
        else if (llList2Integer(input, i) == TYPE_KEY) output += (key)value;
        else if (llList2Integer(input, i) == TYPE_VECTOR) output += (vector)value;
        else if (llList2Integer(input, i) == TYPE_ROTATION) output += (rotation)value;
    }

    return output;
}

testWithValue(string evilString)
{
        list    l;
        string  s;

                l = [ 1, 2, evilString, 5 ];

        s = List2TypeCSV(l);

        l = TypeCSV2List(s);

        if (llGetListEntryType(l, 0) != TYPE_INTEGER) llOwnerSay("Bad! 0");
        if (llGetListEntryType(l, 1) != TYPE_INTEGER) llOwnerSay("Bad! 1");
        if (llGetListEntryType(l, 2) != TYPE_STRING) llOwnerSay("Bad! 2");
        if (llGetListEntryType(l, 3) != TYPE_INTEGER) llOwnerSay("Bad! 3");

        if (llList2Integer(l, 0) != 1) llOwnerSay("Bad! 0b");
        if (llList2Integer(l, 1) != 2) llOwnerSay("Bad! 1b");
        if (llList2String(l, 2) != evilString) llOwnerSay("Bad! 2b");
        if (llList2Integer(l, 3) != 5) llOwnerSay("Bad! 3b");
}

default {
    state_entry() {

        testWithValue("3,4");
        testWithValue("3<4");
        testWithValue("3>4");
        testWithValue("3/4");

        llOwnerSay("Done!");
    }
}
```