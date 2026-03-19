---
name: "llMessageLinked"
category: "example"
type: "example"
language: "LSL"
description: "The purpose of this function is to allow scripts in the same object to communicate. It triggers a link_message event with the same parameters num, str, and id in all scripts in the prim(s) described by link."
wiki_url: "https://wiki.secondlife.com/wiki/LlMessageLinked"
author: "precise link number"
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL


MessageLinkedllMessageLinked

- 1 Summary
- 2 Caveats
- 3 Examples

  - 3.1 Infinite Loop
- 4 Useful Snippets
- 5 Notes

  - 5.1 Link Numbers

  - 5.1.1 Counting Prims & Avatars
  - 5.1.2 Errata
- 6 See Also

  - 6.1 Events
  - 6.2 Functions
- 7 Deep Notes

  - 7.1 Footnotes
  - 7.2 Signature

## Summary

 Function:  **llMessageLinked**( integer link, integer num, string str, key id );

0.0

Forced Delay

10.0

Energy

The purpose of this function is to allow scripts in the same object to communicate. It triggers a link_message event with the same parameters num, str, and id in all scripts in the prim(s) described by link.

• integer

link

–

Link number (0: unlinked, 1: root prim, >1: child prims and seated avatars) or a `LINK_*` flag, controls which prim(s) receive the link_message.

• integer

num

–

Value of the second parameter of the resulting link_message event.

• string

str

–

Value of the third parameter of the resulting link_message event.

• key

id

–

Value of the fourth parameter of the resulting link_message event.

You can use id as a second string field. The sizes of str and id are only limited by available script memory.

Flag

Description

LINK_ROOT

1

sends to the root prim in a multi-prim linked set

LINK_SET

-1

sends to all prims

LINK_ALL_OTHERS

-2

sends to all other prims

Flag

Description

LINK_ALL_CHILDREN

-3

sends to all children, (everything but the root)

LINK_THIS

-4

sends to the prim the script is in

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

## Useful Snippets

```lsl
default
{
    // Quick and dirty debugging link_messages
    link_message(integer sender_num, integer num, string msg, key id)
    {
        llSay(DEBUG_CHANNEL, llList2CSV([sender_num, num, msg, id]));
    }
}
```

```lsl
// This is just an example script, you shouldn't handle link message within single script this way.

default
{
    // To propagate an unlimted number of arguments of any type.
    // Presumed, the separator string isn't used in any source string!
    state_entry()
    {
        list my_list = [1, 2.0, "a string", <1, 2, 3>, <1, 2, 3, 4>, llGetOwner()];
        string list_parameter = llDumpList2String(my_list, "|");    // Convert the list to a string
        llMessageLinked(LINK_THIS, 0, list_parameter, "");
    }

    link_message(integer sender_num, integer num, string list_argument, key id)
    {
        list re_list = llParseString2List(list_argument, ["|"], []);    // Parse the string back to a list
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

•

link_message

### Functions

•

llGetLinkNumber

–

Returns the link number of the prim the script is in.

## Deep Notes

#### Footnotes

1. **^** LINK_ROOT does not work on single prim objects. Unless there is an avatar sitting on the object.
1. **^** In LSL the key type is implemented as a string (but with different operators and restrictions). Typecasting between string and key types has no effect on the data contained.
1. **^** There are four ways for a script to target itself: by precise link number, LINK_THIS, LINK_SET and LINK_ALL_CHILDREN (if the prim is a child prim).

#### Signature

```lsl
function void llMessageLinked( integer link, integer num, string str, key id );
```