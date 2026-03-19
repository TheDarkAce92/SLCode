---
name: "PARCEL_DETAILS_ID"
category: "example"
type: "example"
language: "LSL"
description: "The integer constant PARCEL_DETAILS_ID has the value 5 This is a flag used with llGetParcelDetails to get the parcel UUID."
wiki_url: "https://wiki.secondlife.com/wiki/PARCEL_DETAILS_ID"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL

PARCEL_DETAILS_ID

- 1 Description
- 2 Caveats
- 3 Related Articles

  - 3.1 Constants
  - 3.2 Functions
- 4 Examples
- 5 Deep Notes

  - 5.1 History
  - 5.2 Footnotes
  - 5.3 Signature

## Description

 Constant: integer PARCEL_DETAILS_ID = 5;

The integer constant PARCEL_DETAILS_ID has the value 5


This is a flag used with llGetParcelDetails to get the parcel UUID.

## Caveats

- Division or joining of land will change the UUID of one or both parcels involved. More info on the KB. Changes to land name/desc/options/acess will NOT change the UUID. Nor will physical changes to the parcel such as new builds or terraforming.



## Related Articles

### Constants

Flag

Meaning

Max Length

Return

PARCEL_DETAILS_NAME

0

The name of the parcel.

63 Characters

string

PARCEL_DETAILS_DESC

1

The description of the parcel.

127 Characters

string

PARCEL_DETAILS_OWNER

2

The parcel owner's key.

(36 Characters)

key

PARCEL_DETAILS_GROUP

3

The parcel group's key.

(36 Characters)

key

PARCEL_DETAILS_AREA

4

The parcel's area, in sqm.

(5 Characters)

integer

PARCEL_DETAILS_ID

5

The parcel's key.

(36 Characters)

key

PARCEL_DETAILS_SEE_AVATARS

6

The parcel's avatar visibility setting

(1 character)

integer - boolean

PARCEL_DETAILS_PRIM_CAPACITY

7

The total prim capacity on this and all same-owner parcels, sim-wide.

See llGetParcelMaxPrims for same-parcel-only and/or sim-wide reporting.

integer

PARCEL_DETAILS_PRIM_USED

8

The total prim usage on this and all same-owner parcels, sim-wide.

See llGetParcelPrimCount to get prim count by parcel owner, group, temp, etc. for same-parcel-only and/or sim-wide reporting.

integer

PARCEL_DETAILS_LANDING_POINT

9

Landing point set for this parcel, if any.

vector

PARCEL_DETAILS_LANDING_LOOKAT

10

Look at vector set for the landing point on this parcel, if any.

vector

PARCEL_DETAILS_TP_ROUTING

11

Teleport routing for this parcel.

- 0 = TP_ROUTING_BLOCKED
- 1 = TP_ROUTING_LANDINGP
- 2 = TP_ROUTING_FREE

Note that routing rules are only enforced if the landing point is set.

integer

PARCEL_DETAILS_FLAGS

12

Parcel flags set for this parcel.

See llGetParcelFlags for a listing of the flags and their meaning.

integer

PARCEL_DETAILS_SCRIPT_DANGER

13

Is the script in danger in the indicated parcel.

See llScriptDanger for a discussion of script danger.

integer - boolean

Max Lengths in parentheses represent how many characters required when it is typecast to a string.

### Functions

•

llGetParcelDetails

## Examples

Two ways to create a chatted active link in-world to bring up a destination landmark window.

```lsl
default
{
    touch_start(integer nd) // Nice simple code but a long "anonymous" link...
    {       // ...and no dest position choice (returns the center of the parcel at zero Z).
        llOwnerSay("secondlife:///app/parcel/" +
                   llList2String(llGetParcelDetails(llGetPos(), [PARCEL_DETAILS_ID]), 0) +
                   "/about");
    }
    touch_end(integer nd) // Slightly more complex code but a short "decriptive" link...
    {                                           //  ...as well as dest position fine tuning.
        vector my_pos = llGetPos();
        llOwnerSay("http://slurl.com/secondlife/" +
                   llEscapeURL(llGetRegionName()) +
                   "/" +
                   ((string)llRound(my_pos.x)) +
                   "/" +
                   ((string)llRound(my_pos.y)) +
                   "/" +
                   ((string)llRound(my_pos.z)));
    }
}
```

## Deep Notes

#### History

- Suggested in [SVC-1638](https://jira.secondlife.com/browse/SVC-1638)
- Implemented in Server 1.36

[Search JIRA for related Issues](http://jira.secondlife.com/secure/IssueNavigator!executeAdvanced.jspa?jqlQuery=%28summary+%7E+%22PARCEL_DETAILS_ID%22+OR+description+%7E+%22PARCEL_DETAILS_ID%22%29+&runQuery=true)

#### Footnotes

1. **^** The parcel avatar visibility setting is used to hide avatars, their chat, and objects they sit on when they are in other parcels.

#### Signature

```lsl
integer PARCEL_DETAILS_ID = 5;
```