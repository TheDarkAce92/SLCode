---
name: "llSetLinkPrimitiveParamsFast"
category: "example"
type: "example"
language: "LSL"
description: "These functions are almost entirely identical. For almost all situations we recommend you use llSetLinkPrimitiveParamsFast."
wiki_url: "https://wiki.secondlife.com/wiki/LlSetLinkPrimitiveParamsFast"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL

  SetPrimitiveParamsllSetPrimitiveParams

- 1 Summary

  - 1.1 llSetPrimitiveParams
  - 1.2 llSetLinkPrimitiveParams
  - 1.3 llSetLinkPrimitiveParamsFast

  - 1.3.1 Caveats
- 2 Caveats
- 3 Examples

  - 3.1 Top-size (taper)
- 4 Useful Snippets
- 5 Notes

  - 5.1 Link Numbers

  - 5.1.1 Counting Prims & Avatars
  - 5.1.2 Errata
  - 5.2 PRIM_POSITION

  - 5.2.1 Examples
- 6 See Also

  - 6.1 Functions
  - 6.2 Articles
- 7 Deep Notes

  - 7.1 top_size Explained
  - 7.2 History
  - 7.3 Footnotes
  - 7.4 Signature

## Summary

Summary: llSetPrimitiveParams, llSetLinkPrimitiveParams, llSetLinkPrimitiveParamsFast

These functions are almost entirely identical. For almost all situations we recommend you use llSetLinkPrimitiveParamsFast.

These are very powerful & sharp functions. Each PRIM_* rule takes at least one parameter and has its own quirks and its own dedicated article with specific information.

There are two differences:

- How long does it force the script to sleep?
**Zero**: llSetLinkPrimitiveParamsFast
**200 milliseconds**: llSetPrimitiveParams llSetLinkPrimitiveParams
- Does it have a link parameter?
**No**: llSetPrimitiveParams
**Yes**: llSetLinkPrimitiveParams llSetLinkPrimitiveParamsFast

llSetPrimitiveParams

### llSetPrimitiveParams

 Function:  **llSetPrimitiveParams**( list rules );

0.2

Forced Delay

10.0

Energy

Sets the prim's parameters according to rules.

• list

rules

Please consider using llSetLinkPrimitiveParamsFast in combination with LINK_THIS instead. You avoid the 0.2 second delay.

Although it might not seem obvious you actually can set link rules using this function in combination with PRIM_LINK_TARGET, however **for your own sake** please use llSetLinkPrimitiveParams or llSetLinkPrimitiveParamsFast instead.

### llSetLinkPrimitiveParams

 Function:  **llSetLinkPrimitiveParams**( integer link, list rules );

0.2

Forced Delay

10.0

Energy

Sets the prims parameters according to rules.

• integer

link

–

Link number (0: unlinked, 1: root prim, >1: child prims and seated avatars) or a `LINK_*` flag

• list

rules

Please consider using llSetLinkPrimitiveParamsFast instead. You avoid the 0.2 second delay.

### llSetLinkPrimitiveParamsFast

 Function:  **llSetLinkPrimitiveParamsFast**( integer link, list rules );

0.0

Forced Delay

10.0

Energy

Sets the prims parameters according to rules.

• integer

link

–

Link number (0: unlinked, 1: root prim, >1: child prims and seated avatars) or a `LINK_*` flag

• list

rules

This function is fast compared to the above variations, not other LSL functions.
 Caveats

- Sometimes llSetLinkPrimitiveParamsFast is *too fast*, i.e. the function returns and the next line of code executes & returns before the update has been processed, resulting in the updates being out of order. In most situations, there is no difference in behavior but sometimes there is. In those cases, you need to use llSetPrimitiveParams or llSetLinkPrimitiveParams.

  - This occurs because the llSetLinkPrimitiveParamsFast payload is being executed asynchronously, while llSetPrimitiveParams and llSetLinkPrimitiveParams payloads are executed synchronously (or the delay makes it appear synchronous).

Flag

Description

LINK_ROOT

1

refers to the root prim in a multi-prim linked set

LINK_SET

-1

refers to all prims

LINK_ALL_OTHERS

-2

refers to all other prims

Flag

Description

LINK_ALL_CHILDREN

-3

refers to all children, (everything but the root)

LINK_THIS

-4

refers to the prim the script is in

Flag

V

Description

Usage

PRIM_NAME

27

Sets the prim's name.

[ PRIM_NAME, string name ]

PRIM_DESC

28

Sets the prim's description.

[ PRIM_DESC, string description ]

PRIM_TYPE

9

Sets the prim's shape.

[ PRIM_TYPE, integer flag ] + flag_parameters

PRIM_SLICE

35

Sets the prim's slice (a shape attribute).

[ PRIM_SLICE, vector slice ]

PRIM_PHYSICS_SHAPE_TYPE

30

Sets the prim's physics shape type.

[ PRIM_PHYSICS_SHAPE_TYPE, integer type ]

PRIM_MATERIAL

2

Sets the prim's material.

[ PRIM_MATERIAL, integer flag ]

PRIM_PHYSICS

3

Sets the object's physics status.

[ PRIM_PHYSICS, integer boolean ]

PRIM_TEMP_ON_REZ

4

Sets the object's temporary attribute.

[ PRIM_TEMP_ON_REZ, integer boolean ]

PRIM_PHANTOM

5

Sets the object's phantom status.

[ PRIM_PHANTOM, integer boolean ]

