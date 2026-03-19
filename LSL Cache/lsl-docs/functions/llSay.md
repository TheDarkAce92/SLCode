---
name: "llSay"
category: "function"
type: "function"
language: "LSL"
description: "Broadcasts a message on a chat channel, audible 20m away"
wiki_url: "https://wiki.secondlife.com/wiki/llSay"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "void llSay(integer channel, string msg)"
parameters:
  - name: "channel"
    type: "integer"
    description: "Chat channel to transmit on. Use PUBLIC_CHANNEL (0) for open chat, DEBUG_CHANNEL (0x7FFFFFFF) for debug output, or any negative integer for private channels."
  - name: "msg"
    type: "string"
    description: "The message text to transmit. Truncated to 1024 bytes."
return_type: "void"
energy_cost: "10.0"
sleep_time: "0.0"
patterns: ["llsay"]
deprecated: "false"
---

# llSay

```lsl
void llSay(integer channel, string msg)
```

Broadcasts `msg` on the specified `channel`. The message can be heard by any script using `llListen` on the same channel within 20 metres of the speaking prim (not the root prim).

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `channel` | integer | Chat channel to transmit on |
| `msg` | string | Message text (max 1024 bytes) |

## Channel Constants

| Constant | Value | Purpose |
|----------|-------|---------|
| `PUBLIC_CHANNEL` | 0 | Open chat — visible to nearby avatars in chat history |
| `DEBUG_CHANNEL` | 0x7FFFFFFF | Script debug output — visible to owner only |

## Caveats

- **Throttle:** Messages on channel 0 and `DEBUG_CHANNEL` are throttled to fewer than 200 per 10 seconds per region per owner. Excess messages are silently dropped.
- **Range:** Audible range is 20 metres from the **speaking prim** (not the linkset root). Some simulators allow querying the actual range with `llGetEnv("chat_range")`.
- **Message size:** Maximum 1024 bytes. One UTF-8 character may be 1–4 bytes, so 1024 ASCII characters or fewer for multibyte content.
- **Self-deafness:** A prim cannot hear its own `llSay` output (prevents recursion). Linked prims can hear each other.
- **Not for physical objects sending to themselves:** Use `llMessageLinked` for intra-object communication.

## Examples

```lsl
default
{
    state_entry()
    {
        llSay(0, "Hello, Avatar!");
    }
}
```

```lsl
default
{
    touch_start(integer num_detected)
    {
        llSay(PUBLIC_CHANNEL, "You touched me!");
        llSay(DEBUG_CHANNEL, "Touch detected, sender: " + (string)llDetectedKey(0));
    }
}
```

## See Also

- `llWhisper` — 10 metre range
- `llShout` — 100 metre range
- `llOwnerSay` — owner only (no range limit in same region)
- `llRegionSay` — region-wide (channel must be non-zero)
- `llRegionSayTo` — targeted region-wide message
- `llInstantMessage` — private IM to a specific avatar
- `llListen` — receive chat messages


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSay) — scraped 2026-03-18_

Says the text supplied in string msg on channel supplied in integer channel. The message can be heard 20m away, usually (see caveats)

## Caveats

- Messages sent on channel zero and DEBUG_CHANNEL are throttled to a rate of <200/10sec, per region, per owner/user.

  - Once the rate is exceeded, all following messages on channel zero or DEBUG_CHANNEL will be dropped until the send rate is again below 200/10sec for the previous 10 sec. Dropped messages, despite being dropped still count against the limit.
- msg can only be heard within 20 meters of the speaking prim (rather than the root). This is contrary to how the event listen works, where a msg can only be heard by any prim in the object if and only if the root prim is capable of hearing it.
- Some simulators (mostly event sims or linden-owned ones) have `llGetEnv("chat_range")` set to a value other than 20. On these sims:

  - `llSay(0, msg)` can be heard in a radius of `llGetEnv("chat_range")`
  - `llSay(any_other_channel, msg)` can be heard in a radius of 20m
  - as of 2023-03-26, [Hippotropolis](http://maps.secondlife.com/secondlife/Hippotropolis/67/188/28) (a linden meeting sim) has a chat range of 40m
- msg can be a maximum of 1024 bytes. This can convey 1024 ASCII characters, or 256-512 multibyte UTF-8 characters such as `á` (2 bytes), `ℋ` (3 bytes) or `🧡` (4 bytes).

  - If a multibyte character ends up on the 1024 byte boundary, it is discarded and not split into invalid bytes.
- A prim can **not** hear itself, this to prevent problems with recursion. It can however hear other prims within the same object. Use llMessageLinked instead for intra-prim messaging.

## Examples

```lsl
default
{
    state_entry()
    {
        llSay(0, "Hello, Avatar!");
    }
}
```

To avoid making your object spam its neighborhood, use llInstantMessage, llOwnerSay or llRegionSayTo.

## Notes

- Channel 0 is the PUBLIC_CHANNEL. Everyone can hear chat transmitted on this channel. All other channels are private channels (not sent to users, with the exception of DEBUG_CHANNEL).
- Consider using llInstantMessage, llOwnerSay, or the DEBUG_CHANNEL for debugging purposes. If DEBUG_CHANNEL is used as channel, the script will say msg to the Script Warning/Error window.

  - Note, however, that when using DEBUG_CHANNEL, what *you* consider to be 'debugging messages' will still be seen by others as *scripting errors* indicated by the floating 'script error' icon.
- If one object 'says' something to another object (*e.g.*, a button that, when touched, turns on a lamp), it is a good idea to use a very negative channel, *e.g.*, `-5243212` but don't just use any number take a look at the User-Defined Protocols & APIs and choose one that won't interfere with other protocols. If you are going to sell your script widely, please add it to the appropriate known chat channels list so others won't interfere with your product (do keep in mind you should build your product so that it handles interference appropriately).

```lsl
    llSay(-5243212,"turn on");
```

From at least September 2016 (see Release Notes/Second Life Release/4.0.9.320038), viewers have been able to chat on negative channels, although chat from viewers is [limited to 254 characters](https://jira.secondlife.com/browse/BUG-41541). (Chat from objects caps at 1024 bytes, whether the channel is negative or not). Negative channels were popular for script communications because the standard SL client was unable to chat directly on those channels (`/-xxxx message` would not chat `message` on channel `-xxxx`). The only way for a viewer to generate chat on negative channels prior to llTextBox was to use llDialog which was limited to 24 bytes.

- Be aware that if you mistakenly use an integer bigger than the maximum or smaller than the minimum, SL will treat the literal number as a float and convert it implicitly to an out-of-range integer, resulting in `1`, *without* giving a script/syntax error (since this implicit conversion is legitimate). This means that all scripts listening to an out-of-range integer will be listening to channel 1 instead! (see also llListen).
- Objects with all-whitespace names (e.g., a space or a series of spaces) will appear as "(Unnamed)" if they emit chat via llSay, although this behaviour may vary in third-party viewers.

## See Also

### Events

- **listen** — Receives chat

### Functions

- **llListen** — Ask for listen events
- **llInstantMessage** — PUBLIC_CHANNEL
- **llOwnerSay** — PUBLIC_CHANNEL
- **llRegionSay** — Sends chat region wide
- **llRegionSayTo** — Sends chat region wide to a specific avatar, or their attachments, or to a rezzed object of known UUID
- **llShout** — Sends chat limited to 100 meters
- **llWhisper** — Sends chat limited to 10 meters

### Articles

- Hello Avatar

<!-- /wiki-source -->
