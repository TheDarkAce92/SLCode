---
name: "llAxes2Rot"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a rotation that is defined by the 3 coordinate axes

All three vectors must be mutually orthogonal unit vectors.'
signature: "rotation llAxes2Rot(vector fwd, vector left, vector up)"
return_type: "rotation"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llAxes2Rot'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llaxes2rot"]
---

Returns a rotation that is defined by the 3 coordinate axes

All three vectors must be mutually orthogonal unit vectors.


## Signature

```lsl
rotation llAxes2Rot(vector fwd, vector left, vector up);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `fwd` |  |
| `vector` | `left` |  |
| `vector` | `up` |  |


## Return Value

Returns `rotation`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llAxes2Rot)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llAxes2Rot) — scraped 2026-03-18_

Returns a rotation that is defined by the 3 coordinate axes

## Examples

```lsl
default
{
    state_entry()
    {
        vector i = < 1.0, 0.0, 0.0>;
        vector j = < 0.0, 1.0, 0.0>;
        vector k = < 0.0, 0.0, 1.0>;

        rotation rot = llAxes2Rot( j, -i, k );

        llSay(0, (string) (llRot2Euler(rot) * RAD_TO_DEG) );
    }
}
```

This script displays:

```lsl
  Object: <-0.00000, 0.00000, 90.00000>
```

which shows that (**j**, **-i**, **k**) is obtained by rotating (**i**, **j**, **k**) 90 degrees around z direction.

## Notes

Technically, only the first two vectors are needed to define this rotation, which can be done by calling any of these:

```lsl
llAxes2Rot(fwd, left, fwd % left);
llAxes2Rot(left % up, left, up);
llAxes2Rot(fwd, up % fwd, up);
```

<!-- /wiki-source -->
