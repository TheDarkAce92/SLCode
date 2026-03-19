---
name: "llSetSitText"
category: "function"
type: "function"
language: "LSL"
description: "Displays text rather than the default 'Sit Here' in the right-click menu."
signature: "void llSetSitText(string text)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetSitText'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsetsittext"]
---

Displays text rather than the default "Sit Here" in the right-click menu.


## Signature

```lsl
void llSetSitText(string text);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `text` |  |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetSitText)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetSitText) — scraped 2026-03-18_

Displays text rather than the default "Sit Here" in the right-click menu.

## Caveats

- **Text** will only be displayed if set by a script calling this function in the root. If **text** is set by a script in a child the **text** will only be displayed after unlinking it or relinking it as the root. If either a child or the root is selected as an individual prim and right clicked, the **text** displayed will be the default even if a script in the root has set **text**. More simply - The **text** property displayed on right click will always be that of the root unless, right clicking a prim under individual edit when it will always be the LL default.
- Note that like particles, and the other set text functions, all **text** set via llSetSitText becomes a property of a  prim, not a script. For that reason, the **text** will remain if the script that set it is deactivated or even removed.
- You have no control over the face, size or colour of the displayed **text**.
- **Text** is limited to 9 characters.

## Examples

### Usage

```lsl
default
{
    state_entry()
    {
        llSetSitText("Be Seated");
    }
}
```

### Removing Sit Text

There is no way to stop a pie menu from having a "Sit Here" space reserved on it. Although by setting the string to a space no text will be shown.

To remove custom text that you have placed there, set the text as an empty string like this: "".

```lsl
default
{
    state_entry()
    {
        llSetSitText("");
    }
}
```

Upon your having done so, the text that appears will revert to "Sit Here."

## See Also

### Functions

- llSitTarget
- llSetTouchText

<!-- /wiki-source -->
