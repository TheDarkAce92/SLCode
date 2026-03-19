---
name: "llRegionSay"
category: "function"
type: "function"
language: "LSL"
description: "Broadcasts a chat message region-wide on a non-zero channel"
wiki_url: "https://wiki.secondlife.com/wiki/llRegionSay"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "void llRegionSay(integer channel, string msg)"
parameters:
  - name: "channel"
    type: "integer"
    description: "Chat channel. Cannot be PUBLIC_CHANNEL (0)."
  - name: "msg"
    type: "string"
    description: "Message text (max 1024 bytes)"
return_type: "void"
energy_cost: "0.0"
sleep_time: "0.0"
patterns: ["llregionsay"]
deprecated: "false"
---

# llRegionSay

```lsl
void llRegionSay(integer channel, string msg)
```

Broadcasts `msg` on `channel` so it can be heard anywhere in the region by any `llListen` on that channel. Does not cross region boundaries.

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `channel` | integer | Channel (must not be 0) |
| `msg` | string | Message text (max 1024 bytes, truncated if exceeded) |

## Caveats

- **Cannot use PUBLIC_CHANNEL (0)** — this is intentional, not a bug.
- DEBUG_CHANNEL: throttled to fewer than 200 per 10 seconds per region per owner.
- Does not cross region borders.
- Max message size: 1024 bytes (truncated if longer).
- A prim cannot hear its own messages.

## Example

```lsl
default
{
    state_entry()
    {
        llRegionSay(25, "Region-wide announcement on channel 25");
    }
}
```

## See Also

- `llRegionSayTo` — region-wide to specific avatar or object
- `llSay` — 20m range
- `llShout` — 100m range
- `llListen` — receive messages


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llRegionSay) — scraped 2026-03-18_

Says the string msg on channel number channel that can be heard anywhere in the region by a script listening on channel.

## Caveats

- Messages sent on  DEBUG_CHANNEL are throttled to a rate of <200/10sec, per region, per owner/user.

  - Once the rate is exceeded, all following messages on  DEBUG_CHANNEL will be dropped until the send rate is again below 200/10sec for the previous 10 sec. Dropped messages, despite being dropped still count against the limit.
- This function cannot transmit on PUBLIC_CHANNEL channel 0, this is a design feature and not a bug.
- If msg is longer than 1024 characters it is truncated to 1024 characters. (Note that in Mono, each character occupies 2 memory bytes).
- A prim can **not** hear itself, this to prevent problems with recursion. It can however hear other prims within the same object. Use llMessageLinked instead for intra-prim messaging.

## Examples

```lsl
default
{
    state_entry()
    {
        llRegionSay(25,"This is an incredibly useless program." );
    }
}
```

To avoid making your object spam its neighborhood, use llOwnerSay or llInstantMessage.

## Notes

If one object 'says' something to another object (e.g., a button that, when touched,
turns on a lamp), consider a very negative channel, e.g.,

```lsl
    llRegionSay(-5243212,"turn on");
```

Using negative channels for script communications remains a common practice because, prior to September 2016, the standard SL client was unable to chat on negative channels. The only way to do so prior to llTextBox was to use llDialog which was limited to 24 bytes. However, since 2016, viewers have been able to chat on negative channels, with messages capped to 254 bytes.

If DEBUG_CHANNEL is used as channel, the script will say msg to the Script Warning/Error window.

If you wish two objects owned by the same person to communicate within a SIM, one idea is to make both scripts compute the channel based on the owner UUID. e.g. :-

```lsl
    gChannel = 0x80000000 | (integer) ( "0x" + (string) llGetOwner() );
```

- As of 1.18.3, using llRegionSay on the DEBUG_CHANNEL will wrap around and display on channel 0, with a range of 100m.

## See Also

### Events

- listen

### Functions

- llListen
- **llRegionSayTo** — Sends chat directly to specified target within region
- **llOwnerSay** — Sends chat to the owner only
- **llWhisper** — Sends chat limited to 10 meters
- **llSay** — Sends chat limited to 20 meters
- **llShout** — Sends chat limited to 100 meters
- llInstantMessage
- llDialog
- llTextBox

<!-- /wiki-source -->
