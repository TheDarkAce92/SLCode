---
name: "llGetOwner"
category: "function"
type: "function"
language: "LSL"
description: "Returns the UUID of the object's owner (or group UUID if group-owned)"
wiki_url: "https://wiki.secondlife.com/wiki/llGetOwner"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "key llGetOwner()"
parameters: []
return_type: "key"
energy_cost: "10.0"
sleep_time: "0.0"
patterns: ["llgetowner"]
deprecated: "false"
---

# llGetOwner

```lsl
key llGetOwner()
```

Returns the UUID of the object's owner. If the object is deeded to a group, returns the group UUID.

## Return Value

`key` — owner UUID, or group UUID for group-owned objects.

## Caveats

- **Ownership changes are not automatic:** Cached values from a previous owner remain stale. Listen for `CHANGED_OWNER` in the `changed` event and re-call `llGetOwner` (or `llResetScript`).
- **Group-owned objects:** Returns the group UUID, not an individual avatar. `llOwnerSay` will silently fail in this case — use `llInstantMessage` instead.

## Examples

```lsl
// Basic usage
llOwnerSay((string)llGetOwner());           // print UUID
llOwnerSay(llKey2Name(llGetOwner()));       // print name (if in region)
```

```lsl
// Handle owner changes
integer listenHandle;

init()
{
    key owner = llGetOwner();
    llListenRemove(listenHandle);
    listenHandle = llListen(PUBLIC_CHANNEL, "", owner, "");
    llRequestPermissions(owner, PERMISSION_TRIGGER_ANIMATION);
}

default
{
    state_entry() { init(); }
    on_rez(integer start) { init(); }
    changed(integer change)
    {
        if (change & CHANGED_OWNER) init();
    }
}
```

## See Also

- `llGetKey` — UUID of the prim containing the script
- `llKey2Name` — convert UUID to avatar name
- `changed` event with `CHANGED_OWNER`
- `llOwnerSay` — message to owner
- `llInstantMessage` — IM to owner by key


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetOwner) — scraped 2026-03-18_

Returns a key that is the object owner's UUID.

## Caveats

- When the owner of an object changes, code that depends on this function's return value will not automatically update for the new owner or be automatically re-evaluated.

  - This requires the reregistration of listens and  requesting of permissions from the new owner as needed.

  - This is not limited to listens and permissions but anything that caches the return value, it is up to the programmer to work around this limitation.
  - Detection of owner change can be achieved with the changed event in conjunction with the CHANGED_OWNER flag (see the second example) or by storing the old value and periodically (e.g. in on_rez) checking if it has changed. Both techniques are valid though the latter will not detect the sale of the object if it is sold with "sell original" in-world and not picked up.
- When the object is deeded to a group, the UUID returned is that of the group.

## Examples

```lsl
llOwnerSay( (string)llGetOwner()); // speaks in chat the "key" (UUID code) of the avatar.
llOwnerSay( llKey2Name(llGetOwner())); // speaks in chat the name of the owner if in the sim.
```

```lsl
default
{
    changed(integer change)
    {
        if (change & CHANGED_OWNER)
            llResetScript();
    }

    state_entry()
    {
        key owner = llGetOwner();
        llInstantMessage(owner, "Only you can hear me. Isn't that eerie.");
    }
}
```

## Notes

To retrieve the owners name while the owner is in the region use llKey2Name, llGetUsername or llGetDisplayName. Respectively llRequestAgentData, llRequestUsername or llRequestDisplayName should be used when the owner is not in the region.

The one problem many coders come up against is that previously-activated events referring to the owner don't automatically change when the owner changes.  The most often-seen result is a listen registered to owner will continue to listen to the PREVIOUS owner rather than the CURRENT owner.  It is often confused as a bug in llGetOwner or llListen it is not in fact a bug but part of the design.  There are several ways of working around this problem.  The easy solution is to reset the script when owner changes or it is rezzed. The easy solution is not always the right solution.

There are two ways to detect if the owner has changed, the most reliable is to use the changed event.

```lsl
changed(integer change)
{
    if (change & CHANGED_OWNER)//if owner changes, reset the script.
        llResetScript();
}
```

In many applications resetting the script when the object is rezzed is an adequate and easy solution.

```lsl
on_rez(integer start_param)
{ //when the object is rezzed, reset the script.
    llResetScript();
}
```

Resetting the script is not appropriate if the script needs to keep it's data when it's ownership is transfered or if script startup is slow, in these situations listens will need to be re-keyed to the new owner along with any other owner specific code, like who the script is supposed to be animating.

The on_rez and changed events can be harnessed to reinitialize owner specific code every time the object is rezzed or changes owner.

```lsl
integer listen_handle;

init()
{
    key owner = llGetOwner();
    llListenRemove(listen_handle);
    // PUBLIC_CHANNEL has the integer value 0
    listen_handle = llListen(PUBLIC_CHANNEL, "", owner, "");
    llRequestPermissions(owner, PERMISSION_TRIGGER_ANIMATION);
}

default
{
    state_entry()
    {
        init();
        //insert additional startup code here that doesn't need to run each rez/owner change
        //for example, reading settings from a notecard
    }

    on_rez(integer start)
    {
        init();
    }

    changed(integer change)
    {
        if (change & CHANGED_OWNER)
            init();
    }

    run_time_permissions(integer perm)
    {//always use the run_time_permissions event with llRequestPermissions, never assume
        if(perm & PERMISSION_TRIGGER_ANIMATION)
        {
            //setup your animation code here, start your timers, etc.
            llOwnerSay("I have animation permissions");
        }
    }
}
```

## See Also

### Functions

- llGetCreator
- llGetOwnerKey
- llDetectedOwner

<!-- /wiki-source -->
