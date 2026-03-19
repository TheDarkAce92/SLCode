---
name: "Interpolation Library"
category: "example"
type: "example"
language: "LSL"
description: "Interpolation is a way of constructing new data points within a range of known data points."
wiki_url: "https://wiki.secondlife.com/wiki/Interpolation"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Interpolation is a way of constructing new data points within a range of known data points.

The range of applications is varied, but here in SL it can most directly be used for animating and/or moving prims or linksets via any attribute you can creatively make use of.

Attributes:

- Prim/Object Position
- Prim/Object Rotation
- Texture Scale/Offsets
- or you can just simply interpolate internal values

Potential applications:

- Movement
- Animation
- User Interfaces
- Graphics
- Games

There are many different types of interpolation, which may exhibit different preferred or controllable behaviour.



## Interpolation Library

Linear Interpolation

- Float
- Vector
- Rotation
- List of Vectors



Cosine Interpolation

- Float
- Vector
- Rotation



Cubic Interpolation

- Float
- Vector
- Rotation



Catmull-Rom Cubic Interpolation

- Float



Hermite Interpolation

- Float
- Vector

Spline Interpolation

- List of Vectors

Rescale

- Float
- Float Fixed



Target

- Float

---

## Subpage: Linear/Float

/LSL


Interpolation/Linear/Float

- 1 Summary
- 2 Specification
- 3 Examples

## Summary

 Function: float **fLin**( float x, float y, float t );

Interpolates between two floating point values in a linear fashion.Returns a float

• float

x

• float

y

• float

t

## Specification

```lsl
float fLin(float x, float y, float t) {
    return x*(1-t) + y*t;
}
// Released into public domain. By Nexii Malthus.
```

## Examples

```lsl
float value = fLin(-5, 15, 0.6); // value == 7
```

---

## Subpage: Linear/Vector

/LSL


Interpolation/Linear/Vector

- 1 Summary
- 2 Specification
- 3 Examples

## Summary

 Function: vector **vLin**( vector x, vector y, float t );

Interpolates between two vector values in a linear fashion.Returns a vector

• vector

x

• vector

y

• float

t

## Specification

```lsl
vector vLin(vector x, vector y, float t){
    return x*(1-t) + y*t;
}
// Released into public domain. By Nexii Malthus.
```

## Examples

```lsl
vector x = <-5, 1, 10>;
vector y = <15, 2, 2>;
vector z = vLin(x, y, 0.6); // z == <7, 1.6, 5.2>
```

---

## Subpage: Linear/Rotation

/LSL


Interpolation/Linear/Rotation

- 1 Summary
- 2 Specification
- 3 Examples

## Summary

 Function: rotation **rLin**( rotation x, rotation y, float t );

Interpolates between two rotation values in a linear fashion.Returns a rotation

• rotation

x

• rotation

y

• float

t

## Specification

```lsl
rotation rLin(rotation x, rotation y, float t) {
    float ang = llAngleBetween(x, y);
    if(ang > PI) ang -= TWO_PI;
    return x * llAxisAngle2Rot(llRot2Axis(y/x)*x, ang*t);
}
// Released into public domain. By Nexii Malthus.
```

## Examples

```lsl
rotation x = llEuler2Rot(<0,0,30*DEG_TO_RAD>);
rotation y = llEuler2Rot(<0,0,90*DEG_TO_RAD>);
rotation z = rLin(x, y, 0.5); // z equivalent to euler rotation of 60 degrees on Z axis
llOwnerSay((string)(llRot2Euler(z)*RAD_TO_DEG)); // <0.00000, 0.00000, 60.00001>
```

---

## Subpage: Linear/Vectors

/LSL


Interpolation/Linear/Vectors

- 1 Summary
- 2 Specification
- 3 Examples

## Summary

 Function: vector **pLin**( list v, float t, integer Loop );

Linearly interpolates between two vector points in a list of vectors that define a path.Returns a vector

• list

v

• float

t

–

Ranges between [0, 1]

• integer

Loop

–

Whether the list is a curved line or loops into a closed shape.

## Specification

```lsl
vector pLin(list v, float t, integer Loop) {
    integer l = llGetListLength(v); t *= l-1;
    integer f = llFloor(t); t -= f;
    return llList2Vector(v,pIndex(f,l,Loop))*(1-t) + llList2Vector(v,pIndex(f+1,l,Loop))*t;
}
integer pIndex( integer Index, integer Length, integer Loop) {
    if(Loop) return Index % Length;
    if(Index < 0) return 0;
    if(Index > --Length) return Length;
    return Index;
}
// Released into public domain. By Nexii Malthus.
```

