---
name: "llKeysKeyValue"
category: "function"
type: "function"
language: "LSL"
description: 'Start an asynchronous transaction to request a number of keys from the script's Experience.

Returns a handle (a key) that can be used to identify the corresponding dataserver event to determine if this command succeeded or failed.

This function will attempt to retrieve the number of keys requested'
signature: "key llKeysKeyValue(integer start, integer count)"
return_type: "key"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llKeysKeyValue'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
flags: "experience-api"
patterns: ["llkeyskeyvalue"]
---

Start an asynchronous transaction to request a number of keys from the script's Experience.

Returns a handle (a key) that can be used to identify the corresponding dataserver event to determine if this command succeeded or failed.

This function will attempt to retrieve the number of keys requested but may return less if there are not enough to fulfill the full amount requested or if the list is too large. The length of the returned list is limited to 4097 characters (the success flag "1" and 4096 characters). The order keys are returned is not guaranteed but is stable between subsequent calls as long as no keys are added or removed.
The error XP_ERROR_KEY_NOT_FOUND is returned if there index given is greater than or equal to the number of keys.

For this function to work, the script must be compiled into an Experience.


## Signature

```lsl
key llKeysKeyValue(integer start, integer count);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `first` | Zero-based index of the first key to retrieve |
| `integer` | `count` | Number of keys to retriever |


## Return Value

Returns `key`.


## Caveats

- Energy cost: **10.0**.
- Requires an active **Experience** (Experience API function).


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llKeysKeyValue)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llKeysKeyValue) — scraped 2026-03-18_

Start an asynchronous transaction to request a number of keys from the script's Experience.Returns a handle (a key) that can be used to identify the corresponding dataserver event to determine if this command succeeded or failed.

## Caveats

- If you recompile a script that was previously associated with an Experience but do so with a client that lacks the ability to compile scripts into an experience the script will lose the associated Experience.
- It is recommended that keys do not contain commas due to this function returning keys in CSV format.

## Examples

```lsl
key trans;
default
{
    state_entry()
    {
        // retrieve the first 10 keys
        trans = llKeysKeyValue(0, 10);
    }

    dataserver(key t, string value)
    {
        if (t == trans)
        {
            // our llKeysKeyValue transaction is done
            list result = llCSV2List(value);
            if (llList2Integer(result, 0) == 1)
            {
                llSay(0, "Keys retrieved: "+(string)llGetSubString(value, 2, -1));
            }
            else if (llList2Integer(result, 1) == XP_ERROR_KEY_NOT_FOUND)
            {
                // no more keys
                llSay(0, "No more keys" );
            }
            else
            {
                // keys request failed
                llSay(0, "Key-value failed to request keys: " + llGetExperienceErrorMessage(llList2Integer(result, 1)) );
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
