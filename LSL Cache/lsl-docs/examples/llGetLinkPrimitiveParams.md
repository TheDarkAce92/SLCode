---
name: "llGetLinkPrimitiveParams"
category: "example"
type: "example"
language: "LSL"
description: "These functions are very similar; the difference is the latter takes a link parameter, and does not cause the script to sleep."
wiki_url: "https://wiki.secondlife.com/wiki/LlGetLinkPrimitiveParams"
author: "Anylyn Hax"
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL

  GetPrimitiveParamsllGetPrimitiveParams

- 1 Summary

  - 1.1 llGetPrimitiveParams

  - 1.1.1 Caveats
  - 1.2 llGetLinkPrimitiveParams
- 2 Caveats
- 3 Examples
- 4 Useful Snippets
- 5 Notes

  - 5.1 Link Numbers

  - 5.1.1 Counting Prims & Avatars
  - 5.1.2 Errata
- 6 See Also

  - 6.1 Functions
  - 6.2 Articles
- 7 Deep Notes

  - 7.1 top_size Explained
  - 7.2 History
  - 7.3 Footnotes
  - 7.4 Signature

## Summary

Summary: llGetPrimitiveParams, llGetLinkPrimitiveParams

These functions are very similar; the difference is the latter takes a link parameter, and does not cause the script to sleep.

PRIM_* flags can be broken into three categories, face flags, prim flags, and object flags.

- Supplying a prim or object flag will return that flag's attributes.
- Face flags require the user to also supply a side parameter.

llGetPrimitiveParams

### llGetPrimitiveParams

 Function: list **llGetPrimitiveParams**( list params );

0.2

Forced Delay

10.0

Energy

Returns attribute values (a list) for the attributes requested in the params list.

• list

params

–

PRIM_* flags

If you are planning to use PRIM_LINK_TARGET consider using llGetLinkPrimitiveParams instead.

 Caveats

- This function causes the script to sleep for 0.2 seconds.
- link needs to be either an actual link number or a link constants that equate to a single prim, such as LINK_ROOT and LINK_THIS.

  - LINK_SET, LINK_ALL_CHILDREN and LINK_ALL_OTHERS will not work.

### llGetLinkPrimitiveParams

 Function: list **llGetLinkPrimitiveParams**( integer link, list params );

0.0

Forced Delay

10.0

Energy

