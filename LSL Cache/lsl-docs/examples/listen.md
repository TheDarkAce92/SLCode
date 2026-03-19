---
name: "listen"
category: "example"
type: "example"
language: "LSL"
description: "Sets a handle for msg on channel from name and id.Returns a handle (an integer) that can be used to deactivate or remove the listen."
wiki_url: "https://wiki.secondlife.com/wiki/LlListen"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL


ListenllListen

- 1 Summary
- 2 Specification
- 3 Caveats
- 4 Examples
- 5 Notes
- 6 See Also

  - 6.1 Events
  - 6.2 Functions
- 7 Deep Notes

  - 7.1 Footnotes
  - 7.2 Signature
  - 7.3 Haiku

## Summary

 Function: integer **llListen**( integer channel, string name, key id, string msg );

0.0

Forced Delay

10.0

Energy

Sets a [handle](http://foldoc.org/index.cgi?query=handle) for msg on channel from name and id.Returns a handle (an integer) that can be used to deactivate or remove the listen. • integer channel – input chat channel, any integer value (-2147483648 through 2147483647) • string name – filter for specific prim name or avatar legacy name • key id – filter for specific avatar or prim UUID • string msg – filter for specific message If msg, name or id are blank (i.e. `""`) they are not used to filter incoming messages. If id is an invalid key or assigned the value NULL_KEY, it is considered blank as well. ## Specification For the listen event to be triggered it must first match the criteria set forth by the filters; only when all the criteria have been met is a listen event generated. First the message must have been transmitted on channel. If id is both a valid key and not a null key, then the speaker's key must be equivalent[2] to id. If name is set, then the speaker's legacy name must match name exactly (case sensitive). If msg is set, then the spoken message must match msg exactly (case sensitive). Channel Constant Description DEBUG_CHANNEL 0x7FFFFFFF Chat channel reserved for script debugging and error messages, broadcasts to all nearby users. PUBLIC_CHANNEL 0x0 Chat channel that broadcasts to all nearby users. This channel is sometimes referred to as: open chat, local chat and public chat. ## Caveats - Messages sent on channel zero and DEBUG_CHANNEL are throttled to a rate of ## Examples Trivial example to listen to any chat from the object owner and respond once. Single listen handle

```lsl
//  Says beep to owner the first-time owner says something in main chat
//  and then stops listening

integer listenHandle;

remove_listen_handle()
{
    llListenRemove(listenHandle);
}

default
{
    state_entry()
    {
//      Change the channel number to a positive integer
//      to listen for '/5 hello' style of chat.

//      target only the owner's chat on channel 0 (PUBLIC_CHANNEL)
        listenHandle = llListen(0, "", llGetOwner(), "");
    }

    listen(integer channel, string name, key id, string message)
    {
//      we filtered to only listen on channel 0
//      to the owner's chat in the llListen call above

        llOwnerSay("beep");

//      stop listening until script is reset
        remove_listen_handle();
    }

    on_rez(integer start_param)
    {
        llResetScript();
    }

    changed(integer change)
    {
        if (change & CHANGED_OWNER)
        {
            llResetScript();
        }
    }
}
```

**Two listen handles**

```lsl
//  Opens two listen handles upon touch_start and
//  stops listening whenever something heard passes either filter

integer listenHandle_a;
integer listenHandle_b;

remove_listen_handles()
{
    llListenRemove(listenHandle_a);
    llListenRemove(listenHandle_b);
}

default
{
    touch_start(integer num_detected)
    {
        key    id   = llDetectedKey(0);
        string name = llDetectedName(0);

        listenHandle_a = llListen(5, "", id, "");
        listenHandle_b = llListen(6, "", NULL_KEY, "");

        llSay(0, "Listening now to '" + name + "' on channel 5.");
        llSay(0, "Listening now to anybody/anything on channel 6.");
    }

    listen(integer channel, string name, key id, string message)
    {
        if (channel == 5)
            llSay(0, name + " said: '/5 " + message + "'");

        if (channel == 6)
            llSay(0, name + " said: '/6 " + message + "'");

        remove_listen_handles();
    }
}
```

## Notes

- Avoid channel zero (PUBLIC_CHANNEL) and set name or id where possible to avoid lag. `llListen(0, "", NULL_KEY,"")` can be laggy as it listens to all chat from everyone in chat range and so should be avoided.

- In November 2007, Kelly Linden offered [this explanation](https://lists.secondlife.com/pipermail/secondlifescripters/2007-November/001993.html) to help scripters plan listeners more efficiently:

1. Chat that is said gets added to a history.
1. A script that is running and has a listen event will ask the history for a chat message during its slice of run time.
1. When the script asks the history for a chat message the checks are done in this order:

  - channel
  - self chat (prims can't hear themselves)
  - distance/RegionSay
  - id
  - name
  - msg
1. If a msg is found then a listen event is added to the event queue.

The id/name/msg checks only happen at all if those are specified of course.

So, the most efficient communication method is llRegionSay on a rarely used channel.
Nowadays, llRegionSayTo is to be preferred, where appropriate.

- The integer returned can be assigned to a variable (then called a handle) and used to control the listen via llListenRemove or llListenControl. These handles are assigned sequentially starting at +1 through to +2,147,483,647, going beyond which, according to Simon Linden, will roll the returned integer over to −2,147,483,648, when positive incrementation resumes. If an llListen is repeated with the exact same filters as a currently active listener, then the same handle number is returned. If an llListen's filters do not match any currently active listener, then the next handle in sequence is allocated (it will not re-allocate a recently removed handle).
- If you are using multiple listens in one script, each listen can be assigned its own handle with which to control it.
- Scripts can listen to and speak on DEBUG_CHANNEL. Script errors generated by the server are broadcast the same distance as llSay, but any chat command can be used to speak on DEBUG_CHANNEL.

  - Messages received on DEBUG_CHANNEL in the viewer are hidden unless the message is sent by an object owned by the current user.
  - Users may just see script errors as the hovering 'script error' icon depending on their viewer settings, and in any case will be able to read errors regardless of whether they are errors thrown by the scripting engine or your own debugging messages.

## See Also

### Events

•

listen

### Functions

•

llListenRemove

–

Removes a listen

•

llListenControl

–

Enables/Disables a listen

•

llWhisper

–

Sends chat limited to 10 meters

•

llSay

–

Sends chat limited to 20 meters

•

llShout

–

Sends chat limited to 100 meters

•

llRegionSay

–

Sends chat limited current sim

•

llRegionSayTo

–

Sends chat region wide to a specific avatar, or their attachments, or to a rezzed object of known UUID

## Deep Notes

#### Footnotes

1. **^** Channel zero is also known as: PUBLIC_CHANNEL, open chat, local chat and public chat
1. **^** In general terms this means the matching for id is not case sensitive. See key#equivalency for details on key equivalency.

#### Signature

```lsl
function integer llListen( integer channel, string name, key id, string msg );
```

#### Haiku

Choose not much to say


Someone might overhear it


Blab no big secrets