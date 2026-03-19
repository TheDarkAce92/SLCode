---
name: "llRemoteLoadScript"
category: "function"
type: "function"
language: "LSL"
description: "Deprecated. Remotely loads a script into a prim. Use llRemoteLoadScriptPin instead."
signature: "void llRemoteLoadScript(key target, string name, integer running, integer start_param)"
return_type: "void"
sleep_time: "3.0"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llRemoteLoadScript'
deprecated: "true"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Deprecated


## Signature

```lsl
void llRemoteLoadScript(key target, string name, integer running, integer start_param);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `target` | prim UUID that is in the same region |
| `string` | `name` | a script in the inventory of the prim this script is in |
| `integer` | `running` |  |
| `integer` | `start_param` |  |


## Caveats

- Forced delay: **3.0 seconds** — the script sleeps after each call.
- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llRemoteLoadScript)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llRemoteLoadScript) — scraped 2026-03-18_

Deprecated

## Caveats

- This function causes the script to sleep for 3.0 seconds.
- This function has been deprecated, please use llRemoteLoadScriptPin instead.
- This function returns an error message and does nothing else.

## See Also

### Functions

- llRemoteLoadScriptPin

<!-- /wiki-source -->
