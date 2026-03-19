---
name: "llGetMass"
category: "function"
type: "function"
language: "LSL"
description: "Returns a float that is the mass of object (in lindograms) that script is attached to."
signature: "float llGetMass()"
return_type: "float"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetMass'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetmass"]
---

Returns a float that is the mass of object (in lindograms) that script is attached to.


## Signature

```lsl
float llGetMass();
```


## Return Value

Returns `float`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetMass)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetMass) — scraped 2026-03-18_

Returns a float that is the mass of object (in lindograms) that script is attached to.

## Caveats

- The mass reported by this function is in lindograms, which function the same as kilograms within the bounds of Second Life, but not elsewhere. (See below)
- Attachments do not affect an avatar's mass, only certain Appearance settings.

  - Avatar mass is reported to either be unexpectedly low (when measured using llGetMass) or unexpectedly high (when measured using llGetMassMKS). This is likely due to the weight being calculated based on a fixed value, with a modifier for height. The fixed value being used is incorrect, likely due to an incorrect density value being used.

## Examples

```lsl
//A way of making a constant force that returns the same speed visually whatever the object is
default
{
    touch_start()
    {
        llApplyImpulse(<0.0, 0.0, 5.0> * llGetMass(), FALSE);
        // This fires the object up at the same m/s whatever the size (or difference!)
    }
}//Written by El Taka
```

## See Also

### Functions

- **llGetObjectMass** — Gets the object mass (in lindograms)
- **llGetForce** — Gets the objects force
- llGetOmega
- llGetVel
- llGetTorque
- llGetAccel
- **llGetMassMKS** — Get the mass of an object (in kilograms)

<!-- /wiki-source -->
