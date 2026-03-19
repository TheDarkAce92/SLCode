---
name: "llRegionSayTo"
category: "function"
type: "function"
language: "LSL"
description: "Says the text supplied in string msg on channel supplied in integer channel to the object or avatar specified by target"
signature: "void llRegionSayTo(key target, integer channel, string msg)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llRegionSayTo'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llregionsayto"]
---

Says the text supplied in string msg on channel supplied in integer channel to the object or avatar specified by target


## Signature

```lsl
void llRegionSayTo(key target, integer channel, string msg);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `target` | avatar or prim UUID that is in the same region |
| `integer (chat)` | `channel` |  |
| `string` | `msg` |  |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llRegionSayTo)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llRegionSayTo) — scraped 2026-03-18_

Says[1] the text supplied in string msg on channel supplied in integer channel to the object or avatar specified by target

## Caveats

- Text is spoken directly to the object or avatar within the same region as the script.
- Script in tasks other than target can neither listen for, nor receive these text messages, with an exception for attachments as described below.
- msg can be a maximum of 1024 bytes. This can convey 1024 ASCII characters, or 256-512 multibyte UTF-8 characters such as `á` (2 bytes), `ℋ` (3 bytes) or `🧡` (4 bytes).
- A prim cannot hear itself, to prevent problems with recursion. Use llMessageLinked instead for intra-prim messaging.
- Sending text on DEBUG_CHANNEL is not supported.
- Text sent to an avatar's ID on channel zero will be sent to the receiver's viewer.
- Text sent to an avatar's ID on non-zero channels can be heard by any attachment on the avatar.
- A quick series of messages sent by llRegionSayTo cannot be relied on to arrive at their destination in the same order as sent.
- There is a per-destination throttle of 200 messages sent over 10 seconds on channel zero.   Thereafter, there is also a per-sending-object throttle of 100 messages on channel zero over 300 seconds (5 minutes).  This throttle is relevant only after the first throttle is activated.  Messages sent on channels other than zero do not trigger the throttle but, once it is triggered, the block applies to *all* channels. The block is region-wide and applies to all objects with the same owner. The block apparently lasts until the region is restarted.

## Examples

```lsl
default
{
    touch_start(integer num_detected)
    {
        key id = llDetectedKey(0);

        // send a message to the chat window of the avatar touching
        llRegionSayTo(id, 0, "You touched this!");

        // send a message to the attachments of the avatar touching
        // example channel: -12345
        llRegionSayTo(id, -12345, "Hello there attachments!");
    }
}
```

## Notes

- If one object 'says' something to another object (*e.g.*, a button that, when touched, turns on a lamp), consider using a very negative channel, *e.g.*,

```lsl
llRegionSayTo("55499a64-45c3-4b81-8880-8ffb5a7c251b", -5243212, "turn on");
```

Using negative channels for script communications remains a common practice because, prior to September 2016, the standard Second Life Viewer was unable to chat directly on those channels (/-xxxx message wouldn't chat message on channel -xxxx).

- Messages sent on channel zero via llRegionSayTo() are blocked after 200 messages on to the same destination in a 10 second period.  After this throttle is activated, there is a further throttle, on objects belonging to the owner of the object that triggered the first throttle, of 100 messages per object over 5 minutes (see [BUG-5457](https://jira.secondlife.com/browse/BUG-5457)). The block is region-wide and applies to all objects belonging to the owner, so if a script triggers the throttle, all objects in the same region belonging to the same owner will also be blocked. Messages sent on channels other than zero do not trigger the throttles.  The throttles apparently reset only when the region is restarted.

Therefore, llRegionSayTo() is unsuitable for (say) verbose script debugging, and even moderate use can break users' content completely unrelated to the script for an indeterminate (and potentially very long) period of time.   Consider using llOwnerSay() for debugging instead or, if this is not appropriate, try llRegionSayTo(avatar, non-zero-channel, message) and have an attachment relay the message using llOwnerSay().

## See Also

### Events

| •  | listen | – | Receives chat |  |
| --- | --- | --- | --- | --- |

### Functions

| •  | llListen | – | Ask for listen events |  |
| --- | --- | --- | --- | --- |
| •  | llInstantMessage | – | Sends chat to a specific avatar, inside or outside the current region. |  |
| •  | llOwnerSay | – | Sends chat to the owner only to avoid spamming the PUBLIC_CHANNEL |  |
| •  | llRegionSay | – | Sends chat region wide |  |
| •  | llSay | – | Sends chat limited to 20 meters |  |
| •  | llShout | – | Sends chat limited to 100 meters |  |
| •  | llWhisper | – | Sends chat limited to 10 meters |  |

### Articles

- Hello Avatar

<!-- /wiki-source -->
