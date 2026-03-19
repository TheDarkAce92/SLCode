---
name: "llParcelMediaQuery"
category: "function"
type: "function"
language: "LSL"
description: "Returns a list containing results of query. The results are in the same order as the request."
signature: "list llParcelMediaQuery(list query)"
return_type: "list"
sleep_time: "2.0"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llParcelMediaQuery'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llparcelmediaquery"]
---

Returns a list containing results of query. The results are in the same order as the request.


## Signature

```lsl
list llParcelMediaQuery(list query);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `list` | `query` |  |


## Return Value

Returns `list`.


## Caveats

- Forced delay: **2.0 seconds** — the script sleeps after each call.
- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llParcelMediaQuery)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llParcelMediaQuery) — scraped 2026-03-18_

Returns a list containing results of query. The results are in the same order as the request.

## Caveats

- This function causes the script to sleep for 2.0 seconds.
- This script's object must be owned by the landowner or the function will silently fail.
- If the script's object is over group owned land, then the object must be deeded to **that** group.

## Examples

```lsl
//-- quick function to tell you the URL of the Media the Parcel is set for
default{
  touch_start( integer vIntNull ){ //-- named null because we're ignoring it
    llSay( 0, "The Media URL is\n" + (string)llParcelMediaQuery( (list)PARCEL_MEDIA_COMMAND_URL ) );
  }
}
```

## See Also

### Functions

- llParcelMediaCommandList

<!-- /wiki-source -->
