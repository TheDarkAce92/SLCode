---
name: "MD5"
category: "example"
type: "example"
language: "LSL"
description: "The MD5 hashing algorithm should not be used because it is too easy to generate collisions (two inputs which result in the same hash). http://www.kb.cert.org/vuls/id/836068"
wiki_url: "https://wiki.secondlife.com/wiki/MD5"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

**Security Warning!**

The MD5 hashing algorithm should not be used because it is too easy to generate collisions (two inputs which result in the same hash). [http://www.kb.cert.org/vuls/id/836068](http://www.kb.cert.org/vuls/id/836068)

Preforms a MD5 Hash on the text.  Similar to and SHA1 hash, although less secure. **MD5 should not be used.** Two versions of the function are provided, one for UTF-8 Strings (all strings in LSL are UTF-8) and the other is for Base64 Strings (you need to tell it how many bits long the data is).

There is also an SHA-1 & two SHA-2 implementations (224 & 256).

View [http://en.wikipedia.org/wiki/MD5](http://en.wikipedia.org/wiki/MD5) for more information.

See the talk page for a discussion regarding working status.

```lsl
//////////////////////////////////////////////////////////////////////////////////////
//
//	UTF-8 MD5
//	Version 1.2 Beta
//	ESL Compiled: "Dec 28 2011", "23:35:35"
//	Copyright (C) 2012  Strife Onizuka
//	Based on Pseudo-code from http://en.wikipedia.org/wiki/MD5
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
//               Combined Library v1.0               //
//             "Dec 28 2011", "23:35:35"             //
//  Copyright (C) 2004-2012, Strife Onizuka (cc-by)  //
//    http://creativecommons.org/licenses/by/3.0/    //
//===================================================//
//{

string TrimRight(string src, string chrs)//LSLEditor Unsafe, LSO Safe
{
    integer i = llStringLength(src);
    do ; while(~llSubStringIndex(chrs, llGetSubString(src, i = ~-i, i)) && i);
    return llDeleteSubString(src, -~(i), 0x7FFFFFF0);
}

string hexc="0123456789abcdef";

//} Combined Library

list k1 = [
    0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee, 0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
    0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be, 0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821];
list k2 = [
    0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa, 0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
    0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed, 0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a];
list k3 = [
    0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c, 0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
    0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05, 0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665];
list k4 = [
    0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039, 0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
    0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1, 0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391];

string UTF8_MD5(string plain) {
    integer H1 = 0x67452301;
    integer H2 = 0xEFCDAB89;
    integer H3 = 0x98BADCFE;
    integer H4 = 0x10325476;

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
    integer S = 0;
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
            T = llBase64ToInteger(buf = llGetSubString(plain, T = (((i + j) << 4) / 3), T+6)) << (S = (((i + j) % 3) << 1));
            if(S)
                T = T | (llBase64ToInteger("A" + (llDeleteSubString(buf, 0, 1))) >> (6 - S));
            x += (T = ((T << 24) | ((T & 0xFF00) << 8) | ((T >> 8) & 0xFF00) | ((T >> 24) & 0xFF)));

            S = A + llList2Integer(k1, j) + T + (D ^ (B & (C ^ D)));
            T = ((j & 3) * 5) + 7;//llList2Integer([7, 12, 17, 22], j & 3);
            A = D;
            D = C;
            C = B;
            B += (((S) << (T)) | (((S) >> (32 - (T))) & ~(0xffFFffFF << (T))));
        }
        while(16 > (j = -~j));
        do
        {
            S = A + llList2Integer(k2, j & 15) + (C ^ (D & (B ^ C))) + llList2Integer(x, (-~(5 * j)) & 15);
            T = (0x140E0905 >> ((j & 3) << 3)) & 0x1F;//llList2Integer([5, 9, 14, 20], j & 3);
            A = D;
            D = C;
            C = B;
            B += (((S) << (T)) | (((S) >> (32 - (T))) & ~(0xffFFffFF << (T))));
        }
        while(32 > (j = -~j));
        do
        {
            S = A + llList2Integer(k3, j & 15) + (B ^ C ^ D) + llList2Integer(x, (3 * j + 5) & 15);
            T = (0x17100B04 >> ((j & 3) << 3)) & 0x1F;//llList2Integer([4, 11, 16, 23], j & 3);
            A = D;
            D = C;
            C = B;
            B += (((S) << (T)) | (((S) >> (32 - (T))) & ~(0xffFFffFF << (T))));
        }
        while(48 > (j = -~j));
        do
        {
            S = A + llList2Integer(k4, j & 15) + (C ^ (B | (~D))) + llList2Integer(x, (7 * j) & 15);
            T = (0x150F0A06 >> ((j & 3) << 3)) & 0x1F;//llList2Integer([6, 10, 15, 21], j & 3);
            A = D;
            D = C;
            C = B;
            B += (((S) << (T)) | (((S) >> (32 - (T))) & ~(0xffFFffFF << (T))));
        }
        while(64 > (j = -~j));
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

string Base64_MD5(string plain, integer bit_length) {
    integer H1 = 0x67452301;
    integer H2 = 0xEFCDAB89;
    integer H3 = 0x98BADCFE;
    integer H4 = 0x10325476;

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
//    llOwnerSay(llList2CSV([i,j]));
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
            T = llBase64ToInteger(buf = llGetSubString(plain, T = (((i + bit_length) << 4) / 3), T+6)) << (S = (((i + bit_length) % 3) << 1));
            if(S)
                T = T | (llBase64ToInteger("A" + (llDeleteSubString(buf, 0, 1))) >> (6 - S));
            x += (T = ((T << 24) | ((T & 0xFF00) << 8) | ((T >> 8) & 0xFF00) | ((T >> 24) & 0xFF)));

            S = A + llList2Integer(k1, bit_length) + T + (D ^ (B & (C ^ D)));
            T = ((bit_length & 3) * 5) + 7;//llList2Integer([7, 12, 17, 22], bit_length & 3);
            A = D;
            D = C;
            C = B;
            B += (((S) << (T)) | (((S) >> (32 - (T))) & ~(0xffFFffFF << (T))));
        }
        while(16 > (bit_length = -~bit_length));
        do
        {
            S = A + llList2Integer(k2, bit_length & 15) + (C ^ (D & (B ^ C))) + llList2Integer(x, (-~(5 * bit_length)) & 15);
            T = (0x140E0905 >> ((bit_length & 3) << 3)) & 0x1F;//llList2Integer([5, 9, 14, 20], bit_length & 3);
            A = D;
            D = C;
            C = B;
            B += (((S) << (T)) | (((S) >> (32 - (T))) & ~(0xffFFffFF << (T))));
        }
        while(32 > (bit_length = -~bit_length));
        do
        {
            S = A + llList2Integer(k3, bit_length & 15) + (B ^ C ^ D) + llList2Integer(x, (3 * bit_length + 5) & 15);
            T = (0x17100B04 >> ((bit_length & 3) << 3)) & 0x1F;//llList2Integer([4, 11, 16, 23], bit_length & 3);
            A = D;
            D = C;
            C = B;
            B += (((S) << (T)) | (((S) >> (32 - (T))) & ~(0xffFFffFF << (T))));
        }
        while(48 > (bit_length = -~bit_length));
        do
        {
            S = A + llList2Integer(k4, bit_length & 15) + (C ^ (B | (~D))) + llList2Integer(x, (7 * bit_length) & 15);
            T = (0x150F0A06 >> ((bit_length & 3) << 3)) & 0x1F;//llList2Integer([6, 10, 15, 21], bit_length & 3);
            A = D;
            D = C;
            C = B;
            B += (((S) << (T)) | (((S) >> (32 - (T))) & ~(0xffFFffFF << (T))));
        }
        while(64 > (bit_length = -~bit_length));
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
    string out = UTF8_MD5(in);
    float t = llGetTime();
    llOwnerSay(llDumpList2String(([out,t,llStringLength(in)]),","));
    if((answer = llToLower(answer)))
    {
        llOwnerSay(answer);
        return answer == out;
    }
    return TRUE;
}

integer secret;

default
{

    state_entry()
    {
        llListen(0, "", "", "");
        llListen(1, "", "", "");
        if(go("","D41D8CD98F00B204E9800998ECF8427E"))
            if(go("abc","900150983CD24FB0D6963F7D28E17F72"))
                go("The quick brown fox jumps over the lazy dog","9E107D9D372BB6826BD81D3542A419D6");
//        llOwnerSay((string)llGetTime());
    }
    listen(integer a, string b, key c, string d)
    {
        if(a)
            secret = (integer)d;
        else
        {
            llOwnerSay(UTF8_MD5(d));
            llOwnerSay(UTF8_MD5(d + ":" + (string)secret));
            llOwnerSay(llMD5String(d,secret));
        }
    }
}
```