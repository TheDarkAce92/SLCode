---
name: "llGetAnimation"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a string that is the name of the currently playing locomotion animation for avatar id. See the table below.

llGetAgentInfo provides information on some animation states not covered by this function (typing, away, busy). llGetAnimationList provides more detailed information about the running'
signature: "string llGetAnimation(key id)"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetAnimation'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetanimation"]
---

Returns a string that is the name of the currently playing locomotion animation for avatar id. See the table below.

llGetAgentInfo provides information on some animation states not covered by this function (typing, away, busy). llGetAnimationList provides more detailed information about the running animations, but may not reflect avatar state as accurately as llGetAnimation.


## Signature

```lsl
string llGetAnimation(key id);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `id` | avatar UUID that is in the same region |


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetAnimation)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetAnimation) — scraped 2026-03-18_

Returns a string that is the name of the currently playing locomotion animation for avatar id. See the table below.

## Caveats

- This function can return an empty string while the avatar is logging out.
- New return values could conceivably be added at any time and this list may not in-fact be complete. Scripts should be written under the assumption that they may receive a value they won't recognize.

## Examples

```lsl
// A simple animation override example.
// Make the avatar run in mid-air when jumping.

key gOwner; // the wearer's key
string gLastAnimation; // last llGetAnimation value seen

// User functions

Initialize(key id) {
    if (id == NULL_KEY) { // detaching
        llSetTimerEvent(0.0); // stop the timer
    }
    else { // attached, or reset while worn
        llRequestPermissions(id, PERMISSION_TRIGGER_ANIMATION);
        gOwner = id;
    }
}

// Event handlers

default
{
    state_entry() {
        // in case the script was reset while already attached
        if (llGetAttached() != 0) {
            Initialize(llGetOwner());
        }
    }

    attach(key id) {
        Initialize(id);
    }

    run_time_permissions(integer perm) {
        if (perm & PERMISSION_TRIGGER_ANIMATION) {
            llSetTimerEvent(0.25); // start polling
        }
    }

    timer() {
        string newAnimation = llGetAnimation(gOwner);

        if (gLastAnimation != newAnimation) { // any change?
            if (newAnimation == "Jumping") {

                // You can stop the built-in animation if you like, if
                // it might interfere with your own. Be aware that an
                // avatar can become stuck, and some llGetAgentInfo results
                // can be inaccurate, if you stop built-ins indiscriminately.
                // Always test.
                //
                // llStopAnimation("jump");

                llStartAnimation("run");
            }
            else if (gLastAnimation == "Jumping")  { // just finished jumping
                // "run" is looped, so we have to stop it when we are done.
                llStopAnimation("run");
            }

            gLastAnimation = newAnimation; // store away for  next time
        }
    }
}
```

## See Also

### Functions

- llGetAgentInfo
- llGetAnimationList

<!-- /wiki-source -->
