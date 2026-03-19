---
name: "llGiveInventory"
category: "function"
type: "function"
language: "LSL"
description: 'Give inventory to destination.

If destination is an object then it must be in the same region.
If destination is an avatar they do not have to be in the same region.'
signature: "void llGiveInventory(key destination, string inventory)"
return_type: "void"
sleep_time: "2.0"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGiveInventory'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgiveinventory"]
---

Give inventory to destination.

If destination is an object then it must be in the same region.
If destination is an avatar they do not have to be in the same region.


## Signature

```lsl
void llGiveInventory(key destination, string inventory);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `destination` | avatar or prim UUID |
| `string` | `inventory` | an item in the inventory of the prim this script is in |


## Caveats

- **Conditional sleep:** If `destination` is an avatar, the script sleeps for **2.0 seconds**. Giving to objects or attachments has no delay.
- Energy cost: **10.0**.
- Scripts reach destination **disabled** — they cannot run until the receiving object is taken to inventory and rezzed, or the script is recompiled.
- If `destination` is an avatar who declines, is in busy mode, is offline with IMs capped, or has muted the sender, the item is **deleted** — not returned to the source prim or the owner.
- No-copy items are moved (not copied) on transfer; the `changed` event does NOT fire.
- Attachments cannot give or receive no-copy inventory.
- Throttled at 5,000 gives per hour per owner per region, burst cap 2,500.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGiveInventory)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGiveInventory) — scraped 2026-03-18_

Give inventory to destination.

## Caveats

- If destination is an avatar the script sleeps for 2.0 seconds. (Giving to objects or attachments has no delay)
- If **destination** is not the owner nor shares the same owner,  and **inventory** does not have transfer permissions, an error is shouted on DEBUG_CHANNEL.
- When scripts are copied or moved between inventories, their state does not survive the transfer. Memory, event queue and execution position are all discarded.
- If inventory is missing from the prim's inventory    then an error is shouted on DEBUG_CHANNEL.
- There is no way to know if the transaction failed.  Unless you send a message when inventory is given to a prim and prim's script checks its inventory and sends a message back using llRegionSay.
- Scripts reach destination disabled (not running, and cannot be made to run unless the destination object is taken to inventory and rezzed again, or the script is recompiled). To send a running script to a prim use llSetRemoteScriptAccessPin and llRemoteLoadScriptPin.
- If destination is locked then inventory is not transferred and a **Blocked by permissions** error is shouted on the DEBUG_CHANNEL.
- If destination object is not modifiable then inventory is not transferred and a **Blocked by permissions** error is shouted on the DEBUG_CHANNEL.
- If inventory is no-copy it is transfered to destination without copying it. Since it is no-copy the only copy is given to destination; removing it from the source prim's inventory.

  - the changed event does **not** fire in this case
  - To avoid this problem use llGetInventoryPermMask to check the permissions of inventory.
- Attachments cannot give or receive no-copy inventory. When attempted an error is shouted on DEBUG_CHANNEL.
- When giving to an attachment that is not owned by the script owner, the receiving attachment must have llAllowInventoryDrop set to TRUE.
- If destination is an avatar that refuses to accept it (by manual decline or muting), is in busy mode, or is offline with instant messages capped, it is not returned to the prim's inventory; it is deleted.

  - It is not returned to the owner. It does not show up in their lost and found or any other inventory folder.
  - It is not put in the target's trash folder.
- A successful send to an offline avatar by means of llGiveInventory() counts as an IM against that avatar’s IM cap.
- As of 31th January 2012, llGiveInventory now has similar throttle to instant messages. A throttle of 5k per hour per owner per region; with a maximum burst of 2.5k. This throttle only affects gives to agents, not to non-agents.

  - "With 3k subscribers you will want to send slow enough that it takes ~45 minutes to send 1 item to each subscriber. A general safe way would be to send ~2k as fast as you can, then wait 31 minutes and send another 2k." [Kelly Linden on SVC-7631](https://jira.secondlife.com/browse/SVC-7631?focusedCommentId=308665&page=com.atlassian.jira.plugin.system.issuetabpanels:comment-tabpanel#comment-308665)
  - Be aware that while you script a system to handle the top of these limits that other busy scripted objects can be adding up to the throttle as well, such as vendors.

## Examples

```lsl
default
{
    touch_start(integer n)
    {
        //Gives this script to whoever touches the object.
        llGiveInventory(llDetectedKey(0), llGetScriptName());
    }
}
```

## See Also

### Events

- changed

### Functions

- llGiveInventoryList
- llGiveAgentInventory
- llRemoteLoadScriptPin
- llSetRemoteScriptAccessPin
- llMapDestination

<!-- /wiki-source -->
