---
name: "llKey2Name"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a string that is the legacy name of the prim or avatar specified by id.

id must specify a valid rezzed prim or avatar key, present in or otherwise known to the sim in which the script is running, otherwise an empty string is returned. In the case of an avatar, this function will still retur'
signature: "string llKey2Name(key id)"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llKey2Name'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llkey2name"]
---

Returns a string that is the legacy name of the prim or avatar specified by id.

id must specify a valid rezzed prim or avatar key, present in or otherwise known to the sim in which the script is running, otherwise an empty string is returned. In the case of an avatar, this function will still return a valid name if the avatar is a child agent of the sim (i.e., in an adjacent sim, but presently able to see into the one the script is in), or for a short period after the avatar leaves the sim (specifically, when the client completely disconnects from the sim, either as a main or child agent).

Keys of inventory items will not work; in the case of these, use llGetInventoryName instead.


## Signature

```lsl
string llKey2Name(key id);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `id` | avatar or prim UUID that is in the same region |


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llKey2Name)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llKey2Name) — scraped 2026-03-18_

Returns a string that is the legacy name of the prim or avatar specified by id.

## Caveats

- It is difficult to tell the difference between a prim that has a name that is an empty string and a prim that is not in the sim, or because an invalid key was specified. Use llGetObjectDetails to avoid this problem.
- To get around the "avatar must be present" limitation, you can use the llRequestAgentData function and the dataserver event to obtain the avatar's name from a key.
- The opposite function (llName2Key) can be used to find the user key associated with an avatar in the same region. To find the user key of an avatar anywhere on the grid, use llRequestUserKey, which triggers a dataserver event.
- If an avatar is "ghosted" (which occasionally happens due to a longstanding server bug), an empty string is returned even though the avatar is seemingly present and shows up in llSensor and the Mini-Map.  This fact can be used as the basis of a Ghost Detector script.
- Unlike the related functions llGetUsername and llRequestUsername, this function returns a 'nice' name in proper case and - if applicable - with a space, e.g. "Peter Stindberg", instead of "peter.stindberg" (or "Josh" instead of "josh.resident") as returned by the other two functions.

## Examples

```lsl
// Best viewed in Chat History (ctrl-h)

default
{
    collision_start(integer num_detected)
    {
        key id = llDetectedKey(0);
        string name = llKey2Name(id);

        string detectedName = llDetectedName(0);

        llSay(0, "llKey2Name: " + name
            + "\nllDetectedName: " + detectedName);
    }

    touch_start(integer num_detected)
    {
        key id = llDetectedKey(0);
        string name = llKey2Name(id);

        string detectedName = llDetectedName(0);

        llSay(0, "llKey2Name: " + name
            + "\nllDetectedName: " + detectedName);
    }
}
```

## Notes

**World Wide Web Consortium**

- N2K - Independent of databases or bots, this uses the [W3C html2text](http://cgi.w3.org/cgi-bin/html2txt) to convert the viewer search to text and extract the key from Second Life's own services.

**Active Name2Key Databases:**

- [W-Hat name2key](http://w-hat.com/name2key) (last names replaced with the *Resident* word for the Usernames)
- [KDC name2key](http://kdc.ethernia.net/sys/name2key.php)

**Dead Name2Key Databases:**

- [Kubwa name2key](http://kubwa.net/index.php?cmd=name2key) (Bot based name2key Database; Supports: Legacy and Username formats; Shows related names; SSL support.) (Appears to be gone as of Apr 2013 [Reports Error 404])
- [http://wiki.apez.biz/Development](http://wiki.apez.biz/Development) (web-service API functions getAvatarKey and getAvatarName) (Apez seems to be gone ? - May 2011)
- [http://www.libsecondlife.org/protocol/index.php/Name2key](http://www.libsecondlife.org/protocol/index.php/Name2key)(Appears to be gone as of Apr 2008, but search for name2key on that site for more information)
- [http://www.ulrikasheim.org/tools/name2key.html](http://www.ulrikasheim.org/tools/name2key.html)(Appears to be gone as of Apr 2008)
- [DB4MV name2key](http://www.db4mv.info) (Name2Key Database for Avatars (Legacy Names,Usernames, and Display Names, GroupNames and Keys, LSL API)(Currently listed as non-existant by host)

**Name2Key Libraries:**

- Name2Key_in_LSL
- Ugleh Ulrik's Name2Key PHP script
- Failsafe name2key script

## See Also

### Functions

- llGetUsername
- llGetDisplayName
- llGetObjectDetails
- **llRequestAgentData** — dataserver

### Articles

- Prim Attribute Overloading

<!-- /wiki-source -->
