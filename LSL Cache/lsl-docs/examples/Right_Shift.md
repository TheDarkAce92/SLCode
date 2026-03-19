---
name: "Right Shift"
category: "example"
type: "example"
language: "LSL"
description: "There are two types of Right Shifts, that can be performed on an integer. They are: Unsigned and Arithmetic. LSL currently only supports Arithmetic. The difference between the two modes is how it fills the bits revealed. With the unsigned mode, the revealed bits are always zero; in Arithmetic mode, it duplicates the old top bit to all the new bits. If you take the expression value >> count where value is arithmetically shifted right count bits, then this is the same mathematically as doing value / (2count) or in LSL value / llPow(2.0, count) (but will result in data loss in LSL)."
wiki_url: "https://wiki.secondlife.com/wiki/Right_Shift"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 Unsigned vs. Arithmetic
- 2 How to do Unsigned Right Shifts in LSL

  - 2.1 Method 1
  - 2.2 Method 2
- 3 Example Unsigned Right Shift Function

## Unsigned vs. Arithmetic

There are two types of Right Shifts, that can be performed on an integer. They are: Unsigned and Arithmetic. LSL currently only supports Arithmetic. The difference between the two modes is how it fills the bits revealed. With the unsigned mode, the revealed bits are always zero; in Arithmetic mode, it duplicates the old top bit to all the new bits. If you take the expression `value >> count` where *value* is arithmetically shifted right *count* bits, then this is the same mathematically as doing `value / (2count)` or in LSL `value / llPow(2.0, count)` (but will result in data loss in LSL).

## How to do Unsigned Right Shifts in LSL

Since LSL does not have a unsigned right shift operator you have to do it yourself. There are two methods for doing this, each with it's advantages and disadvantages.

There is a feature suggestion to add an unsigned right shift operator to LSL: [SVC-1171](https://jira.secondlife.com/browse/SVC-1171)

### Method 1

This method is good when count is dynamic (not known at compile time) but is twice as complicated as Method 2.

```lsl
((value & 0x7fFFffFF) >> count) - ((value & 0x80000000) >> count);
```

This works by shifting body and sign bits separately and then recombining them. Since the sign bit is extended as a negative number, we just need to make it positive. Since the left and right values have no bits in common (due to the masking), we can use | or + and they will do the same thing. To simplify the code we merge the negation and combine into a single operation.

### Method 2

This method can only be used when count is a constant value. It works by using a constant mask to remove the extended sign bits.

```lsl
(value >> count) & mask;
```

**Example:** `(value >> 5) & 0x07FFFFFF`**As you can see the top five bits have been turned off in the mask value, if you have trouble seeing that, you can just use the lookup table below. Mask Lookup Table**

Shift

Mask

Mask - Bit View

0

0xFFFFFFFF

11111111 1111111111111111 11111111 1 0x7FFFFFFF 01111111 1111111111111111 11111111 2 0x3FFFFFFF 00111111 1111111111111111 11111111 3 0x1FFFFFFF 00011111 1111111111111111 11111111 4 0x0FFFFFFF 00001111 1111111111111111 11111111 5 0x07FFFFFF 00000111 1111111111111111 11111111 6 0x03FFFFFF 00000011 1111111111111111 11111111 7 0x01FFFFFF 00000001 1111111111111111 11111111 Shift Mask Mask - Bit View 8 0x00FFFFFF 00000000 1111111111111111 11111111 9 0x007FFFFF 00000000 0111111111111111 11111111 10 0x003FFFFF 00000000 0011111111111111 11111111 11 0x001FFFFF 00000000 0001111111111111 11111111 12 0x000FFFFF 00000000 0000111111111111 11111111 13 0x0007FFFF 00000000 0000011111111111 11111111 14 0x0003FFFF 00000000 0000001111111111 11111111 15 0x0001FFFF 00000000 0000000111111111 11111111 Shift Mask Mask - Bit View 16 0x0000FFFF 11111111 11111111 17 0x00007FFF 01111111 11111111 18 0x00003FFF 00111111 11111111 19 0x00001FFF 00011111 11111111 20 0x00000FFF 00001111 11111111 21 0x000007FF 00000111 11111111 22 0x000003FF 00000011 11111111 23 0x000001FF 00000001 11111111 24 0x000000FF 00000000 11111111 25 0x0000007F 00000000 01111111 26 0x0000003F 00000000 00111111 27 0x0000001F 00000000 00011111 28 0x0000000F 00000000 00001111 29 0x00000007 00000000 00000111 30 0x00000003 00000000 00000011 31 0x00000001 00000000 00000001 32 0x00000000 00000000 00000000 ## Example Unsigned Right Shift Function Here's a function that encapsulates the first method. It allows for a signed 32 bit integer along with a value indicating how far to shift the bits to be executed as an unsigned right shift. ```lsl // the lsl right shift is an arithmetic right shift, // this means it more closely resembles dividing by a // positive power of two then a unsigned right shift. // To perform a unsigned right shift you need to be clever integer rightShift(integer value, integer count) { return ((value & 0x7fFFffFF) >> count) - ((value & 0x80000000) >> count); //This works by shifting body and sign bits separately and then //recombining them. Since the sign bit is extended as a negative //number, we just need to make it positive. Since the left and //right values have no bits in common (due to the masking), we //can use | or + and they will do the same thing. To simplify the //code we merge the negation and combine into a single operation. } // Jonhboy Resident integer rightShiftJonhboy(integer value, integer count) { if(count & 31) return ~(0x80000000 >> (count - 1)) & (value >> count); return value; //This works by conditionally applying a calculated mask after //shifting. The disadvantage of this method is that it is hard //to inline due to the condition, not to mention the cost of forking. } ``` Example Usage:

```lsl
default
{
    state_entry()
    {
        // output should be 268435449
        llSay(DEBUG_CHANNEL, (string)rightShift(-99, 4)); // output: 268435449
        llSay(DEBUG_CHANNEL, (string)rightShiftJonhboy(-99, 4));  // output: 268435449
        // before: 1111 1111 1111 1111 1111 1111 1001 1101
        // after:  0000 1111 1111 1111 1111 1111 1111 1001
    }
}
```