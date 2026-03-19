---
name: "timer"
category: "event"
type: "event"
language: "LSL"
description: "Fires repeatedly at the interval set by llSetTimerEvent"
wiki_url: "https://wiki.secondlife.com/wiki/Timer"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "timer()"
parameters: []
deprecated: "false"
---

# timer

```lsl
timer()
{
    // periodic code
}
```

Fires repeatedly at the interval set by `llSetTimerEvent`. Only one active timer per script.

## Caveats

- **Not an interrupt:** The event is queued. It will not fire while another event handler is executing.
- **Timing variability:** Actual interval may exceed the specified value due to time dilation, event queue depth, and handler execution time.
- **One timer per script:** Each script has exactly one timer. Calling `llSetTimerEvent` again replaces the current timer.
- **State changes:** The timer **persists** across state changes. If the new state has a `timer()` event handler, the existing timer will fire in it. Call `llSetTimerEvent(0.0)` in `state_exit` if you want to stop it before transitioning.
- **Script reset:** Timer is cancelled.

## Example

```lsl
float gap = 2.0;
float counter = 0.0;

default
{
    state_entry()
    {
        llSetTimerEvent(gap);
    }

    timer()
    {
        counter += gap;
        llSay(0, (string)counter + " seconds elapsed");
    }
}
```

## See Also

- `llSetTimerEvent` — start, stop, or change timer interval
- `llGetTime` — elapsed time since last script start/reset
- `llGetUnixTime` — Unix epoch timestamp


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/timer) — scraped 2026-03-18_

## Caveats

- The time between timer events can be longer than that specified with llSetTimerEvent, this is caused by:

  - **Time dilation** -  See llGetRegionTimeDilation for more information;
  - **Default event delay** - Only so many events can be triggered per second;
  - **Event Execution** - If the execution of an event takes too long;
  - **llSleep()**.
- Only one timer can be active at one time.
- The timer survives state changes, but does not survive resets.

## Examples

```lsl
float gap = 2.0;
float counter = 0.0;

default
{
    state_entry()
    {
        // Activate the timer listener every 2 seconds
        llSetTimerEvent(gap);
    }

    timer()
    {
        counter = counter + gap;
        llSay(0, (string)counter+" seconds have passed");
    }
}
```

## See Also

### Functions

- llSetTimerEvent

<!-- /wiki-source -->
