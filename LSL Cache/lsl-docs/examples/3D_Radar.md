---
name: "3D Radar"
category: "example"
type: "example"
language: "LSL"
description: "Rezzes a ball for each avatar in range. Each ball tracks it's on AV and displays distance."
source_url: "https://github.com/Outworldz/LSL-Scripts/blob/master/3D_Radar/3D_Radar/Object/3D_Radar_1.lsl"
source_name: "Outworldz LSL Scripts (GitHub) / 3D_Radar"
source_owner: "Outworldz"
source_repo: "LSL-Scripts"
source_branch: "master"
source_path: "3D_Radar/3D_Radar/Object/3D_Radar_1.lsl"
source_project: "3D_Radar"
source_part_total: "2"
first_fetched: "2026-03-18"
last_updated: "2026-03-19"
has_versions: "true"
active_version: "scraped-outworldz-lsl-scripts-github-3d-radar-2026-03-19"
---

```lsl
// === Part 1/2 ===
// :CATEGORY:Radar
// :NAME:3D_Radar
// :AUTHOR:Jesse Barnett
// :KEYWORDS:
// :CREATED:2010-12-27 12:41:03.763
// :EDITED:2013-09-18 15:38:46
// :ID:4
// :NUM:6
// :REV:1.0
// :WORLD:Second Life
// :DESCRIPTION:
// Rezzes a ball for each avatar in range. Each ball tracks it's on AV and displays distance.
// :CODE:
// 
// This formula: vector avDivPos = (avPos - rPos) * 0.010417; Takes the (avatars position - position of scanner) & multiplies by (radius of the distance you want the balls to go(2 meter sphere = 1 meter radius)/scan range(96meters)):
// 
// 1/96 = approximately 0.010417. 

//////////////////////////////////////////////////////////////////////////////////////////////////////

//				3D Radar 2.5

// 				"Oct 15 2008", "18:43:28"

// 				Creator: Jesse Barnett

//				Released into the Public Domain

//////////////////////////////////////////////////////////////////////////////////////////////////////

 

integer Scan = TRUE;

string avKey;

integer list_pos;

list key_list;

integer key_chan;	//Key channel is generated randomly and passed to the scan ball

integer die_chan = -9423753;	//Hey pick your own channels and be sure to paste them into

						//the scan balls too!

integer key_rem_chan = -49222879;

default {

	state_entry() {

		llSetObjectName("3D Radar");

	}

	touch_start(integer total_number) {

		if (Scan) {

			llSensorRepeat("", "", AGENT, 96, PI, 1);

			key_list =[];

			llListen(key_rem_chan, "", "", "");

			llOwnerSay("on");

			Scan = FALSE;

		}

		else {

			llSensorRemove();

			llRegionSay(die_chan, "die");

			llOwnerSay("off");

			Scan = TRUE;

		}

	}

	sensor(integer iNum) {

		integer p = 0;

		for (p = 0; p < iNum; ++p) {

			avKey = llDetectedKey(p);

			list_pos = llListFindList(key_list, (list)avKey);

			if (list_pos == -1) {

				key_list += (list) avKey;

				key_chan = (integer) llFrand(-1000000) - 1000000;

				llRezObject("scan ball", llGetPos(), ZERO_VECTOR, ZERO_ROTATION, key_chan);

				llSleep(.25);

				llRegionSay(key_chan, avKey);

			}

		}

	}

	listen(integer c, string name, key id, string msg) {

		integer r = llListFindList(key_list,[(key)msg]);

		key_list = llDeleteSubList(key_list, r, r);

	}

}

// === Part 2/2 ===
// :CATEGORY:Radar
// :NAME:3D_Radar
// :AUTHOR:Jesse Barnett
// :KEYWORDS:
// :CREATED:2010-12-27 12:41:03.763
// :EDITED:2013-09-18 15:38:46
// :ID:4
// :NUM:7
// :REV:1.0
// :WORLD:Second Life
// :DESCRIPTION:
// DESCRIPTION: []::Rezzes a ball for each avatar in range. Each ball tracks it's on AV and displays distance
// :CODE:

// Place this script in a prim and then place the prim into the inventory of the Scanner/Rezzer. It will automatically name itself.
// 
// Suggestion; Create a sphere prim of 0.05 diameter with glow set about .80. 
//////////////////////////////////////////////////////////////////////////////////////////////////////

//				3D Radar 2.5

// 				"Oct 15 2008", "18:44:36"

// 				Creator: Jesse Barnett

//				Released into the Public Domain

//////////////////////////////////////////////////////////////////////////////////////////////////////

 

string avName;

integer avDistance;

key avKey;

integer avListen;

integer key_chan;

integer die_chan = -9423753;

integer key_rem_chan = -49222879;

vector avPos;

vector rPos;

default {

	state_entry() {

		llSetObjectName("scan ball");

	}

	on_rez(integer start_param) {

		rPos = llGetPos();

		key_chan = start_param;

		llListen(die_chan, "", "", "");

		avListen = llListen(key_chan, "", "", "");

	}

	listen(integer c, string n, key id, string msg) {

		if (c == die_chan)

			llDie();

		else {

			avKey = (key) msg;

			avName = llKey2Name(avKey);

			llSensorRepeat("", avKey, AGENT, 96, PI, 1.0);

			llListenRemove(avListen);

		}

	}

	sensor(integer n) {

		avPos = llDetectedPos(0);

		vector avDivPos = (avPos - rPos) / (96 / 1);	//Scan range/Radius of large sphere

		avDistance = (integer) llVecDist(rPos, llDetectedPos(0));

		llSetPos(rPos + avDivPos);

		llSetText(avName + "[" + (string) avDistance + "]", <1, 1, 1 >, 1);

	}

	no_sensor() {

		llRegionSay(key_rem_chan, avKey);

		llDie();

	}

}
```
