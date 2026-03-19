---
name: "LSL Flow Control"
category: "flow-control"
type: "reference"
language: "LSL"
description: "All LSL flow control constructs: if/else, while, do-while, for, jump/label, return, and state changes"
wiki_url: "https://wiki.secondlife.com/wiki/LSL_Flow_Control"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
---

# LSL Flow Control

LSL supports the following flow control constructs: `if`/`else`, `while`, `do...while`, `for`, `jump`/`@label`, `return`, and `state` changes.

---

## if / else

### Syntax

```lsl
if (condition) statement
if (condition) statement else statement
```

### Condition Truth Values

| Type | Evaluates True When |
|------|-------------------|
| `integer` | Not zero |
| `float` | Not zero |
| `string` | Length is not zero |
| `key` | Is a valid UUID and not NULL_KEY |
| `vector` | Not ZERO_VECTOR (`<0,0,0>`) |
| `rotation` | Not ZERO_ROTATION (`<0,0,0,1>`) |
| `list` | Length is not zero (Mono only; LSO has a bug — see Caveats) |

### Examples

```lsl
// Simple if
if (a == 1) c = b;

// If with block
if (a == 1)
{
    llSay(0, "a is one");
}

// If-else
if (a == 1)
{
    llSay(0, "one");
}
else
{
    llSay(0, "not one");
}

// Else-if chain (no practical limit on chain length)
if (a == "Loren")
{
    llSay(0, "Lorem ipsum!");
}
else if (a == "Bob")
{
    llSay(0, "Babble dabble!");
}
else
{
    llSay(0, "Unknown");
}

// Nested
if (a == 1)
{
    if (b == c)
    {
        // both conditions met
    }
}
```

### Caveats

- **No short-circuit evaluation.** Both sides of `&&` and `||` are always evaluated. `if (x != 0 && 1/x > 2)` will cause a Math Error when `x == 0`.
- **Semicolon trap.** A semicolon after `if (condition)` creates a null statement — the block below always runs:
  ```lsl
  if (a == "Loren");   // semicolon ends the if — WRONG
  {
      llSay(0, "This runs always!");  // not conditional
  }
  ```
- **Missing braces.** Without braces, only the immediately following statement is in scope:
  ```lsl
  if (a == "Loren")
      llSay(0, "First");    // conditional
      llSay(0, "Second");   // always runs — WRONG
  ```
- **Assignment vs comparison.** `if (a = 1)` assigns 1 to `a` and always evaluates true. Use `if (a == 1)`.
- **List bug in LSO:** in LSO-compiled scripts, `if (myList)` incorrectly evaluates non-empty lists as false (BUG-230728). Use `if (llGetListLength(myList) > 0)` for portability.

---

## while

### Syntax

```lsl
while (condition) loop
```

Evaluates `condition` before each iteration. Exits when condition is false.

### Examples

```lsl
// Single statement
integer a = 0;
integer b = 10;
while (a < b)
    llOwnerSay((string)(a++));

// Block statement
integer a = 0;
integer b = 10;
while (a < b)
{
    llOwnerSay((string)a);
    ++a;
}

// Null body (do work in condition expression)
integer a = 0;
integer b = 10;
while (a++ < b);
```

### Caveats

- Same condition truth table as `if` applies.
- LSO bug: non-empty lists evaluate as false in while conditions (BUG-230728).
- OpenSim LSL may require explicit zero checks for float conditions.

---

## do...while

### Syntax

```lsl
do loop while (condition);
```

Executes the loop body **first**, then evaluates the condition. The body always executes at least once.

```lsl
integer a = 0;
integer b = 10;
do
{
    llOwnerSay((string)a);
    ++a;
} while (a < b);
```

**Performance note:** In LSO-compiled scripts, `do...while` is faster than `while` or `for` because the jump is always at the bottom. In Mono, the difference is negligible.

---

## for

### Syntax

```lsl
for (initializer; condition; increment) loop
```

All three parts are optional. The condition is evaluated before each iteration; the increment runs after each iteration.

