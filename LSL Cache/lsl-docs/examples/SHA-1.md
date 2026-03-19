---
name: "SHA-1"
category: "example"
type: "example"
language: "LSL"
description: "There are dire security implications to changing the K constants (these are the hex values near the end of the lines marked with \"//k\" comments). https://malicioussha1.github.io/"
wiki_url: "https://wiki.secondlife.com/wiki/SHA-1"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

**Security Warning!** There are dire security implications to changing the K constants (these are the hex values near the end of the lines marked with "//k" comments). https://malicioussha1.github.io/  NEW  LSL now includes its own (faster) llSHA1String function, which removes the need for the UTF8_SHA1 variant from this library. Also consider the more secure llSHA256String. Performs a SHA-1 hash on the text. This is similar to an MD5 hash, but is slightly more secure. Two versions of the function are provided: one for UTF-8 strings (all strings in LSL are UTF-8) and another for Base64 strings (for which you need to specify the data length in bits). There are also two SHA-2 script implementations (SHA-256 & SHA-224), though consider the faster llSHA256String provided by LSL itself.

View  [SHA-1](https://en.wikipedia.org/wiki/SHA-1) for more information.

```lsl
//////////////////////////////////////////////////////////////////////////////////////
//
//	UTF-8 SHA-1 160
//	Version 1.3
//	ESL Compiled: "Nov 26 2013", "00:11:59"
//	Copyright (C) 2013  Strife Onizuka
//	Based on Pseudo-code from http://en.wikipedia.org/wiki/SHA-1
//	https://wiki.secondlife.com/wiki/SHA-1
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
//             "Nov 26 2013", "00:11:59"             //
//  Copyright (C) 2004-2012, Strife Onizuka (cc-by)  //
//    http://creativecommons.org/licenses/by/3.0/    //
//===================================================//
//{

string hexc="0123456789ABCDEF";

//} Combined Library

string Base64_SHA1(string plain, integer bit_length) {
    integer H1 = 0x67452301;
    integer H2 = 0xefcdab89;
    integer H3 = 0x98badcfe;
    integer H4 = 0x10325476;
    integer H5 = 0xc3d2e1f0;

    integer b = ((bit_length + 40) >> 5) | 15;//this works because we want the value to be one less than the next appropriate multiple of 16.
    string buf = "AAA";
    integer i = -5;
    do buf += buf; while((i = -~i));
    integer S = (6 * llSubStringIndex((plain)+"=", "="));
    integer T = 0x80000000;
    if(bit_length) {
        if(S < bit_length) {
            plain = llDeleteSubString(plain, S, 0x7FFFFFF0);
            i = ((bit_length + 23) / 24) * 24;
            do
                plain += buf;
            while((S += 576) < i);
        }
        T = 23 - ((~-(bit_length)) % 24);
        T = (llBase64ToInteger(llGetSubString((llGetSubString(plain = llGetSubString(plain, 0, (bit_length / 6) | 3), -4, (~-(S / 6)))) + "AAAAA", 0, 5)) & (0xFFFFFF00 << T)) | (0x00000080 << T);
    }
    //llOwnerSay(llList2CSV([b,j, llStringLength(buf), llIntegerToBase64(j << (6 - ((b % 3) << 1)))]));
    plain = llInsertString( llDeleteSubString(plain, -4, -1) +
                            llGetSubString(llIntegerToBase64(T), 0, 5) + buf, (-~((b << 4) / 3)),
                            llGetSubString(llIntegerToBase64(bit_length << (6 - ((b % 3) << 1))), 0, 5));
    //llOwnerSay(llList2CSV([llStringLength(plain), Base64ToHex(plain), T]));
    list x;
    i = 0;
    do {
        integer A = H1;
        integer B = H2;
        integer C = H3;
        integer D = H4;
        integer E = H5;
        x = (list)(bit_length = 0);//the zero gets flushed off the stack by the later loops
        do {
            T = llBase64ToInteger(buf = llGetSubString(plain, T = ((i + bit_length) << 4) / 3, T+6)) << (S = ((i + bit_length) % 3) << 1);
            if(S)
                T = T | (llBase64ToInteger("A" + (llDeleteSubString(buf, 0, 1))) >> (6 - S));
//            llOwnerSay("W["+(string)j+"]="+hex(T));
            x += T;
            T += ((A << 5) | ((A >> 27) & 0x1F)) + (D ^ (B & (C ^ D))) + E + 0x5a827999;//k
            E = D;
            D = C;
            C = ((B << 30) | ((B >> 2) & 0x3FFFFFFF));
            B = A;
            A = T;
        } while(16 > (bit_length = -~bit_length));
//		llOwnerSay(llList2CSV(hexm(x)));
        do {
            S = llList2Integer(x,  -3) ^ llList2Integer(x,  -8) ^ llList2Integer(x, -14) ^ llList2Integer(x, -16);
            x = llList2List(x + (T = ((S << 1) | !!(S & 0x80000000))), -16, -1);
//            llOwnerSay("W["+(string)j+"]="+hex(T));
            T += ((A << 5) | ((A >> 27) & 0x1F)) + (D ^ (B & (C ^ D))) + E + 0x5a827999;//k
            E = D;
            D = C;
            C = ((B << 30) | ((B >> 2) & 0x3FFFFFFF));
            B = A;
            A = T;
        } while(20 > (bit_length = -~bit_length));
        do {
            S = llList2Integer(x,  -3) ^ llList2Integer(x,  -8) ^ llList2Integer(x, -14) ^ llList2Integer(x, -16);
            x = llList2List(x + (T = ((S << 1) | !!(S & 0x80000000))), -16, -1);
//            llOwnerSay("W["+(string)j+"]="+hex(T));
            T += ((A << 5) | ((A >> 27) & 0x1F)) + (B ^ C ^ D) + E + 0x6ed9eba1;//k
            E = D;
            D = C;
            C = ((B << 30) | ((B >> 2) & 0x3FFFFFFF));
            B = A;
            A = T;
        } while(40 > (bit_length = -~bit_length));
        do {
            S = llList2Integer(x,  -3) ^ llList2Integer(x,  -8) ^ llList2Integer(x, -14) ^ llList2Integer(x, -16);
            x = llList2List(x + (T = ((S << 1) | !!(S & 0x80000000))), -16, -1);
//            llOwnerSay("W["+(string)j+"]="+hex(T));
            T += ((A << 5) | ((A >> 27) & 0x1F)) + ((B & C) | (B & D) | (C & D)) + E + 0x8f1bbcdc;//k
            E = D;
            D = C;
            C = ((B << 30) | ((B >> 2) & 0x3FFFFFFF));
            B = A;
            A = T;
        } while(60 > (bit_length = -~bit_length));
        do {
            S = llList2Integer(x,  -3) ^ llList2Integer(x,  -8) ^ llList2Integer(x, -14) ^ llList2Integer(x, -16);
            x = llList2List(x + (T = ((S << 1) | !!(S & 0x80000000))), -16, -1);
//            llOwnerSay("W["+(string)j+"]="+hex(T));
            T += ((A << 5) | ((A >> 27) & 0x1F)) + (B ^ C ^ D) + E + 0xca62c1d6;//k
            E = D;
            D = C;
            C = ((B << 30) | ((B >> 2) & 0x3FFFFFFF));
            B = A;
            A = T;
        } while(80 > (bit_length = -~bit_length));
        H1 += A;
        H2 += B;
        H3 += C;
        H4 += D;
        H5 += E;
    } while(b > (i += 16));
    x = [H1, H2, H3, H4, H5];
    i = -5;
    buf = "";
    do {
        T = llList2Integer(x,i);
        bit_length = 32;
        do {
            buf += llGetSubString(hexc, b = ((T >> (bit_length -= 4)) & 0xF), b);
        } while (bit_length);
    } while ((i = -~i));
    return buf;
}

string UTF8_SHA1(string plain) {
    integer H1 = 0x67452301;
    integer H2 = 0xefcdab89;
    integer H3 = 0x98badcfe;
    integer H4 = 0x10325476;
    integer H5 = 0xc3d2e1f0;

    //ORing on the extra bit. Since we are working in base64 the byte bounderies aren't where we want them.
    //So we get the last byte group and append our extra bit onto it. It contains either 1, 2, or 3 bytes.
    integer j = llSubStringIndex((plain = llStringToBase64(plain))+"=", "=");
    integer T = 0x80000000;
    if(j) {
        j = (6 * (T = j)) & -8;//length in bits
        T = llBase64ToInteger(llGetSubString((llGetSubString(plain, -4, (~-(T)))) + "AAAA", 0, 5)) | (0x00000080 << ((j % 3) << 3));
    }
    integer b = ((j + 40) >> 5) | 15;//this works because we want the value to be one less than the next appropriate multiple of 16.
    string buf = "AAA";
    integer i = -5;
    do buf += buf; while((i = -~i));//We need 85, 96 is close enough
    //llOwnerSay(llList2CSV([b,j, llStringLength(buf), llIntegerToBase64(j << (6 - ((b % 3) << 1)))]));
    plain = llInsertString( llDeleteSubString(plain, -4, -1) +
                            llGetSubString(llIntegerToBase64(T), 0, 5) + buf, (b << 4) / 3,
                            llGetSubString(llIntegerToBase64(j >> ((b % 3) << 1)), 0, 5));
    //llOwnerSay(llList2CSV([llStringLength(plain), Base64ToHex(plain)]));
    list x;
    integer S = 0;
    do {
        integer A = H1;
        integer B = H2;
        integer C = H3;
        integer D = H4;
        integer E = H5;
        x = (list)(j = 0);//the zero gets flushed off the stack by the later loops
        do {
            T = llBase64ToInteger(buf = llGetSubString(plain, T = ((i + j) << 4) / 3, T+6)) << (S = ((i + j) % 3) << 1);
            if(S)
                T = T | (llBase64ToInteger("A" + (llDeleteSubString(buf, 0, 1))) >> (6 - S));
//            llOwnerSay("W["+(string)j+"]="+hex(T));
            x += T;
            T += ((A << 5) | ((A >> 27) & 0x1F)) + (D ^ (B & (C ^ D))) + E + 0x5a827999;//k
            E = D;
            D = C;
            C = ((B << 30) | ((B >> 2) & 0x3FFFFFFF));
            B = A;
            A = T;
        } while(16 > (j = -~j));
//		llOwnerSay(llList2CSV(hexm(x)));
        do {
            S = llList2Integer(x,  -3) ^ llList2Integer(x,  -8) ^ llList2Integer(x, -14) ^ llList2Integer(x, -16);
            x = llList2List(x + (T = ((S << 1) | !!(S & 0x80000000))), -16, -1);
//            llOwnerSay("W["+(string)j+"]="+hex(T));
            T += ((A << 5) | ((A >> 27) & 0x1F)) + (D ^ (B & (C ^ D))) + E + 0x5a827999;//k
            E = D;
            D = C;
            C = ((B << 30) | ((B >> 2) & 0x3FFFFFFF));
            B = A;
            A = T;
        } while(20 > (j = -~j));
        do {
            S = llList2Integer(x,  -3) ^ llList2Integer(x,  -8) ^ llList2Integer(x, -14) ^ llList2Integer(x, -16);
            x = llList2List(x + (T = ((S << 1) | !!(S & 0x80000000))), -16, -1);
//            llOwnerSay("W["+(string)j+"]="+hex(T));
            T += ((A << 5) | ((A >> 27) & 0x1F)) + (B ^ C ^ D) + E + 0x6ed9eba1;//k
            E = D;
            D = C;
            C = ((B << 30) | ((B >> 2) & 0x3FFFFFFF));
            B = A;
            A = T;
        } while(40 > (j = -~j));
        do {
            S = llList2Integer(x,  -3) ^ llList2Integer(x,  -8) ^ llList2Integer(x, -14) ^ llList2Integer(x, -16);
            x = llList2List(x + (T = ((S << 1) | !!(S & 0x80000000))), -16, -1);
//            llOwnerSay("W["+(string)j+"]="+hex(T));
            T += ((A << 5) | ((A >> 27) & 0x1F)) + ((B & C) | (B & D) | (C & D)) + E + 0x8f1bbcdc;//k
            E = D;
            D = C;
            C = ((B << 30) | ((B >> 2) & 0x3FFFFFFF));
            B = A;
            A = T;
        } while(60 > (j = -~j));
        do {
            S = llList2Integer(x,  -3) ^ llList2Integer(x,  -8) ^ llList2Integer(x, -14) ^ llList2Integer(x, -16);
            x = llList2List(x + (T = ((S << 1) | !!(S & 0x80000000))), -16, -1);
//            llOwnerSay("W["+(string)j+"]="+hex(T));
            T += ((A << 5) | ((A >> 27) & 0x1F)) + (B ^ C ^ D) + E + 0xca62c1d6;//k
            E = D;
            D = C;
            C = ((B << 30) | ((B >> 2) & 0x3FFFFFFF));
            B = A;
            A = T;
        } while(80 > (j = -~j));
        H1 += A;
        H2 += B;
        H3 += C;
        H4 += D;
        H5 += E;
    } while(b > (i += 16));
    x = [H1, H2, H3, H4, H5];
    i = -5;
    buf = "";
    do {
        T = llList2Integer(x,i);
        j = 32;
        do {
            buf += llGetSubString(hexc, b = ((T >> (j -= 4)) & 0xF), b);
        } while (j);
    } while ((i = -~i));
    return buf;
}

integer go(string in, string answer) {
    llOwnerSay("");
    string b = llStringToBase64(in);
    integer len = (6 * llSubStringIndex((b)+"=", "=")) & -8;
    llResetTime();
    string outu = UTF8_SHA1(in);
    float tu = llGetTime();
    llOwnerSay(llList2CSV(([outu, tu, len])));
    llResetTime();
    string outb = Base64_SHA1(b, len);
    float tb = llGetTime();
    llOwnerSay(llList2CSV(([outb, tb, len])));
    if(answer) {
        llOwnerSay(llList2CSV(([answer, (answer == outu),(answer == outb)])));
        return (answer == outb) && (answer == outu);
    }
    return TRUE;
}

default
{
    state_entry()
    {
        if(Base64_SHA1("AAAA", 24) != "29E2DCFBB16F63BB0254DF7585A15BB6FB5E927D")
            llOwnerSay("Failed Base64_SHA1(\"AAAA\", 24)");
        if(go("", "DA39A3EE5E6B4B0D3255BFEF95601890AFD80709"))
        if(go("abc", "A9993E364706816ABA3E25717850C26C9CD0D89D"))
        if(go("The quick brown fox jumps over the lazy dog", "2FD4E1C67A2D28FCED849EE1BB76E7391B93EB12"))
            llOwnerSay("All Tests Passed!");
//        llOwnerSay((string)llGetTime());
    }
}
```