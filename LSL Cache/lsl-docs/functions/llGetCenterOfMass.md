---
name: "llGetCenterOfMass"
category: "function"
type: "function"
language: "LSL"
description: 'Returns the vector position of the object's center of mass in region coordinates.

If called from a child prim, the child's center of mass is returned instead (but still in region coordinates).'
signature: "vector llGetCenterOfMass()"
return_type: "vector"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetCenterOfMass'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetcenterofmass"]
---

Returns the vector position of the object's center of mass in region coordinates.

If called from a child prim, the child's center of mass is returned instead (but still in region coordinates).


## Signature

```lsl
vector llGetCenterOfMass();
```


## Return Value

Returns `vector`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetCenterOfMass)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetCenterOfMass) — scraped 2026-03-18_

Returns the vector position of the object's center of mass in region coordinates.

## Caveats

- Works in **physical objects only**.

  - The value is stored as a prim property and will only change when Center Of Mass is computed.
  - If called from within a non-physical object it will return the stored COM value or in the absence of a stored COM value it will return llGetPos().

  - It will not compute or recompute the COM if the object is non-physical.
  - The stored value can only be updated when the object is physical. Neither moving or changing the objects shape will update, invalidate or remove the stored COM value when it is non-physical.

## Examples

```lsl
//  this example script will not check for physical status
//  you'll usually need it though to get a correct vector

default
{
    state_entry()
    {
        vector massCenter = llGetCenterOfMass();
        integer link = llGetLinkNumber();

        if (link == 0 || link == 1) llSay(PUBLIC_CHANNEL,
            "The center of the mass of the object is " + (string)massCenter);

        else if (1 < link) llSay(PUBLIC_CHANNEL,
            "The center of the mass of link no. " + (string)link + " is " + (string)massCenter);

        //  this script was just a test, remove it again
        string thisScript = llGetScriptName();
        llRemoveInventory(thisScript);
    }
}
```

## See Also

### Functions

- llGetPos
- llGetGeometricCenter

<!-- /wiki-source -->
