---
name: "Unix2PST PDT"
category: "example"
type: "example"
language: "LSL"
description: "Returns a string containing the SLT date and time, annotated with PST or PDT as appropriate, corresponding to the given Unix time."
wiki_url: "https://wiki.secondlife.com/wiki/Unix2PST_PDT"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL



## Function: string Unix2PST_PDT(integer unixtime

Returns a string containing the SLT date and time, annotated with PST or PDT as appropriate,  corresponding to the given Unix time.

e.g.       Wed 2013-12-25 06:48 PST

• integer

unixtime

–

a point in time represented by the number of seconds since 00:00 hours, Jan 1, 1970 UTC, e.g. a value returned by llGetUnixTime()

## Specification

```lsl
// Convert Unix Time to SLT, identifying whether it is currently PST or PDT (i.e. Daylight Saving aware)
// Omei Qunhua December 2013

list weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

string Unix2PST_PDT(integer insecs)
{
    string str = Convert(insecs - (3600 * 8) );   // PST is 8 hours behind GMT
    if (llGetSubString(str, -3, -1) == "PDT")     // if the result indicates Daylight Saving Time ...
        str = Convert(insecs - (3600 * 7) );      // ... Recompute at 1 hour later
    return str;
}

// This leap year test is correct for all years from 1901 to 2099 and hence is quite adequate for Unix Time computations
integer LeapYear(integer year)
{
    return !(year & 3);
}

integer DaysPerMonth(integer year, integer month)
{
    if (month == 2)      return 28 + LeapYear(year);
    return 30 + ( (month + (month > 7) ) & 1);           // Odd months up to July, and even months after July, have 31 days
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

    integer LastSunday = days - DayOfWeek;
    string PST_PDT = " PST";                  // start by assuming Pacific Standard Time
    // Up to 2006, PDT is from the first Sunday in April to the last Sunday in October
    // After 2006, PDT is from the 2nd Sunday in March to the first Sunday in November
    if (years > 2006 && month == 3  && LastSunday >  7)     PST_PDT = " PDT";
    if (month > 3)                                          PST_PDT = " PDT";
    if (month > 10)                                         PST_PDT = " PST";
    if (years < 2007 && month == 10 && LastSunday > 24)     PST_PDT = " PST";
    return (llList2String(weekdays, DayOfWeek) + " " + str + PST_PDT);
}
```

## Example

```lsl
default
{
    state_entry()
    {
        llOwnerSay( Unix2PST_PDT (llGetUnixTime() ) );
    }
}
```