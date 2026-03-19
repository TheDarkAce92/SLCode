---
name: "llEmail"
category: "function"
type: "function"
language: "LSL"
description: 'Sends an email to address with subject and message.

The entire message (including the address, subject and other miscellaneous fields) can't be longer than 4096 bytes combined.'
signature: "void llEmail(string address, string subject, string message)"
return_type: "void"
sleep_time: "20.0"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llEmail'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llemail"]
---

Sends an email to address with subject and message.

The entire message (including the address, subject and other miscellaneous fields) can't be longer than 4096 bytes combined.


## Signature

```lsl
void llEmail(string address, string subject, string message);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `address` |  |
| `string` | `subject` |  |
| `string` | `message` |  |


## Caveats

- Forced delay: **20.0 seconds** — the script sleeps after each call.
- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llEmail)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llEmail) — scraped 2026-03-18_

Sends an email to address with subject and message.

## Caveats

- This function causes the script to sleep for 20.0 seconds.
- If you're sending to the object owner, prefer the llTargetedEmail method.
- There is a limit to the number of email messages an object can send in a given amount of time.
- There is a limit of 500 messages from a single agent's objects in a one-hour period.
- The 4096-byte size limit includes the subject line and automatically added text.  The practical maximum body size is approximately 3600 bytes.
- (Sept-2008) The Email Throttle was modified slightly, Per Prospero Linden's comments:


| "there has long been a throttle that makes a single script sleep for 20 seconds after sending an email. The new throttle is per user... some were using many, many different scripts to send spam. (the new throttle applies) when the destination is outside of Second Life. I know that messages within the same region were not throttled (beyond the 20-second delay), and I *believe* that messages between different sims were not throttled (between the 20-second delay)." |
| --- |

- Due to the bug [SVC-23](https://jira.secondlife.com/browse/SVC-23) (present since 2005), objects may stop receiving emails completely until either the region is restarted or the object crosses a region boundary (resetting the script doesn't help).  Emails sent may eventually be received after a restart/region-cross.  Hence, don't rely on this function for reliable inter-region messaging.
- Due to bug [BUG-229767](https://jira.secondlife.com/browse/BUG-229767), an object's email queue can still become suspended until the object crosses a region border (neither a region restart nor a script reset helps). First analysis has revealed a potential workaround, by implementing a delay of about 30 seconds before first trying to send email to a freshly rezzed script - apparently registering the email(...) event handler can take quite some time, and emails arriving prior to said registry process is what gets the entire queue stuck. Official Linden Lab response still pending.
- Due to the bug [SVC-391](https://jira.secondlife.com/browse/SVC-391), llEmail will silently fail (no mail will arrive) when  [non-ASCII](https://en.wikipedia.org/wiki/ASCII) characters are present in the subject. However, non-ASCII characters in the message body will be replaced by "?".

## Examples

```lsl
string emailAddress = "somebody@example.com";
string emailHeader = "Someone touched me!";

default
{
    touch_start(integer num_detected)
    {
        // llSay(PUBLIC_CHANNEL, "Sending eMail report now, this will take ~20 seconds.");

        key id = llDetectedKey(0);
        string name = llDetectedName(0);

        llEmail(emailAddress, emailHeader,
            "I was touched by: '" + name + "' (" + (string)id + ").");

        // llSay(PUBLIC_CHANNEL, "Email has been sent.");
    }
}
```

## Notes

- Because of the long delay on this function, it is often called from a second script triggered by link_message.
- If you are sending email to a prim within Second Life, its address is *[key]*@lsl.secondlife.com

  - Which means if the key returned by llGetKey is "a2e76fcd-9360-4f6d-a924-000000000003", then its email address is "a2e76fcd-9360-4f6d-a924-000000000003@lsl.secondlife.com".
  - Agents do not have fixed email addresses, use llInstantMessage or llOwnerSay.

### Prim2Prim Email

In LSL you can both send email with llEmail and receive it with the email event.

The email event is triggered with five pieces of information:

| • string | time | – | When the message was sent, in the `(string)llGetUnixTime` format |  |
| --- | --- | --- | --- | --- |
| • string | address | – | Who sent the message |  |
| • string | subject | – | Subject of the message |  |
| • string | message | – | Body of the message |  |
| • integer | num_left | – | The number of emails left in the email queue |  |

When receiving a message sent with llEmail it helps to separate the message from the prefixed header. The header and original message body are separated by "\n\n"

```lsl
integer divide = llSubStringIndex(message, "\n\n");
string header = llDeleteSubString(message, divide, -1);
message = llDeleteSubString(message, 0, divide + 1);
```

To get just one of the header items, do this:

```lsl
list lines = llParseStringKeepNulls(header, ["\n"], []);
string objname_line  = llList2String(lines, 0);
string region_line   = llList2String(lines, 1);
string localpos_line = llList2String(lines, 2);
```

To get a pure region name, do this:

```lsl
string region_name = llStringTrim(
            (string)llDeleteSubList(
                llParseStringKeepNulls(
                    llDeleteSubString(region_line, 0, 12),
                    [],
                    ["("]
                ), -2, -1), STRING_TRIM);
```

This application uses email to have objects check with a central server to see if the owner has the latest version. In the objects:

```lsl
string version = "1"; //
string type = "lolcube";
default
{
    on_rez(integer start_param)
    {
        llEmail("5a634b27-f032-283f-2df2-55ead7724b23@lsl.secondlife.com",
            version,
            (string)llGetOwner() + "," + type);
    }
}
```

The server:

```lsl
default
{
    state_entry()
    {
        llSetTimerEvent(15.0);
    }

    timer()
    {
        llGetNextEmail("", "");
    }

    email(string time, string address, string version, string message, integer num_left)
    {
        if ((integer)version < 2)
        {
            list info = llCSV2List(llDeleteSubString(message, 0, llSubStringIndex(message, "\n\n") + 1));
            llGiveInventory(llList2Key(info, 0), llList2String(info, 1));
        }

        if (num_left)
            llGetNextEmail("","");
    }
}
```

## See Also

### Events

- email
- link message

### Functions

- llGetNextEmail
- llMessageLinked

### Articles

- IM to email
- Postcards

<!-- /wiki-source -->
