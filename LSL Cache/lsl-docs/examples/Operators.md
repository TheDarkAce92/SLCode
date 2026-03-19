---
name: "Operators"
category: "example"
type: "example"
language: "LSL"
description: "Operators are used to cause an operation (or mathematical action) to be performed on one (such as !) or two operands. The easy and common example is 1 + 2 where 1 and 2 are operands, and the + is the operator. This concept can be extended much further with LSL since operands can be variables with the special case of the assignment operators requiring that the left hand side be a variable."
wiki_url: "https://wiki.secondlife.com/wiki/LSL_Operators"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL

Operators are used to cause an operation (or mathematical action) to be performed on one (such as !) or two operands. The easy and common example is 1 + 2 where 1 and 2 are operands, and the **+** is the operator. This concept can be extended much further with LSL since operands can be variables with the special case of the assignment operators requiring that the left hand side be a variable.

The following table lists the operators in descending order of evaluation, i.e. higher in the table means higher evaluation precedence. Multiple operators on the same line share evaluation precedence. Parenthesize an expression if you need to force an evaluation order.

Operator

Description

Usage Example

`()`

parentheses: grouping and evaluation precedence

`integer val = a * (b + c);`

`[]`

brackets: list constructor

`list lst = [a, 2, "this", 0.01];`

`(type)`

typecasting

`string message = "The result is:" + (string)result;`

`!` `~` `++` `--`

logical NOT, bitwise NOT, increment, decrement

`counter++;`

`*` `/` `%`

multiply/dot product, divide, modulus/cross product

`integer rollover = (count + 1) % 5;`

`-`

subtraction, negation

`integer one = 3 - 2;`

`integer neg_one = -1;`

`+`

addition, string concatenation

`integer two = 1 + 1;`

`string text = "Hello" + " world";`

`+`

list concatenation

`list myList = [1, 2, 3] + [4, 5];`

`list newList = oldList + addList;`

`<<` `>>`

 arithmetic left shift,  arithmetic right shift `integer eight = 4 << 1;` `integer neg_one = -2 >> 1;` `<` `<=` `>` `>=` less than, less than or equal to, greater than, greater than or equal to `integer isFalse = (6 <= 4);` `==` `!=` comparison: equal, not equal `integer isFalse = ("this" == "that");` `&` bitwise AND `integer zero = 4 & 2;` `integer four = 4 & 4;` `^` bitwise XOR `integer zero = 4 ^ 4;` `integer six = 4 ^ 2;` `|` bitwise OR `integer four = 4 | 4;` `integer six = 4 | 2;` `&&` `||` logical AND, logical OR `integer isFalse = (FALSE && TRUE);` `integer isTrue = (FALSE || TRUE);` `=` `+=` `-=` `*=` `/=` `%=` assignment `integer four = 4;` `integer eight = four; eight *= 2;` **Note:** Unlike most other languages that use the C-style `&&` and `||` operators, **both** operands are **always** evaluated. For example, ```lsl if (TRUE || 1/0) llSay(PUBLIC_CHANNEL, "Aha!"); ``` will cause a Math Error rather than say "Aha!" **Note:** The `++` (increment) and `--` (decrement) operators have two versions, pre- and post-. The pre-increment (or *pre*-decrement) operator increments (or decrements) its operand by 1; the value of the expression is the incremented (or decremented) value. The *post*-increment (or *post*-decrement) operator increases (or decreases) the value of its operand by 1, but the value of the expression is the operand's original value *prior* to the operation. ```lsl integer count = 0; if( ++count == 1 ) // 'count' is incremented then evaluated. llSay(PUBLIC_CHANNEL, "Aha"); // message will be said. ``` ```lsl integer count = 0; if( count++ == 1 ) // 'count' is evaluated then incremented. llSay(PUBLIC_CHANNEL, "Aha"); // message will not be said. ``` **Note:** In most programming languages, and in the LSL bitwise operators, the AND operator has greater precedence than the OR operator. However, the LSL logical operators || and && have *the same* precedence. For example: ```lsl 1 || 1 && 0 // result: 0 because it's the same as (1 || 1) && 0 ``` ```lsl 1 | 1 & 0 // result: 1 because it's the same as 1 | (1 & 0) ``` **Note:** The order of evaluation is from right to left. If the value of x starts as 1 then the first two conditions below evaluate false and the second two evaluate true: ```lsl (x && (x = 0) == 0 && x) ``` ```lsl (x && (x = 0) == 0 && x == 0) ``` ```lsl (x == 0 && (x = 0) == 0) ``` ```lsl (x == 0 && (x = 0) == 0 && x) ``` Both sides are evaluated regardless of the the truth of either side. - 1 % Modulus - 2 + Operator - 3 Shorthand Operators - 4 De Morgan's laws - 5 Useful Snippets ## % Modulus **Note:** Modulus (`%`), like division, cause a *Script run-time error. Math Error* when its second operand equals zero. **Note:** The `%` operator only accepts integer (`%` as modulus) and vector (`%` as cross product) operands. The modulus, also known as [Modulo](https://en.wikipedia.org/wiki/Modulo), produces the remainder after the first operand is divided by the second. Mathematically `a % b` is equivalent to `a - (a/b) * b`, since integer division `a/b` is truncated. This is also why the second operand cannot be zero.

