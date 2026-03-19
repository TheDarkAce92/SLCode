---
name: "llDetectedRot"
category: "function"
type: "function"
language: "LSL"
description: 'Returns the rotation of detected object number.

number does not support negative indexes.
Returns <0.0, 0.0, 0.0, 1.0> if number is not valid sensed object.'
signature: "rotation llDetectedRot(integer number)"
return_type: "rotation"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llDetectedRot'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lldetectedrot"]
---

Returns the rotation of detected object number.

number does not support negative indexes.
Returns <0.0, 0.0, 0.0, 1.0> if number is not valid sensed object.


## Signature

```lsl
rotation llDetectedRot(integer number);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `number` | Index of detection information |


## Return Value

Returns `rotation`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llDetectedRot)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llDetectedRot) — scraped 2026-03-18_

Returns the rotation of detected object number.

## Caveats

- If number is out of bounds this function returns <0.0, 0.0, 0.0, 1.0> and the script continues to execute without an error message.
- Events that enable the llDetected* functions always return at least one detected item.

  - Detection events are not raised if there is nothing detected.
  - The detection event's items detected parameter is initially never less than 1.

## Examples

```lsl
//--// get compass facing of Avatar that touches this object //--//

 //-- list of compass directions starting at East, rotated clockwise
list gLstCompassPoints = [ "East", "NorthEast", "North", "NorthWest", "West", "SouthWest", "South", "SouthEast" ];

 //-- convert rotation to z-axis compass direction
string CompassDirection( rotation rRotBase )
{
  integer iCountCompassPoints = llGetListLength(gLstCompassPoints);
   //-- convert rotation to a direction
  vector vDirection = <0.0, 1.0, 0.0> / rRotBase;
   //-- take the direction and determine the z rotation
  float fAngle = llAtan2(vDirection.x, vDirection.y);
   //-- take the angle and find the compass point
  integer iCompassPoint = llRound(fAngle * iCountCompassPoints / TWO_PI);
   //-- convert to string
  return llList2String( gLstCompassPoints, iCompassPoint );
}

default{
  state_entry()
  {
    llSay( 0, "Touch me to get your compass facing" );
  }

  touch_start( integer vIntTouchCount )
  {
    integer vIntCounter = 0;
    do
    {
      llSay( 0,
             llDetectedName( vIntCounter )
             + " is facing "
              //-- next line gets avatar rotation and converts to compass direction
             + CompassDirection( llDetectedRot( vIntCounter ) ) );
    } while ( ++vIntCounter < vIntTouchCount );
  }
}
```

## See Also

### Articles

- Detected

<!-- /wiki-source -->
