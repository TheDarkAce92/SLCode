---
name: "Unix2GMTorBST"
category: "example"
type: "example"
language: "LSL"
description: "Convert a Unix time (time in seconds since 01-01-1970) to a date in the form Day-of-week + YYYY-MM-DD HH:MM + GMT or BST"
wiki_url: "https://wiki.secondlife.com/wiki/Unix2GMTorBST"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL



## Function: string Unix2GMTorBST(integer unixtime

Convert a Unix time (time in seconds since 01-01-1970) to a date in the form  Day-of-week + YYYY-MM-DD HH:MM + GMT or BST

Day-of-week will be a 3-letter day, and the string ends with "GMT" or "BST" as appropriate, with correct 1-hour adjustment for BST

e.g.       Wed 2013-12-25 06:48 GMT

• integer

unixtime

–

a point in time represented by the number of seconds since 00:00 hours, Jan 1, 1970 UTC, e.g. a value returned by llGetUnixTime()

For a version giving output as PDT/PST see [http://wiki.secondlife.com/wiki/Unix2PST_PDT](http://wiki.secondlife.com/wiki/Unix2PST_PDT)

## Specification

```lsl
// Omei Qunhua  Jan 2013

list weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

// Convert a Unix time in seconds to Day-of-week + YYYY-MM-DD HH:MM + GMT or BST
string Unix2GMTorBST(integer insecs)
{
    string str = Convert(insecs);
    if (llGetSubString(str, -3, -1) == "BST")   // if the result indicates BST ...
        str = Convert(insecs + 3600);            // ... Recompute at 1 hour later
    return str;
}

// This leap year test is correct for all years from 1901 to 2099 and hence is quite adequate for Unix Time computations
integer LeapYear(integer year)
{
    return !(year & 3);
}

integer DaysPerMonth(integer year, integer month)
{
    if (month == 2)  	return 28 + LeapYear(year);
    return 30 + ( (month + (month > 7) ) & 1);   		// Odd months up to July, and even months after July, have 31 days
}

string Convert(integer insecs)
{
    integer w; integer month; integer daysinyear;
    integer mins = insecs / 60;
    integer secs = insecs % 60;
    integer hours = mins / 60;
    mins = mins % 60;
    integer days = hours / 24;
    hours = hours % 24;
    integer DayOfWeek = (days + 4) % 7;    // 0=Sun thru 6=Sat

    integer years = 1970 +  4 * (days / 1461);
    days = days % 1461;                  // number of days into a 4-year cycle

    @loop;
    daysinyear = 365 + LeapYear(years);
    if (days >= daysinyear)
    {
	days -= daysinyear;
	++years;
	jump loop;
    }
    ++days;

    for (w = month = 0; days > w; )
    {
	days -= w;
	w = DaysPerMonth(years, ++month);
    }

    string str =  ((string) years + "-" + llGetSubString ("0" + (string) month, -2, -1) + "-" + llGetSubString ("0" + (string) days, -2, -1) + " " +
	llGetSubString ("0" + (string) hours, -2, -1) + ":" + llGetSubString ("0" + (string) mins, -2, -1) );

    string GMT_BST = " GMT";
    integer LastSunday = days - DayOfWeek;
    // BST is from the last Sunday in March to the last Sunday in October
    if (month == 3  && LastSunday > 24)     GMT_BST = " BST";
    if (month > 3)                          GMT_BST = " BST";
    if (month == 10 && LastSunday > 24)     GMT_BST = " GMT";
    if (month > 10)                         GMT_BST = " GMT";
    return (llList2String(weekdays, DayOfWeek) + " " + str + GMT_BST);
}
```

## Example

```lsl
default
{
    state_entry()
    {
	llSay(0, Unix2GMTorBST(llGetUnixTime() ) );
    }
}
```