---
name: "llSetLinkMedia"
category: "function"
type: "function"
language: "LSL"
description: 'Set the media params for a particular face on the linked prim(s) without a delay.

Returns a status (an integer) that is a STATUS_* flag which details the success/failure of the operation(s).'
signature: "integer llSetLinkMedia(integer link, integer face, list params)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetLinkMedia'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsetlinkmedia"]
---

Set the media params for a particular face on the linked prim(s) without a delay.

Returns a status (an integer) that is a STATUS_* flag which details the success/failure of the operation(s).


## Signature

```lsl
integer llSetLinkMedia(integer link, integer face, list params);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer (link)` | `link` | Link number (0: unlinked, 1: root prim, >1: child prims) or a LINK_* flag  |
| `integer` | `face` | face number |
| `list (instructions)` | `params` | a set of name/value pairs (in no particular order) |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetLinkMedia)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetLinkMedia) — scraped 2026-03-18_

Set the media params for a particular face on the linked prim(s) without a delay.Returns a status (an integer) that is a STATUS_* flag which details the success/failure of the operation(s).

## Caveats

- link needs to be either an actual link number or a link constants that equate to a single prim, such as LINK_ROOT and LINK_THIS.

  - LINK_SET, LINK_ALL_CHILDREN and LINK_ALL_OTHERS will not work.
- link cannot be a seated avatar.
- The function silently fails if its face value indicates a face that does not exist.
- If prim media is not already on this object, it will be added.
- If prim media is newly added to this object, params not specified take their default value.
- If prim media is already on this object, params not specified are unchanged.
- About `PRIM_MEDIA_WIDTH_PIXELS` (width) and `PRIM_MEDIA_HEIGHT_PIXELS` (height) ...

  - Both width and height must be specified for either to work. They narrow the texture space while inversely widening the aperture, i.e. smaller values "zoom in."

  - If width and height are not specified, the function assumes 1024 for each.
  - When `PRIM_MEDIA_AUTO_SCALE` is `TRUE`, any value for width and height that is not precisely 2 where 0 ≤ *n* < 12 will be "rounded up" to the next value, i.e. setting `PRIM_MEDIA_WIDTH_PIXELS` to 257 has the same effect as setting it to 512. Any value outside the range of [0, 2048] will cause the function to shout a message to `DEBUG_CHANNEL` and fail. Using 0 (zero) results in the default value being used, which is 1024.
  - It might be helpful to think of width and height as setting your "screen size." If the media is smaller than this "screen," there will be empty space below and/or to the right of the media. If the media is larger than this "screen," scroll bars will be made visible. Re-scaling the prim without altering the face's *Horizontal scale,* *Vertical scale,* *Horizontal offset,* and *Vertical offset* will only distort (stretch/compress) the media.*Pending review. - NM*
- width and height scaled larger than 1024 pixels will require the texture backdrop to be resized to fit. (See Useful Snippets)

  - If resized to fit, the resulting view will cut off scrolled content outside the bounds making it impossible to be viewed.

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
- llSetPrimMediaParams
- llGetLinkMedia
- llClearLinkMedia

### Articles

- User:Kelly Linden/lsl hacks

<!-- /wiki-source -->
