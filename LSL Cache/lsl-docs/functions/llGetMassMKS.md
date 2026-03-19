---
name: "llGetMassMKS"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a float that is the mass (in Kilograms) of object that script is attached to. Functionally identical to llGetMass except for the unit used in the return value.

MKS as used in the name of this function is likely a reference to the MKS system of units (Meter, Kilogram, Second), which form the'
signature: "float llGetMassMKS()"
return_type: "float"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetMassMKS'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetmassmks"]
---

Returns a float that is the mass (in Kilograms) of object that script is attached to. Functionally identical to llGetMass except for the unit used in the return value.

MKS as used in the name of this function is likely a reference to the MKS system of units (Meter, Kilogram, Second), which form the base of SI units (with some minor differences).


## Signature

```lsl
float llGetMassMKS();
```


## Return Value

Returns `float`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetMassMKS)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetMassMKS) — scraped 2026-03-18_

Returns a float that is the mass (in Kilograms) of object that script is attached to. Functionally identical to llGetMass except for the unit used in the return value.

## Caveats

- Attachments do not effect an avatar's mass, only certain Appearance settings.

  - Avatar mass is reported to either be unexpectedly low (when measured using llGetMass) or unexpectedly high (when measured using llGetMassMKS). This is likely due to the weight being calculated based on a fixed value, with a modifier for height. The fixed value being used is incorrect, likely due to an incorrect density value being used.

## Examples

```lsl
//Reports an object's mass in Lindograms and Kilograms.
default
{
    touch_start()
    {
        llSay(0,"My weight in Lindograms: " + (string)llGetMass() + "\nMy weight in Kilograms: " + (string)llGetMassMKS());
    }
}
```

## Notes

- the Kilogram value seems to be the Lindogram value multiplied by 100.

## See Also

### Functions

- **llGetObjectMass** — Gets the object mass (in Lindograms)
- **llGetForce** — Gets the objects force
- llGetOmega
- llGetVel
- llGetTorque
- llGetAccel
- **llGetMass** — Get the mass of an object (in Lindograms)

<!-- /wiki-source -->