Identical to llGetPrimitiveParams except that it acts on the prim specified by the link number given.Returns attribute values (a list) for the attributes requested in the params list for the link. • integer link – Link number (0: unlinked, 1: root prim, >1: child prims and seated avatars) or a `LINK_*` flag to get the parameters of • list params – PRIM_* flagsPRIM_* flags Flag Description LINK_ROOT 1 refers to the root prim in a multi-prim linked set[1] Flag Description LINK_THIS -4 refers to the prim the script is in Parameter Return Values Description [ PRIM_NAME ] 27 [ string name ] Name: llGetObjectName [ PRIM_DESC ] 28 [ string description ] Description: llGetObjectDesc [ PRIM_TYPE ] 9 [ integer flag ] + flag_parameters Gets the prim shape. [Would you like to know more?][Hide] flag Constants Additional Return Values PRIM_TYPE_BOX 0 [ integer hole_shape, vector cut, float hollow, vector twist, vector top_size, vector top_shear ] PRIM_TYPE_CYLINDER 1 [ integer hole_shape, vector cut, float hollow, vector twist, vector top_size, vector top_shear ] PRIM_TYPE_PRISM 2 [ integer hole_shape, vector cut, float hollow, vector twist, vector top_size, vector top_shear ] PRIM_TYPE_SPHERE 3 [ integer hole_shape, vector cut, float hollow, vector twist, vector dimple] PRIM_TYPE_TORUS 4 [ integer hole_shape, vector cut, float hollow, vector twist, vector hole_size, vector top_shear, vector advanced_cut, vector taper, float revolutions, float radius_offset, float skew ] PRIM_TYPE_TUBE 5 [ integer hole_shape, vector cut, float hollow, vector twist, vector hole_size, vector top_shear, vector advanced_cut, vector taper, float revolutions, float radius_offset, float skew ] PRIM_TYPE_RING 6 [ integer hole_shape, vector cut, float hollow, vector twist, vector hole_size, vector top_shear, vector advanced_cut, vector taper, float revolutions, float radius_offset, float skew ] PRIM_TYPE_SCULPT 7 [ string map, integer type ] Sculpted_Prims:_FAQ   hole_shape Flags Shape hole_shape Flags Shape PRIM_HOLE_DEFAULT 0x00 Default PRIM_HOLE_SQUARE 0x20 Square PRIM_HOLE_CIRCLE 0x10 Circle PRIM_HOLE_TRIANGLE 0x30 Triangle type Flags Style Description PRIM_SCULPT_TYPE_SPHERE 1 Sphere Converge top & bottom, stitch left side to right PRIM_SCULPT_TYPE_TORUS 2 Torus Stitch top to bottom, stitch left side to right PRIM_SCULPT_TYPE_PLANE 3 Plane No stitching or converging PRIM_SCULPT_TYPE_CYLINDER 4 Cylinder Stitch left side to right. PRIM_SCULPT_TYPE_MESH 5 Mesh model See: Mesh PRIM_SCULPT_FLAG_ZZZZZZZZ 63 PRIM_SCULPT_FLAG_ANIMESH 0x20 Animesh Read-only flag to query Animated mesh status. PRIM_SCULPT_FLAG_INVERT 0x40 Invert Render inside out (inverts the normals). PRIM_SCULPT_FLAG_MIRROR 0x80 Mirror Render an X axis mirror of the sculpty. [ PRIM_SLICE ] 35 [ vector slice ] Gets the prim's slice (a shape attribute). [ PRIM_PHYSICS_SHAPE_TYPE ] 30 [ integer type ] Gets the prim's physics shape type. type Flags V Description Notes PRIM_PHYSICS_SHAPE_PRIM 0 The visible shape of the prim determines its physics-shape default for all non-mesh prims PRIM_PHYSICS_SHAPE_CONVEX 2 Use the convex hull formulas for generating the prim's physics-shape default for all mesh prims PRIM_PHYSICS_SHAPE_NONE 1 The prim will not contribute to the object's physics-shape This cannot be applied to the root prim or avatars. This prim has no physics representation at all. Like phantom objects, it will not collide with avatars or other objects. Unlike phantom prims, it will also pass freely through the terrain when the parent object is physical. Like volume detect it doesn't collide with terrain. Unlike volume detect, it will not register collision events. [ PRIM_MATERIAL ] 2 [ integer material ] Gets the prim's material. The material determines the default collision sound, sprite, friction coefficient and restitution coefficient. material Flags Description Friction Restitution PRIM_MATERIAL_STONE 0 stone 0.8 0.4 PRIM_MATERIAL_METAL 1 metal 0.3 0.4 PRIM_MATERIAL_GLASS 2 glass 0.2 0.7 PRIM_MATERIAL_WOOD 3 wood 0.6 0.5 PRIM_MATERIAL_FLESH 4 flesh 0.9 0.3 PRIM_MATERIAL_PLASTIC 5 plastic 0.4 0.7 PRIM_MATERIAL_RUBBER 6 rubber 0.9 0.9 PRIM_MATERIAL_LIGHT 7 light, DEPRECATED: Looks the same as [ PRIM_FULLBRIGHT, ALL_SIDES, TRUE ]

0.6

0.5

[ PRIM_PHYSICS ]

3

[ integer boolean ]

Physics status llGetStatus

[ PRIM_TEMP_ON_REZ ]

4

[ integer boolean ]

Temporary attribute

[ PRIM_PHANTOM ]

5

[ integer boolean ]

Phantom status llGetStatus

[ PRIM_POSITION ]

6

[ vector position ]

Position, llGetPos

[ PRIM_POS_LOCAL ]

33

[ vector position ]

Local position, llGetLocalPos

[ PRIM_ROTATION ]

8

[ rotation rot ]

