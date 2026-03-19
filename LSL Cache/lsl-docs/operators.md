---
name: "LSL Operators"
category: "operators"
type: "reference"
language: "LSL"
description: "All LSL operators: arithmetic, comparison, logical, bitwise, assignment, string/list concatenation — with precedence table and type rules"
wiki_url: "https://wiki.secondlife.com/wiki/LSL_Operators"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
---

# LSL Operators

## Operator Precedence Table

Operators are listed in descending order of evaluation precedence (highest precedence first).

| Operator | Description | Usage Example |
|----------|-------------|---------------|
| `()` | Parentheses — grouping and precedence override | `integer val = a * (b + c);` |
| `[]` | Brackets — list constructor | `list lst = [a, 2, "this", 0.01];` |
| `(type)` | Typecast | `string s = "Result: " + (string)result;` |
| `!` `~` `++` `--` | Logical NOT, bitwise NOT, increment, decrement | `counter++;` |
| `*` `/` `%` | Multiply / dot product, divide, modulus / cross product | `integer r = (count + 1) % 5;` |
| `+` `-` | Addition / string concat / list concat, subtraction / unary negation | `string t = "Hello" + " world";` |
| `<<` `>>` | Arithmetic left shift, arithmetic right shift | `integer eight = 4 << 1;` |
| `<` `<=` `>` `>=` | Relational comparison | `integer isFalse = (6 <= 4);` |
| `==` `!=` | Equality, inequality | `integer isFalse = ("this" == "that");` |
| `&` | Bitwise AND | `integer zero = 4 & 2;` |
| `^` | Bitwise XOR | `integer six = 4 ^ 2;` |
| `\|` | Bitwise OR | `integer six = 4 \| 2;` |
| `&&` `\|\|` | Logical AND, logical OR | `integer isTrue = (FALSE \|\| TRUE);` |
| `=` `+=` `-=` `*=` `/=` `%=` | Assignment operators | `eight *= 2;` |

## Critical Behavioural Notes

### Both Operands of `&&` and `||` Are ALWAYS Evaluated

**Unlike most C-style languages, LSL evaluates BOTH sides of `&&` and `||` regardless of the left operand's value.** There is no short-circuit evaluation.

```lsl
if (TRUE || 1/0)
    llSay(PUBLIC_CHANNEL, "Aha!");
// This causes a Math Error, NOT "Aha!" — because 1/0 is always evaluated.
```

### `&&` and `||` Have EQUAL Precedence

In most languages, `&&` has higher precedence than `||`. In LSL, they share the same precedence level. This produces surprising results:

```lsl
1 || 1 && 0  // evaluates as (1 || 1) && 0 → 0  (LSL)
// In C/Java/Python this would be: 1 || (1 && 0) → 1
```

Note that the bitwise operators DO follow standard precedence (`&` > `^` > `|`):

```lsl
1 | 1 & 0    // evaluates as 1 | (1 & 0) → 1  (correct)
```

### Right-to-Left Evaluation Order

Expressions are evaluated right-to-left in LSL:

```lsl
// x starts at 1
(x && (x = 0) == 0 && x)
// Evaluates: x (rightmost) first, then (x=0)==0, then x (leftmost)
```

### Pre- vs Post-Increment/Decrement

Pre-increment (`++x`): modifies the variable first, then the expression uses the new value.
Post-increment (`x++`): the expression uses the original value, then the variable is modified.

```lsl
integer count = 0;
if (++count == 1)  // count is incremented THEN compared → TRUE
    llSay(PUBLIC_CHANNEL, "Aha");  // This IS said

integer count = 0;
if (count++ == 1)  // count is compared THEN incremented → FALSE (0 != 1)
    llSay(PUBLIC_CHANNEL, "Aha");  // This is NOT said
```

## Arithmetic Operators

### Addition (`+`) Type Rules

| Left Type | Right Type | Result Type | Behaviour |
|-----------|-----------|------------|-----------|
| `integer` | `integer` | `integer` | Numeric addition |
| `integer` | `float` | `float` | Numeric addition |
| `float` | `integer` | `float` | Numeric addition |
| `float` | `float` | `float` | Numeric addition |
| `string` | `string` | `string` | String concatenation |
| `list` | `*` | `list` | Appends right onto end of list |
| `*` | `list` | `list` | Prepends left onto start of list |
| `vector` | `vector` | `vector` | Component-wise addition |
| `rotation` | `rotation` | `rotation` | Component-wise addition (not useful for combining rotations; use `*` or `/`) |

**Note:** `== !=` applied to lists compares only lengths, not contents.

### Multiplication (`*`) Type Rules

| Left Type | Right Type | Result Type | Behaviour |
|-----------|-----------|------------|-----------|
| `integer` | `integer` | `integer` | Multiplication |
| `float` / `integer` | `float` / `integer` | `float` | Multiplication |
| `vector` | `vector` | `float` | Dot product |
| `vector` | `float` / `integer` | `vector` | Scalar multiplication |
| `float` / `integer` | `vector` | `vector` | Scalar multiplication |
| `rotation` | `rotation` | `rotation` | Quaternion multiplication (combines rotations) |
| `vector` | `rotation` | `vector` | Rotates vector by rotation |

