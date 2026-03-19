---
name: "A Basic LSL Tutorial"
category: "tutorial"
type: "reference"
language: "LSL"
description: "10-task beginner tutorial covering chat, colors, floating text, transparency, textures, conditionals, listeners, movement, and physics"
wiki_url: "https://wiki.secondlife.com/wiki/A_Basic_LSL_Tutorial"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
---

# A Basic LSL Tutorial

This tutorial covers 10 practical tasks for beginners, building from basic output to physics control.

## Basic Script Structure

Every LSL script needs at minimum a `default` state with at least one event handler:

```lsl
default
{
    state_entry()
    {
        llSay(0, "Hello, Avatar!");
    }

    touch_start(integer num_detected)
    {
        llSay(0, "Touched.");
    }
}
```

- `state_entry()` — fires when the script is saved, reset, or when the object is rezzed without saved script state
- `touch_start()` — fires when an avatar clicks the prim

## Data Types

| Type | Description | Example |
|------|-------------|---------|
| `string` | Text in quotation marks | `"Hello Bill"` |
| `integer` | Whole number | `42` |
| `float` | Decimal number | `1.23456` |
| `vector` | Three floats `<x, y, z>` | `<1.0, 0.0, 0.0>` |
| `key` | UUID identifier | `"j4m3s000-..."` |

`TRUE` = 1, `FALSE` = 0.

---

## Task 1 — Chat Output

```lsl
llSay(PUBLIC_CHANNEL, "Hello, Avatar!");   // 20m range
llShout(PUBLIC_CHANNEL, "SHOUT!");          // 100m range
llWhisper(PUBLIC_CHANNEL, "WHISPER");       // 10m range
llOwnerSay("Owner only");                   // Owner must be in same region
llRegionSay(25, "Region-wide");             // Region, non-zero channel
```

---

## Task 2 — Comments

```lsl
default
{
    // Fires when script is saved or reset (default state only)
    state_entry()
    {
        llSay(0, "Hello, Avatar!");
    }

    // Fires when an avatar starts touching the prim
    touch_start(integer num_detected)
    {
        llSay(0, "Touched.");
    }
}
```

---

## Task 3 — Change Object Colour

```lsl
default
{
    touch_start(integer num_detected)
    {
        llSetColor(<1.0, 0.0, 0.0>, ALL_SIDES);  // Red
    }
}
```

Colour vectors: Red `<1,0,0>`, Green `<0,1,0>`, Blue `<0,0,1>`, White `<1,1,1>`, Black `<0,0,0>`.

---

## Task 4 — Floating Text

```lsl
default
{
    touch_start(integer num_detected)
    {
        llSetText("Nice to meet you!", <0.0, 1.0, 0.0>, 1.0);
        // Parameters: text, colour vector, alpha (0=transparent, 1=opaque)
    }
}
```

---

## Task 5 — Transparency

```lsl
default
{
    touch_start(integer num_detected)
    {
        llSetAlpha(0.0, ALL_SIDES);  // Fully transparent
        // 0.0 = invisible, 0.5 = half transparent, 1.0 = opaque
    }
}
```

---

## Task 6 — Apply Textures

```lsl
default
{
    touch_start(integer num_detected)
    {
        // By name (texture must be in prim's inventory)
        llSetTexture("MyTexture", ALL_SIDES);

        // By UUID
        llSetTexture("j4m3s000-0000-0000-0000-b3n3d3k00000", ALL_SIDES);
    }
}
```

---

## Task 7 — Owner Detection

```lsl
default
{
    touch_start(integer num_detected)
    {
        key owner = llGetOwner();
        key toucher = llDetectedKey(0);

        if (owner == toucher)
            llSay(0, "Touched by owner.");
        else
            llSay(0, "Touched by someone else.");
    }
}
```

---

## Task 8 — Listen for Chat Commands

```lsl
default
{
    state_entry()
    {
        // Listen on channel 99 (type /99 hello in chat)
        llListen(99, "", llGetOwner(), "");
    }

    listen(integer channel, string name, key id, string message)
    {
        if (message == "hello")
            llOwnerSay("Hello to you too!");
        else
            llOwnerSay("Unknown command: " + message);
    }
}
```

---

## Task 9 — Movement

```lsl
default
{
    touch_start(integer num_detected)
    {
        vector oldPos = llGetPos();
        llSetPos(oldPos + <0.0, 0.0, 1.0>);  // Move up 1 metre
    }
}
```

---

## Task 10 — Physics

```lsl
default
{
    state_entry()
    {
        llSetStatus(STATUS_PHYSICS, TRUE);   // Enable physics
    }

    touch_start(integer num_detected)
    {
        llSetStatus(STATUS_PHYSICS, FALSE);  // Disable physics
    }
}
```

Status constants: `STATUS_PHYSICS` (1), `STATUS_PHANTOM` (16), `STATUS_ROTATE_X` (2), `STATUS_ROTATE_Y` (4), `STATUS_ROTATE_Z` (8).
