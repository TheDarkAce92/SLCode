---
name: "llReleaseControls"
category: "function"
type: "function"
language: "LSL"
description: "Stop taking inputs (that were taken with llTakeControls), dequeues any remaining control events. If PERMISSION_TAKE_CONTROLS was previously granted, it will be revoked."
signature: "void llReleaseControls()"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llReleaseControls'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llreleasecontrols"]
---

Stop taking inputs (that were taken with llTakeControls), dequeues any remaining control events. If PERMISSION_TAKE_CONTROLS was previously granted, it will be revoked.


## Signature

```lsl
void llReleaseControls();
```


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llReleaseControls)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llReleaseControls) — scraped 2026-03-18_

Stop taking inputs (that were taken with llTakeControls), dequeues any remaining control events. If PERMISSION_TAKE_CONTROLS was previously granted, it will be revoked.

## Caveats

- In some cases, calling llReleaseControls() in one script can affect the controls of other script which has also captured the same control bit on the same agent.

## See Also

### Events

- control

### Functions

- llTakeControls

<!-- /wiki-source -->
