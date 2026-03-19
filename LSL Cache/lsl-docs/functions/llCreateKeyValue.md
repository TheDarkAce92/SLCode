---
name: "llCreateKeyValue"
category: "function"
type: "function"
language: "LSL"
description: 'Start an asynchronous transaction to create a key-value pair associated with the script's Experience using the given key (k) and value (v).

Returns a handle (a key) that can be used to identify the corresponding dataserver event to determine if this command succeeded or failed.

If the key already '
signature: "key llCreateKeyValue(string k, string v)"
return_type: "key"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llCreateKeyValue'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
flags: "experience-api"
patterns: ["llcreatekeyvalue"]
---

Start an asynchronous transaction to create a key-value pair associated with the script's Experience using the given key (k) and value (v).

Returns a handle (a key) that can be used to identify the corresponding dataserver event to determine if this command succeeded or failed.

If the key already exists the dataserver will return a failure along with the error XP_ERROR_STORAGE_EXCEPTION.

As of Jan 1, 2016 maximum bytes is 1011 for key and 4095 for value for both LSO and Mono scripts.

For this function to work, the script must be compiled into an Experience.


## Signature

```lsl
key llCreateKeyValue(string k, string v);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `k` | The key for the key-value pair |
| `string` | `v` | The value for the key-value pair. Maximum 2047 characters, or 4095 if using Mono. |


## Return Value

Returns `key`.


## Caveats

- Energy cost: **10.0**.
- Requires an active **Experience** (Experience API function).


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llCreateKeyValue)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llCreateKeyValue) — scraped 2026-03-18_

Start an asynchronous transaction to create a key-value pair associated with the script's Experience using the given key (k) and value (v).Returns a handle (a key) that can be used to identify the corresponding dataserver event to determine if this command succeeded or failed.

## Caveats

- If you recompile a script that was previously associated with an Experience but do so with a client that lacks the ability to compile scripts into an experience the script will lose the associated Experience.
- It is recommended that keys do not contain commas due to llKeysKeyValue returning keys in CSV format.

## Examples

```lsl
key trans;
default
{
    touch_start(integer total_number)
    {
        trans = llCreateKeyValue("FOO", "BAR");
    }

    dataserver(key t, string value)
    {
        if (t == trans)
        {
            // our llCreateKeyValue transaction is done
            integer result = (integer)llGetSubString(value, 0, 0);
            if (result == 1)
            {
                // the key-value pair was successfully created
                llSay(0, "New key-value pair was created");
            }
            else
            {
                // the key-value pair was not created
                integer error = (integer)(llGetSubString(value, 2, -1));
                llSay(0, "Key-value failed to create: " + llGetExperienceErrorMessage(error));
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
- llReadKeyValue
- llUpdateKeyValue
- llDeleteKeyValue
- llDataSizeKeyValue
- llKeyCountKeyValue
- llKeysKeyValue

<!-- /wiki-source -->
