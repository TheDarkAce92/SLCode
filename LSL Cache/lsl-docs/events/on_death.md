---
name: "on_death"
category: "event"
type: "event"
language: "LSL"
description: "This event is triggered on all attachments worn by an avatar when that avatar's health reaches 0."
signature: "on_death()"
wiki_url: 'https://wiki.secondlife.com/wiki/on_death'
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
deprecated: "false"
parameters: []
---

This event is triggered on all attachments worn by an avatar when that avatar's health reaches 0.


## Signature

```lsl
on_death()
{
    // your code here
}
```


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/on_death)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/on_death) — scraped 2026-03-18_

## Examples

```lsl
default
{
    on_death()
    {
        llSay(0, "Faster, faster, Bambi! Don't look back! Keep running! KEEP RUNNING!");
    }
}
```

## See Also

### Events

- on_damage
- final_damage

### Functions

- llDetectedDamage
- llAdjustDamage
- llDamage

<!-- /wiki-source -->
