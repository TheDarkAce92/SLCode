---
name: "llDetectedType"
category: "function"
type: "function"
language: "LSL"
description: 'Returns an integer mask that is the types of detected object or avatar.

number does not support negative indexes.
Returns zero if number is not valid sensed object or avatar.'
signature: "integer llDetectedType(integer number)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llDetectedType'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lldetectedtype"]
---

Returns an integer mask that is the types of detected object or avatar.

number does not support negative indexes.
Returns zero if number is not valid sensed object or avatar.


## Signature

```lsl
integer llDetectedType(integer number);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `number` | Index of detection information |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llDetectedType)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llDetectedType) — scraped 2026-03-18_

Returns a bit field (an integer) that is the types of the detected object or avatar.

## Caveats

- If number is out of bounds this function returns zero and the script continues to execute without an error message.
- Events that enable the llDetected* functions always return at least one detected item.

  - Detection events are not raised if there is nothing detected.
  - The detection event's items detected parameter is initially never less than 1.

## Examples

```lsl
//--// Type & name of collision source //--//

default{
    collision_start( integer vIntCollided ){
        integer vBitType;
        string vStrType;
        do
        {
            vBitType = llDetectedType( --vIntCollided );
            if (vBitType & AGENT_BY_LEGACY_NAME)
                vStrType = "avatar";
            else
                vStrType = "object";
            llOwnerSay( "An " + vStrType + " named '" + llDetectedName( vIntCollided ) + "' collided with me" );
        }
        while (vIntCollided);
    }
}
```

## See Also

### Articles

- Detected

<!-- /wiki-source -->