PRIM_POSITION

6

Sets the prim's position.

[ PRIM_POSITION, vector position ]

PRIM_POS_LOCAL

33

Sets the prim's local position.

[ PRIM_POS_LOCAL, vector position ]

PRIM_ROTATION

8

Sets the prim's global rotation.

[ PRIM_ROTATION, rotation rot ]

PRIM_ROT_LOCAL

29

Sets the prim's local rotation.

[ PRIM_ROT_LOCAL, rotation rot ]

PRIM_SIZE

7

Sets the prim's size.

[ PRIM_SIZE, vector size ]

PRIM_TEXTURE

17

Sets the prim's texture attributes.

[ PRIM_TEXTURE, integer face, string texture, vector repeats, vector offsets, float rotation_in_radians ]

PRIM_RENDER_MATERIAL

49

Sets the prim's render_material. Setting this param will also clear most PRIM_GLTF_* properties on the face, with the exceptions of repeats, offsets, and rotation_in_radians

[ PRIM_RENDER_MATERIAL, integer face, string render_material ]

PRIM_TEXT

26

Sets the prim's floating text.

[ PRIM_TEXT, string text, vector color, float alpha ]

PRIM_COLOR

18

Sets the face's color.

[ PRIM_COLOR, integer face, vector color, float alpha ]

PRIM_BUMP_SHINY

19

Sets the face's shiny & bump.

[ PRIM_BUMP_SHINY, integer face, integer shiny, integer bump ]

PRIM_POINT_LIGHT

23

Sets the prim as a point light.

[ PRIM_POINT_LIGHT, integer boolean, vector linear_color, float intensity, float radius, float falloff ]

PRIM_REFLECTION_PROBE

44

Sets the prim as a reflection probe.

[ PRIM_REFLECTION_PROBE, integer boolean, float ambiance, float clip_distance, integer flags ]

PRIM_FULLBRIGHT

20

Sets the face's full bright flag.

[ PRIM_FULLBRIGHT, integer face, integer boolean ]

PRIM_FLEXIBLE

21

Sets the prim as flexible.

[ PRIM_FLEXIBLE, integer boolean, integer softness, float gravity, float friction, float wind, float tension, vector force ]

PRIM_TEXGEN

22

Sets the face's texture mode.

[ PRIM_TEXGEN, integer face, integer type ]

PRIM_GLOW

25

Sets the face's glow attribute.

[ PRIM_GLOW, integer face, float intensity ]

PRIM_OMEGA

32

Sets the prim's spin to the specified axis and rate.

[ PRIM_OMEGA, vector axis, float spinrate, float gain ]

PRIM_NORMAL

37

Sets the prim's normal map attributes.

[ PRIM_NORMAL, integer face, string texture, vector repeats, vector offsets, float rotation_in_radians ]

PRIM_SPECULAR

36

Sets the prim's specular map attributes.

[ PRIM_SPECULAR, integer face, string texture, vector repeats, vector offsets, float rotation_in_radians, vector color, integer glossiness, integer environment ]

PRIM_ALPHA_MODE

38

Sets the prim's diffuse texture alpha rendering mode attributes.

[ PRIM_ALPHA_MODE, integer face, integer alpha_mode, integer mask_cutoff ]

PRIM_LINK_TARGET

34

Sets the next linknumber to use in the linkset.

[ PRIM_LINK_TARGET, integer link_target ]

PRIM_CAST_SHADOWS

24

Sets the prim's cast shadow attribute. (**DEPRECATED**)

[ PRIM_CAST_SHADOWS, integer boolean ]

PRIM_TYPE_LEGACY

1

Sets the prim's shape  (legacy mode, **DEPRECATED**).

[ 1, integer flag ] + flag_parameters

PRIM_ALLOW_UNSIT

39

Avatars are allowed to manually stand up when seated on this prim.  Only valid for prims in a valid experience.

[ PRIM_ALLOW_UNSIT, integer boolean ]

PRIM_SCRIPTED_SIT_ONLY

40

Avatars are not permitted to manually sit on this prim.

[ PRIM_SCRIPTED_SIT_ONLY, integer boolean ]

PRIM_SIT_TARGET

41

The sit target, if any defined for this prim.

[ PRIM_SIT_TARGET, integer boolean, vector offset, rotation rot ]

PRIM_PROJECTOR

42

Light projector settings for this prim.

[ PRIM_PROJECTOR, string texture, float fov, float focus, float ambiance ]

PRIM_CLICK_ACTION

43

Click action for this prim

[ PRIM_CLICK_ACTION, integer action ]

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

