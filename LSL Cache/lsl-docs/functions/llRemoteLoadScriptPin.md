---
name: "llRemoteLoadScriptPin"
category: "function"
type: "function"
language: "LSL"
description: 'Copy script name into target and set to running with a start_param only if target's pin matches pin

Only works if the script owner can modify target.'
signature: "void llRemoteLoadScriptPin(key target, string name, integer pin, integer running, integer start_param)"
return_type: "void"
sleep_time: "3.0"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llRemoteLoadScriptPin'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llremoteloadscriptpin"]
---

Copy script name into target and set to running with a start_param only if target's pin matches pin

Only works if the script owner can modify target.


## Signature

```lsl
void llRemoteLoadScriptPin(key target, string name, integer pin, integer running, integer start_param);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `target` | prim UUID that is in the same region |
| `string` | `name` | a script in the inventory of the prim this script is in |
| `integer` | `pin` | Must match pin set by llSetRemoteScriptAccessPin |
| `integer (boolean)` | `running` | boolean, if TRUE[1] the script is set as running, if FALSE the script is not set as running |
| `integer` | `start_param` | value returned by llGetStartParameter in the target script. |


## Caveats

- Forced delay: **3.0 seconds** — the script sleeps after each call.
- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llRemoteLoadScriptPin)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llRemoteLoadScriptPin) — scraped 2026-03-18_

Copy script name into target and set to running with a start_param only if target's pin matches pin

## Caveats

- This function causes the script to sleep for 3.0 seconds.
- If **target** is not owned by the same person,  and **name** does not have transfer permissions, an error is shouted on DEBUG_CHANNEL.
- If **name** permissions do not allow copy, the transfer fails and an error is shouted on DEBUG_CHANNEL.
- If **target**  is not in the same region an error is shouted on DEBUG_CHANNEL.
- When scripts are copied or moved between inventories, their state does not survive the transfer. Memory, event queue and execution position are all discarded.
- If name is missing from the prim's inventory   or it is not a script then an error is shouted on DEBUG_CHANNEL.
- If name is present in the target prim's inventory then it is silently replaced.
- start_param only lasts until the script is reset.
- Only the owner of an attachment can modify it while it is being worn.

  - If target is an attachment owned by a different user, regardless of object modify rights granted, this function will silently fail.
- If target is owned by a different user and modify permission has been granted to the script owner via [Edit, delete, or take my objects](http://community.secondlife.com/t5/tkb/articleprintpage/tkb-id/English_KB@tkb/article-id/215), the script owner must be connected to the sim for this function to succeed.
- If pin fails to match, the error "Task ~Prim~ trying to illegally load script onto task ~Other_Prim~!" is shouted on DEBUG_CHANNEL. "~Prim~" and "~Other_Prim~" are substituted with the applicable prim names.
- If target is the script's parent (`target == llGetKey()`) then "Unable to add item!" is shouted on DEBUG_CHANNEL.
- If the object containing this script is deeded to a group, then script name needs transfer permissions; even if target is deeded to the same group.
- When the script is set to run (with running, the running checkbox or llSetScriptState) state_entry will be queued.

## Examples

#### Basic Example

Script copier

```lsl
//Copy a script to the second prim
integer PIN=1341134;

default {
    state_entry() {
        llRemoteLoadScriptPin( llGetLinkKey(2), "some script", PIN, TRUE, 0xBEEEEEEF );
    }
}
```

Pin setter

Simple script used for setting the pin for a prim, so you can later send scripts to it with llRemoteLoadScriptPin.

```lsl
//Child Prim PIN setter
integer PIN=1341134;

