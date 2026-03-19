---
name: "Unix2DateTime"
category: "example"
type: "example"
language: "LSL"
description: "Returns a list of integers comprising the date [year, month, day, hour, minute, second]."
wiki_url: "https://wiki.secondlife.com/wiki/Unix2DateTime"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL



## Function: list Unix2DateTime(integer unixtime

Returns a list of integers comprising the date [year, month, day, hour, minute, second].

• integer

unixtime

–

number of seconds elapsed since 00:00 hours, Jan 1, 1970 UTC, ie. return value of llGetUnixTime()

## Function: integer DateTime2Unix(integer year

Returns an integer comprising the date in number of seconds elapsed since 00:00 hours, Jan 1, 1970 UTC.

• integer

year

–

range from 1970 to 2038

• integer

month

–

range from 1 to 12

• integer

day

–

range from 1 to 31

• integer

hour

–

range from 0 to 23

• integer

minute

–

range from 0 to 59

• integer

second

–

range from 0 to 59

## Function: string DateString(list time

Returns a string comprising the date as DD-MON-YYYY.

• list

time

–

list of integers [year, month, day, hour, minute, second]

## Function: string TimeString(list time

Returns a string comprising the time as HH24:MI:SS.

• list

time

–

list of integers [year, month, day, hour, minute, second]

## Specification

```lsl
/////////////////////////////////////////////////////////////////////
// Script Library Contribution by Flennan Roffo
// Logic Scripted Products & Script Services
// Peacock Park (183,226,69)
// (c) 2007 - Flennan Roffo
//
// Distributed as GPL, donated to wiki.secondlife.com on 19 sep 2007
//
// SCRIPT:  Unix2DateTimev1.0.lsl
//
// FUNCTION:
// Perform conversion from return value of llGetUnixTime() to
// date and time strings and vice versa.
//
// USAGE:
// list timelist=Unix2DateTime(llGetUnixTime());
// llSay(PUBLIC_CHANNEL, "Date: " +  DateString(timelist); // displays date as DD-MON-YYYY
// llSay(PUBLIC_CHANNEL, "Time: " +  TimeString(timelist); // displays time as HH24:MI:SS
/////////////////////////////////////////////////////////////////////

///////////////////////////// Unix Time conversion //////////////////

integer DAYS_PER_YEAR        = 365;           // Non leap year
integer SECONDS_PER_YEAR     = 31536000;      // Non leap year
integer SECONDS_PER_DAY      = 86400;
integer SECONDS_PER_HOUR     = 3600;
integer SECONDS_PER_MINUTE   = 60;

list MonthNameList = [  "JAN", "FEB", "MAR", "APR", "MAY", "JUN",
                        "JUL", "AUG", "SEP", "OCT", "NOV", "DEC" ];

// This leap year test works for all years from 1901 to 2099 (yes, including 2000)
// Which is more than enough for UnixTime computations, which only operate over the range [1970, 2038].  (Omei Qunhua)
integer LeapYear( integer year)
{
    return !(year & 3);
}

integer DaysPerMonth(integer year, integer month)
{
    // Compact Days-Per-Month algorithm. Omei Qunhua.
    if (month == 2)  	return 28 + LeapYear(year);
    return 30 + ( (month + (month > 7) ) & 1);           // Odd months up to July, and even months after July, have 31 days
}

integer DaysPerYear(integer year)
{
    return 365 + LeapYear(year);
}

///////////////////////////////////////////////////////////////////////////////////////
// Convert Unix time (integer) to a Date and Time string
///////////////////////////////////////////////////////////////////////////////////////

/////////////////////////////// Unix2DataTime() ///////////////////////////////////////

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
    integer days_per_month = DaysPerMonth(year, month);

    while (day > days_per_month)
    {
        day -= days_per_month;

        if (++month > 12)
        {
            ++year;
            month = 1;
        }

        days_per_month = DaysPerMonth(year, month);
    }

    integer seconds_since_midnight  = unixtime % SECONDS_PER_DAY;
    integer hour        = seconds_since_midnight / SECONDS_PER_HOUR;
    integer second      = seconds_since_midnight % SECONDS_PER_HOUR;
    integer minute      = second / SECONDS_PER_MINUTE;
    second              = second % SECONDS_PER_MINUTE;

    return [ year, month, day, hour, minute, second ];
}

///////////////////////////////// MonthName() ////////////////////////////

string MonthName(integer month)
{
    if (month >= 0 && month < 12)
        return llList2String(MonthNameList, month);
    else
        return "";
}

///////////////////////////////// DateString() ///////////////////////////

string DateString(list timelist)
{
    integer year       = llList2Integer(timelist,0);
    integer month      = llList2Integer(timelist,1);
    integer day        = llList2Integer(timelist,2);

    return (string)day + "-" + MonthName(month - 1) + "-" + (string)year;
}

///////////////////////////////// TimeString() ////////////////////////////

string TimeString(list timelist)
{
    string  hourstr     = llGetSubString ( (string) (100 + llList2Integer(timelist, 3) ), -2, -1);
    string  minutestr   = llGetSubString ( (string) (100 + llList2Integer(timelist, 4) ), -2, -1);
    string  secondstr   = llGetSubString ( (string) (100 + llList2Integer(timelist, 5) ), -2, -1);
    return  hourstr + ":" + minutestr + ":" + secondstr;
}

///////////////////////////////////////////////////////////////////////////////
// Convert a date and time to a Unix time integer
///////////////////////////////////////////////////////////////////////////////

////////////////////////// DateTime2Unix() ////////////////////////////////////

integer DateTime2Unix(integer year, integer month, integer day, integer hour, integer minute, integer second)
{
	integer time = 0;
	integer yr = 1970;
	integer mt = 1;
	integer days;

	while(yr < year)
	{
		days = DaysPerYear(yr++);
		time += days * SECONDS_PER_DAY;
	}

	while (mt < month)
	{
		days = DaysPerMonth(year, mt++);
		time += days * SECONDS_PER_DAY;
	}

	days = day - 1;
	time += days * SECONDS_PER_DAY;
	time += hour * SECONDS_PER_HOUR;
	time += minute * SECONDS_PER_MINUTE;
	time += second;

	return time;
}
//////////////////////////////////////////////
// End Unix2DateTimev1.0.lsl
//////////////////////////////////////////////
```

## Example

Trivial example to display data and time converted from system time when touched.

```lsl
default
{
    touch_start(integer total_number)
    {
        llOwnerSay("Date: " +  DateString(Unix2DateTime(llGetUnixTime()))); // displays date as DD-MON-YYYY
        llOwnerSay("Time: " +  TimeString(Unix2DateTime(llGetUnixTime()))); // displays time as HH24:MI:SS
    }
}
```