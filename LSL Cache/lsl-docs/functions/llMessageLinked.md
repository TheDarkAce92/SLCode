---
name: "llMessageLinked"
category: "function"
type: "function"
language: "LSL"
description: "Sends a message to scripts in linked prims via the link_message event"
wiki_url: "https://wiki.secondlife.com/wiki/llMessageLinked"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "void llMessageLinked(integer link, integer num, string str, key id)"
parameters:
  - name: "link"
    type: "integer"
    description: "Link number or LINK_* constant specifying target prim(s)"
  - name: "num"
    type: "integer"
    description: "Integer value passed to the link_message event"
  - name: "str"
    type: "string"
    description: "String value passed to the link_message event"
  - name: "id"
    type: "key"
    description: "Key value passed to the link_message event"
return_type: "void"
energy_cost: "10.0"
sleep_time: "0.0"
patterns: ["llmessagelinked"]
deprecated: "false"
---

# llMessageLinked

```lsl
void llMessageLinked(integer link, integer num, string str, key id)
```

Sends a message to all scripts in the specified linked prim(s), triggering their `link_message` event. The primary mechanism for inter-script communication within a linked object.

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `link` | integer | Target link number or LINK_* constant |
| `num` | integer | Integer data payload |
| `str` | string | String data payload |
| `id` | key | Key data payload |

## Link Constants

| Constant | Value | Behaviour |
|----------|-------|-----------|
| `LINK_ROOT` | 1 | Root prim only |
| `LINK_SET` | -1 | All prims in the linkset |
| `LINK_ALL_OTHERS` | -2 | All prims except the sending prim |
| `LINK_ALL_CHILDREN` | -3 | All child prims (not root) |
| `LINK_THIS` | -4 | The prim containing this script |

## Caveats

- **Infinite loop risk:** A script receives its own messages if the `link` target includes its own prim. Always filter in the `link_message` handler.
- **Event queue:** The queue holds 64 events per script. If full, incoming messages are silently dropped.
- **Large payloads:** Oversized `str`/`id` can cause Stack-Heap Collision in the receiving script.
- **State changes:** State changes in the receiving script clear pending queued `link_message` events.
- `str` and `id` sizes are limited only by available script memory.

## Examples

```lsl
// Sender script
default
{
    touch_start(integer n)
    {
        llMessageLinked(LINK_ALL_OTHERS, 1, "activate", NULL_KEY);
    }
}
```

```lsl
// Receiver script
default
{
    link_message(integer sender_num, integer num, string str, key id)
    {
        if (num == 1 && str == "activate")
            llOwnerSay("Activated by link " + (string)sender_num);
    }
}
```

## See Also

- `link_message` event — triggered in target scripts
- `llGetLinkNumber` — get current prim's link number
- `llGetNumberOfPrims` — count prims in linkset


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llMessageLinked) — scraped 2026-03-18_

The purpose of this function is to allow scripts in the same object to communicate. It triggers a link_message event with the same parameters num, str, and id in all scripts in the prim(s) described by link.

## Caveats

- A script can hear its own linked messages if link targets the prim it is in. This creates the possibility of an infinite loop (a bad thing); be very careful about how messages are handled and passed along.
- Messages sent via llMessageLinked to a script that is sleeping, delayed, or lagged, are queued until the end of the delay. The event queue can hold 64 events.

  - If an event is received and the queue is full the event is silently dropped.
  - Avoid sending link_messages to large numbers of scripts simultaneously as it can cause lag spike. This most often happens when using the multi-prim `LINK_*` flags and can cause script execution to slow or halts.
  - Avoid sending link_messages to a target faster than they can be handled. Doing so risks filling the event queue and subsequent messages being silently discarded.
- When a script state changes, all pending events are deleted, including queued link_messages.
- If link is an invalid link number then the function silently fails.
- If str & id exceed the available memory of a script that catches the resulting link_message event, that script will crash with a Stack-Heap Collision.

## Examples

```lsl
default
{
    // assumptions  // object name: LSLWiki // script name: _lslwiki
    state_entry()
    {
        llMessageLinked(LINK_THIS, 0, llGetScriptName(), "");
    }

    link_message(integer sender_num, integer num, string msg, key id)
    {
        llOwnerSay(msg);
        // the owner of object LSLWiki will hear
        // LSLWiki:_lslwiki
    }
}
```

### Infinite Loop

```lsl
Message_Control(integer l, integer n) // Message_Total_Lack_Of_Control
{
    integer r = (++n); // Increment the value of n.
    llMessageLinked( l, r, "", ""); // Send the result to l
}

default
{
    state_entry()
    {
        Message_Control(LINK_SET, 0); // Tell all the scripts in the object that we have state_entered.
    }
    link_message(integer Sender, integer Number, string String, key Key) // This script is in the object too.
    {
        Message_Control(Sender, Number); // No filtering condition exists.
        llOwnerSay(((string)Number)); // Look at all the pretty numbers!
    }
}
```

## Notes

### Link Numbers

Each prim that makes up an object has an address, a link number. To access a specific prim in the object, the prim's link number must be known. In addition to prims having link numbers, avatars seated upon the object do as well.

- If an object consists of only one prim, and there are no avatars seated upon it, the (root) prim's link number is zero.
- However, if the object is made up of multiple prims or there is an avatar seated upon the object, the root prim's link number is one.

When an avatar sits on an object, it is added to the end of the link set and will have the largest link number. In addition to this, while an avatar is seated upon an object, the object is unable to link or unlink prims without unseating all avatars first.

#### Counting Prims & Avatars

There are two functions of interest when trying to find the number of prims and avatars on an object.

- `llGetNumberOfPrims()` - Returns the number of prims and seated avatars.
- `llGetObjectPrimCount(llGetKey())` - Returns only the number of prims in the object but will return zero for attachments.

```lsl
integer GetPrimCount() { //always returns only the number of prims
    if(llGetAttached())//Is it attached?
        return llGetNumberOfPrims();//returns avatars and prims but attachments can't be sat on.
    return llGetObjectPrimCount(llGetKey());//returns only prims but won't work on attachments.
}
```

See llGetNumberOfPrims for more about counting prims and avatars.

#### Errata

If a script located in a child prim erroneously attempts to access link 0, it will get or set the property of the linkset's root prim.  This bug ([BUG-5049](https://jira.secondlife.com/browse/BUG-5049)) is preserved for broken legacy scripts.

- Using llMessageLinked in a single prim object allows developers to mitigate some LSL limits by breaking up functionality between cooperating scripts and synchronizing actions. When you do this, be extremely careful not to create infinite loops as mentioned above.
- Estimated `.25` to `.50` delay between receiving and sending of llMessageLinked has been observed by some users
- Some users have noted occasional failures of linked messages when sending a message to a large number of receiving scripts in different prims using LINK_SET, LINK_ALL_OTHERS, & LINK_ALL_CHILDREN. If you encounter this problem, a workaround is to place all child prim scripts in a single prim, using targeted functions like llSetLinkPrimitiveParams to modify the prim in which the script previously resided. -- Void Singer
- This function seems to create a lower lag level then llListen since it does not need a listener.

## See Also

### Events

- link_message

### Functions

- **llGetLinkNumber** — prim

<!-- /wiki-source -->
