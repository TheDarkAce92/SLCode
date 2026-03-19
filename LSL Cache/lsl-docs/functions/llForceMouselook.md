---
name: "llForceMouselook"
category: "function"
type: "function"
language: "LSL"
description: 'Sets if a sitting avatar should be forced into mouselook when they sit on this prim.

A sit target is not necessary for this function to work.'
signature: "void llForceMouselook(integer mouselook)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llForceMouselook'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llforcemouselook"]
---

Sets if a sitting avatar should be forced into mouselook when they sit on this prim.

A sit target is not necessary for this function to work.


## Signature

```lsl
void llForceMouselook(integer mouselook);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer (boolean)` | `mouselook` | boolean, if TRUE when an avatar sits on the prim, the avatar will be forced into mouselook mode, if FALSE (default) the avatar will keep their current camera mode. |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llForceMouselook)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llForceMouselook) — scraped 2026-03-18_

Sets if a sitting avatar should be forced into mouselook when they sit on this prim.

## Caveats

- This function has no effect on avatars already seated.
- The user may exit mouselook mode at any time.

  - This can be detected by polling llGetAgentInfo.
- There is nothing stopping someone from modifying or making a client that ignores this.

## Examples

**Force Mouselook on Sit**

```lsl
default
{
    state_entry()
    {
        llForceMouselook(TRUE); // Forces sitting avatars into mouselook.

        llForceMouselook(FALSE); // Reverts the setting to the default...
                                 // ...as with a newly created prim.
    }
}
```

## See Also

### Functions

- llAvatarOnSitTarget
- llGetAgentInfo
- llGetCameraRot
- llSetCameraAtOffset
- llSetCameraEyeOffset

<!-- /wiki-source -->
