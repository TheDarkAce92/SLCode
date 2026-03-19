---
name: "Days in Month"
category: "example"
type: "example"
language: "LSL"
description: "The following script is adaptable for use in any calender system, particularly pertaining to tier collection systems that need to do actual monthly billings, not just 28 day or 30 day billing cycles."
wiki_url: "https://wiki.secondlife.com/wiki/Days_in_Month"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

The following script is adaptable for use in any calender system, particularly pertaining to tier collection systems that need to do actual monthly billings, not just 28 day or 30 day billing cycles.

```lsl
integer GetDaysInMonth(integer month, integer year)
{
    if(month == 2)
        return 28 + !(year % 4) - !(year % 100) + !(year % 400);
    if(month >= 1 && month <= 12)
        return 30 | (month & 1) ^ (month > 7);
    return 0;
}

default
{
    state_entry()
    {
        llSay(0, "Touch to confirm the number of days in the current month!");
    }

    touch_start(integer total_number)
    {
        string  date  = llGetDate();
        list    date_info = llParseString2List(date,["-"],[" "]);
        integer year  = llList2Integer(date_info,0);
        integer month = llList2Integer(date_info,1);
        integer day   = llList2Integer(date_info,2);

        integer days_in_month = GetDaysInMonth(month, year);
        llSay(0, (string)days_in_month + " days in this month");
    }
}
```