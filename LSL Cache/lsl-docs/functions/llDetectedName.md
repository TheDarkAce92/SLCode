---
name: "llDetectedName"
category: "function"
type: "function"
language: "LSL"
description: "Returns the name of the Nth detected object or avatar in a detection event"
wiki_url: "https://wiki.secondlife.com/wiki/llDetectedName"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "string llDetectedName(integer item)"
parameters:
  - name: "item"
    type: "integer"
    description: "Zero-based index of the detected entity. Does not support negative indexes."
return_type: "string"
energy_cost: "0.0"
sleep_time: "0.0"
patterns: ["lldetectedname"]
deprecated: "false"
---

# llDetectedName

```lsl
string llDetectedName(integer item)
```

Returns the name of the detected object or avatar at index `item`. For avatars, returns the legacy name (e.g., "John Doe" or "John Resident").

## Valid Contexts

Only works inside: `collision_start`, `collision`, `collision_end`, `sensor`, `touch_start`, `touch`, `touch_end`.

## Caveats

- Out-of-bounds `item` returns `NULL_KEY` silently — no error message.
- Fails silently outside detection events.

## Example

```lsl
default
{
    touch_start(integer num_detected)
    {
        string name = llDetectedName(0);
        llOwnerSay("Touched by " + name);
    }
}
```

## See Also

- `llDetectedKey` — UUID of detected entity
- `llKey2Name` — convert UUID to name
- `llGetUsername` / `llRequestUsername` — fetch display name or username


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llDetectedName) — scraped 2026-03-18_

Returns a string that is the name of the detected item.

## Caveats

- If item is out of bounds this function returns NULL_KEY and the script continues to execute without an error message.
- Events that enable the llDetected* functions always return at least one detected item.

  - Detection events are not raised if there is nothing detected.
  - The detection event's items detected parameter is initially never less than 1.

## Examples

```lsl
default
{
    touch_start(integer num_detected)
    {
        string name = llDetectedName(0);

        llOwnerSay("Touched by " + name);

       // name is the legacy name, as in "John Doe", or "John Resident" if the avatar has the default last name.
    }
}
```

## See Also

### Articles

- Detected

<!-- /wiki-source -->
