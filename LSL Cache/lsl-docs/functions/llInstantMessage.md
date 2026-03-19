---
name: "llInstantMessage"
category: "function"
type: "function"
language: "LSL"
description: "Sends a private instant message to a specific avatar by UUID"
wiki_url: "https://wiki.secondlife.com/wiki/llInstantMessage"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "void llInstantMessage(key user, string message)"
parameters:
  - name: "user"
    type: "key"
    description: "UUID of the recipient avatar"
  - name: "message"
    type: "string"
    description: "Message text (max 1024 bytes)"
return_type: "void"
energy_cost: "10.0"
sleep_time: "2.0"
patterns: ["llinstantmessage"]
deprecated: "false"
---

# llInstantMessage

```lsl
void llInstantMessage(key user, string message)
```

Sends a private instant message to `user`. Works regardless of distance or region. Causes a 2.0-second forced delay.

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `user` | key | Recipient avatar UUID |
| `message` | string | Message text (max 1024 bytes) |

## Caveats

- **2.0-second forced delay** — the script sleeps for 2 seconds after each call.
- Works even if the avatar is offline (message is delivered when they log in).
- Works across regions.
- Throttled to prevent spam.
- Do not use for high-frequency messaging — use `llRegionSayTo` for in-region targeted chat.

## Example

```lsl
default
{
    touch_start(integer num_detected)
    {
        key toucher = llDetectedKey(0);
        llInstantMessage(toucher, "Thanks for touching me!");
    }
}
```

## See Also

- `llOwnerSay` — message to owner (no delay, within same region)
- `llRegionSayTo` — targeted message within region (no delay)
- `llSay` — public chat within 20m
- `llKey2Name` — get avatar name from UUID


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llInstantMessage) — scraped 2026-03-18_

Sends an Instant Message specified in the string message to the user specified by user.

## Caveats

- This function causes the script to sleep for 2.0 seconds.
- All object IMs are throttled at a maximum of 2500 per 30mins, per owner, per region, in a rolling window. This includes IMs sent after the throttle is in place.

  - Throttled IMs are dropped. for implementation see notes below.
- Messages longer than 1023 bytes will be truncated to 1023 bytes. This can convey 1023 ASCII characters, or fewer if non-ASCII characters are present.

- If the specified user is logged in, message will appear in the chat window and will not logged by the InstantMessage logging facility.
- If the specified user is not signed in, the messages will be delivered to their email just like a regular instant message, if the user has enabled email for their account.

  - If messages are sent to the same user by the same object within about 65 seconds, they will be bundled together in a single email.

## Examples

Tell the owner somebody touched the object:

```lsl
default
{
    touch_start( integer total_num )
    {
        llInstantMessage( llGetOwner(), "Someone touched me" );
    }
}
```

Send an IM to a detected avatar only

```lsl
default
{
    touch_start( integer total_num )
    {
        llInstantMessage( llDetectedKey(0), "Hands Off!");
    }
}
```

## Notes

- llRegionSayTo may be a better choice if the target is in the same region as the object sending the message, as it has no built-in delay and can communicate directly with objects, as well as with avatars and their attachments.
- Instant Messaging allows communication from an object to an avatar anywhere on the Grid. However, an object cannot receive an Instant Message.
- Using llInstantMessage from one or more child scripts will avoid delays in the main script. Child scripts will still be subject to delays, message queue limits, and region throttles.
- Throttling Implementation (Kelly Linden):

  - The throttle is on all IMs from the object owner. It does not disable all IMs in the region, but does disable all IMs from the owner of the object.
  - The throttle is not per object, but per owner. Splitting the spamming object into multiple objects will not help unless owned by different people. This also means that owning multiple almost too spammy objects will cause you to hit the limit.
  - 2500 IMs in 30 minutes will trigger the block.
  - IMs that are blocked continue to count against the throttle. The IM count must drop below 2500 before any IMs will be delivered.
  - The IM count of the previous window is used to approximate the rolling window. If it is 20% into the current window the IM count will be the current count + 80% of the previous count. This allows us to approximate a rolling average, however it has the behavior that a flood of IMs can have an effect on the throttle for double the window length. This is why in practice the throttle behaves more like 5k in 1hr than 2.5k in 30min.

## See Also

### Functions

- **llOwnerSay** — Sends chat region wide to owner
- **llRegionSay** — Sends chat region wide
- **llRegionSayTo** — Sends chat region wide to a specific prim/avatar
- **llWhisper** — Sends chat limited to 10 meters
- **llSay** — Sends chat limited to 20 meters
- **llShout** — Sends chat limited to 100 meters

<!-- /wiki-source -->