CLICK_ACTION_BUY 2 When the prim is touched, the buy dialog is opened CLICK_ACTION_PAY 3 When the prim is touched, the pay dialog is opened CLICK_ACTION_OPEN 4 When the prim is touched, the object inventory dialog is opened CLICK_ACTION_PLAY 5 Play or pause parcel media on touch CLICK_ACTION_OPEN_MEDIA 6 Play parcel media on touch, no pause CLICK_ACTION_ZOOM 7 Zoom the avatar camera on this object (Viewer 2) CLICK_ACTION_DISABLED 8 No click action. No touches detected or passed. CLICK_ACTION_IGNORE 9 Clicks go through the object to whatever is behind it. No touches detected. PRIM_GLTF_BASE_COLOR 48 Sets the prim's GLTF Material Base Color map attributes. This parameter's arguments are GLTF overrides. ⚠️ **Warning:** Setting an argument to the empty string ("") will clear the respective override. **GLTF texture transforms are always overrides, so setting them to the empty string ("") will clear them.** See this example for a workaround. The SL team is open to feedback on LSL improvements for GLTF. gltf_alpha_mode Flags V Description PRIM_GLTF_ALPHA_MODE_OPAQUE 0 Ignore the alpha value and render the material as opaque. PRIM_GLTF_ALPHA_MODE_BLEND 1 Render the material with transparency determined by the alpha value. Blending is done in linear color space. As is the case for Blinn-Phong as well, this mode suffers from depth sorting and performance issues. Use alpha mask instead when possible. PRIM_GLTF_ALPHA_MODE_MASK 2 Render the material as fully opaque where the alpha value is greater than the alpha cutoff, and otherwise render the material as fully transparent. [ PRIM_GLTF_BASE_COLOR, integer face, string texture, vector repeats, vector offsets, float rotation_in_radians, vector linear_color, float alpha, integer gltf_alpha_mode, float alpha_mask_cutoff, integer double_sided ] PRIM_GLTF_NORMAL 45 Sets the prim's GLTF Material Normal map attributes. This parameter's arguments are GLTF overrides. ⚠️ **Warning:** Setting an argument to the empty string ("") will clear the respective override. **GLTF texture transforms are always overrides, so setting them to the empty string ("") will clear them.** See this example for a workaround. The SL team is open to feedback on LSL improvements for GLTF. [ PRIM_GLTF_NORMAL, integer face, string texture, vector repeats, vector offsets, float rotation_in_radians ] PRIM_GLTF_METALLIC_ROUGHNESS 47 Sets the prim's GLTF ORM map attributes (Occlusion, Roughness, Metallic). This parameter's arguments are GLTF overrides. ⚠️ **Warning:** Setting an argument to the empty string ("") will clear the respective override. **GLTF texture transforms are always overrides, so setting them to the empty string ("") will clear them.** See this example for a workaround. The SL team is open to feedback on LSL improvements for GLTF. [ PRIM_GLTF_METALLIC_ROUGHNESS, integer face, string texture, vector repeats, vector offsets, float rotation_in_radians, float metallic_factor, float roughness_factor ] PRIM_GLTF_EMISSIVE 46 Sets the prim's GLTF Material Emissive map attributes. This parameter's arguments are GLTF overrides. ⚠️ **Warning:** Setting an argument to the empty string ("") will clear the respective override. **GLTF texture transforms are always overrides, so setting them to the empty string ("") will clear them.** See this example for a workaround. The SL team is open to feedback on LSL improvements for GLTF. [ PRIM_GLTF_EMISSIVE, integer face, string texture, vector repeats, vector offsets, float rotation_in_radians, vector linear_emissive_tint ] PRIM_SIT_FLAGS 50 Sets the flags on the prim's sit target Flag Description SIT_FLAG_SIT_TARGET 0x1 Read-only flag to indicate whether the link has a sit target. Use llSitTarget, llLinkSitTarget, or PRIM_SIT_TARGET to disable or enable this flag. Use llGetLinkSitFlags, or llGetLinkPrimitiveParams with PRIM_SIT_FLAGS to read this flag. SIT_FLAG_ALLOW_UNSIT 0x2 Allow an avatar to manually unsit from a sit target. Only applies to agents who had been seated via an LSL script. See llSitOnLink. SIT_FLAG_SCRIPTED_ONLY 0x4 Only allow scripted sits on this sit target. SIT_FLAG_NO_COLLIDE 0x10 Disable the avatar's collision volume when they are seated on this sit target. SIT_FLAG_NO_DAMAGE 0x20 Do not distribute damage to agents sitting on this sit target. [ PRIM_SIT_FLAGS, integer flags ] PRIM_DAMAGE 51 Sets the damage and damage type delivered by a prim on collision. [ PRIM_DAMAGE, float damage, integer damage_type ] PRIM_HEALTH 52 Sets the health value for this prim. [ PRIM_HEALTH, float health ] Parameter Additional Parameters Description [ PRIM_NAME ] 27 [ string name ] Name: llSetObjectName [ PRIM_DESC ] 28 [ string description ] Description: llSetObjectDesc [ PRIM_TYPE ] 9 [ integer flag ] + flag_parameters Sets the prim shape. [Would you like to know more?][Hide] flag Constants Flag Parameters PRIM_TYPE_BOX 0 [ integer hole_shape, vector cut, float hollow, vector twist, vector top_size, vector top_shear ] PRIM_TYPE_CYLINDER 1 [ integer hole_shape, vector cut, float hollow, vector twist, vector top_size, vector top_shear ] PRIM_TYPE_PRISM 2 [ integer hole_shape, vector cut, float hollow, vector twist, vector top_size, vector top_shear ] PRIM_TYPE_SPHERE 3 [ integer hole_shape, vector cut, float hollow, vector twist, vector dimple] PRIM_TYPE_TORUS 4 [ integer hole_shape, vector cut, float hollow, vector twist, vector hole_size, vector top_shear, vector advanced_cut, vector taper, float revolutions, float radius_offset, float skew ] PRIM_TYPE_TUBE 5 [ integer hole_shape, vector cut, float hollow, vector twist, vector hole_size, vector top_shear, vector advanced_cut, vector taper, float revolutions, float radius_offset, float skew ] PRIM_TYPE_RING 6 [ integer hole_shape, vector cut, float hollow, vector twist, vector hole_size, vector top_shear, vector advanced_cut, vector taper, float revolutions, float radius_offset, float skew ] PRIM_TYPE_SCULPT 7 [ string map, integer type ] Sculpted_Prims:_FAQ   hole_shape Flags Shape hole_shape Flags Shape PRIM_HOLE_DEFAULT 0x00 Default PRIM_HOLE_SQUARE 0x20 Square PRIM_HOLE_CIRCLE 0x10 Circle PRIM_HOLE_TRIANGLE 0x30 Triangle type Flags Style Description PRIM_SCULPT_TYPE_SPHERE 1 Sphere Converge top & bottom, stitch left side to right PRIM_SCULPT_TYPE_TORUS 2 Torus Stitch top to bottom, stitch left side to right PRIM_SCULPT_TYPE_PLANE 3 Plane No stitching or converging PRIM_SCULPT_TYPE_CYLINDER 4 Cylinder Stitch left side to right. PRIM_SCULPT_TYPE_MESH 5 Mesh model See: Mesh PRIM_SCULPT_FLAG_ZZZZZZZZ 63 PRIM_SCULPT_FLAG_ANIMESH 0x20 Animesh Read-only flag to query Animated mesh status. PRIM_SCULPT_FLAG_INVERT 0x40 Invert Render inside out (inverts the normals). PRIM_SCULPT_FLAG_MIRROR 0x80 Mirror Render an X axis mirror of the sculpty. [ PRIM_SLICE ] 35 [ vector slice ] Sets the prim's slice (a shape attribute). [ PRIM_PHYSICS_SHAPE_TYPE ] 30 [ integer type ] Sets the prim's physics shape type. type Flags V Description Notes PRIM_PHYSICS_SHAPE_PRIM 0 The visible shape of the prim determines its physics-shape default for all non-mesh prims PRIM_PHYSICS_SHAPE_CONVEX 2 Use the convex hull formulas for generating the prim's physics-shape default for all mesh prims PRIM_PHYSICS_SHAPE_NONE 1 The prim will not contribute to the object's physics-shape This cannot be applied to the root prim or avatars. This prim has no physics representation at all. Like phantom objects, it will not collide with avatars or other objects. *Unlike* phantom prims, it will also pass freely through the terrain when the parent object is physical. Like volume detect it doesn't collide with terrain. *Unlike* volume detect, it will not register collision events.

