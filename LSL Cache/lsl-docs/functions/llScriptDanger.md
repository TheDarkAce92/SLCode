---
name: "llScriptDanger"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a boolean (an integer) that is TRUE if pos is over public land, sandbox land, land that doesn't allow everyone to edit and build, or land that doesn't allow outside scripts.

The usefulness of this function is limited as it does not give the reason why the script would be in danger. llGetPar'
signature: "integer llScriptDanger(vector pos)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llScriptDanger'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llscriptdanger"]
---

Returns a boolean (an integer) that is TRUE if pos is over public land, sandbox land, land that doesn't allow everyone to edit and build, or land that doesn't allow outside scripts.

The usefulness of this function is limited as it does not give the reason why the script would be in danger. llGetParcelFlags on the other hand can be used in much the same way and gives more detailed information.


## Signature

```lsl
integer llScriptDanger(vector pos);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `pos` | position in region coordinates |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llScriptDanger)

