---
name: "llRotBetween"
category: "function"
type: "function"
language: "LSL"
description: "Returns a rotation that is the shortest rotation between the direction start and the direction end"
signature: "rotation llRotBetween(vector v1, vector v2)"
return_type: "rotation"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llRotBetween'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llrotbetween"]
---

Returns a rotation that is the shortest rotation between the direction start and the direction end


## Signature

```lsl
rotation llRotBetween(vector v1, vector v2);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `start` |  |
| `vector` | `end` |  |


## Return Value

Returns `rotation`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llRotBetween)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llRotBetween) — scraped 2026-03-18_

Returns a rotation that is the shortest rotation between the direction start and the direction end

## Caveats

- `start * llRotBetween(start, end) == end` is only true if **start** and **end** have the same magnitude and neither have a magnitude of zero (see #Useful Snippets for a workaround).

  - This of course is ignoring floating point precision errors.
- The above is true because of vector magnitudes and not a shortcoming of this function. The **rotation** returned is **correct** regardless of magnitudes
- Rotations are from -PI to +PI around each axis.

## Examples

Drop the below script into a prim. This script will cause the object to orient it's positive X axis towards it's owner's avatar when touched.

```lsl
default
{
    touch_start(integer total_number)
    {
        list lTemp = llGetObjectDetails(llGetOwner(),[OBJECT_POS]); //Get the owner's position (region coordinates)
        vector start = llRot2Fwd(ZERO_ROTATION); //Object's X axis is forward. (Can be substituted with llRot2Left (Y axis) or llRot2Up (Z axis). Negative values (-llRot2Fwd) can be used to spin the prim 180 degrees)
        //start = llRot2Fwd( llAxisAngle2Rot(<0,0,1>,45*DEG_TO_RAD) ); //Uncommenting this line will cause the prim to point one of it's corners towards the avatar, instead of the forward face.
        vector end = llVecNorm(llList2Vector(lTemp,0) - llGetPos()); //Convert the owner's position into a normalized direction vector (relative to the prim).
        llSetLinkPrimitiveParamsFast(LINK_THIS,[PRIM_ROTATION,llRotBetween(start,end)]); //Set the prim's rotation accordingly.
    }
    //llRot2Fwd(ZERO_ROTATION) is equivalent to <1,0,0> , llRot2Left would be <0,1,0> and llRot2Up would be <0,0,1>. Negative values ( -llRot2Fwd(ZERO_ROTATION) ) would be <-1,0,0>, -llRot2Left would be <0,-1,0> and -llRot2Up would be <0,0,-1>
    //Note that a value other than ZERO_ROTATION may cause unexpected results. Unless you know the exact offset you need for your object, then leave this as-is.
} //Jenna Huntsman
```



```lsl
llRotBetween(<1.0, 0.0, 0.0>, <0.0, -1.0, 0.0>)
// will return <0.00000, 0.00000, -0.70711, 0.70711> (which represents -90 degrees on the z axis)

llRotBetween(<0.0, 0.0, 0.0>, <0.0, -1.0, 0.0>)
// will return <0.00000, 0.00000, 0.00000, 1.00000> (which represents a zero angle on all axis)
// because <0.0, 0.0, 0.0> does not convey a direction.
```

## Notes

Vectors that are near opposite each other in direction may lead to erroneous results.

```lsl
// First Vector is due north second vector is ALMOST due south.
rotation lRotation = llRotBetween( <0., 1., 0.>, <-0.001, -.1, 0.> );
llSay(0, lRotation );
// Provides a result of <1.00000, 0.00000, 0.00000, 0.00000>.
```

## See Also

### Functions

- llAngleBetween
- llRot2Fwd
- llRot2Left
- llRot2Up
- llVecNorm

<!-- /wiki-source -->
