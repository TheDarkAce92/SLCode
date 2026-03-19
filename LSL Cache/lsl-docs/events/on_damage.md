---
name: "on_damage"
category: "event"
type: "event"
language: "LSL"
description: "{{LSL Warnings/Combat2}}This event is triggered when damage has been inflicted on an avatar or task in the world but before damage has been applied or distributed.All llDetected* functions that are normally available within a collision event are available while processing this event. Additionally th"
signature: "on_damage(integer num_detected)"
wiki_url: 'https://wiki.secondlife.com/wiki/on_damage'
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
deprecated: "false"
parameters: []
---

{{LSL Warnings/Combat2}}This event is triggered when damage has been inflicted on an avatar or task in the world but before damage has been applied or distributed.All llDetected* functions that are normally available within a collision event are available while processing this event. Additionally the llDetectedDamage and llAdjustDamage methods may be called while processing this event.


## Signature

```lsl
on_damage(integer num_detected)
{
    // your code here
}
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `num_detected` | The number of damage events pending against the avatar or task. |


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/on_damage)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/on_damage) — scraped 2026-03-18_

## Caveats

- Requires the region to allow damage adjustment for the event to run

## Examples

```lsl
string damageType2String(integer type)
{
    if (type == DAMAGE_TYPE_GENERIC)
        return "generic";
    else if (type == DAMAGE_TYPE_ACID)
        return "acid";
    else if (type == DAMAGE_TYPE_BLUDGEONING)
        return "bludgeoning";
    else if (type == DAMAGE_TYPE_COLD)
        return "cold";
    else if (type == DAMAGE_TYPE_ELECTRIC)
        return "electric";
    else if (type == DAMAGE_TYPE_FIRE)
        return "fire";
    else if (type == DAMAGE_TYPE_FORCE)
        return "force";
    else if (type == DAMAGE_TYPE_NECROTIC)
        return "necrotic";
    else if (type == DAMAGE_TYPE_PIERCING)
        return "piercing";
    else if (type == DAMAGE_TYPE_POISON)
        return "poison";
    else if (type == DAMAGE_TYPE_PSYCHIC)
        return "psychic";
    else if (type == DAMAGE_TYPE_RADIANT)
        return "radiant";
    else if (type == DAMAGE_TYPE_SLASHING)
        return "slashing";
    else if (type == DAMAGE_TYPE_SONIC)
        return "sonic";
    else if (type == DAMAGE_TYPE_EMOTIONAL)
        return "emotional";

    return "type " + (string)type;
}

default
{
    on_death()
    {
        llSay(0, "I'll be back!");
    }

    on_damage(integer count)
    {
        integer index;
        for (index = 0; index < count; ++index)
        {
            key object = llDetectedKey(index);
            string object_name = llDetectedName(index);
            key owner = llDetectedOwner(index);
            key rezzer = llDetectedRezzer(index);
            list damage = llDetectedDamage(index);

            string owner_name = llKey2Name(owner);
            string rezzer_name = llKey2Name(rezzer);

            llSay(0, "I was struck by " + object_name + "{" + (string)object + "} owned by " +
                owner_name + "{" + (string)owner + "} rezzed by " +
                rezzer_name + "{" + (string)rezzer + "} for " +
                (string)llList2Float(damage, 0) + " points of " + damageType2String(llList2Integer(damage, 1)) +
                " damage (originally " + (string)llList2Float(damage, 2));

            float new_damage = llList2Float(damage, 0) / 2.0;

            llSay(0, "Reducing damage by 50% to " + (string)new_damage);
            llAdjustDamage(index, new_damage);
            llSay(0, "llDetectDamage = [" + llDumpList2String(llDetectedDamage(index), ", ") + "]");
        }

    }
}
```

## See Also

### Events

- on_death
- final_damage

### Functions

- llDetectedDamage
- llAdjustDamage
- llDamage

<!-- /wiki-source -->
