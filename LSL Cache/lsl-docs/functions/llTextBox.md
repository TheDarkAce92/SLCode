---
name: "llTextBox"
category: "function"
type: "function"
language: "LSL"
description: "Shows a dialog box on avatar's screen with the text message. It contains a text box for input, any text that is entered is said by avatar on channel when the 'Submit' button is clicked."
signature: "void llTextBox(key avatar, string message, integer chat_channel)"
return_type: "void"
sleep_time: "1.0"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llTextBox'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lltextbox"]
---

Shows a dialog box on avatar's screen with the text message. It contains a text box for input, any text that is entered is said by avatar on channel when the "Submit" button is clicked.


## Signature

```lsl
void llTextBox(key avatar, string message, integer chat_channel);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `avatar` | avatar UUID that is in the same region |
| `string` | `message` | message to be displayed in the text box |
| `integer` | `channel` | output chat channel, any integer value |


## Caveats

- Forced delay: **1.0 seconds** — the script sleeps after each call.
- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llTextBox)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llTextBox) — scraped 2026-03-18_

Shows a dialog box on avatar's screen with the text message. It contains a text box for input, any text that is entered is said by avatar on channel when the "Submit" button is clicked.

## Caveats

- This function causes the script to sleep for 1.0 seconds.
- Not supported in official Linden Lab viewers prior to version 2.4, and some TPVs may not support it. Unsupported viewers will display a dialog box with a single option of "!!llTextBox!!".
- There is no way by script to kill a text box.
- There is no way for the script to detect if the user clicked the small "ignore" button (no chat is generated as a result of pressing this button).
- If the listening prim is out of the 20 meter range of the sending prim when the "Submit" button is pressed, it will not be able to hear the response.

  - This limitation affects attachments too if the wearer moves more than 20 meters from where the listener is located.
- The textbox input is limited to 250 bytes (characters). This can be a problem for larger text input; if the input can be over 250 characters, you will have to accept it through chat.
- There is an undocumented throttle on llTextBox requests. Exceeding it will shout an error on DEBUG_CHANNEL until the "average" falls.

### message limits

- If it exceeds 7 (Viewer 3) or 8 (Viewer 1) lines a scroll bar will appear.
- message must be less than 512 bytes and not empty. Otherwise, it will shout an error on DEBUG_CHANNEL. One easy way to create an empty message is to use a line feed, as in

```lsl
llTextBox(avatar_key," \n",dialog_channel);
```

## Examples

```lsl
integer  gListener;
default
{
    touch_start(integer total_number)
    {
        // See 'discussion' page for more comments on choosing a channel and possible left-open listener
        integer channel = -13572468;
        // "" saves byte-code over NULL_KEY
        gListener = llListen( channel, "", "", "");
        llTextBox(llDetectedKey(0), "Some info text for the top of the window...", channel);
    }
    listen(integer channel, string name, key id, string message)
    {
        llListenRemove(gListener);
        llSay(0, "You wrote: " + message);
    }
}
```

If the user hits Enter ↵ before clicking the `"Submit"` button, there will be a final carriage return in the message. In the rare event that this could be a problem, it is easily removed:

```lsl
        message = llStringTrim(message,STRING_TRIM);
```

## Notes

Instead of mouse clicking: "Submit", you can use keyboard keys: press Tab ⇆ and then Enter ↵

## See Also

### Events

- listen

### Functions

- llDialog
- llListen
- llSay
- llWhisper
- llShout
- llRegionSay

<!-- /wiki-source -->
