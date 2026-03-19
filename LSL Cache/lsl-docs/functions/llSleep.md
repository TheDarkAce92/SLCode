---
name: "llSleep"
category: "function"
type: "function"
language: "LSL"
description: "Pauses script execution for a specified number of seconds"
wiki_url: "https://wiki.secondlife.com/wiki/llSleep"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "void llSleep(float sec)"
parameters:
  - name: "sec"
    type: "float"
    description: "Seconds to sleep. Zero or negative causes no sleep."
return_type: "void"
energy_cost: "0.0"
sleep_time: "0.0"
patterns: ["llsleep"]
deprecated: "false"
---

# llSleep

```lsl
void llSleep(float sec)
```

Puts the script to sleep for `sec` seconds. No other code in this script executes during the sleep; events queue up.

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `sec` | float | Sleep duration in seconds |

## Caveats

- **Blocks event processing:** Events that arrive during sleep are queued. The event queue holds 64 events; overflow causes silent drops.
- **Minimum duration:** Aligned to server frame rate (~1/45 second ≈ 0.022s). `llSleep(0.0)` yields for one frame — useful for memory readings.
- **Anti-pattern:** Avoid using `llSleep` to implement recurring tasks. Use `llSetTimerEvent` instead — it does not block the event queue.
- **Zero/negative values:** No sleep occurs.

## Examples

```lsl
default
{
    state_entry()
    {
        llSay(0, "Starting...");
        llSleep(5.0);
        llSay(0, "5 seconds later.");
    }
}
```

```lsl
// Use llSleep(0.0) to yield one frame for accurate memory readings
default
{
    state_entry()
    {
        llSleep(0.0);
        llOwnerSay("Used: " + (string)llGetUsedMemory());
    }
}
```

## See Also

- `llSetTimerEvent` — preferred for periodic tasks (non-blocking)
- `timer` event — fires on interval without blocking other events


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSleep) — scraped 2026-03-18_

Puts the script to sleep for sec seconds. The script will not do anything during this time.

## Examples

```lsl
default
{
    state_entry()
    {
        llSay(0, "I going to take a nap for 5 seconds.");
        llSleep(5.0);
        llSay(0, "I feel so refreshed!");
    }
}
```

```lsl
default
{
    state_entry()
    {
        llOwnerSay("Time between sleeps:");

        integer loops = 10;
        float last_time = 0.0;

        llResetTime();
        llSleep(0.02);

        while (--loops)
        {
            float time = llGetTime();
            llOwnerSay((string)(time - last_time));
            last_time = time;
            llSleep(0.0); // Try a value above zero
        }
    }
}
```

## See Also

### Events

- timer

### Functions

- llSetTimerEvent

<!-- /wiki-source -->
