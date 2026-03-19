---
name: "llUpdateKeyValue"
category: "function"
type: "function"
language: "LSL"
description: 'Start an asynchronous transaction to update a key-value pair associated with the script's Experience with the given key (k) and value (v).

Returns a handle (a key) that can be used to identify the corresponding dataserver event to determine if this command succeeded or failed and the results.

If c'
signature: "key llUpdateKeyValue(string k, string v, integer checked, string original_value)"
return_type: "key"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llUpdateKeyValue'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
flags: "experience-api"
patterns: ["llupdatekeyvalue"]
---

Start an asynchronous transaction to update a key-value pair associated with the script's Experience with the given key (k) and value (v).

Returns a handle (a key) that can be used to identify the corresponding dataserver event to determine if this command succeeded or failed and the results.

If checked is set to TRUE then the update will only happen if original_value matches the current value in key-value store, otherwise the dataserver will return a failure along with the error XP_ERROR_RETRY_UPDATE. This can be used to create an in-use flag so that Atomicity can be achieved.

As of Jan 1, 2016 maximum bytes is 1011 for key and 4095 for value for both LSO and Mono scripts.
Using llUpdateKeyValue to update a key that does not exist will not generate XP_ERROR_KEY_NOT_FOUND. Instead, it will generate a new key with the specified value, as if you had used llCreateKeyValue.

For this function to work, the script must be compiled into an Experience.


## Signature

```lsl
key llUpdateKeyValue(string k, string v, integer checked, string original_value);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `k` | The key for the key-value pair |
| `string` | `v` | The value for the key-value pair.  Maximum 2047 characters, or 4095 if using Mono. |
| `integer (boolean)` | `checked` | If TRUE the update will only happen if original_value matches the value in the key-value store. |
| `string` | `original_value` | The value to compare with the current value in the key-value store. |


## Return Value

Returns `key`.


## Caveats

- Energy cost: **10.0**.
- Requires an active **Experience** (Experience API function).


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llUpdateKeyValue)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llUpdateKeyValue) — scraped 2026-03-18_

Start an asynchronous transaction to update a key-value pair associated with the script's Experience with the given key (k) and value (v).Returns a handle (a key) that can be used to identify the corresponding dataserver event to determine if this command succeeded or failed and the results.

## Caveats

- If you recompile a script that was previously associated with an Experience but do so with a client that lacks the ability to compile scripts into an experience the script will lose the associated Experience.
- It is recommended that keys do not contain commas due to llKeysKeyValue returning keys in CSV format.

## Examples

```lsl
key trans;
default
{
    state_entry()
    {
        trans = llUpdateKeyValue("FOO", "BLAH", TRUE, "BAR");
    }

    dataserver(key t, string value)
    {
        if (t == trans)
        {
            // our llUpdateKeyValue transaction is done
            list result = llCSV2List(value);
            if (llList2Integer(result, 0) == 1)
            {
                // the key-value pair was successfully updated
                llSay(0, "New key-value pair was successfully updated");
            }
            else
            {
                integer error = llList2Integer(result, 1);
                if(error == XP_ERROR_RETRY_UPDATE)
                    llSay(0, "Key-value update failed, checked value is out of date");
                else
                    llSay(0, "Key-value update failed: " + llGetExperienceErrorMessage(error) );
            }
        }
    }
}
```

This script demonstrates how to avoid update conflicts (two scripts updating the store at the same time), performing fully atomic updates is more complicated. If all scripts writing to the key-value store abide by the virtual lock ($DB_Lock), and only do updates in update_db state, then all writes will be atomic.

```lsl
key tid;
list tids;

default {
    state_entry() {
        state lock_db;
    }
}

state lock_db {
    state_entry() {
        tid = llUpdateKeyValue("$DB_Lock", "LOCK", TRUE, "unlock");
    }
    dataserver(key did, string value) {
        if(did == tid) {
            string payload = llDeleteSubString(value, 0, 1);
            if(llGetSubString(value+",", 0, 1) == "1,"){
                llUpdateKeyValue("$DB_LockedBy", llDumpList2String([llGetOwner(),llGetKey(),llGetLinkKey(!!llGetLinkNumber()),llGetRegionName(),llGetPos(),llGetAttached()],":"), FALSE, "");
                state update_db;
            } else {
                integer err = (integer)payload;
                if(err == XP_ERROR_RETRY_UPDATE) {
                    llSay(0, "Database is already locked!");
                } else {
                    llSay(0, "Key-value update failed: " + llGetExperienceErrorMessage(err) );
                }
                state error;
            }
        }
    }
}

state update_db {
    state_entry() {
        tids = [
            llUpdateKeyValue("CatsPermissable", "5", FALSE, ""),
            llUpdateKeyValue("MonkeyMutations", "3", FALSE, ""),
            llUpdateKeyValue("CodFlavorSupport", "NEVER", FALSE, "")
        ];
    }
    dataserver(key did, string value) {
        integer i = llListFindList(tid, [did]);
        if(~i) {
            string payload = llDeleteSubString(value, 0, 1);
            if(llGetSubString(value+",", 0, 1) == "1,"){
                tids = llDeleteSubList(tids, i, i);
                if(tids == []) {
                    state unlock_db;
                }
            } else {
                llSay(0, "Key-value update failed: " + llGetExperienceErrorMessage((integer)payload) );
                state error;
            }
        }
    }
}

state unlock_db {
    state_entry() {
        tid = llUpdateKeyValue("$DB_Lock", "unlock", TRUE, "LOCK");
    }
    dataserver(key did, string value) {
        if(did == tid) {
            string payload = llDeleteSubString(value, 0, 1);
            if(llGetSubString(value+",", 0, 1) == "1,"){
                state done;
            } else {
                integer err = (integer)payload;
                if(err == XP_ERROR_RETRY_UPDATE) {
                    llSay(0, "Someone has violated the database lock!");
                } else {
                    llSay(0, "Key-value update failed: " + llGetExperienceErrorMessage(err) );
                }
                state error;
            }
        }
    }
}

state done {
    state_entry(){;}
}

state error {
    state_entry(){;}
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
