---
name: "llLoopSoundMaster"
category: "function"
type: "function"
language: "LSL"
description: "Plays attached sound looping at volume, declares it a sync master."
signature: "void llLoopSoundMaster(string sound, float volume)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llLoopSoundMaster'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llloopsoundmaster"]
---

Plays attached sound looping at volume, declares it a sync master.


## Signature

```lsl
void llLoopSoundMaster(string sound, float volume);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `sound` | a sound in the inventory of the prim this script is in or a UUID of a sound |
| `float` | `volume` | between 0.0 (silent) and 1.0 (loud) (0.0 <= volume <= 1.0) |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llLoopSoundMaster)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llLoopSoundMaster) — scraped 2026-03-18_

Plays attached sound looping at volume, declares it a sync master.

## Caveats

- If sound is missing from the prim's inventory  and it is not a UUID or it is not a sound then an error is shouted on DEBUG_CHANNEL.
- If sound is a UUID then there are no new asset permissions consequences for the object.

  - The resulting object develops no new usage restrictions that might have occurred if the asset had been placed in the prims inventory.
- This function is affected by the Sound Queueing property of the parent prim - this means it's possible to queue a slave sound prior to starting a master, without having to use more than one prim as an emitter. (See below).

## Examples

```lsl
// for an uploaded .wav file called "MasterLoop" in inventory
llLoopSoundMaster("MasterLoop", 1.0);
```

The script below is an example of how using llSetSoundQueueing affects the interaction between master and slave sounds. In the example, it is used to run a car engine.

```lsl
integer playState; //see LUT below.

list lut = ["Engine start, idle.","Accelerate, speed loop.","Decelerate, idle.", "Idle, stop"];

default
{
    state_entry()
    {
        llSetSoundQueueing(TRUE); //Set this so the we don't skip the 1st 'slave' sound.
    }

    touch_start(integer total_number)
    {
        llWhisper(0, "Sound: " + llList2String(lut,playState));
        if(!playState) //start engine.
        {
            llPlaySoundSlave("engine start",1); //This sound is skipped if Sound Queueing is not set.
            llLoopSoundMaster("idle",1);
        }
        else if(playState == 1) //accelerate, then play driving loop
        {
            llPlaySoundSlave("accelerate",1);
            llLoopSoundMaster("speed",1);
        }
        else if(playState == 2) //decelerate to idle.
        {
            llPlaySoundSlave("decelerate",1);
            llLoopSoundMaster("idle",1);
        }
        else //stop the engine.
        {
            llPlaySoundSlave("engine stop",1);
            llSleep(2); //Wait until the above sound completes.
            llStopSound(); //Call this to prevent the master loop from restarting randomly (e.g. upon script reset or region change).
            playState = -1; //This actually resets to 0, as it's incremented below.
        }
        ++playState; //increment playState.
    }
}
```

The script below can be added to an object, to toggle a SoundMaster on and off. Note that the script requires a sound in inventory called MasterLoop, or you need to change the argument in the function for it to work.

```lsl
//This integer (actually a boolean) will be used to manage the toggle effect.
integer soundState = FALSE;
//Change MasterLoop to the sound clip you want to use.
string soundClip = "MasterLoop";
default {
    state_entry()
    {
        //Displays red "OFF" as floating text above the prim
        llSetText("OFF", <1,0,0>, 1.0);
    }
    touch_start(integer num_detected)
    {
        //When touched, soundState inverts its current boolean value. 1 becomes 0, 0 becomes 1.
        soundState = !soundState;
        if(soundState)
        {
            //Run this code when entering soundState 'on'
            //Displays green "ON" as floating text above the prim
            llSetText("ON", <0,1,0>, 1.0);
            llLoopSoundMaster(soundClip, 1.0);
        }else
        {   //Run this code when entering soundState 'off'
            //When touched, stop sound & display red "OFF" as floating text.
            llSetText("OFF", <1,0,0>, 1.0);
            llStopSound();
        }
    }
}
```

## See Also

### Functions

- **llLoopSound** — Plays a sound attached indefinitely.
- **llLoopSoundSlave** — Plays a sound attached indefinitely, and declares it as a sync slave.
- **llPlaySoundSlave** — Plays a sound attached once.
- **llSetSoundQueueing** — Enables the ability to queue sounds.

<!-- /wiki-source -->
