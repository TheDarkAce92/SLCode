---
name: "llEdgeOfWorld"
category: "function"
type: "function"
language: "LSL"
description: 'Checks to see whether the border hit by dir from pos is the edge of the world (has no neighboring simulator).

Returns a boolean (an integer) value. FALSE indicating there is a simulator in the direction indicated.

The z component of dir is ignored.'
signature: "integer llEdgeOfWorld(vector pos, vector dir)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llEdgeOfWorld'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lledgeofworld"]
---

Checks to see whether the border hit by dir from pos is the edge of the world (has no neighboring simulator).

Returns a boolean (an integer) value. FALSE indicating there is a simulator in the direction indicated.

The z component of dir is ignored.


## Signature

```lsl
integer llEdgeOfWorld(vector pos, vector dir);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `pos` | position in region coordinates |
| `vector (direction)` | `dir` | direction |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llEdgeOfWorld)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llEdgeOfWorld) — scraped 2026-03-18_

Checks to see whether the border hit by dir from pos is the edge of the world (has no neighboring simulator).Returns a boolean (an integer) value. FALSE indicating there is a simulator in the direction indicated.

## Caveats

- If the **x** and **y** components of dir are zero (like with ZERO_VECTOR), TRUE is always returned.
- pos must be in the region.
- Can only be used to detect directly adjacent regions, not diagonally adjacent regions
- This function will also return TRUE if llRequestSimulatorData() returns "up" for an adjacent region but that region doesn't visibly show when standing next to its border.

## Examples

```lsl
//--// Tells if there are neighboring sims on touch //--//

default{
  touch_start( integer vIntTouched ){
    vector vPosObject = llGetPos();
    if (!llEdgeOfWorld( vPosObject, <0.0, 1.0, 0.0> )){
      llOwnerSay( "There is a Sim to the North" );
    }
    if (!llEdgeOfWorld( vPosObject, <1.0, 0.0, 0.0> )){
      llOwnerSay( "There is a Sim to the East" );
    }
    if (!llEdgeOfWorld( vPosObject, <0.0, -1.0, 0.0> )){
      llOwnerSay( "There is a Sim to the South" );
    }
    if (!llEdgeOfWorld( vPosObject, <-1.0, 0.0, 0.0> )){
      llOwnerSay( "There is a Sim to the West" );
    }
  }
}
```

## See Also

### Constants

- STATUS_DIE_AT_EDGE
- STATUS_RETURN_AT_EDGE

### Functions

- llScriptDanger

<!-- /wiki-source -->