default {
    state_entry() {
        llOwnerSay(llGetObjectName()+" : "+(string)llGetKey()+" is ready to accept a describer script using the agreed upon PIN.");
        llSetRemoteScriptAccessPin(PIN);
    }
}
```

#### Rez and copy a file from a control object

Notes: There is currently no signing on the starting messages only the owner is checked.

this example rezs a prim from inventory that has a basic control file inside of it and does a basic handshake to setup the
pin and transfer the script.

after the transfert the helper script in the rezzed prim deletes itself.

Control prim

```lsl
integer controlchan = 0;
integer controlid = -1;
start()
{
    llSetTimerEvent(0);
    talkingto = NULL_KEY;
    integer a = (integer)llFrand(43);
    controlchan = a * a;
    controlchan -= controlchan * 3;
    controlid = llListen(controlchan,"","","set-connect");
    llRezObject("card",llGetPos()+<0,0,0.1>,<0,0,0>,ZERO_ROTATION,a);
    llSetTimerEvent(60);
}
key talkingto = NULL_KEY;
integer busy = FALSE;
integer accesspin = 0;
default
{
    timer()
    {
        llSetTimerEvent(0);
        llOwnerSay("Lost connection!");
        llListenRemove(controlid);
        busy = FALSE;
    }
    listen(integer chan,string name,key id,string message)
    {
        if(chan == controlchan)
        {
            if(llGetOwnerKey(id) == llGetOwner())
            {
                if(talkingto == NULL_KEY)
                {
                    if(message == "set-connect")
                    {
                        llSetTimerEvent(0);
                        talkingto = id;
                        llListenRemove(controlid);
                        controlid = llListen(controlchan,"",talkingto,"ready");
                        llRegionSayTo(id,controlchan,"auto-connect");
                        llSetTimerEvent(60);
                    }
                }
                else if(id == talkingto)
                {
                    if(message == "ready")
                    {
                        llSetTimerEvent(0);
                        accesspin = (integer)llFrand(2345)+213;
                        llListenRemove(controlid);
                        controlid = llListen(controlchan,"",talkingto,"pinset");
                        llSleep(1);
                        llRegionSayTo(talkingto,controlchan,(string)accesspin);
                        llSetTimerEvent(60);
                    }
                    else if(message == "pinset")
                    {
                        llSetTimerEvent(0);
                        llListenRemove(controlid);
                        llRemoteLoadScriptPin(talkingto,"demo.lsl",accesspin,1,0);
                        llSleep(3);
                        llRegionSayTo(talkingto,controlchan,"finished");
                        llOwnerSay("Transfer of file finished - control file should have auto deleted itself!");
                        busy = FALSE;
                    }
                }
            }
        }
    }
    touch_end(integer a)
    {
        if(busy == FALSE)
        {
            busy = TRUE;
            if(llGetOwner() == llDetectedKey(0))
            {
                start();
            }
        }
    }
}
```

rezzed prim

```lsl
integer listen_id = -1;
integer listen_chan = -1;
key details_from = NULL_KEY;
default
{
    on_rez(integer a)
    {
        if(a == 0)
        {
            llOwnerSay("- Direct rez -");
        }
        else
        {
            llOwnerSay("- Awaiting config connection -");
            listen_chan = a * a;
            listen_chan -= listen_chan * 3;
            listen_id = llListen(listen_chan,"","","auto-connect");
            llWhisper(listen_chan,"set-connect");
            llSetTimerEvent(30);
        }
    }
    timer()
    {
        llOwnerSay("Failed to connect to rezzer deleting myself!");
        llSetTimerEvent(0);
        llDie();
    }
    listen(integer chan,string name,key id,string message)
    {
        if(llGetOwnerKey(id) == llGetOwner())
        {
            if(message == "auto-connect")
            {
                llSetTimerEvent(0);
                llListenRemove(listen_id);
                listen_id = llListen(listen_chan,"",id,"");
                llRegionSayTo(id,listen_chan,"ready");
                details_from = id;
                llSetTimerEvent(30);
            }
            else if(details_from != NULL_KEY)
            {
                llSetTimerEvent(0);
                if(message == "finished")
                {
                    llSetRemoteScriptAccessPin((integer)message);
                    llRemoveInventory(llGetScriptName());
                }
                else
                {
                    llSetRemoteScriptAccessPin((integer)message);
                    llRegionSayTo(id,listen_chan,"pinset");
                }
                llSetTimerEvent(30);
            }
        }
    }
}
```

## See Also

### Functions

- **llSetRemoteScriptAccessPin** — Used to setup a prim for remote loading
- **llSetScriptState** — Set a scripts running state
- **llResetOtherScript** — Reset another script in the prim

<!-- /wiki-source -->
