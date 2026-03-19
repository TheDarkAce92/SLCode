---
name: "LSL Types"
category: "types"
type: "reference"
language: "LSL"
description: "All LSL data types: integer, float, string, key, vector, rotation, list — with ranges, literals, casting, and pass-by-value semantics"
wiki_url: "https://wiki.secondlife.com/wiki/LSL_Types"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
---

# LSL Types

"A data type is a definition of the type or format of data."

LSL supports seven primary data types for variable declarations and function parameters.

## Data Types Overview

| Type | Description | Example |
|------|-------------|---------|
| `integer` | Whole number values (32-bit signed: 0x00000000 to 0xFFFFFFFF) | `42` |
| `float` | Floating-point decimal number (IEEE 754 single precision) | `3.14159` |
| `string` | Text data (sequence of UTF-8 characters) | `"Hello, world!"` |
| `key` | UUID identifier (Universally Unique Identifier) | `"1fc26194-b2c1-e5e3-20e5-45cb3ae7f73e"` |
| `vector` | 3D coordinate or direction (three floats: x, y, z) | `<1.0, 2.0, 3.0>` |
| `rotation` | 3D rotation stored as a quaternion (four floats: x, y, z, s) | `<0.0, 0.0, 0.0, 1.0>` |
| `list` | Ordered container for mixed-type values | `[42, 3.14, "value", <1,2,3>]` |

## integer

A 32-bit signed integer. Valid range: -2147483648 to 2147483647 (0x80000000 to 0x7FFFFFFF).

Literals can be written in decimal or hexadecimal:

```lsl
integer a = 42;
integer b = -7;
integer c = 0xFF;      // 255
integer d = 0x80000000; // -2147483648 (wraps to negative)
```

Boolean: LSL has no boolean type. Use `integer` with `TRUE` (1) and `FALSE` (0).

## float

An IEEE 754 single-precision (32-bit) floating-point number.

```lsl
float a = 3.14159;
float b = -0.5;
float c = 1.0e10;
float d = 1.5e-3;
```

Floats have approximately 6-7 significant decimal digits of precision. Very large or very small values may lose precision.

## string

A sequence of characters. LSL uses UTF-8 encoding internally. Strings are immutable — operations always create new strings.

```lsl
string greeting = "Hello, world!";
string empty = "";
string escaped = "She said \"hi\".\nNew line here.";
```

Escape sequences: `\"` (quote), `\\` (backslash), `\n` (newline), `\t` (tab).

Maximum string length: 255 characters for most function parameters; script-level strings may be larger (up to 64 KB).

## key

A UUID (Universally Unique Identifier). Keys identify objects, avatars, textures, sounds, notecards, and other assets in Second Life.

```lsl
key owner = llGetOwner();
key nullKey = NULL_KEY;  // "00000000-0000-0000-0000-000000000000"
```

A key is not a string, but can be cast to/from string:

```lsl
key k = (key)"some-uuid-string";
string s = (string)k;
```

`NULL_KEY` is the constant for an invalid/empty key.

## vector

A 3-component floating-point value representing a 3D position, direction, or colour (RGB).

```lsl
vector pos = <128.0, 128.0, 20.5>;
vector red = <1.0, 0.0, 0.0>;
vector zero = ZERO_VECTOR;  // <0.0, 0.0, 0.0>
```

Components are accessed with `.x`, `.y`, `.z`:

```lsl
vector v = <1.0, 2.0, 3.0>;
float x = v.x;  // 1.0
v.y = 5.0;
```

## rotation

A quaternion representing a 3D orientation. Components are x, y, z (imaginary) and s (scalar/real).

```lsl
rotation rot = <0.0, 0.0, 0.0, 1.0>;  // identity rotation (no rotation)
rotation zeroRot = ZERO_ROTATION;
```

Components accessed with `.x`, `.y`, `.z`, `.s`:

```lsl
rotation r = llGetRot();
float s = r.s;
```

**Important:** Do not set rotation components directly for most rotation operations — use `llEuler2Rot`, `llAxisAngle2Rot`, or multiply rotations together.

## list

An ordered, heterogeneous collection of any LSL types (except other lists). Lists are zero-indexed.

```lsl
list empty = [];
list mixed = [42, 3.14, "hello", <1,2,3>];
list names = ["Alice", "Bob", "Carol"];
```

Lists are not nested — attempting to put a list inside a list flattens it:

```lsl
list a = [1, 2];
list b = [3, 4];
list c = a + b;  // [1, 2, 3, 4]  — concatenation, not nesting
```

Common list operations use `llList2*` functions:

```lsl
integer len = llGetListLength(names);  // 3
string first = llList2String(names, 0);  // "Alice"
```

## Basic Variable Declaration

```lsl
integer myInt = 123;
float myFloat = 1.5;
string myString = "text";
key myKey = NULL_KEY;
vector myVec = <0.0, 0.0, 0.0>;
rotation myRot = ZERO_ROTATION;
list myList = [];
```

Variables declared at script scope are global. Variables declared inside functions or event handlers are local.

## Type Casting

LSL supports explicit type casting with `(type)` syntax:

| From | To | Notes |
|------|----|-------|
| `integer` | `float` | Exact when in range |
| `float` | `integer` | Truncates toward zero |
| `integer` | `string` | Decimal representation |
| `float` | `string` | 6 decimal places |
| `string` | `integer` | Parses leading digits; 0 if none |
| `string` | `float` | Parses as decimal |
| `key` | `string` | UUID string |
| `string` | `key` | UUID from string |
| `vector` | `string` | `"<x, y, z>"` format |
| `string` | `vector` | Parses `"<x, y, z>"` |
| `rotation` | `string` | `"<x, y, z, s>"` format |
| `string` | `rotation` | Parses `"<x, y, z, s>"` |
| `list` | `string` | Concatenates all elements |
| `integer` | `list` | Single-element list |

```lsl
// Casting examples
string s = (string)42;          // "42"
integer i = (integer)3.7;       // 3 (truncated)
string fs = (string)3.14;       // "3.140000"
key k = (key)"00000000-0000-0000-0000-000000000000";
string vs = (string)<1.0, 2.0, 3.0>;  // "<1.000000, 2.000000, 3.000000>"

// List to string concatenation
string message = (string)["I have ", 5, " items costing ", 8.20, " each"];
// Result: "I have 5 items costing 8.200000 each"
```

## Pass-by-Value Semantics

"LSL as a language uses pass-by-value for all types."

When a value is passed as a parameter to a function, that function receives its own unique copy. Modifications within the function do not affect the original variable.

```lsl
swap(string a, string b) {
    string t = a;
    a = b;
    b = t;
    // Only the local copies are swapped; caller's variables unchanged
}

default {
    state_entry() {
        string a = "1";
        string b = "2";
        llOwnerSay(llList2CSV([a, b]));  // "1, 2"
        swap(a, b);                       // Does NOT modify a or b
        llOwnerSay(llList2CSV([a, b]));  // "1, 2" — unchanged
    }
}
```

**Implementation note:** The compiled VMs use reference types internally, so passing large lists or strings is not as memory-expensive as it might appear — a full copy is only made if the value is modified.
