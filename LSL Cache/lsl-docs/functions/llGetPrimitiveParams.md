---
name: "llGetPrimitiveParams"
category: "function"
type: "function"
language: "LSL"
description: 'Returns attribute values (a list) for the attributes requested in the params list.

PRIM_* flags can be broken into three categories, face flags, prim flags, and object flags.

* Supplying a prim or object flag will return that flag's attributes.
* Face flags require the user to also supply a side p'
signature: "list llGetPrimitiveParams(list params)"
return_type: "list"
sleep_time: "0.2"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetPrimitiveParams'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetprimitiveparams"]
---

Returns attribute values (a list) for the attributes requested in the params list.

PRIM_* flags can be broken into three categories, face flags, prim flags, and object flags.

* Supplying a prim or object flag will return that flag's attributes.
* Face flags require the user to also supply a side parameter.


## Signature

```lsl
list llGetPrimitiveParams(list params);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `list (instructions)` | `params` | PRIM_* flags |


## Return Value

Returns `list`.


## Caveats

- Forced delay: **0.2 seconds** — the script sleeps after each call.
- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetPrimitiveParams)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetPrimitiveParams) — scraped 2026-03-18_

Returns attribute values (a list) for the attributes requested in the params list.

## Caveats

- The prim description is limited to 127 bytes; any string longer then that will be truncated. This truncation does not always happen when the attribute is set or read.
- The prim description may only contain printable ASCII characters (code points 32-126), except the pipe character '|', which is not permitted for historical reasons. All other characters will be replaced with one '?' character per illegal UTF-8 byte.
- Note that when people have "Hover Tips on All Objects" selected in the viewer's "View" menu, they'll see the object description pop-up for any object under their mouse pointer.  For that reason, it is good practice to only set human-friendly information in the description, e.g. keys and such.
- When an attached object is detached, changes made by script to the name and description (of the root prim) of the attachment will be lost. While the object is attached the name and description can be changed but it will not be reflected in inventory. This caveat does *not* apply to child prims.
- repeats is not only used to get the number of repeats but the sign of the individual components indicate if "Flip" is set.
- With texture as with llGetTexture, NULL_KEY is returned when the owner does not have full permissions to the object and the texture is not in the prim's inventory.
- In the default texture mapping mode the texture repeats units are in texture repeats per face. In the planar texture mapping mode the texture repeats units are in texture repeats per half meter. This is in contrast to the in-world editing tool, in which the planar texture scaling units are repeats per meter.
- With render_material as with llGetRenderMaterial, NULL_KEY is returned when the owner does not have full permissions to the object and the material is not in the prim's inventory.
- In the default texture mapping mode the texture repeats units are in texture repeats per face. In the planar texture mapping mode the texture repeats units are in texture repeats per half meter. This is in contrast to the in-world editing tool, in which the planar texture scaling units are repeats per meter.
- Do not rely on Floating Text as a storage medium; it is neither secure nor finalized.

  - Floating text has been altered in past server updates, breaking existing content; future changes may occur.
  - Even "invisible" floating text is transmitted to the client.

  - It can be viewed by anyone with a client that is capable of rendering text that is supposed to be invisible.
  - The network packets that contain the text can be sniffed and the text read.
- top_size and client values are different, the ranges do not line up, conversion is required. This simple equation can be used: answer = 1.0 - value. See top_size Explained for more information.
- The value of map is NULL_KEY when the owner does not have full permissions to the object and the map asset is not in the prim's inventory.
- If map is missing from the prim's inventory  and it is not a UUID or it is not a texture then an error is shouted on DEBUG_CHANNEL.
- If map is a UUID then there are no new asset permissions consequences for the object.

  - The resulting object develops no new usage restrictions that might have occurred if the asset had been placed in the prims inventory.
- position is always in region coordinates, even if the prim is a child or the root prim of an attachment.
- rot is always the global rotation, even if the prim is a child or the root prim of an attachment.
- PRIM_ROTATION incorrectly reports the avatars rotation when called on the root of an attached object. Use PRIM_ROT_LOCAL for the root prim instead.
- PRIM_OMEGA on nonphysical objects, and child prims of physical objects, is only a client side effect; the object or prim will collide as non-moving geometry.
- PRIM_OMEGA cannot be used on avatars sitting on the object. It will emit the error message "PRIM_OMEGA disallowed on agent".
- If PRIM_OMEGA does not appear to be working, make sure that that Develop > Network > Velocity Interpolate Objects is enabled on the viewer.
- In the parameters returned by `llGetPrimitiveParams([PRIM_OMEGA])`, the vector is normalized, and the spinrate is multiplied by the magnitude of the original vector.
- repeats is not only used to get the number of repeats but the sign of the individual components indicate if "Flip" is set.
- With texture as with llGetTexture, NULL_KEY is returned when the owner does not have full permissions to the object and the texture is not in the prim's inventory.
- If face indicates a face that exists but does not contain a material, the PRIM_NORMAL return is **[ NULL_KEY, <1,1,0>, ZERO_VECTOR, 0.0 ]**
- In the default texture mapping mode the texture repeats units are in texture repeats per face. In the planar texture mapping mode the texture repeats units are in texture repeats per half meter. This is in contrast to the in-world editing tool, in which the planar texture scaling units are repeats per meter.
- repeats is not only used to get the number of repeats but the sign of the individual components indicate if "Flip" is set.
- With texture as with llGetTexture, NULL_KEY is returned when the owner does not have full permissions to the object and the texture is not in the prim's inventory.
- If face indicates a face that exists but does not contain a material, the PRIM_SPECULAR return is **[ NULL_KEY, <1,1,0>, ZERO_VECTOR, 0.0 <1,1,1>, 51, 0]**
- In the default texture mapping mode the texture repeats units are in texture repeats per face. In the planar texture mapping mode the texture repeats units are in texture repeats per half meter. This is in contrast to the in-world editing tool, in which the planar texture scaling units are repeats per meter.
- If  PRIM_LINK_TARGET's link_target describes a seated avatar...

  - Flags not explicitly mentioned have obvious values.
  - PRIM_NAME will return the avatar's legacy name.
  - PRIM_DESC will return `""`.
  - PRIM_TYPE will return `[PRIM_TYPE_BOX, PRIM_HOLE_DEFAULT, <0., 1., 0.>, 0., ZERO_VECTOR, <1., 1., 0.>, ZERO_VECTOR]`
  - PRIM_SLICE will return `[<0., 1., 0.>]`
  - PRIM_MATERIAL will return `PRIM_MATERIAL_FLESH`.
  - PRIM_TEMP_ON_REZ will return `FALSE`.
  - PRIM_PHANTOM will return `FALSE`.
  - PRIM_SIZE will return `llGetAgentSize(llGetLinkKey(link))`.
  - PRIM_TEXT will return `["", ZERO_VECTOR, 1.]`.
  - PRIM_POINT_LIGHT will return `[FALSE, ZERO_VECTOR, 0., 0., 0.]`.
  - PRIM_FLEXIBLE will return `[FALSE, 0, 0., 0., 0., 0., ZERO_VECTOR]`.
  - PRIM_COLOR, PRIM_TEXTURE, PRIM_GLOW, PRIM_FULLBRIGHT, PRIM_BUMP_SHINY, PRIM_TEXGEN

  - will return `[]` and report a script error to the owner: "texture info cannot be accessed for avatars."
- If face is ALL_SIDES then the flag works on all sides.
- If face indicates a face that does not exist the flag returns nothing.
- PRIM_LINK_TARGET is a special parameter which can be inserted to perform actions on multiple prims on the linkset with one call.

  - Passing 0 (zero) as the link number in the formal link parameter on a linked object will return an empty list.
- The legacy value of PRIM_TYPE, 1 (which is often referred to as PRIM_TYPE_LEGACY), is not supported by this function as a flag.

## Examples

To test whether an object is a point light source, and if so get its parameters:

```lsl
default
{
    state_entry()
    {
        list    params  = llGetPrimitiveParams([PRIM_POINT_LIGHT]);
        integer isLight = llList2Integer(params, 0);

        string msg = "Object is ";

        if (!isLight) // read as "not isLight"
            msg += "not a light source.";
        else
        {
            msg += "a point light source.";

        //  llList2String will automatically typecast

            msg += "\n\tColour    = " + llList2String(params, 1);
            msg += "\n\tIntensity = " + llList2String(params, 2);
            msg += "\n\tRadius    = " + llList2String(params, 3);
            msg += "\n\tFalloff   = " + llList2String(params, 4);
        }

        llSay(0, msg);
    }
}
```

```lsl
//code snippets by Strife Onizuka, Xen Lisle and Kireji Haiku
integer AreAllPrimsAreGlowing()
{
	//The root prim is either link number is 0 or 1
	//It is only zero if it is a single prim object with no avatars sitting on it.
	//llGetNumberOfPrims() returns the number of prims and seated avatars.
	integer link = llGetNumberOfPrims() > 1;

	//We want to loop over all prims but not avatars, so we need to know how many prims there are.
	//Fortunately the avatars are added to the end of the link set, their link numbers always come after the last prim.
	//llGetObjectPrimCount(llGetKey()) only returns only the number of prims, it doesn't count avatars.
	//To determine the upper bound, we need to take into consideration the link number of the root prim.
	integer end = link + llGetObjectPrimCount(llGetKey());

	for(;link < end; ++link)//loop through all prims
	{
		if( llListStatistics(LIST_STAT_MAX, llGetLinkPrimitiveParams(link, [PRIM_GLOW, ALL_SIDES])) <= 0.0)
		{//we can exit early because we know that if this value is less than or equal to zero, so will the minimum
			return FALSE;
		}
	}
	//we didn't find a single value that was less than or equal to zero, QED, they are all greater than zero.
	return TRUE;
}

