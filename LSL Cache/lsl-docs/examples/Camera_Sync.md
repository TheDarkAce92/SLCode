---
name: "Camera Sync"
category: "example"
type: "example"
language: "LSL"
description: "Camera sync allows for two users to synchronize their cameras, for use by builders in joint projects or in tutorials and demonstrations."
wiki_url: "https://wiki.secondlife.com/wiki/Camera_Sync"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL

Camera sync allows for two users to synchronize their cameras, for use by builders in joint projects or in tutorials and demonstrations.

**Camera Tween** - Smoothly adjusts the position and rotation of the camera over a given number of steps:

```lsl
camTween(rotation camRot_origin, vector camPos_origin, rotation camRot_target, vector camPos_target, float steps)
{
    //Keep steps a float, but make sure its rounded off to the nearest 1.0
    steps = (float)llRound(steps);

    //Calculate camera position increments
    vector posStep = (camPos_target - camPos_origin) / steps;

    //Calculate camera rotation increments
    //rotation rotStep = (camRot_target - camRot_origin);
    //rotStep = ;


    float cStep = 0.0; //Loop through motion for cStep = current step, while cStep <= Total steps
    for(; cStep <= steps; ++cStep)
    {
        //Set next position in tween
        vector camPos_next = camPos_origin + (posStep * cStep);
        rotation camRot_next = slerp( camRot_origin, camRot_target, cStep / steps);

        //Set camera parameters
        llSetCameraParams([
            CAMERA_ACTIVE, 1, //1 is active, 0 is inactive
            CAMERA_BEHINDNESS_ANGLE, 0.0, //(0 to 180) degrees
            CAMERA_BEHINDNESS_LAG, 0.0, //(0 to 3) seconds
            CAMERA_DISTANCE, 0.0, //(0.5 to 10) meters
            CAMERA_FOCUS, camPos_next + llRot2Fwd(camRot_next), //Region-relative position
            CAMERA_FOCUS_LAG, 0.0 , //(0 to 3) seconds
            CAMERA_FOCUS_LOCKED, TRUE, //(TRUE or FALSE)
            CAMERA_FOCUS_THRESHOLD, 0.0, //(0 to 4) meters
            CAMERA_POSITION, camPos_next, //Region-relative position
            CAMERA_POSITION_LAG, 0.0, //(0 to 3) seconds
            CAMERA_POSITION_LOCKED, TRUE, //(TRUE or FALSE)
            CAMERA_POSITION_THRESHOLD, 0.0, //(0 to 4) meters
            CAMERA_FOCUS_OFFSET, ZERO_VECTOR //<-10,-10,-10> to <10,10,10> meters
        ]);
    }
}

rotation slerp( rotation a, rotation b, float f ) {
    float angleBetween = llAngleBetween(a, b);
    if ( angleBetween > PI )
        angleBetween = angleBetween - TWO_PI;
    return a*llAxisAngle2Rot(llRot2Axis(b/a)*a, angleBetween*f);
}//Written by Francis Chung, Taken from http://forums-archive.secondlife.com/54/3b/50692/1.html
```

**Camera Default** - Sets the camera parameters back to their defaults:

```lsl
camDefault()
{
    llSetCameraParams([
        CAMERA_ACTIVE, FALSE, //1 is active, 0 is inactive
        CAMERA_BEHINDNESS_ANGLE, 10.0, //(0 to 180) degrees
        CAMERA_BEHINDNESS_LAG, 0.0, //(0 to 3) seconds
        CAMERA_DISTANCE, 3.0, //(0.5 to 10) meters
        CAMERA_FOCUS_LAG, 0.1 , //(0 to 3) seconds
        CAMERA_FOCUS_LOCKED, FALSE, //(TRUE or FALSE)
        CAMERA_FOCUS_THRESHOLD, 1.0, //(0 to 4) meters
        CAMERA_PITCH, 0.0, //(-45 to 80) degrees
        CAMERA_POSITION_LAG, 0.1, //(0 to 3) seconds
        CAMERA_POSITION_LOCKED, FALSE, //(TRUE or FALSE)
        CAMERA_POSITION_THRESHOLD, 1.0, //(0 to 4) meters
        CAMERA_FOCUS_OFFSET, ZERO_VECTOR //<-10,-10,-10> to <10,10,10> meters
    ]);
}
```

**Camera Match** - Sets a prim's position and rotation to that of the user's camera (the one we have permissions for):

```lsl
warpPos(vector destpos)
{
    integer jumps = (integer)(llVecDist(destpos, llGetPos()) / 10.0) + 1;
    list rules = [PRIM_POSITION, destpos];
    integer count = 1;
    while (( count = count << 1 ) < jumps)
    {
        rules = (rules=[]) + rules + rules;
    }
    llSetPrimitiveParams(rules + llList2List(rules, (count - jumps) << 1, count));
}
camMatch()
{
    warpPos(llGetCameraPos());
    llSetRot(llGetCameraRot());
}
```

Note: **Camera Match** utilizes WarpPos to enable the camera tracking prim to jump great distances in an efficient manner.