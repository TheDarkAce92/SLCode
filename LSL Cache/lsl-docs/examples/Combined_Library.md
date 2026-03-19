---
name: "Combined Library"
category: "example"
type: "example"
language: "LSL"
description: "The Combined Library is comprised of about 55 functions all of which are released under CC-by v3.0 license."
wiki_url: "https://wiki.secondlife.com/wiki/Library_Combined_Library"
author: "Haravikk Mistral"
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Combined Library

- 1 String Functions

  - 1.1 Replace

  - 1.1.1 Older, user-defined functions
  - 1.2 Trim
  - 1.3 Unescape
- 2 Unicode functions

  - 2.1 UTF8 to Unicode Integer
  - 2.2 Unicode Integer to UTF8
  - 2.3 Byte Length of UTF-8 Encoded String
  - 2.4 Truncate To Length
  - 2.5 Split To Length
- 3 List Functions

  - 3.1 Replace
  - 3.2 Compare
- 4 Base64 & Hex Encoding

  - 4.1 Parameter & Return Based
  - 4.2 Global Buffers
- 5 Float Union Integer

  - 5.1 General
  - 5.2 LSLEditor Safe
- 6 Change Log

  - 6.1 1.0
  - 6.2 Unversioned



The Combined Library is comprised of about 55 functions all of which are released under [CC-by v3.0 license](http://creativecommons.org/licenses/by/3.0/).

The library is still being worked on so only some of the compiled functions will be posted at this time. All functions in the library are hand optimized. To understand the logic, it is best to pull the code apart but be wary of LSL's strict order of operations.

You can download the latest release from here: [CombinedLibrary.zip](http://www.megaupload.com/?d=LV0334YT)

**Note: This project has not been substantially updated since 2008.**

## String Functions

### Replace

As of simulator release 2023-01-27.577942, there is the native LSL function llReplaceSubString.

#### Older, user-defined functions

The originally posted function was largely superseded by this version posted below by Haravikk Mistral, it is much faster (under both LSL and Mono) while having identical behaviour, and in the majority of usages is more memory efficient:

```lsl
string strReplace(string str, string search, string replace) {
    return llDumpList2String(llParseStringKeepNulls((str = "") + str, [search], []), replace);
}
```

Here is the original version of the function, while slower it is more memory efficient in LSO when the input string requires a large number of parts to be replaced. For example when replacing every space in a paragraph with an underscore. In LSO the cost of dividing the string into a list balloons the size of the string considerably.

```lsl
string str_replace(string src, string from, string to)
{//replaces all occurrences of 'from' with 'to' in 'src'.
    integer len = (~-(llStringLength(from)));
    if(~len)
    {
        string  buffer = src;
        integer b_pos = ERR_GENERIC;
        integer to_len = (~-(llStringLength(to)));
        @loop;//instead of a while loop, saves 5 bytes (and runs faster).
        integer to_pos = ~llSubStringIndex(buffer, from);
        if(to_pos)
        {
//            b_pos -= to_pos;
//            src = llInsertString(llDeleteSubString(src, b_pos, b_pos + len), b_pos, to);
//            b_pos += to_len;
//            buffer = llGetSubString(src, (-~(b_pos)), 0x8000);
            buffer = llGetSubString(src = llInsertString(llDeleteSubString(src, b_pos -= to_pos, b_pos + len), b_pos, to), (-~(b_pos += to_len)), 0x8000);
            jump loop;
        }
    }
    return src;
}
```

### Trim

```lsl
string TrimRight(string src, string chrs)//LSLEditor Unsafe, LSL Safe
{
    integer i = llStringLength(src);
    do ; while(~llSubStringIndex(chrs, llGetSubString(src, i = ~-i, i)) && i);
    return llDeleteSubString(src, -~(i), 0x7FFFFFF0);
}

string TrimLeft(string src, string chrs)//LSLEditor Unsafe, LSL Safe
{
    integer i = ~llStringLength(src);
    do ; while(i && ~llSubStringIndex(chrs, llGetSubString(src, i = -~i, i)));
    return llDeleteSubString(src, 0x8000000F, ~-(i));
}

string TrimBoth(string src, string chrs)//LSLEditor Unsafe, LSL Safe
{
    integer i = ~llStringLength(src);
    do ; while(i && ~llSubStringIndex(chrs, llGetSubString(src, i = -~i, i)));
    i = llStringLength(src = llDeleteSubString(src, 0x8000000F, ~-(i)));
    do ; while(~llSubStringIndex(chrs, llGetSubString(src, i = ~-i, i)) && i);
    return llDeleteSubString(src, -~(i), 0x7FFFFFF0);
}
```

### Unescape

This is not the version found in Combined Library, it does not support the \h, \u or \U escape codes which are supported by the library version. Both support these escape codes: \\, \", \n, \t, \s

Like Haravikk's Replace function, this has the potential to use a huge amount of memory, consider using the library version instead if memory usage becomes a problem. If you do not need the extra features and do not have memory limitations this is a great alternative.

```lsl
string Unescape(string in)
{
    list search = ["\\n","\\\"","\\t","\\s"];
    list replace = ["\n","\"","\t"," "];
    list split = llParseStringKeepNulls((in = "") + in, ["\\\\"], []);//"
    integer pos = ([] != split);
    do
    {
        integer qos = -4;
        string item = llList2String(split, pos);
        do
            item = llDumpList2String(llParseStringKeepNulls((item = "") + item, llList2List(search, qos, qos), []), llList2String(replace, qos));
        while(qos = -~qos);
        split = llListReplaceList((split = []) + split, [(item = "") + item], pos, pos);
    }
    while(pos = -~pos);
    return llDumpList2String(split, "\\");
}
```

## Unicode functions

LSL uses UTF-8 to as the base format for strings. UTF-8 is an encoding system for storing Unicode characters, each Unicode character has a number. These functions allow for the conversion between the string form and the integer form. They may not be pretty but they are tight and get the job done quickly.

### UTF8 to Unicode Integer

Converts a character into an integer.

```lsl
integer UTF8ToUnicodeInteger(string input)//Mono Safe, LSO Safe
{
    integer result = llBase64ToInteger(llStringToBase64(input = llGetSubString(input,0,0)));
    if(result & 0x80000000){//multibyte, continuing to use base64 is impractical because it requires smart shifting.
        integer end = (integer)("0x"+llGetSubString(input = (string)llParseString2List(llEscapeURL(input),(list)"%",[]),-8,-1));
        integer begin = (integer)("0x"+llDeleteSubString(input,-8,-1));
        return  (   (  0x0000003f &  end       ) |
                    (( 0x00003f00 &  end) >> 2 ) |
                    (( 0x003f0000 &  end) >> 4 ) |
                    (( 0x3f000000 &  end) >> 6 ) |
                    (( 0x0000003f &  begin) << 24) |
                    (( 0x00000100 &  begin) << 22) ) &
                    (0x7FFFFFFF >> (5 * ((integer)(llLog(~result) / 0.69314718055994530941723212145818) - 25)));
    }
    return result >> 24;
}
```

### Unicode Integer to UTF8

Converts an integer into a character.

```lsl
string UnicodeIntegerToUTF8(integer input)//Mono Safe, LSLEditor Safe, LSO Incomplete
{//LSO allows for the older UTF-8 range, this function only supports the new UTF-16 range.
    if(input > 0)
    {
        if(input <= 0x7FF)
        {
            if(input <= 0x7F)
                return llBase64ToString(llIntegerToBase64(input << 24));
            return llBase64ToString(llIntegerToBase64(0xC0800000 | ((input << 18) & 0x1F000000) | ((input << 16) & 0x3F0000)));here.
        }
        if(input <= 0xFFFF)
            return llBase64ToString(llIntegerToBase64(0xE0808000 | ((input << 12) & 0x0F000000) | ((input << 10) & 0x3F0000) | ((input << 8) & 0x3F00)));
        if(input <= 0x10FFFF)
            return llBase64ToString(llIntegerToBase64(0xF0808080 | ((input << 06) & 0x07000000) | ((input << 04) & 0x3F0000) | ((input << 2) & 0x3F00) | (input & 0x3F)));
    }
    return "";
}
```

### Byte Length of UTF-8 Encoded String

Returns the number of bytes that would be used if the string were encoded in UTF-8.

```lsl
integer StringUTF8Size(string str) {
    return (3 * llSubStringIndex(llStringToBase64(str)+"=", str = "=")) >> 2;
}
```

### Truncate To Length

Keep the first n-bytes, discard the rest. If a character is truncated, the damaged portion is discarded.

```lsl
string TruncateToLength(string str, integer bytes) {
    string temp = llStringToBase64(str);
    if(llStringLength(temp) <= (bytes * 8) / 6)
        return str;
    temp = llBase64ToString(llGetSubString(temp+"==", (bytes * -2) % 3, (bytes * 4 - 1) / 3));
    integer i = llStringLength(temp) - 1;
    if(llGetSubString(temp, i, i) != llGetSubString(str, i, i))
        return llDeleteSubString(temp, i, i);//last char was multi-byte and was truncated.
    return temp;
}
```

### Split To Length

Splits a string so at most only a specified number of bytes appear in each substring. If an entire character cannot fit in the current stride, it is pushed into the next.

```lsl
list SplitToLength(string in, integer bytes) {
    list out = [];
    while(in) {
        string str = llDeleteSubString(in, bytes, 0x7ffffff0);
        string temp = llStringToBase64(str);
        if(llStringLength(temp) <= (bytes * 8) / 6) {
            out += str;
            in = llDeleteSubString(in, 0, bytes);
        } else {
            temp = llBase64ToString(llGetSubString(temp + "==", (bytes * -2) % 3, (bytes * 4 - 1) / 3));
            integer i = llStringLength(temp) - 1;
            if(llGetSubString(temp, i, i) != llGetSubString(str, i, i)) {
                if(!i)
                    return out + ["", in, -2];
                out += llDeleteSubString(temp, i, i);//last char was multi-byte and was truncated.
                in = llGetSubString(in, i, 0x7ffffff0);
            } else {
                out += temp;
                in = llDeleteSubString(in, 0, i);
            }
        }
    }
    return out;
}
```

## List Functions

### Replace

The design of the logic had to overcome two hurdles. The first was keeping it from searching previous replacements (otherwise you could fall into an infinite loop or infinitely grow the memory). The second was so that it could do null replacements. Both of these hurdles were overcome but at the cost of some readability.

The way it works is it keeps an Unsearched Buffer (UB) which is a subset of the Input Buffer (IB) and it records the Position of the UB in the IB (P). Each iteration it searches the UB and adds that resulting index to the P, then it uses P as the index to replace that section in the IB, finally it recalculates the new P, then is uses IB with the new P to update UB.

```lsl
list ListReplace(list src, list from, list to)
{//replaces all occurrences of 'from' with 'to' in 'src'.
    integer len = ~([] != from);
    if(~len)
    {
        list  buffer = src;
        integer b_pos = ERR_GENERIC;
        integer to_len = ~([] != to);
        @loop;//instead of a while loop, saves 5 bytes (and runs faster).
        integer to_pos = ~llListFindList(buffer, from);
        if(to_pos)
        {
//            b_pos -= to_pos;
//            src = llListReplaceList(src, to, b_pos, b_pos + len);
//            b_pos += to_len;
//            buffer = llList2List(src, (-~(b_pos)), 0x4000);
            buffer = llList2List(src = llListReplaceList(src, to, b_pos -= to_pos, b_pos + len), (-~(b_pos += to_len)), 0x4000);
            jump loop;
        }
    }
    return src;
}
```

### Compare

Compares two lists, returns true if identical.

**Note:** It will ignore the sign on zero (0.0 == -0.0). If the sign on zero is important to you, follow the instructions in the comments on how to enable checking for this. Currently no functions in LSL treat negative zero differently then positive zero.

```lsl
integer ListCompare(list input_a, list input_b)
{
    integer b = input_a != input_b;
    if(!b)
    {
        if((b = [] != input_a))
        {
            integer counter = b;
            do
            {
                if((b = llGetListEntryType(input_a,counter)) - llGetListEntryType(input_b,counter))
                    jump end_a;
                //Don't need to bother with TYPE_KEY
                if(b == TYPE_FLOAT) {
                    if((b = (llList2Float(input_a,counter) != llList2Float(input_b,counter))))
                        jump end_b;
                } else if(b == TYPE_VECTOR) {//it costs more to update b and jump out then to just return
                    if((b = (llList2Vector(input_a,counter) != llList2Vector(input_b,counter))))//so just return.
                        jump end_c;
                } else if(b == TYPE_ROTATION) {
                    if((b = (llList2Rot(input_a,counter) != llList2Rot(input_b,counter))))
                        jump end_d;
                }
                else//comment this line out if you care about the sign on zero.
                    if((b = (llList2String(input_a,counter) != llList2String(input_b,counter))))
                        jump end_e;
            }while((counter = -~counter));
            //if you get here, b equals zero, so we don't even have to change it's value for the return.
        }
    }
    @end_a;@end_b;@end_c;@end_d;@end_e;
    return !b;
}
```

If you do not care about positive/negative zero, then a better way to perform the comparison is:

```lsl
integer ListCompare(list a, list b) {
    integer aL = a != [];
    if (aL != (b != [])) return 0;
    else if (aL == 0)    return 1;

    return llListFindList((a = []) + a, (b = []) + b) == 0;
}
```

If you just want to compare the length of the lists use `(a == b)`:

```lsl
integer ListCompare(list a, list b){
    return (a==b);
}
```



## Base64 & Hex Encoding

### Parameter & Return Based

Binary functions that use parameters and returns

```lsl
integer ReadBase64Integer(string data, integer index)
{
    integer S = (index << 5) % 6;
    index = llBase64ToInteger(llGetSubString((data = llGetSubString(data, index = ((index << 5) / 6), index+6)) + "AAAAAA", 0, 5)) << S;
    if(S)
        index = index | (llBase64ToInteger(llGetSubString("A" + (llDeleteSubString(data, 0, 1)) + "AAAAA", 0, 5)) >> (6 - S));
    return index;
}

list ReadBase64IntegerPair(string data, integer index)
{
    integer S = (index << 5) % 6;
    index = llBase64ToInteger(llGetSubString("A" + (llDeleteSubString(data = llGetSubString(data, index = ((index << 5) / 6), index + 11), 0, 2)) + "AAAAA", 0, 5));
    return [
        (llBase64ToInteger(llGetSubString((data) + "AAAAAA", 0, 5)) << S) | (index >> (12 - S)),
        ((llBase64ToInteger(llGetSubString((llDeleteSubString(data,0,5)) + "AAAAAA", 0, 5)) >> (4 - S)) & ~(0xF0000000 << S)) | (index << (20 + S))
    ];
}

string WriteBase64Integer(string data, integer index, integer value)
{

    integer S = 12 - ((index % 3) << 1);
    return  llDeleteSubString(
        llInsertString(
        data,
        index = ((index << 4) / 3),
            llInsertString(
                llIntegerToBase64(
                    (llBase64ToInteger(llGetSubString((data = llGetSubString(data, index, index+7)) + "AAAAAA", 0, 5)) & (0xFFF00000 << S)) |
                    ((value >> (12 - S)) & ~(0xFFF00000 << S))
                ), 2,
                llIntegerToBase64(
                    (llBase64ToInteger(llGetSubString((llDeleteSubString(data, 0, 1)) + "AAAAAA", 0, 5)) & ~(0xFFFFFFFF << S)) |
                    (value << S)
        )	)	), index+7, index + 22);//insert it then remove the old and the extra.
}

string WriteBase64IntegerPair(string data, integer index, integer low, integer high)
{

    integer S = 10 - ((index << 5) % 6);
    return  llDeleteSubString(
        llInsertString(
            data,
            index = ((index << 5) / 6),
            llInsertString(
                llInsertString(
                    llIntegerToBase64(
                        (llBase64ToInteger(llGetSubString((data = llGetSubString(data, index, index + 12)) + "AAAAAA", 0, 5)) & (0xFFC00000 << S)) |
                        ((low >> (10 - S)) & ~(0xFFC00000 << S))
                    ), 3,
                    llIntegerToBase64(
                        ((high >> (24 - S)) & ~(0xFFFFFF00 << S)) |
                        (low << (8 + S))
                )   ), 7,
                llIntegerToBase64(
                    (llBase64ToInteger(llGetSubString((llDeleteSubString(data, 0, 6)) + "AAAAAA", 0, 5)) & ~(0xFFFFFFFF << S)) |
                    (high << S)
        )   )   ), index + 12, index + 35);//insert it then remove the old and the extra.
}

string DwordList2Hex(list in)
{
    string out = ""; integer len = ~(in != []);

    while((len = -~len))
    {
        integer int = llList2Integer(in, len);
        integer j = 8;
        string mout = "";
        do
        {
            mout = llGetSubString(hexc, int & 15, int & 15) + mout;
            int = int >> 4;
        }while((j = ~-j));
        out += mout;
    }
    return out;

}

string HexToBase64(string a)
{
    string d = "";
    integer e = (llStringLength(a += "0000000000000000") - 9) & 0xFFFFFFF8;
    integer g;
    do{
        d = WriteBase64IntegerPair(d, g >> 3, ((integer)("0x"+(llGetSubString(a, g, g + 7)))), ((integer)("0x"+(llGetSubString(a, g + 8, g + 15)))));
    }while((g += 16) < e);
    return d;
}

list Base64ToHex(string a)
{
    list out = [];
    integer len = ((llStringLength(a = TrimRight(a,"A=")) + 4) * 6) >> 5;
    integer i = -1;
    integer int;

    while((i = -~i) <= len)
    {
        if((int = ReadBase64Integer(a, i)) || (i ^ len))
        {
            integer j = 8;
            string mout = "";
            do
            {
                mout = llGetSubString(hexc, int & 15, int & 15) + mout;
                int = int >> 4;
            }while((j = ~-j));
            out += mout;
        }
    }
    return out;

}

integer ReadBase64Byte(string data, integer index)
{
    return 0xFF & (
        llBase64ToInteger(llGetSubString((llGetSubString(data, (index << 3) / 6, (-~((index << 3) / 6)))) + "AAAAAA", 0, 5)) >>
        (24 - ((index << 3) % 6)));
}

string WriteBase64Byte(string data, integer index, integer value)
{
    integer S = 24 - ((index = (index << 3)) % 6);
    return llDeleteSubString(llInsertString(data, index /= 6,
        llIntegerToBase64(
            (llBase64ToInteger(llGetSubString((llGetSubString(data, index, (-~(index)))) + "AAAAAA", 0, 5)) & ~(0xFF << S)) |
            ((value & 0xFF) << S)
    )   ), index + 2, index + 9);//insert it then remove the old and the extra.
}

list Base64ToDwordList(string a)
{
    integer len = (6 * (llStringLength(a = TrimRight(a,"A=")) + 4)) >> 5;
    integer i = -1;
    list out;
    integer int;
    while((i = -~i) <= len)
        if((int = ReadBase64Integer(a, i)) || (i ^ len))
            out += int;
    return out;
}

string DwordListToBase64(list a)
{
    integer len = (a != []);
    integer i = -1;
    string out;
    while((i = -~i) < len)
        out = WriteBase64Integer(out, i, llList2Integer(a, i));
    return TrimRight(out,"A");
}

string hexc="0123456789ABCDEF";
```

### Global Buffers

These versions of the functions depend upon global buffers. Not all the functions have been ported to this model (because it is very complicated to build functions with macros so they can be flipped from one mode to the other).

```lsl
integer v0;
integer v1;
string v;

ReadBase64Integer(integer index)
{
    integer S = (index << 5) % 6;
    string T = llGetSubString(v, index = ((index << 5) / 6), index+6);
    v0 = llBase64ToInteger(llGetSubString((T) + "AAAAAA", 0, 5)) << S;
    if(S)
        v0 = v0 | (llBase64ToInteger(llGetSubString("A" + (llDeleteSubString(T, 0, 1)) + "AAAAA", 0, 5)) >> (6 - S));

}

ReadBase64IntegerPair(integer index)
{
    integer S = (index << 5) % 6;
    string buf = llGetSubString(v, index = ((index << 5) / 6), index + 11);
    index = llBase64ToInteger(llGetSubString("A" + (llDeleteSubString(buf, 0, 2)) + "AAAAA", 0, 5));

        v0 = (llBase64ToInteger(llGetSubString((buf) + "AAAAAA", 0, 5)) << S) | (index >> (12 - S));
        v1 = ((llBase64ToInteger(llGetSubString((llDeleteSubString(buf,0,5)) + "AAAAAA", 0, 5)) >> (4 - S)) & ~(0xF0000000 << S)) | (index << (20 + S));

}

WriteBase64Integer(integer index)
{

    integer S = 12 - ((index % 3) << 1);
    v =  llDeleteSubString(
        llInsertString(
        v,
        index = ((index << 4) / 3),
            llInsertString(
                llIntegerToBase64(
                    (llBase64ToInteger(llGetSubString((v = llGetSubString(v, index, index+7)) + "AAAAAA", 0, 5)) & (0xFFF00000 << S)) |
                    ((v0 >> (12 - S)) & ~(0xFFF00000 << S))
                ), 2,
                llIntegerToBase64(
                    (llBase64ToInteger(llGetSubString((llDeleteSubString(v, 0, 1)) + "AAAAAA", 0, 5)) & ~(0xFFFFFFFF << S)) |
                    (v0 << S)
        )	)	), index+7, index + 22);//insert it then remove the old and the extra.
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
        v0 = ((integer)("0x"+(llGetSubString(a, g, g + 7))));
        v1 = ((integer)("0x"+(llGetSubString(a, g + 8, g + 15))));
        WriteBase64IntegerPair(g >> 3);
    }while((g += 16) < e);

}

list Base64ToHex()
{
    list out = [];
    integer len = ((llStringLength(v = TrimRight(v,"A=")) + 4) * 6) >> 5;
    integer i = 0;

    do{
        ReadBase64Integer(i); if(v0 || (i ^ len))
        {
            integer j = 8;
            string mout = "";
            do{
                mout = llGetSubString(hexc, v0 & 15, v0 & 15) + mout;
                v0 = v0 >> 4;
            }while((j = ~-j));
            out += mout;
        }
    }while((i = -~i) <= len);
    return out;

}

list Base64ToDwordList()
{
    integer len = (6 * (llStringLength(v = TrimRight(v,"A=")) + 4)) >> 5;
    integer i = 0;
    list out = [];

    do
    {
        ReadBase64Integer(i);
        if(v0 || (i ^ len))
            out += v0;
    }while((i = -~i) <= len);
    return out;
}

ReadBase64Byte(integer index)
{
    v0 = 0xFF & (
        llBase64ToInteger(llGetSubString((llGetSubString(v, (index << 3) / 6, (-~((index << 3) / 6)))) + "AAAAAA", 0, 5)) >>
        (24 - ((index << 3) % 6)));
}

WriteBase64Byte(integer index)
{
    integer S = 24 - ((index = (index << 3)) % 6);
    v = llDeleteSubString(llInsertString(v, index /= 6,
        llIntegerToBase64(
            (llBase64ToInteger(llGetSubString((llGetSubString(v, index, (-~(index)))) + "AAAAAA", 0, 5)) & ~(0xFF << S)) |
            ((v0 & 0xFF) << S)
    )   ), index + 2, index + 9);//insert it then remove the old and the extra.
}

string hexc="0123456789ABCDEF";
```

## Float Union Integer

The Float Union Integer functions allow for safely storing floats in integers and provide for retrieval. All real numbers are supported.

For versions that support Infinity and NaN see User:Strife_Onizuka/Float_Functions (the two versions have not been reconciled yet).

### General

These versions will work well in LSO and Mono.

```lsl
integer fui(float input)//Mono Safe, LSO Safe, Doubles Unsupported, LSLEditor Unsafe
{//union float to integer
    if((input) != 0.0){//is it non zero?
        integer sign = (input < 0) << 31;//the sign, but later this variable is reused to store the shift
        if((input = llFabs(input)) < 2.3509887016445750159374730744445e-38)//Denormalized range check & last stride of normalized range
            return sign | (integer)(input / 1.4012984643248170709237295832899e-45);//the math overlaps; saves cpu time.
        integer exp = llFloor((llLog(input) / 0.69314718055994530941723212145818));//extremes will error towards extremes. following yuch corrects it.
        return (0x7FFFFF & (integer)(input * (0x1000000 >> sign))) | (((exp + 126 + (sign = ((integer)input - (3 <= (input /= (float)("0x1p"+(string)(exp -= ((exp >> 31) | 1)))))))) << 23 ) | sign);
    }//for grins, detect the sign on zero. it's not pretty but it works. the previous requires alot of unwinding to understand it.
    return ((string)input == (string)(-0.0)) << 31;
}

float iuf(integer input)//LSLEditor Unsafe, LSO Safe, Mono Safe
{//union integer to float
    return llPow(2.0, (input | !input) - 150) * (((!!(input = (0xff & (input >> 23)))) << 23) | ((input & 0x7fffff))) * (1 | (input >> 31));
}//will crash if the raw exponent == 0xff; reason for crash deviates from float standard; though a crash is warented.
```

### LSLEditor Safe

These versions will run in LSLEditor (as well as LSO and Mono). Doubles are not supported and anything outside the float range will become signed infinity or zero respectively.

```lsl
integer fui(float input)//Mono Safe, LSO Safe, Doubles Unsupported, LSLEditor Safe
{//union float to integer
    if((input) != 0.0){//is it non zero?
        integer sign = (integer)(input < 0) << 31;//the sign, but later this variable is reused to store the shift
        if((input = llFabs(input)) < 2.3509887016445750159374730744445e-38)//Denormalized range check & last stride of normalized range
            return sign | (integer)(input / 1.4012984643248170709237295832899e-45);//the math overlaps; saves cpu time.
        if(input > 3.4028234663852885981170418348452e+38)//infinity generation for doubles x_x
            return sign | 0x7F800000;//return signed infinity
        integer exp = llFloor((llLog(input) / 0.69314718055994530941723212145818));//extremes will error towards extremes. following yuch corrects it.
        input /= llPow(2.0, exp -= ((exp >> 31) | 1));
        integer d = (integer)input - (3 <= input);
        return (0x7FFFFF & (integer)(input * (0x1000000 >> d))) | (((exp + 126 + d) << 23 ) | sign);
    }//for grins, detect the sign on zero. it's not pretty but it works. the previous requires alot of unwinding to understand it.
    return (integer)((string)input == (string)(-0.0)) << 31;
}

float iuf(integer input)//LSLEditor Safe, LSO Safe, Mono Safe
{//union integer to float
    if((input & 0x7FFFFFFF) == 0x7F800000)//Infinity Check
        return ((input >> 31) | 1) / 0.0;
    integer exp = 0xff & (input >> 23);
    return llPow(2.0, (exp | !exp) - 150) * (((!!exp) << 23) | ((input & 0x7fffff))) * (1 | (input >> 31));
}//will crash if the raw exponent == 0xff; reason for crash deviates from float standard; though a crash is warented.
```

## Change Log

#### 1.0

- New Macros for hiding implementation details of optimizations.

  - These macros can also be disabled so the resulting LSL is readable.
- New Macros for VM specific Order-of-Execution compiling.

  - More pointless parentheses are now generated. Too lazy at this time to create extra macros keep this from happening.
  - Only operators that are commutative are supported at this time.

  - Be warned: It won't stop you if you use a non-commutative operator and your code will be wrong.
  - This means that you can write optimized code and not have to worry about which VM is executing it.
- Many functions have been updated to use the new macros.

#### Unversioned

- Changes before 1.0 were never recorded.