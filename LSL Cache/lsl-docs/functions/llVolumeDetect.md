---
name: "llVolumeDetect"
category: "function"
type: "function"
language: "LSL"
description: 'If detect is TRUE, VolumeDetect is enabled, physical object and avatars can pass through the object.

This works much like Phantom, but unlike Phantom, VolumeDetect objects trigger collision_start and collision_end events when interpenetrating. Collision events will trigger in any script in the obje'
signature: "void llVolumeDetect(integer detect)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llVolumeDetect'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llvolumedetect"]
---

If detect is TRUE, VolumeDetect is enabled, physical object and avatars can pass through the object.

This works much like Phantom, but unlike Phantom, VolumeDetect objects trigger collision_start and collision_end events when interpenetrating. Collision events will trigger in any script in the object.


## Signature

```lsl
void llVolumeDetect(integer detect);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer (boolean)` | `detect` | TRUE enables, FALSE (default) disables |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llVolumeDetect)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llVolumeDetect) — scraped 2026-03-18_

If detect is TRUE, VolumeDetect is enabled, physical object and avatars can pass through the object.

## Caveats

- llDetectedLinkNumber will return 0 in collision_start and collision_end events of VolumeDetect objects (SVC-2996).
- It can only be applied to the root prim (which will make the entire object VolumeDetect).
- If the volume detecting object is *not* physical, it can only detect physical objects and avatars. If the object *is* physical, it can detect its collisions with static and keyframed motion objects as well.

### Attachments

**Note:** Attachments are not included in the avatar's bounding box. Collision events received by attachments are collisions the avatar is having with the world, not collisions the attachment is having. Nothing actually can collide with an attachment.

- It is meaningless to enabled on attachments. Attachments cannot collide with anything.
- Attachments do not receive collision events for avatar collisions with VolumeDetect objects.

  - Attachments do receive collision events for avatar collisions with non-VolumeDetect, non-phantom objects.

## Examples

```lsl
default
{
    state_entry()
    {
        llVolumeDetect(TRUE); // Starts llVolumeDetect
    }
    collision_start(integer total_number)
    {
        llSay(0, "Detected!"); // Tells you when something penetrates the prim
    }
}
```

## See Also

### Events

- collision_start
- collision
- collision_end

### Functions

- llPassCollisions

<!-- /wiki-source -->
