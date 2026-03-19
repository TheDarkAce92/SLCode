---
name: "llLinksetDataDelete"
category: "function"
type: "function"
language: "LSL"
description: 'Removes an unprotected name:value pair from the linkset's datastore. If the pair was created

When this function successfully removes a name:value pair a linkset_data event is triggered in all scripts running in the linkset with an action of LINKSETDATA_DELETE and the name parameter set to the name '
signature: "integer llLinksetDataDelete(string key)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llLinksetDataDelete'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Removes an unprotected name:value pair from the linkset's datastore. If the pair was created

When this function successfully removes a name:value pair a linkset_data event is triggered in all scripts running in the linkset with an action of LINKSETDATA_DELETE and the name parameter set to the name that was removed. The value parameter in the event is set to an empty string.


## Signature

```lsl
integer llLinksetDataDelete(string key);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `name` | The key of the linkset name:value pair to be deleted. |
| `string` | `pass` | A pass phrase previously used to protect the name:value pair. |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llLinksetDataDelete)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llLinksetDataDelete) — scraped 2026-03-18_

Removes an unprotected name:value pair from the linkset's datastore. If the pair was createdReturns an integer success or failure code.

## Caveats

- If the name does not exist or the pass does not match, no event is triggered.

## Examples

```lsl
// Simple blacklist management.

integer gDialogChannel;
integer gDialogHandle;
integer gManagingBlocks;

startDialog(key person)
{
    gManagingBlocks = 0;
    gDialogHandle = llListen(gDialogChannel, "", person, "");
    llDialog(person, "\nSelect action", ["List blocks", "Add block", "Remove block"], gDialogChannel);
    llSetTimerEvent(60);
}

stopDialog()
{
    llSetTimerEvent(0);
    llListenRemove(gDialogHandle);
}

default
{

    on_rez(integer sp)
    {
        llResetScript();
    }

    state_entry()
    {
        gDialogChannel = (integer)(llFrand(-10000000)-10000000);
        llListen(PUBLIC_CHANNEL, "", NULL_KEY, "");;
    }

    timer()
    {
        stopDialog();
    }

    touch_start(integer nd)
    {
        key toucherKey = llDetectedKey(0);
        if (toucherKey == llGetOwner())
        {
            startDialog(toucherKey);
        }
    }

    listen(integer channel, string name, key id, string message)
    {

        if (llGetAgentSize(id) == ZERO_VECTOR)
        {
            return;
        }

        if (channel == gDialogChannel)
        {
            stopDialog();
            if (gManagingBlocks)
            {
                message = llStringTrim(message, STRING_TRIM);
                if ((key)message)
                {
                    if (gManagingBlocks == 1)
                    {
                        llOwnerSay("Addition request has been sent to the blacklist storage");
                        llLinksetDataWrite("blocklist:" + message, "1");
                    }
                    else
                    {
                        llOwnerSay("Removal request has been sent to the blacklist storage.");
                        llLinksetDataDelete("blocklist:" + message);
                    }
                }
                else
                {
                    llOwnerSay("The UUID '" + message + "' appears to be invalid.");
                }
                startDialog(id);
            }
            else if (message == "List blocks")
            {
                list blocks = llLinksetDataFindKeys("^blocklist:", 0, 0);
                integer listLength = llGetListLength(blocks);
                llOwnerSay("Blacklist items: " + (string)listLength);
                integer i;
                while (i < listLength)
                {
                    string record = llGetSubString(llList2String(blocks, i), 10, -1);
                    llOwnerSay("- secondlife:///app/agent/" + record + "/about" + " - " + record);
                    ++i;
                }
                blocks = [];
                startDialog(id);
            }
            else if (message == "Add block" || message == "Remove block")
            {
                string label = "add to";
                gManagingBlocks = 1;
                if (message == "Remove block")
                {
                    gManagingBlocks = 2;
                    label = "remove from";
                }
                gDialogHandle = llListen(gDialogChannel, "", id, "");
                llTextBox(id, "\nPlease specify one single avatar UUID you'd like to " + label + " the blacklist storage.", gDialogChannel);
                llSetTimerEvent(60);
            }
            return;
        }

        if (llGetListLength(llLinksetDataFindKeys("blocklist:" + (string)id, 0, 1)) > 0)
        {
            llRegionSayTo(id, 0, "You're blacklisted.");
            return;
        }

        llRegionSayTo(id, 0, "Hello there, secondlife:///app/agent/" + (string)id + "/about - your message: " + message);

    }

    linkset_data(integer action, string name, string value)
    {
        if (action == LINKSETDATA_RESET || action == LINKSETDATA_DELETE || action == LINKSETDATA_UPDATE)
        {
            llOwnerSay("Blacklist storage modified.");
        }
    }

}
```

## See Also

### Events

- linkset_data

### Functions

- llLinksetDataAvailable
- llLinksetDataCountKeys
- llLinksetDataFindKeys
- llLinksetDataListKeys
- llLinksetDataDeleteFound
- llLinksetDataRead
- llLinksetDataReadProtected
- llLinksetDataReset
- llLinksetDataWrite
- llLinksetDataWriteProtected

<!-- /wiki-source -->
