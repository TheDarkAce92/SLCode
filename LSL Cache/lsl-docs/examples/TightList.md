---
name: "TightList"
category: "example"
type: "example"
language: "LSL"
description: "TightList is a family of functions for encoding lists as strings and then decoding them back into lists."
wiki_url: "https://wiki.secondlife.com/wiki/TightList"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 Goals
- 2 Points to customize
- 3 TightList Deviations
- 4 LSL
- 5 ESL

TightList is a family of functions for encoding lists as strings and then decoding them back into lists.

There are two flavors, TightList and TightListType. The big differences are that TLT preserves types and uses a 6 char header (TL uses a 1 char header).

### Goals

1. Minimal amount of data required without having to use a specialized decoder for data types.
1. The functions must be fast.
1. A standardized string format so encoders can be customized.

### Points to customize

- Separator selection
- Data -> String conversion

### TightList Deviations

• TLT

BTLT

–

Uses a complicated float encoder that is tighter than using hex floats (and faster).

### LSL

Here are the functions in LSL, they aren't the easiest to customize in this state, it best to use the ESL versions.

```lsl
//TightList family of functions Version 1.0
//Copyright Strife Onizuka 2004-2006
//Free to use and distribute as long as this message is not removed.

list TightListParse(string input)
{
    string seperator = llGetSubString(input,(0),(0));//save memory
    return llParseStringKeepNulls(llDeleteSubString(input,(0),(0)), [input=seperator],[]);
}

string TightListDump(list input, string possibles)
{//TLD( complex) makes a string from a list using a seperator that is supposed to be unique to the string
    string buffer = (string)(input);//dump the list without a seperator
    integer counter = -39 - llStringLength(possibles);
    if(counter == -40)
        if(!~llSubStringIndex(buffer,possibles))
            jump end;//woot, we were given a unique seperator
    possibles += "|/?!@#$%^&*()_=:;~`'<>{}[],.\n\" qQxXzZ\\";//"//Good character set of rarely used letters.
    do; while(~llSubStringIndex(buffer,llGetSubString(possibles,counter,counter)) && (counter=-~counter));//search for unique seperator

    possibles = llGetSubString(possibles,counter,counter);

    @end;
    buffer = "";//save memory
    return possibles + llDumpList2String((input = []) + input, possibles);
}

integer TightListTypeLength(string input)
{
    string seperators = llGetSubString(input,(0),6);
    return ((llParseStringKeepNulls(llDeleteSubString(input,(0),5), [],[input=llGetSubString(seperators,(0),(0)),
           llGetSubString(seperators,1,1),llGetSubString(seperators,2,2),llGetSubString(c,3,3),
           llGetSubString(seperators,4,4),llGetSubString(seperators,5,5)]) != []) + (llSubStringIndex(seperators,llGetSubString(seperators,6,6)) < 6)) >> 1;
}

integer TightListTypeEntryType(string input, integer index)
{
    string seperators = llGetSubString(input,(0),6);
    return llSubStringIndex(seperators, input) + ((input = llList2String(llList2List(input + llParseStringKeepNulls(llDeleteSubString(input,(0),5), [],[input=llGetSubString(seperators,(0),(0)), llGetSubString(seperators,1,1),llGetSubString(seperators,2,2),llGetSubString(seperators,3,3), llGetSubString(seperators,4,4),llGetSubString(seperators,5,5)]), (llSubStringIndex(seperators,llGetSubString(seperators,6,6)) < 6) << 1, -1),  index << 1)) != "");
}

