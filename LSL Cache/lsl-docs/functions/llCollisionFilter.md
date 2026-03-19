---
name: "llCollisionFilter"
category: "function"
type: "function"
language: "LSL"
description: 'Sets the collision filter, exclusively or inclusively.

If accept == TRUE, only accept collisions with objects name AND id (either is optional), otherwise with objects not name AND id
If name or id are blank they are not used to filter incoming messages (or you could say they match everything). If i'
signature: "void llCollisionFilter(string name, key id, integer accept)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llCollisionFilter'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llcollisionfilter"]
---

Sets the collision filter, exclusively or inclusively.

If accept == TRUE, only accept collisions with objects name AND id (either is optional), otherwise with objects not name AND id
If name or id are blank they are not used to filter incoming messages (or you could say they match everything). If id is an invalid key or a null key, it is considered blank.


## Signature

```lsl
void llCollisionFilter(string name, key id, integer accept);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `name` | filter for specific object name or avatar legacy name |
| `key` | `id` | filter by group, avatar or object UUID |
| `integer (boolean)` | `accept` | TRUE only process collisions that match, FALSE instead excludes matches |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llCollisionFilter)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llCollisionFilter) — scraped 2026-03-18_

Sets the collision filter, exclusively or inclusively.

## Caveats

- Any call of llCollisionFilter in the same event as llVolumeDetect changing (not just being called, but actually moving from FALSE to TRUE or vice versa) will be disregarded (before or after), **if** the event handler previously called a user-defined function. See #SVC-2490

  - You can get around this by calling them in separate events, such as touch_start and touch_end.
- Damage caused by llSetDamage will still apply to a filtered avatar.

  - Consequently, the object will immediately die on collision with the avatar. (And kill the avatar their health reaches 0.)

## Examples

- Stop filtering:

`llCollisionFilter("", NULL_KEY, TRUE);`

- Filter out all collisions:

`llCollisionFilter("", NULL_KEY, FALSE);`

This script, placed in a wearable object, detects a collision when the person wearing it collides with an object named "Post":

- 1st instance :

an object named "Post" has several child prims named "Object" .
The prim named "Post" hits the scripted object or scripted prim , the collision will be detected

- 2nd instance :

an object named "Post" has several child prims named "Object" .
A child prim named "Object" hits the scripted object or scripted prim, the collision will be detected

- 3rd instance :

an object named "Object" has several child prims named "Post" .
A prim named "Post" hits the scripted object or scripted prim, the collision will not be detected

```lsl
default
{
    state_entry()
    {
        llCollisionFilter("Post","",TRUE);
    }

    collision_start(integer total_number)
    {
        llSay(0, "OUCH!");
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
- llVolumeDetect

<!-- /wiki-source -->
