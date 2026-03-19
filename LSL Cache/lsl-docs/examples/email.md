---
name: "email"
category: "example"
type: "example"
language: "LSL"
description: "Triggered as a result of calling llGetNextEmail where there is a matching email in the email queue."
wiki_url: "https://wiki.secondlife.com/wiki/Email"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL


email

- 1 Description
- 2 Specification
- 3 Caveats
- 4 Examples
- 5 Notes
- 6 See Also

  - 6.1 Functions
- 7 Deep Notes

  - 7.1 Issues
  - 7.2 All Issues
  - 7.3 Footnotes
  - 7.4 Signature
  - 7.5 Haiku

## Description

! Event: email( string time, string address, string subject, string message, integer num_left ){ ; }


	21
	Event ID


	Delay


Triggered as a result of calling llGetNextEmail where there is a matching email in the email queue.

• string

time

–

In the `(string)llGetUnixTime` format

• string

address

• string

subject

• string

message

• integer

num_left

–

The number of emails remaining in the email queue.

The email queue is associated with the prim and any script in the prim can access it.
 The prim's email address is its key with "@lsl.secondlife.com" appended, `llGetKey() + "@lsl.secondlife.com"`.

## Specification

The email event is triggered as a result of calling llGetNextEmail when there is an email that matches llGetNextEmail's optional filters. The first email that matches the filters is removed from the email queue and its data is used as the parameters for this event. If no email matches the filters but the queue is not empty this event is not triggered. Besides the effects of filtering, the email queue is FIFO.

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

•

llEmail

•

llGetNextEmail

## Deep Notes

#### Issues

#### All Issues

 ~ [Search JIRA for related Issues](http://jira.secondlife.com/secure/IssueNavigator!executeAdvanced.jspa?jqlQuery=%28summary+%7E+%22event+AND+email%22+OR+description+%7E+%22event+AND+email%22%29+&runQuery=true)

[](https://jira.secondlife.com/secure/ShowConstantsHelp.jspa?decorator=popup#IssueTypes)

[](https://jira.secondlife.com/secure/ShowConstantsHelp.jspa?decorator=popup#StatusTypes)

[SVC-23](http://jira.secondlife.com/browse/SVC-23)

A



Region incoming email queue for objects becomes suspended

[](https://jira.secondlife.com/secure/ShowConstantsHelp.jspa?decorator=popup#IssueTypes)

[](https://jira.secondlife.com/secure/ShowConstantsHelp.jspa?decorator=popup#StatusTypes)

[SVC-391](http://jira.secondlife.com/browse/SVC-391)

A



llEmail and llHTTPRequest do not handle non-ASCII characters

[](https://jira.secondlife.com/secure/ShowConstantsHelp.jspa?decorator=popup#IssueTypes)

[](https://jira.secondlife.com/secure/ShowConstantsHelp.jspa?decorator=popup#StatusTypes)

[SVC-412](http://jira.secondlife.com/browse/SVC-412)

A



Include "Content-Type: text/plain; charset=UTF-8" header in the messages forwarded from second life.

[](https://jira.secondlife.com/secure/ShowConstantsHelp.jspa?decorator=popup#IssueTypes)

[](https://jira.secondlife.com/secure/ShowConstantsHelp.jspa?decorator=popup#StatusTypes)

[SCR-499](http://jira.secondlife.com/browse/SCR-499)

A



llEmails to objects not in the same region arrive without a body or do not arrive at all.

[](https://jira.secondlife.com/secure/ShowConstantsHelp.jspa?decorator=popup#IssueTypes)

[](https://jira.secondlife.com/secure/ShowConstantsHelp.jspa?decorator=popup#StatusTypes)

[BUG-229767](http://jira.secondlife.com/browse/BUG-229767)

A



Object-to-object email sporadically fails

#### Footnotes

1. **^** The email being processed is not counted as it has already been popped from the queue.
1. **^** Preview grid email address are constructed differently: `llGetKey() + "@lsl." + grid + ".lindenlab.com"`; for the main beta grid set grid to "aditi".

#### Signature

```lsl
event void email( string time, string address, string subject, string message, integer num_left );
```

#### Haiku

Refulgent cockcrow


A red, full mailbox blows up


near the avatar