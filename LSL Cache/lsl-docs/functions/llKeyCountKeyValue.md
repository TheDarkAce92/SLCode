---
name: "llKeyCountKeyValue"
category: "function"
type: "function"
language: "LSL"
description: 'Start an asynchronous transaction to request the number of keys with the script's Experience.

Returns a handle (a key) that can be used to identify the corresponding dataserver event to determine if this command succeeded or failed and the results.'
signature: "key llKeyCountKeyValue()"
return_type: "key"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llKeyCountKeyValue'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
flags: "experience-api"
patterns: ["llkeycountkeyvalue"]
---

Start an asynchronous transaction to request the number of keys with the script's Experience.

Returns a handle (a key) that can be used to identify the corresponding dataserver event to determine if this command succeeded or failed and the results.


## Signature

```lsl
key llKeyCountKeyValue();
```


## Return Value

Returns `key`.


## Caveats

- Energy cost: **10.0**.
- Requires an active **Experience** (Experience API function).


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llKeyCountKeyValue)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llKeyCountKeyValue) — scraped 2026-03-18_

Start an asynchronous transaction to request the number of keys with the script's Experience.Returns a handle (a key) that can be used to identify the corresponding dataserver event to determine if this command succeeded or failed and the results.

## Caveats

- If you recompile a script that was previously associated with an Experience but do so with a client that lacks the ability to compile scripts into an experience the script will lose the associated Experience.

## Examples

```lsl
key trans;
default
{
    state_entry()
    {
        trans = llKeyCountKeyValue();
    }

    dataserver(key t, string value)
    {
        if (t == trans)
        {
            // our llKeyCountKeyValue transaction is done
            list result = llCSV2List(value);
            if (llList2Integer(result, 0) == 1)
            {
                // data size retrieved
                llSay(0, "Keys in use: "+llList2String(result, 1));
            }
            else
            {
                // key count failed
                llSay(0, "Key-value failed to count keys: " + llList2String(result, 1) );
            }
        }
    }
}
```

## Notes

#### Compiling

For a script to be associated with an Experience...

- It must be compiled with a client that is Experience aware,
- The "Use Experience" checkbox must be checked,
- And one of the users Experience keys selected.

|  | Important: Not all TPVs have this functionality. |
| --- | --- |

## See Also

### Functions

- llGetExperienceErrorMessage
- llCreateKeyValue
- llReadKeyValue
- llUpdateKeyValue
- llDeleteKeyValue
- llDataSizeKeyValue
- llKeyCountKeyValue
- llKeysKeyValue

<!-- /wiki-source -->