Global rotation, llGetRot

[ PRIM_ROT_LOCAL ]

29

[ rotation rot ]

Local rotation, llGetLocalRot

[ PRIM_SIZE ]

7

[ vector size ]

Size, llGetScale

[ PRIM_TEXTURE, integer face ]

17

[ string texture, vector repeats, vector offsets, float rotation_in_radians ]

Texture:
llGetTexture

Repeats:
llGetTextureScale

Offset:
llGetTextureOffset

Rotation:
llGetTextureRot

[ PRIM_RENDER_MATERIAL, integer face ]

49

[ string render_material ]

Material:
llGetRenderMaterial

[ PRIM_TEXT ]

26

[ string text, vector color, float alpha ]

Floating Text: NA

[ PRIM_COLOR, integer face ]

18

[ vector color, float alpha ]

Alpha:
llGetAlpha

Color:
llGetColor

[ PRIM_BUMP_SHINY, integer face ]

19

[ integer shiny, integer bump ]

shiny & bump Flags

Description

PRIM_SHINY_NONE

0

none

PRIM_SHINY_LOW

1

low

PRIM_SHINY_MEDIUM

2

medium

PRIM_SHINY_HIGH

3

high

PRIM_BUMP_NONE

0

none: no bump map

PRIM_BUMP_BRIGHT

1

brightness: generate from highlights

PRIM_BUMP_DARK

2

darkness: generate from lowlights

PRIM_BUMP_WOOD

3

woodgrain

PRIM_BUMP_BARK

4

bark

PRIM_BUMP_BRICKS

5

bricks

PRIM_BUMP_CHECKER

6

checker

PRIM_BUMP_CONCRETE

7

concrete

PRIM_BUMP_TILE

8

crustytile

PRIM_BUMP_STONE

9

cutstone: blocks

PRIM_BUMP_DISKS

10

discs: packed circles

PRIM_BUMP_GRAVEL

11

gravel

PRIM_BUMP_BLOBS

12

petridish: blobby amoeba like shapes

PRIM_BUMP_SIDING

13

siding

PRIM_BUMP_LARGETILE

14

stonetile

PRIM_BUMP_STUCCO

15

stucco

PRIM_BUMP_SUCTION

16

suction: rings

PRIM_BUMP_WEAVE

17

weave

[ PRIM_FULLBRIGHT, integer face ]

20

[ integer boolean ]

[ PRIM_FLEXIBLE ]

21

[ integer boolean, integer softness, float gravity, float friction, float wind, float tension, vector force ]

[ PRIM_TEXGEN, integer face ]

22

[ integer mode ]

mode Constants

Description

PRIM_TEXGEN_DEFAULT

0

The texture repeats units are in texture repeats per face.

PRIM_TEXGEN_PLANAR

1

The texture repeats units are in texture repeats per half meter. This is in contrast to the in-world editing tool, in which the planar texture scaling units are repeats per meter.

[ PRIM_POINT_LIGHT ]

23

[ integer boolean, vector linear_color, float intensity, float radius, float falloff ]

linear_color param accepts color in Linear space - use llsRGB2Linear to convert regular LSL color into Linear space.

[ PRIM_REFLECTION_PROBE ]

44

[ integer boolean, float ambiance, float clip_distance, integer flags ]

Gets the prim's reflection probe parameters.

type Flags

V

Description

Notes

PRIM_REFLECTION_PROBE_BOX

1

Determines if the reflection probe is a box or a sphere.

Unset by default (probe is a sphere)

PRIM_REFLECTION_PROBE_DYNAMIC

2

Determines if avatars are included by the probe for imaging.

Unset by default (probe does not image avatars). Imaging avatars in probes has a performance cost.

PRIM_REFLECTION_PROBE_MIRROR

4

Determines if objects intersecting the probe act as a mirror.

Unset by default (probe does not act as a mirror). Rendering mirrors has a performance cost.

[ PRIM_GLOW, integer face ]

25

[ float intensity ]

[ PRIM_OMEGA ]

32

[ vector axis, float spinrate, float gain ]

