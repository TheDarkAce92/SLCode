---
name: "First Name Letter Prize"
category: "example"
type: "example"
language: "LSL"
description: "I got bored one day and saw these lucky chairs and made something of my own and decided to open source it"
wiki_url: "https://wiki.secondlife.com/wiki/First_Name_Letter_Prize"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

## First Name Letter Prize

I got bored one day and saw these *lucky chairs* and made something of my own and decided to open source it

-- UPDATE ADDED 19 DECEMBER 2009 DUE TO PEOPLE WITH LOWERCASE NAMES

```lsl
   // CONVERT IT ALL INTO LOWERCASE
   firstletter  = llToLower(firstletter);
   winnerletter = llToLower(winnerletter);
```

## Okay, let's see the script!

Here's the script.

```lsl
//    First Name Prize Script for use in Second Life
//    Copyright (C) 2009  RaithSphere Whybrow (Second Life Avatar Name)/Gavin Owen (Real Name)

//    This program is free software: you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation, either version 3 of the License, or
//    (at your option) any later version.

//    This program is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License for more details.

//    You should have received a copy of the GNU General Public License
//    along with this program.  If not, see .

// CONFIG \\

// How Often do we change Letter?
// THIS IS IN MINUITES
// SO SIMPLE MATHS
integer changeletter = 10;
integer timerevent;
string winnerletter;

// ENABLE DEBUG MODE 0 = NO & 1 = YES
integer debug = 0;

// LETS GET TEH ALPHABET!
list letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"];

// DEBUG SHIT DON'T MESS WITH THIS
deBug(string dmsg)
{
    if(debug)
    llOwnerSay(dmsg);
}


// THIS IS THE CHECK NAME SUB
checkname(key whositting)
{
    // SAYS THE AVATARS KEY IN DEBUG MESSAGE
    deBug((string)whositting);
    // WE NEED TO KNOW WHO IS SITTING HERE A KEY IS USELESS!
    string whothat = llKey2Name(whositting);
    // SPLIT THER NAME UP
    list name  = llParseString2List(whothat, [" "], []);
    // 0 is the First name change to 1 if you want to use LASTNAME
    string who = llList2String(name, 0);
    // Get the Length of the name
    integer length = llStringLength(who);
    // DELETE EVERYTHING AFTER LAST LETTER
    string firstletter= llDeleteSubString(who, 1, length);

    // CONVERT IT ALL INTO LOWERCASE
    firstletter  = llToLower(firstletter);
    winnerletter = llToLower(winnerletter);

            // OK SO LETS SEE THEN IF THIS MATCHES
             if(firstletter == winnerletter)
             {
                 llSay(0, "We Have a Winner!!!");
                 llUnSit(whositting);

                // to give a different inventory item type,
                // replace "INVENTORY_OBJECT" with "INVENTORY_NOTECARD", etc.
                 llGiveInventory(whositting,llGetInventoryName(INVENTORY_OBJECT, 0));

                 getnewletter();
             }
             // NOPE THEY LOSE!!
             else
             {
                 llSay(0, "Your first name doesn't begin with the letter "+winnerletter+ " it's "+firstletter);
                 llUnSit(whositting);
            }
}

// SUB TO GET A NEW LETTER
getnewletter()
{
    // LETS SHUFFLE THE LIST AND GET A LETTER!
    list shuffled = llListRandomize(letters, 1);
    // NOW LETS SAY
    winnerletter = llList2String(shuffled, 0);
    llShout(0, "We are now looking for a lucky winner who's firstname starts with "+winnerletter);
    llSetText("Current letter is "+winnerletter, <1,1,1>, 1);
}

default
{
    state_entry()
    {
     // START BE GETTING A LETTER
     getnewletter();

     // THIS CONVERTS THE MINUITES INTO SECONDS WHICH IS WHAT LSL LIKES FOR TIMERS
     timerevent = (changeletter * 60);

     // START THE TIMER EVENT
     llSetTimerEvent(timerevent);

     // MAKE A SIT TARGET
     llSitTarget(<0.0, 0.0, 0.1>, ZERO_ROTATION);

    }

    timer()
    {
        // TIMER HAS RUN GET A NEW LETTER!!
        getnewletter();
    }

    changed(integer change)
    {
        if (change & CHANGED_INVENTORY)
        {
            // YOU CHANGED THE SCRIPT OR SOMETHING IN HERE
            // RESET THE SCRIPT
            llResetScript();
        }
        if (change & CHANGED_LINK)
        {
          key av = llAvatarOnSitTarget();
          if (av) { checkname(llAvatarOnSitTarget());}
        }
    }
}
```

