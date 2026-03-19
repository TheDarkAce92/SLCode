---
name: "llGetNumberOfSides"
category: "function"
type: "function"
language: "LSL"
description: 'Returns an integer that is the number of faces (or sides) of the prim.

See Face for more information about faces and the conditions that control the number of faces a prim will have.'
signature: "integer llGetNumberOfSides()"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetNumberOfSides'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetnumberofsides"]
---

Returns an integer that is the number of faces (or sides) of the prim.

See Face for more information about faces and the conditions that control the number of faces a prim will have.


## Signature

```lsl
integer llGetNumberOfSides();
```


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetNumberOfSides)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetNumberOfSides) — scraped 2026-03-18_

Returns an integer that is the number of faces (or sides) of the prim.

## Examples

```lsl
default
{
    state_entry()
    {
        // Set the hovertext to indicate the number of sides
        integer numOfSides = llGetNumberOfSides();
        llSetText( "I have " + (string)numOfSides + " sides.", <1,1,1>, 1 );
    }
}
```

## See Also

### Functions

- **llGetLinkNumberOfSides** — Get number of faces for a linked prim

<!-- /wiki-source -->
