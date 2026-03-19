---
name: "XTEA"
category: "example"
type: "example"
language: "LSL"
description: "Another XTEA implementation for LSL. Not sure if i have used the correct endian."
wiki_url: "https://wiki.secondlife.com/wiki/XTEA"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 Changes

  - 1.1 0.3
  - 1.2 0.2
  - 1.3 0.1
- 2 Source

Another XTEA implementation for LSL. Not sure if i have used the correct endian.

### Changes

#### 0.3

- Fixed length calculation
- Reduced loop logic, now parses backwards.
- Better memory cleanup.
- Less Vertical whitespace

#### 0.2

- Uses globals cutting down on instances and copies, should result in a huge time and bytecode savings.
- Base64 functions moved from XTEA in to CL.
- All functions optimized further.
- Introduction of ReadBase64IntegerPair - By doing read and writes this way it reduces bytecode.

#### 0.1

- Initial Release

### Source

```lsl
//===================================================//
//                 XTEA Library v0.3                 //
//             "Dec  9 2007", "05:15:17"             //
//  Copyright (C) 2004-2007, Strife Onizuka (cc-by)  //
//    http://creativecommons.org/licenses/by/3.0/    //
//===================================================//
//{

string v;
integer v0;
integer v1;

string Base64_XTEA_Encipher(integer num_rounds, string in, list k) {
    integer len = ((llStringLength(v = TrimRight(in,in="=")) * 6) >> 5);
    ReadBase64IntegerPair(len);//ReadBase64Integer could be used here instead
    if((len = ((len + (2 >> !v0)) & 0xFFFFFFFE)))//just a little length fudging
        do{
            integer sum = 0;
            ReadBase64IntegerPair(len -= 2);
            integer j = (-~(num_rounds));
            while((j = ~-j)){
                v0 += (((v1 << 4) ^ ((v1 >> 5) & 0x07FFFFFF)) + v1) ^ (sum + llList2Integer(k, sum & 3));
                sum += 0x9E3779B9;
                v1 += (((v0 << 4) ^ ((v0 >> 5) & 0x07FFFFFF)) + v0) ^ (sum + llList2Integer(k, (sum >> 11) & 3));
            }
            WriteBase64IntegerPair(len);
        }while(len);
    return TrimRight(v, v = "A");
}

string Base64_XTEA_Decipher(integer num_rounds, string in, list k) {
    integer len = ((llStringLength(v = TrimRight(in,in="=")) * 6) >> 5);
    ReadBase64IntegerPair(len);//ReadBase64Integer could be used here instead
    if((len = ((len + (2 >> !v0)) & 0xFFFFFFFE)))//just a little length fudging
        do{
            integer sum = 0x9E3779B9 * num_rounds;
            ReadBase64IntegerPair(len -= 2);
            integer j = (-~(num_rounds));
            while((j = ~-j)){
                v1 -= (((v0 << 4) ^ ((v0 >> 5) & 0x07FFFFFF)) + v0) ^ (sum + llList2Integer(k, (sum >> 11) & 3));
                sum -= 0x9E3779B9;
                v0 -= (((v1 << 4) ^ ((v1 >> 5) & 0x07FFFFFF)) + v1) ^ (sum + llList2Integer(k, sum & 3));
            }
            WriteBase64IntegerPair(len);
        }while(len);
    return TrimRight(v, v = "A");
}

//} XTEA Library

//===================================================//
//                 Combined Library                  //
//             "Dec  9 2007", "05:15:17"             //
//  Copyright (C) 2004-2007, Strife Onizuka (cc-by)  //
//    http://creativecommons.org/licenses/by/3.0/    //
//===================================================//
//{

//Functions marked "Mono Safe" are safe for use in LSLEditor & Mono
//Functions marked "LSO Safe" are safe for use in LSO
//Functions marked "Double Safe" are safe for use in VM's that support doubles (Mono, LSLEditor).
//Mono is the future VM for LSL, LSO is the current VM of LSL.
//To achieve safety, the functions require more bytecode and sacrifice a bit of performance.

string TrimRight(string src, string chrs)//Mono Safe, LSO Safe
{
    integer i = llStringLength(src);
    integer j = i;
    do ; while(~llSubStringIndex(chrs, llGetSubString(src, i = (~-(j = i)), i)) && j);
    return llDeleteSubString(src, j, 0x7FFFFFF0);
}

ReadBase64IntegerPair(integer index)
{
    integer S = (index << 5) % 6;
    string buf = llGetSubString(v, index = ((index << 5) / 6), index + 11);
    index = llBase64ToInteger(llGetSubString("A" + (llDeleteSubString(buf, 0, 2)) + "AAAAA", 0, 5));

        v0 = (llBase64ToInteger(llGetSubString((buf) + "AAAAAA", 0, 5)) << S) | (index >> (12 - S));
        v1 = ((llBase64ToInteger(llGetSubString((llDeleteSubString(buf,0,5)) + "AAAAAA", 0, 5)) >> (4 - S)) & ~(0xF0000000 << S)) | (index << (20 + S));

}

WriteBase64IntegerPair(integer index)
{

    integer S = 10 - ((index << 5) % 6);
    v =  llDeleteSubString(
        llInsertString(
            v,
            index = ((index << 5) / 6),
            llInsertString(
                llInsertString(
                    llIntegerToBase64(
                        (llBase64ToInteger(llGetSubString((v = llGetSubString(v, index, index + 12)) + "AAAAAA", 0, 5)) & (0xFFC00000 << S)) |
                        ((v0 >> (10 - S)) & ~(0xFFC00000 << S))
                    ), 3,
                    llIntegerToBase64(
                        ((v1 >> (24 - S)) & ~(0xFFFFFF00 << S)) |
                        (v0 << (8 + S))
                )   ), 7,
                llIntegerToBase64(
                    (llBase64ToInteger(llGetSubString((llDeleteSubString(v, 0, 6)) + "AAAAAA", 0, 5)) & ~(0xFFFFFFFF << S)) |
                    (v1 << S)
        )   )   ), index + 12, index + 35);//insert it then remove the old and the extra.
}

HexToBase64(string a)
{
    v = "";
    integer e = (llStringLength(a += "0000000000000000") - 9) & 0xFFFFFFF8;
    integer g;
    do{
        v0 = ((integer)("0x"+(llGetSubString(a, g, g + 7)))); v1 = ((integer)("0x"+(llGetSubString(a, g + 8, g + 15)))); WriteBase64IntegerPair(g >> 3);
    }while((g += 16) < e);

}

//} Combined Library

list mk;
integer rounds = 128;

default
{

    state_entry()
    {
        key owner = llGetOwner();
        llListen(0, "", owner, "");
        llListen(1, "", owner, "");
        llListen(2, "", owner, "");
        llListen(3, "", owner, "");
        llListen(4, "", owner, "");
        llListen(5, "", owner, "");

    }
    listen(integer a, string b, key c, string d)
    {
        if(a == 1)
        {
            rounds = (integer)d;
            llOwnerSay(llList2CSV([rounds, "~~~~"] + mk));
        }
        else if(a == 2)
        {
            mk = [];
            list e = llCSV2List(d);
            for(a = 0; a < 3; ++a)
                mk += (integer)llList2String(e,a);
            llOwnerSay(llList2CSV([rounds, "~~~~"] + mk));
        }
        else if(a == 3)
        {
            v = TrimRight(llStringToBase64(d), "=");
            ReadBase64IntegerPair(0);
            mk = [v0,v1];
            ReadBase64IntegerPair(2);
            mk += [v0,v1];
            llOwnerSay(llList2CSV([rounds, "~~~~"] + mk));
        }
        else if(a == 4)
        {
            HexToBase64(d);
            ReadBase64IntegerPair(0);
            mk = [v0,v1];
            ReadBase64IntegerPair(2);
            mk += [v0,v1];
            llOwnerSay(llList2CSV([rounds, "~~~~"] + mk));
        }
        else
        {
            if(a == 5)
                HexToBase64(d);
            else
                v = llStringToBase64(d);
            llOwnerSay(b = d = v);
            llOwnerSay(llList2CSV([d = Base64_XTEA_Encipher(rounds, b, mk)]));
            llOwnerSay(llList2CSV([d = Base64_XTEA_Decipher(rounds, d, mk), llBase64ToString(d)]));
            llOwnerSay(llList2CSV([b, llBase64ToString(b)]));
        }
    }
}
```