default
{
	touch_start(integer num_detected)
	{
		if(AreAllPrimsAreGlowing())
			llSay(0, "All prims glowing.");
		else
			llSay(0, "Not all prims glowing.");
	}
}
```

## Notes

### Link Numbers

Each prim that makes up an object has an address, a link number. To access a specific prim in the object, the prim's link number must be known. In addition to prims having link numbers, avatars seated upon the object do as well.

- If an object consists of only one prim, and there are no avatars seated upon it, the (root) prim's link number is zero.
- However, if the object is made up of multiple prims or there is an avatar seated upon the object, the root prim's link number is one.

When an avatar sits on an object, it is added to the end of the link set and will have the largest link number. In addition to this, while an avatar is seated upon an object, the object is unable to link or unlink prims without unseating all avatars first.

#### Counting Prims & Avatars

There are two functions of interest when trying to find the number of prims and avatars on an object.

- `llGetNumberOfPrims()` - Returns the number of prims and seated avatars.
- `llGetObjectPrimCount(llGetKey())` - Returns only the number of prims in the object but will return zero for attachments.

```lsl
integer GetPrimCount() { //always returns only the number of prims
    if(llGetAttached())//Is it attached?
        return llGetNumberOfPrims();//returns avatars and prims but attachments can't be sat on.
    return llGetObjectPrimCount(llGetKey());//returns only prims but won't work on attachments.
}
```

See llGetNumberOfPrims for more about counting prims and avatars.

#### Errata

If a script located in a child prim erroneously attempts to access link 0, it will get or set the property of the linkset's root prim.  This bug ([BUG-5049](https://jira.secondlife.com/browse/BUG-5049)) is preserved for broken legacy scripts.

## See Also

### Functions

- **llGetLinkNumber** — prim
- **llGetLinkNumberOfSides** — Returns the number of faces of the linked prim.
- **llSetPrimitiveParams** — Set many primitive parameters
- **llSetLinkPrimitiveParams** — Set parameters on other prims in linkset
- **llSetLinkPrimitiveParamsFast** — Set parameters on other prims in linkset without sleep
- llGetObjectDetails

### Articles

- **Limits** — SL limits and constrictions
- **Limits** — SL limits and constrictions
- Color in LSL
- Translucent Color
- Color in LSL
- Color in LSL
- Translucent Color

<!-- /wiki-source -->
