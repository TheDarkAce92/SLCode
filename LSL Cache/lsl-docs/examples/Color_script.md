---
name: "Color script"
category: "example"
type: "example"
language: "LSL"
description: "integer CHANNEL = PUBLIC_CHANNEL; // channel to listen for commands on integer OWNER_ONLY = FALSE; // only owner can control integer USE_IMS = TRUE; // send IMs instead of using chat string COMMAND..."
wiki_url: "https://wiki.secondlife.com/wiki/Color_script"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

## Color script

Compare:

- ColorConvert
- Color

Color lists:

- [common HTML color names](http://www.w3schools.com/HTML/html_colornames.asp)
- [web safe colors](http://en.wikipedia.org/wiki/Web_colors#Web-safe_colors)

```lsl
// Created by:  Masakazu Kojima
// Reposted by: ALicia Sautereau

integer CHANNEL                 = PUBLIC_CHANNEL;        // channel to listen for commands on
integer OWNER_ONLY              = FALSE;                 // only owner can control
integer USE_IMS                 = TRUE;                  // send IMs instead of using chat
string  COMMAND_CHANGE_COLOR    = "change";              // command to change color
string  COMMAND_LIST_COLORS     = "listcolors";          // command to list colors
integer MAX_CHAT_LENGTH         = 255;                   // max size for one message
string  PREFIX_HEX              = "#";                   // prefix to specify hex code
string  PREFIX_VECTOR           = "<";                   // prefix to specify vector code
list    LINKS_TO_SET            = [LINK_SET, ALL_SIDES]; // [link number, link face, ...]

list    COLORS;

set_colors() {
    COLORS = [
        "navy",    "#001f3f",
        "blue",    "#0074d9",
        "aqua",    "#7fdbff",
        "teal",    "#39cccc",
        "olive",   "#3d9970",
        "green",   "#2ecc40",
        "lime",    "#01ff70",
        "yellow",  "#ffdc00",
        "orange",  "#ff851b",
        "red",     "#ff4136",
        "maroon",  "#85144b",
        "fuchsia", "#f012be",
        "purple",  "#b10dc9",
        "white",   "#ffffff",
        "silver",  "#dddddd",
        "gray",    "#aaaaaa",
        "black",   "#111111"
    ];
}

say(key id, string str) {
    if (USE_IMS)
        llInstantMessage(id, str);
    else
        llWhisper(PUBLIC_CHANNEL, str);
}

vector color_from_hex(string str) {
    return <(integer)("0x" + llGetSubString(str,1,2)),
            (integer)("0x" + llGetSubString(str,3,4)),
            (integer)("0x" + llGetSubString(str,5,6))> / 255;
}

vector color_from_vector(string vec) {
    // caveat: 1,1,1 will be treated as #ffffff, not #010101
    list   l = llParseString2List(vec, [" ", ",", "<", ">"], []);
    vector v;

    v.x = (float)llList2String(l, 0);
    v.y = (float)llList2String(l, 1);
    v.z = (float)llList2String(l, 2);

    if (v.x > 1 || v.y > 1 || v.z > 1)
        v /= 255;

    return v;
}

vector color_from_name(string name) {
    //                                   vv strip spaces and force lowercase                                vv
    integer x = llListFindList(COLORS, [ llToLower(llDumpList2String(llParseString2List(name, [" "], []), "")) ]);

    if (x == -1)
        return <-1, -1, -1>;

    return color_from_hex(llList2String(COLORS, x+1));
}

set_color(key id, string str) {
    vector color;
    integer i;
    if (llGetSubString(str, 0, 0) == PREFIX_HEX) // hex code
        color = color_from_hex(str);
    else if (llGetSubString(str, 0, 0) == PREFIX_VECTOR) // vector
        color = color_from_vector(str);
    else
        color = color_from_name(str);

    if (color.x < 0 || color.x > 1 || color.y < 0 || color.y > 1 || color.z < 0 || color.z > 1) {
        say(id, "Invalid color specified: " + str);
        return;
    }

    llSetColor(color, ALL_SIDES);
}

list_colors(key id) {
    string str  = "";
    string nstr = "";
    integer i;

    for (i = 0; i < llGetListLength(COLORS); i += 2) {
        nstr = str + llList2String(COLORS, i) + ", ";

        if (llStringLength(nstr) > MAX_CHAT_LENGTH) {
            say(id, str);
            str = llList2String(COLORS, i);
        } else {
            str = nstr;
        }
    }
    if (str != "") say(id, str);
}

default {

    on_rez(integer bla)
    {
        llResetScript();
    }

    changed(integer change)
    {
        if ((OWNER_ONLY) && (change & CHANGED_OWNER))
            llResetScript();
    }

    state_entry()
    {
        set_colors();

        if (OWNER_ONLY)
            llListen(CHANNEL, "", llGetOwner(), "");
        else
            llListen(CHANNEL, "", "", "");
    }

    listen(integer channel, string name, key id, string msg)
    {
        string command;
        string argument;
        list l;

        l = llParseStringKeepNulls(msg, [" "], []);
        command = llList2String(l, 0);
        argument = llDumpList2String(llList2List(l, 1, -1), " ");

        if (command == COMMAND_CHANGE_COLOR)
            set_color(id, argument);
        else if (command == COMMAND_LIST_COLORS)
            list_colors(id);

    }
}
```