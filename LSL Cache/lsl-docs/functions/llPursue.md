---
name: "llPursue"
category: "function"
type: "function"
language: "LSL"
description: "Causes the object to pursue target."
signature: "void llPursue(key target, list options)"
return_type: "void"
sleep_time: ""
energy_cost: ""
wiki_url: 'https://wiki.secondlife.com/wiki/llPursue'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llpursue"]
---

Causes the object to pursue target.


## Signature

```lsl
void llPursue(key target, list options);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `target` | group, avatar or object UUID to pursue. |
| `list (instructions)` | `options` | Parameters for pursuit; see below. |


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llPursue)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llPursue) — scraped 2026-03-18_

Causes the object to pursue target.

## Caveats

- Must use llCreateCharacter or script crash (script error)
- Vertical positions specified for any vectors should be chosen to be as close as possible to the actual height of the terrain requested. Large difference between the provided vertical position and the actual terrain/object will result in failure of the behaviour.
- Z value is unused (erroneous if not 0.0) in parameter for PURSUIT_OFFSET.
- REQUIRE_LINE_OF_SIGHT does not require line of sight immediately after llPursue() is called - it only affects target position updates after the target object/agent moves.
- FUZZ_FACTOR picks a point within an area of approximately (scale * lengthOfOffset) around the offset position. Value must be between 0.0 and 1.0.

## Examples

```lsl
default
{
    state_entry()
    {
        llCreateCharacter([CHARACTER_DESIRED_SPEED, 35.0, CHARACTER_MAX_SPEED, 35.0]);
    }

    touch_start(integer total_number)
    {
        llPursue(llDetectedKey(0), [PURSUIT_OFFSET, <-2.0, 0.0, 0.0>, PURSUIT_FUZZ_FACTOR, 0.2]);
    }
}
```

## See Also

### Events

- path_update

### Functions

- llCreateCharacter
- llDeleteCharacter
- llEvade
- llExecCharacterCmd
- llGetClosestNavPoint
- llFleeFrom
- llNavigateTo
- llPatrolPoints
- llPursue
- llUpdateCharacter
- llWanderWithin

<!-- /wiki-source -->
