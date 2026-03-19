---
name: "llGetEnergy"
category: "function"
type: "function"
language: "LSL"
description: "Returns a float that is how much energy is in the object as a percentage of maximum"
signature: "float llGetEnergy()"
return_type: "float"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetEnergy'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetenergy"]
---

Returns a float that is how much energy is in the object as a percentage of maximum


## Signature

```lsl
float llGetEnergy();
```


## Return Value

Returns `float`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetEnergy)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetEnergy) — scraped 2026-03-18_

Returns a float that is how much energy is in the object as a percentage of maximum

## Examples

```lsl
// This script tests the energy use of most of the physics functions
// Last version: 07 October 2009 by Gianni Lupindo

vector homePos;
integer timerCount = 0;
integer testCount = 0;
string space = "  ";

// move more than 10m
moveTo(vector origin, vector destination) {
    float dist = llVecDist(origin, destination);
    integer passes = llCeil( llLog(dist/10.0) / llLog(2.0) );
    integer i;
    list params = [PRIM_POSITION, destination];
    for (i=0; i

);
        llSetStatus(STATUS_PHYSICS,TRUE);
        llSetTimerEvent(1.0);

        vector impulse = <0,0,5>*llGetMass();
        if (testCount == 0) {
            llOwnerSay("ApplyImpulse (test 0)");
            llApplyImpulse( impulse, TRUE );
        } else if (testCount == 1) {
            llOwnerSay("ApplyRotImpulse (test 1)");
            llApplyRotationalImpulse( impulse, TRUE);
        } else if (testCount == 2) {
            llOwnerSay("PushObject (test 2)");
            llPushObject(llGetKey(), impulse, ZERO_VECTOR, TRUE);
        } else if (testCount == 3) {
            llSetForceAndTorque( ZERO_VECTOR, ZERO_VECTOR, TRUE );
            llOwnerSay("Force (test 3)");
            llSetForce( impulse, TRUE );
        } else if (testCount == 4) {
            llSetForceAndTorque( ZERO_VECTOR, ZERO_VECTOR, TRUE );
            llOwnerSay("Torque (test 4)");
            llSetTorque( impulse, TRUE );
        } else if (testCount == 5) {
            llSetForceAndTorque( ZERO_VECTOR, ZERO_VECTOR, TRUE );
            llOwnerSay("Force and Torque (test 5)");
            llSetForceAndTorque( impulse, impulse, TRUE );
        } else if (testCount == 6) {
            llSetForceAndTorque( ZERO_VECTOR, ZERO_VECTOR, TRUE );
            llOwnerSay("MoveToTarget (test 6)");
            llMoveToTarget( impulse, 0.4 );
        } else if (testCount == 7) {
            llStopMoveToTarget ( );
            llOwnerSay("RotLookAt (test 7)");
            llRotLookAt( llEuler2Rot(impulse*DEG_TO_RAD), 0.4, 0.4 );
        } else if (testCount == 8) {
            llStopLookAt ( );
            llOwnerSay("LookAt (test 8)");
            llLookAt( impulse, 0.4, 0.4 );
        } else if (testCount == 9) {
            llStopLookAt ( );
            llOwnerSay("Hover Height (test 9)");
            llSetHoverHeight( 5.0, TRUE, 0.5);
        } else if (testCount == 10) {
            llSetHoverHeight( 0, TRUE, 0.5);
            llOwnerSay("Ground Repel (test 10)");
            llGroundRepel( 5, TRUE, 0.5);
        } else if (testCount == 11) {
            llGroundRepel( 0, TRUE, 0.5);
            llOwnerSay("Buoyancy (test 11)");
            llSetBuoyancy( 0.997 );
        } else {
            llSetBuoyancy( 0.0 );
            llOwnerSay("Done");
        }
        timerCount = 0;
        if (testCount != 12) {
            llOwnerSay((string)timerCount+". Energy:    "+space+(string)llGetEnergy());
            testCount++;
        }
        else {
            testCount = 0;
            returnHome();
        }
    }
    timer() {
        timerCount++;
        if (timerCount >= 10) space = "";
        llOwnerSay((string)timerCount+". Energy:    "+space+(string)llGetEnergy());
        if (timerCount>=10) {
            returnHome();
        }
    }
    collision(integer n) {
        llOwnerSay("*. Energy:    "+space+(string)llGetEnergy()+" (collision)");
    }
}
```

<!-- /wiki-source -->
