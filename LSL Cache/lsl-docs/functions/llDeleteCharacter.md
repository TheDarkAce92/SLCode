---
name: "llDeleteCharacter"
category: "function"
type: "function"
language: "LSL"
description: "Convert the object back to a standard object, removing all pathfinding properties."
signature: "void llDeleteCharacter()"
return_type: "void"
sleep_time: ""
energy_cost: ""
wiki_url: 'https://wiki.secondlife.com/wiki/llDeleteCharacter'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lldeletecharacter"]
---

Convert the object back to a standard object, removing all pathfinding properties.


## Signature

```lsl
void llDeleteCharacter();
```


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llDeleteCharacter)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llDeleteCharacter) — scraped 2026-03-18_

Convert the object back to a standard object, removing all pathfinding properties.

## Examples

```lsl
create_character()
{
//  Clear any previous character behaviors
    llDeleteCharacter();

//  default speed is 20
    llCreateCharacter([CHARACTER_DESIRED_SPEED, 10.0]);
    llWanderWithin(llGetPos(), <10.0, 10.0, 2.0>, []);
}

default
{
    on_rez(integer start_param)
    {
        llResetScript();
    }

    state_entry()
    {
        create_character();
    }

    touch_start(integer num_detected)
    {
    //  Clear any previous character behaviors
        llDeleteCharacter();
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
