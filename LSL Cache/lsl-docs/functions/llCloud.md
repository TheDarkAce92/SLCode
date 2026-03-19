---
name: "llCloud"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a float that is the cloud density at the prim position + offset

Only the x and y coordinates in offset are important, the z component is ignored.
Returned values are in the range [0.0, 2.0]. Values above 1.0 indicate rain.'
signature: "float llCloud(vector offset)"
return_type: "float"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llCloud'
deprecated: "true"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Returns a float that is the cloud density at the prim position + offset

Only the x and y coordinates in offset are important, the z component is ignored.
Returned values are in the range [0.0, 2.0]. Values above 1.0 indicate rain.


## Signature

```lsl
float llCloud(vector offset);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `offset` | offset relative to the prim's position and expressed in local coordinates |


## Return Value

Returns `float`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llCloud)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llCloud) — scraped 2026-03-18_

Returns a float that is the cloud density at the prim position + offset

## Caveats

- This function has been deprecated.
- There are currently no SecondLife clients that render rain.
- The client attempts to render clouds from the cloud algorithm results sent from the server, which is why different clients can see different cloud formations and de-synchronizes cloud view from the server over time. The cloud density data is sent from the server to the client when the region is loaded by the client. This can happen when the region comes into view, during teleport or during login.

## Examples

```lsl
default
{
    touch_start(integer num)
    {
        llSay(0,"Cloud density:" + (string)llCloud(ZERO_VECTOR));
    }
}
```

## Notes

Clouds and wind are interrelated.

### Client

Clouds are always rendered between about 180-200m absolute height.

### Algorithm

The cloud seed/growth/dissipation algorithm uses a solenoidal vector field, which is a vector field with zero-divergence: ∇ · v = 0

This condition is satisfied whenever v has a vector potential A, because if v = ∇ ⨯ A then ∇ · v = ∇ · (∇ ⨯ A) = 0

## See Also

### Functions

- llWind
- llGetSunDirection

<!-- /wiki-source -->