list TightListTypeParse(string input) {
    list partial;
    if(llStringLength(input) > 6)
    {
        string seperators = llGetSubString(input,(0),6);
        integer pos = ([] != (partial = llList2List(input + llParseStringKeepNulls(llDeleteSubString(input,(0),5), [],[input=llGetSubString(seperators,(0),(0)), llGetSubString(seperators,1,1),llGetSubString(seperators,2,2),llGetSubString(seperators,3,3), llGetSubString(seperators,4,4),llGetSubString(seperators,5,5)]), (llSubStringIndex(seperators,llGetSubString(seperators,6,6)) < 6) << 1, -1)));
        integer type = (0);
        integer sub_pos = (0);
        do
        {
            list current = (list)(input = llList2String(partial, sub_pos= -~pos));//TYPE_STRING || TYPE_INVALID (though we don't care about invalid)
            if(!(type = llSubStringIndex(seperators, llList2String(partial,pos))))//TYPE_INTEGER
                current = (list)((integer)input);
            else if(type == 1)//TYPE_FLOAT
                current = (list)((float)input);
            else if(type == 3)//TYPE_KEY
                current = (list)((key)input);
            else if(type == 4)//TYPE_VECTOR
                current = (list)((vector)input);
            else if(type == 5)//TYPE_ROTATION
                current = (list)((rotation)input);
            partial = llListReplaceList(partial, current, pos, sub_pos);
        }while((pos= -~sub_pos) & 0x80000000);
    }
    return partial;
}

string TightListTypeDump(list input, string seperators) {//This function is dangerous
    seperators += "|/?!@#$%^&*()_=:;~`'<>{}[],.\n\" qQxXzZ\\"; //"//Buggy highlighter fix
    string cumulator = (string)(input);
    integer counter = (0);
    do
        if(~llSubStringIndex(cumulator,llGetSubString(seperators,counter,counter)))
            seperators = llDeleteSubString(seperators,counter,counter);
        else
            counter = -~counter;
    while(counter<6);
    seperators = llGetSubString(seperators,(0),5);

        cumulator =  "";

    if((counter = (input != [])))
    {
        do
        {
            integer type = ~-llGetListEntryType(input, counter = ~-counter);

            cumulator = (cumulator = llGetSubString(seperators,type,type)) + llList2String(input,counter) + cumulator;
        }while(counter);
    }
    return seperators + cumulator;
}
```

### ESL

Macro

Description

TIGHTLISTPARSE

Standard TightListParse function TightListParse(string in)

TIGHTLISTDUMP

Standard TightListDump function TightListDump(list in, string seps)

TIGHTLISTDUMPSIMPLE

Simple TightListDump function (takes on less parameter) TightListDump(list in)

TIGHTLISTDUMPUNICODE
requires byte2hex

A Standard version of TLD which generates it's separator systematicaly instead of using the built in list.

TIGHTLISTUNICODESUPPORT
requires byte2hex

Adds unicode generation support TIGHTLISTDUMP and TIGHTLISTDUMPSIMPLE

TIGHTLISTTYPEQUICKREAD

A function for breaking a TightListType string into it's pairs, TightListTypeQuickRead is usualy a macro but by specifying this flag, it becomes a stand alone function (which can be advantageous if using more then one TLT function as a bytecode savings).

NO_TIGHTLISTTYPEQUICKREAD

Causes TIGHTLISTTYPEQUICKREAD to become undefined

TIGHTLISTTYPELENGTH

Returns the number of entries in a TLT string. TightListTypeLength(string in)

TIGHTLISTTYPEENTRYTYPE

Returns the entry type of an entry in a TLT string. TightListTypeEntryType(string in, integer index)

TIGHTLISTTYPEPARSE

Converts a TLT string into a fully type list. TightListTypeParse(string in)

TIGHTLISTTYPEDUMP

Converts a list into a TLT string TightListTypeDump(list in, string seps)

ALL_TLTD(type, input, index, output_buffer)
optional

A specialized mode that passes the list entry onto another function to escape.

TLD_DUMPLIST2STRING_MASK
required if ALL_TLTD is defined

A macro that effects ALL_TLTD, a mask of types (1 << (TYPE_* - 1))

TLTDV(input, index)
optional

Specialized function for converting a vector into a string

TLTDR(input, index)
optional

Specialized function for converting a rotation into a string

TLTDF(input, index)
optional

Specialized function for converting a float into a string

TLTDI(input, index)
optional

Specialized function for converting an integer into a string

TLTDK(input, index)
optional

Specialized function for converting a key into a string

TLTDS(input, index)
optional

Specialized function for converting a string into a string

TLD_DUMPLIST2STRING(in, sep)
Optional, used in TLD and TLTD

If left undefined, it resolves to llDumpList2String(in, sep), this is useful for when a script uses a specialized encoder for list types.

TIGHTLISTDUMPCHARS
Optional, used in TLD and TLTD

List of characters to use in TLD and TLTD

TIGHTLISTDUMPCHARS_LENGTH

Number of characters in TIGHTLISTDUMPCHARS
must be defined if TIGHTLISTDUMPCHARS is defined, otherwise it must be undefined.

TIGHTLISTDUMPCHARS_LENGTH_1

TIGHTLISTDUMPCHARS_LENGTH - 1
must be defined if TIGHTLISTDUMPCHARS is defined, otherwise it must be undefined.

TIGHTLISTDUMPCHARS_LENGTH_2

-TIGHTLISTDUMPCHARS_LENGTH - 1
must be defined if TIGHTLISTDUMPCHARS is defined, otherwise it must be undefined.

TIGHTLISTDUMPCHARS_LENGTH_3

-TIGHTLISTDUMPCHARS_LENGTH - 2
must be defined if TIGHTLISTDUMPCHARS is defined, otherwise it must be undefined.

TIGHTLISTDUMPCHARS_LENGTH_4

-TIGHTLISTDUMPCHARS_LENGTH
must be defined if TIGHTLISTDUMPCHARS is defined, otherwise it must be undefined.

NICENAMES

Translates the variable names into nice easily read names.

ZERO_INTEGER

Used to define zero, this value does not need to be set

CRAZY_MODE

Only works if ZERO_INTEGER is left unset, it enables a bytecode savings for ZERO_INTEGER (which comes at the cost of speed).

Example:

```lsl
#define TIGHTLISTTYPEDUMP
#define TIGHTLISTTYPEPARSE
#define TIGHTLISTTYPELENGTH
#define TIGHTLISTTYPEENTRYTYPE
#define TIGHTLISTDUMP
#define TIGHTLISTPARSE
#define NICENAMES
#include "Tightlist.esl"
```

```lsl
string hexc="0123456789ABCDEF";

