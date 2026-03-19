---
name: "llSetLinkAlpha"
category: "function"
type: "function"
language: "LSL"
description: 'If a prim exists in the link set at link, set the Blinn-Phong alpha on face of that prim.

If face is ALL_SIDES then the function works on all sides.'
signature: "void llSetLinkAlpha(integer linknumber, float alpha, integer face)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetLinkAlpha'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsetlinkalpha"]
---

If a prim exists in the link set at link, set the Blinn-Phong alpha on face of that prim.

If face is ALL_SIDES then the function works on all sides.


## Signature

```lsl
void llSetLinkAlpha(integer linknumber, float alpha, integer face);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer (link)` | `link` | Link number (0: unlinked, 1: root prim, >1: child prims and seated avatars) or a LINK_* flag |
| `float` | `alpha` | from 0.0 (clear) to 1.0 (solid) (0.0 <= alpha <= 1.0) |
| `integer` | `face` | face number or ALL_SIDES |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetLinkAlpha)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetLinkAlpha) — scraped 2026-03-18_

If a prim exists in the link set at link, set the Blinn-Phong alpha on face of that prim.

## Caveats

- The function silently fails if its face value indicates a face that does not exist.
- llSetLinkAlpha will have no visible effect on faces with a PBR material. To work on faces both with and without a PBR material, use one of these snippets:

  - invisible

```lsl
llSetLinkAlpha(LINK_THIS, 0.0, ALL_SIDES);
llSetLinkPrimitiveParamsFast(LINK_THIS, [PRIM_GLTF_BASE_COLOR, ALL_SIDES, "", "", "", "", "", 0.0, PRIM_GLTF_ALPHA_MODE_MASK, 1.0, ""]);
```
  - visible

```lsl
llSetLinkAlpha(LINK_THIS, 1.0, ALL_SIDES);
llSetLinkPrimitiveParamsFast(LINK_THIS, [PRIM_GLTF_BASE_COLOR, ALL_SIDES, "", "", "", "", "", "", "", "", ""]);
```

## Examples

```lsl
// Make the entire object disappear for 5 seconds

default
{
    touch_start(integer num_detected)
    {
        // transparent
        llSetLinkAlpha(LINK_SET, 0.0, ALL_SIDES);
        llSetTimerEvent(5.0);
    }

    timer()
    {
        // opaque
        llSetLinkAlpha(LINK_SET, 1.0, ALL_SIDES);
        llSetTimerEvent(0.0);
    }
}
```

```lsl
// when the object is touched,
// fade it out and back in again

default
{
    touch_start(integer num_detected)
    {
        // fade out
        float alpha = 1.0;
        while (alpha >= 0.0)
        {
            llSetLinkAlpha(LINK_SET, alpha, ALL_SIDES);
            alpha -= 0.001;
        }

        // fade in
        while (alpha < 1.0)
        {
            alpha += 0.001;
            llSetLinkAlpha(LINK_SET, alpha, ALL_SIDES);
        }
    }
}
```

```lsl
// Makes selected prims in a linkset become transparent or visible on chat command. Give each prim a unique name.

list PrimList = ["ALL"];
// Start our prim list with a dummy entry, so that the index into this list will correspond directly to the link number
// By making the dummy entry 'ALL' we provide a match for that option too

default
{
    changed (integer change)
    {
	if (change & CHANGED_LINK)
	    llResetScript();
    }

    state_entry()
    {
	integer PrimCount = llGetNumberOfPrims();
	llListen(37, "", NULL_KEY, "");  		    //  listen to chat commands from anyone on channel 37
	integer i;
	for (i = 1; i <= PrimCount; ++i)
	    PrimList += llToUpper(llGetLinkName(i) );  	    // Build a list of upper-case link names, where list position equals link number
    }

    listen(integer channel, string name, key id, string msg)
    {
	list    TempList = llCSV2List( llToUpper(msg) );    // make a list from upper-case version of user command line
	integer ListLen  = llGetListLength (TempList);
	integer alpha    = (llList2String(TempList, 0) == "SHOW");
	// 'SHOW' sets selected prims visible, otherwise set them transparent
	// e.g.  HIDE,PLATE,SPOON,NAPKIN	            <---- makes named prims invisible
	// e.g.  SHOW,ALL                                   <---- makes all prims visible

	integer i;
	for (i = 1; i < ListLen; ++i)
	{
	    string  ThisPrim   = llStringTrim(llList2String(TempList, i), STRING_TRIM);
	    integer LinkNumber = llListFindList(PrimList, [ThisPrim]);
	    if (~LinkNumber)    // i.e. if LinkNumber != -1
	    {
		if (!LinkNumber)
		    LinkNumber = LINK_SET;   	// list position 0 is 'ALL'

		llSetLinkAlpha(LinkNumber, alpha, ALL_SIDES);
	    }
	}
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

### Events

- **changed** — CHANGED_COLOR

### Functions

- **llGetLinkNumber** — prim
- **llGetAlpha** — Gets the prim's alpha
- **llSetAlpha** — Sets the prim's alpha
- **llGetColor** — Gets the prim's color
- **llSetColor** — Sets the prim's color
- llSetLinkColor
- llSetLinkTexture
- llSetLinkPrimitiveParams
- **PRIM_COLOR** — llSetPrimitiveParams
- **PRIM_GLTF_BASE_COLOR** — llSetPrimitiveParams

### Articles

- Translucent Color

<!-- /wiki-source -->