[ PRIM_MATERIAL ]

2

[ integer material ]

Sets the prim's material. The material determines the default collision sound, sprite, friction coefficient and restitution coefficient.

material Flags

Description

Friction

Restitution

PRIM_MATERIAL_STONE

0

stone

0.8

0.4

PRIM_MATERIAL_METAL

1

metal

0.3

0.4

PRIM_MATERIAL_GLASS

2

glass

0.2

0.7

PRIM_MATERIAL_WOOD

3

wood

0.6

0.5

PRIM_MATERIAL_FLESH

4

flesh

0.9

0.3

PRIM_MATERIAL_PLASTIC

5

plastic

0.4

0.7

PRIM_MATERIAL_RUBBER

6

rubber

0.9

0.9

PRIM_MATERIAL_LIGHT

7

light, **DEPRECATED**: Looks the same as [ PRIM_FULLBRIGHT, ALL_SIDES, TRUE ]

0.6

0.5

[ PRIM_PHYSICS ]

3

[ integer boolean ]

Physics status llSetStatus

[ PRIM_TEMP_ON_REZ ]

4

[ integer boolean ]

Temporary attribute

[ PRIM_PHANTOM ]

5

[ integer boolean ]

Phantom status llSetStatus

[ PRIM_POSITION ]

6

[ vector position ]

Position, llSetPos

[ PRIM_POS_LOCAL ]

33

[ vector position ]

Local position, llSetPos

[ PRIM_ROTATION ]

8

[ rotation rot ]

Global rotation, llSetRot (broken for child prims)

[ PRIM_ROT_LOCAL ]

29

[ rotation rot ]

Local rotation, llSetLocalRot

[ PRIM_SIZE ]

7

[ vector size ]

Size, llSetScale

[ PRIM_TEXTURE, integer face ]

17

[ string texture, vector repeats, vector offsets, float rotation_in_radians ]

Texture:

llSetTexture

Repeats:

llScaleTexture

Offset:

llOffsetTexture

Rotation:

llRotateTexture

[ PRIM_RENDER_MATERIAL, integer face ]

49

[ string render_material ]

Material:

llSetRenderMaterial

[ PRIM_TEXT ]

26

[ string text, vector color, float alpha ]

Floating Text: llSetText

[ PRIM_COLOR, integer face ]

18

[ vector color, float alpha ]

Alpha:

llSetAlpha

Color:

llSetColor

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

Sets the prim's reflection probe parameters.

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

Multiple llSetLinkPrimitiveParams calls.

[ PRIM_CAST_SHADOWS ]

24

[ integer boolean ]

**DEPRECATED**: Shadow casting for the primitive