string byte2hex(integer x)
{//Helper function for use with unicode characters.
    return llGetSubString(hexc, x = ((x >> 4) & 0xF), x) + llGetSubString(hexc, x & 0xF, x & 0xF);
}
```

Source:

```lsl
//TightList family of functions Version 1.0
//Copyright Strife Onizuka 2004-2006
//Free to use and distribute as long as this message is not removed.
#ifndef TIGHTLISTDUMPCHARS
    #define TIGHTLISTDUMPCHARS "|/?!@#$%^&*()_=:;~`'<>{}[],.\n\" qQxXzZ\\"
    #define TIGHTLISTDUMPCHARS_LENGTH_1  37
    #define TIGHTLISTDUMPCHARS_LENGTH    38
    #define TIGHTLISTDUMPCHARS_LENGTH_4 -38
    #define TIGHTLISTDUMPCHARS_LENGTH_2 -39
    #define TIGHTLISTDUMPCHARS_LENGTH_3 -40
#endif
#if !defined(ZERO_INTEGER)
    #ifndef REMOVE_ZERO_INTEGER
    #define REMOVE_ZERO_INTEGER
    #endif
    #ifdef CRAZY_MODE
        #define ZERO_INTEGER ((integer)"")
    #else
        #define ZERO_INTEGER (0)
    #endif
#endif

