---
name: "llListenRemove"
category: "function"
type: "function"
language: "LSL"
description: "Removes a listener registered by llListen using its handle"
wiki_url: "https://wiki.secondlife.com/wiki/llListenRemove"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "void llListenRemove(integer handle)"
parameters:
  - name: "handle"
    type: "integer"
    description: "The handle returned by llListen when the listener was registered"
return_type: "void"
energy_cost: "10.0"
sleep_time: "0.0"
patterns: ["lllistenremove"]
deprecated: "false"
---

# llListenRemove

```lsl
void llListenRemove(integer handle)
```

Removes the listener identified by `handle`. If `handle` is invalid or already removed, the call is silently ignored.

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `handle` | integer | Handle returned by `llListen` |

## Best Practice

Always remove listeners when they are no longer needed:
- After receiving the expected response
- When a timer expires (timeout)
- In `state_exit` (though state changes auto-remove all listeners anyway)

```lsl
integer gListener;

default
{
    touch_start(integer n)
    {
        llListenRemove(gListener);  // remove any previous listener first
        gListener = llListen(-99, "", llDetectedKey(0), "");
        llDialog(llDetectedKey(0), "Choose:", ["Yes", "No"], -99);
        llSetTimerEvent(30.0);
    }

    listen(integer ch, string nm, key id, string msg)
    {
        llListenRemove(gListener);
        llSetTimerEvent(0.0);
        llOwnerSay("Choice: " + msg);
    }

    timer()
    {
        llListenRemove(gListener);
        llSetTimerEvent(0.0);
    }
}
```

## See Also

- `llListen` — register a listener
- `llListenControl` — enable/disable without removing


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llListenRemove) — scraped 2026-03-18_

Removes listen event callback handle

## Caveats

- On state change or script reset all listens are removed automatically.

  - A state change can be used as a shortcut to releasing all listens in the script.
- No error is thrown if handle has already been released or is invalid.

## Examples

```lsl
// Listen for one line of chat from the owner, echo it back to them, then stop listening
integer ListenHandle;
default
{
    state_entry()
    {
        // Start listening on channel 0, for text from owner only
        ListenHandle = llListen(0, "", llGetOwner(), "");
    }
    listen(integer channel, string name, key id, string message)
    {
        llOwnerSay(message);            // Echo the message back to the owner
        llListenRemove(ListenHandle);   // Stop listening
    }
}
```

## Notes

- It is good practice to remove listeners when they are no longer required, or set them inactive via llListenControl

## See Also

### Events

| • listen |  |  |  |  |
| --- | --- | --- | --- | --- |

### Functions

- llListen
- llListenControl

<!-- /wiki-source -->
