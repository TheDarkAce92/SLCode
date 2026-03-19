---
name: "Key Compression"
category: "example"
type: "example"
language: "LSL"
description: "One annoying issue with the current LSL language is its handling of keys. Keys are essentially stored as strings, 36 characters long, that is; 32 hexadecimal characters, plus four hyphens. This is a total of 36-bytes (UTF-8) or even 72-bytes (UTF-16), for a key, which in truth represents a 128-bit (16-byte) integer value. Pretty wasteful!"
wiki_url: "https://wiki.secondlife.com/wiki/Key_Compression"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 Key Compression
- 2 Base 256 Script

  - 2.1 Description
  - 2.2 Serialisation
  - 2.3 Implementation
- 3 Base 64 Script

  - 3.1 Description
  - 3.2 Serialisation
  - 3.3 Implementation
- 4 Base 32768 Script

  - 4.1 Description
  - 4.2 Serialisation
  - 4.3 Caveat
  - 4.4 Implementation
- 5 Base 256 Script (Reduced Code Size)

  - 5.1 Description
  - 5.2 Serialisation
- 6 Variable Base Script (Reduced Code Size)

  - 6.1 Description
  - 6.2 Serialisation
- 7 Base 4096 Script (Reduced Code Size)

  - 7.1 Description
  - 7.2 Serialisation

Key Compression

One annoying issue with the current LSL language is its handling of keys. Keys are essentially stored as strings, 36 characters long, that is; 32 hexadecimal characters, plus four hyphens. This is a total of 36-bytes (UTF-8) or even 72-bytes (UTF-16), for a key, which in truth represents a 128-bit (16-byte) integer value. Pretty wasteful!

For this reason, scripts which store a lot of keys can run of out memory very quickly, or may find that they can't fit many keys into a message, especially when sending to a webiste. For this reason it may be beneficial to use key-compression, to reduce the size of keys.

Base 256 Script

## Description

The following script compresses keys into a more compact, base 256 representation of the key. The alphabet used for this is arbitrary, and you may substitute your own preferred 256 characters if you wish, but must make sure you use these for both compression and decompression!

The functions you will be interested in are `compressKey()` and `decompressKey()`, you do not need to add both to your script, indeed most scripts only require one of the two functions.

A compressed key will typically be a little smaller than 50% the size of the key it represents.

You should only use these functions in scripts where the number of compressions/decompressions is relatively low. Decompressions are much faster than compressions, but still add overhead. If however you are mainly just storing the keys, or only occasionally need the key itself for something, then compression can be ideal. Comparisons can actually benefit greatly from compression, as the shorter length of the strings means that the comparison can be performed a lot faster, not as quickly as comparing two 128-bit integers, but we don't have those =)

## Serialisation

One important note when serialising compressed keys stored in lists is that llList2CSV() and llCSV2List() tend to introduce errors and may result in incorrectly decompressed keys. You are recommended to use the following:

```lsl
list compressedKeys = ...;
string str = llDumpList2String(compressedKeys, ",");
list lst = llParseStringKeepNulls(str, [","], []);
```

