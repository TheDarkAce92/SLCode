---
name: "llDetectedKey"
category: "function"
type: "function"
language: "LSL"
description: "Returns the UUID of the Nth detected object or avatar in a detection event"
wiki_url: "https://wiki.secondlife.com/wiki/llDetectedKey"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "key llDetectedKey(integer number)"
parameters:
  - name: "number"
    type: "integer"
    description: "Zero-based index of the detected entity. Does not support negative indexes."
return_type: "key"
energy_cost: "0.0"
sleep_time: "0.0"
patterns: ["lldetectedkey"]
deprecated: "false"
---

# llDetectedKey

```lsl
key llDetectedKey(integer number)
```

Returns the UUID of the detected object or avatar at index `number`. Valid only within detection event handlers.

## Return Value

`key` — UUID of the detected entity, or empty key if `number` is out of bounds.

## Valid Contexts

Only works inside these events:
- `collision_start`, `collision`, `collision_end`
- `sensor`, `no_sensor`
- `touch_start`, `touch`, `touch_end`

Returns an unusable value if called outside these events.

## Caveats

- Out-of-bounds `number` silently returns empty key with no error.
- Detection events always have at least one detection (index 0 always valid when the event fires).
- Does not support negative indices.

## Example

```lsl
default
{
    touch_start(integer num_detected)
    {
        llSay(0, "Touched by: " + (string)llDetectedKey(0));
    }
}
```

## See Also

- `llDetectedName` — name of detected entity
- `llDetectedPos` — position of detected entity
- `llDetectedType` — type flags of detected entity
- `llDetectedOwner` — owner of detected object


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llDetectedKey) — scraped 2026-03-18_

Returns a key that is the UUID of the detected object or avatar number.

## Caveats

- If number is out of bounds  the script continues to execute without an error message.
- Events that enable the llDetected* functions always return at least one detected item.

  - Detection events are not raised if there is nothing detected.
  - The detection event's items detected parameter is initially never less than 1.

## Examples

```lsl
default
{
    touch_start(integer num_detected)
    {
        llSay(0, "touch_start event: key of avatar touching: " + (string) llDetectedKey(0) );
    }
}
```

## See Also

### Articles

- Detected

<!-- /wiki-source -->
