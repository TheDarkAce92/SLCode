---
name: "game_control"
category: "event"
type: "event"
language: "LSL"
description: "Experimental event only available in some testing regions (soon).  Triggered when compatible viewer sends fresh GameControlInput message, but only for scripts on attachments or seat."
signature: "game_control(key id, integer button_levels, list axes)"
wiki_url: 'https://wiki.secondlife.com/wiki/game_control'
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
deprecated: "false"
parameters: []
---

Experimental event only available in some testing regions (soon).  Triggered when compatible viewer sends fresh GameControlInput message, but only for scripts on attachments or seat.


## Signature

```lsl
game_control(key id, integer button_levels, list axes)
{
    // your code here
}
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `id` | avatar UUID |
| `integer` | `button_levels` | bitfield of buttons held down |
| `list` | `axes` | list of axes float values in range [-1, 1] |


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/game_control)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/game_control) — scraped 2026-03-18_

## Caveats

- If enabled at the client: avatar movements may be translated into GameControl input.
- There is room for 32 buttons [bits 0 through 31] however at most only 16 buttons can be simultaneously held down at any one time.
- There are always 6 **axes** values, even when the controller device has more or less

  - All **axes** elements will be in range [-1,1]
  - By default,

  - Left-tilting a thumbstick on **GAME_CONTROL_AXIS_LEFTX** or **GAME_CONTROL_AXIS_RIGHTX** yields a positive value, while right-tilting yields a negative value
  - Up-tilting a thumbstick on **GAME_CONTROL_AXIS_LEFTY** or **GAME_CONTROL_AXIS_RIGHTY** yields a positive value, while down-tilting yields a negative value
  - Pulling a trigger will increase the value of **GAME_CONTROL_AXIS_TRIGGERLEFT** or **GAME_CONTROL_AXIS_TRIGGERRIGHT**, while releasing will decrease the value

## Examples

```lsl
integer prev_button_levels = 0;
integer print_list(string name, integer type, list data)
{
    integer data_length = llGetListLength(data);
    string text = name + " : ";
    if (data_length > 0)
    {
        integer use_comma = FALSE;
        integer i = 0;
        for (i = 0; i < data_length; i++)
        {
            if (!use_comma)
            {
                use_comma = TRUE;
            }
            else
            {
                text += ",";
            }
            if (type == TYPE_INTEGER)
            {
                integer b = (llList2Integer(data, i));
                text += (string)(b);
                llOwnerSay("pack i=" + (string)(i) + " b=" + (string)(b));
            }
            else if (type == TYPE_FLOAT)
            {
                text += (string)(llList2Float(data, i));
            }
        }
    }
    llOwnerSay(text);
    return data_length;
}

string bits2nybbles(integer bits)
{
    integer lsn; // least significant nybble
    string nybbles = "";
    do
        nybbles = llGetSubString("0123456789ABCDEF", lsn = (bits & 0xF), lsn) + nybbles;
    while (bits = (0xfffFFFF & (bits >> 4)));
    return nybbles;
}

default
{
    state_entry()
    {
        llOwnerSay("Ready for game_control events");
    }

    game_control(key id, integer button_levels, list axes)
    {
        integer button_edges = button_levels ^ prev_button_levels;
        prev_button_levels = button_levels;

        string button_levels_hex = bits2nybbles(button_levels);
        string button_edges_hex = bits2nybbles(button_edges);
        llOwnerSay("game_control :");
        llOwnerSay("  button_levels=0x" + button_levels_hex);
        llOwnerSay("  button_edges=0x" + button_edges_hex);
        print_list("  axes", TYPE_FLOAT, axes);
    }
}
```

## See Also

### Events

- control

### Articles

LSL Game Control Beta

<!-- /wiki-source -->