#if defined(TLD_DUMPLIST2STRING)
    #if !defined(ALL_TLTD) && defined(TLD_DUMPLIST2STRING_MASK) && (TLD_DUMPLIST2STRING_MASK > 0 || TLD_DUMPLIST2STRING_MASK < 0)
        #if TLD_DUMPLIST2STRING_MASK == 0x3F
            #define PURE_ALL_TLTD(list,pos) \
                TLD_DUMPLIST2STRING(llList2List(list,pos,pos)TLD_DUMPLIST2STRING_PARAM)
        #else
            #ifndef TLD_DUMPLIST2STRING_PARAM
                #define TLD_DUMPLIST2STRING_PARAM
            #endif
            #define ALL_TLTD(type,list,pos,return) \
                if(TLD_DUMPLIST2STRING_MASK & (1 << type)) \
                    return = TLD_DUMPLIST2STRING(llList2List(list,pos,pos)TLD_DUMPLIST2STRING_PARAM)
        #endif
    #endif
#endif
#ifndef TLD_DUMPLIST2STRING
    #define TLD_DUMPLIST2STRING llDumpList2String
    #ifndef TLD_TYPECAST_DUMPLIST2STRING
        #define TLD_TYPECAST_DUMPLIST2STRING(a) (string)(a)
    #endif
#endif
#ifndef TLD_TYPECAST_DUMPLIST2STRING
    #define TLD_TYPECAST_DUMPLIST2STRING(a) TLD_DUMPLIST2STRING(a,"")
#endif

#ifdef TIGHTLISTPARSE
    #ifdef NICENAMES
        #define a input
        #define b seperator
    #endif
    #ifdef CRAZY_MODE
list TightListParse(string a)
{
    string b = llGetSubString(a,ZERO_INTEGER,ZERO_INTEGER);//save memory
    return llParseStringKeepNulls(llDeleteSubString(a,(integer)(a=""),ZERO_INTEGER), [b],[]);
}
    #else
list TightListParse(string a)
{
    string b = llGetSubString(a,ZERO_INTEGER,ZERO_INTEGER);//save memory
    return llParseStringKeepNulls(llDeleteSubString(a,ZERO_INTEGER,ZERO_INTEGER), [a=b],[]);
}
    #endif
    #ifdef NICENAMES
        #undef a
        #undef b
    #endif
#endif

#if defined(TIGHTLISTDUMPSIMPLE) || defined(TIGHTLISTDUMP)
    #ifdef NICENAMES
        #define a input
        #define b possibles
        #define c buffer
        #define d counter
        #define e uft8char
    #endif
    #ifdef TIGHTLISTDUMPUNICODE
string TightListDump(list a)
{//TLD(unicode) makes a string from a list using a seperator that is supposed to be unique to the string
    string c = TLD_TYPECAST_DUMPLIST2STRING(a);//dump the list without a seperator
    integer e = ZERO_INTEGER;
    do //generate a seperator
    {
        integer d = ((e >= 0x80) + (e >= 0x800) + (e >= 0x10000) + (e >= 0x200000) + ((e=-~e) >= 0x4000000));
        string b = "%" + byte2hex((e >> (6 * d)) | ((0x7F80 >> d) << !d));
        while(d)
            b += "%" + byte2hex((((e >> (6 * (d=~-d))) | 0x80) & 0xBF));
    }while(b != "" && ~llSubStringIndex(c,b = llUnescapeURL(b)));
    c = "";
    return b + TLD_DUMPLIST2STRING(a, b);//pray we don't have a collision.
}
    #elif defined(TIGHTLISTDUMPSIMPLE)
