---
name: "llSetRemoteScriptAccessPin"
category: "function"
type: "function"
language: "LSL"
description: "Allows a prim to have scripts remotely loaded via llRemoteLoadScriptPin when it is passed the correct pin and the prim is set mod."
signature: "void llSetRemoteScriptAccessPin(integer pin)"
return_type: "void"
sleep_time: "0.2"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetRemoteScriptAccessPin'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsetremotescriptaccesspin"]
---

Allows a prim to have scripts remotely loaded via llRemoteLoadScriptPin when it is passed the correct pin and the prim is set mod.


## Signature

```lsl
void llSetRemoteScriptAccessPin(integer pin);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `pin` | zero disables (ie llRemoteLoadScriptPin will fail), non-zero enables. |


## Caveats

- Forced delay: **0.2 seconds** — the script sleeps after each call.
- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetRemoteScriptAccessPin)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetRemoteScriptAccessPin) — scraped 2026-03-18_

Allows a prim to have scripts remotely loaded via llRemoteLoadScriptPin when it is passed the correct pin and the prim is set mod.

## Caveats

- This function causes the script to sleep for 0.2 seconds.
- A prim has only one pin for remotely loading scripts.

  - By changing the pin, a script can deny other scripts the ability to load scripts into the prim.

  - This could result in unintentionally breaking a products ability to be updated by an upstream creator.
  - This can be used to intentionally stop an upstream creator from updating a product.
  - There is no way to find out whether a script pin has been set by another script in the prim. If the prim contains scripts from other developers, the safe approach is to assume a script pin has been set by an upstream creator.

## See Also

### Functions

- **llRemoteLoadScriptPin** — Used to load a script into a remote prim

<!-- /wiki-source -->
