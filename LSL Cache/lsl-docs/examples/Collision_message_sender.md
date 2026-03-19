---
name: "Collision message sender"
category: "example"
type: "example"
language: "LSL"
description: "Receiving a message every time that you step on a prim is annoying, so this script uses a short name store to check that the avatar has not been sent the message for at least 10 minutes. As an avatar stands on or hits against the prim, the timer is reset to a further 10 minutes, at the end of the timer period, the name list is cleared."
wiki_url: "https://wiki.secondlife.com/wiki/Collision_message_sender"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Receiving a message every time that you step on a prim is annoying, so this script uses a short name store to check that the avatar has not been sent the message for at least 10 minutes.
As an avatar stands on or hits against the prim, the timer is reset to a further 10 minutes, at the end of the timer period, the name list is cleared.

<source lang="lsl2">

// The script written by Taff Nouvelle.
// Use it in any way that you want
// but please leave this header intact.



string message = " Merry Christmas ";   // put your message here.
list users;
string user;
default
{

```lsl
   collision_start(integer num_detected)   // check for an avatar colliding with the prim.
   {
       user = llDetectedName(0);
       if (llListFindList(users,[user]) == -1)// look at the list, if the name is not there,
       {
           llSay(0, message + user);       // send the message to the detected avatar.
           users += user;                  // add the users name to a list so they only get the message once.
           llSetTimerEvent(600);           // change the number for the number of seconds before clearing the list.
       }
   }
   timer()
   {
       llSetTimerEvent(0);                 // turn the timer off
       users = [];                         // clear the list
   }
```

}