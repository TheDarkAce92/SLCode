---
name: "llGetScriptName"
category: "function"
type: "function"
language: "LSL"
description: "Returns a string that is the name of the script that called this function."
signature: "string llGetScriptName()"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetScriptName'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetscriptname"]
---

Returns a string that is the name of the script that called this function.


## Signature

```lsl
string llGetScriptName();
```


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetScriptName)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetScriptName) — scraped 2026-03-18_

Returns a string that is the name of the script that called this function.

## Examples

Remove the current script from the object

```lsl
default
{
    state_entry()
    {
        llRemoveInventory(llGetScriptName());
    }
}
```

<!-- /wiki-source -->