llTargetOmega

[ PRIM_NORMAL, integer face ]

37

[ string texture, vector repeats, vector offsets, float rotation_in_radians ]

[ PRIM_SPECULAR, integer face ]

36

[ string texture, vector repeats, vector offsets, float rotation_in_radians, vector color, integer glossiness integer environment ]

[ PRIM_ALPHA_MODE, integer face ]

38

[ integer alpha_mode, integer mask_cutoff ]

[ PRIM_LINK_TARGET, integer link_target ]

34

[]

Multiple llGetLinkPrimitiveParams calls.

[ PRIM_CAST_SHADOWS ]

24

[ integer boolean ]

**DEPRECATED**: Shadow casting for the primitive

[ PRIM_ALLOW_UNSIT ]

39

[ integer boolean ]

[ PRIM_SCRIPTED_SIT_ONLY ]

40

[ integer boolean ]

[ PRIM_SIT_TARGET ]

41

[ integer boolean , vector offset, rotation rot ]

Sit target, llSitTarget. The position can be ZERO_VECTOR.

[ PRIM_PROJECTOR ]

42

[ string texture, float fov, float focus, float ambiance ]

Light projector settings, the texture may be NULL_KEY. *(Write only, for now. See here)*

[ PRIM_CLICK_ACTION ]

43

[ integer action ]

sets the default action to take when a user clicks on this prim.

Flag

Description

Cursor

CLICK_ACTION_NONE

0

Performs the default action: when the prim is touched, touch events are triggered

CLICK_ACTION_TOUCH

0

When the prim is touched, touch events are triggered

CLICK_ACTION_SIT

1

When the prim is touched, the avatar sits upon it

CLICK_ACTION_BUY

2

When the prim is touched, the buy dialog is opened

CLICK_ACTION_PAY

3

When the prim is touched, the pay dialog is opened

CLICK_ACTION_OPEN

4

When the prim is touched, the object inventory dialog is opened

CLICK_ACTION_PLAY

5

Play or pause parcel media on touch

CLICK_ACTION_OPEN_MEDIA

6

Play parcel media on touch, no pause

CLICK_ACTION_ZOOM

7

Zoom the avatar camera on this object (Viewer 2)

CLICK_ACTION_DISABLED

8

No click action. No touches detected or passed.

CLICK_ACTION_IGNORE

9

Clicks go through the object to whatever is behind it. No touches detected.

[ PRIM_GLTF_BASE_COLOR, integer face ]

48

[ string texture, vector repeats, vector offsets, float rotation_in_radians, vector color, float alpha, integer gltf_alpha_mode, float alpha_mask_cutoff, integer double_sided ]

linear_color param accepts color in Linear space - use llsRGB2Linear to convert regular LSL color into Linear space.

