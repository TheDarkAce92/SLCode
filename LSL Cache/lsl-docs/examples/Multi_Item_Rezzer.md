---
name: "Multi Item Rezzer"
category: "example"
type: "example"
language: "LSL"
description: "This is a rework of my old High Altitude Rezzer."
wiki_url: "https://wiki.secondlife.com/wiki/Multi_Item_Rezzer"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- Click Here  To see my page and more of my scripts



This is a rework of my old High Altitude Rezzer.

Sit on it, pick the object to rez and then the height. It will go up to the target height and rez the object. It allows the owner to set the rez offset simply. Also has a scanner built in, if there is no av around the rezzer will derez the object and go back to its starting position.

Place this in the item you wish to be the rezzer to set the sit target and follow the onscreen instructions. It will remove itself once the sit target is set. Without a sit target the rezzer will not work.

```lsl
//////////////////////////////////////////////////////////////////////////////////////////////////////
//				Set SitTarget 1.0
// 				"Dec 14 2008", "15:30:50"
// 				Creator: Jesse Barnett
//				Released into the Public Domain
//////////////////////////////////////////////////////////////////////////////////////////////////////

vector pos;
rotation rot;
rotation adj_rot;

default {
	state_entry() {
		llSetClickAction(CLICK_ACTION_SIT);
		llOwnerSay("Go into edit and check the Edit linked parts box" +
					"\nMove the prim to the postion you want" +
					"\Touch the prim to set the llSitTarget & remove the script" +
					"\nSit Target is a property of the prim and doesn't need" +
					"\nthe script, once set" +
					"\nPut the prim where you want and when you sit on it" +
					"\nyou will be in the right position ");
		pos = llGetPos();
		rot = llGetRot();
		adj_rot = ZERO_ROTATION / rot;
		llSitTarget(<0, 0, 0.01 >, adj_rot);
	}
	touch_start(integer total_number) {
		vector new_pos = (pos - llGetPos()) * adj_rot;
		llSitTarget(new_pos, adj_rot);	//applies offset
		llSetPos(pos);	//back to original position and rotation
		llSetRot(rot);
		llOwnerSay(" Sit Target has been set ");
		llRemoveInventory(llGetScriptName());
	}
}
```

Place a copy of this into each linkset of the objects you wish to rez, take into inventory and then place in the rezzer. The rezzer will work with collated builds. (Again make sure there is a die script in each linkset)

```lsl
//////////////////////////////////////////////////////////////////////////////////////////////////////
//				Rezzed Object Die 1.0
// 				"Dec 14 2008", "11:19:14"
// 				Creator: Jesse Barnett
//				Released into the Public Domain
//////////////////////////////////////////////////////////////////////////////////////////////////////

//Place a copy inside each linkset and the rezzed object will delete itself when the rezzer moves
default {
    on_rez(integer sp) {
        llListen(sp,"","","die");
    }
    listen(integer channel, string name, key id, string msg) {
        llDie();
    }
}
```

And finally this is the script for the rezzer itself. Enjoy!

