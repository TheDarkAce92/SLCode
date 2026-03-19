---
name: "PhysicsLib"
category: "example"
type: "example"
language: "LSL"
description: "Experimental untested function, supposed to be used together with a device to prevent the familiar avatar 'splat', to calculate when a falling object hits Z=0, based on the (relative) float Height."
wiki_url: "https://wiki.secondlife.com/wiki/PhysicsLib"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 Non-License
- 2 Trajectory Functions

  - 2.1 Time Of Flight
  - 2.2 Angle of Reach
  - 2.3 Angle of Reach, Height
- 3 Target Interception
- 4 Usage Example

## Non-License

```lsl
//===================================================//
//                Physics Library 0.2                //
//          "May 6 2009", "11:00:00 GMT-0"           //
//                  By Nexii Malthus                 //
//                   Public Domain                   //
//===================================================//
```

## Trajectory Functions

### Time Of Flight

```lsl
float pTimeOfFlight(float Dist, float Angle, float Height, float Vel, float Gravity ){// UNTESTED!
    float cos = llCos(Angle); float sin = llSin(Angle);
    return ( Dist / Vel*cos ) * ( ( llPow(Vel*sin,2) + 2 * Gravity * Height ) / Gravity);}
```

Experimental untested function, supposed to be used together with a device to prevent the familiar avatar 'splat', to calculate when a falling object hits Z=0, based on the (relative) float Height.

### Angle of Reach

```lsl
rotation pAngleOfReach(vector cPos,vector tPos,float V,float G,integer cAng){
    float Theta;
    float V2 = V*V;float V4 = V*V*V*V;
    float X = llVecDist(,);float X2 = X*X;
    float Y = 0.0;

    float Thingy = V4 - ( G * (G*X2 + 2*Y*V2 ));
    if(Thingy <= 0){
        //llSetText("Over max distance!",<1,1,1>,1.0);
        return ZERO_ROTATION;}

    float Sqrt = llSqrt(Thingy);
    float x;
    if( cAng ) x = V2 + Sqrt;
    else x = V2 - Sqrt;
    float y = G*X;
    Theta = llAtan2(x,y);
    return <0, llSin( Theta/2 ), 0, -llCos( Theta/2 )>;
}
```

Returns quaternion rotation equivilant to the Y-Axis Rotation that is required to fullfill the conditions. Returns ZERO_ROTATION if there is an error though.

### Angle of Reach, Height

```lsl
rotation pAngleOfReachHeight(vector cPos,vector tPos,float V,float G,integer cAng){
    float Theta;
    float V2 = V*V;float V4 = V*V*V*V;
    float X = llVecDist(,);float X2 = X*X;
    float Y = tPos.z - cPos.z;

    //float MaxD =  (V * llCos(PI/4) / G) + (V * llSin(PI/4) + llSqrt( llPow( (V*llSin(PI/4)) + (2*G*Y),2) ) );
    // MaxD is the Maximum Distance. Can be useful if you need to know how far you can shoot with certain velocities!

    float Thingy = V4 - ( G * (G*X2 + 2*Y*V2 ));
    if(Thingy <= 0){
        //llSetText("Over max distance!",<1,1,1>,1.0);
        return ZERO_ROTATION;}

    float Sqrt = llSqrt(Thingy);
    float x;
    if( cAng ) x = V2 + Sqrt;
    else x = V2 - Sqrt;
    float y = G*X;
    Theta = llAtan2(x,y);
    return <0, llSin( Theta/2 ), 0, -llCos( Theta/2 )>;
}
```

Same as the other one, but this time can cope when the target may be at a different height than the source.

## Target Interception

```lsl
vector Interception( vector cPos, vector tPos, vector cVel, vector tVel ){
    vector rPos = tPos - cPos;
    float tVxtV = tVel * tVel;
    float b = rPos * tVel;
    float a = cVel * cVel - tVxtV;
    return tPos + ( b + llSqrt( b*b + a * (rPos*rPos) ) ) / a * tVel;}
```

Returns vector of position to aim at so that an accurate hit is made. This is assuming both objects travel in a linear fashion in a constant speed. Still pretty damn good and close enough. Doesn't account for gravity though, so cannot be used with Angle of Reach unless you work out the average XY velocity for a preliminary trajectory I suppose.

## Usage Example

```lsl
    rotation PointRot = llRotBetween(<1,0,0>,llVecNorm( - cPos));
    rotation TrajRot = pAngleOfReachHeight(cPos, tPos, 10.0, 9.8, FALSE );

    if(TrajRot == ZERO_ROTATION) return;

    RezPos = cPos;
    RezVel = < 10.0, 0.0, 0.0 > * (TrajRot * PointRot);
    RezRot = PointRot;
    RezObj = llGetInventoryName(INVENTORY_OBJECT,0);
```

A simple example.