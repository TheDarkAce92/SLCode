---
name: "llListen"
category: "function"
type: "function"
language: "LSL"
description: "Registers a listener for chat messages on a channel, with optional filters for name, key, and message text"
wiki_url: "https://wiki.secondlife.com/wiki/llListen"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "integer llListen(integer channel, string name, key id, string msg)"
parameters:
  - name: "channel"
    type: "integer"
    description: "Chat channel to listen on (-2147483648 through 2147483647)"
  - name: "name"
    type: "string"
    description: "Filter: speaker legacy name. Empty string matches any name."
  - name: "id"
    type: "key"
    description: "Filter: speaker UUID. NULL_KEY matches any speaker."
  - name: "msg"
    type: "string"
    description: "Filter: exact message text. Empty string matches any message."
return_type: "integer"
energy_cost: "10.0"
sleep_time: "0.0"
patterns: ["lllisten"]
deprecated: "false"
---

# llListen

```lsl
integer llListen(integer channel, string name, key id, string msg)
```

Registers a listener that fires the `listen` event when a chat message matching all specified filters is received. Returns a handle used to manage the listener with `llListenRemove` and `llListenControl`.

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `channel` | integer | Channel to listen on |
| `name` | string | Speaker name filter (empty = any) |
| `id` | key | Speaker key filter (NULL_KEY = any) |
| `msg` | string | Message content filter (empty = any) |

## Return Value

`integer` — a listener handle. Pass to `llListenRemove` to remove the listener.

## Filter Behaviour

The `listen` event fires only when ALL non-empty filters match:

1. Message is on the specified `channel`
2. If `id` is not NULL_KEY: speaker's key matches `id`
3. If `name` is non-empty: speaker's legacy name matches exactly (case-sensitive)
4. If `msg` is non-empty: message text matches exactly (case-sensitive)

## Caveats

- **Listener limit:** Maximum 65 simultaneous active listeners per script. Exceeding this causes a "Too Many Listens" runtime error.
- **Listener removal:** State changes and script resets automatically remove all listeners. Call `llListenRemove` explicitly when a listener is no longer needed.
- **Channel 0 / DEBUG_CHANNEL throttle:** Messages are rate-limited to fewer than 200 per 10 seconds per region per owner.
- **Self-deafness:** A prim cannot hear its own `llSay` output. Linked prims can hear each other.
- **Message truncation:** Messages longer than 1024 bytes (scripts), 1023 bytes (positive channel chat), or 254 bytes (negative channel chat) are truncated.
- **Filter immutability:** Listener filters cannot be changed after registration — remove and re-register.
- **Owner changes:** Listeners set up using the previous owner's key continue with that stale key. Handle `CHANGED_OWNER` in the `changed` event and reset.
- **Channel 0 range:** Listens on channel 0 are limited to the `llSay` range (20m) unless using `llRegionSay`/`llShout`.

## Examples

```lsl
// Basic: listen for owner chat on channel 0
integer listenHandle;

default
{
    state_entry()
    {
        listenHandle = llListen(0, "", llGetOwner(), "");
    }

    listen(integer channel, string name, key id, string message)
    {
        llOwnerSay("You said: " + message);
        llListenRemove(listenHandle);
    }

    changed(integer change)
    {
        if (change & CHANGED_OWNER)
            llResetScript();
    }
}
```

```lsl
// Multiple listeners with cleanup
integer listenA;
integer listenB;

default
{
    touch_start(integer num_detected)
    {
        key toucher = llDetectedKey(0);
        listenA = llListen(5, "", toucher, "");
        listenB = llListen(6, "", NULL_KEY, "");
        llSetTimerEvent(60.0);  // timeout
    }

    listen(integer channel, string name, key id, string message)
    {
        llOwnerSay(name + " on ch " + (string)channel + ": " + message);
        llListenRemove(listenA);
        llListenRemove(listenB);
        llSetTimerEvent(0.0);
    }

    timer()
    {
        llListenRemove(listenA);
        llListenRemove(listenB);
        llSetTimerEvent(0.0);
    }
}
```

## See Also

- `llListenRemove` — remove a listener by handle
- `llListenControl` — enable or disable a listener
- `listen` event — triggered when a matching message is received
- `llSay`, `llWhisper`, `llShout`, `llRegionSay` — transmit chat
- `llDialog` — show dialog box (requires a listener on the same channel)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llListen) — scraped 2026-03-18_