This parameter's arguments are GLTF overrides.


      ⚠️
      **Warning:** Setting an argument to the empty string ("") will clear the respective override. **GLTF texture transforms are always overrides, so setting them to the empty string ("") will clear them.** See this example for a workaround. The SL team is [open to feedback](https://feedback.secondlife.com/) on LSL improvements for GLTF.


gltf_alpha_mode Flags

V

Description

PRIM_GLTF_ALPHA_MODE_OPAQUE

0

Ignore the alpha value and render the material as opaque.

PRIM_GLTF_ALPHA_MODE_BLEND

1

Render the material with transparency determined by the alpha value. Blending is done in linear color space. As is the case for Blinn-Phong as well, this mode suffers from depth sorting and performance issues. Use alpha mask instead when possible.

PRIM_GLTF_ALPHA_MODE_MASK

2

Render the material as  fully opaque where the alpha value is greater than the alpha cutoff, and otherwise render the material as fully transparent.

[ PRIM_GLTF_NORMAL, integer face ]

45

[ string texture, vector repeats, vector offsets, float rotation_in_radians ]

This parameter's arguments are GLTF overrides.


      ⚠️
      **Warning:** Setting an argument to the empty string ("") will clear the respective override. **GLTF texture transforms are always overrides, so setting them to the empty string ("") will clear them.** See this example for a workaround. The SL team is [open to feedback](https://feedback.secondlife.com/) on LSL improvements for GLTF.


[ PRIM_GLTF_METALLIC_ROUGHNESS, integer face ]

47

[ string texture, vector repeats, vector offsets, float rotation_in_radians, float metallic_factor, float roughness_factor ]

This parameter's arguments are GLTF overrides.


      ⚠️
      **Warning:** Setting an argument to the empty string ("") will clear the respective override. **GLTF texture transforms are always overrides, so setting them to the empty string ("") will clear them.** See this example for a workaround. The SL team is [open to feedback](https://feedback.secondlife.com/) on LSL improvements for GLTF.


[ PRIM_GLTF_EMISSIVE, integer face ]

46

[ string texture, vector repeats, vector offsets, float rotation_in_radians, vector emissive_tint ]

emissive_tint param accepts color in Linear space - use llsRGB2Linear to convert regular LSL color into Linear space.

This parameter's arguments are GLTF overrides.


      ⚠️
      **Warning:** Setting an argument to the empty string ("") will clear the respective override. **GLTF texture transforms are always overrides, so setting them to the empty string ("") will clear them.** See this example for a workaround. The SL team is [open to feedback](https://feedback.secondlife.com/) on LSL improvements for GLTF.


[ PRIM_SIT_FLAGS ]

50

[ integer flags ]

Gets the sit flags currently set on this prim.

Flag

Description

SIT_FLAG_SIT_TARGET

0x1

Read-only flag to indicate whether the link has a sit target.  Use llSitTarget, llLinkSitTarget, or PRIM_SIT_TARGET to disable or enable this flag. Use llGetLinkSitFlags, or llGetLinkPrimitiveParams with PRIM_SIT_FLAGS to read this flag.

SIT_FLAG_ALLOW_UNSIT

0x2

Allow an avatar to manually unsit from a sit target.  Only applies to agents who had been seated via an LSL script. See llSitOnLink.

SIT_FLAG_SCRIPTED_ONLY

0x4

Only allow scripted sits on this sit target.

SIT_FLAG_NO_COLLIDE

0x10

Disable the avatar's collision volume when they are seated on this sit target.

SIT_FLAG_NO_DAMAGE

0x20

Do not distribute damage to agents sitting on this sit target.

[ PRIM_DAMAGE ]

51

[ float damage, integer damage_type ]

Gets the damage and damage type delivered by a prim on collision.

[ PRIM_HEALTH ]

52

[ float health ]

Gets the health of a prim

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

## Useful Snippets

```lsl
list GetPrimitiveParams(list input)
{//Returns a list that can be fed to llSetPrimitiveParams
    integer link = LINK_THIS;
    list output;
    integer c = ~llGetListLength(input);
    while(0x80000000 & (c = - ~c))
    {
        integer f = llList2Integer(input, c);
        list flag = (list)f;
        if(~llListFindList([PRIM_BUMP_SHINY, PRIM_COLOR, PRIM_TEXTURE,
                            PRIM_FULLBRIGHT, PRIM_TEXGEN, PRIM_GLOW], flag ))
        {
            integer side = llList2Integer(input, (c = - ~c));
            if(~side)//pop the stack
                output += flag + side + llGetLinkPrimitiveParams(link, flag + side );
            else
                for(side = llGetLinkNumberOfSides(link); side; ) //we return the sides in reverse order, easier to code; runs faster.
                    output += flag + side + llGetLinkPrimitiveParams(link, flag + (side = ~ -side) );
        }
        else if(PRIM_LINK_TARGET ^ f)
            output += flag + (link = llList2Integer(input, (c = - ~c)));
        else
            output += flag + llGetLinkPrimitiveParams(link, flag );
    }
    return output;
}
//Contributed by Strife Onizuka
```

```lsl
list GetLinkPrimitiveParams(integer link, list input)
{//Returns a list that can be fed to llSetPrimitiveParams
    list output;
    integer c = ~llGetListLength(input);
    while(0x80000000 & (c = - ~c))
    {
        integer f = llList2Integer(input, c);
        list flag = (list)f;
        if(~llListFindList([PRIM_BUMP_SHINY, PRIM_COLOR, PRIM_TEXTURE,
                            PRIM_FULLBRIGHT, PRIM_TEXGEN, PRIM_GLOW], flag ))
        {
            integer side = llList2Integer(input, (c = - ~c));
            if(~side)//pop the stack
                output += flag + side + llGetLinkPrimitiveParams(link, flag + side );
            else
                for(side = llGetLinkNumberOfSides(link); side; ) //we return the sides in reverse order, easier to code; runs faster.
                    output += flag + side + llGetLinkPrimitiveParams(link, flag + (side = ~ -side) );
        }
        else if(PRIM_LINK_TARGET ^ f)
            output += flag + (link = llList2Integer(input, (c = - ~c)));
        else
            output += flag + llGetLinkPrimitiveParams(link, flag );
    }
    return output;
}
//Contributed by Strife Onizuka
```

SetPrimitiveParams-Example by Anylyn Hax makes reading primitive parameters easy.
SetPrimitiveParams-Example by Anylyn Hax makes reading primitive parameters easy.

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

•

llGetLinkNumber

–

Returns the link number of the prim the script is in.

•

llGetLinkNumberOfSides

–

Returns the number of faces of the linked prim.

•

llSetPrimitiveParams

–

Set many primitive parameters

•

llSetLinkPrimitiveParams

–

Set parameters on other prims in linkset

•

llSetLinkPrimitiveParamsFast

–

Set parameters on other prims in linkset without sleep

•

llGetObjectDetails

### Articles

•

Limits

–

SL limits and constrictions

•

Limits

–

SL limits and constrictions

•

Color in LSL

•

Translucent Color

•

Color in LSL

•

Color in LSL

•

Translucent Color

## Deep Notes

PRIM_TYPE top_size and client taper conversion

Range

Top
Tapered

No
Tapering

Bottom
Tapered

Client

[-1, 1]

1.0

0.0

-1.0

PRIM_TYPE

[0, 2]

0.0

1.0

2.0

LEGACY

[0, 1]

0.0

1.0

NA

Client < 1.11

[0, 1]

0.0

1.0

NA

#### top_size

When the original PRIM_TYPE interface was retired (PRIM_TYPE_LEGACY, [SL 1.5](http://secondlife.wikia.com/wiki/Version_1.5)), the new PRIM_TYPE interface did not yet support tapering of the bottom of the prim, this feature wasn't added until [SL 1.11](http://secondlife.wikia.com/wiki/Version_1.11) (two years later). Instead of retiring the new PRIM_TYPE when it was added, the range of top_size was enlarged; meanwhile in the client they redefined the parameter and it's values. This redefinition and range enlargement resulted in two interfaces that did the same thing but achieved it through different values. Meanwhile PRIM_TYPE_LEGACY's interface was not updated to support tapering of the bottom of the prim. Consequently all three interfaces have different ranges, making for a rather nasty caveat.

#### History

- Date of release llGetLinkPrimitiveParams 29-03-2010

#### Footnotes

1. **^** LINK_ROOT does not work on single prim objects. Unless there is an avatar sitting on the object.
1. **^** When LL deprecated this flag they stripped it of it's name, however they did not remove the functionality. To aid in documenting the functionality, the value was given a new name in the documentation only. That is why PRIM_TYPE_LEGACY is not recognized by the compiler.
1. **^** The pipe character historically has been used to separate fields in the serialized version of inventory and possibly other internal fields for prim parameters.
1. **^** Floating text with an alpha set to 0.0 is rendered "invisible"
1. **^** The ranges in this article are written in [Interval Notation](http://en.wikipedia.org/wiki/Interval_(mathematics)#Notations_for_intervals).
1. **^** llGetPrimitiveParams came after PRIM_TYPE_LEGACY was deprecated.

#### Signature

```lsl
function list llGetPrimitiveParams( list params );
function list llGetLinkPrimitiveParams( integer link, list params );
```