string TightListDump(list a)
{//TLD(simple) makes a string from a list using a seperator that is supposed to be unique to the string
    string b = TIGHTLISTDUMPCHARS;//Good character set of rarely used letters.
    string c = TLD_TYPECAST_DUMPLIST2STRING(a);//dump the list without a seperator
    integer d = TIGHTLISTDUMPCHARS_LENGTH_2;
    do; while(~llSubStringIndex(c,llGetSubString(b,d,d)) && (d= -~d));//search for unique seperator
#if TIGHTLISTUNICODESUPPORT
    if(d)
        b = llGetSubString(b,d,d);//extract the seperator
    else
    {
        integer e = 0;
        do for(b = "%" + byte2hex((e >> (6 * d)) | ((0x7F80 >> d) << !(d = ((e >= 0x80) + (e >= 0x800) + (e >= 0x10000) + (e >= 0x200000) + ((e=-~e) >= 0x4000000)))));d;b += "%" + byte2hex((((e >> (6 * (d=~-d))) | 0x80) & 0xBF))); while(b != "" &&~llSubStringIndex(c,b = llUnescapeURL(b)));
    }
    c = "";//saves memory
    return b + TLD_DUMPLIST2STRING(a, b);//pray we don't have a collision.
#else
    c = llGetSubString(b,d,d);//extract the seperator, saves memory (by releasing c)
    return c + TLD_DUMPLIST2STRING(a, c);//pray we don't have a collision.
#endif
}
    #else
string TightListDump(list a, string b)
{//TLD( complex) makes a string from a list using a seperator that is supposed to be unique to the string
    string c = TLD_TYPECAST_DUMPLIST2STRING(a);//dump the list without a seperator
    integer d = TIGHTLISTDUMPCHARS_LENGTH_2 - llStringLength(b);
    if(d == TIGHTLISTDUMPCHARS_LENGTH_3)
        if(!~llSubStringIndex(c,b))
            jump end;//woot, we were given a unique seperator
    b += TIGHTLISTDUMPCHARS;//Good character set of rarely used letters.
    do; while(~llSubStringIndex(c,llGetSubString(b,d,d)) && (d=-~d));//search for unique seperator
        #if TIGHTLISTUNICODESUPPORT
    if(d)
        b = llGetSubString(b,d,d);//extract the seperator
    else
    {
        integer e = 0;
        do for(b = "%" + byte2hex((e >> (6 * d)) | ((0x7F80 >> d) << !(d = ((e >= 0x80) + (e >= 0x800) + (e >= 0x10000) + (e >= 0x200000) + ((e=-~e) >= 0x4000000)))));d;b += "%" + byte2hex((((e >> (6 * (d=~-d))) | 0x80) & 0xBF))); while(b != "" &&~llSubStringIndex(c,b = llUnescapeURL(b)));
    }

        #else
    b = llGetSubString(b,d,d);
        #endif
    @end;
    c = "";//save memory
    return b + TLD_DUMPLIST2STRING((a = []) + a, b);
}
    #endif
    #ifdef NICENAMES
        #undef a
        #undef b
        #undef c
        #undef d
        #undef e
    #endif
#endif

#if defined(TIGHTLISTTYPEQUICKREAD) && defined(NO_TIGHTLISTTYPEQUICKREAD)
    #undef TIGHTLISTTYPEQUICKREAD
#endif
#if defined(TIGHTLISTTYPEQUICKREAD) || defined(TIGHTLISTTYPELENGTH) || defined(TIGHTLISTTYPEENTRYTYPE) || defined(TIGHTLISTTYPEPARSE) || defined(TIGHTLISTTYPEDUMP)
    #ifdef TIGHTLISTTYPEQUICKREAD
        #ifdef NICENAMES
            #define a input
            #define m seperators
        #endif
list TightListTypeQuickRead(string a, string m)
{//all TightListType* parse functions call QuickRead, as a macro or as a function. QuickRead
    #endif //{
    #ifndef TightListTypeQuickRead
        #define TightListTypeQuickRead(a,m) llList2List(a + \
                                llParseStringKeepNulls(llDeleteSubString(a,ZERO_INTEGER,5), [],[a=llGetSubString(m,ZERO_INTEGER,ZERO_INTEGER), \
                                llGetSubString(m,1,1),llGetSubString(m,2,2),llGetSubString(m,3,3), \
                                llGetSubString(m,4,4),llGetSubString(m,5,5)]), \
                                (llSubStringIndex(m,llGetSubString(m,6,6)) < 6) << 1, -1)
        #ifdef TIGHTLISTTYPEQUICKREAD
    return TightListTypeQuickRead(a,m);
            #undef TightListTypeQuickRead
        #endif
    #elif defined(TIGHTLISTTYPEQUICKREAD)
    return TightListTypeQuickRead(a,m);


    #endif
    #ifdef TIGHTLISTTYPEQUICKREAD //}
}
        #ifdef NICENAMES
            #undef a
            #undef m
        #endif
    #endif
