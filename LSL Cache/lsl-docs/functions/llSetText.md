---
name: "llSetText"
category: "function"
type: "function"
language: "LSL"
description: "Displays hovering text above a prim with specified colour and opacity"
wiki_url: "https://wiki.secondlife.com/wiki/llSetText"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "void llSetText(string text, vector color, float alpha)"
parameters:
  - name: "text"
    type: "string"
    description: "Text to display (max 254 bytes UTF-8). Pass empty string to remove text."
  - name: "color"
    type: "vector"
    description: "RGB colour as <r, g, b> with each component 0.0–1.0"
  - name: "alpha"
    type: "float"
    description: "Opacity: 0.0 = transparent, 1.0 = fully opaque"
return_type: "void"
energy_cost: "10.0"
sleep_time: "0.0"
patterns: ["llsettext"]
deprecated: "false"
---

# llSetText

```lsl
void llSetText(string text, vector color, float alpha)
```

Displays hovering text above the prim's centre. Text is visible through walls and other objects.

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `text` | string | Text to display (max 254 bytes UTF-8) |
| `color` | vector | `<red, green, blue>` each 0.0–1.0 |
| `alpha` | float | 0.0 (transparent) to 1.0 (opaque) |

## Caveats

- Maximum 254 bytes in UTF-8 encoding (may be fewer characters for multibyte text).
- **Removing the script or deactivating it does not remove the text.** Use `llSetText("", ZERO_VECTOR, 0)` to clear.
- Text is visible through walls and other geometry.
- Trailing vertical whitespace is stripped.
- Multiple consecutive blank lines are collapsed to a single line break.
- Height scales proportionally with the prim's Z dimension.

## Examples

```lsl
// Set green label
vector COLOR_GREEN = <0.0, 1.0, 0.0>;
llSetText(llGetObjectName(), COLOR_GREEN, 1.0);

// Remove text
llSetText("", ZERO_VECTOR, 0.0);

// Multi-line
llSetText("Line one\nLine two", <1.0, 1.0, 1.0>, 1.0);

// Colour reference
// White:  <1.0, 1.0, 1.0>
// Black:  <0.0, 0.0, 0.0>
// Red:    <1.0, 0.0, 0.0>
// Green:  <0.0, 1.0, 0.0>
// Blue:   <0.0, 0.0, 1.0>
// Yellow: <1.0, 1.0, 0.0>
```

## See Also

- `llSetPrimitiveParams` with `PRIM_TEXT` — equivalent via params list
- `llGetObjectName` — get object name for labelling


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetText) — scraped 2026-03-18_

Displays text that hovers over the prim with specific color and translucency (specified with alpha).

## Caveats

- Do not rely on Floating Text as a storage medium; it is neither secure nor finalized.

  - Floating text has been altered in past server updates, breaking existing content; future changes may occur.
  - Even "invisible" floating text is transmitted to the client.

  - It can be viewed by anyone with a client that is capable of rendering text that is supposed to be invisible.
  - The network packets that contain the text can be sniffed and the text read.