## Examples

---

## Subpage: Cosine/Float

/LSL


Interpolation/Cosine/Float

- 1 Summary
- 2 Specification
- 3 Examples

## Summary

 Function: float **fCos**( float x, float y, float t );

Cosine interpolation between two floating point values.Returns a float

• float

x

• float

y

• float

t

## Specification

```lsl
float fCos(float x, float y, float t) {
    float F = (1-llCos(t*PI))/2;
    return x*(1-F)+y*F;
}
// Released into public domain. By Nexii Malthus.
```

## Examples

---

## Subpage: Cosine/Vector

/LSL


Interpolation/Cosine/Vector

- 1 Summary
- 2 Specification
- 3 Examples

## Summary

 Function: vector **fCos**( vector x, vector y, float t );

Cosine interpolation between two vectors.Returns a vector

• vector

x

• vector

y

• float

t

## Specification

```lsl
vector vCos(float x, float y, float t) {
    float F = (1-llCos(t*PI))/2;
    return x*(1-F)+y*F;
}
// Released into public domain. By Nexii Malthus.
```

## Examples

---

## Subpage: Cosine/Rotation

/LSL


Interpolation/Cosine/Rotation

- 1 Summary
- 2 Specification
- 3 Examples

## Summary

 Function: rotation **rCos**( rotation x, rotation y, float t );

Spherical-Cosine interpolation between two rotations.Returns a rotation

• rotation

x

• rotation

y

• float

t

## Specification

```lsl
rotation rCos(rotation x, rotation y, float t){
    float f = (1-llCos(t*PI))/2;
    float ang = llAngleBetween(x, y);
    if(ang > PI) ang -= TWO_PI;
    return x * llAxisAngle2Rot(llRot2Axis(y/x)*x, ang*f);
}
// Released into public domain. By Nexii Malthus.
```

## Examples

---

## Subpage: Cubic/Float

/LSL


Interpolation/Cubic/Float

- 1 Summary
- 2 Specification
- 3 Examples

## Summary

 Function: float **fCub**( float a, float b, float c, float d, float t );

Cubic interpolation between four floating point values.Returns a float

• float

a

• float

b

• float

c

• float

d

• float

t

## Specification

```lsl
float fCub(float a, float b, float c, float d,float t) {
    float P = (d-c)-(a-b);
    return P*llPow(t,3) + ((a-b)-P)*llPow(t,2) + (c-a)*t + b;
}
// Released into public domain. By Nexii Malthus.
```

## Examples

---

## Subpage: Cubic/Vector

/LSL


Interpolation/Cubic/Vector

- 1 Summary
- 2 Specification
- 3 Examples

## Summary

 Function: vector **vCub**( vector a, vector b, vector c, vector d, float t );

Cubic interpolation between four vectors.Returns a vector

• vector

a

• vector

b

• vector

c

• vector

d

• float

t

## Specification

```lsl
vector vCub(vector a, vector b, vector c, vector d, float t) {
    float P = (d-c)-(a-b);
    return P*llPow(t,3) + ((a-b)-P)*llPow(t,2) + (c-a)*t + b;
}
// Released into public domain. By Nexii Malthus.
```

## Examples

---

## Subpage: Cubic/Rotation

/LSL


Interpolation/Cubic/Rotation

- 1 Summary
- 2 Specification
- 3 Examples

## Summary

 Function: rotation **rCub**( rotation a, rotation b, rotation c, rotation d, float t );

Spherical-Cubic interpolation between four rotations.Returns a rotation

• rotation

a

–

Start

• rotation

b

–

End

• rotation

c

–

Affects path curve

• rotation

d

–

Affects path curve

• float

t

## Specification

```lsl
rotation rCub(rotation a, rotation b, rotation c, rotation d, float t){
    return rLin( rLin(a,b,t), rLin(c,d,t), 2*t*(1-t) );
}
rotation rLin(rotation x, rotation y, float t) {
    float ang = llAngleBetween(x, y);
    if(ang > PI) ang -= TWO_PI;
    return x * llAxisAngle2Rot(llRot2Axis(y/x)*x, ang*t);
}
// Released into public domain. By Nexii Malthus.
```

## Examples

---

## Subpage: Catmull-Rom/Float

/LSL


Interpolation/Catmull-Rom/Float

- 1 Summary
- 2 Specification
- 3 Examples

## Summary

 Function: float **fCos**( rotation H, float t );

