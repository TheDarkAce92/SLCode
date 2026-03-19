---
name: "llGetGMTclock"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a float that is the time in seconds since midnight GMT. Value appears to be truncated to the second.

For SL time, which is the same as California time, use llGetWallclock'
signature: "float llGetGMTclock()"
return_type: "float"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetGMTclock'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetgmtclock"]
---

Returns a float that is the time in seconds since midnight GMT. Value appears to be truncated to the second.

For SL time, which is the same as California time, use llGetWallclock


## Signature

```lsl
float llGetGMTclock();
```


## Return Value

Returns `float`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetGMTclock)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetGMTclock) — scraped 2026-03-18_

Returns a float that is the time in seconds since midnight GMT. Value appears to be truncated to the second.

## Examples

```lsl
//--// GMT function with local offsets in 12hr format //--//

integer gIntMinute = 60;    //-- 1 minute in seconds
integer gIntHour   = 3600;  //-- 1 hour in seconds
integer gInt12Hr   = 43200; //-- 12hrs in seconds
integer gIntDay    = 86400; //-- 1 day in seconds

string fStrGMTwOffset( integer vIntLocalOffset ){
   //-- get the correct time in seconds for the given offset
  integer vIntBaseTime = ((integer)llGetGMTclock() + gIntDay + vIntLocalOffset * gIntHour) % gIntDay;
  string vStrReturn;

   //-- store morning or night and reduce to 12hour format if needed
  if (vIntBaseTime < gInt12Hr){
    vStrReturn = " AM";
  }else{
    vStrReturn = " PM";
    vIntBaseTime = vIntBaseTime % gInt12Hr;
  }

   //-- get and format minutes
  integer vIntMinutes = (vIntBaseTime % gIntHour) / gIntMinute;
  vStrReturn = (string)vIntMinutes + vStrReturn;
  if (10 > vIntMinutes){
    vStrReturn = "0" + vStrReturn;
  }

   //-- add in the correct hour, force 0 to 12
  if (vIntBaseTime < gIntHour){
    vStrReturn = "12:" + vStrReturn;
  }else{
    vStrReturn = (string)(vIntBaseTime / gIntHour) + ":" + vStrReturn;
  }
  return vStrReturn;
}

default{
  touch_start( integer vIntTouched ){
     //-- '-8' is california time, no adjustment for DST
    llSay( 0, "The time is now " + fStrGMTwOffset( -8 ) );
  }
}
```

```lsl
// Gets the number of milliseconds since midnight UTC.
integer GetGMTmsclock()
{
    string stamp = llGetTimestamp();
    return
        (integer) llGetSubString(stamp, 11, 12) * 3600000 +
        (integer) llGetSubString(stamp, 14, 15) * 60000 +
        llRound((float) llGetSubString(stamp, 17, -2) * 1000.0);
}
```

## See Also

### Functions

- **llGetWallclock** — Seconds since midnight SLT (i.e. PST or PDT)

<!-- /wiki-source -->
