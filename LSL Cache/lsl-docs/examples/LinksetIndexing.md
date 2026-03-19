---
name: "LinksetIndexing"
category: "example"
type: "example"
language: "LSL"
description: "Searches for multiple prims that share a common specific name and returns a list of linkset numbers. Otherwise an empty list if none found."
wiki_url: "https://wiki.secondlife.com/wiki/LinksetIndexing"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 By Exact Name

  - 1.1 One Name - Multiple Links
  - 1.2 One Name - One Link
  - 1.3 Multiple Names - One Link each
  - 1.4 Multiple Names - Roll Your Own Loop

## By Exact Name

### One Name - Multiple Links

Searches for multiple prims that share a common specific name and returns a list of linkset numbers. Otherwise an empty list if none found.

```lsl
list LinkedList(string Needle) {
    list Needles;
    integer Hay = 1;
    integer Stacks = llGetNumberOfPrims();
    for(; Hay <= Stacks; ++Hay ) if(llGetLinkName(Hay) == Needle) Needles += Hay;
    return Needles;
}
```

Input

Description

string Needle

Common name that multiple prims share.

Output

Description

return list LinkedList

Returns list of linkset numbers that have exactly same prim name as Needle does.

Released into public domain. By Nexii Malthus.



### One Name - One Link

Searches for a single prim that has a specific name. Returns 0 if not found.

```lsl
integer Linked(string Needle) {
    integer Prims = llGetNumberOfPrims()+1;
    while(--Prims) if(llGetLinkName(Prims) == Needle) return Prims;
    return FALSE;
}
```

Input

Description

string Needle

Specific name that a prim possesses.

Output

Description

return integer Linked

Returns integer linkset number of a prim that has exactly same prim name as Needle does.

Released into public domain. By Nexii Malthus.



### Multiple Names - One Link each

Searches and replaces all strings in Needles list with integer linkset numbers, where the strings exactly match a prim name.

```lsl
list ListLinked(list Needles) {
    integer Prims = llGetNumberOfPrims()+1;
    while(--Prims) {
        integer Ptr = llListFindList(Needles,[llGetLinkName(Prims)]);
        if(~Ptr) Needles = llListReplaceList(Needles,[Prims],Ptr,Ptr);
    }
    return Needles;
}
```

Input

Description

list Needles

Specific names that prims possess.

Output

Description

return list ListLinked

Returns list of linksets number of prims that had exact same prim names as the list position in Needles did.

Released into public domain. By Nexii Malthus.



### Multiple Names - Roll Your Own Loop

This is how I do most of my linkset indexing. A loop with if-else conditions, it is as simple as you can get.

Create a global integer for each linkset you want to track and then an if-else condition to assign the linkset number to it.

```lsl
integer Foot;
integer Leg;
integer Torso;
integer Head;

LinksetInit() {
    integer Prims = llGetNumberOfPrims();
    do {
        string Prim = llGetLinkName(Prims);
        if(Prim == "Foot") Foot = Prims; else
        if(Prim == "Leg") Leg = Prims; else
        if(Prim == "Torso") Torso = Prims; else
        if(Prim == "Head") Head = Prims;
    }
    while(--Prims > 1);
}
```

Released into public domain. By Nexii Malthus.