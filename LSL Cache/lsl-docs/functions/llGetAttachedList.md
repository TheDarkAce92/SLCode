---
name: "llGetAttachedList"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a list of object keys corresponding to public attachments worn by an avatar.

By design HUD attachment keys are not reported by this function.

If avatar is a child agent, ['NOT ON REGION'] is returned.
If avatar is not a main agent and not a child agent or not an agent at all, ['NOT FOUND']'
signature: "list llGetAttachedList(key agent)"
return_type: "list"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetAttachedList'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetattachedlist"]
---

Returns a list of object keys corresponding to public attachments worn by an avatar.

By design HUD attachment keys are not reported by this function.

If avatar is a child agent, ["NOT ON REGION"] is returned.
If avatar is not a main agent and not a child agent or not an agent at all, ["NOT FOUND"] is returned.


## Signature

```lsl
list llGetAttachedList(key agent);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `avatar` | avatar UUID that is in the same region |


## Return Value

Returns `list`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetAttachedList)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetAttachedList) — scraped 2026-03-18_

Returns a list of object keys corresponding to public attachments worn by an avatar in the order they were attached.

## Caveats

When an avatar first arrives in a region, there is a brief period when their attachments are not yet fully rezzed or added.  During this time, those attachments will not appear in the results.

## Examples

```lsl
// Touch to list all attachments

default
{
    touch_start(integer total_number)
    {
        list AttachedNames;
        list AttachedUUIDs = llGetAttachedList(llDetectedKey(0));
        integer i;
        while (i < llGetListLength(AttachedUUIDs) )
        {
            list temp = llGetObjectDetails(llList2Key(AttachedUUIDs,i),[OBJECT_NAME]);
            AttachedNames += [llList2String(temp,0)];
            ++i;
        }
        llSay(PUBLIC_CHANNEL,"\n" + llDumpList2String(AttachedNames,"\n"));
    }
}
```

## See Also

### Events

- attach

### Functions

- llGetAttached
- llGetAttachedListFiltered
- llAttachToAvatar
- llDetachFromAvatar
- llAttachToAvatar
- **llGetObjectDetails** — OBJECT_ATTACHED_POINT

<!-- /wiki-source -->
