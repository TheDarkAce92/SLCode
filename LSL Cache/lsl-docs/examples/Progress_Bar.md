---
name: "Progress Bar"
category: "example"
type: "example"
language: "LSL"
description: "<a href=\"http://zetaphor.wikidot.com/floating-text-progress-bar\">http://zetaphor.wikidot.com/floating-text-progress-bar</a>"
source_url: "https://github.com/Outworldz/LSL-Scripts/blob/master/Progress_Bar/Progress_Bar/Object/Progress_Bar_1.lsl"
source_name: "Outworldz LSL Scripts (GitHub) / Progress_Bar"
source_owner: "Outworldz"
source_repo: "LSL-Scripts"
source_branch: "master"
source_path: "Progress_Bar/Progress_Bar/Object/Progress_Bar_1.lsl"
source_doc_kind: "script"
source_project: "Progress_Bar"
source_project_dir: "Progress_Bar"
source_project_confidence: "medium"
first_fetched: "2026-03-18"
last_updated: "2026-03-19"
has_versions: "true"
active_version: "scraped-outworldz-lsl-scripts-github-progress-bar-2026-03-19"
---

```lsl
// :CATEGORY:Effects
// :NAME:Progress_Bar
// :AUTHOR:Zetaphor
// :CREATED:2013-03-29 18:19:09.220
// :EDITED:2013-09-18 15:39:00
// :ID:662
// :NUM:902
// :REV:1.0
// :WORLD:Second Life
// :DESCRIPTION:
// <a href="http://zetaphor.wikidot.com/floating-text-progress-bar">http://zetaphor.wikidot.com/floating-text-progress-bar</a>
// :CODE:


string empty = "□";

string filled = "■";

integer value;

progressbar(float percent)

{

      string progress;  // moved so it does not have to be initted - fkb

    integer x;

    integer length = llFloor(percent/10);

    while (x!=length)

    {

        progress+=filled;

        x++;

    }

    while (x!=10)

    {

        progress+=empty;

        x++;

    }

    integer dpercent = llFloor(percent);

    llSetText((string)dpercent+"%\n"+progress,<1,1,1>,1);

}



default

{

    touch_start(integer total_number)

    {

        llSetText("",<1,1,1>,1);

        value=0;

        llSetTimerEvent(0.1);

    }



    timer()

    {

        value++;

        if (value<101)

        {

            progressbar(value);

        }

        else

        {

            llSay(0,"Completed!");

            llSetTimerEvent(0);

        }

    }

}
```
