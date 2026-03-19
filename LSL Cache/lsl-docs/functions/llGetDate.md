---
name: "llGetDate"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a string that is the current date in the UTC time zone in the format 'YYYY-MM-DD'.

If you wish to know the time as well use: llGetTimestamp which uses the format'
signature: "string llGetDate()"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetDate'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetdate"]
---

Returns a string that is the current date in the UTC time zone in the format "YYYY-MM-DD".

If you wish to know the time as well use: llGetTimestamp which uses the format


## Signature

```lsl
string llGetDate();
```


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetDate)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetDate) — scraped 2026-03-18_

Returns a string that is the current date in the UTC time zone in the format "YYYY-MM-DD".

## Examples

```lsl
// Birthday surprise
default
{
    state_entry()
    {
        llSetTimerEvent(0.1);
    }

    timer()
    {
        if(llGetDate() == "2009-02-15")
            llSetText("HAPPY BIRTHDAY!", <0,1,0>, 1.0);
        else
            llSetText("A surprise is coming...", <0,1,0>, 1.0);

        llSetTimerEvent(3600.0);  // check every hour.
    }
}
```

```lsl
// Function to calculate the numeric day of year
integer dayOfYear(integer year, integer month, integer day)
{
    return day + (month - 1) * 30 + (((month > 8) + month) / 2)
        - ((1 + (((!(year % 4)) ^ (!(year % 100)) ^ (!(year % 400))) | (year <= 1582))) && (month > 2));
}

default
{
    touch_end(integer count)
    {
        list dateComponents = llParseString2List(llGetDate(), ["-"], []);
        integer year  = (integer) llList2String(dateComponents, 0);
        integer month = (integer) llList2String(dateComponents, 1);
        integer day   = (integer) llList2String(dateComponents, 2);
        llSay(0, "The current day of the year is " + (string) dayOfYear(year, month, day));
    }
}
```

```lsl
// Function to calculate whether a current year is a leap year

integer is_leap_year( integer year )
{
    if( year % 4 )         return FALSE;   // Not a leap year under any circumstances
    if( year <= 1582 )     return TRUE;    // In the Julian calender before 24 February 1582, every fourth year was a leap year
    if( !( year % 400 ))   return TRUE;    // A leap century is a leap year if divisible by 400
    if( !( year % 100 ))   return FALSE;   // Any other century is not a leap year
    return TRUE;                           // It is divisible by 4 and not a century and not Julian, therefore it is a leap year
}
```

The previous script is way unnecessary for Avatar age, SL sales history etc. Here is all that is needed for 99% of SL applications.

This code is in fact valid for all years from 1901 to 2099, as 2000 was a leap year.

```lsl
    if (year % 4)          //  TRUE if NOT a leap year
```

## See Also

### Functions

- **llGetTimestamp** — Same format but with the time.

### Articles

- ISO 8601

<!-- /wiki-source -->
