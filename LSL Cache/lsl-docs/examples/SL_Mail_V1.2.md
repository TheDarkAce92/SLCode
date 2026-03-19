---
name: "SL Mail V1.2"
category: "example"
type: "example"
language: "LSL"
description: "Send and receive email from within Second Life from and to any address."
wiki_url: "https://wiki.secondlife.com/wiki/SL_Mail_V1.2"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Updated: 10-2-2011

**Second Life mail client**

**Send and receive email from within Second Life from and to any address.**

Implemented with Address Book function (in a notecard named 'Address Book') to stores addresses by name  and to compile groups of named addresses. Current version is stand-alone (no server functionality) and uses chat commands only.

URL: slmail.info (website coming soon!) **url slmail.info no longer used for SL Mail, and was taken for some other purpose.** Release Notes V1.2 SL Mail V1.2 Release notes (edition 2, 4 sept 2007) ### IMPORTANT NOTICE Development of SL Mail was abandoned midyear 2008. The domain slmail.info was abandoned and is now taken by another domain holder (ISS) who has nothing to do with SL Mail. SL Mail is considered for redevelopment under the same terms, using a version of the Serverless Key Exchange script. This allows mail clients to exchange their key adresses to other rezzed mail clients in world, and send each other info about the public name they use, and other info that could be usefull. This protocol does not use a central server. See: Serverless Key Exchange

Future annoucements about SL Mail development will be made here.