Catmull-Rom cubic interpolation spline of four floats with fraction t.Returns a float

• rotation

H

–

The four floats are stored in a compact rotation format.

• float

t

## Specification

A bit more optimised:

```lsl
float fCatmullRom(rotation H, float t) {
    rotation ABCD = <
        (H.x *-0.5) + (H.y * 1.5) + (H.z *-1.5) + (H.s * 0.5),
        (H.x * 1.0) + (H.y *-2.5) + (H.z * 2.0) + (H.s *-0.5),
        (H.x *-0.5) + (H.z * 0.5), (H.y * 1.0)
    >;
    rotation T; T.s = 1.0; T.z = t; T.y = T.z*T.z; T.x = T.y*T.z;
    return T.x*ABCD.x + T.y*ABCD.y + T.z*ABCD.z + T.s*ABCD.s;
}
// Released into public domain. By Nexii Malthus.
```

With full matrix:

```lsl
rotation mCat1 = <-0.5,  1.0, -0.5,  0.0>;
rotation mCat2 = < 1.5, -2.5,  0.0,  1.0>;
rotation mCat3 = <-1.5,  2.0,  0.5,  0.0>;
rotation mCat4 = < 0.5, -0.5,  0.0,  0.0>;
float fCatmullRom(rotation H, float t) {
    rotation ABCD = <
        (H.x * mCat1.x) + (H.y * mCat2.x) + (H.z * mCat3.x) + (H.s * mCat4.x),
        (H.x * mCat1.y) + (H.y * mCat2.y) + (H.z * mCat3.y) + (H.s * mCat4.y),
        (H.x * mCat1.z) + (H.y * mCat2.z) + (H.z * mCat3.z) + (H.s * mCat4.z),
        (H.x * mCat1.s) + (H.y * mCat2.s) + (H.z * mCat3.s) + (H.s * mCat4.s)
    >;
    rotation T; T.s = 1.0; T.z = t; T.y = T.z*T.z; T.x = T.y*T.z;
    return T.x*ABCD.x + T.y*ABCD.y + T.z*ABCD.z + T.s*ABCD.s;
}
// Released into public domain. By Nexii Malthus.
```

## Examples

---

## Subpage: Hermite/Float

/LSL


Interpolation/Hermite/Float

- 1 Summary
- 2 Specification
- 3 Examples

## Summary

 Function: float **fHem**( float a, float b, float c, float d, float t, float tens, float bias );

Hermite interpolation of floating points a, b, c and d with fraction t, tension and bias.Returns a float

• float

a

• float

b

• float

c

• float

d

• float

t

• float

tens

• float

bias

## Specification

```lsl
float fHem(float a, float b, float c, float d, float t, float tens, float bias){
    float t2 = t*t;float t3 = t2*t;
    float a0 =  (b-a)*(1+bias)*(1-tens)/2;
          a0 += (c-b)*(1-bias)*(1-tens)/2;
    float a1 =  (c-b)*(1+bias)*(1-tens)/2;
          a1 += (d-c)*(1-bias)*(1-tens)/2;
    float b0 =  2*t3 - 3*t2 + 1;
    float b1 =    t3 - 2*t2 + t;
    float b2 =    t3 -   t2;
    float b3 = -2*t3 + 3*t2;
    return b0 * b + b1 * a0 + b2 * a1 + b3 * c;
}
// Released into public domain. By Nexii Malthus.
```

## Examples

---

## Subpage: Hermite/Vector

/LSL


Interpolation/Hermite/Vector

- 1 Summary
- 2 Specification
- 3 Examples

## Summary

 Function: vector **vHem**( vector a, vector b, vector c, vector d, float t, float tens, float bias );

Hermite interpolation of vectors a, b, c and d with fraction t, tension and bias.Returns a vector

• vector

a

• vector

b

• vector

c

• vector

d

• float

t

• float

tens

• float

bias

## Specification

```lsl
//A: start tangent, B: start vector, C: end vector, D: end tangent
vector vHem(vector a, vector b, vector c, vector d, float t, float tens, float bias){
    float t2 = t*t;float t3 = t2*t;
    vector a0 =  (b-a)*(1+bias)*(1-tens)/2;
           a0 += (c-b)*(1-bias)*(1-tens)/2;
    vector a1 =  (c-b)*(1+bias)*(1-tens)/2;
           a1 += (d-c)*(1-bias)*(1-tens)/2;
    float b0 =  2*t3 - 3*t2 + 1;
    float b1 =    t3 - 2*t2 + t;
    float b2 =    t3 -   t2;
    float b3 = -2*t3 + 3*t2;
    return b0 * b + b1 * a0 + b2 * a1 + b3 * c;
}
// Released into public domain. By Nexii Malthus.
```

