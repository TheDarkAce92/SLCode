---
name: "LSL Style Guide"
category: "style-guide"
type: "reference"
language: "LSL"
description: "LSL coding style conventions: indentation, naming, commenting, code organisation, and readability guidelines"
wiki_url: "https://wiki.secondlife.com/wiki/LSL_Style_Guide"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
---

# LSL Style Guide

## Indentation Styles

Two primary indentation styles are used in the LSL community. Both are acceptable — the key is **consistency**.

### K&R Style

Conserves vertical space. Opening brace on same line as construct.

```lsl
default {
    state_entry() {
        llSay(0, "Hello World.");
    }
}
```

### Allman Style

Easier to read and visually bracket-match. Opening brace on its own line.

```lsl
default
{
    state_entry()
    {
        llSay(0, "Hello World.");
    }
}
```

**Key principle:** "Consistent indenting makes reading both styles easier — that's why it really comes down to whatever works for you."

**Rules:**
- Use spaces (2–6, typically 4), never tabs.
- Style changes are inappropriate unless you are also making substantial code revisions.
- White-space edits should only fix inconsistencies, not change someone's chosen style.

---

## Naming Conventions

### Global Variables

Lowercase with underscores, or camelCase:

```lsl
integer index = 0;
string name = "Please set one";
```

Alternative: prefix with `g` to clearly distinguish globals from locals:

```lsl
integer gIndex;
string gName = "Please set one";
```

### Constants (User-Defined)

All uppercase, following Linden Labs convention:

```lsl
integer DIALOG_CHANNEL = -517265;
vector RED = <1.0, 0.0, 0.0>;
```

### Functions

camelCase (matching built-in `ll` function style), or lowercase with underscores:

```lsl
integer getNumberOfItems()
{
    return llGetInventoryNumber(INVENTORY_ALL);
}
```

### Event Parameters

Use the standard names as documented in the official wiki. This makes code immediately recognisable to other LSL developers:

```lsl
listen(integer channel, string name, key id, string message)
{
    key ownerKey = llGetOwner();
    if (channel == 1 && id == ownerKey)
        llOwnerSay("Hello Avatar");
}
```

---

## Code Separation Guidelines

Avoid cramming multiple nested function calls onto a single line. Readable intermediate variables are preferred.

**Hard to read:**

```lsl
string name = llToLower(llGetSubString(llList2String(
    llParseString2List(llDetectedName(0), [" "], []), 0),
    0, NUM_DIGITS - 1));
```

**Readable:**

```lsl
string detectedName = llDetectedName(0);
list nameParts = llParseString2List(detectedName, [" "], []);
string firstName = llList2String(nameParts, 0);
string lowerFirst = llToLower(llGetSubString(firstName, 0, NUM_DIGITS - 1));

integer index = llListFindList(listOfStrings, [lowerFirst]);
if (index == -1)
    listOfStrings += lowerFirst;
```

**Note:** "Line combination optimization should only be done after the code is working and bug-free."

---

## Script Structure

LSL mandates this order:

1. User-defined global variables
2. User-defined functions
3. `default` state (required; must contain at least one event handler)
4. User-defined states (each must contain at least one event handler)

```lsl
// 1. Global variables
integer gCount = 0;
string gName = "Widget";

// 2. User-defined functions
integer increment(integer val)
{
    return val + 1;
}

// 3. Default state (required)
default
{
    state_entry()
    {
        gCount = increment(gCount);
        llOwnerSay("Count: " + (string)gCount);
    }
}

// 4. Additional states
state running
{
    state_entry()
    {
        llOwnerSay("Running");
    }
}
```

---

## Commenting Guidelines

Use comments to explain *why*, not *what*:

```lsl
// BAD: explains what the code obviously does
integer i = 0; // set i to zero

// GOOD: explains why a non-obvious value is used
integer CHANNEL = -982437;  // Unique channel — avoid collisions with other objects
```

Function headers should document parameters and return values:

```lsl
// Returns the link number of the prim with the given name,
// or -1 if no prim with that name exists in the linkset.
integer getLinkByName(string name)
{
    // ...
}
```

---

## Acceptable Formats for the LSL Portal

When contributing code examples to the Second Life wiki:

- Use K&R or Allman style consistently.
- Use spaces (2–6, typically 4), never tabs.
- White-space-only edits should only fix inconsistencies.
- Do not change a contributor's chosen style unless making substantial code revisions.

---

## Memory and Performance Style Notes

- Declare variables in the narrowest scope possible — globals persist in memory for the script's lifetime.
- Prefer `integer` over `float` when integer arithmetic suffices.
- Avoid calling `llGetListLength()` repeatedly in a loop — cache the result.
- Use `llSetLinkPrimitiveParamsFast` instead of `llSetLinkPrimitiveParams` when the delay is not needed.
- Profile with `llGetUsedMemory()` and `llGetMemoryLimit()` during development.
