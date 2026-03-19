---
name: "llSetKeyframedMotion"
category: "function"
type: "function"
language: "LSL"
description: 'Specify a list of positions, orientations, and timings to be followed by an object. The object will be smoothly moved between those keyframes by the simulator.

Collisions with other nonphysical or keyframed objects will be ignored (no script events will fire and collision processing will not occur)'
signature: "void llSetKeyframedMotion(list keyframes, list options)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetKeyframedMotion'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsetkeyframedmotion"]
---

Specify a list of positions, orientations, and timings to be followed by an object. The object will be smoothly moved between those keyframes by the simulator.

Collisions with other nonphysical or keyframed objects will be ignored (no script events will fire and collision processing will not occur). Collisions with physical objects will be computed and reported, but the keyframed object will be unaffected by those collisions. (The physical object will be affected, however.)


## Signature

```lsl
void llSetKeyframedMotion(list keyframes, list options);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `list` | `keyframes` | Strided keyframe list of the form:
* ''vector'' position (optional via KFM_TRANSLATION and KFM_DATA)
* ''rotation'' orientation (optional via KFM_ROTATION and KFM_DATA)
* ''float'' time

Each keyframe is interpreted relative to the previous transform of the object. Time values must be 1/9s. or greater. For example, consider the following list of keyframes:
 [<0, 0, 10>, ZERO_ROTATION, 5, <0, 0, 0>, ZERO_ROTATION, 5, <0, 0, -10>, ZERO_ROTATION, 5]
This would cause the object to move up 10m over the course of 5s. It would then remain at the location for 5s before moving down 10m over the course of another 5s.

An empty list will terminate any keyframed animation currently playing. |
| `list (instructions)` | `options` | modifiers and future options |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetKeyframedMotion)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetKeyframedMotion) — scraped 2026-03-18_

Specify a list of positions, orientations, and timings to be followed by an object. The object will be smoothly moved between those keyframes by the simulator.

## Caveats

- This function does not work in attachments.
- This function can only be called on NON-physical objects. In the future it could be extended to support physical objects, but this is more complicated as collisions could prevent the object from reaching its goal positions on time.
- You cannot use scripts to move any prim in the linkset while the keyframed motion is active. If you must, first pause and restart it with KFM_CMD_PLAY when done. #Example
- Collisions with avatars affect the angular movement of the object and it may not reach the final rotation.
- This function can only be called on the root prim of a linkset.
- This function requires the linkset to use the Prim Equivalency system. However, it keyframed objects will not receive the dynamics penalty and can have a physics weight of up to 64.
- Linear velocity greater than Second Life's maximum of 250 meters per second will produce an error on DEBUG_CHANNEL.
- llSetKeyframedMotion is implemented in terms of frames and not real time. To avoid a drift from the expected positions and rotations, use times which are integer multiples of 1/45, e.g. 20.0/45.0, 40.0/45.0, 90.0/45.0, etc. [Forum Thread](http://community.secondlife.com/t5/LSL-Scripting/llSetKeyframedMotion-turning-a-corner/td-p/1225219) KFM claims delta times must be larger than 0.1 seconds; in practice, however, delta times slightly over 0.1 will produce an error on DEBUG_CHANNEL. Testing shows a minimum delta time is about 6/45 (.13333) seconds.

  - Natural drift can still occur; for best results use moving_end to determine when the animation has ended and confirm the target position with llSetPos.  Or you can use at_target or at_rot_target.
- There are a few bugs in the avatar animation system that may cause strange looking animations to play when standing on a moving platform (e.g., walking in place, feet-at-pelvis). We hope to fix these in the future, but doing so is out of scope for this feature.
- As with dynamic objects, objects moving using this function are paused when they are selected by an avatar with adequate permissions (object owner, passenger, etc). When such an avatar deselects the object, motion resumes, even if the object had been paused using KFM_CMD_PAUSE.
- A Key Framed Motion is a **prim property** in some respect. When a KFM_LOOP or KFM_PING_PONG is initiated the **the motion** is **preserved after the script is removed**. I.E. The prim will continue what motion it had. It will survive take and copy. It will survive server restart.
- Inter region movement is far from perfect. Crossing from sim 1 to sim 2 using a Key Frame list with numerous frames on a curved path will pick up conspicuous errors on the crossing and when reversed by [ KFM_MODE, KFM_REVERSE ] the object will stay in sim 2 and never return to sim 1

## Examples

A KFM object must use the new Prim Equivalency system in order to work. One of many ways to achieve this is to make sure the object uses Convex Hull for its physics shape. (Mainly new prims need a workaround like this. Mesh objects always use the new Prim Equivalency system.)

```lsl
llSetLinkPrimitiveParamsFast(LINK_THIS, [PRIM_PHYSICS_SHAPE_TYPE, PRIM_PHYSICS_SHAPE_CONVEX]);
```

This is a simple example of back-and-forth or "ping pong" motion, using only positions and time.

```lsl
llSetKeyframedMotion([<0.0, 0.0, 10.0>, 5, <0.0, 0.0, -10.0>, 5], [KFM_DATA, KFM_TRANSLATION, KFM_MODE, KFM_PING_PONG]);
```

This example includes position, rotation, and time.

```lsl
llSetKeyframedMotion(
    [<0.0, 0.0, 10.0>, llEuler2Rot(<90, 45, 180> * DEG_TO_RAD), 5,
     <0.0, 0.0, -10.0>, llEuler2Rot(<270, 225, 360> * DEG_TO_RAD), 5],
    [KFM_MODE, KFM_REVERSE]);