[ 1 ]PRIM_TYPE_LEGACY[2] 1 [ integer flag] + flag_parameters flag Constants Flag Parameters PRIM_TYPE_BOX 0 [ vector cut, float hollow, float twist_end, vector top_size, vector top_shear ] PRIM_TYPE_CYLINDER 1 [ vector cut, float hollow, float twist_end, vector top_size, vector top_shear ] PRIM_TYPE_PRISM 2 [ vector cut, float hollow, float twist_end, vector top_size, vector top_shear ] PRIM_TYPE_SPHERE 3 [ vector cut, float hollow, vector dimple ] PRIM_TYPE_TORUS 4 [ vector cut, float hollow, float twist_end, float hole_size_y, vector top_shear, vector advanced_cut ] PRIM_TYPE_TUBE 5 [ vector cut, float hollow, float twist_end, float topshear_x ] [ PRIM_ALLOW_UNSIT ] 39 [ integer boolean ] [ PRIM_SCRIPTED_SIT_ONLY ] 40 [ integer boolean ] [ PRIM_SIT_TARGET ] 41 [ integer boolean , vector offset, rotation rot ] Sit target, llSitTarget. The position can be ZERO_VECTOR. [ PRIM_PROJECTOR ] 42 [ string texture, float fov, float focus, float ambiance ] Light projector settings, the texture may be NULL_KEY. (Write only, for now. See here) [ PRIM_CLICK_ACTION ] 43 [ integer action ] sets the default action to take when a user clicks on this prim. Flag Description Cursor CLICK_ACTION_NONE 0 Performs the default action: when the prim is touched, touch events are triggered CLICK_ACTION_TOUCH 0 When the prim is touched, touch events are triggered CLICK_ACTION_SIT 1 When the prim is touched, the avatar sits upon it CLICK_ACTION_BUY 2 When the prim is touched, the buy dialog is opened CLICK_ACTION_PAY 3 When the prim is touched, the pay dialog is opened CLICK_ACTION_OPEN 4 When the prim is touched, the object inventory dialog is opened CLICK_ACTION_PLAY 5 Play or pause parcel media on touch CLICK_ACTION_OPEN_MEDIA 6 Play parcel media on touch, no pause CLICK_ACTION_ZOOM 7 Zoom the avatar camera on this object (Viewer 2) CLICK_ACTION_DISABLED 8 No click action. No touches detected or passed. CLICK_ACTION_IGNORE 9 Clicks go through the object to whatever is behind it. No touches detected. [ PRIM_GLTF_BASE_COLOR, integer face ] 48 [ string texture, vector repeats, vector offsets, float rotation_in_radians, vector color, float alpha, integer gltf_alpha_mode, float alpha_mask_cutoff, integer double_sided ] linear_color param accepts color in Linear space - use llsRGB2Linear to convert regular LSL color into Linear space. This parameter's arguments are GLTF overrides. ⚠️ Warning: Setting an argument to the empty string ("") will clear the respective override. **GLTF texture transforms are always overrides, so setting them to the empty string ("") will clear them.** See this example for a workaround. The SL team is [open to feedback](https://feedback.secondlife.com/) on LSL improvements for GLTF.


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
- If texture is missing from the prim's inventory  and it is not a UUID or it is not a texture then an error is shouted on DEBUG_CHANNEL.
- If texture is a UUID then there are no new asset permissions consequences for the object.

  - The resulting object develops no new usage restrictions that might have occurred if the asset had been placed in the prims inventory.
- repeats is not only used to set the number of repeats but the sign of the individual components is also used to set the "Flip" attribute.
- In the default texture mapping mode the texture repeats units are in texture repeats per face. In the planar texture mapping mode the texture repeats units are in texture repeats per half meter. This is in contrast to the in-world editing tool, in which the planar texture scaling units are repeats per meter.
- If render_material is missing from the prim's inventory  and it is not a UUID or it is not a material then an error is shouted on DEBUG_CHANNEL.
- If render_material is a UUID then there are no new asset permissions consequences for the object.

  - The resulting object develops no new usage restrictions that might have occurred if the asset had been placed in the prims inventory.
- If render_material is provided as NULL_KEY, the glTF Material is removed from face, reverting back to any underlying Blinn-Phong materials.
- In the default texture mapping mode the texture repeats units are in texture repeats per face. In the planar texture mapping mode the texture repeats units are in texture repeats per half meter. This is in contrast to the in-world editing tool, in which the planar texture scaling units are repeats per meter.
- Do not rely on Floating Text as a storage medium; it is neither secure nor finalized.

  - Floating text has been altered in past server updates, breaking existing content; future changes may occur.
  - Even "invisible" floating text is transmitted to the client.

  - It can be viewed by anyone with a client that is capable of rendering text that is supposed to be invisible.
  - The network packets that contain the text can be sniffed and the text read.
- PRIM_TYPE can only be used with LINK_SET if the object contains 10 or fewer prims. It can only be used with LINK_ALL_OTHERS or LINK_ALL_CHILDREN if the object contains 11 or fewer prims. If there are more prims, the operation will fail and an error will be shouted to DEBUG_CHANNEL. Work around this by looping through the prims with llSetLinkPrimitiveParamsFast.
- PRIM_TYPE will silently fail when executed by a script placed inside a mesh, whether the affect object is the mesh or not (in linksets for example), use a normal prim as your root prim.
- top_size and client values are different, the ranges do not line up, conversion is required. This simple equation can be used: answer = 1.0 - value. See top_size Explained for more information.
- PRIM_POSITION caveats

  - Depending upon the situation position may need to be in local coordinates or region coordinates, See llSetPos#Specification for details.

  - It is usually not a good idea to combine PRIM_POSITION with LINK_SET. The root will treat the coordinates as world or attachment, while the children will treat them as local, yielding inconsistent results or failure. If you want to move the object as a unit, use LINK_ROOT instead.
  - The range the prim can move is limited if it is an unattached root prim. The distance is capped to 10m per PRIM_POSITION call. See WarpPos. This is a very special case. Do not rely on rule duplication of other flags - the results are undefined, and things *will* break in the future.
  - Moving avatars with PRIM_POSITION

  - Moving the prim the avatar sat upon does not move the avatar.
  - Moving an avatar does not move the prim they sat upon.
  - Sit-target coordinates do not easily map to prim coordinates, use UpdateSitTarget.
  - If you have explicitally set your object as "static obstacle" for pathfinding , the function will fail with the error in the debug channel : "Unable to set prim position or scale: object contributes to the navmesh."
  - If position is greater than 54 meters away from the center, the repositioning will silently fail.
