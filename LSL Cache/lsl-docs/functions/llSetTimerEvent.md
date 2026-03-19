---
name: "llSetTimerEvent"
category: "function"
type: "function"
language: "LSL"
description: "Starts or stops a repeating timer that fires the timer event at a given interval"
wiki_url: "https://wiki.secondlife.com/wiki/llSetTimerEvent"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "void llSetTimerEvent(float sec)"
parameters:
  - name: "sec"
    type: "float"
    description: "Timer interval in seconds. Pass 0.0 to stop the timer. Any positive non-zero value enables the timer."
return_type: "void"
energy_cost: "0.0"
sleep_time: "0.0"
patterns: ["llsettimerevent"]
deprecated: "false"
---

# llSetTimerEvent

```lsl
void llSetTimerEvent(float sec)
```

Sets the interval for the `timer` event. The event will fire at most once every `sec` seconds. Pass `0.0` to stop the timer.

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `sec` | float | Interval in seconds (0.0 = stop timer) |

## Caveats

- **Not an interrupt:** The timer event is queued — it will not fire while another event handler is executing.
- **Minimum practical interval:** The actual interval may be longer than specified due to time dilation (`llGetRegionTimeDilation`), event queue processing time, and event handler execution time.
- **Calling repeatedly:** If you call `llSetTimerEvent` with an interval shorter than the current interval before it fires, the timer clock resets. Calling too frequently will prevent the timer from ever firing.
- **Replacing the timer:** Calling `llSetTimerEvent` again replaces the existing timer and resets the countdown.
- **State changes:** The timer **persists** across state changes. If the new state has a `timer()` event handler, the timer will fire in it. Stop the timer explicitly in `state_exit` if you do not want it to carry over.
- **Script reset:** The timer is cancelled on script reset.
- **No forced delay on the function itself** — the 0.0 sleep applies to calling `llSetTimerEvent`, not the timer interval.

## Examples

```lsl
// Basic repeating timer
integer counter;

default
{
    state_entry()
    {
        llSetTimerEvent(2.0);  // fire every 2 seconds
    }

    touch_start(integer total_number)
    {
        llSetTimerEvent(0.0);  // stop timer on touch
        counter = 0;
    }

    timer()
    {
        ++counter;
        llSay(0, (string)counter + " ticks in " + (string)llGetTime() + "s");
    }
}
```

```lsl
// Random interval timer
default
{
    state_entry()
    {
        llSetTimerEvent(15.0 + llFrand(15.0));  // 15–30 seconds
    }

    timer()
    {
        llSay(0, "Random tick!");
        llSetTimerEvent(15.0 + llFrand(15.0));  // reset to new random interval
    }
}
```

```lsl
// Multiple virtual timers using counters
integer counterA = 0;
integer counterB = 0;

default
{
    state_entry()
    {
        llSetTimerEvent(1.0);  // 1-second base tick
    }

    timer()
    {
        ++counterA;
        ++counterB;

        if (counterA >= 10)
        {
            counterA = 0;
            llOwnerSay("Timer A fired (10s)");
        }

        if (counterB >= 30)
        {
            counterB = 0;
            llOwnerSay("Timer B fired (30s)");
        }
    }
}
```

## See Also

- `timer` event — fired by this function
- `llGetTime` — time elapsed since last script reset or `llResetTime`
- `llResetTime` — reset the script clock
- `llGetUnixTime` — Unix timestamp
- `llGetRegionTimeDilation` — current region time dilation (affects timer accuracy)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetTimerEvent) — scraped 2026-03-18_

Cause the timer event to be triggered a maximum of once every sec seconds. Passing in 0.0 stops further timer events.

## Caveats

- The time between timer events can be longer, this is caused by:

  - **Time dilation** -  See llGetRegionTimeDilation for more information.
  - **Default event delay** - Only so many events can be triggered per second.
  - **Event Execution** - If the execution of an event takes too long.
- The timer persists across state changes, but gets removed when the script is reset. So if you change to a state that has a timer() event, with the timer still running, it will fire in the new state.
- Setting a new timer replaces the old timer and resets the timer clock.

  - If you repeatedly call this function at some interval less than sec the timer event will never fire.
- The timer event is not an interrupt, it will not pause the execution of the currently running event to execute the timer. The current event must finish executing before the timer executes.

## Examples

```lsl
// default of counter is 0 upon script load
integer counter;
float   gap = 2.0;

default
{
    state_entry()
    {
        llSetTimerEvent(gap);
    }

    touch_start(integer total_number)
    {
        llSay(0, "The timer stops.");
        llSetTimerEvent(0.0);
        counter = 0;
    }

    timer()
    {
        ++counter;
        llSay(0,
            (string)counter+" ticks have passed in " + (string)llGetTime()
            + " script seconds.\nEstimated elapsed time: " + (string)(counter * gap));
    }
}
```

```lsl
//  random period in between (+15.0, +30.0]
//  which means the resulting float could be 30.0 but not 15.0

    llSetTimerEvent( 30.0 - llFrand(15.0) );

//  same results for:
//  llSetTimerEvent( 30.0 + llFrand(-15.0) );
```

```lsl
// The timer event will never fire.
default
{
    state_entry()
    {
        llSetTimerEvent(5.0);
        // Sensor every 2.5 seconds
        llSensorRepeat("", NULL_KEY, FALSE, 0.0, 0.0, 2.5);
    }

    no_sensor()
    {
        llSetTimerEvent(5.0);
    }

    timer()
    {
        llSay(0, "I will never happen.");
        llSay(0, "Well, unless llSensorRepeat() magically finds something,"+
                    "or maybe there's 2.5+ seconds of lag and the timer()"+
                    "event queues.");
    }
}
```

```lsl
// Using a timer to simulate multiple timers
integer counter_a = 0;
integer counter_b = 0;

default
{
    state_entry()
    {
        //Starting Timer Event
        llSetTimerEvent(1.0);
    }

    timer()
    {
        //Increment counters
        counter_a++;
        counter_b++;

        if(counter_a >= 100)
        {
            //Resetting Counter A
            counter_a = 0;
            llOwnerSay("Counter a has reached 100");
        }

        if(counter_b >= 200)
        {
            //Resetting counter B
            counter_b = 0;
            llOwnerSay("Counter b has reached 200");
        }

    }
}
```

## Notes

- [Notes on minimum practical llSetTimerEvent values](http://community.secondlife.com/t5/LSL-Scripting/quot-on-mouselook-quot/m-p/768291#M545), Second Life forum, 2011-03-21

## See Also

### Events

- timer

### Functions

- llSensorRepeat
- llGetRegionTimeDilation
- llGetTime

<!-- /wiki-source -->
