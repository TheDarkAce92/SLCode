---
name: "High Altitude Rezzer"
category: "example"
type: "example"
language: "LSL"
description: "Create something pretty to put this script in and to sit on. Place the script inside along with the object which you wish to rez. Sit on your beautiful creation and then touch it to ascend to the height you set below where it will rez your object. Stand up walk around, enjoy. When you want to return to where you started then just sit on it, delete your rezzed object and touch again."
wiki_url: "https://wiki.secondlife.com/wiki/High_Altitude_Rezzer"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- Click Here  To see my page and more of my scripts



Create something pretty to put this script in and to sit on.
Place the script inside along with the object which you wish to rez.
Sit on your beautiful creation and then touch it to ascend to the height you set below where it
will rez your object. Stand up
walk around, enjoy. When you want to return to where you started then just sit on it, delete your rezzed object and touch again.



```lsl
//High Altitude Rezzer
//Creator: Jesse Barnett
integer target_height = 4090;//Set the elevation you want to go to here. Maximum you can rez objects is 4096.
float zSpeed = 500.0;
vector x;
vector w;
list grnd;
vector ground;
vector rez_obj_offset = <0.0, 0.0, -0.5>;
//Adjust this as necessary for postion of
//rezzed object in relation to vehicle. (no more then 10.0 in any axis)
default{
    on_rez(integer start_param) {
        llResetScript();
    }
    state_entry(){
        grnd = [];
        grnd += llGetPos();
        ground = llList2Vector(grnd, 0);
        vector pos = llGetPos();
        llSetStatus(STATUS_ROTATE_X | STATUS_ROTATE_Y | STATUS_ROTATE_Z, FALSE);
        if(pos.z >= (target_height - 5)){
            state descend;
        }
        llSetText("Sit and touch to ascend", <0,0,0>,1.0);
    }
    touch_start(integer total_number){
       llSetStatus(STATUS_PHYSICS, TRUE);
        x = llGetPos();
        x.z = target_height;
        llTarget(x,50);
    }
    not_at_target(){
        llApplyImpulse(llGetMass()*<0,0,zSpeed>,FALSE);
    }
    at_target(integer ascend, vector target, vector cPos){
        llTargetRemove(ascend);
        llMoveToTarget(target,1);
        llSetTimerEvent(5.0);
    }
    timer(){
        vector pos = llGetPos();
        if(pos.z >= (target_height - 1)){
            llStopMoveToTarget();
            llApplyImpulse(-llGetMass()*llGetVel(),FALSE);
            llSetStatus(STATUS_PHYSICS, FALSE);
            llRezObject(llGetInventoryName(INVENTORY_OBJECT, 0), llGetPos() + rez_obj_offset, ZERO_VECTOR, ZERO_ROTATION, 42);
            state descend;
       }
    }
}
state descend{
    state_entry() {
        vector pos = llGetPos();
        llSetStatus(STATUS_ROTATE_X | STATUS_ROTATE_Y | STATUS_ROTATE_Z, FALSE);
        if(pos.z <= (ground.z + 5)){
            state default;
        }
        llSetText("Sit and touch to descend", <0,0,0>,1.0);
    }
    touch_start(integer total_number){
         llSetStatus(STATUS_PHYSICS, TRUE);
        w = llGetPos();
        w.z = ground.z;
        llTarget(w,50);
    }
    not_at_target(){
        llApplyImpulse(llGetMass()*<0,0,-500>,FALSE);
    }
    at_target(integer descend, vector target2, vector Pos){
        llTargetRemove(descend);
        llMoveToTarget(target2,1);
        llSetTimerEvent(5.0);
    }
    timer(){
        vector pos = llGetPos();
        if(pos.z <= (ground.z + 1)){
            llStopMoveToTarget();
            llApplyImpulse(-llGetMass()*llGetVel(),FALSE);
            llSetStatus(STATUS_PHYSICS, FALSE);
            llSetPos(ground);
            state default;
       }
    }
}
```