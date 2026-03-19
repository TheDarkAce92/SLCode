---
name: "UUID2Channel"
category: "example"
type: "example"
language: "LSL"
description: "Varying functions to convert a Key (UUID) to an Integer, for use as a LSL Chat Channel."
wiki_url: "https://wiki.secondlife.com/wiki/UUID2Channel"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 Description
- 2 Method 1 - Simple

  - 2.1 Improvement - App Key
- 3 Method 2 - Defined Base/Range

## Description

Varying functions to convert a Key (UUID) to an Integer, for use as a LSL Chat Channel.

## Method 1 - Simple

Well, I've figured out a more effective way of using the UUID2Channel method, you know.
The one where you put a hexadecimal prefix in front of a person's UUID. Always generates
negative integers, for safety.

```lsl
// Project Neox was here.
// Web Gearbox was here too

integer Key2Chan(key ID) {
    return 0x80000000 | (integer)("0x"+(string)ID);
}
```

#### Improvement - App Key

This generates a unique channel ID from the input key, but also XOR's it with another value, this value should be application specific.

I encountered an issue where one of the commonly used combat meters (Gorean Meter I think) is using the exact function above to generate its personal channel numbers, and starts complaining - loudly (shouts) - if you put other data on the same channel (user is flooding their own channels!).

As such you shouldn't really use the above function directly for channel IDs, if everyone did, it would negate the entire point of the function, the version below allows you to supply a random constant number to push the allocations around so we're not going to see same-user collisions between applications.

```lsl
// modified channel generator to include per-application key, preventing cross-application collisions
// - Iain Maltz

integer Key2AppChan(key ID, integer App) {
    return 0x80000000 | ((integer)("0x"+(string)ID) ^ App);
}
```

## Method 2 - Defined Base/Range

```lsl
// # Base/Range-Method Channel Generator.
// > Allows for limiting the channel-band spread to only the amount needed for the application.
// - Faust Vollmar

integer uiKey2Range(key vkID, integer viBase, integer viRange)
{// # Result will be added or subtracted dependent on viBase being positive or negative, for intuitive results.
 // > Example: -56000/1000 will result in -56000 to -56999, whereas 56000/1000 will result in 56000 to 56999
    integer viMult = 1;
    if( viBase < 0 ) { viMult = -1; }
    return (viBase+(viMult*(((integer)("0x"+(string)vkID)&0x7FFFFFFF)%viRange)));
}
```