## First Name Letter Prize (Linden Version)

After being contacted by Zoom Blitz i changed this now so there is also a linden giving version

As with most scripts involving money i advise you get a few people you trust or a few alts to test this out

```lsl
//    Lucky Chair Script for use in Second Life (LINDEN VERSION)
//    Copyright (C) 2009  RaithSphere Whybrow (Second Life Avatar Name)/Gavin Owen (Real Name)

//    This program is free software: you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation, either version 3 of the License, or
//    (at your option) any later version.

//    This program is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License for more details.

//    You should have received a copy of the GNU General Public License
//    along with this program.  If not, see .

// CONFIG \\

// How Often do we change Letter?
// THIS IS IN MINUITES
// SO SIMPLE MATHS
integer changeletter = 10;
integer timerevent;
string winnerletter;

// LINDEN
integer lindens = 100;

// ENABLE DEBUG MODE 0 = NO & 1 = YES
integer debug = 0;

// LETS GET TEH ALPHABET!
list letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"];

// DEBUG SHIT DON'T MESS WITH THIS
deBug(string dmsg)
{
    if(debug)
    llOwnerSay(dmsg);
}

// THIS IS THE CHECK NAME SUB
checkname(key whositting)
{
    // SAYS THE AVATARS KEY IN DEBUG MESSAGE
    deBug((string)whositting);
    // WE NEED TO KNOW WHO IS SITTING HERE A KEY IS USELESS!
    string whothat = llKey2Name(whositting);
    // SPLIT THER NAME UP
    list name  = llParseString2List(whothat, [" "], []);
    // 0 is the First name change to 1 if you want to use LASTNAME
    string who = llList2String(name, 0);
    // Get the Length of the name
    integer length = llStringLength(who);
    // DELETE EVERYTHING AFTER LAST LETTER
    string firstletter= llDeleteSubString(who, 1, length);

    // CONVERT IT ALL INTO LOWERCASE
    firstletter  = llToLower(firstletter);
    winnerletter = llToLower(winnerletter);

            // OK SO LETS SEE THEN IF THIS MATCHES
             if(firstletter == winnerletter)
             {
                 llSay(0, "Congratulations "+who+" you just won L$"+(string)lindens);



                 llUnSit(whositting);

                // OK THIS WILL GIVE CASH TO THE WINNER
                llGiveMoney(whositting, lindens);
                 getnewletter();
             }
             // NOPE THEY LOSE!!
             else
             {
                 llSay(0, "Your first name doesn't begin with the letter "+winnerletter+ " it's "+firstletter);
                 llUnSit(whositting);
            }
}

// SUB TO GET A NEW LETTER
getnewletter()
{
    // LETS SHUFFLE THE LIST AND GET A LETTER!
    list shuffled = llListRandomize(letters, 1);
    // NOW LETS SAY
    winnerletter = llList2String(shuffled, 0);
    llShout(0, "We are now looking for a lucky winner who's firstname starts with "+winnerletter+" who will get L$"+(string)lindens);
}

default
{
    state_entry()
    {
     // OK LETS GET THE DEBIT PERMISSIONS
     llRequestPermissions(llGetOwner(), PERMISSION_DEBIT );
    }

    timer()
    {
        // TIMER HAS RUN GET A NEW LETTER!!
        getnewletter();
    }

    changed(integer change)
    {
        if (change & CHANGED_INVENTORY)
        {
            // YOU CHANGED THE SCRIPT OR SOMETHING IN HERE
            // RESET THE SCRIPT
            llResetScript();
        }
        if (change & CHANGED_LINK)
        {
          key av = llAvatarOnSitTarget();
          if (av) { checkname(llAvatarOnSitTarget());}
        }
    }
    // OK CHECKING RUNTIME PERMISSIONS
    run_time_permissions (integer perm)
    {
        // OK WE GRANTED IT DEBIT RIGHTS
        if(perm & PERMISSION_DEBIT)
        {
           // START BE GETTING A LETTER
           getnewletter();

           // THIS CONVERTS THE MINUITES INTO SECONDS WHICH IS WHAT LSL LIKES FOR TIMERS
           timerevent = (changeletter * 60);

     // START THE TIMER EVENT
     llSetTimerEvent(timerevent);

     // MAKE A SIT TARGET
     llSitTarget(<0.0, 0.0, 0.1>, ZERO_ROTATION);
        }
    }
}
```