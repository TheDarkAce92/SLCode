---
name: "Unpacker On Rez (NewAge)"
category: "example"
type: "example"
language: "LSL"
description: "NewAge Auto Unpacker v1.1"
wiki_url: "https://wiki.secondlife.com/wiki/Unpacker_On_Rez_(NewAge)"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

**NewAge Auto Unpacker v1.1**

Just copy and paste this script into your object that will contain your product and configure the few lines in // Configure; section

```lsl
//  NewAge Auto Unpacker Script
//  By Asia Snowfall

string  nameOfFolderToBeCreated;
string  messageToSendUponRez;
integer addThisScriptToFolder;
integer typeOfInventoryItemsToBeSent;
integer killAfterCompletion;

init()
{
    nameOfFolderToBeCreated      = llGetObjectName();//  do not use an empty string
    messageToSendUponRez         = "";//  leave empty to not send a message upon rez
    typeOfInventoryItemsToBeSent = INVENTORY_ALL;//  use INVENTORY_ALL to not apply a filter
    addThisScriptToFolder        = FALSE;
    killAfterCompletion          = TRUE;
}

try_to_send_items(key inputKey, integer inputType)
{
    integer numberOfItems = llGetInventoryNumber(inputType);
    string  thisScript    = llGetScriptName();
    string  itemName;
    list    listOfItemsToSend;

    integer index;
    do
    {
        itemName = llGetInventoryName(inputType, index);

        if(itemName != "")
        {
            if(addThisScriptToFolder && itemName == thisScript)
                listOfItemsToSend += [itemName];

            else if(itemName != thisScript)
                listOfItemsToSend += [itemName];
        }
    }
    while(++index < numberOfItems);

//  change to number of items in list now
    numberOfItems = llGetListLength(listOfItemsToSend);

    if(numberOfItems)
    {
        llGiveInventoryList(inputKey, nameOfFolderToBeCreated, listOfItemsToSend);
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
        init();

        key owner = llGetOwner();

        if (messageToSendUponRez != "")
            llInstantMessage(owner, messageToSendUponRez);

        try_to_send_items(owner, typeOfInventoryItemsToBeSent);

        if (killAfterCompletion)
            llDie();
    }
}
```