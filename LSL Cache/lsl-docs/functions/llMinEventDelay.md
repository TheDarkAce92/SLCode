---
name: "llMinEventDelay"
category: "function"
type: "function"
language: "LSL"
description: 'Set the minimum time between events being handled.

Defaults and minimums vary by the event type, see LSL Delay.'
signature: "void llMinEventDelay(float delay)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llMinEventDelay'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llmineventdelay"]
---

Set the minimum time between events being handled.

Defaults and minimums vary by the event type, see LSL Delay.


## Signature

```lsl
void llMinEventDelay(float delay);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `float` | `delay` | time in seconds |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llMinEventDelay)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llMinEventDelay) — scraped 2026-03-18_

Set the minimum time between events being handled.

## Caveats

Minimum delay is maintained between state changes.

## Examples

```lsl
default
{
    state_entry()
    {
        llMinEventDelay(5.0);
    }
    touch(integer detected)
    {
        llSay(0, "Touched.");//Without the event delay set touch would cause the screen to fill
                             //with the word "Touched" in a split second if you held the mouse button down.
    }
}
```

Where as, if in one object you place this script (for the sake of fun call the object "Sandy Powell"). -

```lsl
default
{
    touch(integer detected)
    {
        llSay(0, "Can you hear me mother?"); //Northern English accent. Catch phase of Sandy Powell (comedian).
    }
}
```

and this in another object called "Mother" -

```lsl
default
{
    state_entry()
    {
        llMinEventDelay(5.0);
        llListen(0, "Sandy Powell", "", "");
    }
    listen(integer chan, string name, key id, string msg)
    {
        llSay(0, "Eh?");
    }
}
```

the result in chat is as follows -

[12:51]  Sandy Powell: Can you hear me mother?
[12:51]  Mother: Eh?
[12:51]  Sandy Powell: Can you hear me mother?
[12:51]  Sandy Powell: Can you hear me mother?
[12:51]  Sandy Powell: Can you hear me mother?
[12:51]  Sandy Powell: Can you hear me mother?
[12:51]  Sandy Powell: Can you hear me mother?
[12:51]  Sandy Powell: Can you hear me mother?
[12:51]  Sandy Powell: Can you hear me mother?
[12:51]  Sandy Powell: Can you hear me mother?
[12:51]  Sandy Powell: Can you hear me mother?
[12:51]  Sandy Powell: Can you hear me mother?
[12:51]  Sandy Powell: Can you hear me mother?
[12:51]  Sandy Powell: Can you hear me mother?
[12:51]  Sandy Powell: Can you hear me mother?
[12:51]  Sandy Powell: Can you hear me mother?
[12:51]  Sandy Powell: Can you hear me mother?
[12:51]  Sandy Powell: Can you hear me mother?
[12:51]  Sandy Powell: Can you hear me mother?
[12:51]  Sandy Powell: Can you hear me mother?
[12:51]  Sandy Powell: Can you hear me mother?
[12:51]  Sandy Powell: Can you hear me mother?
[12:51]  Sandy Powell: Can you hear me mother?
[12:51]  Sandy Powell: Can you hear me mother?
[12:51]  Sandy Powell: Can you hear me mother?
[12:51]  Sandy Powell: Can you hear me mother?
[12:51]  Sandy Powell: Can you hear me mother?
[12:51]  Sandy Powell: Can you hear me mother?
[12:51]  Sandy Powell: Can you hear me mother?
[12:51]  Sandy Powell: Can you hear me mother?
[12:51]  Sandy Powell: Can you hear me mother?
[12:51]  Mother: Eh?
[12:51]  Mother: Eh?
[12:51]  Mother: Eh?
[12:51]  Mother: Eh?
[12:51]  Mother: Eh?
[12:51]  Mother: Eh?
[12:52]  Mother: Eh?
[12:52]  Mother: Eh?
[12:52]  Mother: Eh?
[12:52]  Mother: Eh?
[12:52]  Mother: Eh?
[12:52]  Mother: Eh?
[12:52]  Mother: Eh?

and no more events are triggered. This is an example of lost transferred info because of llMinEventDelay so be careful with it.

## See Also

### Articles

- **LSL Delay** — for default values

<!-- /wiki-source -->
