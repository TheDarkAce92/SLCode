---
name: "PRIM_LINK_TARGET"
category: "example"
type: "example"
language: "LSL"
description: "The integer constant PRIM_LINK_TARGET has the value 34 Used to get or set multiple links with a single PrimParameters call."
wiki_url: "https://wiki.secondlife.com/wiki/PRIM_LINK_TARGET"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL

PRIM_LINK_TARGET

- 1 Description
- 2 llSetPrimitiveParams
- 3 llGetPrimitiveParams
- 4 Caveats
- 5 Related Articles

  - 5.1 Constants
  - 5.2 Functions
  - 5.3 Articles
- 6 Examples
- 7 Notes

  - 7.1 Link Numbers

  - 7.1.1 Counting Prims & Avatars
  - 7.1.2 Errata
- 8 Deep Notes

  - 8.1 top_size Explained
  - 8.2 All Issues
  - 8.3 Footnotes
  - 8.4 Signature

## Description

 Constant: integer PRIM_LINK_TARGET = 34;

The integer constant PRIM_LINK_TARGET has the value 34


Used to get or set multiple links with a single PrimParameters call.

## llSetPrimitiveParams

 llSetPrimitiveParams([ PRIM_LINK_TARGET, integer link_target ]);

• integer

link_target

–

Link number (0: unlinked, 1: root prim, >1: child prims and seated avatars) or a `LINK_*` flag

The same syntax applies to llSetLinkPrimitiveParams and llSetLinkPrimitiveParamsFast but with an additional prefixed link parameter in the function call.

## llGetPrimitiveParams

 llGetPrimitiveParams([ PRIM_LINK_TARGET, integer link_target ]);

Returns the list [  ]

• integer

link_target

–

Link number (0: unlinked, 1: root prim, >1: child prims and seated avatars) or a `LINK_*` flag

The same syntax applies to llGetLinkPrimitiveParams, but with an additional prefixed link parameter in the function call.

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
- Do not rely on Floating Text as a storage medium; it is neither secure nor finalized.

  - Floating text has been altered in past server updates, breaking existing content; future changes may occur.
  - Even "invisible" floating text is transmitted to the client.

  - It can be viewed by anyone with a client that is capable of rendering text that is supposed to be invisible.
  - The network packets that contain the text can be sniffed and the text read.
- top_size and client values are different, the ranges do not line up, conversion is required. This simple equation can be used: answer = 1.0 - value. See top_size Explained for more information.
- PRIM_OMEGA on nonphysical objects, and child prims of physical objects, is only a client side effect; the object or prim will collide as non-moving geometry.
- PRIM_OMEGA cannot be used on avatars sitting on the object. It will emit the error message "PRIM_OMEGA disallowed on agent".
- If PRIM_OMEGA does not appear to be working, make sure that that Develop > Network > Velocity Interpolate Objects is enabled on the viewer.
- In the parameters returned by `llGetPrimitiveParams([PRIM_OMEGA])`, the vector is normalized, and the spinrate is multiplied by the magnitude of the original vector.
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



## Related Articles

### Constants

Flag

Description

LINK_ROOT

1

refers to the root prim in a multi-prim linked set

Flag

Description

LINK_THIS

-4

refers to the prim the script is in

### Functions

•

llSetLinkPrimitiveParams

•

llSetLinkPrimitiveParamsFast

•

llGetLinkPrimitiveParams

•

llSetPrimitiveParams

•

llGetPrimitiveParams

•

llGetLinkNumber

–

Returns the link number of the prim the script is in.

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

## Examples

```lsl
default
{
    touch_start(integer num_detected)
    {
    //  color the root prim red and the first linked-prim green
        llSetLinkPrimitiveParamsFast(LINK_ROOT,
                [PRIM_COLOR, ALL_SIDES, <1.0, 0.0, 0.0>, (float)TRUE,
            PRIM_LINK_TARGET, 2,
                PRIM_COLOR, ALL_SIDES, <0.0, 1.0, 0.0>, (float)TRUE]);

    //  instead of:
    //  llSetLinkPrimitiveParamsFast(LINK_ROOT,
    //          [PRIM_COLOR, ALL_SIDES, <1.0, 0.0, 0.0>, (float)TRUE]);
    //  llSetLinkPrimitiveParamsFast(2,
    //          [PRIM_COLOR, ALL_SIDES, <0.0, 1.0, 0.0>, (float)TRUE]);
    }
}
```

```lsl
//  assume that you have a global list "gPanels" loaded with the link numbers of prims
//  named "panel" and that the global integer parameter "gON" has been defined ....

    touch_start(integer num)
    {
    //  basic on/off switch
        gON = !gON;

    //  conditions which will change on touch
    //  white panel
        list WhichWay = [PRIM_COLOR, ALL_SIDES, <1.0, 1.0, 1.0>, (float)TRUE];

        if (gON)//  red panel
            WhichWay = [PRIM_COLOR, ALL_SIDES, <1.0, 0.0, 0.0>, (float)TRUE];

    //  to accumulate the parameter list that will be affected by SLPPF in this event
        list params;
        integer numberOfPrims = llGetNumberOfPrims();

    //  Links in a linkset start numbering with 1
        integer index = 1;
        do
        {
        //  build the parameters list, in the format PRIM_LINK_TARGET, link number, parameters
            params += [PRIM_LINK_TARGET, llList2Integer(gPanels, index)] + WhichWay;
        }
        while (++index < numberOfPrims);

    //  apply the parameters to all "panel" prims
        llSetLinkPrimitiveParamsFast(LINK_SET, params);
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

#### All Issues

 ~ [Search JIRA for related Issues](http://jira.secondlife.com/secure/IssueNavigator!executeAdvanced.jspa?jqlQuery=%28summary+%7E+%22PRIM_LINK_TARGET%22+OR+description+%7E+%22PRIM_LINK_TARGET%22%29+&runQuery=true)

[](https://jira.secondlife.com/secure/ShowConstantsHelp.jspa?decorator=popup#IssueTypes)

[](https://jira.secondlife.com/secure/ShowConstantsHelp.jspa?decorator=popup#StatusTypes)

[SVC-914](http://jira.secondlife.com/browse/SVC-914)

A



CHANGED_TEXTURE is not triggered when texture is changed via script

#### Footnotes

1. **^** The pipe character historically has been used to separate fields in the serialized version of inventory and possibly other internal fields for prim parameters.
1. **^** Floating text with an alpha set to 0.0 is rendered "invisible"
1. **^** The ranges in this article are written in [Interval Notation](http://en.wikipedia.org/wiki/Interval_(mathematics)#Notations_for_intervals).
1. **^** LINK_ROOT does not work on single prim objects. Unless there is an avatar sitting on the object.

#### Signature

```lsl
integer PRIM_LINK_TARGET = 34;
```