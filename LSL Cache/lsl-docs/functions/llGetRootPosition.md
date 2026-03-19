---
name: "llGetRootPosition"
category: "function"
type: "function"
language: "LSL"
description: "Returns a vector that is the region position of the root object of the object script is attached to"
signature: "vector llGetRootPosition()"
return_type: "vector"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetRootPosition'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetrootposition"]
---

Returns a vector that is the region position of the root object of the object script is attached to


## Signature

```lsl
vector llGetRootPosition();
```


## Return Value

Returns `vector`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetRootPosition)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetRootPosition) — scraped 2026-03-18_

Returns a vector that is the region position of the root object of the object script is attached to

## Examples

```lsl
default{
  touch_start( integer vIntTouched ){
    string vStrMessage = "The prim with this script is ";
    if (llGetPos() != llGetRootPosition()){
      vStrMessage += "NOT ";
    }
    llSay( PUBLIC_CHANNEL, vStrMessage + "centered on the root prim." );
  }
}
```

## See Also

### Functions

- **llGetLocalPos** — Gets the child prims position relative to the root
- **llGetPos** — Gets the prims global position
- **llSetPos** — Sets the prims global position

<!-- /wiki-source -->