- If more than one llSetText is called (By reset,interaction or script state) within a prim the latest call will take priority over the previous.
- text is limited to 254 bytes (compare Limits#Building) in UTF-8 encoding. If the string is longer it will be truncated to 254 bytes, and any multibyte characters getting split will be removed entirely.
- An unbroken line of text of a great length may be broken automatically into two lines (one above the other).
- text can be seen through walls and other object. Be considerate of neighbors in malls and apartment buildings.

  - Visibility distance increases with prim size.
- Removing the script or deactivating it **will not remove** a prim's text property. Floating text is not dependent on a script for its continued existence but only when wanting to change it.
- To remove a prim's text, use the following:

| Preferred method to remove a prim's floating text | Second method does the same effect-wise. |
| --- | --- |
| ```lsl // empty string & black & transparent llSetText("", ZERO_VECTOR, 0); ``` | ```lsl // empty string & black & transparent llSetText("", , 0.0); ``` |

- Vertical whitespace is removed from the end of the text string, so if you want vertical whitespace put any character (like a space) on the last line.
- Multiple linebreaks with empty lines are converted to a single linebreak, so add a whitespace character on every line you want to skip:

| Good | Bad |
| --- | --- |
| ```lsl vector COLOR_WHITE = ; float OPAQUE = 1.0; llSetText("Monkeys\n \n \n \n \n ", COLOR_WHITE, OPAQUE); ``` | ```lsl vector COLOR_WHITE = ; float OPAQUE = 1.0; llSetText("Monkeys\n\n\n\n\n", COLOR_WHITE, OPAQUE); ``` |

- **Measurements showed a high impact of process time when doing numerous iterations in a while loop**. For approx. 65 thousand iterations the process times are ca. 5 seconds without floating text, 24 seconds with llSetText and 96 seconds when using llSetPrimitiveParams#llSetLinkPrimitiveParamsFast in combination with PRIM_TEXT. Thats why you are **not advised** to make excessive use of changing a prim's text within such iterations.

## Examples

Example of how llSetText could be used to show prim's name in green text:

```lsl
default
{
    state_entry()
    {
        vector COLOR_GREEN = <0.0, 1.0, 0.0>;
        float  OPAQUE      = 1.0;

//      prim's name (not necessarily object's)
        llSetText(llGetObjectName(), COLOR_GREEN, OPAQUE );

//      delete the script as we only needed it to change the floating text property
        llRemoveInventory(llGetScriptName());
    }
}
```

By default the floating text will appear on a single line. However, it can be spread over multiple lines by using a line break `"\n"` (read SplitLine in section 'See Also').

### String escape codes:

LSL has four string escape codes:

- `\n` for a new line
- `\\` for a backslash
- `\t` for a tab
- `\"` for a double-quote

### Color & Alpha

| Color | Code |
| --- | --- |
| NAVY | `<0.000, 0.122, 0.247>` |
| BLUE | `<0.000, 0.455, 0.851>` |
| AQUA | `<0.498, 0.859, 1.000>` |
| TEAL | `<0.224, 0.800, 0.800>` |
| OLIVE | `<0.239, 0.600, 0.439>` |
| GREEN | `<0.180, 0.800, 0.251>` |
| LIME | `<0.004, 1.000, 0.439>` |
| YELLOW | `<1.000, 0.863, 0.000>` |
| ORANGE | `<1.000, 0.522, 0.106>` |
| RED | `<1.000, 0.255, 0.212>` |
| MAROON | `<0.522, 0.078, 0.294>` |
| FUCHSIA | `<0.941, 0.071, 0.745>` |
| PURPLE | `<0.694, 0.051, 0.788>` |
| WHITE | `<1.000, 1.000, 1.000>` |
| SILVER | `<0.867, 0.867, 0.867>` |
| GRAY | `<0.667, 0.667, 0.667>` |
| BLACK | `<0.000, 0.000, 0.000>` |

The x, y & z components of the vector are used to represent red, green, and blue respectively. The range is different from traditional RGB, instead of being 0 -> 255, LSL uses 0 -> 1. `<1.0, 1.0, 1.0>` represents "white" and `<0.0, 0.0, 0.0>` represents "black":

```lsl
//  white & opaque
    llSetText("I am white", <1.0, 1.0, 1.0>, 1.0);
```

```lsl
    vector myColor;// defaults to ZERO_VECTOR or <0.0, 0.0, 0.0> which is black

    llSetText("I am black and 30% transparent.", myColor, 0.7);

    llSleep(7.5);   // before: <0.0, 0.0, 0.0> black
    myColor.x = 1.0;// now:    <1.0, 0.0, 0.0> red

    llSetText("I am now red and 10% transparent.", myColor, 0.9);
```

If alpha is 1.0 it means the text is fully opaque (alpha), 0.0 would make it completely transparent (invisible):

```lsl
    llSetText("green text with alpha 0.7", <0.0, 1.0, 0.0>, 0.7);

    llSetText("white text with alpha 0.4\n60% transparent", <1.0, 1.0, 1.0>, 0.4);
    llSetText("white text with alpha 1.0\nfully opaque", <1.0, 1.0, 1.0>, 1.0);

//  next to lines have the same effect
    llSetText("invisible black text with alpha 0.0\nfully transparent", ZERO_VECTOR, 0);
    llSetText("invisible black text with alpha 0.0\nfully transparent", <0.0, 0.0, 0.0>, 0.0);
```

### Multiple lines

```lsl
//  two lines of orange text

    llSetText("I am\non two lines!", <1.0, 0.4, 0.0>, 1.0);
```

## Notes

To actually display text on a prim, see XyzzyText, or consider using parcel prim Media options (useful only if you have control over the land's media settings.)

The function displays text that hover over the prim's center, the prim position. The height over the center is proportional to the prim's Z-dimension exclusively

- It doesn't matter how the prim is rotated, so if Z is smaller than X and Y the text may be seen on the prim

## See Also

### Constants

- PRIM_TEXT

### Articles

- **Limits** — SL limits and constrictions
- Color in LSL
- Translucent Color
- **Examples** — Insert 'new line' escape codes at certain positions of a string
- **llGetObjectPermMask** — Label an object with text and newlines to give away or sell
- **escape codes** — for details on how and when they work

<!-- /wiki-source -->
