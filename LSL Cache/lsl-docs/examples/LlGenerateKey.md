---
name: "LlGenerateKey"
category: "example"
type: "example"
language: "LSL"
description: "Generates a key using Version 5 (SHA-1 hash) UUID generation to create a unique key.Returns the key generated."
wiki_url: "https://wiki.secondlife.com/wiki/LlGenerateKey"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL


GenerateKeyllGenerateKey

- 1 Summary
- 2 Caveats
- 3 Examples
- 4 Deep Notes

  - 4.1 History
  - 4.2 Signature

## Summary

 Function: key **llGenerateKey**(  );

Forced Delay

Energy

Generates a key using [Version 5 (SHA-1 hash)](http://en.wikipedia.org/wiki/UUID#Version_5_.28SHA-1_hash.29) UUID generation to create a unique key.Returns the key generated.

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

## Deep Notes

#### History

- Inspired by the library function generateKey.
- Changed from using [Version 3 (MD5 hash)](http://en.wikipedia.org/wiki/UUID#Version_3_.28MD5_hash.29) to [Version 5 (SHA-1 hash)](http://en.wikipedia.org/wiki/UUID#Version_5_.28SHA-1_hash.29). Date of this change is unknown.

#### Signature

```lsl
function key llGenerateKey();
```