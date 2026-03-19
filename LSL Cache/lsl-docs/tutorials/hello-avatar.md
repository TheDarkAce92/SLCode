---
name: "Hello Avatar"
category: "tutorial"
type: "reference"
language: "LSL"
description: "The default LSL script template — the Hello World of Second Life scripting"
wiki_url: "https://wiki.secondlife.com/wiki/Hello_Avatar"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
---

# Hello Avatar

The default script placed in every new Second Life script. The LSL equivalent of "Hello World".

## The Script

```lsl
default
{
    state_entry()
    {
        llSay(0, "Hello, Avatar!");
    }

    touch_start(integer total_number)
    {
        llSay(0, "Touched.");
    }
}
```

## What It Does

- **`state_entry()`** — fires when the script is saved, reset, or when the object is rezzed without saved script state. Outputs "Hello, Avatar!" to public chat.
- **`touch_start(integer total_number)`** — fires when an avatar clicks the object. Outputs "Touched." to public chat.

## Best Practices for Beginners

1. Use `llOwnerSay` instead of `llSay(0, ...)` to avoid spamming nearby avatars with test output.
2. Use `llInstantMessage(llGetOwner(), "msg")` for private messages that work even when the owner is not nearby.

```lsl
// Better version
default
{
    state_entry()
    {
        llOwnerSay("Script started!");
    }

    touch_start(integer total_number)
    {
        llOwnerSay("Touched by: " + llDetectedName(0));
    }
}
```
