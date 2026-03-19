---
name: "Geometric Library"
category: "example"
type: "example"
language: "LSL"
description: "Please vote for: https://jira.secondlife.com/browse/WEB-235 So that I can expand each function into deeper detail without the page starting to fail in readability. --Nexii Malthus 23:05, 24 October 2008 (UTC)"
wiki_url: "https://wiki.secondlife.com/wiki/Geometric"
author: "Hewee Zetkin"
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

**Please vote for:**
[https://jira.secondlife.com/browse/WEB-235](https://jira.secondlife.com/browse/WEB-235)****
*So that I can expand each function into deeper detail without the page starting to fail in readability.* --Nexii Malthus 23:05, 24 October 2008 (UTC)

```lsl
:Break it up so each major section has its own page... thats why hypertext was invented. -Overbrain Unplugged 13:36, 10 October 2010 (UTC)
```

## Geometric Library

- 1 Geometric Library

  - 1.1 Line Functions

  - 1.1.1 Line and Point, Vector
  - 1.1.2 Line and Point, Distance
  - 1.1.3 Line Nearest Point, Nearest Point
  - 1.1.4 Line and Line, Vector
  - 1.1.5 Line and Line, Distance
  - 1.1.6 Line and Line, Nearest point
  - 1.1.7 Line and Line, intersection point
  - 1.1.8 Line and Line, two nearest points of lines
  - 1.1.9 Line and Line, nearest line
  - 1.1.10 Line and Line Segments, nearest line segment
  - 1.1.11 Line and Line, two nearest points with vector and distance
  - 1.1.12 Line and Point, Direction
  - 1.2 Plane Functions

  - 1.2.1 Plane and Point, Distance
  - 1.2.2 Plane and Point, Vector
  - 1.2.3 Plane and Point, Nearest point
  - 1.2.4 Plane and Ray, Intersection Distance
  - 1.2.5 Plane and Ray, Vector
  - 1.2.6 Plane and Ray, Intersection Point
  - 1.2.7 Plane and Line, Intersection Point
  - 1.2.8 Plane and Plane, Intersection Line
  - 1.2.9 Plane and Ray, Projection
  - 1.3 Sphere Functions

  - 1.3.1 Sphere and Ray, Intersection Point
  - 1.3.2 Sphere and Ray, Intersection Boolean
  - 1.4 Ray Functions

  - 1.4.1 Ray and Point, projected distance
  - 1.5 Box Functions

  - 1.5.1 Box and Ray, Intersection Distance
  - 1.5.2 Box and Ray, Intersection Point
  - 1.5.3 Box and Point, Intersection Boolean
  - 1.5.4 Box and Point, Nearest Point on Edge
  - 1.6 Cylinder

  - 1.6.1 Cylinder and Point, Intersection Boolean
  - 1.7 Polygon

  - 1.7.1 Polygon and Point, Intersection Boolean
  - 1.7.2 Polygon and Line Segment, Intersection Boolean
  - 1.8 Other Functions

  - 1.8.1 3D Projection
  - 1.8.2 Reflection
  - 1.9 Glossary
  - 1.10 Licenses

  - 1.10.1 #1
  - 1.10.2 #2

### Line Functions

#### Line and Point, Vector

Calculates the vector from a point '**to'** the closest point on a line

```lsl
vector gLXdV(vector O,vector D,vector A){
    return (O-A)-((O-A)*D)*D;}
```

Input

Description

vector O

Origin of Line

vector D

Direction of Line

vector A

Origin of Point

Output

Description

return vector gLXdV

Returns origin of closest point on Line to Point

**3D**

By Nexii Malthus

#### Line and Point, Distance

Calculates distance of line to point, same as measuring magnitude of Line and Point Vector, but faster on it's own

```lsl
float gLXdZ(vector O,vector D,vector A){
    vector k = ( A - O ) % D;
    return llSqrt( k * k );}
```

Input

Description

vector O

Origin of Line

vector D

Direction of Line (unit vector)

vector A

Origin of Point

Output

Description

return float gLXdZ

Returns numerical distance from Line to Point

**3D**

By Nexii Malthus

#### Line Nearest Point, Nearest Point

Returns nearest point on line to given point

```lsl
vector gLXnX(vector O,vector D,vector A){
    return gLXdV(O,D,A) + A;}
```

Input

Description

vector O

Origin of Line

vector D

Direction of Line

vector A

Origin of Point

Output

Description

return vector gLXnX

Returns nearest point on line given point

Requirement

function vector gLXdV(vector O,vector D,vector A)

**3D**

By Nexii Malthus

#### Line and Line, Vector

Shortest vector of two lines

```lsl
vector gLLdV(vector O1,vector D1,vector O2,vector D2){
    vector A = O2 - O1; vector B = D1 % D2;
    return B*( (A*B)/(B*B) );}
```

Input

Description

vector O1

Origin of Line 1

vector D1

Direction of Line 1

vector O2

Origin of Line 2

vector D2

Direction of Line 2

Output

Description

return vector gLLdV

Returns shortest vector between the two lines

**3D**

By Nexii Malthus

#### Line and Line, Distance

Returns the distance between two lines

```lsl
float gLLdZ(vector O1,vector D1,vector O2,vector D2){
    vector A = D1%D2;float B = llVecMag(A);A = ;
    return (O2-O1) * A;}
```

Input

Description

vector O1

Origin of Line 1

vector D1

Direction of Line 1

vector O2

Origin of Line 2

vector D2

Direction of Line 2

Output

Description

return float gLLdZ

Returns numerical distance between the two lines

**3D**

By Nexii Malthus

#### Line and Line, Nearest point

Closest point of two lines

```lsl
vector gLLnX(vector O1,vector D1,vector O2,vector D2){
    vector nO1 = < O1*D1, O1*D2, 0>;
    vector nO2 = < O2*D1, O2*D2, 0>;
    vector nD1 = < D1*D1, O1*D2, 0>;
    vector nD2 = < O2*D1, O2*D2, 0>;

    float t = ( nD2.x*nD1.y - nD1.x*nD2.y );

    t = ( nD2.y*(nO1.x-nO2.x) - nD2.x*(nO1.y-nO2.y) ) / t;

    return O1 + D1*t;}
```

Input

Description

vector O1

Origin of Line 1

vector D1

Direction of Line 1

vector O2

Origin of Line 2

vector D2

Direction of Line 2

Output

Description

return vector gLLnX

Returns closest point between the two lines

**2D**

By Nexii Malthus

#### Line and Line, intersection point

Computes intersection point of two lines, if there is any, else <-1,-1,-1> if none.

```lsl
vector gLLxX( vector A, vector B, vector C, vector D ){
    vector b = B-A; vector d = D-C;
    float dotperp = b.x*d.y - b.y*d.x;
    if (dotperp == 0) return <-1,-1,-1>;
    vector c = C-A;
    float t = (c.x*d.y - c.y*d.x) / dotperp;
    return ;}
```

Input

Description

vector A

Start of Line 1

vector B

End of Line 1

vector C

Start of Line 2

vector D

End of Line 2

Output

Description

return vector gLLxX

The intersection point of the two lines, else <-1,-1,-1> if none

**2D**

By Nexii Malthus

#### Line and Line, two nearest points of lines

Two closest points of two lines on each line

```lsl
vector X1;vector X2;
gLLnnXX(vector O1,vector D1,vector O2,vector D2){
    vector nO1 = < O1*D1, O1*D2, 0>;
    vector nO2 = < O2*D1, O2*D2, 0>;
    vector nD1 = < D1*D1, O1*D2, 0>;
    vector nD2 = < O2*D1, O2*D2, 0>;

    float t = ( nD2.x*nD1.y - nD1.x*nD2.y );

    t = ( nD2.y*(nO1.x-nO2.x) - nD2.x*(nO1.y-nO2.y) ) / t;

    X1 = O1 + D1*t;
    X2 = X1 + nD1%nD2;}
```

Input

Description

vector O1

Origin of Line 1

vector D1

Direction of Line 1

vector O2

Origin of Line 2

vector D2

Direction of Line 2

Output

Description

vector X1

Closest point on line 1 to line 2

vector X2

Closest point on line 2 to line 1

Requirement

global vector X1

global vector X2

**2D**

By Nexii Malthus

#### Line and Line, nearest line

Input two lines, the function will return a list containing two vectors responding to the line nearest between them. As well as two floats corresponding to the scalar value on the two line of where the line has an end located at.

```lsl
list gLLnL( vector v0, vector v1, vector v2, vector v3 ) {
    float Eps = 0.000001; vector vx; vector vy; vector va; vector vb; vector vc;
    float x; float y; float d0; float d1; float d2; float d3; float d4;
    va = v0-v2; vb = v3-v2; if(llVecMag(vb)

Input

Description

vector v0

Point on Line 1

vector v1

Point on Line 1

vector v2

Point on Line 2

vector v3

Point on Line 2

Output

Description

[vx]

Nearest point on Line 1 to Line 2

[vy]

Nearest point on Line 2 to Line 1

[x]

Scalar value representing location of vx on line 1 (range [v0,v1])

[y]

Scalar value representing location of vy on line 2 (range [v2,v3])

**3D**

By Nexii Malthus

#### Line and Line Segments, nearest line segment

Input two line segments, the function will return a list containing two vectors responding to the line segment nearest between them. As well as two floats corresponding to the scalar value on the two line segments of where the line segment has an end located at.

```lsl
list gLSLSnLS( vector v0, vector v1, vector v2, vector v3 ) {
    float Eps = 0.000001; vector vx; vector vy; vector va; vector vb; vector vc;
    float x; float y; float d0; float d1; float d2; float d3; float d4;
    va = v0-v2; vb = v3-v2; if(llVecMag(vb)1)x=1; if(y<0)y=0; else if(y>1)y=1;
    vx = v0+vc*x; vy = v2+vb*y; return [vx,vy,x,y]; }
```

Input

Description

vector v0

Start of Line Segment 1

vector v1

End of Line Segment 1

vector v2

Start of Line Segment 2

vector v3

End of Line Segment 2

Output

Description

[vx]

Nearest point on Line Segment 1 to Line Segment 2

[vy]

Nearest point on Line Segment 2 to Line Segment 1

[x]

Scalar value representing location of vx on Line Segment 1 (range [v0,v1])

[y]

Scalar value representing location of vy on Line Segment 2 (range [v2,v3])

**3D**

By Nexii Malthus

#### Line and Line, two nearest points with vector and distance

Computes two closest points of two lines, vector and distance

```lsl
vector X1;vector X2;vector V1;float Z1;
gLLnnXXVZ(vector O1,vector D1,vector O2,vector D2){
    vector nO1 = < O1*D1, O1*D2, 0>;
    vector nO2 = < O2*D1, O2*D2, 0>;
    vector nD1 = < D1*D1, O1*D2, 0>;
    vector nD2 = < O2*D1, O2*D2, 0>;

    float t = ( nD2.x*nD1.y - nD1.x*nD2.y );

    t = ( nD2.y*(nO1.x-nO2.x) - nD2.x*(nO1.y-nO2.y) ) / t;

    X1 = O1 + D1*t;
    X2 = X1 + CP(nD1,nD2);
    V1 = nD1%nD2;
    Z1 = llVecMag(V1);}
```

Input

Description

vector O1

Origin of Line 1

vector D1

Direction of Line 1

vector O2

Origin of Line 2

vector D2

Direction of Line 2

Output

Description

vector X1

Closest point on line 1 to line 2

vector X2

Closest point on line 2 to line 1

vector V1

Direction vector of line 1 to line 2

float Z1

Numerical distance of line 1 to line 2

Requirement

global vector X1

global vector X2

global vector V1

global float Z1

**2D**

By Nexii Malthus

#### Line and Point, Direction

Works out where point (X) is relative to the line of the segment (L0, L1).

```lsl
float gLSPdir( vector L0, vector L1, vector X ){
    return (L1.x - L0.x)*(X.y - L0.y) - (X.x - L0.x)*(L1.y - L0.y);
}
```

Input

Description

vector L0, vector L1

Start and End of line segment

vector X

Origin of Point

Output

Description

float isLeft( vector L0, vector L1, vector X )

Returns float, >0 is Left, 0 on Line, <0 is Right, according to line angle

**2D**

Copyright 2001, softSurfer (www.softsurfer.com) (Must accept License #2), LSL-Port By Nexii Malthus

### Plane Functions

#### Plane and Point, Distance

Finds distance of a point from a plane

```lsl
float gPXdZ(vector Pn,float Pd,vector A){
    return A * Pn + Pd;}
```

Input

Description

vector Pn

Normal of Plane (unit vector)

float Pd

Distance of Plane

vector A

Origin of Point

Output

Description

return float gPXdZ

Returns Distance between plane and point

**3D**

By Nexii Malthus

#### Plane and Point, Vector

Finds vector that points from point to nearest on plane

```lsl
vector gPXdV(vector Pn,float Pd,vector A){
    return -(Pn * A + Pd)*Pn;}
```

Input

Description

vector Pn

Normal of Plane (unit vector)

float Pd

Distance of Plane

vector A

Origin of Point

Output

Description

return vector gPXdV

Returns vector from point to closest point on plane

**3D**

By Nexii Malthus

#### Plane and Point, Nearest point

Finds closest point on plane given point

```lsl
vector gPXnX(vector Pn,float Pd,vector A){
    return A - (Pn * A + Pd) * Pn;}
```

Input

Description

vector Pn

Normal of Plane (unit vector)

float Pd

Distance of Plane

vector A

Origin of Point

Output

Description

return vector gPXnX

Returns vector of a point from closest of point to plane

**3D**

By Nexii Malthus

#### Plane and Ray, Intersection Distance

Finds distance to intersection of plane along ray

```lsl
float gPRxZ(vector Pn,float Pd,vector O,vector D){
    return -((Pn*O+Pd)/(Pn*D));}
```

Input

Description

vector Pn

Normal of Plane (unit vector)

float Pd

Distance of Plane

vector O

Origin of Ray

vector D

Direction of Ray

Output

Description

return float gPRxZ

Returns float distance of intersection between ray and plane

**3D**

By Nexii Malthus

#### Plane and Ray, Vector

Finds distance vector along a ray to a plane

```lsl
vector gPRdV(vector Pn,float Pd,vector O,vector D){
    return D * gPRxZ(Pn,Pd,O,D);}
```

Input

Description

vector Pn

Normal of Plane (unit vector)

float Pd

Distance of Plane

vector O

Origin of Ray

vector D

Direction of Ray

Output

Description

return vector gPRdV

Returns vector along a ray to a plane

Requirement

function float gPRxZ(vector Pn,float Pd,vector O,vector D)

**3D**

By Nexii Malthus

#### Plane and Ray, Intersection Point

Finds intersection point along a ray to a plane

```lsl
vector gPRxX(vector Pn,float Pd,vector O,vector D){
    return O + gPRdV(Pn,Pd,O,D);}
```

Input

Description

vector Pn

Normal of Plane (unit vector)

float Pd

Distance of Plane

vector O

Origin of Ray

vector D

Direction of Ray

Output

Description

return vector gPRxX

Returns vector point of intersection between ray and plane

Requirement

function vector gPRdV(vector Pn,float Pd,vector O,vector D)

**3D**

By Nexii Malthus

#### Plane and Line, Intersection Point

Finds interesection point of a line and a plane

```lsl
vector gPLxX(vector Pn,float Pd,vector O,vector D){
    return O + D*-( (Pn*O-Pd)/(Pn*D) );}
```

Input

Description

vector Pn

Normal of Plane (unit vector)

float Pd

Distance of Plane

vector O

Origin of Line

vector D

Direction of Line

Output

Description

return vector gPLxX

Returns vector point of intersection between line and plane

**3D**

By Nexii Malthus

#### Plane and Plane, Intersection Line

Finds line of intersection of two planes

```lsl
vector oO;vector oD;

gPPxL(vector Pn,float Pd,vector Qn,float Qd){
    oD = (Pn%Qn)/llVecMag(Pn%Qn);
    vector Cross = (Pn%Qn)%Pn;
    vector Bleh = (-Pd*Pn);
    oO = Bleh - (Qn*Cross)/(Qn*Bleh+Qd)*Cross/llVecMag(Cross);}
```

Input

Description

vector Pn

Normal of Plane 1 (unit vector)

float Pd

Distance of Plane 1

vector Qn

Normal of Plane 2 (unit vector)

float Qd

Distance of Plane 2

Output

Description

vector oO

Intersection Line's origin

vector oD

Intersection Line's direction

Requirement

global vector oO

global vector oD

**3D**

By Nexii Malthus

#### Plane and Ray, Projection

Projects a ray onto a plane

```lsl
vector oO;vector oD;

gPRpR(vector Pn,float Pd,vector O,vector D){
    oO = O - (Pn * O + Pd) * Pn;
    vector t = llVecNorm( D - (Pn*((D*Pn)/(Pn*Pn))) );t = <1.0/t.x,1.0/t.y,1.0/t.z>;
    oD = Pn%t;}
```

Input

Description

vector Pn

Normal of Plane (unit vector)

float Pd

Distance of Plane

vector O

Origin of Ray

vector D

Direction of Ray

Output

Description

vector oO

Projected Ray Origin

vector oD

Projected Ray Direction

Requirement

global vector oO

global vector oD

**3D**

By Nexii Malthus

### Sphere Functions

#### Sphere and Ray, Intersection Point

Finds intersection point of sphere and ray

```lsl
vector gSRxX(vector Sp, float Sr, vector Ro, vector Rd){
    float t; Ro -= Sp;
    if(Rd == ZERO_VECTOR) return ZERO_VECTOR;

    float a = Rd * Rd;
    float b = 2 * Rd * Ro;
    float c = (Ro * Ro)  - (Sr * Sr);

    float disc = b * b - 4 * a * c;

    if(disc < 0) return ZERO_VECTOR;

    float distSqrt = llSqrt(disc);
    float q;

    if(b < 0)
        q = (-b - distSqrt)/2.0;
    else
        q = (-b + distSqrt)/2.0;

    float t0 = q / a;
    float t1 = c / q;

    if(t0 > t1){
        float temp = t0;
        t0 = t1;
        t1 = temp;
    }

    if(t1 < 0) return ZERO_VECTOR;

    if(t0 < 0)
        t = t1;
    else
        t = t0;

    return Sp + Ro + (t * Rd);
}
```

Input

Description

vector Sp

Origin of Sphere

float Sr

Radius of Sphere

vector Ro

Origin of Ray

vector Rd

Direction of Ray

Output

Description

vector gSRxX

Returns intersection point of sphere and ray otherwise ZERO_VECTOR

**3D**

By Nexii Malthus

#### Sphere and Ray, Intersection Boolean

Finds if there is a intersection of sphere and ray

```lsl
integer gSRx(vector Sp, float Sr, vector Ro, vector Rd){
    float t;Ro = Ro - Sp;
    //vector RayOrg = llDetectedPos(x) - llGetPos();
    if(Rd == ZERO_VECTOR) return FALSE;

    float a = Rd * Rd;
    float b = 2 * Rd * Ro;
    float c = (Ro * Ro)  - (Sr * Sr);

    float disc = b * b - 4 * a * c;

    if(disc < 0) return FALSE;
    return TRUE;
}
```

Input

Description

vector Sp

Origin of Sphere

float Sr

Radius of Sphere

vector Ro

Origin of Ray

vector Rd

Direction of Ray

Output

Description

integer gSRx

Returns a boolean indicating if there is a valid intersection

**3D**

By Nexii Malthus

### Ray Functions

#### Ray and Point, projected distance

Finds projected distance of a point along a ray

```lsl
float gRXpZ(vector O,vector D,vector A){
    return (A-O)*D;}
```

Input

Description

vector O

Origin of Ray

vector D

Direction of Ray

vector A

Origin of Point

Output

Description

float gRXpZ

Returns projected distance of a point along a ray

**3D**

By Nexii Malthus

### Box Functions

#### Box and Ray, Intersection Distance

Finds intersection of a Ray to a Box and returns intersection distance, otherwise -1 if there is no legal intersection.

```lsl
float gBRxZ(vector Ro,vector Rd, vector Bo, vector Bs, rotation Br){
    vector oB = (Ro-Bo)/Br;    vector dB = Rd/Br;    vector eB = 0.5*Bs;
    float mD = -1.0;    float D;    vector X;

    if(llFabs(dB.x) > 0.000001){
        D = (-eB.x - oB.x ) / dB.x;
        if(D >= 0.0){
            X = oB + D * dB;
            if(X.y >= -eB.y && X.y <= eB.y && X.z >= -eB.z && X.z <= eB.z)
                mD = D;
        }
        D = ( eB.x - oB.x ) / dB.x;
        if (D >= 0.0){
            X = oB + D * dB;
            if(X.y >= -eB.y && X.y <= eB.y && X.z >= -eB.z && X.z <= eB.z)
                if (mD < 0.0 || mD > D)
                    mD = D;
        }
    }

    if(llFabs(dB.y) > 0.000001){
        D = (-eB.y - oB.y ) / dB.y;
        if(D >= 0.0){
            X = oB + D * dB;
            if(X.x >= -eB.x && X.x <= eB.x && X.z >= -eB.z && X.z <= eB.z)
                if (mD < 0.0 || mD > D)
                    mD = D;
        }
        D = ( eB.y - oB.y ) / dB.y;
        if (D >= 0.0){
            X = oB + D * dB;
            if(X.x >= -eB.x && X.x <= eB.x && X.z >= -eB.z && X.z <= eB.z)
                if (mD < 0.0 || mD > D)
                    mD = D;
        }
    }

    if(llFabs(dB.z) > 0.000001){
        D = (-eB.z - oB.z ) / dB.z;
        if(D >= 0.0){
            X = oB + D * dB;
            if(X.x >= -eB.x && X.x <= eB.x && X.y >= -eB.y && X.y <= eB.y)
                if (mD < 0.0 || mD > D)
                    mD = D;
        }
        D = ( eB.z - oB.z ) / dB.z;
        if (D >= 0.0){
            X = oB + D * dB;
            if(X.x >= -eB.x && X.x <= eB.x && X.y >= -eB.y && X.y <= eB.y)
                if (mD < 0.0 || mD > D)
                    mD = D;
        }
    }

    return mD;
}
```

Input

Description

vector Ro

Origin of Ray

vector Rd

Direction of Ray

vector Bo

Origin of Box

vector Bs

Size of Box

rotation Br

Rotation of Box

Output

Description

float gBRxZ

Returns distance to intersection of a ray and a box

**3D**

By [Hewee Zetkin](http://forums.secondlife.com/showpost.php?p=1984100&postcount=7)

#### Box and Ray, Intersection Point

Finds intersection of a Ray to a Box and returns intersection point, otherwise ZERO_VECTOR if there is no legal intersection.

```lsl
vector gBRxX( vector Ro, vector Rd, vector Bo, vector Bs, rotation Br){
    float k = gBRxZ(Ro,Rd,Bo,Bs,Br);
    if( k != -1.0 ) return Ro + Rd * k;
    else return ZERO_VECTOR;}
```

Input

Description

vector Ro

Origin of Ray

vector Rd

Direction of Ray

vector Bo

Origin of Box

vector Bs

Size of Box

rotation Br

Rotation of Box

Output

Description

vector gBRxX

Returns point of intersection of a ray and a box

Requirement

float gBRxZ(vector Ro,vector Rd, vector Bo, vector Bs, rotation Br)

**3D**

By [Hewee Zetkin](http://forums.secondlife.com/showpost.php?p=1984100&postcount=7)

#### Box and Point, Intersection Boolean

Finds if there is an intersection of a Point and a Box and returns boolean

```lsl
integer gBXx(vector A, vector Bo, vector Bs, rotation Br){
    vector eB = 0.5*Bs; vector rA = (A-Bo)/Br;
    return (rA.x-eB.x && rA.y-eB.y && rA.z-eB.z); }
```

Input

Description

vector A

Origin of Point

vector Bo

Origin of Box

vector Bs

Size of Box

rotation Br

Rotation of Box

Output

Description

integer gBXx(vector A, vector Bo, vector Bs, rotation Br)

Returns boolean check of intersection of a point and a box if there is one, otherwise FALSE

**3D**

By Nexii Malthus

#### Box and Point, Nearest Point on Edge

Processes point on nearest edge of box to given point

```lsl
vector gBXnEX(vector A, vector Bo, vector Bs, rotation Br){
    vector eB = 0.5*;
    vector rA = (A-Bo)/Br;

    float mD = 3.402823466E+38;
    vector X;
    list EdgesX = [< 0, eB.y, eB.z>, < 0,-eB.y, eB.z>, < 0,-eB.y,-eB.z>, < 0, eB.y,-eB.z>];
    list EdgesY = [< eB.x, 0, eB.z>, <-eB.x, 0, eB.z>, <-eB.x, 0,-eB.z>, < eB.x, 0,-eB.z>];
    list EdgesZ = [< eB.x, eB.y, 0>, <-eB.x, eB.y, 0>, <-eB.x,-eB.y, 0>, < eB.x,-eB.y, 0>];

    integer x = (EdgesX != []);
    while( x-- ){
        float y = gLXdZ( llList2Vector( EdgesX, x ), <1,0,0>, rA );

        if( rA.x > eB.x ) y += rA.x - eB.x;
        else if( rA.x < -eB.x ) y -= rA.x - -eB.x;

        if( y < mD ){ mD = y; X = gLXnX( llList2Vector( EdgesX, x ), <1,0,0>, rA ); }
    }
    x = (EdgesY != []);
    while( x-- ){
        float y = gLXdZ( llList2Vector( EdgesY, x ), <0,1,0>, rA );

        if( rA.y > eB.y ) y += rA.y - eB.y;
        else if( rA.y < -eB.y ) y -= rA.y - -eB.y;

        if( y < mD ){ mD = y; X = gLXnX( llList2Vector( EdgesY, x ), <0,1,0>, rA ); }
    }
    x = (EdgesZ != []);
    while( x-- ){
        float y = gLXdZ( llList2Vector( EdgesZ, x ), <0,0,1>, rA );

        if( rA.z > eB.z ) y += rA.z - eB.z;
        else if( rA.z < -eB.z ) y -= rA.z - -eB.z;

        if( y < mD ){ mD = y; X = gLXnX( llList2Vector( EdgesZ, x ), <0,0,1>, rA ); }
    }

    if( mD < 0.000001 ) return <-1,-1,-1>;
    if(      X.x >  eB.x ) X.x =  eB.x;
    else if( X.x < -eB.x ) X.x = -eB.x;
    if(      X.y >  eB.y ) X.y =  eB.y;
    else if( X.y < -eB.y ) X.y = -eB.y;
    if(      X.z >  eB.z ) X.z =  eB.z;
    else if( X.z < -eB.z ) X.z = -eB.z;

    return Bo + ( X * Br );}
```

Input

Description

vector A

Origin of Point

vector Bo

Origin of Box

vector Bs

Size of Box

rotation Br

Rotation of Box

Output

Description

vector gBXnEX(vector A, vector Bo, vector Bs, rotation Br)

Returns nearest point on edge of box B closest to point A. Returns <-1,-1,-1> if already on closest point.

Requirement

float gLXdZ(vector O,vector D,vector A)

vector gLXdV(vector O,vector D,vector A)

vector gLXnX(vector O,vector D,vector A)

**3D**

By Nexii Malthus

### Cylinder

#### Cylinder and Point, Intersection Boolean

Finds if there is an intersection of a Point and a Cylinder and returns boolean

```lsl
integer gCXx( vector A, vector O, rotation R, vector S ) {
    A = ( A - O ) / R;// Converts to local object frame
    return (llPow(A.x/S.x*2,2) + llPow(A.y/S.y*2,2)) <= 1. // Test radius
        && llFabs(A.z/S.z*2) <= 1.;// Test top/bottom
}
```

Input

Description

vector A

Origin of Point

vector Bo

Origin of Cylinder

vector Bs

Size of Cylinder

rotation Br

Rotation of Cylinder

Output

Description

integer gCXx( vector A, vector O, rotation R, vector S )

Returns boolean check of intersection of a point and a cylinder if there is one, otherwise FALSE

**3D**

By Nexii Malthus

### Polygon #### Polygon and Point, Intersection Boolean Figures out if point is inside of polygon or otherwise. ```lsl integer gCPXx( list CP, vector X ) {//Copyright (c) 1970-2003, Wm. Randolph Franklin; 2008, Strife Onizuka integer i = ~(CP != []); integer c = 0; if(i X.y) ^ (vj.y > X.y)){ if(vj.y != vi.y) c = c ^ (X.x Input Description list CP Vertices of Concave Polygon vector X Origin of Point Output Description integer gCPXx( list CP, vector X ) Returns TRUE if point (X) intersects concave polygon (CP), otherwise FALSE 2D

Copyright (c) 1970-2003, Wm. Randolph Franklin (Must accept License #1), LSL-Port By Strife Onizuka

#### Polygon and Line Segment, Intersection Boolean

Figures out if line segment intersects with polygon.

```lsl
integer gVPLSx( vector P0, vector P1, list VP ){
    //Copyright 2001, softSurfer (www.softsurfer.com); 2008, Nexii Malthus
    if( P0 == P1 ) return gCPXx( VP, P0 );
    float tE = 0; float tL = 1;
    float t; float N; float D;
    vector dS = P1 - P0;
    vector e; integer x; integer y = VP!=[];
    @start;
    for( x = 0; x < y; ++x ){
        e = llList2Vector( VP, x+1 ) - llList2Vector( VP, x );
        N = Perp( e, P0 - llList2Vector( VP, x ) );
        D = -Perp( e, dS );
        if( llFabs(D) < 0.00000001 )
            if( N < 0 ) return FALSE;
            else jump start;
        t = N / D;
        if( D < 0 ){
            if( t > tE ){   tE = t; if( tE > tL ) return FALSE;     }
        } else {
            if( t < tL ){   tL = t; if( tL < tE ) return FALSE;     }
    }   }
    // PointOfEntrance = P0 + tE * dS;
    // PointOfExit = P0 + tL * dS;
    return TRUE;
}
```

Input

Description

list VP

Vertices of Convex Polygon

vector P0, vector P1

Start and End of Line Segment

Output

Description

integer gVPLSx( vector P0, vector P1, list VP )

Returns TRUE if line segment (P0,P1) intersects convex polygon (VP), otherwise FALSE

Requirement

```lsl
float Perp( vector U, vector V ){ return U.x*V.y - U.y*V.x; }
```

Perpendicular dot product

integer gCPXx( list CP, vector X )

Only needed for (P0 == P1) safety catch check, so optional

**2D**

Copyright 2001, softSurfer (www.softsurfer.com) (Must accept License #2), LSL-Port By Nexii Malthus

### Other Functions

#### 3D Projection

Projects a vector A by vector B.

```lsl
vector Project3D(vector A,vector B){
    return B * ( ( A * B ) / ( B * B ) );}
```

Input

Description

vector A

First Vector

vector B

Second Vector

Output

Description

return Project3D(vector A, vector B)

Returns result of projection

**3D**

By Nexii Malthus

#### Reflection

Reflects Ray R with surface normal N

```lsl
vector Reflect(vector R,vector N){
    return R - 2 * N * ( R * N );}
```

Input

Description

vector R

Ray Normal

vector N

Surface Normal

Output

Description

return Reflect(vector R, vector N)

Returns result of reflection

**3D**

By Nexii Malthus

### Glossary

For anyone curious to the shorthand used and who wish to use a lookup table can use this as a reference. Or anyone who wishes to add a new function to the library is welcome to but it would be recommended to keep consistency.
I tried to minimize the script function names to be easily readable. All the geometric function names start with a g.

*g* (**Shape1**) (**Shape2**) (**Process**) (**Return** (*Only needed if other than integer*))

Here is the legend:

**Shorthand**

**Name**

**Description**

Geometric Types, all the shapes in the library

X

Point

vector defining a point in space

L

**L**ine

A line has an origin and a direction and is infinitely long

LS

**L**ine **S**egment

A line segment is a finite line and therefore consists of a start and end position

R

**R**ay

A ray is like a line, except it is more distinct as it defines wether it points forward or back

P

**P**lane

A 2D doubly ruled surface of infinite size

S

**S**phere

A sphere is defined by origin and radius (No ellipsoid functions available yet)

B

**B**ox

A box primitive is six sided and defined by origin, size as well as a rotation.

C

**C**ylinder

An elliptic cylinder primitive .

VP

Con**v**ex **P**olygon

Convex Polygon defined by list of vertices.

CP

Con**c**ave **P**olygon

Concave Polygon defined by list of vertices. Automatic backward compatibility with Convex Polygons.

The Process, What does it do?

d

**d**istance

Calculate distance

n

**n**earest

Calculate nearest

p

**p**roject

Calculates projection

x

Intersection

Calculates intersection

dir

**dir**ection

Calculates direction

Return, What kind of data do I get out of it?

Z

Float

Represents that a float is returned

V

**V**ector

Represents that a vector is returned

O

**O**rigin

Represents the Origin of the ray or line

D

**D**irection

Direction from the Origin

E

**E**dge

Edge of a shape, such as an edge on a box, suffix may mark special case return type

### Licenses

#### #1

```lsl
//Copyright (c) 1970-2003, Wm. Randolph Franklin
//Copyright (c) 2008, Strife Onizuka (porting to LSL)
//
//Permission is hereby granted, free of charge, to any person obtaining a copy
//of this software and associated documentation files (the "Software"), to deal
//in the Software without restriction, including without limitation the rights
//to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
//copies of the Software, and to permit persons to whom the Software is
//furnished to do so, subject to the following conditions:
//
// 1. Redistributions of source code must retain the above copyright notice,
//    this list of conditions and the following disclaimers.
// 2. Redistributions in binary form must reproduce the above copyright
//    notice in the documentation and/or other materials provided with the
//    distribution.
// 3. The name of W. Randolph Franklin may not be used to endorse or promote
//    products derived from this Software without specific prior written
//    permission.

//THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
//IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
//FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
//AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
//LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
//OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
//SOFTWARE.
```

#### #2

```lsl
// Copyright 2001, softSurfer (www.softsurfer.com); 2008, LSL-port by Nexii Malthus
// This code may be freely used and modified for any purpose
// providing that this copyright notice is included with it.
// SoftSurfer makes no warranty for this code, and cannot be held
// liable for any real or imagined damage resulting from its use.
// Users of this code must verify correctness for their application.
```