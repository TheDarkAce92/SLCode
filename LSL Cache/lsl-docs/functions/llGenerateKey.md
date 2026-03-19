---
name: "llGenerateKey"
category: "function"
type: "function"
language: "LSL"
description: 'Generates a key using Version 5 (SHA-1 hash) UUID generation to create a unique key.

Returns the key generated.'
signature: "key llGenerateKey()"
return_type: "key"
sleep_time: ""
energy_cost: ""
wiki_url: 'https://wiki.secondlife.com/wiki/llGenerateKey'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgeneratekey"]
---

Generates a key using Version 5 (SHA-1 hash) UUID generation to create a unique key.

Returns the key generated.


## Signature

```lsl
key llGenerateKey();
```


## Return Value

Returns `key`.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGenerateKey)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGenerateKey) — scraped 2026-03-18_

Generates a key using Version 5 (SHA-1 hash) UUID generation to create a unique key.Returns the key generated.

## Caveats

- The specific UUID version is an implementation detail that has changed in the past and may change again in the future. Do not depend upon the UUID that is returned to be Version 5.
- As the UUID produced is versioned, it should never return a value of NULL_KEY.

## Examples

```lsl
default
{
    touch_start(integer num_detected)
    {
        // avatar touching
        key avatarKey = llDetectedKey(0);
        string avatarName = llKey2Name(avatarKey);

        // key of the owner
        key owner = llGetOwner();

        // generated random key
        key random = llGenerateKey();

        // number of objects inside the same prim
        integer numberOfObjects = llGetInventoryNumber(INVENTORY_OBJECT);

        if (numberOfObjects)
        {
            // name of first object sorted by name inside the prim's inventory
            string itemName = llGetInventoryName(INVENTORY_OBJECT, 0);

            llGiveInventory(avatarKey, itemName);
            llInstantMessage(avatarKey, "Your transaction key is '" + (string)random + "'.");

            llInstantMessage(owner, "Transaction record:\n"
                + "receiver: " + avatarName + " (" + (string)avatarKey + ")\n"
                + "item: " + itemName + "\n"
                + "transaction key: " + (string)random);
        }
        else
        {
            // PUBLIC_CHANNEL has the integer value 0
            llSay(PUBLIC_CHANNEL, "No items to give away, sorry!");
        }
    }
}
```

<!-- /wiki-source -->
