---
name: "Float2Hex"
category: "example"
type: "example"
language: "LSL"
description: "Use to encode floats in hex notation, minimal overhead, does not introduce errors. No special decoder needed. Try it. Use this instead of (string) when converting floats to strings."
wiki_url: "https://wiki.secondlife.com/wiki/Float2Hex"
author: "me"
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL

- 1 About

  - 1.1 Update
- 2 Float2Hex

  - 2.1 Double Unsafe
  - 2.2 Safe
  - 2.3 Overkill
  - 2.4 Usage
  - 2.5 Helper Functions
  - 2.6 How it works

## About

Use to encode floats in hex notation, minimal overhead, does not introduce errors. No special decoder needed. Try it.

 Use this instead of (string) when converting floats to strings.

LSL (float) typecast supports [C99 hex floats](http://gcc.gnu.org/onlinedocs/gcc/Hex-Floats.html). This is good because with hex you can store floats without the need for a special decoder (just use (float)) and since hex is a power of 2 format, floats can be stored without any loss or rounding errors.

A similar function (also by me) Float to Scientific Notation, works much the same way (except it uses base 10). The trouble is it has to emulates higher precision math; in a scripting language this is a bad solution. Because of the base conversion using logs would introduce a huge accumulated error (read as: floats suck). Resulting in the need to do the shifting with a while loop. This wasn't good enough, even with 32 bits, small numbers would still be corrupted by the shifting. An integer and a float (or in one rewrite two integers) were used, one to store the integer portion, and the other the float. This worked, but was slow for large and small numbers (2 seconds). Finally some optical approaches were used to do the conversion which sped up large numbers. While accurate, the function was slow and used a lot of memory.

This function is much faster, it requires about 300 instructions with little deviation from that number (unless the input is zero, which takes about 20 instructions). In the scheme of things it is not too costly. There isn't much that can be done to reduce the number of instructions executed, unless LL wants to give us an llInteger2HexString or an llFloat2HexString. A built in function would have the benefit of direct access to the memory that holds the float, much of the math performed here could be eliminated (see User:Strife_Onizuka/Float_Functions#FUI2HexFloat).

### Update

- Full and seamless support for doubles.
- Better handling of rounding errors in the exponent (removes need for boundary checking)

## Float2Hex

### Double Unsafe

Fast & accurate in LSO and Mono but will not return full double precision in LSLEditor. LSLEditor is a bit of a moving target anyway so best not to worry about it.



```lsl
string hexc="0123456789ABCDEF";//faster

string Float2Hex(float input)// Doubles Unsupported, LSO Safe, Mono Safe
{// Copyright Strife Onizuka, 2006-2007, LGPL, http://www.gnu.org/copyleft/lesser.html or (cc-by) http://creativecommons.org/licenses/by/3.0/
    if(input != (integer)input)//LL screwed up hex integers support in rotation & vector string typecasting
    {
        string str = (string)input;
        if(!~llSubStringIndex(str, ".")) return str; //NaN and Infinities, it's quick, it's easy.
        float unsigned = llFabs(input);//logs don't work on negatives.
        integer exponent = llFloor((llLog(unsigned) / 0.69314718055994530941723212145818));//floor(log2(b)) + rounding error

        integer mantissa = (integer)((unsigned / (float)("0x1p"+(string)(exponent -= ((exponent >> 31) | 1)))) * 0x4000000);//shift up into integer range
        integer index = (integer)(llLog(mantissa & -mantissa) / 0.69314718055994530941723212145818);//index of first 'on' bit
        str = "p" + (string)(exponent + index - 26);
        mantissa = mantissa >> index;
        do
            str = llGetSubString(hexc, 15 & mantissa, 15 & mantissa) + str;
        while(mantissa = mantissa >> 4);

        if(input < 0)
            return "-0x" + str;
        return "0x" + str;
    }//integers pack well so anything that qualifies as an integer we dump as such, supports negative zero
    return llDeleteSubString((string)input,-7,-1);//trim off the float portion, return an integer
}
```

### Safe

This version isn't as fast but will work in LSLEditor, LSO and Mono.

```lsl
string hexc="0123456789ABCDEF";//faster

string Float2Hex(float input)// Supports Doubles, LSO Safe, Mono Safe
{// Copyright Strife Onizuka, 2006-2007, LGPL, http://www.gnu.org/copyleft/lesser.html or (cc-by) http://creativecommons.org/licenses/by/3.0/
    if(input != (integer)input)//LL screwed up hex integers support in rotation & vector string typecasting
    {
        string str = (string)input;
        if(!~llSubStringIndex(str, ".")) return str; //NaN and Infinities, it's quick, it's easy.
        float unsigned = llFabs(input);//logs don't work on negatives.
        integer exponent = llFloor((llLog(unsigned) / 0.69314718055994530941723212145818));//floor(log2(b)) + rounding error

        integer mantissa_a = (integer)(unsigned = ((unsigned / (float)("0x1p"+(string)(exponent -= ((exponent >> 31) | 1)))) * 0x4000000));
        integer index = (integer)(llLog(mantissa_a & -mantissa_a) / 0.69314718055994530941723212145818);//index of first 'on' bit
        str = "p" + (string)(exponent + index - 26);//final exponent for single or simple double
        integer mantissa_b = (integer)((unsigned - mantissa_a) * 0x10000000);
        if(mantissa_b)//this code only gets activated if the lower bytes of the double mantissa are set
        {//this code won't get activated in single precision environments
            str = "p" + (string)(exponent + (index = (integer)(llLog(mantissa_b & -mantissa_b) / 0.69314718055994530941723212145818)) - 54);
            mantissa_b = (mantissa_b >> index) | ((mantissa_a << (28 - index)) & 0x0FFFFFFF);//mask it so we can shift check
            exponent = -7 * !!(mantissa_a >> index);// use the shift checking exclusively if there is no mantissa_a
            do// if there is mantissa_a then the loop must run 7 times; otherwise run as many times as needed
                str = llGetSubString(hexc, 15 & mantissa_b, 15 & mantissa_b) + str;
            while((mantissa_b = (mantissa_b >> 4)) | ((exponent = -~exponent) & 0x80000000));//dodge bugs in LSLEditor
        }// mantissa_a will always be non-zero before shifting unless it is in the denormalized range.
        if((mantissa_a = (mantissa_a >> index)))//if it is double then after the shifting we can't be sure
            do//we wouldn't want to pad the output with an extra zero by accident.
                str = llGetSubString(hexc, 15 & mantissa_a, 15 & mantissa_a) + str;
            while((mantissa_a = (mantissa_a >> 4)) );

        if(input < 0)
            return "-0x" + str;
        return "0x" + str;
    }//integers pack well so anything that qualifies as an integer we dump as such, supports negative zero
    return llDeleteSubString((string)input,-7,-1);//trim off the float portion, return an integer
}
```

### Overkill

This version will eat up as much precision as the hardware supports

```lsl
string hexc="0123456789ABCDEF";

string Float2Hex(float input)//Float width irrelevant, LSO Safe, Mono Safe
{// Copyright Strife Onizuka, 2006-2007, LGPL, http://www.gnu.org/copyleft/lesser.html or (cc-by) http://creativecommons.org/licenses/by/3.0/
    if(input != (integer)input)//LL screwed up hex integers support in rotation & vector string typecasting
    {
        string str = (string)input;
        if(!~llSubStringIndex(str, ".")) return str; //NaN and Infinities, it's quick, it's easy.
        float unsigned = llFabs(input);//logs don't work on negatives.
        integer exponent = llFloor((llLog(unsigned) / 0.69314718055994530941723212145818));//floor(log2(b)) + rounding error
        unsigned /= (float)("0x1p"+(string)(exponent -= ((exponent >> 31) | 1)));
        integer count = -1;
        integer group = 0;
        list mantissa = [];
        do{
            count = -~count;
            mantissa += group = (integer)(unsigned *= 0x10000000);
        }while((unsigned -= group));
        integer index = (integer)(llLog(group & -group) / 0.69314718055994530941723212145818);//index of first 'on' bit
        str = "p" + (string)(exponent + index + (28 * ~count));//final exponent for single or simple double
        mantissa += 0;
        do{
            exponent = -7 * !!count;
            integer value = group >> index;
            value = value | (((group = llList2Integer(mantissa, (count = ~-count))) << (28 - index)) & 0x0FFFFFFF);
            do//if this is not the last value the loop must run 7 times; otherwise run as many times as needed
                str = llGetSubString(hexc, 15 & value, 15 & value) + str;
            while((value = (value >> 4)) | ((exponent = -~exponent) & 0x80000000));//dodge bugs in LSLEditor
        }while(~count);
        if(input < 0)
            return "-0x" + str;
        return "0x" + str;
    }//integers pack well so anything that qualifies as an integer we dump as such, supports negative zero
    return llDeleteSubString((string)input,-7,-1);//trim off the float portion, return an integer
}
```



### Usage

```lsl
string a = Float2Hex(100.000000); // a == "100"
string b = Float2Hex(14353.344727); // b == "0xE04561p-10"
float c = (float)a;//c == 100.000000
float d = (float)b;//d == 14353.344727
```

### Helper Functions

```lsl
string Rot2Hex(rotation a)
{
    return "<"+Float2Hex(a.x)+","+Float2Hex(a.y)+","+Float2Hex(a.z)+","+Float2Hex(a.s)+">";
}

string Vec2Hex(vector a)
{
    return "<"+Float2Hex(a.x)+","+Float2Hex(a.y)+","+Float2Hex(a.z)+">";
}

string DumpList2String(list input, string seperator)// for csv use ", " as the seperator.
{// LSLEditor Unsafe, LSO Safe, Mono Safe
    integer b = (input != []);
    string c;
    string d;
    integer e;
    if(b)
    {
        @top;
        if((e = llGetListEntryType(input,--b)) == TYPE_FLOAT)
            d=Float2Hex(llList2Float(input,b));
        else if(e == TYPE_ROTATION)
            d=Rot2Hex(llList2Rot(input,b));
        else if(e == TYPE_VECTOR)
            d=Vec2Hex(llList2Vector(input,b));
        else
            d=llList2String(input,b);
        if(b)
        {
            c = d + (c=seperator) + c;
            jump top;
        }
    }
    return (c=d) + c;
}
```

### How it works

```lsl
string hexc="0123456789ABCDEF";//faster

string Float2Hex(float input)// LSLEditor Safe, LSO Safe, Mono Safe
{// Copyright Strife Onizuka, 2006-2007, LGPL, http://www.gnu.org/copyleft/lesser.html or (cc-by) http://creativecommons.org/licenses/by/3.0/
    //LL screwed up hex integers support in rotation & vector string typecasting
    if(input != (integer)input)
    {
        //Convert it to a string and see if it has a decimal in it, if it does not, it's a string.
        string str = (string)input;
        if(!~llSubStringIndex(str, ".")) return str; //NaN and Infinities, it's quick, it's easy.
        //logs don't work on negatives.
        float unsigned = llFabs(input);
        //calculate the exponent, this value is approxomit and it unfortunately will be rounded towards the extreams
        integer exponent = llFloor((llLog(unsigned) / 0.69314718055994530941723212145818));//floor(log2(b)) + rounding error
        //adjust the exponent so it errors towards zero
        //if we don't adjust it, it will crash the script on overflow (bad)
        exponent -= ((exponent >> 31) | 1);
        //using the exponent calculate the upper part of the mantisa with a few extra bits
        unsigned = (unsigned / llPow(2., exponent)) * 0x4000000;
        //store it to an integer
        integer mantissa_a = (integer)unsigned;
        //find the first turned on bit, this also corrects for the rounding errors in the exponent
        integer index = (integer)(llLog(mantissa_a & -mantissa_a) / 0.69314718055994530941723212145818);//index of first 'on' bit
        //write the final exponent for single or simple double
        string str = "p" + (string)(exponent + index - 26);
        //subtract the upper part of the mantisa from the mantisa so that we have the fpart left
        integer mantissa_b = (integer)((unsigned - mantissa_a) * 0x10000000);
        //check to see if there is an fpart
        if(mantissa_b)
        {
            //this code only gets activated if the lower bytes of the double mantissa are set
            //this code won't get activated in single percission environments
            //there was an fpart so the shift and final exponenet are wrong
            index = (integer)(llLog(mantissa_b & -mantissa_b) / 0.69314718055994530941723212145818);
            //generate the new final exponent
            str = "p" + (string)(exponent + index - 54);
            //apply the shift and adds some bits from the upper part
            //mask it so it so we can shift check
            mantissa_b = (mantissa_b >> index) | ((mantissa_a << (28 - index)) & 0x0FFFFFFF);
            //use the shift checking exclusively if there is no upper part to the mantissa
            //we recycle exponent
            exponent = -7 * !!mantissa_a;
            //if there is an upper part to the mantissa then the loop must run 7 times; otherwise run as many times as needed (less then 7 maybe)
            //we do this by peaking at the sine on exponent
            do
                str = llGetSubString(hexc, 15 & mantissa_b, 15 & mantissa_b) + str;
            while((mantissa_b = (mantissa_b >> 4)) | ((exponent = -~exponent) & 0x80000000));//dodge bugs in LSLEditor
        }
        //mantissa_a will always be non-zero before shifting unless it is in the denormalized range.
        //if it is double then after the shifting we can't be sure
        //we wouldn't want to pad the output with an extra zero by accident.
        if((mantissa_a = (mantissa_a >> index)))
            do
                str = llGetSubString(hexc, 15 & mantissa_a, 15 & mantissa_a) + str;
            while((mantissa_a = (mantissa_a >> 4)) );
        //Put the sign and 0x on
        if(input < 0)
            return "-0x" + str;
        return "0x" + str;
    }
    //integers pack well so anything that qualifies as an integer we dump as such, supports netative zero
    //trim off the float portion, return an integer
    return llDeleteSubString((string)input,-7,-1);
}
```