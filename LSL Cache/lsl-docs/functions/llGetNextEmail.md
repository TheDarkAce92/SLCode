---
name: "llGetNextEmail"
category: "function"
type: "function"
language: "LSL"
description: 'Get the next queued email that comes from address, with specified subject.

If address or subject an empty string, then that parameter will be treated as a wildcard.'
signature: "void llGetNextEmail(string address, string subject)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetNextEmail'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetnextemail"]
---

Get the next queued email that comes from address, with specified subject.

If address or subject an empty string, then that parameter will be treated as a wildcard.


## Signature

```lsl
void llGetNextEmail(string address, string subject);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `address` | Sender's mail address |
| `string` | `subject` | Mail subject |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetNextEmail)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetNextEmail) — scraped 2026-03-18_

Get the next queued email that comes from address, with specified subject.

## Examples

```lsl
default
{
    state_entry()
    {
        llOwnerSay("My email address is: " + (string)llGetKey() + "@lsl.secondlife.com");

        // check every half minute
        llSetTimerEvent(30.0);
    }

    timer()
    {
        //Check for emails
        llGetNextEmail("", "");
    }

    email(string time, string address, string subj, string message, integer num_left)
    {
          llOwnerSay("I got an email: " + subj + "\n" + message);
     }
}
```

## See Also

### Events

- email

### Functions

- llEmail

<!-- /wiki-source -->
