---
name: "CHANGED constants"
category: "constant"
type: "constant"
language: "LSL"
description: "Bitmask constants used with the changed event to identify what changed on an object"
wiki_url: "https://wiki.secondlife.com/wiki/CHANGED_OWNER"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
---

# CHANGED_* Constants

Used with the `changed` event's `change` parameter. Test with bitwise `&`.

## Constants

| Constant | Value | Description | Scope |
|----------|-------|-------------|-------|
| `CHANGED_INVENTORY` | 0x001 | Prim inventory changed (not from scripts or `llAllowInventoryDrop`) | prim |
| `CHANGED_COLOR` | 0x002 | Colour or alpha changed | prim |
| `CHANGED_SHAPE` | 0x004 | Prim shape changed | prim |
| `CHANGED_SCALE` | 0x008 | Scale changed (root prim only receives this) | prim |
| `CHANGED_TEXTURE` | 0x010 | Texture parameters changed | prim |
| `CHANGED_LINK` | 0x020 | Prims linked/unlinked or avatar seated/stood | object |
| `CHANGED_ALLOWED_DROP` | 0x040 | Non-owner added inventory by drag-drop | prim |
| `CHANGED_OWNER` | 0x080 | Ownership changed; fires in original on take/deed and in new object on first rez | object |
| `CHANGED_REGION` | 0x100 | Object crossed into different region | object |
| `CHANGED_TELEPORT` | 0x200 | Attached avatar teleported | object |
| `CHANGED_REGION_START` | 0x400 | Region came back online after restart | region |
| `CHANGED_MEDIA` | 0x800 | Prim Media changed | prim |
| `CHANGED_RENDER_MATERIAL` | 0x1000 | Render material (GLTF) changed | prim |

## Usage

```lsl
default
{
    changed(integer change)
    {
        // Single flag test
        if (change & CHANGED_OWNER)
            llResetScript();

        // Multiple flags at once
        if (change & (CHANGED_OWNER | CHANGED_INVENTORY))
            llResetScript();

        // All possible checks
        if (change & CHANGED_INVENTORY)    llOwnerSay("Inventory changed");
        if (change & CHANGED_COLOR)        llOwnerSay("Color changed");
        if (change & CHANGED_SHAPE)        llOwnerSay("Shape changed");
        if (change & CHANGED_SCALE)        llOwnerSay("Scale changed");
        if (change & CHANGED_TEXTURE)      llOwnerSay("Texture changed");
        if (change & CHANGED_LINK)         llOwnerSay("Link changed");
        if (change & CHANGED_ALLOWED_DROP) llOwnerSay("Item dropped in");
        if (change & CHANGED_REGION)       llOwnerSay("Crossed region");
        if (change & CHANGED_TELEPORT)     llOwnerSay("Avatar teleported");
        if (change & CHANGED_REGION_START) llOwnerSay("Region restarted");
    }
}
```

## See Also

- `changed` event
- `llResetScript` — common response to CHANGED_OWNER
