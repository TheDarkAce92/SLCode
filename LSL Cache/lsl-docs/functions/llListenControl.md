---
name: "llListenControl"
category: "function"
type: "function"
language: "LSL"
description: "Makes listen event callback handle active or inactive"
signature: "void llListenControl(integer number, integer active)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llListenControl'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lllistencontrol"]
---

Makes listen event callback handle active or inactive


## Signature

```lsl
void llListenControl(integer number, integer active);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer (handle)` | `handle` | handle to control listen event |
| `integer (boolean)` | `active` | TRUE (default) activates, FALSE deactivates |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llListenControl)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llListenControl) — scraped 2026-03-18_

Makes listen event callback handle active or inactive

## Caveats

- On state change or script reset all listens are removed automaticaly.

## Examples

a small example of an on and off switchable listen by use of llListenControl()

```lsl
integer handle;
integer toggle;
default
{
    state_entry()
    {
        handle = llListen(5, "", NULL_KEY, "");    // Establish a listener to listen to anything on channel 5 ...
        llListenControl(handle, FALSE);            // ... but make the listener inactive for now
        llSetText("not listening", <0.0,0.0,0.0>, 1.0);
    }

    touch_start(integer total_number)
    {
        toggle = !toggle;
        llListenControl(handle, toggle);           // Make the listener active or inactive as required

        if(toggle)
        {
            llSay(0, "now listening on channel 5");
            llSetText("listening on ch 5", <1.0,0.0,0.0>, 1.0);
        }
        else
        {
            llSay(0, "not listening any more");
            llSetText("not listening", <0.0,0.0,0.0>, 1.0);
        }
    }

    listen(integer channel, string name, key id, string message)
    {
        llSay(0, name + " just said " + message);
    }
}
```

## See Also

### Events

- listen

### Functions

- llListen
- llListenRemove

<!-- /wiki-source -->
