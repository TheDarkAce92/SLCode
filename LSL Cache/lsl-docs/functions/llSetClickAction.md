---
name: "llSetClickAction"
category: "function"
type: "function"
language: "LSL"
description: 'Sets the action performed when a prim is clicked upon (aka click action).

When the cursor hovers over the prim, its image changes to reflect the action.'
signature: "void llSetClickAction(integer action)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetClickAction'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsetclickaction"]
---

Sets the action performed when a prim is clicked upon (aka click action).

When the cursor hovers over the prim, its image changes to reflect the action.


## Signature

```lsl
void llSetClickAction(integer action);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer (click_action)` | `action` | CLICK_ACTION_* flag |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetClickAction)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetClickAction) — scraped 2026-03-18_

Sets the action performed when a prim is clicked upon (aka click action).

## Caveats

- When set in the root of an object the chosen CLICK_ACTION_* will be that for the children also even if they have their own llSetClickAction set (it will be over-ridden). However (in the case of touch for example) if the CLICK_ACTION_* is set in the root but not at all in the children (including not having touch event scripts in them (this creates a default CLICK_ACTION_TOUCH)) the effect of the roots CLICK_ACTION_* is not *seen* but the CLICK_ACTION_* is *used* on clicking. To both use **and see** the correct cursor the CLICK_ACTION_* flags must match in the children and root.
- If llSetClickAction is CLICK_ACTION_PAY then you must have a money event, or it will revert to CLICK_ACTION_NONE.
- While this function works or attached objects (click action can be changed), the configured click action of an attachment is ignored by the viewer (with exceptions).  The viewer always* behaves as though an attached object has CLICK_ACTION_TOUCH set.

  - The only exception to the above rule is when the chosen click action is CLICK_ACTION_DISABLED, which will disable the cursor changing from the standard pointer arrow to the touch pointer.
- llSetClickAction has to be called **before** an avatar clicks on an object. Calling it while an avatar is clicking (click & holding) will cause this function to silently fail. You *can* set the click action after an avatar touches an object, but bear in mind that there may be some delay before the given avatar's viewer will update due to ping times, etc.

## Examples

| make sitting easier | make unpacking for next owner easier | make buying for customers easier |
| --- | --- | --- |
| ```lsl default { state_entry() { llSetClickAction(CLICK_ACTION_SIT); llRemoveInventory(llGetScriptName()); } } ``` | ```lsl default { state_entry() { llSetClickAction(CLICK_ACTION_OPEN); llRemoveInventory(llGetScriptName()); } } ``` | ```lsl // remember you'll have to set a price // in the general tab of the edit window // for your object before using this script default { state_entry() { llSetClickAction(CLICK_ACTION_BUY); llRemoveInventory(llGetScriptName()); } } ``` |

```lsl
//  simple tipjar

default
{
    state_entry()
    {
        llSetClickAction(CLICK_ACTION_PAY);

    //  enabled edit field to put own amount, all quick-pay-buttons hidden
        llSetPayPrice(PAY_DEFAULT, [PAY_HIDE, PAY_HIDE, PAY_HIDE, PAY_HIDE]);
    }

    money(key id, integer amount)
    {
        string name = llKey2Name(id);

        llInstantMessage(id, "Thank you for the tip, " + name + "!");
    }
}
```

```lsl
//Sit Only with Permission

list gAvWhitelist = ["953d10f1-44ce-462a-8bc1-f634333ee031", "599dce91-a2b8-48c5-b96d-54965433022b"];

default
{
    state_entry()
    {
        llSitTarget(<0.0, 0.0, 0.5>, ZERO_ROTATION);
    }

    changed(integer change)
    {
        if (change & CHANGED_LINK)
        {
            list Properties = llGetObjectDetails(llGetKey(), [OBJECT_CLICK_ACTION]);
            integer Click = llList2Integer(Properties, 0);
            key Av = llAvatarOnSitTarget();
            if ((Av != NULL_KEY) && (!Click))
            {
                llSay(0, "Please click first for permission to sit.");
                llUnSit(Av);
            }
        }
    }
    touch_start(integer total_number)
    {
        list Properties = llGetObjectDetails(llGetKey(), [OBJECT_CLICK_ACTION]);
        integer Click = llList2Integer(Properties, 0);
        if (!Click && (~llListFindList(gAvWhitelist, [(string)llDetectedKey(0)])))
        {
            llSetClickAction(CLICK_ACTION_SIT);
            llSetTimerEvent(10.0);
            llSay(0, "Please take a seat.");
        }
        else
        {
            llSetClickAction(CLICK_ACTION_TOUCH);
            if (llAvatarOnSitTarget() != NULL_KEY)
            {
                llSay(0, "Good bye!");
            }
            else
            {
                llSay(0, "Sorry.  You are not allowed to sit here.");
            }
            llUnSit(llDetectedKey(0));
        }
    }

    timer()
    {
        llSetTimerEvent(0.0);
        llSetClickAction(CLICK_ACTION_TOUCH);
    }
}
```

## See Also

### Events

- touch_start
- touch
- touch_end

### Functions

- llPassTouches

### Articles

- Detected

<!-- /wiki-source -->
