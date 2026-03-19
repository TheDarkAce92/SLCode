---
name: "llSetTouchText"
category: "function"
type: "function"
language: "LSL"
description: 'Displays text rather than the default 'Touch' in the right-click menu

This is very similar to LlSetSitText.
To restore the default value, use an empty string for text.
To make it appear as if there is no text, use some combination of whitespace characters for text.'
signature: "void llSetTouchText(string text)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetTouchText'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsettouchtext"]
---

Displays text rather than the default "Touch" in the right-click menu

This is very similar to LlSetSitText.
To restore the default value, use an empty string for text.
To make it appear as if there is no text, use some combination of whitespace characters for text.


## Signature

```lsl
void llSetTouchText(string text);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `text` |  |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetTouchText)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetTouchText) — scraped 2026-03-18_

Displays text rather than the default "Touch" in the right-click menu

## Caveats

- **text** will only be displayed if set by a script calling this function in the root. If **text** is set by a script in a child the **text** will only be displayed after unlinking it or relinking it as the root. If either a child or the root is selected as an individual prim and right clicked, the **text** displayed will be the default even if a script in the root has set **text**. More simply - The **text** property displayed on right click will always be that of the root unless, right clicking a prim under individual edit when it will always be the LL default.
- Note that like particles, and the other set text functions, all **text** set via llSetTouchText becomes a property of a prim, not a script. For that reason, the **text** will remain if the script that set it is deactivated or even removed.
- You have no control over the face, size or colour of the displayed **text**.
- **text** is limited to 9 characters.

## Examples

```lsl
default
{
    state_entry()
    {
        llSetTouchText("Touch me!");
    }
    touch_start(integer detected)
    {
        llSay(0, "you touched me!");
    }
}
```

## See Also

### Functions

- llSetSitText

### Articles

- Touch

<!-- /wiki-source -->
