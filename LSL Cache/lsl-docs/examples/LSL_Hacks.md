---
name: "LSL Hacks"
category: "example"
type: "example"
language: "LSL"
description: "A page dedicated to LSL Hacks, those things that make your code so much better but at the same time so much worse."
wiki_url: "https://wiki.secondlife.com/wiki/LSL_Hacks"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL

- 1 Hacks

  - 1.1 llMessageLinked key parameter as string
  - 1.2 llGetListLength(myList) and (myList != [])
  - 1.3 ++c and c++
  - 1.4 (c = -~c) same as ++c
  - 1.5 Testing key validity
  - 1.6 if(~c) and if(c != -1)
  - 1.7 myList = (myList = []) + and myStr = (myStr = "") +  Hack
  - 1.8 32bit hexadecimal notation instead of negative integer notation for constants (ex: 0xFFFFFFFF instead of -1)
  - 1.9 Cast negative number to itself
  - 1.10 VM Detection
  - 1.11 (c & 0x80000000) instead of (c < 0)
  - 1.12 (c & power_of_two_minus_one) instead of (c % power_of_two)
  - 1.13 Multiplying by reciprocal instead of dividing
  - 1.14 HTML-on-a-prim hacks
- 2 Footnotes

Hacks

A page dedicated to LSL Hacks, those things that make your code so much better but at the same time so much worse.


      ⚠️
      **Warning:** The below comments in regards to speed is unverified on modern simulator versions, and thus cannot be assumed to be true.**Always test execution speed claims for yourself.**


**## llMessageLinked key parameter as string VM**: LSO

**Discover**: Unknown

Instead of passing a valid key as the forth parameter of the llMessageLinked function, a string value can be used. When the link_message event is triggered, the key can be typecast to a string (implicitly or explicitly) without any value degradation.

```lsl
llMessageLinked(LINK_THIS, 10, "Hello", "World!")
```

**Pros**

- Allows for a second string to be sent to the receiving scripts
- Faster then splitting a single string into two.

**Cons**

- May no longer be a valid key value.

## llGetListLength(myList

**VM**: LSO

**Discover**: Strife Onizuka

- Instead of using `llGetListLength(myList)` you can use `(myList != [])`.
- Instead of using `-llGetListLength(myList)` you can use `([] != myList)`.

**Pros**

- Faster
- Uses less bytecode

**Cons**

- Less readable
- Will likely be removed in LSL3
- Mono's llGetListLength function has been optimized and is about 100% faster than `list!=[]`;

## ++c

**VM**: LSO

**Discover**: Not Applicable

In LSO LSL (as opposed to Mono LSL) ++c is faster than c++ because of how the bytecode is generated. There are very few applications where ++c can't be used instead.

**Pros**

- Faster code.
- Saves 6 bytes and 2 instructions.

**Cons**

- None

## (c

**VM**: LSO

**Discover**: Strife Onizuka

For the same instruction cost of `(++c)`, `(c = -~c)` can be substituted giving a 4 byte savings.

**Pros**

- Saves 4 bytes of bytecode.

**Cons**

- Will fail on hardware that doesn't support two's compliment (unlikely LL will ever use such a platform).
- Harder to understand.

## Testing key validity

**VM**: LSO & Mono

**Discover**: Strife Onizuka

By passing the key value to a conditional, if it is valid and not a NULL_KEY then it will execute the true branch.

```lsl
integer isKey(key in) {
    if(in) return 2;
    return (in == NULL_KEY);
}
```

**Pros**

- Fast
- Easy
- Painless

**Cons**

- Can give false positives if the variable type is not a key
- can only be tested by itself

## if(~c

**VM**: LSO

**Discover**: Unknown

Instead of using `if(c != -1)` you can use `if(~c)`. This applies to all conditionals.

**Pros**

- Faster (60%)
- Uses less bytecode (6 bytes, 1 instruction)

**Cons**

- Harder to understand
- Only for Integers

## myList = (myList = []) + and myStr = (myStr = "") + Hack

**VM**: LSO

**Discover**: Strife Onizuka

This hack works equally well for both strings and lists.

Instead of using `myList = myList + addition` you can use `myList = (myList = []) + myList + addition` which will in certain situations reduce memory fragmentation. Memory fragmentation can result in what appears to be a memory leak. This works because LSL execution is Right-To-Left, it frees the value stored at the variable's memory location after copying it to the stack but before storing the return back to the location; the result can be better memory compacting.

**Pros**

- Possibility of reduced memory fragmentation

**Cons**

- More costly in bytecode and slower
- Doesn't work in LSLEditor (LSLEditor uses Left-To-Right order of execution).
- No real benefit when used in Mono
- Possibility of slightly increasing memory fragmentation

**Notes**

- Be sure to test it both ways around before using this.
- This can also be used with any function.

  - `llDeleteSubList((myList = []) + myList, x, y)`

## 32bit hexadecimal notation instead of negative integer notation for constants (ex: 0xFFFFFFFF instead of -1)

**VM**: LSO, Mono

**Discover**: Void Singer

instead of using negative integer constants in code (does not apply to global declarations) use the 32bit hexadecimal notation. Works because the compiler does not optimize out the negation sign for integer literals (LSO confirmed, Mono confirmed)

**Pros**

- Faster (one less operation)
- Less Byte Code (2 bytes saved on the operation under LSO, 1 under Mono)

**Cons**

- Harder to read

## Cast negative number to itself

**VM**: Mono

**Discoverer**: Pedro Oval