#endif
#ifdef TIGHTLISTTYPELENGTH
#ifdef QUICKREAD
#define TightListTypeLength(a) ((TightListTypeQuickRead(a) != []) >> 1)
#else
    #ifdef NICENAMES
        #define a input
        #define m seperators
    #endif
integer TightListTypeLength(string a)
{
    string m = llGetSubString(a,ZERO_INTEGER,6);
    return ((llParseStringKeepNulls(llDeleteSubString(a,ZERO_INTEGER,5), [],[a=llGetSubString(m,ZERO_INTEGER,ZERO_INTEGER),
           llGetSubString(m,1,1),llGetSubString(m,2,2),llGetSubString(c,3,3),
           llGetSubString(m,4,4),llGetSubString(m,5,5)]) != []) + (llSubStringIndex(m,llGetSubString(m,6,6)) < 6)) >> 1;
}
    #ifdef NICENAMES
        #undef a
        #undef m
    #endif
#endif
#endif
#ifdef TIGHTLISTTYPEENTRYTYPE
    #ifdef NICENAMES
        #define a input
        #define b index
        #define m seperators
    #endif
integer TightListTypeEntryType(string a, integer b)
{
    string m = llGetSubString(a,ZERO_INTEGER,6);
    return llSubStringIndex(m, a) + ((a = llList2String(TightListTypeQuickRead(a, m),  b << 1)) != "");
}
    #ifdef NICENAMES
        #undef a
        #undef b
        #undef m
    #endif
#endif
#ifdef TIGHTLISTTYPEPARSE
    #ifdef NICENAMES
        #define a input
        #define b partial
        #define c pos
        #define d type
        #define e sub_pos
        #define f current
        #define m seperators
    #endif
list TightListTypeParse(string a) {
    list b;
    if(llStringLength(a) > 6)
    {
        string m = llGetSubString(a,ZERO_INTEGER,6);
        integer c = ([] != (b = TightListTypeQuickRead(a, m)));
        integer d = ZERO_INTEGER;
        integer e = ZERO_INTEGER;
        do
        {
            list f = (list)(a = llList2String(b, e= -~c));//TYPE_STRING || TYPE_INVALID (though we don't care about invalid)
            if(!(d = llSubStringIndex(m, llList2String(b,c))))//TYPE_INTEGER
                f = (list)((integer)a);
            else if(d == 1)//TYPE_FLOAT
                f = (list)((float)a);
            else if(d == 3)//TYPE_KEY
                f = (list)((key)a);
            else if(d == 4)//TYPE_VECTOR
                f = (list)((vector)a);
            else if(d == 5)//TYPE_ROTATION
                f = (list)((rotation)a);
            b = llListReplaceList(b, f, c, e);
        }while((c= -~e) & 0x80000000);
    }
    return b;
}
    #ifdef NICENAMES
        #undef a
        #undef b
        #undef c
        #undef d
        #undef e
        #undef f
        #undef m
    #endif
#endif
#ifdef TIGHTLISTTYPEDUMP
    #ifdef NICENAMES
        #define a input
        #define b seperators
        #define c cumulator
        #define d counter
        #define e type
        #define f buffer
    #endif
