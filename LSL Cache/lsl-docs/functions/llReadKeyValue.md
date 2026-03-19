---
name: "llReadKeyValue"
category: "function"
type: "function"
language: "LSL"
description: 'Start an asynchronous transaction to read the value associated with the specified key (k) and the script's Experience.

Returns a handle (a key) that can be used to identify the corresponding dataserver event to determine if this command succeeded or failed and the results.

If the key does not exis'
signature: "key llReadKeyValue(string k)"
return_type: "key"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llReadKeyValue'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
flags: "experience-api"
patterns: ["llreadkeyvalue"]
---

Start an asynchronous transaction to read the value associated with the specified key (k) and the script's Experience.

Returns a handle (a key) that can be used to identify the corresponding dataserver event to determine if this command succeeded or failed and the results.

If the key does not exist the dataserver will return a failure along with the error XP_ERROR_KEY_NOT_FOUND.

For this function to work, the script must be compiled into an Experience.


## Signature

```lsl
key llReadKeyValue(string k);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `k` | The key for the key-value pair |


## Return Value

Returns `key`.


## Caveats

- Energy cost: **10.0**.
- Requires an active **Experience** (Experience API function).


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llReadKeyValue)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llReadKeyValue) — scraped 2026-03-18_

Start an asynchronous transaction to read the value associated with the specified key (k) and the script's Experience.Returns a handle (a key) that can be used to identify the corresponding dataserver event to determine if this command succeeded or failed and the results.

## Caveats

- If you recompile a script that was previously associated with an Experience but do so with a client that lacks the ability to compile scripts into an experience the script will lose the associated Experience.

## Examples

```lsl
key trans;
default
{
    state_entry()
    {
        trans = llReadKeyValue("FOO");
    }
    dataserver(key t, string value)
    {
        if (t == trans)
        {
            // our llReadKeyValue transaction is done
            if (llGetSubString(value, 0, 0) == "1")
            {
                // the key-value pair was successfully read
                llSay(0, "New key-value pair value: " + llGetSubString(value, 2, -1));
            }
            else
            {
                // the key-value pair failed to read
                integer error =  (integer)llGetSubString(value, 2, -1);
                llSay(0, "Key-value failed to read: " + llGetExperienceErrorMessage(error));
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
