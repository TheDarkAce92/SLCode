---
name: "Timers and Scheduling"
category: "tutorials"
type: "reference"
language: "LSL"
description: "Using llSetTimerEvent to schedule recurring work, avoiding llSleep, and multiplexing multiple virtual timers from a single timer event"
wiki_url: ""
local_only: true
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
---

# Timers and Scheduling

LSL provides one timer per script via `llSetTimerEvent`. The `timer` event fires repeatedly at the interval you set. This is the correct way to schedule recurring work — not `llSleep`.

## Basic Usage

```lsl
default
{
    state_entry()
    {
        llSetTimerEvent(5.0);  // fire every 5 seconds
    }

    timer()
    {
        llSay(0, "Tick.");
    }
}
```

Call `llSetTimerEvent(0.0)` to stop the timer:

```lsl
touch_end(integer num_detected)
{
    llSetTimerEvent(0.0);  // stop
    llSay(0, "Timer stopped.");
}
```

## One Timer Per Script

Each script has exactly **one** timer. Calling `llSetTimerEvent` again while a timer is running replaces it — it does not add a second timer. The interval resets from the moment of the new call.

```lsl
// This replaces the 10-second timer with a 2-second timer:
llSetTimerEvent(10.0);
llSetTimerEvent(2.0);  // only this one runs
```

## Why Not llSleep?

`llSleep` pauses the entire script. While sleeping, the script does nothing — events that arrive queue up and are not processed until the sleep ends. If the queue fills (64 events) during a long sleep, further events are dropped.

Use `llSetTimerEvent` for recurring delays. Use `llSleep` only for very short, intentional pauses where you know no events need to be handled (for example, a short delay between consecutive `llSay` calls to avoid flooding chat).

```lsl
// Avoid this pattern for anything the user might interact with:
default
{
    state_entry()
    {
        while (TRUE)
        {
            llSay(0, "Running...");
            llSleep(5.0);  // script is unresponsive while sleeping
        }
    }
}

// Use this instead:
default
{
    state_entry()
    {
        llSetTimerEvent(5.0);
    }

    timer()
    {
        llSay(0, "Running...");
    }
}
```

## Timers Persist Across State Changes

The timer is **not** cancelled when the script changes state. It keeps running and will fire in the new state if that state has a `timer()` event handler. If the new state has no `timer()` handler, the event is simply discarded when it fires.

This means if you do not want the timer to carry over, you must stop it explicitly — either in `state_exit` or before the `state` keyword:

```lsl
default
{
    state_entry()
    {
        llSetTimerEvent(3.0);
    }

    timer()
    {
        llSetTimerEvent(0.0);  // stop before transitioning
        state active;
    }
}

state active
{
    state_entry()
    {
        llSetTimerEvent(1.0);  // start a fresh timer for this state
    }

    timer()
    {
        llSay(0, "Active tick.");
    }
}
```

If you transition via `state_exit`, stop the timer there:

```lsl
state_exit()
{
    llSetTimerEvent(0.0);
}
```

## Resetting the Interval

Each call to `llSetTimerEvent` resets the countdown from zero. This is useful for debouncing — delaying an action until activity stops:

```lsl
default
{
    listen(integer channel, string name, key id, string message)
    {
        // Reset the timer each time a message arrives.
        // The timer only fires if no message arrives for 10 seconds.
        llSetTimerEvent(10.0);
    }

    timer()
    {
        llSetTimerEvent(0.0);
        llSay(0, "No chat for 10 seconds.");
    }
}
```

## Multiplexing Multiple Virtual Timers

Because only one timer exists per script, track multiple intervals manually using global variables and a single fast timer:

```lsl
float INTERVAL_A = 2.0;   // fires every 2 seconds
float INTERVAL_B = 7.0;   // fires every 7 seconds

float next_a;
float next_b;

default
{
    state_entry()
    {
        float now = llGetTime();
        next_a = now + INTERVAL_A;
        next_b = now + INTERVAL_B;
        llSetTimerEvent(0.5);  // fast tick — check both intervals
    }

    timer()
    {
        float now = llGetTime();

        if (now >= next_a)
        {
            next_a = now + INTERVAL_A;
            llSay(0, "A fired.");
        }

        if (now >= next_b)
        {
            next_b = now + INTERVAL_B;
            llSay(0, "B fired.");
        }
    }
}
```

Use `llGetTime()` (seconds since the script started or was last reset) or `llGetUnixTime()` (Unix epoch seconds) as the time source. `llGetTime()` is a float and suitable for interval tracking within a session; `llGetUnixTime()` returns an integer and is better for wall-clock scheduling or when you need time to remain consistent across script resets.

## Minimum Interval

`llSetTimerEvent` accepts any positive float. Very fast timers increase script load — keep intervals as long as the task allows. The simulator may reduce very short intervals; a practical lower bound appears to be around 0.02 seconds, though no official minimum is documented.

## Timer Events Are Not Interrupt-Based

The `timer` event is queued like any other event. If the script is busy processing another event when the timer fires, the timer event waits in the queue. This means the timer event may be slightly late if the script is under heavy load.

## Caveats

- `llSetTimerEvent(0.0)` stops the timer. Any other value starts or restarts it.
- Only one timer per script — subsequent calls replace the previous timer.
- The timer **persists across state changes** — stop it explicitly with `llSetTimerEvent(0.0)` in `state_exit` or before the `state` keyword if you do not want it to carry over.
- The `timer` event is queued, not interrupt-based — it can be late if the script is busy.
- Avoid calling `llSetTimerEvent` from within the `timer` event with the same interval — it is unnecessary, and resets the countdown each time, which may cause drift.