string TightListTypeDump(list a, string b) {//This function is dangerous
    b += TIGHTLISTDUMPCHARS;
    string c = TLD_TYPECAST_DUMPLIST2STRING(a);
    integer d = ZERO_INTEGER;
    do
        if(~llSubStringIndex(c,llGetSubString(b,d,d)))
            b = llDeleteSubString(b,d,d);
        else
            d = -~d;
    while(d<6);
    b = llGetSubString(b,ZERO_INTEGER,5);
    #ifndef PURE_ALL_TLTD
        #if defined(ALL_TLTD) || defined(TLTDV) || defined(TLTDR) || defined(TLTDF) || defined(TLTDI) || defined(TLTDS) || defined(TLTDK)
        string f = c =  "";
        #else
        c =  "";
            #ifdef f
                #undef f
            #endif
            #define f llList2String(a,d)
        #endif
    #else
        #ifdef f
            #undef f
        #endif
        #define f PURE_ALL_TLTD(a,d)
    #endif
    if((d = (a != [])))
    {
        do
        {
            integer e = ~-llGetListEntryType(a, d = ~-d);
#ifndef PURE_ALL_TLTD
    #if defined(ALL_TLTD) || defined(TLTDV) || defined(TLTDR) || defined(TLTDF) || defined(TLTDI) || defined(TLTDS) || defined(TLTDK)
        #if defined(TLTDV) && defined(TLTDR) && defined(TLTDF) && defined(TLTDI) && defined(TLTDS) && defined(TLTDK)
            #ifdef ALL_TLTD //you use this like #define ALL_TLTD(type, data, pos, out) if(type == TYPE_*){  out = your code( llList2*(data, pos)); }
            ALL_TLTD(e, a, d, f);
            else
            #endif
            if(e == 4)//TYPE_VECTOR - 1
                f = TLTDV(a,d);
            else if(e == 5)//TYPE_ROTATION - 1
                f = TLTDR(a,d);
            else if(e == 1)//TYPE_FLOAT - 1
                f = TLTDF(a,d);
            else if(e == 0)//TYPE_INTEGER - 1
                f = TLTDI(a,d);
            else if(e == 3)//TYPE_KEY - 1
                f = TLTDK(a,d);
            else if(e == 2)//TYPE_STRING - 1
                f = TLTDS(a,d);
        #// //}
        #else //{
            #ifdef ALL_TLTD //you use this like #define ALL_TLTD(type, data, pos, out) if(type == TYPE_*){  out = your code( llList2*(data, pos)); }
            ALL_TLTD(e, a, d, f);
            else
            #endif


            #ifdef TLTDV //you use this like #define TLTDV(data, pos) your_func(llList2Vector(data, pos));
            if(e == 4)//TYPE_VECTOR - 1
                f = TLTDV(a,d);
            else
            #endif


            #ifdef TLTDR //you use this like #define TLTDR(data, pos) your_func(llList2Rotation(data, pos));
            if(e == 5)//TYPE_ROTATION - 1
                f = TLTDR(a,d);
            else
            #endif


            #ifdef TLTDF //you use this like #define TLTDF(data, pos) your_func(llList2Float(data, pos));
            if(e == 1)//TYPE_FLOAT - 1
                f = TLTDF(a,d);
            else
            #endif


            #ifdef TLTDI //you use this like #define TLTDI(data, pos) your_func(llList2Integer(data, pos));
            if(e == 0)//TYPE_INTEGER - 1
                f = TLTDI(a,d);
            else
            #endif


            #ifdef TLTDK //you use this like #define TLTDK(data, pos) your_func(llList2Key(data, pos));
            if(e == 3)//TYPE_KEY - 1
                f = TLTDK(a,d);
            else
            #endif


            #ifdef TLTDS //you use this like #define TLTDS(data, pos) your_func(llList2Key(data, pos));
            if(e == 2)//TYPE_STRING - 1
                f = TLTDS(a,d);
            else
            #endif
                f = llList2String(a,d);
        #endif
    #endif
#endif
            c = (c = llGetSubString(b,e,e)) + f + c;
        }while(d);
    }
    return b + c;
}
    #ifdef f
        #undef f
    #endif
    #ifdef NICENAMES
        #undef a
        #undef b
        #undef c
        #undef d
        #undef e
    #endif
#endif

#ifdef REMOVE_ZERO_INTEGER
    #undef REMOVE_ZERO_INTEGER
    #undef ZERO_INTEGER
#endif
```