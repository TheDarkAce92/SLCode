---
name: "llExecCharacterCmd"
category: "function"
type: "function"
language: "LSL"
description: 'Send a command to the pathing system.

Currently only supports stopping the current pathfinding operation or causing the character to jump.'
signature: "void llExecCharacterCmd(integer cmd, list options)"
return_type: "void"
sleep_time: ""
energy_cost: ""
wiki_url: 'https://wiki.secondlife.com/wiki/llExecCharacterCmd'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llexeccharactercmd"]
---

Send a command to the pathing system.

Currently only supports stopping the current pathfinding operation or causing the character to jump.


## Signature

```lsl
void llExecCharacterCmd(integer cmd, list options);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `command` | Command to be sent. |
| `list (instructions)` | `options` | CHARACTER_CMD_* |


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llExecCharacterCmd)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llExecCharacterCmd) — scraped 2026-03-18_

Send a command to the pathing system.

## Caveats

- If another script in the same object issues CHARACTER_CMD_STOP then pathing in all scripts is cancelled.

## Examples

```lsl
vector patrol;

default
{
    state_entry()
    {
        patrol = llGetPos();
        llCreateCharacter([CHARACTER_MAX_SPEED, 25, CHARACTER_DESIRED_SPEED, 15.0]);
        state awake;
    }
}

state awake
{
    state_entry()
    {
        llSay(0, "I am guarding now");
        list points = [patrol + <5,0,0>, patrol - <5,0,0>];
        llPatrolPoints(points, []);
    }

    touch_start(integer total_number)
    {
        state sleep;
    }
}

state sleep
{
    state_entry()
    {
        llSay(0, "Going to sleep");
        llExecCharacterCmd(CHARACTER_CMD_SMOOTH_STOP, []);
    }

    touch_start(integer total_number)
    {
        patrol = llGetPos();
        //Jump to attention!
        llExecCharacterCmd(CHARACTER_CMD_JUMP, [0.5]);
        state awake;
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
