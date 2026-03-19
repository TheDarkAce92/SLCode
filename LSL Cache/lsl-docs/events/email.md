---
name: "email"
category: "event"
type: "event"
language: "LSL"
description: "Triggered as a result of calling llGetNextEmail where there is a matching email in the email queue."
signature: "email(string time, string address, string subject, string message, integer num_left)"
wiki_url: 'https://wiki.secondlife.com/wiki/email'
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
deprecated: "false"
parameters: []
---

Triggered as a result of calling llGetNextEmail where there is a matching email in the email queue.


## Signature

```lsl
email(string time, string address, string subject, string message, integer num_left)
{
    // your code here
}
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `time` | In the (string)llGetUnixTime format |
| `string` | `address` |  |
| `string` | `subject` |  |
| `string` | `message` |  |
| `integer` | `num_left` | The number of emails remaining in the email queue.{{Footnote |


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/email)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/email) — scraped 2026-03-18_

## Caveats

- The email queue is limited to 100 emails, any email after that is bounced.
- The message field may have a maximum of 1000 single-byte characters. This count includes the header information (**address**, **subject**, etc).
- Emails sent from within SL will have their message body prefixed with a header detailing the originating prim. See llEmail for more details.
- Due to bug [SVC-23](https://jira.secondlife.com/browse/SVC-23) (present since 2005), objects may stop receiving emails completely until either the region is restarted or the object crosses a region boundary (resetting the script doesn't help).
- Due to bug [BUG-229767](https://jira.secondlife.com/browse/BUG-229767), an object's email queue can still become suspended until the object crosses a region border (neither a region restart nor a script reset helps). First analysis has revealed a potential workaround, by implementing a delay of about 30 seconds before first trying to send email to a freshly rezzed script - apparently registering the email(...) event handler can take quite some time, and emails arriving prior to said registry process is what gets the entire queue stuck. Official Linden response still pending.

## Examples

```lsl
default
{
    state_entry()
    {
        llSetTimerEvent(5.0);
    }

    timer()
    {
    //  get next email, don't filter by sender or subject
        llGetNextEmail("", "");
    }

    email( string time, string address, string subject, string message, integer num_left )
    {
    //  if we received an email from an object within Second Life
        if (llGetSubString(address, -19, -1) == "@lsl.secondlife.com")
//      {
            message = llDeleteSubString(message, 0, llSubStringIndex(message, "\n\n") + 1);
//      }

    //  PUBLIC_CHANNEL has the integer value 0
        llSay(PUBLIC_CHANNEL, message);

    //  if there's another email in the queue waiting
    //  get next email, don't filter by sender or subject
        if(num_left)
            llGetNextEmail("", "");
    }
}
```

## Notes

For tips on how to process emails sent from within SL, see the entry on llEmail.

## See Also

### Functions

- llEmail
- llGetNextEmail

<!-- /wiki-source -->
