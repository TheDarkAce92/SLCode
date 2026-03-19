---
name: "llGetObjectMass"
category: "function"
type: "function"
language: "LSL"
description: "Returns a float that is the mass of id"
signature: "float llGetObjectMass(key id)"
return_type: "float"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetObjectMass'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetobjectmass"]
---

Returns a float that is the mass of id


## Signature

```lsl
float llGetObjectMass(key id);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `id` | avatar or object UUID that is in the same region |


## Return Value

Returns `float`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetObjectMass)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetObjectMass) — scraped 2026-03-18_

Returns a float that is the mass of id

## Caveats

- Returns zero if **id** is not found in the region.
- **id** can be any prim in the object.

## Examples

```lsl
default
{
    touch(integer n)
    {
        llSay(0, llDetectedName(0) + " your mass is " + (string)llGetObjectMass(llDetectedKey(0)) + " lindogram.");
    }
}
//Anylyn Hax 15:02, 28 July 2007 (PDT)
```

## Notes

- [Mass](http://en.wikipedia.org/wiki/Mass) in SL is expressed as *lindogram*. One lindogram appears to be equal to 100 kilograms.
- Mass for avatars is relative to shape/size, and unaffected by attachments. However, a survey of masses for avatars shows less variation than one would expect relative to shape/size, and the lindogram masses do not appear in any way realistic.
- Sitting avatars add their mass to the object.
- This function returns a mass of 0.01 for child agents.
- This function is a handy way to determine if an object or avatar still exists on a region. Other methods exist (such as checking that OBJECT_OWNER returned by llGetObjectDetails is a valid key), but this has slightly less overhead.

## See Also

### Functions

- **llGetMass** — Gets the current object mass.

<!-- /wiki-source -->