## Examples

---

## Subpage: Spline/Vectors

/LSL


Interpolation/Spline/Vectors

- 1 Summary
- 2 Specification
- 3 Examples

## Summary

 Function: vector **pSpline**( list v, float t, integer Loop );

B-Spline Interpolation between four vector points in a list of vectors that define a path.Returns a vector

• list

v

• float

t

–

Ranges between [0, 1]

• integer

Loop

–

Whether the list is a curved line or loops into a closed shape.

## Specification

```lsl
vector pSpline(list v, float t, integer Loop) {
    integer l = llGetListLength(v); t *= l-1;
    integer f = llFloor(t); t -= f;
    float t2 = t * t; float t3 = t2 * t;
    return (
      ( (-t3 + (3.*t2) - (3.*t) + 1.) * llList2Vector(v, pIndex(f-1,l,Loop)) )
    + ( ((3.*t3) - (6.*t2) + 4.) * llList2Vector(v, pIndex(f,l,Loop)) )
    + ( ((-3.*t3) + (3.*t2) + (3.*t) + 1.) * llList2Vector(v, pIndex(f+1,l,Loop)) )
    + ( t3 * llList2Vector(v, pIndex(f+2,l,Loop)) )
    ) / 6.0;
}
integer pIndex( integer Index, integer Length, integer Loop) {
    if(Loop) return Index % Length;
    if(Index < 0) return 0;
    if(Index > --Length) return Length;
    return Index;
}
// Released into public domain. By Nexii Malthus.
```

## Examples

```lsl
//Quick Dirty Example By To-mos Codewarrior (tomos.halsey)
integer LINK_cube;integer LINK_1;
integer LINK_2;   integer LINK_3;
integer LINK_4;   integer LINK_5;
integer LINK_6;   integer LINK_7;

vector pos_1;vector pos_2;
vector pos_3;vector pos_4;
vector pos_5;vector pos_6;
vector pos_7;

getlinks()
{
    integer total=llGetNumberOfPrims()+1;
    string name;
    while((total--)-1)
    {
        name=llGetLinkName(total);
        if(name == "Cube")LINK_cube = total;
        if(name == "1")   LINK_1 = total;
        if(name == "2")   LINK_2 = total;
        if(name == "3")   LINK_3 = total;
        if(name == "4")   LINK_4 = total;
        if(name == "5")   LINK_5 = total;
        if(name == "6")   LINK_6 = total;
        if(name == "7")   LINK_7 = total;
    }
}

getPositions()
{
    pos_1 = llList2Vector(llGetLinkPrimitiveParams(LINK_1, [PRIM_POS_LOCAL]), 0);
    pos_2 = llList2Vector(llGetLinkPrimitiveParams(LINK_2, [PRIM_POS_LOCAL]), 0);
    pos_3 = llList2Vector(llGetLinkPrimitiveParams(LINK_3, [PRIM_POS_LOCAL]), 0);
    pos_4 = llList2Vector(llGetLinkPrimitiveParams(LINK_4, [PRIM_POS_LOCAL]), 0);
    pos_5 = llList2Vector(llGetLinkPrimitiveParams(LINK_5, [PRIM_POS_LOCAL]), 0);
    pos_6 = llList2Vector(llGetLinkPrimitiveParams(LINK_6, [PRIM_POS_LOCAL]), 0);
    pos_7 = llList2Vector(llGetLinkPrimitiveParams(LINK_7, [PRIM_POS_LOCAL]), 0);
}

vector bSpline(list v, float t, integer Loop) {
    integer l = llGetListLength(v); t *= l-1;
    integer f = llFloor(t); t -= f;
    float t2 = t * t; float t3 = t2 * t;
    vector out=(
      ( (-t3 + (3.*t2) - (3.*t) + 1.) * llList2Vector(v, pIndex(f-1,l,Loop)) )
    + ( ((3.*t3) - (6.*t2) + 4.) * llList2Vector(v, pIndex(f,l,Loop)) )
    + ( ((-3.*t3) + (3.*t2) + (3.*t) + 1.) * llList2Vector(v, pIndex(f+1,l,Loop)) )
    + ( t3 * llList2Vector(v, pIndex(f+2,l,Loop)) )
    ) / 6.0;
    llSetText(
        "time: "+(string)t+"\n"+
        "vector pos: "+(string)out
    ,<1.0,1.0,1.0>,1.0);
    return out;
}
integer pIndex( integer Index, integer Length, integer Loop) {
    if(Loop) return Index % Length;
    if(Index < 0) return 0;
    if(Index > --Length) return Length;
    return Index;
}

interpolate()
{
    getPositions();

    float t;
    for(t = 0; t < 1; t += 0.001)
    {
        llSetLinkPrimitiveParamsFast(LINK_cube, [PRIM_POS_LOCAL,bSpline([pos_1,pos_2,pos_3,pos_4,pos_5,pos_6,pos_7,pos_7,pos_7],t,0)]);
    }
}

default
{
    state_entry()
    {getlinks();}

    touch_start(integer num)
    {interpolate();}
}
```

