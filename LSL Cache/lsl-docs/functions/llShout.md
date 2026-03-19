---
name: "llShout"
category: "function"
type: "function"
language: "LSL"
description: "Transmits a chat message audible within 100 metres of the speaking prim"
wiki_url: "https://wiki.secondlife.com/wiki/llShout"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "void llShout(integer channel, string msg)"
parameters:
  - name: "channel"
    type: "integer"
    description: "Chat channel to transmit on"
  - name: "msg"
    type: "string"
    description: "Message text (max 1024 bytes)"
return_type: "void"
energy_cost: "0.0"
sleep_time: "0.0"
patterns: ["llshout"]
deprecated: "false"
---

# llShout

```lsl
void llShout(integer channel, string msg)
```

Broadcasts `msg` on the specified `channel`. Audible within 100 metres of the speaking prim.

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `channel` | integer | Chat channel |
| `msg` | string | Message text (max 1024 bytes) |

## Channel Constants

| Constant | Value | Purpose |
|----------|-------|---------|
| `PUBLIC_CHANNEL` | 0 | Open chat |
| `DEBUG_CHANNEL` | 0x7FFFFFFF | Script debug output |

## Caveats

- Range: 100 metres from the **speaking prim**.
- Channel 0 and DEBUG_CHANNEL throttle: fewer than 200 messages per 10 seconds per region per owner. Excess dropped.
- Max message size: 1024 bytes.
- A prim cannot hear its own shouts.

## Example

```lsl
default
{
    state_entry()
    {
        llShout(0, "I scream icecream!");
    }
}
```

## See Also

- `llWhisper` — 10m range
- `llSay` — 20m range
- `llRegionSay` — region-wide (non-zero channel only)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llShout) — scraped 2026-03-18_

Shouts the text supplied in string msg on channel supplied in integer channel.

## Caveats

- Messages sent on channel zero and DEBUG_CHANNEL are throttled to a rate of <200/10sec, per region, per owner/user.

  - Once the rate is exceeded, all following messages on channel zero or DEBUG_CHANNEL will be dropped until the send rate is again below 200/10sec for the previous 10 sec. Dropped messages, despite being dropped still count against the limit.
- Text can be a maximum of 1024 bytes. This can convey 1024 ASCII characters, or 512 UTF-8 characters such as á
- Shouts can be heard within 100 meters of the speaking prim (rather than the root). This is contrary to how listens work, where a message can only be heard by any prim in the object if and only if the root prim is capable of hearing it.
- A prim can **not** hear itself, this to prevent problems with recursion. It can however hear other prims within the same object. Use llMessageLinked instead for intra-prim messaging.

## Examples

If  you prefer, you can make use of certain mnemonic constants such as PUBLIC_CHANNEL instead of channel 0 and DEBUG_CHANNEL instead of channel +2,147,483,647.

```lsl
default
{
    state_entry()
    {
        llShout(0, "I scream icecream!");
    }
}
```

For communicating with a user or owner it is preferable to use  llOwnerSay or llInstantMessage or llRegionSayTo as they won't spam other users.

The latter is also an excellent choice for communicating to an attachment of a known avatar, or to an object of known UUID.

## See Also

### Events

- listen

### Functions

- llListen
- llOwnerSay
- **llRegionSay** — Sends chat region wide
- **llRegionSayTo** — Sends chat region wide to a specific avatar, or their attachments, or to a rezzed object of known UUID
- **llWhisper** — Sends chat limited to 10 meters
- **llSay** — Sends chat limited to 20 meters
- llInstantMessage

<!-- /wiki-source -->