The operator can be confusing, even to veteran scripters. The following example(s) may prove useful in understanding how modulus can be used:

- Determine if an integer ***input*** is even or odd:

```lsl
if (input % 2 == 0) // input is even
{
    // do even things
}
else // it's odd
{
    // do odd things
}
```

- In the LSL implementation, the result always has the same sign as the first operand.

  - -7 divided by 3 is -2 with a remainder of -1 (3 * -2 = -6, so the difference is -7 - -6 = -7 + 6 = -1), `-7 % 3 == -1`.
  - Conversely, 7 divided by -3 is -2 with a remainder of 1 (-3 * -2 = 6, so the difference is 7 - 6 = 1), `7 % -3 == 1`.
- If the second operand is known to be a positive power of two, the modulus `a % b` can be replaced with the bitwise AND operator `a & (b-1)` which is more efficient.

  - `7 % 4` and `7 & 3` are both 3.
  - However, AND always returns a positive value: `-7 % 4 == -3`, but `-7 & 3 == 1`, which is 4 greater than the modulus putting it in the positive. This may or may not be desirable depending on the situation.
- Sometimes taking a modulus of floating point numbers is useful. The formula from the introduction works as long as the quotient is cast to an integer: `a - (integer)(a/b) * b`.

  - Take the fractional part of `a` (`b` is 1.0 and can be left out): `7.8813 - (integer)(7.8813) == 0.8813`.
  - Limit an angle `a` within TWO_PI radians, i.e. a full circle: `7.8813 - (integer)(7.8813/TWO_PI) * TWO_PI == 1.598114`.

## + Operator

**Note:** Equality test on lists does not compare contents, only the length.

`result = left + right`

Left Type

Right Type

Result Type

Description

integer

integer

integer

Adds **left** and **right**

integer

float

float

Adds **left** and **right**

float

integer

float

Adds **left** and **right**

string

string

string

Concatenates **right** onto the end of **left**.

list

*

list

Concatenates **right** onto the end of **left**.

*

list

list

Affixes **left** onto the start of **right**.

vector

vector

vector

Adds **left** and **right**

rotation

rotation

rotation

Adds **left** and **right**Not useful for combining rotations, use * or / instead. ## Shorthand Operators Alternatives to the simple '=' operator... Simple assignment operator Shorthand operator a = a + 1 a += 1 a = a – 1 a -= 1 a = a * (n+1) a *= (n+1) a = a / (n+1) a /= (n+1) a = a % b a %= b ## Bitwise Equivalencies AND OR `~(a & b)` `~a | ~b` `~a & ~b` `~(a | b)` `a & ~b` `~(~a | b)` `~(a & ~b)` `~a | b` Boolean Equivalencies AND OR `!(a && b)` `!a || !b` `!a && !b` `!(a || b)` `a && !b` `!(!a || b)` `!(a && !b)` `!a || b` Due to  De Morgan's laws, by row, code in the AND column is logically equivalent to code in the **OR**. **a** and **b** need not be variables, they can be expressions. In certain circumstances these equivalencies can be used to simplify complex code. It is important not to confuse the two sets when using them. The first two rows depict De Morgan's laws as it is formulated, the second two build upon it.

## Useful Snippets

Typecasting can also be used if you have to concatenate many parts into a string:

```lsl
// the following twp statements are equivalent:
string message1 = (string)["I have ", 5, " children at the average age of ", 8.2, " years"];
string message2 = "I have 5 children at the average age of 8.200000 years";
```