## LICENCE INFO

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <[http://www.gnu.org/licenses/](http://www.gnu.org/licenses/)>.

## PRODUCTION & MAINTANENCE

by Logic Scripted Products and Script Services

URL: [logicscripts.org](http://www.logicscripts.org) (website coming soon!)

SLurl:
[Logic Scripted products and Script services](http://slurl.com/secondlife/Beeratron/57/168/75/?&title=Logic+Scripted+products+and+Script+services)

Contact: Flennan Roffo

## DESCRIPTION

SL Mail V1.2 is a simple tool to send and receive mail from within SL.
You can either compose a message yourself using chat recording, or choose a notecard from inventory to send. The Address Book functionality allows you to use short names for mail recipients stored in a notecard. The current version does not have a persisent mail address. Watch out for the upcoming next release (V1.3) which will facilitate persisent in-world mail addresses and will be enhanced with many new features (See: Requests For Change (RFC).

## COMMANDS

**Command**

**Description**

**@Help**

Show Help about available commands

**@Record**

Starts a chat recording (for owner only).

**@Stop**

Stops the chat recording without sending

**@Continue**

Continues a previously stopped chat recording. Lines will be appended to you recording buffer.

**@Show**

Shows the content of the recording buffer.

**@Send**

If recording, stops the recording, and sends the mail (need to supply mail address and subject first!)

**@Send <notecard>**

Sends the content of the notecard, instead of the chat recording.

**@Ignore**

Ignores your current chat recording.

**@Mail <address>**

Define the mail address to send to.

**@Mail**

Shows the current mail address to send to.

**@Subject <subject>**

Define the subject of the mail.

**@Subject**

Shows the current mail subject.

**@Home <address>**

Set the HOME address of the owner (mail will be forwarder to this address when offline).

**@Home**

Show the HOME address.

**@Info**

Shows the mail address the object this script is running in uses (e.g. <object-key>@lsl.secondlife.com).

**@Read**

Reads the current message from the mail buffer (the mail buffer gets filled with mail you receive)

**@Select <msg>**

Select a message number from the availabe messages in the mail buffer.

**@Next**

Make next message the current message.

**@Prev**

Make previous message the current message.

**@First**

Make the first message the current message.

**@Last**

Make the last message the current message.

**@Clear**

Clear the mail buffer

**@Delete**

Deletes only the current message

**@Reply**

Starts a chat recording to reply to the current message. Mail adress and subject are filled in automatically.

Note:

- Commands are case insensitive ("@read" == "@READ"). Arguments might not be case insensitive.

## ADDRESS BOOK FORMAT

A notecard of the name 'Address Book' is read during initialization which may contain Address Book items and Groups.
The notecard is split in two sections, which need to be defined in that particular order.

**[ADDRESS BOOK]**

Defines the section in which you can put names for mail addresses,  like this:

**Name1=account@thisdomain.com**

**Name2=user@otherdomain.com**

etc.

**[GROUP]**

Define groups of previously defined names under a new name, like for instance:

**MyGroup=Name1, Name2**

Note that names of groups and individual mail adresses share the same namespace and must be unique.

So when you filled in your mail adresses in the Address Book, you can now use:

**@Mail Name1**

To send mail to  <account@thisdomain.com>

or you can use

**@Mail MyGroup**

To send mail to <account@thisdomain.com> and <user@otherdomain.com>
Mails will be sent one after another.

Notes:

- Names for Addreses and Groups are case insensitive (e.g. "mary"  == "MARY")

- The special address 'Self' can be used in commands where otherwise an address specification can be used. 'Self' is case insensitive (e.g. "self" == "SELF")

## LIMITATIONS

The current version is limited by the following:

- Chat recording lines are limited by the 255 byte limit

- Output of lines from the mail buffer are also limited by this 255 byte limit

- Incoming mail is limited to a 1000 (1024?) byte limit

- Outgoing mai is limited by a 4096 byte limit, which includes the standard mail header (region/location info on the first two lines)

We are making adjustments to this release to help overcome these limitations. At least the line lenght limit can be overcome by introducing a line continuation character (for example a hyphen '-') that when used at the end of a line appends the next line, so lines longer then 255 bytes are possible then.

To overcome the outgoing mail length limit, the mail can be broken textualy into parts, and each part can be send seperatedely, with an indication in the subject or in an introduced primary line of the mail body to indicate that the mail was split into parts.
For incoming mail and at least to receive mail from other SL Mail programs, a protocol will be introduced to receive mail in parts that are joined together after receiving them to form a single mail.

These enhancements will be made available in the next release (V1.3) of SL Mail

## BUGS

Report any bugs you find in this release to Logic (IM: Flennan Roffo).

## REQUEST FOR CHANGE (RFC)

Do you have additional wishes for enhancement of this product?
Contact Flennan Roffo and we will see if they can be implemented in the next release.

Existing RFC's are:

- Menu support for commands.

- Lines on incoming/outgoing mail longer than 255 bytes.

- Send messages longer than 4096 (minus SL mail header) bytes.

- Receive messages longer than 1024 bytes.

- Permanent mail addresses for the SL Mail client (like: )

Add your RFC!

## SL MAIL SUPPORT & DEVELOPMENT

In-world join the group "SL Mail" for bug reports, feature requests, the latest SL Mail release, and notices about development issues.

Scripts

## Script: SL Mail v1.2

SL Mail core module which scans for incoming mail messages and executes commands used by the owner.

```lsl
// SL Mail V1.2.lsl
// (c) 2007 Logic Scripted Products and Script Services
// Flennan Roffo

// VERSION
// Version: 1.2

// HISTORY
// Date         Version     Author              Comment
// --------------------------------------------------------------------------------------
// 28 aug 2007  V 1.0       Flennan Roffo       Created
//
//  1 sep 2007  V 1.1       Flennan Roffo       @Reply empties the recording buffer.
//                                                @Send while recording ends recording
//                                                and sends the mail if a mail address
//                                                and subject are supplied.
//                                                Fixed incorrect date in Unix2DateTime.
//  3 sep 2007  V 1.2       Flennan Roffo       Notification options:
//                                              - When online, send an IM when mail is received.
//                                              - When offline, send to HOME mail adress.
//                                              Adressbook
//                                              - Read adress book from config notecard.

// LICENCE
// This program is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License
// as published by the Free Software Foundation; either version 2
// of the License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
// (Also available at http://www.gnu.org/copyleft/gpl.html)

// DESCRIPTION
// Let's you record a message and sent to email and get messages and reply to messages.
// Must supply a valid mail adress and non-empty subject using chat commands.

// TODO:
// 1) Check for the maximum length of an email message (including newline and header).
// 2) Read adress book from notecard.                                    *DONE*
// 3) Send incoming mail to personal mail adress when offline.            *DONE*
// 4) Alert with an IM when online upon receiving new mail.                *DONE*

string   SL_MAIL_VERSION    = "V 1.2";
string   SL_MAIL_DATE       = "02 sep 2007";
integer  ErrorFlag          = FALSE;
list     ScriptList         = ["SL Mail Help V1.2", "SL Mail AddressBook V1.2",
                                "SL Mail OnlineStatus V1.2", "SL Mail FetchNotecard V1.2" ];
string   LSL_DOMAIN         = "lsl.secondlife.com";
integer  StatusOnline       = FALSE;

// Commands

string  COMMAND_RECORD     = "@RECORD";
string  COMMAND_CONTINUE   = "@CONTINUE";
string  COMMAND_STOP       = "@STOP";
string  COMMAND_MAIL       = "@MAIL";
string  COMMAND_SUBJECT    = "@SUBJECT";
string  COMMAND_SEND       = "@SEND";
string  COMMAND_SEE        = "@SEE";
string  COMMAND_IGNORE     = "@IGNORE";
string  COMMAND_READ       = "@READ";
string  COMMAND_DELETE     = "@DELETE";
string  COMMAND_CLEAR      = "@CLEAR";
string  COMMAND_REPLY      = "@REPLY";
string  COMMAND_NEXT       = "@NEXT";
string  COMMAND_PREV       = "@PREV";
string  COMMAND_FIRST      = "@FIRST";
string  COMMAND_LAST       = "@LAST";
string  COMMAND_LIST       = "@LIST";
string  COMMAND_SELECT     = "@SELECT";
string  COMMAND_HELP       = "@HELP";
string  COMMAND_INFO       = "@INFO";
string  COMMAND_RESET      = "@RESET";
string  COMMAND_SHOW       = "@SHOW";
string  COMMAND_ON         = "@ON";
string  COMMAND_OFF        = "@OFF";
string  COMMAND_HOME       = "@HOME";
string  COMMAND_LOAD       = "@LOAD";
string  COMMAND_ADDRESS    = "@ADDRESS";

// Recording

integer Recording = FALSE;

list    ChatRecording;
integer NumLines;
integer Length;

list     TimeList;
list     AddressList;
list     SubjectList;
list     BodyList;
integer  NumMessages;
integer  CurrentMessage = -1;

float    MAIL_FETCH_INTERVAL = 5.0;

// Link Messages

integer MSG_HELP                        = 10000;
integer MSG_STATUS_ONLINE               = 30000;
integer MSG_STATUS_OFFLINE              = 30100;

integer MSG_MESSAGE_SETADDRESS          = 90000;
integer MSG_MESSAGE_GETADDRESS          = 90050;
integer MSG_MESSAGE_SETSUBJECT          = 90100;
integer MSG_MESSAGE_GETSUBJECT          = 90150;
integer MSG_MESSAGE_SEND                = 90200;
integer MSG_MESSAGE_SENDHOME            = 90300;
integer MSG_MESSAGE_SEND_NOTECARD       = 90400;
integer MSG_MESSAGE_ADDRESSBOOK         = 90500;
integer MSG_MESSAGE_GETHOME             = 90600;
integer MSG_MESSAGE_SETHOME             = 90700;
integer MSG_MESSAGE_INFO                = 90800;

integer MSG_ADDRESSBOOK_LOADED          = 91000;
integer MSG_ADDRESSBOOK_ERROR           = 91100;

integer MSG_MESSAGE_REPLY               = 99000;

integer MSG_NOTECARD_READ               = 100000;
integer MSG_NOTECARD_FETCHED            = 100100;

// Unix Time conversion

integer DAYS_PER_YEAR        = 365;//  Non leap year
integer SECONDS_PER_YEAR     = 31536000;//  Non leap year
integer SECONDS_PER_DAY      = 86400;
integer SECONDS_PER_HOUR     = 3600;
integer SECONDS_PER_MINUTE   = 60;

integer isLeapYear(integer year)
{
    if (year % 4 == 0)
    {
        if (year % 100 == 0)
        {
            if (year % 400 == 0)
                return TRUE;
        //  else
                return FALSE;
        }
    //  else
            return TRUE;
    }
//  else
        return FALSE;
}

integer DaysPerMonth(integer year,integer month)
{
    if (month < 8)
    {
        if (month % 2 == 0)
        {
            if (month == 2)
            {
                if (isLeapYear(year))
                    return 29;

            //  else
                    return 28;
            }
        //  else
                return 30;
        }
    //  else
            return 31;
    }
    else
    {
        if (month % 2 == 0)
            return 31;

    //  else
            return 30;
    }
}

integer DaysPerYear(integer year)
{
    if (isLeapYear(year))
        return DAYS_PER_YEAR + 1;
    else
        return DAYS_PER_YEAR;
}

list Unix2DateTime(integer unixtime)
{
    integer days_since_1_1_1970     = unixtime / SECONDS_PER_DAY;
    integer day = days_since_1_1_1970 + 1;
    integer year  = 1970;
    integer days_per_year = DaysPerYear(year);

    while (day > days_per_year)
    {
        day -= days_per_year;
        ++year;
        days_per_year = DaysPerYear(year);
    }

    integer month = 1;
    integer days_per_month = DaysPerMonth(year,month);

    while (day > days_per_month)
    {
        day -= days_per_month;

        if (++month > 12)
        {
            ++year;
            month = 1;
        }

        days_per_month = DaysPerMonth(year,month);
    }

    integer seconds_since_midnight  = unixtime % SECONDS_PER_DAY;
    integer hour          = seconds_since_midnight / SECONDS_PER_HOUR;
    integer second         = seconds_since_midnight % SECONDS_PER_HOUR;
    integer minute      = second / SECONDS_PER_MINUTE;
    second               = second % SECONDS_PER_MINUTE;

    return [ year, month, day, hour, minute, second ];
}

list MonthNameList = [     "JAN", "FEB", "MAR", "APR", "MAY", "JUN",
                        "JUL", "AUG", "SEP", "OCT" , "NOV", "DEC" ];

string MonthName(integer month)
{
    if (0 <= month < 12)
        return llList2String(MonthNameList, month);
//  else
        return "";
}

string DateString(list timelist)
{
    integer year       = llList2Integer(timelist, 0);
    integer month      = llList2Integer(timelist, 1);
    integer day        = llList2Integer(timelist, 2);

    return (string)day + "-" + MonthName(month - 1) + "-" + (string)year;
}

string TimeString(list timelist)
{
    integer hour          = llList2Integer(timelist, 3);
    integer minute         = llList2Integer(timelist, 4);
    integer second         = llList2Integer(timelist, 5);
    string  hourstr     = llGetSubString("0" + (string)hour, -2, -1);
    string  minutestr   = llGetSubString("0" + (string)minute, -2, -1);
    string  secondstr   = llGetSubString("0" + (string)second, -2, -1);

    return
        hourstr + ":" + minutestr + ":" + secondstr;
}

SendMail(string body)
{
    // llOwnerSay("Sending message to '" + address + "' with subject '" + subject +"'.");
    llMessageLinked(LINK_THIS, MSG_MESSAGE_SEND, body, NULL_KEY);
}

SendHome(string subject, string body)
{
    llMessageLinked(LINK_THIS, MSG_MESSAGE_SENDHOME, body, (key)subject);
}

Show()
{
    llOwnerSay("Current chat recording is:");
    llOwnerSay("--------------------------");

    integer i;
    do
    {
        llOwnerSay(llList2String(ChatRecording, i));
    }
    while (++i < NumLines);

    llOwnerSay("--------------------------");
    llOwnerSay("Lines is " + (string)NumLines);
    llOwnerSay("Message length is " + (string)Length);
}

Read()
{
    llOwnerSay("Reading message " + (string)CurrentMessage + " from mail buffer.");
    integer time = (integer)llList2Integer(TimeList,CurrentMessage);
    list timelist=Unix2DateTime(time);
    string Address = llList2String(AddressList,CurrentMessage);
    string Subject = llList2String(SubjectList,CurrentMessage);
    string Body    = llList2String(BodyList,CurrentMessage);
    llOwnerSay("Date   : " + DateString(timelist));
    llOwnerSay("Time   : " + TimeString(timelist));
    llOwnerSay("Address: " + Address);
    llOwnerSay("Subject: " + Subject);
    llOwnerSay("Begin of message body:");
    llOwnerSay("-------------------------");
    list bodylist=llParseStringKeepNulls(Body, [ "\n" ], []);
    integer num=llGetListLength(bodylist);

    integer i;
    do
    {
        llOwnerSay(llList2String(bodylist, i));
    }
    while (++i < num);

    llOwnerSay("-------------------------");
    llOwnerSay("End of message body.");
}

List()
{
    llOwnerSay("The mail buffer contains the following messages:\n");

    integer i;
    do
    {
        integer time=llList2Integer(TimeList,i);
        list timelist=Unix2DateTime(time);
        if (/* 0 < */ i) llOwnerSay("+-+-+-+-+-+-+-+-+-+-+-+-");
        llOwnerSay("Message: " + (string)i);
        llOwnerSay("Date   : " + DateString(timelist));
        llOwnerSay("Time   : " + TimeString(timelist));
        llOwnerSay("From:    " + llList2String(AddressList,i));
        llOwnerSay("Subject: " + llList2String(SubjectList,i));
    }
    while (++i < NumMessages);
}

NotifyNewMail(string time, string address, string subject, string body)
{
    list timelist=Unix2DateTime((integer)time);

    if (StatusOnline)
    {
        llInstantMessage(llGetOwner(), "You received a new mail message on "
                                    + DateString(timelist) + " at " + TimeString(timelist)
                                    + " from " + address
                                    + " with the subject " + subject);
    }
    else
    {
        SendHome("FW: " + subject, "Received at: " + DateString(timelist) + " " + TimeString(timelist) + "\nFrom: " +  address
                    + "\nBegin message body:\n-------------------\n" + body + "\n-------------------\nEnd message body.");
    }
}

ResetOtherScripts()
{
    string name;
    integer num=llGetListLength(ScriptList);

    integer i;
    do
    {
        name = llList2String(ScriptList, i);

        if (llGetInventoryType(name) == INVENTORY_SCRIPT)
        {
            llResetOtherScript(name);
        }
        else
        {
            llOwnerSay("Error - script '" + name + "' not found.");
            ErrorFlag = TRUE;
        }
    }
    while (++i < num);
}

default
{
    on_rez(integer start_param)
    {
        llResetScript();
    }

    changed(integer perm)
    {
        if (perm & (CHANGED_OWNER | CHANGED_INVENTORY))
            llResetScript();
    }

    state_entry()
    {
        llOwnerSay("Welcome to SL Mail, released under GNU software licence.");
        llOwnerSay("Version " + SL_MAIL_VERSION + " " + SL_MAIL_DATE);
        llOwnerSay("Produced by Logic Scripted Products & Product Services");
        llOwnerSay("Free memory: " + (string)llGetFreeMemory());
        ResetOtherScripts();

        if (ErrorFlag)
            state Error;
    }

    link_message(integer sender, integer msgid, string message, key id)
    {
        if (msgid == MSG_STATUS_ONLINE)
            StatusOnline = TRUE;

        else if (msgid == MSG_STATUS_OFFLINE)
            StatusOnline = FALSE;

        else if (msgid == MSG_ADDRESSBOOK_LOADED)
            state running;

        else if (msgid == MSG_ADDRESSBOOK_ERROR)
            state Error;
    }
}

state running
{
    on_rez(integer start_param)
    {
        llResetScript();
    }

    changed(integer perm)
    {
        if (perm & (CHANGED_OWNER | CHANGED_INVENTORY))
            llResetScript();
    }

    state_entry()
    {
        llListen(PUBLIC_CHANNEL, "", llGetOwner(), "");
        llOwnerSay("SL mail ready.\nSend and Get mail in Second Life.\nType @HELP for more info.");
        llMessageLinked(LINK_THIS, MSG_MESSAGE_INFO, "", NULL_KEY);
        llGetNextEmail("", "");
        llSetTimerEvent(MAIL_FETCH_INTERVAL);
    }

    listen(integer channel, string name, key id, string message)
    {
        string trimmessage=llStringTrim(message,STRING_TRIM);
        list   parse = llParseStringKeepNulls(trimmessage, [ " "], []);
        string command = llToUpper(llList2String(parse,0));
        string arg     = llStringTrim(llList2String(parse,1),STRING_TRIM);
        integer nargs  = llGetListLength(parse);
        string argstr="";

        if (nargs > 1) argstr=llGetSubString(message, llSubStringIndex(message, " ") + 1, -1);

        if (Recording)
        {
            if (command == COMMAND_STOP)
            {
                llOwnerSay("Recording stopped. Type @SHOW to see the message you have entered,"
                            + " or @SEND to send it.");
                Recording = FALSE;
                return;
            }
            if (command == COMMAND_SEND)
            {
                Recording = FALSE;

                SendMail(llDumpList2String(ChatRecording, "\n"));
                return;
            }
            else
            {
                ChatRecording = (ChatRecording=[]) + ChatRecording + [ message ];
                ++NumLines;
                Length += llStringLength(message) + 2;
                return;
            }
        }
        else
        {
            if (command == COMMAND_RECORD)
            {
                llOwnerSay("Start recording your message. Type @STOP to end recording.");
                ChatRecording = [];
                NumLines=0;
                Length=0;
                Recording = TRUE;
                return;
            }
            if (command == COMMAND_CONTINUE)
            {
                llOwnerSay("Continue recording your message. Type @STOP to end recording.");
                Recording = TRUE;
                return;
            }
            if (command == COMMAND_REPLY)
            {
                if (CurrentMessage == -1)
                {
                    llOwnerSay("The mail buffer is empty.");
                }
                else
                {
                    string address=llList2String(AddressList,CurrentMessage);
                    string subject="Re: " + llList2String(SubjectList,CurrentMessage);
                    llMessageLinked(LINK_THIS, MSG_MESSAGE_SETADDRESS, address, NULL_KEY);
                    llMessageLinked(LINK_THIS, MSG_MESSAGE_SETSUBJECT, subject, NULL_KEY);
                    ChatRecording = [];
                    NumLines=0;
                    Length=0;
                    Recording = TRUE;
                }
                return;
            }
            if (command == COMMAND_MAIL)
            {
                string mailaddress=llStringTrim(argstr,STRING_TRIM);

                if (mailaddress != "")
                {
                    llMessageLinked(LINK_THIS, MSG_MESSAGE_SETADDRESS, mailaddress, NULL_KEY);
                }
                else
                {
                    llMessageLinked(LINK_THIS, MSG_MESSAGE_GETADDRESS, "", NULL_KEY);
                }
                return;
            }
            if (command == COMMAND_SUBJECT)
            {
                string mailsubject=llStringTrim(argstr,STRING_TRIM);

                if (mailsubject != "")
                {
                    llMessageLinked(LINK_THIS, MSG_MESSAGE_SETSUBJECT, mailsubject, NULL_KEY);
                }
                else
                {
                    llMessageLinked(LINK_THIS, MSG_MESSAGE_GETSUBJECT, "", NULL_KEY);
                }
                return;
            }
            if (command == COMMAND_STOP)
            {
                llOwnerSay("Not recording.");
                return;
            }
            if (command == COMMAND_SEND)
            {
                if (nargs == 1)
                {
                    if (NumLines == 0)
                    {
                        llOwnerSay("No lines recorded.");
                    }
                    else
                    {
                        SendMail(llDumpList2String(ChatRecording, "\n"));
                    }
                }
                else
                {
                    llMessageLinked(LINK_THIS, MSG_MESSAGE_SEND_NOTECARD, argstr, NULL_KEY);
                }
                return;
            }
            if (command == COMMAND_IGNORE)
            {
                if (NumLines == 0)
                {
                    llOwnerSay("No lines recorded.");
                }
                else
                {
                    ChatRecording = [];
                    NumLines = 0;
                    Length = 0;
                }
                return;
            }
            if (command == COMMAND_SHOW)
            {
                if (NumLines == 0)
                {
                    llOwnerSay("No lines recorded.");
                }
                else
                {
                    Show();
                }
                return;
            }
            if (command == COMMAND_READ)
            {
                if (NumMessages == 0)
                {
                    llOwnerSay("The mail buffer is empty.");
                }
                else
                {
                    Read();
                }
                return;
            }
            if (command == COMMAND_NEXT)
            {
                if (CurrentMessage == -1)
                {
                    llOwnerSay("The mail buffer is empty.");
                }
                else
                {
                    if (CurrentMessage == NumMessages - 1)
                    {
                        llOwnerSay("Already at last message.");
                    }
                    else
                    {
                        ++CurrentMessage;
                        Read();
                    }
                }
                return;
            }
            if (command == COMMAND_PREV)
            {
                if (CurrentMessage == -1)
                {
                    llOwnerSay("The mail buffer is empty.");
                }
                else
                {
                    if (CurrentMessage == 0)
                    {
                        llOwnerSay("Already at first message.");
                    }
                    else
                    {
                        --CurrentMessage;
                        Read();
                    }
                }
                return;
            }
            if (command == COMMAND_FIRST)
            {
                if (CurrentMessage == -1)
                {
                    llOwnerSay("The mail buffer is empty.");
                }
                else
                {
                    if (CurrentMessage == 0)
                    {
                        llOwnerSay("Already at first message.");
                    }
                    else
                    {
                        CurrentMessage = 0;
                        Read();
                    }
                }
                return;
            }
            if (command == COMMAND_LAST)
            {
                if (CurrentMessage == -1)
                {
                    llOwnerSay("The mail buffer is empty.");
                }
                else
                {
                    if (CurrentMessage == NumMessages - 1)
                    {
                        llOwnerSay("Already at last message.");
                    }
                    else
                    {
                        CurrentMessage = NumMessages - 1;
                        Read();
                    }
                }
                return;
            }
            if (command == COMMAND_LIST)
            {
                if (CurrentMessage == -1)
                {
                    llOwnerSay("The mail buffer is empty.");
                }
                else
                {
                    List();
                }
                return;
            }
            if (command == COMMAND_SELECT)
            {
                if (CurrentMessage == -1)
                {
                    llOwnerSay("The mail buffer is empty.");
                }
                else if (nargs == 1)
                {
                    llOwnerSay("Need to supply a message number.");
                }
                else
                {
                    integer msgnum = (integer)arg;

                    if (msgnum < 0 || msgnum >= NumMessages)
                    {
                        llOwnerSay("Message number " + arg + " not in mail buffer.");
                    }
                    else
                    {
                        CurrentMessage = msgnum;
                    }
                }
                return;
            }
            if (command == COMMAND_DELETE)
            {
                if (CurrentMessage == -1)
                {
                    llOwnerSay("The mail buffer is empty.");
                }
                else
                {
                    TimeList = llDeleteSubList(TimeList,CurrentMessage,CurrentMessage);
                    AddressList = llDeleteSubList(AddressList,CurrentMessage,CurrentMessage);
                    SubjectList = llDeleteSubList(SubjectList,CurrentMessage,CurrentMessage);
                    BodyList = llDeleteSubList(BodyList,CurrentMessage,CurrentMessage);
                    --NumMessages;

                    if (NumMessages == 0)
                    {
                        CurrentMessage = -1;
                    }
                    else if (CurrentMessage >= NumMessages)
                    {
                        CurrentMessage = NumMessages - 1;
                    }
                }
                return;
            }
            if (command == COMMAND_CLEAR)
            {
                if (CurrentMessage == -1)
                {
                    llOwnerSay("The mail buffer is empty.");
                }
                else
                {
                    TimeList = [];
                    AddressList = [];
                    SubjectList = [];
                    BodyList = [];
                    NumMessages = 0;
                    CurrentMessage = -1;
                }
                return;
            }
            if (command == COMMAND_HELP)
            {
                llMessageLinked(LINK_THIS, MSG_HELP, arg, NULL_KEY);
                return;
            }
            if (command == COMMAND_INFO)
            {
                llMessageLinked(LINK_THIS, MSG_MESSAGE_INFO, "", NULL_KEY);
                return;
            }
            if (command == COMMAND_SHOW)
            {
                Show();
                return;
            }
            if (command == COMMAND_RESET)
            {
                llResetScript();
                return;
            }
            if (command == COMMAND_OFF)
            {
                state not_running;
            }
            if (command == COMMAND_HOME)
            {
                if (nargs==1)
                {
                    llMessageLinked(LINK_THIS, MSG_MESSAGE_GETHOME, "", NULL_KEY);
                }
                else
                {
                    llMessageLinked(LINK_THIS, MSG_MESSAGE_SETHOME, argstr, NULL_KEY);
                }
                return;
            }
        }
    }

    timer()
    {
        llGetNextEmail("", "");
    }

    email(string time, string address, string subject, string body, integer queued)
    {
        NotifyNewMail(time, address, subject, body);
        TimeList = (TimeList=[]) + TimeList + [time];
        AddressList = (AddressList=[]) + AddressList + [address];
        SubjectList = (SubjectList=[]) + SubjectList + [subject];
        BodyList = (BodyList=[]) + BodyList + [body];
        ++NumMessages;

        if (CurrentMessage == -1)
        {
            CurrentMessage = 0;
        }
        else
        {
            CurrentMessage = NumMessages - 1;
        }
    }

    link_message(integer sender, integer msgid, string message, key id)
    {
        if (msgid == MSG_STATUS_ONLINE)
        {
            StatusOnline = TRUE;
        }
        else if (msgid == MSG_STATUS_OFFLINE)
        {
            StatusOnline = FALSE;
        }
        else if (msgid == MSG_MESSAGE_REPLY)
        {
            llOwnerSay(message);
        }
    }
}

state not_running
{
    on_rez(integer start_param)
    {
        llResetScript();
    }

    changed(integer perm)
    {
        if (perm & (CHANGED_OWNER | CHANGED_INVENTORY))
            llResetScript();
    }

    state_entry()
    {
        llOwnerSay("SL Mailbox switched OFF. Say @ON to switch it back on.");
        llListen(PUBLIC_CHANNEL, "", llGetOwner(), "");
    }

    listen(integer chan, string name, key id, string message)
    {
        string command=llToUpper(message);

        if (command == COMMAND_ON)
        {
            state running;
        }
    }

    link_message(integer sender, integer msgid, string message, key id)
    {
        if (msgid == MSG_STATUS_ONLINE)
        {
            StatusOnline = TRUE;
        }
        else if (msgid == MSG_STATUS_OFFLINE)
        {
            StatusOnline = FALSE;
        }
    }
}

state Error
{
    on_rez(integer start_param)
    {
        llResetScript();
    }

    changed(integer perm)
    {
        if (perm & (CHANGED_OWNER | CHANGED_INVENTORY))
            llResetScript();
    }

    state_entry()
    {
        llOwnerSay("Error in SL Mail: not all component scripts found.");
    }
}

//////////////////////////////////
// End SL Mail V1.2.lsl
//////////////////////////////////
```

## Script: SL Mail Address Book V1.2

Read and interpret the contents of the Address Book.

```lsl
// SL Mail AddressBook V1.2.lsl
//
// DESCRIPTION
//
//  Read the Address Book from a notecard named "Address Book".
//
//  The Address Book has the following format:
//
//  [ADDRESS BOOK]
//  Name1=username@yourdomain.com
//  Name2=otheruser@otherdomain.com
//  ...
//  [GROUP]
//  group1=Name1, Name2
//  ...
//
//  Notes:
//  1. Group and Name share the same namespace, and must be unique.
//  2. It is allowed to have a name in the addressbook with multiple addresses, seperated by comma's.
//
/////////////////////////////////////////////////

string  CurrentMailAddress = "";
string  CurrentMailSubject = "";
integer StatusOnline = FALSE;

// Fetch or Send notecard

string  Notecard2Fetch="";

// Address Book Names

list    AddressBookList=[];
list    MailAddressList=[];

string  STRING_HOME="HOME";
string  STRING_SELF="SELF";

// Address Book Groups

list   GroupList=[];
list   GroupNameList=[];

string LSL_DOMAIN = "lsl.secondlife.com";

// Read Address Book notecard

string  ADDRESSBOOK_NOTECARD="Address Book";
integer Line=0;
key     reqAddressBook=NULL_KEY;
float   TIMEOUT_INTERVAL=5.0;

integer Section=0;
integer SECTION_ADDRESS_BOOK=1;
integer SECTION_GROUP=2;
string  STRING_ADDRESS_BOOK="ADDRESS BOOK";
string  STRING_GROUP="GROUP";

// Links messages

integer MSG_MESSAGE_SETADDRESS          = 90000;
integer MSG_MESSAGE_GETADDRESS          = 90050;
integer MSG_MESSAGE_SETSUBJECT          = 90100;
integer MSG_MESSAGE_GETSUBJECT          = 90150;
integer MSG_MESSAGE_SEND                = 90200;
integer MSG_MESSAGE_SENDHOME            = 90300;
integer MSG_MESSAGE_SEND_NOTECARD       = 90400;
integer MSG_MESSAGE_ADDRESSBOOK         = 90500;
integer MSG_MESSAGE_GETHOME             = 90600;
integer MSG_MESSAGE_SETHOME             = 90700;
integer MSG_MESSAGE_INFO                = 90800;
integer MSG_MESSAGE_NOTIFY              = 90900;

integer MSG_ADDRESSBOOK_LOADED            = 91000;
integer MSG_ADDRESSBOOK_ERROR            = 91100;

integer MSG_MESSAGE_REPLY               = 99000;

integer MSG_NOTECARD_READ               = 100000;
integer MSG_NOTECARD_FETCHED            = 100100;

///////////////////////////// GetSelfAddress() ///////////////////////

string GetSelfAddress()
{
    return (string)llGetKey() + "@" + LSL_DOMAIN;
}

///////////////////////////// Info() /////////////////////////////////

Info()
{
    llMessageLinked(LINK_THIS, MSG_MESSAGE_REPLY, "The mail address for this object is: "
                    + GetSelfAddress() + ".", NULL_KEY);
}

///////////////////////////////// IsValidKeyFormat() //////////////////////

integer IsValidKeyFormat(string str)
{
    string keychars = "0123456789abcdef";

    if (llStringLength(str) != 36)
        return FALSE;

    if( (llGetSubString( str, 8, 8 )   != "-" ||
        llGetSubString( str, 13, 13 )  != "-" ||
        llGetSubString( str, 18, 18 )  != "-" ||
        llGetSubString( str, 23, 23 )  != "-" ) )
        return FALSE;

    integer i;

    for (i = 0; i < 8; ++i)
    {
        if (llSubStringIndex(keychars, llGetSubString(str,i,i)) == -1)
            return FALSE;
    }

    for (i = 9; i < 13; ++i)
    {
        if (llSubStringIndex(keychars, llGetSubString(str,i,i)) == -1)
            return FALSE;
    }

    for (i = 14; i < 18; ++i)
    {
        if (llSubStringIndex(keychars, llGetSubString(str,i,i)) == -1)
            return FALSE;
    }

    for (i = 19; i < 23; ++i)
    {
        if (llSubStringIndex(keychars, llGetSubString(str,i,i)) == -1)
            return FALSE;
    }

    for (i = 24; i < 36; ++i)
    {
        if (llSubStringIndex(keychars, llGetSubString(str,i,i)) == -1)
            return FALSE;
    }

    return TRUE;
}

///////////////////////////////// ValidMailAddress() ////////////////////////

integer ValidMailAddress(string arg)
{
    string adress = llToLower(llStringTrim(arg,STRING_TRIM));

    if (adress == "")
        return FALSE;

    list parse = llParseStringKeepNulls(adress, [ "@" ], []);
    string account = llList2String(parse,0);
    string domain  = llList2String(parse,1);

    if (llGetListLength(parse) != 2 || llStringLength(account) == 0 || llStringLength(domain) == 0)
        return FALSE;

    if (domain == LSL_DOMAIN)
    {
        return IsValidKeyFormat(account);
    }
    else
    {
        list parsedomain = llParseString2List(domain, [ "." ], []);

        if (llGetListLength(parsedomain) < 2)
            return FALSE;

        integer num = llGetListLength(parsedomain);
        integer i;

        for (i = 0; i < num; ++i)
        {
            if (llStringLength(llList2String(parsedomain,i)) < 2)
            {
                return FALSE;
            }
        }
    }

    return TRUE;
}

/////////////////////////////////// GetAddressStr() ///////////////////

string GetAndCheckAddressStr(string address)
{
    list addresslist = llCSV2List(address);
    integer num=llGetListLength(addresslist);
    integer i;
    string addressstr="";
    string curaddress="";

    for (i = 0; i < num; ++i)
    {
        curaddress=llList2String(addresslist,i);

        if (ValidMailAddress(curaddress))
        {
            addressstr = (addressstr="") + addressstr + curaddress + ",";
        }
        else
        {
            llMessageLinked(LINK_THIS, MSG_MESSAGE_REPLY, "Invalid address string: '"
                            + curaddress + "'.", NULL_KEY);
        }
    }

    return llGetSubString(addressstr, 0, -2);
}

///////////////////////////// ProcessLine() ////////////////////////////

ProcessLine(string rawline)
{
    string line=llStringTrim(rawline,STRING_TRIM);
    string first=llGetSubString(line,0,0);
    string last=llGetSubString(line,-1,-1);

    // Ignore a blank line or comment line
    if (line == "" || first == "#")
        return;

    // Check for the right section

    if (first == "[" && last == "]")
    {
        string sectionstr=llToUpper(llStringTrim(llGetSubString(line,1,-2),STRING_TRIM));

        if (sectionstr == STRING_ADDRESS_BOOK)
        {
            Section = SECTION_ADDRESS_BOOK;
        }
        else if (sectionstr == STRING_GROUP)
        {
            if (Section == 0)
            {
                llMessageLinked(LINK_THIS, MSG_MESSAGE_REPLY, "Invalid syntax in '" + ADDRESSBOOK_NOTECARD
                        + "' at line " + (string)(Line + 1)
                        + ". Group section defined before Address Book section.", NULL_KEY);
            }
            else
            {
                Section = SECTION_GROUP;
            }
        }
        else
        {
            llMessageLinked(LINK_THIS, MSG_MESSAGE_REPLY, "Invalid section header '" + sectionstr
                        + "' in " + ADDRESSBOOK_NOTECARD + " at line " + (string)(Line + 1) + ".", NULL_KEY);
        }

        return;
    }

    // Must be in a section

    if (Section == 0)
    {
        llMessageLinked(LINK_THIS, MSG_MESSAGE_REPLY, "Invalid syntax in '" + ADDRESSBOOK_NOTECARD
                        + "' at line " + (string)(Line + 1) + ". No section header.", NULL_KEY);
        return;
    }

    list     parse=llParseString2List(line, [ "=" ], []);
    integer  num=llGetListLength(parse);

    // Format must be correct

    if (num != 2)
    {
        llMessageLinked(LINK_THIS, MSG_MESSAGE_REPLY, "Invalid syntax in '" + ADDRESSBOOK_NOTECARD
                        + "' at line " +  (string)(Line+1) + ":\n" + rawline, NULL_KEY);
        return;
    }

    if (Section == SECTION_ADDRESS_BOOK)
    {
        string name=llStringTrim(llList2String(parse,0),STRING_TRIM);

        if (llToUpper(name) == STRING_SELF)
        {
            llMessageLinked(LINK_THIS, MSG_MESSAGE_REPLY, "Invalid address book entry '" + name
                            + "'. Reserved word in '" + ADDRESSBOOK_NOTECARD
                        + "' at line " + (string)(Line + 1) + ".", NULL_KEY);
        }
        else if (llListFindList(AddressBookList, [ name ]) == -1)
        {
            string address=llStringTrim(llList2String(parse,1),STRING_TRIM);
            string addressstr=GetAndCheckAddressStr(address);

            if (addressstr != "")
            {
                AddressBookList     = (AddressBookList=[])     + AddressBookList     + [ name ];
                MailAddressList     = (MailAddressList=[])     + MailAddressList     + [ addressstr ];
            }
            else
            {
                llMessageLinked(LINK_THIS, MSG_MESSAGE_REPLY, "No valid mail address for '" + name
                    + "'. Entry skipped in '" + ADDRESSBOOK_NOTECARD + "' at line " + (string)(Line + 1)
                    + ".", NULL_KEY);
            }
        }
        else
        {
            llMessageLinked(LINK_THIS, MSG_MESSAGE_REPLY, "Name '" + name
                + "' already defined. Entry skipped in '" + ADDRESSBOOK_NOTECARD + "' at line "
                + (string)(Line + 1) + ".", NULL_KEY);
        }
    }
    else // Group
    {
        string group=llStringTrim(llList2String(parse,0),STRING_TRIM);

        if (llToUpper(group) == STRING_SELF)
        {
            llMessageLinked(LINK_THIS, MSG_MESSAGE_REPLY, "Invalid address book entry '" + group
                            + "'. Reserved word in '" + ADDRESSBOOK_NOTECARD
                        + "' at line " + (string)(Line + 1) + ".", NULL_KEY);
        }
        else if (llListFindList(AddressBookList, [ group ]) == -1)
        {
            if (llListFindList(GroupList, [ group ]) == -1)
            {
                string names=llStringTrim(llList2String(parse,1),STRING_TRIM);
                list   namelist=llCSV2List(names);
                integer num=llGetListLength(namelist);
                integer i;
                integer index;
                string  name;
                string  namestr="";

                for (i = 0; i < num; ++i)
                {
                    name=llList2String(namelist,i);
                    index=llListFindList(AddressBookList, [ name ]);

                    if (index == -1)
                    {
                        llMessageLinked(LINK_THIS, MSG_MESSAGE_REPLY, "Name '" + name + "' defined in Group '"
                                + group + "' not found in '" + ADDRESSBOOK_NOTECARD + "' at line "
                                + (string)(Line + 1) + ".", NULL_KEY);
                    }
                    else
                    {
                        namestr = (namestr="") + namestr + name + ",";
                    }
                }

                if (namestr != "")
                {
                    namestr=llGetSubString(namestr,0,-2);
                    GroupList         = (GroupList=[])         + GroupList     + [ group ];
                    GroupNameList     = (GroupNameList=[])    + GroupNameList + [ namestr ];
                }
                else
                {
                    llMessageLinked(LINK_THIS, MSG_MESSAGE_REPLY, "Group '" + group
                        + "' has no valid names. Entry skipped in '" + ADDRESSBOOK_NOTECARD + "' at line "
                        + (string)(Line + 1) + ".", NULL_KEY);
                }
            }
            else
            {
                llMessageLinked(LINK_THIS, MSG_MESSAGE_REPLY, "Group '" + group
                    + "' already defined in Group. Entry skipped in '" + ADDRESSBOOK_NOTECARD + "' at line "
                    + (string)(Line + 1) + ".", NULL_KEY);
            }
        }
        else
        {
            llMessageLinked(LINK_THIS, MSG_MESSAGE_REPLY, "Group '" + group
                + "' already defined in Address Book. Entry skipped in '" + ADDRESSBOOK_NOTECARD + "' at line "
                + (string)(Line + 1) + ".", NULL_KEY);
        }
    }
}

//////////////////////////////// GetGroupAddressList ///////////////

string GetGroupAddressList(string group)
{
    integer index=llListFindList(GroupList, [ group ]);
    integer i;
    integer num=llGetListLength(GroupList);
    string  grouplist="";

    if (index == -1)
    {
        return "";
    }
    else
    {
        for (i = index; i < num; ++i)
        {
            if (llList2String(GroupList,i) == group)
            {
                grouplist = (grouplist="") + grouplist + llList2String(GroupNameList,i) + ",";
            }
        }

        if (grouplist != "") grouplist=llGetSubString(grouplist,0,-2);   // remove last ","
        return grouplist;
    }
}

//////////////////////////////// SetMailAddress() //////////////////

SetMailAddress(string address)
{
    integer index=llListFindList(AddressBookList, [ address ]);

    if (index == -1)
    {
        index=llListFindList(GroupList, [ address ]);

        if (index == -1)
        {
            if (llToUpper(address) == STRING_SELF)
            {
                CurrentMailAddress = GetSelfAddress();
                llMessageLinked(LINK_THIS, MSG_MESSAGE_REPLY, "Current mail address set to: "
                                + CurrentMailAddress, NULL_KEY);
            }
            else if(ValidMailAddress(address))
            {
                CurrentMailAddress = address;
                llMessageLinked(LINK_THIS, MSG_MESSAGE_REPLY, "Current mail address set to: "
                                + CurrentMailAddress, NULL_KEY);
            }
            else
            {
                llMessageLinked(LINK_THIS, MSG_MESSAGE_REPLY, "Mail adress " + address
                            + " : not found in adress book or invalid format.", NULL_KEY);
            }
        }
        else
        {
            CurrentMailAddress = GetGroupAddressList(address);
            llMessageLinked(LINK_THIS, MSG_MESSAGE_REPLY, "Current mail subject set to: "
                            + CurrentMailAddress, NULL_KEY);
        }
    }
    else
    {
        CurrentMailAddress = llList2String(MailAddressList,index);
        llMessageLinked(LINK_THIS, MSG_MESSAGE_REPLY, "Current mail address set to: "
                        + CurrentMailAddress, NULL_KEY);
    }
}

/////////////////////////////////// SendMail() ///////////////////////

SendMail(string message)
{
    if (CurrentMailAddress == "")
    {
        llMessageLinked(LINK_THIS, MSG_MESSAGE_REPLY, "SendMail: No mail address defined.", NULL_KEY);
    }
    else if (CurrentMailSubject == "")
    {
        llMessageLinked(LINK_THIS, MSG_MESSAGE_REPLY, "SendMail: No subject defined.", NULL_KEY);
    }
    else
    {
        list mailaddresslist=llCSV2List(CurrentMailAddress);
        integer num=llGetListLength(mailaddresslist);
        integer i;
        string address;

        for (i = 0; i < num; ++i)
        {
            address=llList2String(mailaddresslist,i);
            llEmail(address, CurrentMailSubject, message);
        }
    }
}

/////////////////////////////////// SendMailHome() ////////////////////

SendMailHome(string message, string subject)
{
    integer index=llListFindList(AddressBookList, [ STRING_HOME ]);

    if (index == -1)
    {
        llMessageLinked(LINK_THIS, MSG_MESSAGE_REPLY, STRING_HOME
                + " not set. Set your home adress with @HOME .", NULL_KEY);
    }
    else
    {
        string homeaddress=llList2String(AddressBookList,index);
        list   homelist=llCSV2List(homeaddress);
        integer num=llGetListLength(homelist);
        integer i;
        string address;

        for (i = 0; i < num; ++i)
        {
            address=llList2String(homelist,i);
            llEmail(address, subject, message);
        }
    }
}

/////////////////////////////////// GetHomeAddress() //////////////////

string GetHomeAddress()
{
    integer index=llListFindList(AddressBookList, [ STRING_HOME ]);

    if (index == -1)
    {
        return "not set";
    }
    else
    {
        return llList2String(MailAddressList,index);
    }
}

/////////////////////////////////// SetHomeAddress() //////////////////

SetHomeAddress(string address)
{
    integer index=llListFindList(AddressBookList, [ STRING_HOME ]);

    if (index == -1)
    {
        AddressBookList     = (AddressBookList=[]) + [ STRING_HOME ] + AddressBookList;
        MailAddressList     = (MailAddressList=[]) + [ GetAndCheckAddressStr(address) ]  + MailAddressList;
    }
    else
    {
        MailAddressList = llListReplaceList(MailAddressList, [ GetAndCheckAddressStr(address) ], index, index);
    }
}

////////////////////////////////////
// default
////////////////////////////////////

default
{
    ///////////////////// state_entry() //////////////////

    state_entry()
    {
        Line=0;
        Section=0;
        llSetTimerEvent(TIMEOUT_INTERVAL);
        reqAddressBook=llGetNotecardLine(ADDRESSBOOK_NOTECARD, 0);
    }

    ///////////////////// dataserver() ////////////////////

    dataserver(key id, string data)
    {
        if (id == reqAddressBook)
        {
            reqAddressBook = NULL_KEY;

            if (data != EOF)
            {
                ProcessLine(data);
                reqAddressBook=llGetNotecardLine(ADDRESSBOOK_NOTECARD, ++Line);
            }
            else
            {
                llMessageLinked(LINK_THIS, MSG_ADDRESSBOOK_LOADED, "", NULL_KEY);
                llMessageLinked(LINK_THIS, MSG_MESSAGE_REPLY, "Address Book loaded.", NULL_KEY);
                state running;
            }
        }
    }

    //////////////////////// timer() ///////////////////////////

    timer()
    {
        llMessageLinked(LINK_THIS, MSG_ADDRESSBOOK_ERROR, "", NULL_KEY);
        llMessageLinked(LINK_THIS, MSG_MESSAGE_REPLY, "Could not read Address Book: "
                            + ADDRESSBOOK_NOTECARD + ".", NULL_KEY);
        llSetTimerEvent(0.0);
    }
}

////////////////////////////////////////////
// state running
////////////////////////////////////////////

state running
{
    state_entry()
    {
        llMessageLinked(LINK_THIS, MSG_ADDRESSBOOK_LOADED, "", NULL_KEY);
    }

    ///////////////////////// link_message() ////////////////////

    link_message(integer sender, integer msgid, string message, key id)
    {
        if (msgid == MSG_MESSAGE_GETSUBJECT)
        {
            if (CurrentMailSubject == "")
            {
                llMessageLinked(LINK_THIS, MSG_MESSAGE_REPLY, "Current mail subject is empty.", NULL_KEY);
            }
            else
            {
                llMessageLinked(LINK_THIS, MSG_MESSAGE_REPLY, "Current mail subject is: "
                            + CurrentMailSubject, NULL_KEY);
            }
        }
        else if (msgid == MSG_MESSAGE_SETSUBJECT)
        {
            CurrentMailSubject = message;
            llMessageLinked(LINK_THIS, MSG_MESSAGE_REPLY, "Current mail subject set to: "
                            + CurrentMailSubject, NULL_KEY);
        }
        else if (msgid == MSG_MESSAGE_GETADDRESS)
        {
            if (CurrentMailAddress == "")
            {
                llMessageLinked(LINK_THIS, MSG_MESSAGE_REPLY, "Current mail address is empty.", NULL_KEY);
            }
            else
            {
                llMessageLinked(LINK_THIS, MSG_MESSAGE_REPLY, "Current mail address is: "
                            + CurrentMailAddress, NULL_KEY);
            }
        }
        else if (msgid == MSG_MESSAGE_SETADDRESS)
        {
            SetMailAddress(message);
        }
        else if (msgid == MSG_MESSAGE_SEND)
        {
            if (message == "")
            {
                llMessageLinked(LINK_THIS, MSG_MESSAGE_REPLY, "Body of message to send is empty. "
                                +  "No mail is send.", NULL_KEY);
            }
            else
            {
                SendMail(message);
            }
        }
        else if (msgid == MSG_MESSAGE_SENDHOME)
        {
            SendMailHome(message, (string)id);
        }
        else if (msgid == MSG_MESSAGE_SEND_NOTECARD)
        {
            if (llGetInventoryType(message) == INVENTORY_NOTECARD)
            {
                Notecard2Fetch = message;
                llMessageLinked(LINK_THIS, MSG_NOTECARD_READ, message, NULL_KEY);
            }
            else
            {
                llMessageLinked(LINK_THIS, MSG_MESSAGE_REPLY, "Notecard " + message + " not found.", NULL_KEY);
            }
        }
        else if (msgid == MSG_NOTECARD_FETCHED)
        {
            if (message == "")
            {
                llMessageLinked(LINK_THIS, MSG_MESSAGE_REPLY, "Notecard " + Notecard2Fetch
                            + " was empty or could not be read.", NULL_KEY);
            }
            else
            {
                SendMail(message);
            }
        }
        else if (msgid == MSG_MESSAGE_GETHOME)
        {
            llMessageLinked(LINK_THIS, MSG_MESSAGE_REPLY, "Home address is: " + GetHomeAddress() + ".", NULL_KEY);
        }
        else if (msgid == MSG_MESSAGE_SETHOME)
        {
            SetHomeAddress(message);
        }
        else if (msgid == MSG_MESSAGE_INFO)
        {
            Info();
        }
    }
}

/////////////////////////////////////
// End SL Mail AddressBook V1.2.lsl
/////////////////////////////////////
```

## Script: SL Mail FetchNotecard V1.2

Fetch the contents of a notecard and return it via link message as a string.

```lsl
// SL Mail FetchNotecard V1.2.lsl
//
//

// Notecard

integer Line=0;
string  Notecard2Fetch="";
key     reqNotecard=NULL_KEY;
float   TIMEOUT_INTERVAL=10.0;
integer Fetched=FALSE;

// Lines

list LineList=[];

// Link messages

integer MSG_NOTECARD_READ               = 100000;
integer MSG_NOTECARD_FETCHED            = 100100;

///////////////////////////////////////////
// default
//////////////////////////////////////////

default
{
    /////////////////////// dataserver() //////////////////////////////

    dataserver(key id, string data)
    {
        if (id == reqNotecard)
        {
            reqNotecard=NULL_KEY;

            if (data != EOF)
            {
                LineList = (LineList=[]) + LineList + [ data ];
                reqNotecard = llGetNotecardLine(Notecard2Fetch, ++Line);
            }
            else
            {
                Fetched=TRUE;
                llMessageLinked(LINK_THIS, MSG_NOTECARD_FETCHED, llDumpList2String(LineList, "\n"), NULL_KEY);
                llSetTimerEvent(0.0);
            }
        }
    }

    /////////////////////// timer() ///////////////////////////////////

    timer()
    {
        if (!Fetched)
        {
            llMessageLinked(LINK_THIS, MSG_NOTECARD_FETCHED, "", NULL_KEY);
            llSetTimerEvent(0.0);
        }
    }

    /////////////////////// link_message() ////////////////////////////

    link_message(integer send, integer msgid, string message, key id)
    {
        if (msgid == MSG_NOTECARD_READ)
        {
            Line=0;
            Notecard2Fetch=message;
            LineList=[];
            Fetched=FALSE;
            reqNotecard=llGetNotecardLine(Notecard2Fetch, Line);
            llSetTimerEvent(TIMEOUT_INTERVAL);
        }
    }
}

// End SL Mail FetchNotecard V1.2.lsl
```

## Script: SL OnlineStatus V1.2

Fetch online status of owner.

```lsl
// SL Mail OnlineStatus V1.2.lsl
//
//

// Online status

key     reqOnlineStatus=NULL_KEY;
float   STATUS_INTERVAL=2.0;

// Link messages

integer MSG_STATUS_ONLINE       = 30000;
integer MS_STATUS_OFFLINE       = 30100;

////////////////////////////////
// default
////////////////////////////////

default
{
    ///////////////////////// state_entry() /////////////////////////

    state_entry()
    {
        reqOnlineStatus=llRequestAgentData(llGetOwner(), DATA_ONLINE);
        llSetTimerEvent(STATUS_INTERVAL);
    }

    ///////////////////////// dataserver() //////////////////////////

    dataserver(key id, string data)
    {
        if (id == reqOnlineStatus)
        {
            reqOnlineStatus = NULL_KEY;

            if (data=="1")
            {
                llMessageLinked(LINK_THIS, MSG_STATUS_ONLINE, "", NULL_KEY);
            }
            else if (data=="0")
            {
                llMessageLinked(LINK_THIS, MS_STATUS_OFFLINE, "", NULL_KEY);
            }
        }
    }

    ///////////////////////// timer() ///////////////////////////////

    timer()
    {
        reqOnlineStatus = llRequestAgentData(llGetOwner(), DATA_ONLINE);
    }
}

// End SL Mail OnlineStatus V1.2.lsl
```

## Script: SL Mail Help V1.2

Display help information.

```lsl
// SL Mail Help V1.2.lsl
//
//

integer MSG_HELP    = 10000;

///////////////////////////////// Help() ///////////////////////////////////////

Help()
{
    llOwnerSay("HELP for SL Mail V1.2.");
    llOwnerSay("COMMANDS:");
    llOwnerSay("@HELP               - displays help info.");
    llOwnerSay("@INFO               - display mailaddress of this object.");
    llOwnerSay("@RECORD             - start recording.");
    llOwnerSay("@CONTINUE           - continue recording.");
    llOwnerSay("@STOP               - stop recording.");
    llOwnerSay("@IGNORE             - ignore the recording.");
    llOwnerSay("@SHOW               - show what your recorded.");
    llOwnerSay("@SEND               - send the recording.");
    llOwnerSay("@MAIL   - set the mail adress.");
    llOwnerSay("@SUBJECT subject    - set the mail subject.");
    llOwnerSay("@LIST               - list messages in mail buffer.");
    llOwnerSay("@SELECT    - select message from mail buffer.");
    llOwnerSay("@READ               - read current message from mail buffer.");
    llOwnerSay("@NEXT               - read next message from mail buffer.");
    llOwnerSay("@PREV               - read previous message from mail buffer.");
    llOwnerSay("@FIRST              - read first message from mail buffer.");
    llOwnerSay("@LAST               - read last message from mail buffer.");
    llOwnerSay("@DELETE             - delete current message from mail buffer.");
    llOwnerSay("@CLEAR              - clear the mail buffer.");
    llOwnerSay("@REPLY              - reply to current message.");
    llOwnerSay("@RESET              - reset the script.");
    llOwnerSay("@HOME               - set the home mail adress.");
    llOwnerSay("@OFF                - switch mailbox OFF.");
    llOwnerSay("@ON                 - switch mailbox ON.");
}

/////////////////////////////////////////////
// default
/////////////////////////////////////////////

default
{
    link_message(integer sender, integer msgid, string message, key id)
    {
        if (msgid == MSG_HELP)
        {
            Help();
        }
    }
}

// End SL Mail Help V1.2.lsl
```