Sets a handle for msg on channel from name and id.Returns a handle (an integer) that can be used to deactivate or remove the listen.

## Caveats

- Messages sent on channel zero and DEBUG_CHANNEL are throttled to a rate of <200/10sec, per region, per owner/user.

  - Once the rate is exceeded, all following messages on channel zero or DEBUG_CHANNEL will be dropped until the send rate is again below 200/10sec for the previous 10 sec. Dropped messages, despite being dropped still count against the limit.
- On state change or script reset all listens are removed automatically.

  - A state change can be used as a shortcut to releasing listens.
- Only 65 listens can simultaneously be open in any single script.

  - If this number is exceeded *Script run-time error* and *Too Many Listens* errors occur.
- For some time, the official SL viewer and several third-party viewers can use negative channels from the chat bar directly just as any other non-zero channel. Formerly, the standard SL viewer could only send chat on negative channels through llDialog or llTextBox responses, meaning negative channels were best suited for applications that did not require direct avatar chat.
- Be aware that if you mistakenly use an integer literal bigger than the maximum or smaller than the minimum, LSL will treat it as -1, *without* giving any compilation error. This means that all scripts listening to an out-of-range integer will be listening to channel -1 instead, or if the number has a minus sign in front, to channel 1. A safe rule is to never use more than 9 digits. If the channel number comes from a conversion from float (for example from llFrand), if the float is out of range for an integer, it will be converted to the number -2147483648 regardless of its sign or value.
- Messages sent by script on positive and negative channels are truncated to 1024 bytes. Messages sent by chat on positive channels are truncated to 1023 bytes. Messages sent by chat from negative channels are truncated to 254 bytes.
- Once a listen is registered its filters cannot be updated, if the listen is registered to llGetOwner, the listen will remain registered to the previous owner upon owner change.

  - Owner change can be detected with the changed event.
  - To work around this the old listen will need to be closed and a new one opened for the new owner.
- A prim cannot hear/listen to chat it generates. It can, however, hear a linked prim.

  - Chat indirectly generated (as a result of llDialog, llTextBox or from a linked prim) can be heard if in range.

## Examples

Trivial example to listen to any chat from the object owner and respond once.

| Single listen handle |
| --- |
| ```lsl // Says beep to owner the first-time owner says something in main chat // and then stops listening integer listenHandle; remove_listen_handle() { llListenRemove(listenHandle); } default { state_entry() { // Change the channel number to a positive integer // to listen for '/5 hello' style of chat. // target only the owner's chat on channel 0 (PUBLIC_CHANNEL) listenHandle = llListen(0, "", llGetOwner(), ""); } listen(integer channel, string name, key id, string message) { // we filtered to only listen on channel 0 // to the owner's chat in the llListen call above llOwnerSay("beep"); // stop listening until script is reset remove_listen_handle(); } on_rez(integer start_param) { llResetScript(); } changed(integer change) { if (change & CHANGED_OWNER) { llResetScript(); } } } ``` |

| Two listen handles |
| --- |
| ```lsl // Opens two listen handles upon touch_start and // stops listening whenever something heard passes either filter integer listenHandle_a; integer listenHandle_b; remove_listen_handles() { llListenRemove(listenHandle_a); llListenRemove(listenHandle_b); } default { touch_start(integer num_detected) { key id = llDetectedKey(0); string name = llDetectedName(0); listenHandle_a = llListen(5, "", id, ""); listenHandle_b = llListen(6, "", NULL_KEY, ""); llSay(0, "Listening now to '" + name + "' on channel 5."); llSay(0, "Listening now to anybody/anything on channel 6."); } listen(integer channel, string name, key id, string message) { if (channel == 5) llSay(0, name + " said: '/5 " + message + "'"); if (channel == 6) llSay(0, name + " said: '/6 " + message + "'"); remove_listen_handles(); } } ``` |

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

- listen

### Functions

- **llListenRemove** — Removes a listen
- **llListenControl** — Enables/Disables a listen
- **llWhisper** — Sends chat limited to 10 meters
- **llSay** — Sends chat limited to 20 meters
- **llShout** — Sends chat limited to 100 meters
- **llRegionSay** — Sends chat limited current sim
- **llRegionSayTo** — Sends chat region wide to a specific avatar, or their attachments, or to a rezzed object of known UUID

<!-- /wiki-source -->