In most cases these functions are actually faster (not sure why) and will ensure correct serialisation/de-serialisation of lists containing compressed keys. If you have lists containing vectors and/or rotations then you will already be using these, however you should ensure that any custom character you use for separating entries is NOT part of the base256 alphabet provided (if it is then you should either change to a comma, or place a different character into the base256 alphabet in your character's place).

## Implementation

```lsl
string lslBase256Chars = "0123456789abcdefghijklmnopqrstuvwxyz!\"#$%&'()*+™-./:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`{|}~¡¢£¤¥¦§¨©ª«¬­®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿĀāĂăĄąĆćĈĉĊċČčĎďĐđĒēĔĕĖėĘęĚěĜĝĞğĠġĢģĤĥĦħĨĩĪīĬĭĮįİıĲĳĴĵĶķĸĹĺĻļĽľĿŀŁłŃńŅ";
string lslHexChars = "0123456789abcdef";

string compressKey(key _key) {
    string k = llToLower((string)llParseString2List((string)_key, ["-"], []));
    integer l = llStringLength(k);
    integer j;
    integer v;

    string out = "";
    integer i = 0;
    do {
        j = i + 1;
        v = (llSubStringIndex(lslHexChars, llGetSubString(k, i, i)) << 4) |
            llSubStringIndex(lslHexChars, llGetSubString(k, j, j));
        out = (out = "") + out + llGetSubString(lslBase256Chars, v, v);
    } while ((i += 2) < l);

    return (out = k = "") + out;
}

key decompressKey(string k) {
    integer l = llStringLength(k);
    string out = "";
    integer v; integer j; integer x;
    integer i = 0;

    do {
        v = llSubStringIndex(lslBase256Chars, llGetSubString(k, i, i));
        j = v >> 4; x = v & 0xF;
        out = (out = "") + out +
            llGetSubString(lslHexChars, j, j) +
            llGetSubString(lslHexChars, x, x);
    } while ((++i) < l);

    return (key)llInsertString(
        llInsertString(
            llInsertString(
                llInsertString((out = "") + out, 8,"-"),
                13,
                "-"
            ),
            18,
            "-"
        ),
        23,
        "-"
    );
}
```

Base 64 Script

## Description

While not as compact or character set flexible as the base 256 script above, this base 64 compression scheme provides reasonable compression in a speedy manner with very little code.

## Serialisation

As above, care should be taken to choose serialisation seperators not in the encoding character set, A-Z, a-z, 0-9, +, and /.

## Implementation

```lsl
string compress_key(string s) {
   s = llDumpList2String(llParseString2List(s, ["-"], []), "");
   return
      llGetSubString(llIntegerToBase64((integer)("0x"+llGetSubString(s,0,7))),0,5) +
      llGetSubString(llIntegerToBase64((integer)("0x"+llGetSubString(s,8,15))),0,5) +
      llGetSubString(llIntegerToBase64((integer)("0x"+llGetSubString(s,16,23))),0,5) +
      llGetSubString(llIntegerToBase64((integer)("0x"+llGetSubString(s,24,31))),0,5);
}

string integer2hex(integer in) {
   string s = "0123456789abcdef";
   string ret = "";
   integer i;
   for (i = 0; i < 8; i++) {
      ret = llGetSubString(s, in & 0xF, in & 0xF) + ret;
      in = in >> 4;
   }
   return ret;
}

string pad_dash(string s) {
   return
      llGetSubString(s, 0, 7) + "-" +
      llGetSubString(s, 8,11) + "-" +
      llGetSubString(s,12,15) + "-" +
      llGetSubString(s,16,19) + "-" +
      llGetSubString(s,20,31);
}

key uncompress_key(string s) {
   return (key) pad_dash(
      integer2hex(llBase64ToInteger(llGetSubString(s,0,5))) +
      integer2hex(llBase64ToInteger(llGetSubString(s,6,11))) +
      integer2hex(llBase64ToInteger(llGetSubString(s,12,17))) +
      integer2hex(llBase64ToInteger(llGetSubString(s,18,23))));
}
```

Base 32768 Script

## Description

Internally to the SL servers, strings are stored with UTF-16 encoding, and since internal memory is of concern, it makes sense to target the final internal representation.  This compression scheme takes a 36 character key and reduces it to 9 characters.  Because some code points are not allowed in UTF-16, compression to 8 characters is not possible.

## Serialisation

The character set in this example was chosen to leave all ASCII characters available as serialisation separators.

## Caveat

Not all LL functions handle Unicode characters properly, and in almost all cases using llEscapeURL() on these compressed keys will produce a string significantly longer than the actual key.  This method is best used for in memory storage only.  The code footprint is also large (approx 7K), so it is probably best to use this only if you're going to be storing MANY keys.

## Implementation

```lsl
// Copyright (C) 2009 Adam Wozniak and Doran Zemlja
// Released into the public domain.
// Free for anyone to use for any purpose they like.
//
// Tests with llGetFreeMemory seem to indicate a character takes up 2 bytes.
// this jibes with
// http://msdn.microsoft.com/en-us/library/system.string(VS.71).aspx
//
// INTERNALLY, strings are represented as UTF-16, and internal memory
// is what we actually care about
//
// going for maximum compression, we should be able to get a 128 bit key
// down to 8 x 16 bit characters
//
// we'll do this by encoding integers as UTF-8 URL escaped characters,
// and calling llUnescapeURL to convert them to strings.
//
// unfortunately, UTF-16 has some unallowed codepoints.  In particular,
// llEscapeURL/llUnescapeURL fails on the following code points:
//
// 0000, D800-DFFF, FDD0-FDEF, FFFE, FFFF
//
// Let's just make our lives easy and go with 15 bits per character.
// We'll encode 0000-7FFF as 0100-8100 to avoid null characters and leave
// all ASCII characters available as serialisation seperators.
// Also, let's go easy and just save up the 8 MSB as a final character at
// the end.
//
// this gives us a quick and easy 9 character key

string integer2hex(integer in, integer chars) {
   string s = "0123456789abcdef";
   string ret = "";
   integer i;
   for (i = 0; i < chars; i++) {
      ret = llGetSubString(s, in & 0xF, in & 0xF) + ret;
      in = in >> 4;
   }
   return ret;
}

integer char2integer(string s) {
   list l = llParseString2List(llEscapeURL(s), ["%"], []);
   integer i;
   integer value;
   integer ret = 0;
   for (i = 0; i < llGetListLength(l); i++) {
      value = (integer) ("0x" + llList2String(l, i));
      if (value & 0x80) {
         if (value & 0x40) {
            if (value & 0x20) {
               if (value & 0x10) {
                  ret = ret << 3;
                  ret = ret | (value & 0x07);
               }
               else {
                  ret = ret << 4;
                  ret = ret | (value & 0x0F);
               }
            }
            else {
               ret = ret << 5;
               ret = ret | (value & 0x1F);
            }
         }
         else {
            ret = ret << 6;
            ret = ret | (value & 0x3F);
         }
      }
      else {
         ret = ret << 7;
         ret = value;
      }
   }
   return ret;
}

string integer2eutf8(integer i) {
   string urlencoded_utf8;

   i += 256;

   if (i < 0x80) {
      urlencoded_utf8 = ("%" + integer2hex(i, 2));
   }
   else if (i < 0x800) {
      urlencoded_utf8  = ("%" + integer2hex(0xC0 | (i >> 6), 2));
      urlencoded_utf8 += ("%" + integer2hex(0x80 | (i & 0x3f), 2));
   }
   else {
      urlencoded_utf8  = ("%" + integer2hex(0xe0 | (i >> 12), 2));
      urlencoded_utf8 += ("%" + integer2hex(0x80 | ((i >> 6) & 0x3f), 2));
      urlencoded_utf8 += ("%" + integer2hex(0x80 | (i & 0x3f), 2));
   }

   return urlencoded_utf8;
}

string key2eutf8(key k) {
   string s = llDumpList2String(llParseString2List((key) k, ["-"], []), "");
   string ret;
   integer i;
   integer msbs = 0;
   integer word = 0;

   for (i = 0; i < 8; i++) {
      word = (integer) ("0x" + llGetSubString(s, 4*i, 4*i+3));
      msbs = msbs >> 1;
      msbs = msbs | (word & 0x8000);
      ret = ret + integer2eutf8(word & 0x7FFF);
   }
   ret = ret + integer2eutf8(msbs >> 8);
   return ret;
}

string compress_key(key k) {
   string s = key2eutf8(k);
   return llUnescapeURL(s);
}

string pad_dash(string s) {
   return
      llGetSubString(s, 0, 7) + "-" +
      llGetSubString(s, 8,11) + "-" +
      llGetSubString(s,12,15) + "-" +
      llGetSubString(s,16,19) + "-" +
      llGetSubString(s,20,31);
}

key uncompress_key(string s) {
   integer i;
   integer value;
   integer msbs = char2integer(llGetSubString(s, 8, 8));
   msbs -= 256;
   string ret;
   for (i = 0; i < 8; i++) {
      value = char2integer(llGetSubString(s, i, i));
      value -= 256;
      if (msbs & (1 << i)) {
         value = value | 0x8000;
      }
      ret = ret + integer2hex(value, 4);
   }
   return (key) pad_dash(ret);
}
```

Base 256 Script (Reduced Code Size)

## Description

Like the base 32768 script, this script also uses llEscapeURL and llUnescapeURL for compression.  It is optimized for code size by using a noncontiguous alphabet (chosen based on peculiarities of UTF-8 encoding and llEscapeURL/llUnescapeURL) and avoiding conversions from integer to string and string to integer.

## Serialisation

The character set in this example was chosen to leave all ASCII characters available as serialisation separators.

```lsl
// Copyright (C) 2009 Adam Wozniak and Doran Zemlja
// Released into the public domain.
// Free for anyone to use for any purpose they like.
// Updated 2024 Peter Stindberg
//
// like the base 32768 compressor, this base 256 compressor relies on
// llEscapeURL/llUnescapeURL.
//
// it is optimized for size.

string compress_key(key k) {
   string s = llReplaceSubString((string) k, "-", "", 0);
   string ret;
   integer i;
   for (i = 0; i < 32; i += 2) {
      ret = ret + "%d"+llGetSubString(s,i,i)+"%b"+llGetSubString(s,i+1,i+1);
   }
   return llUnescapeURL(ret);
}

string pad_dash(string s) {
   return
      llGetSubString(s, 0, 7) + "-" +
      llGetSubString(s, 8,11) + "-" +
      llGetSubString(s,12,15) + "-" +
      llGetSubString(s,16,19) + "-" +
      llGetSubString(s,20,31);
}

key uncompress_key(string s) {
   integer i;
   string ret;
   s = llToLower(llEscapeURL(s));
   for (i = 0; i < 32; i++) {
      ret = ret + llGetSubString(s,i*3+2,i*3+2);
   }
   return pad_dash(ret);
}
```

Variable Base Script (Reduced Code Size)

## Description

Like the base 32768 script, this script also uses llEscapeURL and llUnescapeURL for compression.  It is optimized for code size by using a noncontiguous alphabet and avoiding conversions from integer to string and string to integer.  This script takes advantage of even more peculiarities of UTF-8 encoding than the base 256 reduced code size script.  Because of this, the base is not actually a fixed size, but instead switches back and forth between base 256 and base 4096, depending on the input data and the resulting UTF-8 output.

The final compressed key is between 11 characters (best case) and 16 characters (worst case).  An empirical test of 2000 random keys gave an average length of 11.95 characters.

## Serialisation

The character set in this example was chosen to leave all ASCII characters available as serialisation separators.

```lsl
// Copyright (C) 2009 Adam Wozniak and Doran Zemlja
// Released into the public domain.
// Free for anyone to use for any purpose they like.
// Updated 2024 Peter Stindberg
//
// like the base 32768 compressor, this compressor relies on
// llEscapeURL/llUnescapeURL.
//
// It produces variable length encodings between
// 11 and 16 characters.

string compress_key(key k) {
   string s = llReplaceSubString((string) k, "-", "", 0) + "000";
   string ret;
   integer i;
   integer j;
   for (i = 0; i < 32; ) {
      j = (integer)("0x"+ llGetSubString(s,i,i));
      if (j > 0 && j < 0xd) { // TODO test with ((j>0&&j<0xd)||j==0xe), might get better compression
         ret = ret + llUnescapeURL("%e"+llGetSubString(s,i,i)+
               "%b"+llGetSubString(s,i+1,i+1)+
               "%b"+llGetSubString(s,i+2,i+2));
         i += 3;
      }
      else {
         ret = ret + llUnescapeURL("%d"+llGetSubString(s,i,i)+
               "%b"+llGetSubString(s,i+1,i+1));
         i += 2;
      }
   }
   return ret;
}

string pad_dash(string s) {
   return
      llGetSubString(s, 0, 7) + "-" +
      llGetSubString(s, 8,11) + "-" +
      llGetSubString(s,12,15) + "-" +
      llGetSubString(s,16,19) + "-" +
      llGetSubString(s,20,31);
}

key uncompress_key(string s) {
   integer i;
   string ret;
   s = llToLower(llEscapeURL(s));
   for (i = 0; i < 32; i++) {
      ret = ret + llGetSubString(s,i*3+2,i*3+2);
   }
   return pad_dash(ret);
}
```

Base 4096 Script (Reduced Code Size)

## Description

This is the final evolution of the Reduced Code Size scripts.  It uses base 4096, and produces compressed keys of a fixed size (11 characters).  It uses a number of tricks demonstrated in the previous Reduced Code Size scripts.  Under mono it takes approximately 3.5K of code memory.

## Serialisation

The character set in this example was chosen to leave all ASCII characters available as serialisation separators.

```lsl
// Copyright (C) 2009 Adam Wozniak and Doran Zemlja
// Released into the public domain.
// Free for anyone to use for any purpose they like.
// Updated 2024 Peter Stindberg
//
// deep voodoo base 4096 key compression
//
// It produces fixed length encodings of 11 characters.

string compress_key(key k) {
   string s = llToLower(llReplaceSubString((string) k, "-", "", 0) + "0");
   string ret;
   integer i;

   string A;
   string B;
   string C;
   string D;

   for (i = 0; i < 32; ) {
      A = llGetSubString(s, i, i);
      i++;
      B = llGetSubString(s, i, i);
      i++;
      C = llGetSubString(s, i, i);
      i++;
      D = "b";

      if (A == "0") {
         A = "e";
         D = "8";
      }
      else if (A == "d") {
         A = "e";
         D = "9";
      }
      else if (A == "f") {
         A = "e";
         D = "a";
      }

      ret += "%e"+A+"%"+D+B+"%b"+C;
   }
   return llUnescapeURL(ret);
}

string pad_dash(string s) {
   return
      llGetSubString(s, 0, 7) + "-" +
      llGetSubString(s, 8,11) + "-" +
      llGetSubString(s,12,15) + "-" +
      llGetSubString(s,16,19) + "-" +
      llGetSubString(s,20,31);
}

key uncompress_key(string s) {
   integer i;
   string ret;
   string A;
   string B;
   string C;
   string D;

   s = llToLower(llEscapeURL(s));
   for (i = 0; i < 99; i += 9) {
      A = llGetSubString(s,i+2,i+2);
      B = llGetSubString(s,i+5,i+5);
      C = llGetSubString(s,i+8,i+8);
      D = llGetSubString(s,i+4,i+4);

      if (D == "8") {
         A = "0";
      }
      else if (D == "9") {
         A = "d";
      }
      else if (D == "a") {
         A = "f";
      }
      ret = ret + A + B + C;
   }
   return pad_dash(ret);
}
```