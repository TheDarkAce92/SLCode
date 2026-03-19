---
name: "Unpacker On Touch (NewAge)"
category: "example"
type: "example"
language: "LSL"
description: "Just Copy and Paste into the object that contains your product and configure the script to your needs!"
wiki_url: "https://wiki.secondlife.com/wiki/Unpacker_On_Touch_(NewAge)"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

**Unpacker On Touch**

Just Copy and Paste into the object that contains your product and configure the script to your needs!

New Motto: Save and Sell!

```lsl
// NewAge Unpacker On Touch Script
// By Asia Snowfall
string nameOfFolderToBeCreated;
string messageToSendUponRez;
integer addThisScriptToFolder;
integer typeOfInventoryItemsToBeSent;
integer killAfterCompletion;

init()
{
//  do not use an empty string
    nameOfFolderToBeCreated = llGetObjectName();

//  leave empty to not send a message upon rez
    messageToSendUponRez = "";

//  use INVENTORY_ALL to not apply a filter
    typeOfInventoryItemsToBeSent = INVENTORY_ALL;

    addThisScriptToFolder = FALSE;

    killAfterCompletion = TRUE;
}

try_to_send_items(key inputKey, integer inputType)
{
    integer numberOfItems = llGetInventoryNumber(inputType);

    string thisScript = llGetScriptName();
    string itemName;
    list listOfItemsToSend;

    integer i;
    do
    {
        itemName = llGetInventoryName(inputType, i);

        if(itemName != "")
        {
            if(addThisScriptToFolder && itemName == thisScript)
                listOfItemsToSend += [itemName];

            else if(itemName != thisScript)
                listOfItemsToSend += [itemName];
        }
    }
    while(++i < numberOfItems);

//  change to number of items in list now
    numberOfItems = llGetListLength(listOfItemsToSend);

    if(numberOfItems)
    {
        llGiveInventoryList(inputKey, nameOfCreatedFolder, listOfItemsToSend);
        llInstantMessage(inputKey,
                    "/me [" + thisScript + "]: Items have been sent into a folder named '"
                    + nameOfFolderToBeCreated + "' within your inventory.");
    }
    else
        llInstantMessage(inputKey,
            "/me [" + thisScript + "]: Could not find inventory items to send!");
}

default
{
    on_rez(integer start_param)
    {
        llResetScript();
    }

    touch_start(integer num_detected)
    {
        key owner = llGetOwner();
        key id = llDetectedKey(0);

    //  if not the owner touching, abort process
        if (id != owner)
            return;

        if (messageToSendUponRez != "")
            llInstantMessage(owner, messageToSendUponRez);

        try_to_send_items(owner, typeOfInventoryItemsToBeSent);

        if (killAfterCompletion)
            llDie();
    }
}
```