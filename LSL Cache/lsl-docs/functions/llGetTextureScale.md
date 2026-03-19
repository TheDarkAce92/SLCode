---
name: "llGetTextureScale"
category: "function"
type: "function"
language: "LSL"
description: "Returns a vector that is the texture scale on face (only the x and y components are used)."
signature: "vector llGetTextureScale(integer side)"
return_type: "vector"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetTextureScale'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgettexturescale"]
---

Returns a vector that is the texture scale on face (only the x and y components are used).


## Signature

```lsl
vector llGetTextureScale(integer side);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `face` | face number or ALL_SIDES |


## Return Value

Returns `vector`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetTextureScale)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetTextureScale) — scraped 2026-03-18_

Returns a vector that is the texture scale on face (only the x and y components are used).

## Caveats

- If face indicates a face that does not exist the  return is <1.0, 1.0, 0.0>
- ALL_SIDES seems to return the scale of the *first* face, not an average or other function of all the faces.  It acts much like if it were called with `face=0`.

## Examples

```lsl
//Script by Basil Wijaya, 2009 August 08
//Sets texture scale on face 0.
//Corresponds to the object edit window, Texture tab, Repeats per Face: Horiontal U and Vertical V

float U_repeats = 1.0;
float V_repeats = 1.0;
integer face = 0;

default
{
    state_entry()
    {
        llScaleTexture( U_repeats, V_repeats, ALL_SIDES);
    }

    touch_start(integer num)
    {
        U_repeats = U_repeats + .2;
        V_repeats = V_repeats + .5;

        //set texture scale on a face
        llScaleTexture( U_repeats , V_repeats, face);
        llOwnerSay("Scale has been set to " + (string)U_repeats +  " and " +  (string)V_repeats);

        //get texture scale of a face
        vector scale_vector = llGetTextureScale(face);
        llOwnerSay("llGetTextureScale(0) gives a vector :  " +  (string)scale_vector);
        //You can see that the first 2 values of the vector contain the U_repeats and V_repeats values we have setted.

        //The object edit window, in the Texture tab, shows the changes of the U and V values, but only for face 0.
        //Other faces changes are done but do not show in the edit window.
    }
}
```

## See Also

### Functions

- llScaleTexture

<!-- /wiki-source -->
