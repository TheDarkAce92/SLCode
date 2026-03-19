---
name: "IsPointInPolygon2D"
category: "example"
type: "example"
language: "LSL"
description: "Tests a polygon (described as a list of 2D vectors) to see if a 2D point lies within it. Useful for detecting where an event occurred within 2D space.Returns an integer TRUE if the point lies within the described polygon, FALSE if not"
wiki_url: "https://wiki.secondlife.com/wiki/IsPointInPolygon2D"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL


IsPointInPolygon2DisPointInPolygon2D

- 1 Summary
- 2 Caveats
- 3 Examples
- 4 Notes
- 5 Implementations

  - 5.1 Copyright
  - 5.2 Code

## Summary

 Function: integer **isPointInPolygon2D**( list polygon, vector point );

Tests a polygon (described as a list of 2D vectors) to see if a 2D point lies within it. Useful for detecting where an event occurred within 2D space.Returns an integer TRUE if the point lies within the described polygon, FALSE if not

• list

polygon

–

A polygon described as a list of 2D vectors for its points in around the edge order.

• vector

point

–

The point to test for, described by a 2D vector (a vector using only the x and y values)

It is possible (and fairly easy) to adapt this function to use a list of paired floats, both implementations are provided.

## Caveats

- the polygon MAY need to be a shape that can be built with triangles, it's unclear from the original if this is a requirement.
- 0,0 should NOT be a regular point on the polygon list. See notes below.

## Examples

```lsl
if (isPointInPolygon2D( [<1,1,0>, <1,2,0>, <2,2,0>, <2,1,0>], <1.5,1.5,0> )){
	llOwnerSay( "Point is in polygon" );
}else{
	llOwnerSay( "Point is not in polygon" );
}
```

```lsl
if (isPointInPolygon2D_XY( [<1,1,0>, <1,2,0>, <2,2,0>, <2,1,0>], 1.5, 1.5 )){
	llOwnerSay( "Point is in polygon" );
}else{
	llOwnerSay( "Point is not in polygon" );
}
```

## Notes

- you can have polygons with holes, either by separating the polygon list of points into distinct parts and placing a 0,0 point after each part, or by making a two partt call to the function, that uses an outer and an inner detection polygon with the inner (cutout) overriding the outer.


Implementations

This implementation is adapted from the original found [here](http://www.ecse.rpi.edu/Homepages/wrf/Research/Short_Notes/pnpoly.html). Please include the copyright comments below when using this code. See original page for indepth discussion of usage.

## Copyright

```lsl
/*//-- LSL Port 2009 Void Singer --//*/
/*//-- Copyright (c) 1970-2003, Wm. Randolph Franklin	--//*/
/*
Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:
1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimers.
2. Redistributions in binary form must reproduce the above copyright notice
   in the documentation and/or other materials provided with the distribution.
3. The name of W. Randolph Franklin may not be used to endorse or promote
   products derived from this Software without specific prior written permission

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/
```

## Code

It should be noted that this vector version is typically faster (fewer function calls), and will actually use less memory (due to the overhead of list entries). It is therefore preferable to try and re-write your script to use vectors in favour of using the float-pair version unless you have no choice.

Vector version:

```lsl
integer isPointInPolygon2D( list vLstPolygon, vector vPosTesting ){
	integer vBooInPlygn;
	integer vIntCounter = [] != vLstPolygon;
	vector  vPosVertexA = llList2Vector( vLstPolygon, vIntCounter );
	vector  vPosVertexB;

	while (vIntCounter){
		vPosVertexB = vPosVertexA;
		vPosVertexA = llList2Vector( vLstPolygon, ++vIntCounter );

		if ((vPosVertexA.y > vPosTesting.y) ^ (vPosVertexB.y > vPosTesting.y)){
			if (vPosTesting.x < (vPosVertexB.x - vPosVertexA.x) * (vPosTesting.y - vPosVertexA.y) /
			                     (vPosVertexB.y - vPosVertexA.y) +  vPosVertexA.x ){
				vBooInPlygn = !vBooInPlygn;
			}
		}
	}
	return vBooInPlygn;
}
```

Float Pair Version:

```lsl
integer isPointInPolygon2D_XY( list vLstPolygonXY, float vFltTesting_X, float vFltTesting_Y ){
	integer vBooInPlygnXY;
	integer vIntCounterXY = ([] != vLstPolygonXY);
	float   vFltVertexA_X = llList2Float( vLstPolygonXY, -2 );
	float   vFltVertexA_Y = llList2Float( vLstPolygonXY, -1 );
	float   vFltVertexB_X;
	float   vFltVertexB_Y;

	while (vIntCounterXY){
		vFltVertexB_X = vFltVertexA_X;
		vFltVertexB_Y = vFltVertexA_Y;
		vFltVertexA_X = llList2Float( vLstPolygonXY, vIntCounterXY++ );
		vFltVertexA_Y = llList2Float( vLstPolygonXY, vIntCounterXY++ );

		if ((vFltVertexA_Y > vFltTesting_Y) ^ (vFltVertexB_Y > vFltTesting_Y)){
			if (vFltTesting_X < (vFltVertexB_X - vFltVertexA_X) * (vFltTesting_Y - vFltVertexA_Y) /
			                     (vFltVertexB_Y - vFltVertexA_Y) +  vFltVertexA_X ){
				vBooInPlygnXY = !vBooInPlygnXY;
			}
		}
	}
	return vBooInPlygnXY;
}
```