### Modulus (`%`) Operator

Type restriction: `%` only accepts `integer` (modulus) and `vector` (cross product) operands.

Division by zero causes a script runtime Math Error.

Mathematical definition: `a % b` is equivalent to `a - (a/b) * b` where integer division truncates toward zero.

Sign rule: the result always has the same sign as the first operand.

```lsl
-7 % 3   // = -1  (negative because first operand is negative)
 7 % -3  // =  1  (positive because first operand is positive)
```

Optimization with powers of two — if second operand is a positive power of 2, `%` can be replaced by `&`:

```lsl
7 % 4   // = 3
7 & 3   // = 3  (faster, but only valid for positive power-of-2 divisors with positive dividend)
```

**Floating-point modulus** (no direct operator — use formula):

```lsl
// Extract fractional part of a float:
float frac = 7.8813 - (integer)(7.8813);  // = 0.8813

// Wrap angle within TWO_PI radians:
float wrapped = 7.8813 - (integer)(7.8813 / TWO_PI) * TWO_PI;  // = 1.598114
```

Even/odd test:

```lsl
if (input % 2 == 0) {
    // even
} else {
    // odd
}
```

## Shift Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `<<` | Arithmetic left shift | `4 << 1` = 8; `4 << 2` = 16 |
| `>>` | Arithmetic right shift (sign-extends) | `-2 >> 1` = -1; `8 >> 1` = 4 |

Both operators only accept `integer` operands. Shifting by 0–31 is defined; shifting by negative amounts or ≥32 produces 0.

## Comparison Operators

Relational operators (`<`, `<=`, `>`, `>=`) and equality operators (`==`, `!=`) return `integer` 1 (TRUE) or 0 (FALSE).

- `integer`, `float`: numeric comparison
- `string`: lexicographic comparison
- `key`: treated as strings for comparison
- `vector`, `rotation`: `==` and `!=` only (component-wise equality); no `<`, `>` etc.
- `list`: `==` and `!=` compare **length only**, not contents

```lsl
[1, 2, 3] == [4, 5, 6]  // TRUE (both length 3) — does NOT compare values!
```

## Bitwise Operators

| Operator | Name | Example |
|----------|------|---------|
| `&` | Bitwise AND | `4 & 2` = 0; `4 & 4` = 4 |
| `\|` | Bitwise OR | `4 \| 2` = 6; `4 \| 4` = 4 |
| `^` | Bitwise XOR | `4 ^ 4` = 0; `4 ^ 2` = 6 |
| `~` | Bitwise NOT | `~0` = -1; `~1` = -2 |

All bitwise operators accept `integer` operands only and return `integer`.

Common use — checking and setting flag bits:

```lsl
integer flags = STATUS_PHYSICS | STATUS_ROTATE_X;
if (flags & STATUS_PHYSICS) { /* physics is on */ }
flags &= ~STATUS_ROTATE_X;  // clear the ROTATE_X bit
```

## Logical Operators

| Operator | Name | Result |
|----------|------|--------|
| `&&` | Logical AND | 1 if both non-zero, else 0 |
| `\|\|` | Logical OR | 1 if either non-zero, else 0 |
| `!` | Logical NOT | 1 if zero, else 0 |

Accept `integer` operands. **Both operands are always evaluated** (no short-circuit).

`&&` and `||` have equal precedence in LSL (unlike C/Java where `&&` > `||`).

## Assignment Operators

| Shorthand | Equivalent |
|-----------|-----------|
| `a += b` | `a = a + b` |
| `a -= b` | `a = a - b` |
| `a *= b` | `a = a * b` |
| `a /= b` | `a = a / b` |
| `a %= b` | `a = a % b` |

Assignment operators work on any type that supports the corresponding binary operator.

## Typecast Operator

`(type)expression` — converts the value of expression to the specified type.

```lsl
string s = (string)42;              // "42"
integer i = (integer)3.7;           // 3 (truncated, not rounded)
float f = (float)"3.14";            // 3.14
key k = (key)"00000000-...";
string vs = (string)<1.0,2.0,3.0>; // "<1.000000, 2.000000, 3.000000>"

// Cast list to string (concatenates all elements):
string msg = (string)["Value: ", 42, " weight: ", 1.5];
// = "Value: 42 weight: 1.500000"
```

## De Morgan's Laws

### Bitwise

| AND form | Equivalent OR form |
|----------|--------------------|
| `~(a & b)` | `~a \| ~b` |
| `~a & ~b` | `~(a \| b)` |
| `a & ~b` | `~(~a \| b)` |
| `~(a & ~b)` | `~a \| b` |

### Boolean (logical)

| AND form | Equivalent OR form |
|----------|--------------------|
| `!(a && b)` | `!a \|\| !b` |
| `!a && !b` | `!(a \|\| b)` |
| `a && !b` | `!(!a \|\| b)` |
| `!(a && !b)` | `!a \|\| b` |

Each row's AND and OR forms are logically equivalent. `a` and `b` may be any expressions.
