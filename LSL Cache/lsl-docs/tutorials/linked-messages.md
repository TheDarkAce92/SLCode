---
name: "Linked Messages"
category: "tutorials"
type: "reference"
language: "LSL"
description: "Coordinating multiple scripts in a linkset using llMessageLinked and the link_message event, including the command-dispatcher pattern and common pitfalls"
wiki_url: ""
local_only: true
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
---

# Linked Messages

When an object is made up of multiple linked prims, each prim can contain scripts. `llMessageLinked` lets those scripts communicate with each other without using the public chat channel.

## How It Works

A script calls `llMessageLinked` to send a message. Any script that has a `link_message` event handler in a targeted prim will receive it.

```lsl
// Sender (in any script)
llMessageLinked(LINK_SET, 42, "hello", NULL_KEY);
```

```lsl
// Receiver (in any script in the linkset)
link_message(integer sender_num, integer num, string str, key id)
{
    llSay(0, "Got message " + (string)num + ": " + str);
}
```

## Link Target Constants

| Constant | Value | Targets |
|---|---|---|
| `LINK_SET` | -1 | Every prim in the linkset, including the sender |
| `LINK_ALL_OTHERS` | -2 | Every prim except the one containing the sending script |
| `LINK_ALL_CHILDREN` | -3 | All child prims (excludes the root prim) |
| `LINK_ROOT` | 1 | The root prim only |
| `LINK_THIS` | -4 | The prim containing the sending script only |

You can also pass an explicit link number (integer) to target a specific prim.

## The Command-Dispatcher Pattern

Use the `num` parameter as a command identifier. Define integer constants so the meaning is clear:

```lsl
// Shared constants (must be identical in all scripts that use them)
integer CMD_OPEN   = 100;
integer CMD_CLOSE  = 101;
integer CMD_STATUS = 102;

// Controller script (in root prim)
default
{
    touch_end(integer num_detected)
    {
        llMessageLinked(LINK_ALL_OTHERS, CMD_OPEN, "", NULL_KEY);
    }
}
```

```lsl
// Door script (in a child prim)
integer CMD_OPEN   = 100;
integer CMD_CLOSE  = 101;
integer CMD_STATUS = 102;

default
{
    link_message(integer sender_num, integer num, string str, key id)
    {
        if (num == CMD_OPEN)
        {
            llSay(0, "Opening door.");
        }
        else if (num == CMD_CLOSE)
        {
            llSay(0, "Closing door.");
        }
        else if (num == CMD_STATUS)
        {
            llMessageLinked(sender_num, CMD_STATUS, "open", NULL_KEY);
        }
    }
}
```

## Passing Data with the Message

All four parameters can carry data:

- `num` — an integer (use as command ID, flag, or small integer value)
- `str` — a string (use for text data, serialised lists, JSON, etc.)
- `id` — a key (use for UUIDs, or cast to/from string for a second string value)

To pass a list, serialise it first:

```lsl
// Sender
list data = ["alpha", "beta", "gamma"];
llMessageLinked(LINK_SET, 0, llList2CSV(data), NULL_KEY);

// Receiver
link_message(integer sender_num, integer num, string str, key id)
{
    list data = llCSV2List(str);
    llSay(0, "First item: " + llList2String(data, 0));
}
```

## Infinite Loop Warning

Scripts receive messages they send to `LINK_SET`. If a `link_message` handler sends another `llMessageLinked(LINK_SET, ...)`, and that triggers another `link_message` in the same script, you will create an infinite loop that crashes the script.

```lsl
// DANGER — infinite loop
link_message(integer sender_num, integer num, string str, key id)
{
    llMessageLinked(LINK_SET, num, str, id);  // sends to self — loops forever
}
```

Use `LINK_ALL_OTHERS` when you want to broadcast without triggering your own handler, or guard with a check on `sender_num`.

## Event Queue Limit

Each script has an event queue of **64 events**. If a controller sends messages faster than the receiver processes them, events will be dropped. Avoid flooding the channel in tight loops.

## `sender_num` in `link_message`

`sender_num` is always the link number of the prim containing the script that called `llMessageLinked`. It does not change based on which LINK constant was used to broadcast.

Use it with care when routing replies: if the prim contains multiple scripts, all of them share the same `sender_num`. Replying to `sender_num` sends to the prim, and every script in that prim with a `link_message` handler will receive the reply.

## Caveats

- `llMessageLinked` has **no sleep** and is fast — do not flood it in a tight loop.
- There is no delivery confirmation. Messages are silently dropped if the receiving script's event queue is full, if the receiving script is not running, or if no script in the targeted prim has a `link_message` handler in its current state.
- `link_message` does not fire if the receiving script is in a state that does not define the event.
- If the payload (num + str + id combined) is too large, the receiving script can crash.
- Sending `llMessageLinked` from within `link_message` targeting `LINK_SET` will trigger your own handler again.
