---
name: "llDetectedRezzer"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a key that is the UUID of the object or avatar that rezzed the Detected object number.

Returns an  if number does not correspond to a valid sensed object or avatar.'
signature: "key llDetectedRezzer(integer index)"
return_type: "key"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llDetectedRezzer'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
flags: "experimental"
---

Returns a key that is the UUID of the object or avatar that rezzed the Detected object number.

Returns an  if number does not correspond to a valid sensed object or avatar.


## Signature

```lsl
key llDetectedRezzer(integer index);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `number` |  |


## Return Value

Returns `key`.


## Caveats

- Energy cost: **10.0**.
- **Experimental** — behaviour may change.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llDetectedRezzer)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llDetectedRezzer) — scraped 2026-03-18_

Returns a key that is the UUID of the object or avatar that rezzed the detected object number.

## Caveats

- If number is out of bounds  the script continues to execute without an error message.
- Events that enable the llDetected* functions always return at least one detected item.

  - Detection events are not raised if there is nothing detected.
  - The detection event's items detected parameter is initially never less than 1.

## See Also

### Articles

- Detected

<!-- /wiki-source -->