```lsl
//////////////////////////////////////////////////////////////////////////////////////////////////////
//				Multi Item Rezzer 3.0
// 				"Dec 14 2008", "18:03:38"
// 				Creator: Jesse Barnett
//				Released into the Public Domain
//////////////////////////////////////////////////////////////////////////////////////////////////////

//Set the sit target in the item you want to use as the rezzer first
//See my llSitTarget Set for one way of setting it
//Then place this script plus the objects you want to rezz into the rezzer.
float sensorRange = 20.0;
integer index;
integer menuChan;
integer menuHandle;
integer offsetTest = 0;
integer rezTest = 0;
key id;
//You can change the heights that you want for destinations here in this list.
list destList =["start", "ground", "100", "200", "500", "1000", "2000", "3000", "4000"];
list objList;
list offsetList;
string rezObj;
vector infVec = <1.304382E+19, 1.304382E+19, 0.0 >;
vector rezOffset = <0, 0, 0 >;
vector startPos;
vector target;

inventory()
{
	objList =[];
	integer invCnt = llGetInventoryNumber(INVENTORY_OBJECT);
	integer x;
	for (x = 0; x < invCnt; x++) {
		objList += (list) llGetInventoryName(INVENTORY_OBJECT, x);
		offsetList += <0, 0, 0 >;
	}
}

posJump()
{
	llSetPrimitiveParams([PRIM_POSITION, infVec, PRIM_POSITION, target]);
}

default {
	state_entry() {
		llSetClickAction(CLICK_ACTION_SIT);
		startPos = llGetPos();
		llSetText("Sit and pick from menu", <0, 0, 0 >, 1.0);
		menuChan = (integer) llFrand(-1000000) - 1000000;
		inventory();
	}
	on_rez(integer start_param) {
		llSetClickAction(CLICK_ACTION_SIT);
		startPos = llGetPos();
	}
	listen(integer channel, string name, key id, string msg) {
		if ("Height" == msg)
			llDialog(id, "Pick an elevation", destList, menuChan);
		else if ("Object" == msg)
			llDialog(id, "Pick an object", objList, menuChan);
		else if ("Set Offset" == msg) {
			llOwnerSay("Move seat to desired position then touch again to set offet" + "\nMaximum 10 meters");
			offsetTest = 1;
		}
		else if (~llListFindList(destList,[msg]) && llAvatarOnSitTarget() != NULL_KEY) {
			llSay(menuChan, "die");
			target = startPos;
			if (msg == "ground") {
				vector primSize = llGetScale();
				target.z = llGround(ZERO_VECTOR) + (primSize.z / 2);
				llSensorRemove();
			}
			else if (msg == "start") {
				target = startPos;
				llSensorRemove();
			}
			else {
				target.z = (float) msg;
				rezTest = 1;
			}
			posJump();
			if (rezTest) {
				if (rezObj == "")
					rezObj = llGetInventoryName(INVENTORY_OBJECT, 0);
				llRezObject(rezObj, llGetPos() + rezOffset, ZERO_VECTOR, ZERO_ROTATION, menuChan);
				rezTest = 0;
				llSensorRepeat("", "", AGENT, sensorRange, PI, 60.0);
			}
			llUnSit(llAvatarOnSitTarget());
		}
		else if (~llListFindList(objList,[msg])) {
			index = llListFindList(objList,[msg]);
			rezObj = msg;
			rezOffset = llList2Vector(offsetList, index);
			llDialog(id, "Pick an elevation", destList, menuChan);
		}
	}
	touch_start(integer total_number) {
		if (!offsetTest) {
			id = llDetectedKey(0);
			menuHandle = llListen(menuChan, "", "", "");
			if (llGetOwner() == id) {
				llDialog(id, "Choice",["Height", "Object", "Set Offset"], menuChan);
			}
			else {
				llDialog(id, "Choice",["Height", "Object"], menuChan);
			}
		}
		else {
			if (llVecDist(target, llGetPos()) > 10)
				llOwnerSay("Too far. Try again");
			else {
				rezOffset = (target - llGetPos()) + rezOffset;
				offsetList = llListReplaceList(offsetList,[rezOffset], index, index);
				offsetTest = 0;
				llListenRemove(menuHandle);
				llUnSit(llAvatarOnSitTarget());
			}
		}
	}
	sensor(integer n) {

	}
	no_sensor() {
		llSay(menuChan, "die");
		llSensorRemove();
		target = startPos;
		posJump();
	}
	changed(integer change) {
		if (CHANGED_INVENTORY & change) {
			inventory();
		}
		else if (CHANGED_LINK & change) {
			if (llAvatarOnSitTarget() != NULL_KEY) {
				key id = llAvatarOnSitTarget();
				llSetText("", <0, 0, 0 >, 0);
				menuHandle = llListen(menuChan, "", "", "");
				llSetClickAction(CLICK_ACTION_TOUCH);
				if (id == llGetOwner()) {
					llDialog(llAvatarOnSitTarget(), "Choice",["Height", "Object", "Set Offset"], menuChan);
				}
				else {
					llDialog(llAvatarOnSitTarget(), "Choice",["Height", "Object"], menuChan);
				}
			}
			else {
				llSetText("Sit and touch to ascend", <0, 0, 0 >, 1.0);
				llSetClickAction(CLICK_ACTION_SIT);
				llListenRemove(menuHandle);
			}
		}
		else if (CHANGED_OWNER & change) {
			llResetScript();
		}
	}
}
```