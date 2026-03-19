---
name: "llTargetedEmail"
category: "function"
type: "function"
language: "LSL"
description: 'Sends an email to the owner (selected by target) of an object with subject and message.

The entire message (including the address, subject and other miscellaneous fields) can't be longer than 4096 bytes combined.'
signature: "void llTargetedEmail(integer target, string subject, string body)"
return_type: "void"
sleep_time: "20.0"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llTargetedEmail'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Sends an email to the owner (selected by target) of an object with subject and message.

The entire message (including the address, subject and other miscellaneous fields) can't be longer than 4096 bytes combined.


## Signature

```lsl
void llTargetedEmail(integer target, string subject, string body);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `target` |  |
| `string` | `subject` |  |
| `string` | `message` |  |


## Caveats

- Forced delay: **20.0 seconds** — the script sleeps after each call.
- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llTargetedEmail)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llTargetedEmail) — scraped 2026-03-18_

Sends an email to the owner (selected by target) of an object with subject and message.

## Caveats

- This function causes the script to sleep for 20.0 seconds.
- Originally this function was intended to enable sending email to either the object owner or creator; however, the ability to email creators was removed to avoid abuse scenarios.
- There is a limit to the number of email messages an object can send in a given amount of time.
- There is a limit of 500 messages from a single agent's objects in a one hour period.
- The 4096 byte size limit includes the subject line and automatically added text.  The practical maximum body size is approximately 3600 bytes.
- (Sept-2008) The Email Throttle was modified slightly, Per Prospero Linden's comments: "there has long been a throttle that makes a single script sleep for 20 seconds after sending an email. The new throttle is per user... some were using many, many different scripts to send spam. (the new throttle applies) when the destination is outside of Second Life. I know that messages within the same region were not throttled (beyond the 20-second delay), and I *believe* that messages between different sims were not throttled (between the 20-second delay)."
- Due to the bug [SVC-23](https://jira.secondlife.com/browse/SVC-23) (present since 2005), objects may stop receiving emails completely until either the region is restarted or the object crosses a region boundary (resetting the script doesn't help).  Emails sent may eventually be received after a restart/region-cross.  Hence, don't rely on this function for reliable inter-region messaging.
- Due to the bug [SVC-391](https://jira.secondlife.com/browse/SVC-391) llEmail will silently fail (no mail will arrive) when non-ascii characters are present in the subject. However, non-ascii characters in the message body will be replaced by "?".

## Examples

```lsl
string emailSubject = "Someone touched me!";

default
{
    touch_start(integer num_detected)
    {
        // llSay(PUBLIC_CHANNEL, "Sending eMail report now, this will take ~20 seconds.");

        key id = llDetectedKey(0);
        string name = llDetectedName(0);

        llTargetedEmail(TARGETED_EMAIL_OBJECT_OWNER, emailSubject,
            "I was touched by: '" + name + "' (" + (string)id + ").");

        // llSay(PUBLIC_CHANNEL, "Email has been sent.");
    }
}
```

## See Also

### Functions

- llEmail

<!-- /wiki-source -->