- PRIM_OMEGA on nonphysical objects, and child prims of physical objects, is only a client side effect; the object or prim will collide as non-moving geometry.
- PRIM_OMEGA cannot be used on avatars sitting on the object. It will emit the error message "PRIM_OMEGA disallowed on agent".
- If PRIM_OMEGA does not appear to be working, make sure that that Develop > Network > Velocity Interpolate Objects is enabled on the viewer.
- In the parameters returned by `llGetPrimitiveParams([PRIM_OMEGA])`, the vector is normalized, and the spinrate is multiplied by the magnitude of the original vector.
- If texture is missing from the prim's inventory  and it is not a UUID or it is not a texture then an error is shouted on DEBUG_CHANNEL.
- If texture is a UUID then there are no new asset permissions consequences for the object.

  - The resulting object develops no new usage restrictions that might have occurred if the asset had been placed in the prims inventory.
- repeats is not only used to set the number of repeats but the sign of the individual components is also used to set the "Flip" attribute.
- offsets and rotation_in_radians are limited to positive values only, unlike PRIM_TEXTURE and GLTF Overrides. To convert a negative offset to positive, add 1, and to convert a negative rotation to positive, add TWO_PI.
- To clear the normal map parameters from the face (and possibly remove the material), set  texture to NULL_KEY (the other parameters must be supplied in this case but will be ignored).
- Note that whenever any face in a linkset contains a material (i.e. has a non-default PRIM_NORMAL, PRIM_SPECULAR, or PRIM_ALPHA_MODE), the linkset will use the [new accounting system](http://community.secondlife.com/t5/English-Knowledge-Base/Calculating-land-impact/ta-p/974163).
- In the default texture mapping mode the texture repeats units are in texture repeats per face. In the planar texture mapping mode the texture repeats units are in texture repeats per half meter. This is in contrast to the in-world editing tool, in which the planar texture scaling units are repeats per meter.
- If texture is missing from the prim's inventory  and it is not a UUID or it is not a texture then an error is shouted on DEBUG_CHANNEL.
- If texture is a UUID then there are no new asset permissions consequences for the object.

  - The resulting object develops no new usage restrictions that might have occurred if the asset had been placed in the prims inventory.
- repeats is not only used to set the number of repeats but the sign of the individual components is also used to set the "Flip" attribute.
- offsets and rotation_in_radians are limited to positive values only, unlike PRIM_TEXTURE and GLTF Overrides. To convert a negative offset to positive, add 1, and to convert a negative rotation to positive, add TWO_PI.
- To clear the specular map parameters from the face (and possibly remove the material), set  texture to NULL_KEY (the other parameters must be supplied in this case but will be ignored).
- Note that whenever any face in a linkset contains a material (i.e. has a non-default PRIM_NORMAL, PRIM_SPECULAR, or PRIM_ALPHA_MODE), the linkset will use the [new accounting system](http://community.secondlife.com/t5/English-Knowledge-Base/Calculating-land-impact/ta-p/974163).
- In the default texture mapping mode the texture repeats units are in texture repeats per face. In the planar texture mapping mode the texture repeats units are in texture repeats per half meter. This is in contrast to the in-world editing tool, in which the planar texture scaling units are repeats per meter.
- If face is ALL_SIDES then the flag works on all sides.
- The flag silently fails if its face value indicates a face that does not exist.
- PRIM_SIZE has similar constraints to llSetScale and fails silently on physical prims/links. One workaround is to set items to non-physical before changing their size, then changing them back to physical; this can be accomplished in a single llSetLinkPrimitiveParamsFast command using PRIM_LINK_TARGET.
- PRIM_PHANTOM, PRIM_PHYSICS and PRIM_TEMP_ON_REZ applies to the entire object (linkset).
- Values may drift, become truncated or be range-limited. Some limits are applied by the client during deserialization and before rendering, others are applied by the simulator before storing the values.

  - When testing vectors and rotations use llVecDist and llAngleBetween (respectively) to perform fuzzy tests.
- PRIM_LINK_TARGET is a special parameter which can be inserted to perform actions on multiple prims on the linkset with one call.
- Scripts written before September 2004 that use PRIM_TYPE depend on PRIM_TYPE to have the value 1; if these scripts are recompiled, the new value of PRIM_TYPE will be used, causing errors at runtime.

  - To fix this, replace the PRIM_TYPE flag with the value 1 or update to the newer PRIM_TYPE syntax.
- PRIM_ROTATION is bugged in child prims. See Useful Snippets for a workaround, or the linked SVC-93 issue below.
- This function will return an error if given data of the wrong type. This is problematic when providing data from user input or notecard. To remedy this, see List Cast function.
- Applying an operation to LINK_SET will apply it first to the root prim, then to each child prim.
- The sim will clamp attributes before storing them.
- The client will clamp attributes before rendering.
- **Some prim properties are reset** by this function

  - A flexible prim will become not flexible
  - A sliced prim will become unsliced

In order to preserve properties they must be saved and explicitly set in the function call



      **Important:** When wanting to change the alpha value of a face, please consider using llSetLinkAlpha(integer link, float alpha, integer face); instead of llSetLinkPrimitiveParamsFast(integer link, [ PRIM_COLOR, integer face, vector color, float alpha ]);, that way you don't have to mess with the color settings. Also don't expect llSetLinkPrimitiveParamsFast being faster than llSetText when setting a float text property within a loop like at "% loading" status bars. Measurements showed llSetText being 3-4 times faster. That also might applies for similar functions.


- Attempting to change PRIM_TYPE of a mesh object has no effect.

  - Keeping the PRIM_TYPE as PRIM_TYPE_SCULPT and trying to set a different sculpt map or sculpt flags on a mesh also does nothing. Additionally, a script residing inside a mesh type prim cannot change the sculpt parameters of *any* prim in the linkset.
- The caveats described at |llSetClickAction all apply to PRIM_CLICK_ACTION.

## Examples

A simple script to light up a prim in a linkset when touched, and unlight the others using llSetLinkPrimitiveParams, when script is installed in the root prim of the linkset.

```lsl
// Turn all prims off and the one touched turn on

default
{
    touch_start(integer num_detected)
    {
        llSetLinkPrimitiveParamsFast(LINK_SET, [
                PRIM_FULLBRIGHT, ALL_SIDES, FALSE,
            PRIM_LINK_TARGET, llDetectedLinkNumber(0),
                PRIM_FULLBRIGHT, ALL_SIDES, TRUE]);
    }
}
```

A simple script which moves all child prims .25m forward on the root's Z axis, when touched.

```lsl
default
{
    touch_start(integer total_number)
    {
        integer numberOfPrims = llGetNumberOfPrims();

        if (numberOfPrims < 2) return;

        vector  link_pos;
        list    params;

        integer link = 2;// start with first child prim
        do
        {
//          get a child prim's local position (i.e, relative to the root prim)
            link_pos = llList2Vector(llGetLinkPrimitiveParams(link, [PRIM_POS_LOCAL]), 0);

            link_pos.z += 0.25;// relative to root's local z-axis !!!

            params += [PRIM_LINK_TARGET, link,
                            PRIM_POS_LOCAL, link_pos];
        }
        while (++link <= numberOfPrims);

        if (!llGetListLength(params)) return;

//      the params list starts with a PRIM_LINK_TARGET (a hack so we can start
//      with the first child prim), so it doesn't really matter which number you
//      put as first parameter in this function call
        llSetLinkPrimitiveParamsFast(2, params);
    }
}
```



      **Important:** You can use one function call instead of two when making use of PRIM_LINK_TARGET.


**Preferred method using PRIM_LINK_TARGET**

**Second method does the same effect-wise.**

```lsl
//  color the root prim red and the first linked-prim green

default
{
    touch_start(integer num_detected)
    {
        llSetLinkPrimitiveParamsFast(LINK_ROOT, [
                PRIM_COLOR, ALL_SIDES, <1.0, 0.0, 0.0>, 1.0,
            PRIM_LINK_TARGET, 2,
                PRIM_COLOR, ALL_SIDES, <0.0, 1.0, 0.0>, 1.0]);
    }
}
```

```lsl
//  color the root prim red and the first linked-prim green

default
{
    touch_start(integer num_detected)
    {
        llSetLinkPrimitiveParamsFast(LINK_ROOT, [
                PRIM_COLOR, ALL_SIDES, <1.0, 0.0, 0.0>, 1.0]);
        llSetLinkPrimitiveParamsFast(2, [
                PRIM_COLOR, ALL_SIDES, <0.0, 1.0, 0.0>, 1.0]);
    }
}
```

**Combining function calls**

```lsl
// Combined function calls

default
{
    touch_start(integer num_detected)
    {
        // color prim faces, set texture and set fullbright
        llSetPrimitiveParams([
            PRIM_COLOR, ALL_SIDES, ZERO_VECTOR, 1.0,
            PRIM_COLOR, 3, <1.0, 1.0, 1.0>, 1.0,
            PRIM_TEXTURE, 3, "4d304955-2b01-c6c6-f545-c1ae1e618288", <1.0, 1.0, 0.0>, ZERO_VECTOR, 0.0,
            PRIM_FULLBRIGHT, 3, TRUE]);
    }
}
```

```lsl
// Single function calls

default
{
    touch_start(integer num_detected)
    {
        // color prim faces
        llSetPrimitiveParams([
            PRIM_COLOR, ALL_SIDES, ZERO_VECTOR, 1,
            PRIM_COLOR, 3, <1.0, 1.0, 1.0>, 1.0]);

        // set texture
        llSetPrimitiveParams([
            PRIM_TEXTURE, 3, "4d304955-2b01-c6c6-f545-c1ae1e618288", <1.0, 1.0, 0.0>, ZERO_VECTOR, 0.0]);

        // set fullbright
        llSetPrimitiveParams([
            PRIM_FULLBRIGHT, 3, TRUE]);
    }
}
```

```lsl
// And if you want to place it above your bed, to make you sleep well, and the coords
// of that place are, for example,
llSetPrimitiveParams([
    PRIM_COLOR, ALL_SIDES, ZERO_VECTOR, 1.0,
    PRIM_COLOR, 3, <1.0,1.0,1.0>, 1.0,
    PRIM_TEXTURE, 3, "4d304955-2b01-c6c6-f545-c1ae1e618288", <1.0, 1.0, 0.0>, ZERO_VECTOR,0.0,
    PRIM_FULLBRIGHT, 3, TRUE,
    PRIM_POSITION, ]);

// You can set the texture of several sides at once, with no time penalty,
// just by repeating the param for that:
llSetPrimitiveParams([
    PRIM_TEXTURE, 3, "4d304955-2b01-c6c6-f545-c1ae1e618288", <1.0, 1.0, 0.0>, ZERO_VECTOR, 0.0,
    PRIM_TEXTURE, 4, "4d304955-2b01-c6c6-f545-c1ae1e618288", <1.0, 1.0, 0.0>, ZERO_VECTOR, 0.0]);
```

### Top-size (taper)

```lsl
default
{
    state_entry()
    {
        vector scale = llGetScale();
        float  X     = scale.x;
        float  Y     = scale.y;

        llSetPrimitiveParams([
            PRIM_SIZE, , // keep the prim thin
            PRIM_TYPE, PRIM_TYPE_BOX, 0, <0.0,1.0,0.0>, 0.0, ZERO_VECTOR,
                <1.0 - (0.4 / X), 1.0 - (0.4 / Y), 0.0>, ZERO_VECTOR]);
        // We used the equation "answer = 1 - desired_taper"

        // The proportions of the top-size (taper) will be maintained (as close as possible)
        // whenever the prim is resized. The proportion above will produce a reasonably
        // pleasing picture frame kinda thing.
    }

    changed(integer change)
    {
        if(change & CHANGED_SCALE)
        {
            llResetScript();
        }
    }
}
```

## Useful Snippets

```lsl
//-- PRIM_ROTATION workaround for child prims (works in unattached objects only)
llSetLinkPrimitiveParamsFast(linknumber, [
    PRIM_ROT_LOCAL, rot*llGetRootRotation()]);

//-- PRIM_ROTATION workaround for child prims (works in linked objects only)
llSetLinkPrimitiveParamsFast(linknumber, [
    PRIM_ROT_LOCAL, rot*llList2Rot(llGetLinkPrimitiveParams(LINK_ROOT, [PRIM_ROT_LOCAL]), 0)]);

//-- PRIM_ROTATION workaround for child prims (works in all scenarios)
llSetLinkPrimitiveParamsFast(linknumber, [
    PRIM_ROT_LOCAL, rot*llList2Rot(llGetLinkPrimitiveParams(!!llGetLinkNumber(), [PRIM_ROT_LOCAL]), 0)]);
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
The old PRIM_TYPE interface (labeled PRIM_TYPE_LEGACY), while technically retired, can still be used.

### PRIM_POSITION

Avatars sitting on the object can be moved with llSetLinkPrimitiveParams and PRIM_POSITION. This was originally a mis-feature but according to [Andrew Linden](http://jira.secondlife.com/browse/SVC-3408?focusedCommentId=88574#action_88574) LL has decided to support it.

Examples

The below example moves an avatar to x,y,z without moving the prim they are sitting on. If x,y,z is more than 54 meters away the call will silently fail. Remember x,y,z is in object relative coordinates just like any other linked prim in a set.

Avatars are always the last prims in the set, so llGetNumberOfPrims can be used for a single avatar sitting on a vehicle.

Example:

```lsl
llSetLinkPrimitiveParams(llGetNumberOfPrims(), [PRIM_POSITION, ]);
```

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

llGetPrimitiveParams

–

Get many primitive parameters

•

llSetLinkPrimitiveParams

–

Set parameters on other prims in linkset

•

llGetLinkPrimitiveParams

–

Get many primitive parameters of other prims in likset

•

llSetLinkPrimitiveParamsFast

–

Set parameters on other prims in linkset without sleep

•

llSetAlpha

–

Simpler way to set alpha (transparency) without (re-)setting color.

•

llSetTexture

–

Simpler way to set texture

•

llSetColor

–

Simpler way to set color

•

llSetScale

–

Simpler way to set scale

•

llSetStatus

–

Simpler way to set physics and phantom

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

•

Internal Textures

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

- Date of release llSetLinkPrimitiveParams 21-02-2007 or 14-03-2007
- Date of release llSetLinkPrimitiveParamsFast 29-03-2010

#### Footnotes

1. **^** LINK_ROOT does not work on single prim objects. Unless there is an avatar sitting on the object.
1. **^** When LL deprecated this flag they stripped it of it's name, however they did not remove the functionality. To aid in documenting the functionality, the value was given a new name in the documentation only. That is why PRIM_TYPE_LEGACY is not recognized by the compiler.
1. **^** The pipe character historically has been used to separate fields in the serialized version of inventory and possibly other internal fields for prim parameters.
1. **^** Floating text with an alpha set to 0.0 is rendered "invisible"
1. **^** The ranges in this article are written in [Interval Notation](http://en.wikipedia.org/wiki/Interval_(mathematics)#Notations_for_intervals).

#### Signature

```lsl
function void llSetPrimitiveParams( list rules );
function void llSetLinkPrimitiveParams( integer link, list rules );
function void llSetLinkPrimitiveParamsFast( integer link, list rules );
```