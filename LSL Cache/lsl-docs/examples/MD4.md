---
name: "MD4"
category: "example"
type: "example"
language: "LSL"
description: "The MD4 hashing algorithm should not be used because it is too easy to generate collisions (two inputs which result in the same hash)."
wiki_url: "https://wiki.secondlife.com/wiki/MD4"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

**Security Warning!**

The MD4 hashing algorithm should not be used because it is too easy to generate collisions (two inputs which result in the same hash).

Preforms a MD4 Hash on the text. Similar to the MD5 hash. **MD4 should not be used.** This code is provided for the sake of completeness. Two versions of the function are provided, one for UTF-8 Strings (all strings in LSL are UTF-8) and the other is for Base64 Strings (you need to tell it how many bits long the data is).

There is also an SHA-1 & two SHA-2 implementations (224 & 256).

View [http://en.wikipedia.org/wiki/MD4](http://en.wikipedia.org/wiki/MD4) for more information.

```lsl
//////////////////////////////////////////////////////////////////////////////////////
//
//	UTF-8 MD4
//	Version 1.1 Beta
//	ESL Compiled: "Dec 13 2010", "01:20:46"
//	Copyright (C) 2010  Strife Onizuka
//	Based on code RFC 1320
//
//
//	This library is free software; you can redistribute it and/or
//	modify it under the terms of the GNU Lesser General Public License
//	as published by the Free Software Foundation;
//	version 3 of the License.
//
//	This library is distributed in the hope that it will be useful,
//	but WITHOUT ANY WARRANTY; without even the implied warranty of
//	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//	GNU Lesser General Public License for more details.
//
//	You should have received a copy of the GNU Lesser General Public License
//	along with this library.  If not, see
//	or write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330,
//	Boston, MA  02111-1307  USA
//
//////////////////////////////////////////////////////////////////////////////////////

//===================================================//
//                 Combined Library                  //
//             "Dec 13 2010", "01:20:46"             //
//  Copyright (C) 2004-2008, Strife Onizuka (cc-by)  //
//    http://creativecommons.org/licenses/by/3.0/    //
//===================================================//
//{

string TrimRight(string src, string chrs)//LSLEditor Safe, LSO Safe
{
    integer i = llStringLength(src);
    integer j = i;
    do ; while(~llSubStringIndex(chrs, llGetSubString(src, i = ~-(j = i), i)) && j);
    return llDeleteSubString(src, j, 0x7FFFFFF0);
}

string hexc="0123456789ABCDEF";

//} Combined Library

list r1 = [3,  7, 11, 19];
list r2 = [3,  5,  9, 13];
list r3 = [3,  9, 11, 15];

list i3 = [0,  8,  4, 12,    2, 10,  6, 14,       1,  9,  5, 13,    3, 11,  7, 15];

string UTF8_MD4(string plain) {
    integer H1 = 1732584193;
    integer H2 = -271733879;
    integer H3 = -1732584194;
    integer H4 = 271733878;

    //OR on the extra bit.
    integer j = llStringLength(plain = llStringToBase64(plain));
    integer T = 0x80000000;
    if (j) {
        do ; while (llGetSubString(plain, (j = ~-j), j) == "=");
        j = (-6 * ~j) & -8;
        T = llBase64ToInteger((llGetSubString(plain, -4, j / 6)) + "AAAAAA") | (0x00000080 << ((j % 3) << 3));
    }
    integer b = ((j + 40) >> 5) | 15;
    string buf = "AAA";
    integer i = -5;
    do buf += buf; while((i = -~i));
//    llOwnerSay(llList2CSV([i,j]));
    plain = llGetSubString( llDeleteSubString(plain, -4, -1) +
                            llGetSubString(llIntegerToBase64(T), 0, 5) +
                            buf, 0, ((b << 4) / 3) - 7) +
            llGetSubString(llIntegerToBase64((((j & 0xFF) << 20) | ((j & 0xFF00) << 4) | ((j >> 12) & 0xFF0) | ((j >> 28) & 0xF)) >> ((b % 3) << 1)), 0, 5) +
            "AAAAAAAA";
    integer S = i = 0;
    list x;
    do
    {
        integer A = H1;
        integer B = H2;
        integer C = H3;
        integer D = H4;

        j = 0;
        x = [];
        do
        {
            T = llBase64ToInteger(buf = llGetSubString(plain, T = ((i + j) << 4) / 3, T+6)) << (S = (((i + j) % 3) << 1));
            if(S)
                T = T | (llBase64ToInteger("A" + (llDeleteSubString(buf, 0, 1))) >> (6 - S));
            x += (T = ((T << 24) | ((T & 0xFF00) << 8) | ((T >> 8) & 0xFF00) | ((T >> 24) & 0xFF)));

            S = A + (D ^ (B & (C ^ D))) + T;
            T = llList2Integer(r1, j & 3);
            A = D;
            D = C;
            C = B;
            B = (S << T) | ((S >> (32 - T)) & ~(-1 << T));
        }
        while(16 > (j = -~j));
        do
        {
            S = A + ((B & C) | (B & D) | (C & D)) + llList2Integer(x, (-~(((j << 2) - 65) % 15))) + 1518500249;
            T = llList2Integer(r2, j & 3);
            A = D;
            D = C;
            C = B;
            B = (S << T) | ((S >> (32 - T)) & ~(-1 << T));
        }
        while(32 > (j = -~j));
        do
        {
            S = A + (B ^ C ^ D) + llList2Integer(x, llList2Integer(i3, j & 15)) + 1859775393;
            T = llList2Integer(r3, j & 3);
            A = D;
            D = C;
            C = B;
            B = (S << T) | ((S >> (32 - T)) & ~(-1 << T));
        }
        while(48 > (j = -~j));
//        llOwnerSay(llList2CSV(x));
        H1 += A;
        H2 += B;
        H3 += C;
        H4 += D;
    }while(b > (i += 16));
    x = [H4, H3, H2, H1];
    i = -4;
    buf = "";
    do
    {
        T = llList2Integer(x,i);
        j = 32;
        do
            buf = llGetSubString(hexc, b = ((T >> (j - 4)) & 0xF), b) + llGetSubString(hexc, b = ((T >> (j - 8)) & 0xF), b) + buf;
        while ((j -= 8));
    }while ((i = -~i));
    return buf;
}

string Base64_MD4(string plain, integer bit_length) { //$[E20009]
    integer H1 = 1732584193;
    integer H2 = -271733879;
    integer H3 = -1732584194;
    integer H4 = 271733878;

    //OR on the extra bit.
    integer b = (~-(((bit_length + 552) & -512) >> 5));
    integer T = llBase64ToInteger((TrimRight(llGetSubString(plain = llStringToBase64(plain), -4, -1),"=")) + "AAAA");
    string buf = "AAA";
    integer i = -5;
    do buf += buf; while((i = -~i));
    if(bit_length)
    {
        i = 0x800000;
        if(T & 0xFF00)
            i = 0x00000080;
        else if(T & 0xFF0000)
            i = 0x00008000;
    }
    else
        T = 0x80000000;//T is corrupt because of https://jira.secondlife.com/browse/SVC-104
//    llOwnerSay(llList2CSV([i,bit_length]));
    plain = llGetSubString( llDeleteSubString(plain, -4, -1) +
                            llGetSubString(llIntegerToBase64(T | i), 0, 5) +
                            buf, 0, ((b << 4) / 3) - 7) +
            llGetSubString(llIntegerToBase64((((bit_length & 0xFF) << 20) | ((bit_length & 0xFF00) << 4) | ((bit_length >> 12) & 0xFF0) | ((bit_length >> 28) & 0xF)) >> ((b % 3) << 1)), 0, 5) +
            "AAAAAAAA";
    integer S = i = 0;
    list x;
    do
    {
        integer A = H1;
        integer B = H2;
        integer C = H3;
        integer D = H4;

        bit_length = 0;
        x = [];
        do
        {
            T = llBase64ToInteger(buf = llGetSubString(plain, T = ((i + bit_length) << 4) / 3, T+6)) << (S = (((i + bit_length) % 3) << 1));
            if(S)
                T = T | (llBase64ToInteger("A" + (llDeleteSubString(buf, 0, 1))) >> (6 - S));
            x += (T = ((T << 24) | ((T & 0xFF00) << 8) | ((T >> 8) & 0xFF00) | ((T >> 24) & 0xFF)));

            S = A + (D ^ (B & (C ^ D))) + T;
            T = llList2Integer(r1, bit_length & 3);
            A = D;
            D = C;
            C = B;
            B = (S << T) | ((S >> (32 - T)) & ~(-1 << T));
        }
        while(16 > (bit_length = -~bit_length));
        do
        {
            S = A + ((B & C) | (B & D) | (C & D)) + llList2Integer(x, (-~(((bit_length << 2) - 65) % 15))) + 1518500249;
            T = llList2Integer(r2, bit_length & 3);
            A = D;
            D = C;
            C = B;
            B = (S << T) | ((S >> (32 - T)) & ~(-1 << T));
        }
        while(32 > (bit_length = -~bit_length));
        do
        {
            S = A + (B ^ C ^ D) + llList2Integer(x, llList2Integer(i3, bit_length & 15)) + 1859775393;
            T = llList2Integer(r3, bit_length & 3);
            A = D;
            D = C;
            C = B;
            B = (S << T) | ((S >> (32 - T)) & ~(-1 << T));
        }
        while(48 > (bit_length = -~bit_length));
//        llOwnerSay(llList2CSV(x));
        H1 += A;
        H2 += B;
        H3 += C;
        H4 += D;
    }while(b > (i += 16));
    x = [H4, H3, H2, H1];
    i = -4;
    buf = "";
    do
    {
        T = llList2Integer(x,i);
        bit_length = 32;
        do
            buf = llGetSubString(hexc, b = ((T >> (bit_length - 4)) & 0xF), b) + llGetSubString(hexc, b = ((T >> (bit_length - 8)) & 0xF), b) + buf;
        while ((bit_length -= 8));
    }while ((i = -~i));
    return buf;
}

integer go(string in, string answer)
{
    llOwnerSay("");
    llResetTime();
    string out = UTF8_MD4(in);
    float t = llGetTime();
    llOwnerSay(llDumpList2String(([out,t,llStringLength(in)]),","));
    if(answer)
    {
        llOwnerSay(answer);
        return answer == out;
    }
    return TRUE;
}

default
{

    state_entry()
    {
        llListen(0, "", "", "");
        if(go("","31D6CFE0D16AE931B73C59D7E0C089C0"))
            if(go("abc","A448017AAF21D8525FC10AE87AA6729D"))
                go("The quick brown fox jumps over the lazy dog","1BEE69A46BA811185C194762ABAEAE90");
//        llOwnerSay((string)llGetTime());
    }
    listen(integer a, string b, key c, string d)
    {
        llOwnerSay(UTF8_MD4(d));
    }
}
```