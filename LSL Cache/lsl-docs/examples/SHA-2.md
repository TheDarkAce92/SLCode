---
name: "SHA-2"
category: "example"
type: "example"
language: "LSL"
description: "NEW  LSL now includes the function llSHA256String."
wiki_url: "https://wiki.secondlife.com/wiki/SHA-2"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 SHA-256
- 2 SHA-224

 NEW  LSL now includes the function llSHA256String.

Performs an SHA-2 Hash on the text. Similar to an MD5 hash, but (slightly) more secure. Two versions of the function are provided, one for UTF-8 Strings (all strings in LSL are UTF-8) and the other is for Base64 Strings (you need to tell it how many bits long the data is).

View  [SHA-2](https://en.wikipedia.org/wiki/SHA-2) for more information.

## SHA-256

```lsl
//////////////////////////////////////////////////////////////////////////////////////
//
//	UTF-8 SHA-2 256
//	Version 1.4
//	ESL Compiled: "Nov 20 2013", "04:02:14"
//	Copyright (C) 2013  Strife Onizuka
//	Based on Pseudo-code from http://en.wikipedia.org/wiki/SHA2
//	https://wiki.secondlife.com/wiki/SHA2
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
//             "Nov 20 2013", "04:02:14"             //
//  Copyright (C) 2004-2012, Strife Onizuka (cc-by)  //
//    http://creativecommons.org/licenses/by/3.0/    //
//===================================================//
//{

string hexc="0123456789ABCDEF";

//} Combined Library

list k1 = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174];
list k2 = [
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2];

string UTF8_SHA_256(string plain) {
    integer H1 = 0x6a09e667;
    integer H2 = 0xbb67ae85;
    integer H3 = 0x3c6ef372;
    integer H4 = 0xa54ff53a;
    integer H5 = 0x510e527f;
    integer H6 = 0x9b05688c;
    integer H7 = 0x1f83d9ab;
    integer H8 = 0x5be0cd19;

    //ORing on the extra bit. Since we are working in base64 the byte bounderies aren't where we want them.
    //So we get the last byte group and append our extra bit onto it. It contains either 1, 2, or 3 bytes.
    integer j = llSubStringIndex((plain = llStringToBase64(plain))+"=", "=");
    integer T = 0x80000000;
    if(j) {
        j = (6 * (T = j)) & -8;//length in bits
        T = llBase64ToInteger(llGetSubString((llGetSubString(plain, -4, (~-(T)))) + "AAAAAA", 0, 5)) | (0x00000080 << ((j % 3) << 3));
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
        integer F = H6;
        integer G = H7;
        integer H = H8;
        x = (list)(j = 0);//the zero gets flushed off the stack by the later loop
        do {
            T = llBase64ToInteger(buf = llGetSubString(plain, T = (((i + j) << 4) / 3), T + 6)) << (S = (((i + j) % 3) << 1));
            if(S)
                T = T | (llBase64ToInteger("A" + (llDeleteSubString(buf, 0, 1))) >> (6 - S));
//            llOwnerSay("W["+(string)j+"]="+hex(T));
            x += T;
            T += H + (((E << 26) | ((E >>  6) & 0x03FFFFFF)) ^
                      ((E << 21) | ((E >> 11) & 0x001FFFFF)) ^
                      ((E <<  7) | ((E >> 25) & 0x000007F))) +
                     (G ^ (E & (F ^ G))) +
                     llList2Integer(k1, j);
            H = G;
            G = F;
            F = E;
            E = D + T;
            D = C;
            C = B;
            B = A;
            A = T + (((B << 30) | ((B >>  2) & 0x3FFFFFFF)) ^
                     ((B << 19) | ((B >> 13) & 0x0007FFFF)) ^
                     ((B << 10) | ((B >> 22) & 0x000003FF))) +
                    ((B & C) ^ (B & D) ^ (C & D));
        } while(16 > (j = -~j));
//		llOwnerSay(llList2CSV(hexm(x)));
        j = 0;
        do {
            x = llList2List(x, -16, -1);
            do {
                T = llList2Integer(x, -15);
                S = llList2Integer(x, -2);
                x += (T = llList2Integer(x,  -16) +
                         (((T << 25) | ((T >>  7) & 0x01FFFFFF)) ^
                          ((T << 14) | ((T >> 18) & 0x00003FFF)) ^
                          ((T >>  3) & 0x1FFFFFFF)) +
                         llList2Integer(x,  -7) +
                         (((S << 15) | ((S >> 17) & 0x00007FFF)) ^
                          ((S << 13) | ((S >> 19) & 0x00001FFF)) ^
                          ((S >> 10) & 0x03FFFFF)));
//                llOwnerSay("W["+(string)(j+16)+"]="+hex(T));
                T += H + (((E << 26) | ((E >>  6) & 0x03FFFFFF)) ^
                          ((E << 21) | ((E >> 11) & 0x001FFFFF)) ^
                          ((E <<  7) | ((E >> 25) & 0x0000007F))) +
                         (G ^ (E & (F ^ G))) + llList2Integer(k2, j);
                H = G;
                G = F;
                F = E;
                E = D + T;
                D = C;
                C = B;
                B = A;
                A = T + (((B << 30) | ((B >>  2) & 0x3FFFFFFF)) ^
                         ((B << 19) | ((B >> 13) & 0x0007FFFF)) ^
                         ((B << 10) | ((B >> 22) & 0x000003FF))) +
                        ((B & C) ^ (B & D) ^ (C & D));
            } while(3 & (j = -~j));
        } while(48 > j);
        H1 += A;
        H2 += B;
        H3 += C;
        H4 += D;
        H5 += E;
        H6 += F;
        H7 += G;
        H8 += H;
    } while(b > (i += 16));
    x = [H1, H2, H3, H4, H5, H6, H7, H8];
    i = -8;
    buf = "";
    do {
        T = llList2Integer(x,i);
        j = 32;
        do
            buf += llGetSubString(hexc, b = ((T >> (j -= 4)) & 0xF), b);
        while (j);
    } while ((i = -~i));
    return buf;
}

string Base64_SHA_256(string encoded, integer bit_length) {
    integer H1 = 0x6a09e667;
    integer H2 = 0xbb67ae85;
    integer H3 = 0x3c6ef372;
    integer H4 = 0xa54ff53a;
    integer H5 = 0x510e527f;
    integer H6 = 0x9b05688c;
    integer H7 = 0x1f83d9ab;
    integer H8 = 0x5be0cd19;

    integer b = ((bit_length + 40) >> 5) | 15;//this works because we want the value to be one less than the next appropriate multiple of 16.
    string buf = "AAA";
    integer i = -5;
    do buf += buf; while((i = -~i));
    integer S = (6 * llSubStringIndex((encoded)+"=", "="));
    integer T = 0x80000000;
    if(bit_length) {
        if(S < bit_length) {
            encoded = llDeleteSubString(encoded, S, 0x7FFFFFF0);
            i = ((bit_length + 23) / 24) * 24;
            do
                encoded += buf;
            while((S += 576) < i);
        }
        T = 23 - ((~-(bit_length)) % 24);
        T = (llBase64ToInteger(llGetSubString((llGetSubString(encoded = llGetSubString(encoded, 0, (bit_length / 6) | 3), -4, (~-(S / 6)))) + "AAAAAA", 0, 5)) & (0xFFFFFF00 << T)) | (0x00000080 << T);
    }
    //llOwnerSay(llList2CSV([b,j, llStringLength(buf), llIntegerToBase64(j << (6 - ((b % 3) << 1)))]));
    encoded = llInsertString( llDeleteSubString(encoded, -4, -1) +
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
        integer F = H6;
        integer G = H7;
        integer H = H8;
        x = (list)(bit_length = 0);//the zero gets flushed off the stack by the later loop
        do {
            T = llBase64ToInteger(buf = llGetSubString(encoded, T = (((i + bit_length) << 4) / 3), T+6)) << (S = (((i + bit_length) % 3) << 1));
            if(S)
                T = T | (llBase64ToInteger("A" + (llDeleteSubString(buf, 0, 1))) >> (6 - S));
//            llOwnerSay("W["+(string)j+"]="+hex(T));
            x += T;
            T += H + (((E << 26) | ((E >>  6) & 0x03FFFFFF)) ^
                      ((E << 21) | ((E >> 11) & 0x001FFFFF)) ^
                      ((E <<  7) | ((E >> 25) & 0x0000007F))) +
                     (G ^ (E & (F ^ G))) +
                     llList2Integer(k1, bit_length);
            H = G;
            G = F;
            F = E;
            E = D + T;
            D = C;
            C = B;
            B = A;
            A = T + (((B << 30) | ((B >>  2) & 0x3FFFFFFF)) ^
                     ((B << 19) | ((B >> 13) & 0x0007FFFF)) ^
                     ((B << 10) | ((B >> 22) & 0x000003FF))) +
                    ((B & C) ^ (B & D) ^ (C & D));
        } while(16 > (bit_length = -~bit_length));
//		llOwnerSay(llList2CSV(hexm(x)));
        bit_length = 0;
        do {
            x = llList2List(x, -16, -1);
            do {
                T = llList2Integer(x, -15);
                S = llList2Integer(x, -2);
                x += T = llList2Integer(x,  -16) +
                         (((T << 25) | ((T >>  7) & 0x01FFFFFF)) ^
                          ((T << 14) | ((T >> 18) & 0x00003FFF)) ^
                          ((T >> 3) & 0x1FFFFFFF)) +
                         llList2Integer(x,  -7) +
                         (((S << 15) | ((S >> 17) & 0x00007FFF)) ^
                          ((S << 13) | ((S >> 19) & 0x00001FFF)) ^
                          ((S >> 10) & 0x3FFFFF));
    //            llOwnerSay("W["+(string)(j+16)+"]="+hex(T));
                T += H + (((E << 26) | ((E >>  6) & 0x03FFFFFF)) ^
                          ((E << 21) | ((E >> 11) & 0x001FFFFF)) ^
                          ((E <<  7) | ((E >> 25) & 0x0000007F))) +
                         (G ^ (E & (F ^ G))) +
                         llList2Integer(k2, bit_length);
                H = G;
                G = F;
                F = E;
                E = D + T;
                D = C;
                C = B;
                B = A;
                A = T + (((B << 30) | ((B >>  2) & 0x3FFFFFFF)) ^
                         ((B << 19) | ((B >> 13) & 0x0007FFFF)) ^
                         ((B << 10) | ((B >> 22) & 0x000003FF))) +
                        ((B & C) ^ (B & D) ^ (C & D));
            } while(3 & (bit_length = -~bit_length));
        } while(48 > bit_length);
        H1 += A;
        H2 += B;
        H3 += C;
        H4 += D;
        H5 += E;
        H6 += F;
        H7 += G;
        H8 += H;
    } while(b > (i += 16));
    x = [H1, H2, H3, H4, H5, H6, H7, H8];
    i = -8;
    buf = "";
    do {
        T = llList2Integer(x,i);
        bit_length = 32;
        do
            buf += llGetSubString(hexc, b = ((T >> (bit_length -= 4)) & 0xF), b);
        while (bit_length);
    } while ((i = -~i));
    return buf;
}

integer go(string in, string answer) {
    llOwnerSay("");
    string b = llStringToBase64(in);
    integer len = (6 * llSubStringIndex((b)+"=", "=")) & -8;
    llResetTime();
    string outu = UTF8_SHA_256(in);
    float tu = llGetTime();
    llOwnerSay(llList2CSV(([outu, tu, len])));
    llResetTime();
    string outb = Base64_SHA_256(b, len);
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
        if(go("1","6B86B273FF34FCE19D6B804EFF5A3F5747ADA4EAA22F1D49C01E52DDB7875B4B"))
        if(go("22","785F3EC7EB32F30B90CD0FCF3657D388B5FF4297F2F9716FF66E9B69C05DDD09"))
        if(go("333","556D7DC3A115356350F1F9910B1AF1AB0E312D4B3E4FC788D2DA63668F36D017"))
        if(go("4444","79F06F8FDE333461739F220090A23CB2A79F6D714BEE100D0E4B4AF249294619"))
        if(go("","E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855"))
        if(go("foo","2C26B46B68FFC68FF99B453C1D30413413422D706483BFA0F98A5E886266E7AE"))
        if(go("abc","BA7816BF8F01CFEA414140DE5DAE2223B00361A396177A9CB410FF61F20015AD"))
        if(go("The quick brown fox jumps over the lazy dog","D7A8FBB307D7809469CA9ABCB0082E4F8D5651E46D3CDB762D02D0BF37C9E592"))
        if(go("D7A8FBB307D7809469CA9ABCB0082E4F8D5651E46D3CDB762D02D0BF37C9E592D7A8FBB307D7809469CA9ABCB0082E4F8D5651E46D3CDB762D02D0BF37C9E592D7A8FBB307D7809469CA9ABCB0082E4F8D5651E46D3CDB762D02D0BF37C9E592D7A8FBB307D7809469CA9ABCB0082E4F8D5651E46D3CDB762D02D0BF37C9E592D7A8FBB307D7809469CA9ABCB0082E4F8D5651E46D3CDB762D02D0BF37C9E592D7A8FBB307D7809469CA9ABCB0082E4F8D5651E46D3CDB762D02D0BF37C9E592D7A8FBB307D7809469CA9ABCB0082E4F8D5651E46D3CDB762D02D0BF37C9E592D7A8FBB307D7809469CA9ABCB0082E4F8D5651E46D3CDB762D02D0BF37C9E592D7A8FBB307D7809469CA9ABCB0082E4F8D5651E46D3CDB762D02D0BF37C9E592D7A8FBB307D7809469CA9ABCB0082E4F8D5651E46D3CDB762D02D0BF37C9E592D7A8FBB307D7809469CA9ABCB0082E4F8D5651E46D3CDB762D02D0BF37C9E592D7A8FBB307D7809469CA9ABCB0082E4F8D5651E46D3CDB762D02D0BF37C9E592D7A8FBB307D7809469CA9ABCB0082E4F8D5651E46D3CDB762D02D0BF37C9E592D7A8FBB307D7809469CA9ABCB0082E4F8D5651E46D3CDB762D02D0BF37C9E592D7A8FBB307D7809469CA9ABCB0082E4F8D5651E46D3CDB762D02D0BF37C9E592D7A8FBB307D7809469CA9ABCB0082E4F8D5651E46D3CDB762D02D0BF37C9E592","D12F3745538D85DDBFD9F3F9D334CE3324BBB7EEF3F5545BD818D93183614E42"))
            llOwnerSay("All Tests Passed!");
//        llOwnerSay((string)llGetTime());
    }
}
```

## SHA-224

```lsl
//////////////////////////////////////////////////////////////////////////////////////
//
//	UTF-8 SHA-2 224
//	Version 1.4
//	ESL Compiled: "Nov 20 2013", "04:01:23"
//	Copyright (C) 2013  Strife Onizuka
//	Based on Pseudo-code from http://en.wikipedia.org/wiki/SHA2
//	https://wiki.secondlife.com/wiki/SHA2
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
//             "Nov 20 2013", "04:01:23"             //
//  Copyright (C) 2004-2012, Strife Onizuka (cc-by)  //
//    http://creativecommons.org/licenses/by/3.0/    //
//===================================================//
//{

string hexc="0123456789ABCDEF";

//} Combined Library

list k1 = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174];
list k2 = [
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2];

string UTF8_SHA_224(string plain) {
    integer H1 = 0xC1059ED8;
    integer H2 = 0x367CD507;
    integer H3 = 0x3070DD17;
    integer H4 = 0xF70E5939;
    integer H5 = 0xFFC00B31;
    integer H6 = 0x68581511;
    integer H7 = 0x64F98FA7;
    integer H8 = 0xBEFA4FA4;

    //ORing on the extra bit. Since we are working in base64 the byte bounderies aren't where we want them.
    //So we get the last byte group and append our extra bit onto it. It contains either 1, 2, or 3 bytes.
    integer j = llSubStringIndex((plain = llStringToBase64(plain))+"=", "=");
    integer T = 0x80000000;
    if (j) {
        j = (6 * (T = j)) & -8;//length in bits
        T = llBase64ToInteger(llGetSubString((llGetSubString(plain, -4, (~-(T)))) + "AAAAAA", 0, 5)) | (0x00000080 << ((j % 3) << 3));
    }
    integer b = ((j + 40) >> 5) | 15;//this works because we want the value to be one less than the next appropriate multiple of 16.
    string buf = "AAA";
    integer i = -5;
    do buf += buf; while((i = -~i));//We need 85, 96 is close enough
    //llOwnerSay(llList2CSV([b,j, llStringLength(buf), llIntegerToBase64(j << (6 - ((b % 3) << 1)))]));
    plain = llInsertString( llDeleteSubString(plain, -4, -1) +
                            llGetSubString(llIntegerToBase64(T), 0, 5) +
                            buf, (b << 4) / 3,
                            llGetSubString(llIntegerToBase64(j >> ((b % 3) << 1)), 0, 5));
    //llOwnerSay(llList2CSV([llStringLength(plain), Base64ToHex(plain)]));
    list x;
    integer S = 0;
    do
    {
        integer A = H1;
        integer B = H2;
        integer C = H3;
        integer D = H4;
        integer E = H5;
        integer F = H6;
        integer G = H7;
        integer H = H8;
        x = (list)(j = 0);//the zero gets flushed off the stack by the later loop
        do
        {
            T = llBase64ToInteger(buf = llGetSubString(plain, T = ((i + j) << 4) / 3, 6+T)) << (S = (((i + j) % 3) << 1));
            if(S)
                T = T | (llBase64ToInteger("A" + (llDeleteSubString(buf, 0, 1))) >> (6 - S));
//            llOwnerSay("W["+(string)j+"]="+hex(T));
            x += T;
            T += H + (((E << 26) | ((E >>  6) & 0x03FFFFFF)) ^
                      ((E << 21) | ((E >> 11) & 0x001FFFFF)) ^
                      ((E <<  7) | ((E >> 25) & 0x0000007F))) +
                     ((E & F) ^ ((~E) & G)) + llList2Integer(k1, j);
            H = G;
            G = F;
            F = E;
            E = D + T;
            D = C;
            C = B;
            B = A;
            A = T + (((B << 30) | ((B >>  2) & 0x3FFFFFFF)) ^
                     ((B << 19) | ((B >> 13) & 0x0007FFFF)) ^
                     ((B << 10) | ((B >> 22) & 0x000003FF))) +
                    ((B & C) ^ (B & D) ^ (C & D));
        }while(16 > (j = -~j));
//		llOwnerSay(llList2CSV(hexm(x)));
        do
        {
            T = llList2Integer(x, -15);
            S = llList2Integer(x, -2);
            x = llList2List(x + (T = (llList2Integer(x,  -16) +
                                    (((T << 25) | ((T >>  7) & 0x01FFFFFF)) ^
                                     ((T << 14) | ((T >> 18) & 0x00003FFF)) ^
                                     ((T >>  3) & 0x1FFFFFFF)) +
                                    llList2Integer(x,  -7) +
                                    (((S << 15) | ((S >> 17) & 0x00007FFF)) ^
                                     ((S << 13) | ((S >> 19) & 0x00001FFF)) ^
                                     ((S >> 10) & 0x003FFFFF)))), -16, -1);
//            llOwnerSay("W["+(string)j+"]="+hex(T));
            T += H + (((E << 26) | ((E >>  6) & 0x03FFFFFF)) ^
                      ((E << 21) | ((E >> 11) & 0x001FFFFF)) ^
                      ((E <<  7) | ((E >> 25) & 0x0000007F))) +
                     ((E & F) ^ ((~E) & G)) + llList2Integer(k2, j - 16);
            H = G;
            G = F;
            F = E;
            E = D + T;
            D = C;
            C = B;
            B = A;
            A = T + (((B << 30) | ((B >>  2) & 0x3FFFFFFF)) ^
                     ((B << 19) | ((B >> 13) & 0x0007FFFF)) ^
                     ((B << 10) | ((B >> 22) & 0x000003FF))) +
                    ((B & C) ^ (B & D) ^ (C & D));
        }while(64 > (j = -~j));
        H1 += A;
        H2 += B;
        H3 += C;
        H4 += D;
        H5 += E;
        H6 += F;
        H7 += G;
        H8 += H;
    }while(b > (i += 16));
    x = [H1, H2, H3, H4, H5, H6, H7];//, H8];
    i = -7;
    buf = "";
    do
    {
        T = llList2Integer(x,i);
        j = 32;
        do
            buf += llGetSubString(hexc, b = ((T >> (j -= 4)) & 0xF), b);
        while (j);
    }while ((i = -~i));
    return buf;
}

string Base64_SHA_224(string plain, integer bit_length) {
    integer H1 = 0xC1059ED8;
    integer H2 = 0x367CD507;
    integer H3 = 0x3070DD17;
    integer H4 = 0xF70E5939;
    integer H5 = 0xFFC00B31;
    integer H6 = 0x68581511;
    integer H7 = 0x64F98FA7;
    integer H8 = 0xBEFA4FA4;

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
        T = (llBase64ToInteger(llGetSubString((llGetSubString(plain = llGetSubString(plain, 0, (bit_length / 6) | 3), -4, (~-(S / 6)))) + "AAAAAA", 0, 5)) & (0xFFFFFF00 << T)) | (0x00000080 << T);
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
        integer F = H6;
        integer G = H7;
        integer H = H8;
        x = (list)(bit_length = 0);//the zero gets flushed off the stack by the later loop
        do {
            T = llBase64ToInteger(buf = llGetSubString(plain, T = ((i + bit_length) << 4) / 3, 6+T)) << (S = (((i + bit_length) % 3) << 1));
            if(S)
                T = T | (llBase64ToInteger("A" + (llDeleteSubString(buf, 0, 1))) >> (6 - S));
//            llOwnerSay("W["+(string)j+"]="+hex(T));
            x += T;
            T += H + (((E << 26) | ((E >>  6) & 0x03FFFFFF)) ^
                      ((E << 21) | ((E >> 11) & 0x001FFFFF)) ^
                      ((E <<  7) | ((E >> 25) & 0x0000007F))) +
                     ((E & F) ^ ((~E) & G)) + llList2Integer(k1, bit_length);
            H = G;
            G = F;
            F = E;
            E = D + T;
            D = C;
            C = B;
            B = A;
            A = T + (((B << 30) | ((B >>  2) & 0x3FFFFFFF)) ^
                     ((B << 19) | ((B >> 13) & 0x0007FFFF)) ^
                     ((B << 10) | ((B >> 22) & 0x000003FF))) +
                    ((B & C) ^ (B & D) ^ (C & D));
        } while(16 > (bit_length = -~bit_length));
//		llOwnerSay(llList2CSV(hexm(x)));
        do {
            T = llList2Integer(x, -15);
            S = llList2Integer(x, -2);
            x = llList2List(x + (T = (llList2Integer(x,  -16) +
                                    (((T << 25) | ((T >>  7) & 0x01FFFFFF)) ^
                                     ((T << 14) | ((T >> 18) & 0x00003FFF)) ^
                                     ((T >>  3) & 0x1FFFFFFF)) +
                                    llList2Integer(x,  -7) +
                                    (((S << 15) | ((S >> 17) & 0x00007FFF)) ^
                                     ((S << 13) | ((S >> 19) & 0x00001FFF)) ^
                                     ((S >> 10) & 0x003FFFFF)))), -16, -1);
//            llOwnerSay("W["+(string)j+"]="+hex(T));
            T += H + (((E << 26) | ((E >>  6) & 0x03FFFFFF)) ^
                      ((E << 21) | ((E >> 11) & 0x001FFFFF)) ^
                      ((E <<  7) | ((E >> 25) & 0x0000007F))) +
                     ((E & F) ^ ((~E) & G)) + llList2Integer(k2, bit_length - 16);
            H = G;
            G = F;
            F = E;
            E = D + T;
            D = C;
            C = B;
            B = A;
            A = T + (((B << 30) | ((B >>  2) & 0x3FFFFFFF)) ^
                     ((B << 19) | ((B >> 13) & 0x0007FFFF)) ^
                     ((B << 10) | ((B >> 22) & 0x000003FF))) +
                    ((B & C) ^ (B & D) ^ (C & D));
        } while(64 > (bit_length = -~bit_length));
        H1 += A;
        H2 += B;
        H3 += C;
        H4 += D;
        H5 += E;
        H6 += F;
        H7 += G;
        H8 += H;
    } while(b > (i += 16));
    x = [H1, H2, H3, H4, H5, H6, H7, H8];
    i = -8;
    buf = "";
    do {
        T = llList2Integer(x,i);
        bit_length = 32;
        do
            buf += llGetSubString(hexc, b = ((T >> (bit_length -= 4)) & 0xF), b);
        while (bit_length);
    }while ((i = -~i));
    return buf;
}

integer go(string in, string answer) {
    llOwnerSay("");
    string b = llStringToBase64(in);
    integer len = (6 * llSubStringIndex((b)+"=", "=")) & -8;
    llResetTime();
    string outu = UTF8_SHA_224(in);
    float tu = llGetTime();
    llOwnerSay(llList2CSV(([outu, tu, len])));
    llResetTime();
    string outb = Base64_SHA_224(b, len);
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
        if(go("","D14A028C2A3A2BC9476102BB288234C415A2B01F828EA62AC5B3E42F"))
        if(go("abc","23097D223405D8228642A477BDA255B32AADBCE4BDA0B3F7E36C9DA7"))
        if(go("The quick brown fox jumps over the lazy dog","730E109BD7A8A32B1CB9D9A09AA2325D2430587DDBC0C38BAD911525"))
        if(go("D7A8FBB307D7809469CA9ABCB0082E4F8D5651E46D3CDB762D02D0BF37C9E592D7A8FBB307D7809469CA9ABCB0082E4F8D5651E46D3CDB762D02D0BF37C9E592D7A8FBB307D7809469CA9ABCB0082E4F8D5651E46D3CDB762D02D0BF37C9E592D7A8FBB307D7809469CA9ABCB0082E4F8D5651E46D3CDB762D02D0BF37C9E592D7A8FBB307D7809469CA9ABCB0082E4F8D5651E46D3CDB762D02D0BF37C9E592D7A8FBB307D7809469CA9ABCB0082E4F8D5651E46D3CDB762D02D0BF37C9E592D7A8FBB307D7809469CA9ABCB0082E4F8D5651E46D3CDB762D02D0BF37C9E592D7A8FBB307D7809469CA9ABCB0082E4F8D5651E46D3CDB762D02D0BF37C9E592D7A8FBB307D7809469CA9ABCB0082E4F8D5651E46D3CDB762D02D0BF37C9E592D7A8FBB307D7809469CA9ABCB0082E4F8D5651E46D3CDB762D02D0BF37C9E592D7A8FBB307D7809469CA9ABCB0082E4F8D5651E46D3CDB762D02D0BF37C9E592D7A8FBB307D7809469CA9ABCB0082E4F8D5651E46D3CDB762D02D0BF37C9E592D7A8FBB307D7809469CA9ABCB0082E4F8D5651E46D3CDB762D02D0BF37C9E592D7A8FBB307D7809469CA9ABCB0082E4F8D5651E46D3CDB762D02D0BF37C9E592D7A8FBB307D7809469CA9ABCB0082E4F8D5651E46D3CDB762D02D0BF37C9E592D7A8FBB307D7809469CA9ABCB0082E4F8D5651E46D3CDB762D02D0BF37C9E592","24BA6743F9D552F124E741D870690FD7704978D297E202206C02E18F"))
            llOwnerSay("All Tests Passed!");
//        llOwnerSay((string)llGetTime());
    }
}
```