When using a negative integer constant, add a type cast to integer. Under Mono, a type cast of a type to itself adds no extra code, and in the case of negatives, it can parse the number as a negative integer rather than adding a negate operator, saving 1 byte and being slightly faster.

The same can be done with negative floating point constants: cast them to float.

**Examples:**

```lsl
integer i = (integer)-1; // sets i to -1 and saves 1 byte
float f = (float)-1.0; // sets f to -1.0 and saves 1 byte
```

**Note:** Don't use `(integer)(-1)` or `(float)(-1.0)` as that destroys the magic. Put the minus sign immediately after the closing parenthesis of the type cast.

**Pros**

- Easier to read than 0xFFFFFFFF
- Applicable to more numbers without significant loss of readability
- Applicable to floats too
- Less byte code under Mono

**Cons**

- Not usable with LSO, as LSO still adds a type cast which is also 2 bytes, thus saving nothing

## VM Detection



**VM**: Both

**Discoverer**: Void Singer

```lsl
(llToLower( "Ü" ) == "Ü"); //-- yields TRUE for LSO, and FALSE for MONO.
(llToLower( "Ü" ) != "Ü"); //-- yields TRUE for MONO, and FALSE for LSO.
```

**Pros**

- Gives a boolean result (0 or 1) in two variations.

**Cons**

- Uses a function call (about 63 bytes of code memory total)
- Uses an Unicode character not available in many keyboards, thus it isn't immediate to type

**VM**: Both

**Discoverer**: Strife Onizuka

```lsl
(llGetListEntryType( (list)((key)"") ) & 1); //-- yields TRUE for LSO, and FALSE for MONO.
(llGetListEntryType( (list)((key)"") ) >> 2); //-- yields TRUE for MONO, and FALSE for LSO.
```

**Pros**

- Gives a boolean result (0 or 1) in two variations.

**Cons**

- Uses a function call and several operators, meaning more code memory than other methods
- Doesn't work as written

**VM**: Both

**Discoverer**: Pedro Oval

```lsl
(""!="x")  //-- yields -1 for LSO, 1 for MONO
```

**Comments**

Any non-empty string works for the right hand side. Just keep the empty string on the left. Appears to yield a strcmp of the UTF-8 strings under LSO, and a real boolean result (yielding either 0 or 1 and nothing else) under Mono.

**Pros**

- Small code memory usage, as it uses no function calls (about 19 bytes code memory total)
- Easy to remember and thus to type

**Cons**

- Doesn't yield TRUE/FALSE.

**```lsl ~(""!="x") //-- yields FALSE for LSO, -2 for MONO ``` Pros**

- Small code memory usage, as it uses no function calls (about 20 bytes code memory total)
- Easy to remember and thus to type
- Result is directly usable as an `if` condition, for example:

```lsl
if (~(""!="x")) llOwnerSay("VM is Mono"); else llOwnerSay("VM is LSO");
```

**Cons**

- Doesn't yield 1 (TRUE) for Mono.

**```lsl !~(""!="x") //-- yields TRUE for LSO, FALSE for MONO !~-(""!="x") //-- yields FALSE for LSO, TRUE for MONO ``` Pros**

- Small code memory usage, as it uses no function calls (about 23/24 bytes code memory total resp.)
- Gives a boolean result (0 or 1) in two variations.

**Cons**

- They use 3 and 4 extra code memory bytes respectively with respect to other versions.

**```lsl llList2Key([], 0)=="" //-- yields TRUE for MONO, FALSE for LSO ``` Cons**

- Uses a function call (70 bytes code memory in total)

## (c & 0x80000000) instead of (c < 0)

**VM**: LSO

**Discover**: Unknown

Instead of checking if an integer is less than 0 using the comparison operator, the bitwise AND operator can be used to check for the sign-bit. If the sign bit (0x80000000) is true, then the number is negative, and thus less than 0.

**Pros**

- Saves one byte

**Cons**

- Harder to understand
- Only for Integers

## (c & power_of_two_minus_one) instead of (c % power_of_two)

**VM**: LSO

**Discover**: Unknown

Instead of using the modulus operator with a power of two (such as 2^2 or 4), the bitwise AND operator can be used with the value of the power of two minus one (such as 3 instead of 4).

```lsl
if(var & 3);
```

 will work the same as

```lsl
if(var % 4);
```

**Pros**

- Saves one byte in LSO, four in Mono
- 500% faster in Mono.
- A few percent faster in LSL.

**Cons**

- Harder to understand

## Multiplying by reciprocal instead of dividing

**VM**: Both

**Discover**: Unknown

Implementations of division as a whole are more complex than implementations of multiplication. This includes the algorithmic implementation on a hardware level. Because of this, multiplication is faster than division. Many compilers will automatically 'optimize' these sort of tiny things where possible. Only 'where possible' because sometimes floating-point rounding error can make an output difference. LSL doesn't do it at all.

For example, x/2.0 will have the same output as x*0.5, but will run faster.

**Pros**

- A few percent faster in LSL with floats; about 10 to 15% faster in LSL with integers.
- About 600% faster in Mono with floats; about 1000% faster in Mono with integers.

**Cons**

- May be less intuitive depending on implementation.
- In the scheme of things, the time difference is tiny. Still interesting regardless!

## HTML-on-a-prim hacks

All sorts of tricks you never thought that the SL Viewer was able to do with MOAP:

User:Ama_Omega/archive/lsl_hacks

Footnotes

1. **^** Plans for LSL3 are still being worked out, nothing has been finalized, no release date has been set, LSL3 may in-fact never happen.
1. **^** The LSO LSL compiler does not produce optimized code.