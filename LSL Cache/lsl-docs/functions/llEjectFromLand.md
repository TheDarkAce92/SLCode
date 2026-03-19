---
name: "llEjectFromLand"
category: "function"
type: "function"
language: "LSL"
description: 'Ejects avatar from the parcel.

Generally, the object owner must also be the land owner but there is an exception for land deeded to a group for group members with the 'Eject and freeze Residents on parcels' ability. See #Ownership Limitations for details.'
signature: "void llEjectFromLand(key avatar)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llEjectFromLand'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llejectfromland"]
---

Ejects avatar from the parcel.

Generally, the object owner must also be the land owner but there is an exception for land deeded to a group for group members with the "Eject and freeze Residents on parcels" ability. See #Ownership Limitations for details.


## Signature

```lsl
void llEjectFromLand(key avatar);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `avatar` | avatar UUID that is in the same region |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llEjectFromLand)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llEjectFromLand) — scraped 2026-03-18_

Ejects avatar from the parcel.

## Examples

```lsl
// Here a script done by shenanigan oh

//It's a easy script that I came up with. When I worked for a carnage I put this script in a computer that was
//attached to me. The carnage it self was a pvp sims so it was alot easier and fast to eject some this way
//then running after them and clicking on them. The way this work is by trying eject and half type plays name.
//Example: /1 eject shenan

//Warning if you type someone name in short be careful of other plays with same name!
string msg;
string name;
default
{
    on_rez(integer n)
    {
        llResetScript();
    }

    state_entry()
    {
        llListen(1, "", llGetOwner(), "");
        llListen(0, "", llGetOwner(), "");
    }

    listen(integer n, string m, key k, string msg)
    {
        if (llGetSubString(msg, 0, 5) == "eject ")
        {
            name = llToLower(llStringTrim(llDeleteSubString(msg, 0, 5), STRING_TRIM));
            llSensor("", "", AGENT, 96, PI);
        }
    }

    sensor(integer n)
    {
        integer i = 0;
        for (;i

<!-- /wiki-source -->
