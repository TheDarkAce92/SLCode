---
name: "link_message"
category: "event"
type: "event"
language: "LSL"
description: "Fires when a script in a linked prim calls llMessageLinked targeting this prim"
wiki_url: "https://wiki.secondlife.com/wiki/Link_message"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "link_message(integer sender_num, integer num, string str, key id)"
parameters:
  - name: "sender_num"
    type: "integer"
    description: "Link number of the prim whose script called llMessageLinked"
  - name: "num"
    type: "integer"
    description: "Integer data payload from llMessageLinked"
  - name: "str"
    type: "string"
    description: "String data payload from llMessageLinked"
  - name: "id"
    type: "key"
    description: "Key data payload from llMessageLinked (also used as a second string)"
deprecated: "false"
---

# link_message

```lsl
link_message(integer sender_num, integer num, string str, key id)
{
    // handle inter-script message
}
```

Fires when `llMessageLinked` targets this prim. Primary mechanism for inter-script communication within a linked object.

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `sender_num` | integer | Link number of the sending prim |
| `num` | integer | Integer payload |
| `str` | string | String payload |
| `id` | key | Key payload (often used as a second string) |

## Caveats

- **Self-hearing:** A script receives its own link messages if the target includes its prim. Compare `sender_num` to `llGetLinkNumber()` to detect this.
- **Queue limit:** 64 link_message events can queue per script. Excess events are silently dropped.
- **Large payloads:** Oversized `str` or `id` can cause Stack-Heap Collision crashes.
- **State changes:** Pending link_message events are cleared when the receiving script changes state.

## Examples

```lsl
// Command dispatcher pattern
default
{
    link_message(integer sender_num, integer num, string str, key id)
    {
        if (num == 1)       // command 1: activate
            llSetStatus(STATUS_PHYSICS, TRUE);
        else if (num == 2)  // command 2: deactivate
            llSetStatus(STATUS_PHYSICS, FALSE);
    }
}
```

```lsl
// Passing a list through str
default
{
    link_message(integer sender_num, integer num, string str, key id)
    {
        if (str == "") return;
        list data = llParseStringKeepNulls(str, ["|"], []);
        // use data[0], data[1], etc.
    }
}
```

## See Also

- `llMessageLinked` — send a link message
- `llGetLinkNumber` — get this prim's link number


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/link_message) — scraped 2026-03-18_

## Caveats

- 64 link_message events can queue, past that, they are silently dropped!  Don't do too much in the event if they might be coming in fast.
- sender_num does not reflect how a message was sent, there is no way to know if it was sent with a LINK_* flag or the specific link number.
- If str and id are bigger than available memory the script will crash with a Stack-Heap Collision.

## Examples

```lsl
// This is just an example script, you shouldn't handle touches within a single script this way.

default
{
    touch_start(integer num_detected)
    {
        llMessageLinked(LINK_THIS, 0, llDetectedName(0), llDetectedKey(0));
    }

    link_message(integer source, integer num, string str, key id)
    {
        llWhisper(0, str + " (" + (string)id + ") touched me!");
    }
}
```

## Notes

|  | Important: A script can hear its own link messages. |
| --- | --- |

- sender_num can be compared to llGetLinkNumber to determine whether the message was sent by the same prim, regardless of whether the prim is unlinked, a root, or a child.

## See Also

### Functions

- llMessageLinked

<!-- /wiki-source -->
