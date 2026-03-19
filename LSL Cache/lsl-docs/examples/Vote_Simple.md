---
name: "Vote Simple"
category: "example"
type: "example"
language: "LSL"
description: "Simple voting script. One avi, one vote with a click."
wiki_url: "https://wiki.secondlife.com/wiki/Vote_Simple"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Simple voting script. One avi, one vote with a click.

```lsl
//  Voting script, only allows one vote per avi
//  by JB Kraft

string thankYouMessage = "Thanks for voting";
string floatText = "Vote for me!";

//  _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
//  _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

integer numberOfVotes;
list listOfVoterNames;

update_floattext()
{
//  set white and opaque floattext
    llSetText(floatText + "\n"
        + (string)numberOfVotes + " votes", <1.0, 1.0, 1.0>, (float)TRUE);
}

integer added_vote(key id)
{
//  cut list if memory shortage
    if(llGetFreeMemory() < 5000)
        listOfVoterNames = llList2List(listOfVoterNames, -50, -1);

    string avatarLegacyName = llKey2Name(id);

//  TRUE if found, else FALSE
//  watch out, this is bit-wise NOT (~) not minus (-)
    integer thisAvatarHasVotedAlready = ~llListFindList(listOfVoterNames, [avatarLegacyName]);

    if (thisAvatarHasVotedAlready)
        return FALSE;
//  else
//  {
        listOfVoterNames += [avatarLegacyName];
        numberOfVotes = llGetListLength(listOfVoterNames);

        update_floattext();

        return TRUE;
//  }
}

default
{
    on_rez(integer start_param)
    {
        llResetScript();
    }

    state_entry()
    {
        update_floattext();
    }

    touch_start(integer num_detected)
    {
        key id = llDetectedKey(0);

        if( added_vote(id)  && thankYouMessage != "" )
            llInstantMessage(id, thankYouMessage);
    }
}
```