---
name: "changed"
category: "event"
type: "event"
language: "LSL"
description: "Fires when various properties of the object or prim change, with CHANGED_* flags indicating what changed"
wiki_url: "https://wiki.secondlife.com/wiki/Changed"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "changed(integer change)"
parameters:
  - name: "change"
    type: "integer"
    description: "Bit field of CHANGED_* flags indicating what changed"
deprecated: "false"
---

# changed

```lsl
changed(integer change)
{
    if (change & CHANGED_OWNER)
    {
        // handle ownership change
    }
}
```

Fires when various properties of the prim or object change. The `change` parameter is a bit field — test individual flags with `&`.

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `change` | integer | Bitmask of `CHANGED_*` flags |

## CHANGED_* Constants

| Constant | Value | Description | Scope |
|----------|-------|-------------|-------|
| `CHANGED_INVENTORY` | 0x001 | Prim inventory changed | prim |
| `CHANGED_COLOR` | 0x002 | Colour or alpha changed | prim |
| `CHANGED_SHAPE` | 0x004 | Shape changed | prim |
| `CHANGED_SCALE` | 0x008 | Scale changed | prim |
| `CHANGED_TEXTURE` | 0x010 | Texture parameters changed | prim |
| `CHANGED_LINK` | 0x020 | Prims linked/unlinked or avatar seated/stood | object |
| `CHANGED_ALLOWED_DROP` | 0x040 | Non-owner added inventory via drag-drop | prim |
| `CHANGED_OWNER` | 0x080 | Ownership changed | object |
| `CHANGED_REGION` | 0x100 | Object crossed into a different region | object |
| `CHANGED_TELEPORT` | 0x200 | Attached avatar teleported | object |
| `CHANGED_REGION_START` | 0x400 | Region restarted | region |
| `CHANGED_MEDIA` | 0x800 | Prim Media changed | prim |
| `CHANGED_RENDER_MATERIAL` | 0x1000 | Render material changed | prim |

## Caveats

- Use bitwise `&` to test flags, not `&&`.
- Multiple flags can be set in one event.
- `CHANGED_INVENTORY` does not fire for script-initiated inventory changes or `llAllowInventoryDrop`.
- `CHANGED_SCALE` only fires on the root prim.
- Fires in any script using it, whether in child or root prim.

## Examples

```lsl
// Basic usage
default
{
    changed(integer change)
    {
        if (change & CHANGED_INVENTORY)
            llOwnerSay("Inventory changed");
        if (change & CHANGED_OWNER)
            llResetScript();
    }
}
```

```lsl
// Test multiple flags at once
default
{
    changed(integer change)
    {
        if (change & (CHANGED_OWNER | CHANGED_INVENTORY))
            llResetScript();
    }
}
```

## See Also

- `llResetScript` — reset script on owner change
- `llGetOwner` — get current owner
- `CHANGED_*` constants


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/changed) — scraped 2026-03-18_

## Caveats

- This event will trigger in any script using it (in its current running state) whether the script be in a child or root prim of a link_set, e. g., a changed event in a script in the wheel (child prim) of a car will trigger when any avatar sits on or stands from the seat (root prim) of that car.
- `CHANGED_SCALE` will fire when the scale of at least one prim in the linked object has changed. Only the root prim will receive this event.

## Examples

```lsl
default
{
    changed(integer change)
    {
        // note that it's & and not &&... it's bitwise!
        if (change & CHANGED_INVENTORY)
        {
            llOwnerSay("The inventory has changed.");
        }
        if (change & CHANGED_COLOR)
        {
            llOwnerSay("The color or alpha changed.");
        }
        if (change & CHANGED_SHAPE)
        {
            llOwnerSay("The prims shape has changed.");
        }
        if (change & CHANGED_SCALE)
        {
            llOwnerSay("The prims size has changed.");
        }
        if (change & CHANGED_TEXTURE)
        {
            llOwnerSay("The prims texture or texture attributes have changed.");
        }
        if (change & CHANGED_LINK)
        {
            llOwnerSay("The number of links have changed.");
        }
        if (change & CHANGED_ALLOWED_DROP)
        {
            llOwnerSay("The inventory has changed as a result of a user without mod permissions "+
                       "dropping an item on the prim and it being allowed by the script.");
        }
        if (change & CHANGED_OWNER)
        {
            llOwnerSay("The owner of the object has changed.");
        }
        if (change & CHANGED_REGION)
        {
            llOwnerSay("The region the object is in has changed.");
        }
        if (change & CHANGED_TELEPORT)
        {
            llOwnerSay("The object has been teleported while attached.");
        }
        if (change & CHANGED_REGION_START)
        {
            llOwnerSay("The regions has just restarted.");
        }
    }
}
```

For the same action to be called for multiple changes we can use the following syntax:

```lsl
default
{
    changed(integer change)
    {
        if(change & (CHANGED_OWNER | CHANGED_INVENTORY)) // Either of the changes will return true.
            llResetScript();
    }
}
```

## Notes

- Always test the value of change for the specific `CHANGED_*` flags you are interested in, unless you want your script to act upon any change that can cause a changed event to trigger.

  - New `CHANGED_*` flags, bugs and bug fixes could conceivably be added by LL at any time. Scripts should be written under the assumption that they will receive *changed* events not expected at the time or place of writing. For future proof scripts, use bitwise conditions as in the examples.
- See llGetOwner for a full discussion on `(change & CHANGED_OWNER)`
- CHANGED_INVENTORY will also trigger when inventory permissions are changed, a new feature request for a CHANGED_PERMISSIONS flag to trigger when the object permissions are changed can be voted for at [SCR-411](https://jira.secondlife.com/browse/SCR-411)
- If leaving a state from within a changed event that registers a change just before the state change, on return to that state, the changed event will trigger. For example —

```lsl
default
{
    changed(integer change)
    {
        if(change & CHANGED_LINK)
        {
            integer links = 0;
            if(llGetObjectPrimCount(llGetKey()) < (links = llGetNumberOfPrims()))
            {
                llUnSit(llGetLinkKey(links));
                state whatever;
            }
            else
            llOwnerSay("Some kind of linking or unlinking has changed me but, I am not being sat on.");
            // This will be chatted after returning to the default state.
        }
    }
}
state whatever
{
    state_entry()
    {
        llSetTimerEvent(10.0);
    }
    timer()
    {
        state default;
    }
}
```

<!-- /wiki-source -->
