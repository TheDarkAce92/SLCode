---
name: "Aim Detection"
category: "example"
type: "example"
language: "LSL"
description: "This script detects who's aiming at you with mouselook"
source_url: "https://github.com/Outworldz/LSL-Scripts/blob/master/Aim_Detection/Aim_Detection/Object/Aim_Detection_1.lsl"
source_name: "Outworldz LSL Scripts (GitHub) / Aim_Detection"
source_owner: "Outworldz"
source_repo: "LSL-Scripts"
source_branch: "master"
source_path: "Aim_Detection/Aim_Detection/Object/Aim_Detection_1.lsl"
source_doc_kind: "script"
source_project: "Aim_Detection"
source_project_dir: "Aim_Detection"
source_project_confidence: "medium"
first_fetched: "2026-03-18"
last_updated: "2026-03-19"
has_versions: "true"
active_version: "scraped-outworldz-lsl-scripts-github-aim-detection-2026-03-19"
---

```lsl
// :CATEGORY:Combat
// :NAME:Aim_Detection
// :AUTHOR:Unrevoked Clarity
// :CREATED:2010-12-27 12:46:31.257
// :EDITED:2013-09-18 15:38:47
// :ID:21
// :NUM:31
// :REV:1.0
// :WORLD:Second Life
// :DESCRIPTION:
// This script detects who's aiming at you with mouselook
// :CODE:
//This script was designed by Han Shuffle

//Cleaned up a bit by another resident.

//Cleaned up some more by another resident.

 

default

{

    state_entry()

    {

        llSetText("", <1.0, 1.0, 1.0>, 1.0);

        llSensorRepeat("", "", AGENT, 90, PI, 0.1);

    }

    sensor(integer n)

    {

        integer i;

        list sweep;

        for (i=0;i<n;++i)

        {

            if (llGetAgentInfo(llDetectedKey(i)) & AGENT_MOUSELOOK)

            {

                if (llVecDist(llGetPos(), llDetectedPos(i)+llRot2Fwd(llDetectedRot(i))*llVecDist(llGetPos(),llDetectedPos(i))) < 1.5)

                    sweep += llDetectedName(i);

            }

            if (i == n-1)

                llSetText(llDumpList2String( sweep, "\n"), <1.0, 1.0, 1.0>, 1.0);

        }

    }

}
```