---

## Subpage: Rescale/Float

/LSL


Interpolation/Rescale/Float

- 1 Summary
- 2 Specification
- 3 Examples

## Summary

 Function: float **fScl**( float from_min, float from_max, float to_min, float to_max, float from );

Rescales a value from one range to another range.Returns a float

• float

from_min

–

Minimum of range From

• float

from_max

–

Maximum of range From

• float

to_min

–

Minimum of range To

• float

to_max

–

Maximum of range To

• float

from

–

Value in range From

## Specification

```lsl
float fScl(float from_min, float from_max, float to_min, float to_max, float from) {
    return to_min + ((to_max-to_min) * ((from_min-from) / (from_min-from_max)));
}
// Released into public domain. By Nexii Malthus.
```

## Examples

```lsl
float value = fScl(0.0, 1.0, -5, 15, 0.6); // value == 7
```

---

## Subpage: Rescale/FloatFixed

/LSL


Interpolation/Rescale/FloatFixed

- 1 Summary
- 2 Specification
- 3 Examples

## Summary

 Function: float **fSclFix**( float from_min, float from_max, float to_min, float to_max, float from );

Rescales a value from one range to another range.

The value is also clamped between the range.Returns a float

• float

from_min

–

Minimum of range From

• float

from_max

–

Maximum of range From

• float

to_min

–

Minimum of range To

• float

to_max

–

Maximum of range To

• float

from

–

Value in range From

## Specification

```lsl
float fSclFix(float from_min, float from_max, float to_min, float to_max, float from) {
    from = to_min + ((to_max-to_min) * ((from_min-from) / (from_min-from_max)));
    if(to_min < to_max) {
        if(from < to_min) from = to_min; else if(from > to_max) from = to_max;
    } else {
        if(from < to_max) from = to_max; else if(from > to_min) from = to_min;
    }
    return from;
}
// Released into public domain. By Nexii Malthus.
```

## Examples

```lsl
float value = fSclFix(0.0, 1.0, -5, 15, 0.6); // value == 7
```

---

## Subpage: Target/Float

/LSL


Interpolation/Target/Float

- 1 Summary
- 2 Specification
- 3 Examples

## Summary

 Function: float **fTarget**( float Now, float Target, float Min, float Max, float Vel );

Steps float 'Now' closer using increment float 'Vel' towards 'Target' while clamping between 'Min' and 'Max'. Useful for games, simulations and vehicles. For example keeping realtime track of linear and angular acceleration and velocity of a vehicle.Returns a float

• float

Now

–

Current Value

• float

Target

–

Desired Goal

• float

Min

–

Clamp Minimum

• float

Max

–

Clamp Maximum

• float

Vel

–

Increment

## Specification

```lsl
float fTarget(float Now, float Target, float Min, float Max, float Vel) {
    if(llFabs(Target-Now) < Vel) {
        if(Target < Min) return Min;
        if(Target > Max) return Max;
        return Target;
    }
    if(Now < Target) Now += Vel; else Now -= Vel;
    if(Now < Min) Now = Min; else if(Now > Max) Now = Max;
    return Now;
}
// Released into public domain. By Nexii Malthus.
```

## Examples

```lsl
float Speed = 15.0;
float Desired = 45.0;

float Min = 0.0;
float Max = 40.0;

float Acceleration = 10.0;

Speed = fTarget(Speed, Desired, Min, Max, Acceleration); // Speed == 25.0 (Step closer to Desired)
Speed = fTarget(Speed, Desired, Min, Max, Acceleration); // Speed == 35.0 (Step closer to Desired)
Speed = fTarget(Speed, Desired, Min, Max, Acceleration); // Speed == 40.0 (Hit Max clamp)
```