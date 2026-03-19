---
name: "llGetTexture"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a string that is the Blinn-Phong diffuse texture on face

If the texture is in the prim's inventory, the return value is the inventory name, otherwise the returned value is the texture UUID.'
signature: "string llGetTexture(integer face)"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetTexture'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgettexture"]
---

Returns a string that is the Blinn-Phong diffuse texture on face

If the texture is in the prim's inventory, the return value is the inventory name, otherwise the returned value is the texture UUID.


## Signature

```lsl
string llGetTexture(integer face);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `face` | face number or ALL_SIDES |


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetTexture)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetTexture) — scraped 2026-03-18_

Returns a string that is the Blinn-Phong diffuse texture on face

## Caveats

- If face indicates a face that does not exist the  return is NULL_KEY
- NULL_KEY is returned when the owner does not have full permissions to the object and the texture is not in the prim's inventory.
- The white texture from the texture picker is "5748decc-f629-461c-9a36-a35a221fe21f"
- The default texture (plywood) is "89556747-24cb-43ed-920b-47caed15465f"

## Examples

```lsl
//Tells (on chat) the texture keys / texture names on 6 sides
default
{
    state_entry()
    {
        integer i = 0;
        integer max = llGetNumberOfSides();
        while(i < max)
        {
            llSay(0,"Side " + (string)i + " texture is: " + (string)llGetTexture(i));
            ++i;
        }
    }
}
```

## See Also

### Functions

- **PrimitiveParams** — PRIM_TEXTURE
- llSetTexture
- **llSetLinkTexture** — Sets link's texture
- **llGetNumberOfSides** — Gets the number of faces on the prim

<!-- /wiki-source -->
