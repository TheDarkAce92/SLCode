---
name: "llOwnerSay"
category: "function"
type: "function"
language: "LSL"
description: "Sends a chat message to the object owner only (no range limit within the region)"
wiki_url: "https://wiki.secondlife.com/wiki/llOwnerSay"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "void llOwnerSay(string msg)"
parameters:
  - name: "msg"
    type: "string"
    description: "The message to send to the owner. Truncated to 1024 bytes."
return_type: "void"
energy_cost: "10.0"
sleep_time: "0.0"
patterns: ["llownersay"]
deprecated: "false"
---

# llOwnerSay

```lsl
void llOwnerSay(string msg)
```

Transmits `msg` to the object's owner. Unlike `llSay`, there is no distance restriction — the message reaches the owner anywhere in the same region.

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `msg` | string | Message to send (max 1024 bytes) |

## Caveats

- **Owner not in region:** Silently fails approximately 45 seconds after the owner leaves the region.
- **Group-owned objects:** Silently fails when the object is deeded to a group (there is no single owner to message).
- **Message length:** Truncated to 1024 bytes.
- **Empty messages:** Some viewers do not display `llOwnerSay` output when `msg` is empty.
- **Visual effect:** Produces particle swirls visible **only** to the owner, not to other avatars.

## Examples

```lsl
default
{
    touch_start(integer num_detected)
    {
        llOwnerSay("Ouch!");
    }
}
```

```lsl
// Debug logging pattern
debug(string msg)
{
    llOwnerSay("[DEBUG] " + msg);
}

default
{
    state_entry()
    {
        debug("Script started. Owner: " + (string)llGetOwner());
    }
}
```

```lsl
// Workaround for group-owned objects
ownerNotify(string msg)
{
    key owner = llGetOwner();
    if (llKey2Name(owner) != "")
    {
        llOwnerSay(msg);  // owner present, individual owner
    }
    else
    {
        // Group-owned: fall back to IM or whisper
        llInstantMessage(owner, msg);
    }
}
```

## See Also

- `llSay` — public chat (20m range)
- `llInstantMessage` — IM to any avatar by key
- `llRegionSayTo` — targeted region-wide message
- `llWhisper` — 10m range public chat
- `llGetOwner` — retrieve the owner's key


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llOwnerSay) — scraped 2026-03-18_

Says msg to the object's owner only, if the owner is currently in the same region.

## Caveats

- If msg is longer than 1024 bytes, it will be truncated to 1024 bytes. This can convey 1024 ASCII characters, or fewer if non-ASCII are present.
- Silently fails ~45 seconds after the owner leaves the region the object is in.
- Silently fails when the object to which the script is attached is deeded to a group.
- Some viewers do not display llOwnerSay text when msg is empty ("").
- Produces swirly particle effects for the owner (who sees the message) but these effects do not appear to be visible to other avatars (who don't).

## Examples

```lsl
default
{
    touch_start(integer num_detected)
    {
        llOwnerSay("Ouch!");
    }
}
```

## See Also

### Functions

- **llRegionSay** — Sends chat region wide
- **llWhisper** — Sends chat limited to 10 meters
- **llSay** — Sends chat limited to 20 meters
- **llShout** — Sends chat limited to 100 meters
- **llRegionSayTo** — Sends private chat region wide
- **llInstantMessage** — Sends private chat anywhere on the grid

### Articles

- **Limits** — SL limits and constrictions

<!-- /wiki-source -->
