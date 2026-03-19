---
name: "llOpenFloater"
category: "function"
type: "function"
language: "LSL"
description: 'Returns an integer Error code, or 0 if no error.

This function may be called only from a Linden owned experience.'
signature: "integer llOpenFloater(string title, string url, list params)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llOpenFloater'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
flags: "experience-api"
---

Returns an integer Error code, or 0 if no error.

This function may be called only from a Linden owned experience.


## Signature

```lsl
integer llOpenFloater(string title, string url, list params);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `floater_name` | Identifier of the viewer floater to open. |
| `string` | `url` | URL to open in the floater. |
| `list` | `params` | Options to apply to floater. |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.
- Requires an active **Experience** (Experience API function).


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llOpenFloater)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llOpenFloater) — scraped 2026-03-18_

Returns an integer Error code, or 0 if no error.

## Notes

Known valid values for the floater_name parameter:

- guidebook
- how_to
- web_content

<!-- /wiki-source -->
