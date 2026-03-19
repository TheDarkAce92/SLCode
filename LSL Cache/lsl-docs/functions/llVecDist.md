---
name: "llVecDist"
category: "function"
type: "function"
language: "LSL"
description: "Returns a float that is the undirected nonnegative distance between vec_a and vec_b."
signature: "float llVecDist(vector v1, vector v2)"
return_type: "float"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llVecDist'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llvecdist"]
---

Returns a float that is the undirected nonnegative distance between vec_a and vec_b.


## Signature

```lsl
float llVecDist(vector v1, vector v2);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `vec_a` | Any valid vector |
| `vector` | `vec_b` | Any valid vector |


## Return Value

Returns `float`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llVecDist)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llVecDist) — scraped 2026-03-18_

Returns a float that is the undirected nonnegative distance between vec_a and vec_b.

## Examples

```lsl
default {
    state_entry()
    {
        vector input_1 = <1.0,2.0,3.0>;
        vector input_2 = <3.0,2.0,1.0>;
        llOwnerSay("The distance between " + (string) input_1 +
            " and " + (string) input_2 + " is: "+(string)llVecDist(input_1, input_2) );
    }
}
```

```lsl
//To reset script on touch if the object has been rotated since the last script reset
float gTolerance = 0.05;  //This corresponds to about a 3 degree rotation
default
{
	state_entry()
	{
		llSetObjectDesc((string)llRot2Euler(llGetRot()));
	}

	touch_start(integer total_number)
	{
		if (llVecDist(llRot2Euler(llGetRot()), (vector)llGetObjectDesc()) > gTolerance)
		{
			llSay(0,"This object has rotated. Automatic reset engaged.");
			llResetScript();
		}
	}
}
```

### Video Tutorial

[https://www.youtube.com/watch?v=D0WvH58IWEo](https://www.youtube.com/watch?v=D0WvH58IWEo)

## Notes

- Mathematically equivalent to:

  - llVecMag( vec_a - vec_b )
  - llSqrt( (vec_b.x - vec_a.x) * (vec_b.x - vec_a.x) + (vec_b.y - vec_a.y) * (vec_b.y - vec_a.y) + (vec_b.z - vec_a.z) * (vec_b.z - vec_a.z) )
- Knowing this, there are ways to circumvent llVecDist for more efficient code.

  - For example, vector v3 = (v1-v2); v3*v3 < (f*f); is over twice as fast as llVecDist(v1,v2) < f;

## See Also

### Functions

- llVecMag
- llVecNorm

<!-- /wiki-source -->
