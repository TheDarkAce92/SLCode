---
name: "llAllowInventoryDrop"
category: "function"
type: "function"
language: "LSL"
description: 'Allows for all users without modify permissions to add inventory items to a prim.

To actually do the dropping, you need to drag an item from your inventory and drop it onto the prim WHILE holding down your Ctrl key. If you've got everything right, then just before you release it, you will see the p'
signature: "void llAllowInventoryDrop(integer add)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llAllowInventoryDrop'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llallowinventorydrop"]
---

Allows for all users without modify permissions to add inventory items to a prim.

To actually do the dropping, you need to drag an item from your inventory and drop it onto the prim WHILE holding down your Ctrl key. If you've got everything right, then just before you release it, you will see the prim framed in red.

Ownership of the dropped inventory item changes to the owner of the prim. Next owner permissions kick in on the item that was dropped in. Non-transfer items cannot be dropped into a prim owned by someone else.

An application might be a public "suggestion box" that you want to let people drop notecards into.


## Signature

```lsl
void llAllowInventoryDrop(integer add);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer (boolean)` | `add` | boolean, If TRUE it allows anyone, even if they don't have modify rights to a prim, regardless of whether they are the owner or not, to drop items into that prim, If FALSE (default) inventory dropping can still be done, but it is restricted only to people with modify permissions to that prim |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llAllowInventoryDrop)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llAllowInventoryDrop) — scraped 2026-03-18_

Allows for all users without modify permissions to add inventory items to a prim.

## Caveats

- In a link set llAllowInventoryDrop must be executed from a script within the root prim or it fails silently.
- Scripts are an exception to what is allowed to be dropped in. If a user without modify permissions to a prim attempts to drop a script into it, the inventory addition is rejected and the prim shouts (sic -- shouts, not says) "Not permitted to edit this!" This is for obvious security reasons. If you own the prim and have mod rights to it, you can drop a script in. Friends who have mod rights to your stuff can also drop scripts in.
- Will not work if, under the Object tab on the prim, "Locked" is ticked.
- Bear in mind when dropping a texture into a prim to be sure (a) that you see a red box framing the target prim, and (b) not to release the Ctrl button until you are sure that the texture is actually inside the box. If you see a white frame instead, or release Ctrl too soon, the texture will instead be applied to the prim face that you were on.
- There is no way to tell who dropped the item in. If you really need to know, consider making the user touch the prim first to turn the llAllowInventoryDrop on, and then grab the user's information from the touch event, and then set it back to FALSE through a timer.
- Nor is there any way based on just llAllowInventoryDrop to tell *what* the user dropped in. See WhoAddedWhat script to handle that.
- Ordinary end-users may face challenges when confronted with actually performing the drag and drop. See the section below.
- People with modify rights to your (modifiable) stuff can do this anyway, as can you, even without the presence of llAllowInventoryDrop.
- Even if you own the prim, but don't have modify rights to it, you cannot drop anything at all into it, ever, unless the creator put in it an llAllowInventoryDrop(TRUE) first before passing it to you.
- If you have a prim that you don't have mod rights to, but that the creator did set an llAllowInventoryDrop(TRUE) in, that even though you can drop stuff in, you will never be able to delete it! You can however move it to your inventory.

#### llAllowInventoryDrop and Everyday Users

- If you want someone to drag and drop notecards into a suggestion box, say, or whatever, you have to both invite them to do so, and explain how to do it (the holding down of the Ctrl key being essential to communicate.)

- A fair bit of fine motor skill is required to do this. Someone who doesn't have this, either because of failing or unsteady hands, or using a trackpad on a laptop in an awkward seated position, may not be able to perform this operation accurately.

- If you sell a user something such as, say, a gift box, which you instruct them to fill via inventory drag and drop, bear in mind that there is often many a slip betwixt inventory and prim, and the user may by mistake (in this example) drag the gifts in question into a piece of the bow instead, and then panic when s/he doesn't see them in the main part of the giftbox. (Remember: if they have mod rights to the prim, they can drag and drop stuff into any part of the prim, regardless of whether there is an llAllowInventoryDrop in it or not.) You may wish to suggest instead that the user right-click the prim, choose open, and drag and drop stuff onto the "Open" Object Contents window -- a much larger, safer target.

## Examples

When llAllowInventoryDrop is set to TRUE, and an item is successfully dropped BY SOMEONE WITHOUT MODIFY PERMISSIONS, the event that occurs is changed with the CHANGED_ALLOWED_DROP bit set.

```lsl
changed(integer change)
{
    if (change & CHANGED_ALLOWED_DROP)
        llSay(0, "Your contribution is appreciated, o ye non-permitted modifier!");
}
```

When an item is successfully dropped by someone WITH modify permissions, the event that occurs is CHANGED_INVENTORY, regardless of the state of llAllowInventoryDrop()

```lsl
changed(integer change)
{
    if (change & CHANGED_INVENTORY)
        llSay(0, "Your contribution is appreciated, o ye permitted modifier!");
}
```

Tip! To test for either changed event, the proper syntax is:

```lsl
changed(integer change)
{
    //PUBLIC_CHANNEL has the integer value 0
    if (change & (CHANGED_ALLOWED_DROP | CHANGED_INVENTORY))
        llSay(PUBLIC_CHANNEL, "yeppers, inventory changed somehow.");
}
```

The following example is a bit elaborate. It illustrates alternating AllowInventoryDrop off and on. (This is likely not something you would actually do unless you really wanted to play with users' minds.)

```lsl
integer allow;

default
{
    touch_start(integer num)
    {
        llAllowInventoryDrop(allow = !allow);
        llOwnerSay("llAllowInventoryDrop == " + llList2String(["FALSE","TRUE"], allow));
    }

    changed(integer change)
    {
        //note that it's & and not &&... it's bitwise!
        if (change & CHANGED_ALLOWED_DROP)
            llOwnerSay("The inventory has changed as a result of a user without mod permissions dropping
                        an item on the prim and it being allowed by the script.");
    }
}
```

## See Also

### Events

- **changed** — CHANGED_ALLOWED_DROP

<!-- /wiki-source -->