### Examples

```lsl
// Standard form
integer a;
integer b = 10;
for (a = 0; a < b; ++a)
{
    llOwnerSay((string)a);
}

// Single statement body
for (a = 0; a < b; ++a)
    llOwnerSay((string)a);

// Minimal form (not recommended)
for ( ; a < b; llOwnerSay((string)(++a)) );
```

### Equivalence to while

```lsl
// for loop:
for (init; condition; increment)
    body;

// Equivalent while loop:
init;
while (condition)
{
    body;
    increment;
}
```

### Caveats

- LSO list condition bug (BUG-230728) applies to `for` conditions as well.

---

## jump / @label

### Syntax

```lsl
jump target_name;
@target_name;
```

Transfers execution to the labeled location within the same function or event handler scope.

### Rules

- Labels must be in the same function/event scope as the `jump` statement.
- A label cannot be in a parent scope if the `jump` is in a child scope.
- Labels must be unique within a function/event scope.
- **LSO bug:** if multiple `jump` statements target the same label, only the first works as expected.
- Generally discouraged in favour of structured loops; useful for "break from nested loops" patterns.

### Examples

```lsl
// Simple forward jump (skip code)
integer a = 5;
jump over;
@in;
a = 6;
@over;
llOwnerSay((string)a);
if (a < 6) jump in;
// Outputs: "5" then "6"

// Break from nested loop (common practical use)
integer getLinkWithName(string name)
{
    integer i = llGetLinkNumber() != 0;
    integer x = llGetNumberOfPrims() + i;
    for (; i < x; ++i)
    {
        if (llGetLinkName(i) == name)
            jump break;
    }
    i = -1;
    @break;
    return i;
}
```

---

## return

### Syntax

```lsl
return;           // in void function or event
return expression; // in typed function
```

Exits the current function immediately. In a typed function, evaluates `expression` and returns its value to the caller.

```lsl
// Void function early exit
cleanUp()
{
    if (someCondition)
        return;  // exit early
    // ... more code
}

// Return value
integer max(integer a, integer b)
{
    if (a > b) return a;
    return b;
}
```

### Caveats

- In an event handler, `return` exits the event.
- Unreachable code after `return` causes a compiler error (except when reached via `jump`).
- A typed function must return a value on all code paths.

---

## state

### Syntax

```lsl
state state_name;
state default;
```

Changes the current script state. Triggers `state_exit` on the current state and `state_entry` on the new state.

### What Happens on a State Change

1. The `state` statement causes **immediate exit** from the current event handler — any code after it does NOT execute.
2. `state_exit` event fires in the current state (if defined).
3. All active listeners, sensors, and targets are **automatically cancelled**. The timer is NOT cancelled — it **persists** into the new state.
4. `state_entry` event fires in the new state.

```lsl
default
{
    state_entry()
    {
        llSay(0, "In default state");
        state active;  // transition to 'active' state
    }

    state_exit()
    {
        llSay(0, "Leaving default");
    }
}

state active
{
    state_entry()
    {
        llSay(0, "Now in active state");
    }
}
```

### Caveats

- `state default` transitions back to the default state.
- You cannot transition to the currently active state (it is silently ignored or may cause unexpected behaviour).
- Global variables retain their values across state changes; local variables do not.
- Pending events queued before a state change are **dropped** (cleared from the event queue).
- Timers, listeners (`llListen`), sensors (`llSensorRepeat`), and targets (`llTarget`, `llRotTarget`) are cancelled on state change.

---

## Null Statement

A lone semicolon `;` is a valid statement that does nothing:

```lsl
while (someCondition);  // busy-waits (usually wrong — ensure condition changes)
for (; condition; ++i); // body is null, work done in init/increment
```

---

## General Flow Control Notes

- LSL uses 32-bit integers for all integer conditions (truthy when non-zero).
- There is no `break` or `continue` keyword — use `jump` for early loop exit.
- There is no `switch` statement — use else-if chains or list-based dispatch.
- Event handlers cannot be called directly; they are only triggered by the runtime.
