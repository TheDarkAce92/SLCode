---
name: "llGetMemoryLimit"
category: "function"
type: "function"
language: "LSL"
description: 'Get the maximum memory a script can use.

Returns the integer amount of memory the script can use in bytes.'
signature: "integer llGetMemoryLimit()"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetMemoryLimit'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetmemorylimit"]
---

Get the maximum memory a script can use.

Returns the integer amount of memory the script can use in bytes.


## Signature

```lsl
integer llGetMemoryLimit();
```


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.

## Example

```lsl
default
{
    state_entry()
    {
        llSetMemoryLimit(4000);
        llSay(0, "Memory free: " + (string)llGetFreeMemory() + " bytes, limit: " +
            (string)llGetMemoryLimit() + " bytes.");
    }
}
```

## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetMemoryLimit)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetMemoryLimit) — scraped 2026-03-18_

Get the maximum memory a script can use.Returns the integer amount of memory the script can use in bytes.

## Examples

```lsl
default
{
    state_entry()
    {
        llSetMemoryLimit( 4000 ); // set the memory limit

        // display memory usage...
        llSay(0, "Memory used: " + (string)llGetFreeMemory() + " bytes, total memory: " +
            (string)llGetMemoryLimit() + " bytes." );
    }
}

// outputs
// Object: Memory used: 124 bytes, total memory: 4000 bytes.
```

## See Also

### Functions

- llSetMemoryLimit
- llGetFreeMemory
- llGetUsedMemory
- llGetObjectDetails

<!-- /wiki-source -->
