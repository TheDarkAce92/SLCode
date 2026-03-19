---
name: "Rental Cube"
category: "example"
type: "example"
language: "LSL"
description: "Just a simple cube for renting a stall or store. Supports refunding rent to an avatar if they wish to end the lease early."
wiki_url: "https://wiki.secondlife.com/wiki/Rental_Cube"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Just a simple cube for renting a stall or store. Supports refunding rent to an avatar if they wish to end the lease early.

```lsl
//Rental Script v1.5.3
//Copyright 2003-2009 by Hank Ramos

//Options
vector  rentalOffset   = <0,0,10>;
float   updateInterval = 60.0; //seconds
string  infoNotecard   = "Rent This Space Info";

//Variables
string  tierName;
float   rentalCost;
integer primCount;
integer rentalVolume;
float   refundFee;
key     renterID;
string  renterName;
float   rentalTime;
integer listenQueryID;
vector  initPos;
vector  initScale;
integer count;
integer lineCount;
key     readKey;
string  rentalGrade;
integer primAllotment;

//Constants
float ONE_WEEK = 604800.0;
float ONE_DAY  = 86400.0;
float ONE_HOUR = 3600.0;

dispString(string value)
{
    llSetText(value, <1,1,1>, 1);
}
sendReminder(string message)
{
    llInstantMessage(renterID, "Your lease located in " + llGetRegionName() + " (" + (string)initPos.x + "," + (string)initPos.y + "," + (string)initPos.z + ") will expire " + message);
}
saveData()
{
    list saveData;
    vector storageVector;

    saveData += renterID;
    saveData += renterName;
    saveData += llRound(rentalTime);
    storageVector = initPos * 1000;
    saveData += "<" + (string)llRound(storageVector.x) + "," + (string)llRound(storageVector.y) + "," + (string)llRound(storageVector.z) + ">";
    storageVector = initScale * 1000;
    saveData += "<" + (string)llRound(storageVector.x) + "," + (string)llRound(storageVector.y) + "," + (string)llRound(storageVector.z) + ">";

    llSetObjectDesc(llDumpList2String(saveData, "|"));
}
string getTimeString(integer time)
{
    integer days;
    integer hours;
    integer minutes;
    integer seconds;

    days = llRound(time / 86400);
    time = time % 86400;

    hours = (time / 3600);
    time  = time % 3600;

    minutes = time / 60;
    time    = time % 60;

    seconds = time;

    return (string)days + " days, " + (string)hours + " hours, " + (string)minutes + " minutes"; // + ":" + (string)seconds;
}

integer setupDialogListen()
{
    integer chatChannel = (integer)llFrand(2000000);
    llListenRemove(listenQueryID);
    listenQueryID = llListen(chatChannel, "", NULL_KEY, "");
    return chatChannel;
}

updateTimeDisp()
{
    dispString("Leased by: " + renterName + "\nTime Remaining: " + getTimeString(llRound(rentalTime)));
}

dispData()
{
    llSay(0, "========================");
    llSay(0, "Rental Space Information");
    llSay(0, "========================");
    llSay(0, "This space is currently leased by " + renterName);
    llSay(0, "The current rental price is L$" + (string)((integer)rentalCost) + " per week.");
    llSay(0, "This space will be open for lease in " + getTimeString(llRound(rentalTime)) + ".");
    llSay(0, "Memory Free: " + (string)llGetFreeMemory());
}
default
{
    state_entry()
    {
        state initialize;
    }
}

state initialize
{
    state_entry()
    {
        llSetTimerEvent(300);
        llOwnerSay("Waiting to obtain Debit Permissions.");
        llRequestPermissions(llGetOwner(), PERMISSION_DEBIT);
    }
    run_time_permissions(integer permissions)
    {
        //Only wait for payment if the owner agreed to pay out money
        if (permissions & PERMISSION_DEBIT)
        {
            state loadSettings;
        }
    }
    on_rez(integer start_param)
    {
        llResetScript();
    }
    timer()
    {
        llRequestPermissions(llGetOwner(), PERMISSION_DEBIT);
    }
    touch_start(integer total_number)
    {
        integer x;
        for (x = 0; x < total_number; x += 1)
        {
            if (llDetectedKey(x) == llGetOwner())
            {
                llResetScript();
            }
        }
        llSay(0, "Waiting to obtain Debit Permissions from Owner.");
    }
    state_exit()
    {
        llSetTimerEvent(0);
        llSay(0, "Initialized.");
    }
}

state loadSettings
{
    state_entry()
    {
        integer found = FALSE;
        integer x;

        count = 0;
        lineCount = 0;

        list savedList = llCSV2List(llGetObjectDesc());

        if (llGetListLength(savedList) == 4)
        {
            rentalGrade = llList2String(savedList, 0);
        }
        else
        {
            rentalGrade = llGetObjectDesc();
        }
        for (x = 0; x < llGetInventoryNumber(INVENTORY_NOTECARD); x += 1)
        {
            if (llGetInventoryName(INVENTORY_NOTECARD, x) == "Settings")
            {
                found = TRUE;
            }
        }
        if (found)
        {
            llOwnerSay("Reading Settings Notecard...");
            readKey = llGetNotecardLine("Settings", lineCount);
        }
        else
        {
            llOwnerSay("Settings Notecard Not Found.");
            llResetScript();
        }
    }
    dataserver(key requested, string data)
    {
        integer integerData;
        float   floatData;

        if (requested == readKey)
        {
            if (data != EOF)
            {
                if ((llSubStringIndex(data, "#") != 0) && (data != "") && (data != " "))
                {
                    integerData = (integer)data;
                    floatData   = (float)data;

                    if (count == 0)
                    {
                        tierName = data;
                    }
                    else if (count == 1)
                    {
                        if (integerData >= 0)
                        {
                            rentalCost = integerData;
                        }
                        else
                        {
                            rentalCost = 0;
                        }
                    }
                    else if (count == 2)
                    {
                        if (integerData >= 1)
                        {
                            primCount = integerData;
                        }
                        else
                        {
                            primCount = 1;
                        }
                    }
                    else if (count == 3)
                    {
                        if (integerData >= 16)
                        {
                            rentalVolume = integerData;
                        }
                        else
                        {
                            rentalVolume = 16;
                        }
                    }
                    else if (count == 4)
                    {
                        if (integerData >= 0)
                        {
                            refundFee = integerData;
                        }
                        else
                        {
                            refundFee = 0;
                        }
                    }
                    else if (count == 5)
                    {
                        rentalOffset = (vector)data;
                    }
                    else if (count == 6)
                    {
                        infoNotecard = data;
                    }
                    count += 1;
                }
                lineCount += 1;
                readKey = llGetNotecardLine("Settings", lineCount);
            }
            else
            {
                llOwnerSay("===============");
                llOwnerSay("Settings Loaded");
                llOwnerSay("===============");
                llOwnerSay("Space Name: " + tierName);
                llOwnerSay("Rental Cost: L$" + (string)llRound(rentalCost));
                llOwnerSay("Prim Count: " + (string)primCount);
                llOwnerSay("Space Volume: " + (string)rentalVolume + " sqm");
                llOwnerSay("Refund Fee: L$" + (string)refundFee);
                llOwnerSay("===============");
                llOwnerSay("Ready for Service!");

                list savedList = llParseString2List(llGetObjectDesc(), ["|"], []);

                if (llGetListLength(savedList) == 5)
                {
                    renterID    = llList2Key(savedList, 01);
                    renterName  = llList2String(savedList, 1);
                    rentalTime  = llList2Integer(savedList, 2);
                    initPos     = (vector)llList2String(savedList, 3) / 1000;
                    initScale   = (vector)llList2String(savedList, 4) / 1000;
                    state rented;
                }
                else
                {
                    renterID   = NULL_KEY;
                    renterName = "Nobody";
                    rentalTime = 0;
                    initPos    = llGetPos();
                    initScale  = llGetScale();
                    state idle;
                }
            }
        }
    }
}
state idle
{
    state_entry()
    {
        llSetObjectDesc("");
        llSetTexture("rentthisspace", ALL_SIDES);
        llSetScale(initScale);
        llSetPos(initPos);
        llSetTimerEvent(updateInterval);

        dispString(tierName + "\nLease this space for L$" + (string)llRound(rentalCost) + " per week.\n" + (string)rentalVolume + " sq meters\n" + (string)primCount + " prims\nPay this Sign to begin your lease.");
    }
    moving_end()
    {
        initPos = llGetPos();
    }
    changed(integer change)
    {
        if (change & CHANGED_SCALE)
        {
            initScale = llGetScale();
        }
    }
    touch_start(integer num_detected)
    {
        integer x;
        integer chatChannel;

        for (x = 0; x < num_detected; x += 1)
        {
            if (llDetectedKey(x) == llGetOwner())
            {
                llDialog(llGetOwner(), "Owner Options.  Select one of the options below...", ["Info", "Reset"], setupDialogListen());
                return;
            }
        }

        llSay(0, "Lease this space for L$" + (string)llRound(rentalCost) + " per week. " + (string)rentalVolume + " sq meters. " + (string)primCount + " prims. Pay this Sign to begin your lease.");

        for (x = 0; x < num_detected; x += 1)
        {
            llGiveInventory(llDetectedKey(x), infoNotecard);
        }
    }
    listen(integer channel, string name, key id, string message)
    {
        if (message == "Reset")
        {
            llResetScript();
        }
        else if (message == "Info")
        {
            llListenRemove(listenQueryID);
            dispData();
            llSay(0, "Lease this space for L$" + (string)llRound(rentalCost) + " per week. " + (string)rentalVolume + " sq meters. " + (string)primCount + " prims. Pay this Sign to begin your lease.");
            llGiveInventory(id, infoNotecard);
        }
    }
    money(key id, integer amount)
    {
        if (amount >= rentalCost)
        {
            renterID   = id;
            renterName = llKey2Name(renterID);
            rentalTime = ONE_WEEK * amount / rentalCost;
            saveData();

            llSay(0, "Thank you " + renterName + " for leasing!  Your lease will expire in " + getTimeString((integer)rentalTime) + ".");

            state rented;
        }
        else
        {
            llSay(0, "This space costs L$" + (string)rentalCost + " to rent. Refunding paid balance.");
            llGiveMoney(id, amount);
        }
    }
}

state rented
{
    state_entry()
    {
        llSetTexture("infosign", ALL_SIDES);
        llSetScale(<0.5, 0.5, 0.5>);
        llSetPos(initPos + rentalOffset);

        updateTimeDisp();
        llResetTime();
        llSetTimerEvent(updateInterval);
    }
    touch_start(integer num_detected)
    {
        integer x;
        key     detectedKey;

        for (x = 0; x < num_detected; x += 1)
        {
            detectedKey = llDetectedKey(x);
            if (detectedKey == llGetOwner())
            {
                llDialog(detectedKey, "Lease Options. Select one of the options below...", ["Refund Time", "Info", "Release", "Reset"], setupDialogListen());
            }
            else if (detectedKey == renterID)
            {
                llDialog(detectedKey, "Lease Options. Select one of the options below...", ["Refund Time", "Info"], setupDialogListen());
            }
            else
            {
                dispData();
                llGiveInventory(detectedKey, infoNotecard);
            }
        }
    }
    money(key id, integer amount)
    {
        if ((id == renterID)||(id == llGetOwner()))
        {
            float addTime;

            addTime = ONE_WEEK*amount/rentalCost;
            rentalTime += addTime;

            llInstantMessage(id, "Adding " + getTimeString(llRound(addTime)) + " to your lease. Lease Time is Now: " + getTimeString(llRound(rentalTime)) + ".");
            saveData();
            updateTimeDisp();
        }
        else
        {
            llInstantMessage(id, "Refunding Money...");
            llGiveMoney(id, amount);
            llInstantMessage(id, "This space is currently leased by " + renterName + ". This space will be open for lease in " + getTimeString(llRound(rentalTime)) + ".");
        }
    }
    listen(integer channel, string name, key id, string message)
    {
        integer refundAmount;

        llListenRemove(listenQueryID);

        if (message == "Info")
        {
            dispData();
            llGiveInventory(id, infoNotecard);
        }
        else if (message == "Refund Time")
        {
            llDialog(id, "Are you sure you want to TERMINATE your lease and refund your money, minus a L$" + (string)refundFee + " fee?", ["YES", "NO"], setupDialogListen());
        }
        else if (message == "YES")
        {
            refundAmount = llRound((rentalTime/ONE_WEEK)*rentalCost - refundFee);
            llInstantMessage(renterID, "Refunding L$" + (string)refundAmount + ", which includes a L$" + (string)refundFee + " termination fee.");
            llGiveMoney(renterID, refundAmount);
            llInstantMessage(llGetOwner(), "LEASE REFUNDED: leased by " + renterName + " located in " + llGetRegionName() + " (" + (string)initPos.x + "," + (string)initPos.y + "," + (string)initPos.z + ") has ended. Refunded L$" + (string)refundAmount + ".");
            state idle;
        }
        else if (message == "Release")
        {
            llDialog(id, "Are you sure you want to TERMINATE this lease with NO REFUND?", ["Yes", "No"], setupDialogListen());
        }
        else if (message == "Yes")
        {
            llInstantMessage(llGetOwner(), "LEASE TERMINATED: leased by " + renterName + " located in " + llGetRegionName() + " (" + (string)initPos.x + "," + (string)initPos.y + "," + (string)initPos.z + ") has ended. Refunded L$0.");
            state idle;
        }
        else if (message == "Reset")
        {
            llResetScript();
        }
    }
    timer()
    {
        float timeElapsed = llGetAndResetTime();
        if (timeElapsed > (updateInterval * 4))
        {
            timeElapsed = updateInterval;
        }
        rentalTime -= timeElapsed;

        saveData();

        updateTimeDisp();

        //Process Reminders
        if (rentalTime <= 0)
        {
            llInstantMessage(llGetOwner(), "LEASE EXPIRED: leased by " + renterName + " located in " + llGetRegionName() + " (" + (string)initPos.x + "," + (string)initPos.y + "," + (string)initPos.z + ") has expired.");

            state idle;
        }
        if ((rentalTime <= ONE_DAY)&&(rentalTime >= ONE_DAY - (updateInterval*2)))
        {
            sendReminder("in one day.");
        }
        else if ((rentalTime <= ONE_HOUR*12)&&(rentalTime >= ONE_HOUR*12 - (updateInterval*2)))
        {
            sendReminder("in 12 hours.");
        }
        else if ((rentalTime <= ONE_HOUR)&&(rentalTime >= ONE_HOUR - (updateInterval*2)))
        {
            sendReminder("in one hour.");
        }
    }
}
```



Here is the associated settings notecard (not a script):

```lsl
#Rent This Space
#Options Notecard
#All lines beginning with "#" are comments, and are ignored
#DO NOT CHANGE the order of the options!!!

#Spot Name
This Place for Rent!

#Rental Cost
#The weekly rate to rent this space
50

#Prim Count
#The number of prims allowed by the renter in this space
20

#Rental Size
#The volume of the rental space, in square meters
100

#Refund Fee
#The fee charged to obtain a refund on the currently paid rent
20

#Rental Offset
#The relative position of the prim when rented, when compared
#to the non-rented position
#e.g. 6.75m above the rented spot: <0,0,6.75>
#e.g. 15m above and 5m to the West: <5,0,15>
<0,0,6.75>

#Info Notecard Name
#The name of the notecard to give to someone
#who clicks the cube. Note: case-sensitive
Rental Info
```