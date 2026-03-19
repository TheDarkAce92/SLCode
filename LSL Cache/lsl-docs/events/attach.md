---
name: "attach"
category: "event"
type: "event"
language: "LSL"
description: "Fires when the object is attached to or detached from an avatar"
wiki_url: "https://wiki.secondlife.com/wiki/Attach"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "attach(key id)"
parameters:
  - name: "id"
    type: "key"
    description: "Avatar UUID if attached; NULL_KEY if detached"
deprecated: "false"
---

# attach

```lsl
attach(key id)
{
    if (id)
    {
        // attached
    }
    else
    {
        // detached
    }
}
```

Fires when the object is attached to an avatar (`id` = avatar UUID) or detached (`id` = NULL_KEY).

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | key | Avatar UUID when attached; NULL_KEY when detached |

## When Triggered

**Attachment:**
- Object attached from ground
- Object attached from inventory
- Avatar wearing object logs in

**Detachment:**
- Object dropped to ground
- Object taken to inventory
- (Avatar logout — anticipated but not reliable)

## When NOT Triggered

- Avatar teleports — use `CHANGED_TELEPORT` in `changed` event instead
- Region crossing — use `CHANGED_REGION` instead
- Temp attachment (`llAttachToAvatarTemp`) detach — no reliable detection

## Caveats

- When detaching to inventory, execution time is limited — keep the handler short.
- `llGetAttached()` returns 0 both on detach to inventory and drop to ground; check `id == NULL_KEY && llGetAttached() == 0` to confirm detach.
- `on_rez` fires before `attach` when attaching from inventory or logging in.
- Bug in child prims: when attaching, a detached event fires first, then an attached event. When detaching from a child prim, **no event is triggered at all**.

## Example

```lsl
default
{
    attach(key id)
    {
        if (id)
        {
            llOwnerSay("Attached to " + llKey2Name(id));
            llRequestPermissions(id, PERMISSION_TRIGGER_ANIMATION);
        }
        else
        {
            llOwnerSay("Detached");
        }
    }
}
```

## See Also

- `on_rez` — fires before `attach` on login/inventory attach
- `changed` event with `CHANGED_TELEPORT`, `CHANGED_REGION`
- `llGetAttached` — get current attachment point
- `llRequestPermissions` — request avatar permissions


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/attach) — scraped 2026-03-18_

## Caveats

- When detached to inventory, an object is only given limited time to execute its attach events. If these events are active when the script derezzes but have not completed, execution will finish when the object is next rezzed.  If the script is busy handling a *different* event at detach time, an attach event with id=NULL_KEY can happen on the next rez, followed by one with the wearer's key. To verify a real detach, check that id == NULL_KEY *AND* llGetAttached() == 0.
- If the script is busy with a complex event handler before it is taken to inventory, the event queue can overflow, leaving no room to capture new events. The queue is preserved, so attach and on_rez may not be triggered the next time the object is rezzed. To guard against this possibility, llGetAttached can be checked in other events.
- When detaching an object, llGetAttached() returns 0, but the same happens when dropping an object from an attachment point to the ground. No other indicative event is triggered in the latter case; in particular, the on_rez event is not triggered for attachment drops. If you need to distinguish a drop from a detach, a possible hack is to check llGetObjectPrimCount(llGetKey()). If it's zero, it can be assumed that the object is being detached; otherwise, that it is being dropped.
- There is a bug when an attach event is in a script in a child prim.  When the object is attached, a detached event is first triggered, and then an attached event is triggered.  When the object is detached, no event is triggered.

## Examples

The following is a simplified example of the attach event. The variable id will be the key of the avatar the scripted object is attached to otherwise it will take on the value of NULL_KEY. The conditional if statement is used to determine the value of the variable id.

```lsl
default
{
    attach(key id)
    {
        if (id)     // is a valid key and not NULL_KEY
        {
            llSay(0, "I have been attached!");
        }
        else
        {
            llSay(0, "I have been detached!");
        }
    }
}
```

## Notes

### on_rez & attach

on_rez will be triggered prior to attach when attaching from inventory or during login.

## See Also

### Events

| • on_rez |  |  |  |  |
| --- | --- | --- | --- | --- |

### Functions

| • llAttachToAvatar |  |  |  |  |
| --- | --- | --- | --- | --- |
| • llDetachFromAvatar |  |  |  |  |
| • llGetAttached |  |  |  |  |

### Articles

| • Attachment |  |  |  |  |
| --- | --- | --- | --- | --- |

<!-- /wiki-source -->