```

### Pause-Play

If you need to update a KFM object's position, you will need to pause KFM and continue it afterwards.

```lsl
llSetKeyframedMotion([],[KFM_COMMAND, KFM_CMD_PAUSE]);
// Modify prim positions here
llSetKeyframedMotion([],[KFM_COMMAND, KFM_CMD_PLAY]);
```

### Sample Script - Key Framed Follower

Under some circumstances, rotations will generate a run-time error unless they are normalized. This script illustrates a way to use llKeyframedMotion to create a follower -- think, for example, of a cart behind a vehicle -- using normalized target rotation.

```lsl
key scriptedObjectToFollow = "daf4847b-967d-bff6-69c0-fd7022241be7";
integer isSensorRepeatOn;

rotation NormalizeRotation(rotation Q)
{
    float MagQ = llSqrt(Q.x*Q.x + Q.y*Q.y +Q.z*Q.z + Q.s*Q.s);
    return ;
}

default
{
    state_entry()
    {
        llSetLinkPrimitiveParamsFast(LINK_ROOT, [
            PRIM_PHYSICS_SHAPE_TYPE, PRIM_PHYSICS_SHAPE_CONVEX,
            PRIM_LINK_TARGET, LINK_ALL_CHILDREN,
            PRIM_PHYSICS_SHAPE_TYPE, PRIM_PHYSICS_SHAPE_NONE
        ]);
    }

    touch_start(integer total_number)
    {
        isSensorRepeatOn = !isSensorRepeatOn;

        if (isSensorRepeatOn)
        {
            llSay(PUBLIC_CHANNEL, "Sensor repeat switched on!");
            llSensorRepeat("", scriptedObjectToFollow, SCRIPTED, 10.0, PI, 0.3);
        }
        else
        {
            llSensorRemove();
        }
    }

    sensor(integer num_detected)
    {
        vector ownPosition = llGetPos();
        rotation ownRotation = llGetRot();
        vector detectedPosition = llDetectedPos(0);
        rotation detectedRotation = llDetectedRot(0);

        vector kfmPosition = (detectedPosition - ownPosition) + <-1.0, 0.0, 0.2> * detectedRotation;
        rotation kfmRotation = NormalizeRotation(detectedRotation / ownRotation);
        llSetKeyframedMotion([kfmPosition, kfmRotation, 0.15], []);
    }
}
```

### Universal Hinged Motion in 8 Key Frames

The script will turn a box prim around one edge parallel to the prim's Y-axis

The script will work for any prim orientation

Note that the smallest accepted time per frame is 1/9S=0.11111111S and NOT 0.1S

```lsl
float angleEnd=PI_BY_TWO;
float speed=0.2; // m/S
float steps=8.0; // number of Key Frames
float step=0.0;
list KFMlist=[];
vector V;
integer open=TRUE;
vector basePos;
rotation baseRot;

float motion_time( float mt)
{
    mt = llRound(45.0*mt)/45.0;
    if ( mt > 0.11111111 ) return mt;
    else return 0.11111111;
}

default
{
    state_entry()
    {
        llSetMemoryLimit(0x2000);
        llSetPrimitiveParams([PRIM_PHYSICS_SHAPE_TYPE, PRIM_PHYSICS_SHAPE_CONVEX]);
        basePos = llGetPos();
        baseRot = llGetRot();
        vector v1 = 0.5*llGetScale()*llGetRot();
        rotation deltaRot = llEuler2Rot(< 0.0, angleEnd/steps, 0.0>);
        while ( step < steps )
        {
            V = v1*llAxisAngle2Rot(llRot2Left(llGetRot()), angleEnd*step/steps);
            V = v1*llAxisAngle2Rot(llRot2Left(llGetRot()), angleEnd*(step+1.0)/steps) - V;
            KFMlist += [V, deltaRot, motion_time(llVecMag(V)/speed)];
            step += 1.0;
        }
    }
    touch_end( integer n)
    {
        llSetKeyframedMotion( [], []);
        if ( open )
        {
            llSetPrimitiveParams([PRIM_POSITION, basePos, PRIM_ROTATION, baseRot]);
            llSetKeyframedMotion( KFMlist, []);
        }
        else
        {
            llSetKeyframedMotion( KFMlist, [KFM_MODE, KFM_REVERSE]);
        }
        open = !open;
    }
    on_rez( integer n) { llResetScript(); }
}
```

After editing prim position, rotation and/or size the script should be reset in order to update the motion

### Continuous Spin

The following example does the same thing as using llTargetOmega(<0.0,0.0,1.0>,PI,1.0) to make a prim rotate continuously around its Z-axis, assuming that the prim is set to convex hull and is non-physical.

```lsl
integer gON;

default
{
    touch_end(integer total_number)
    {
        if (gON = !gON)
        {
            // Make repeated rotations of PI radians, each taking 1 seconds
            rotation r = llEuler2Rot(<0.0, 0.0, PI>);
            llSetKeyframedMotion(
                [
                    r, 1,
                    r, 1
                ],
                [KFM_DATA, KFM_ROTATION, KFM_MODE, KFM_LOOP]
            );
            return;
        }

        llSetKeyframedMotion([], []);
    }
}
```

### More Examples

- 3D Spinning Pendulum Motion, Suitable for spinning tops, swings, tire swings. Highly configurable
- Oscillator Motion in 12 Key Frames
- Simple Pendulum Motion in 24 Key Frames, a good motion for a swing

## Notes

Potential Use Cases:

- Elevators
- Moving platforms
- Trains/Fixed-Track Vehicles
- Moving doors/walls/gates
- Windmills and other machines

Targeted coordinate systems: The Translation is in Global coordinates, the Rotation in Local coordinates

- Say: a move on the X-axis will move the object along the global, region X-axis no matter how the object is rotated
- Say: a rotate around the X-axis will rotate the object around it's local, prim X-axis no matter the object's rotation
- When the object is not rotated in the global system you won't notice the difference

<!-- /wiki-source -->
