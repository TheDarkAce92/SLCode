---
name: "Date Library"
category: "example"
type: "example"
language: "LSL"
description: "These two function are directly translated from Gary Katch web site : [[1]]. I however had to make some modifications."
wiki_url: "https://wiki.secondlife.com/wiki/Date_Library"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL

These two function are directly translated from Gary Katch web site : [[[1]](http://alcor.concordia.ca/~gpkatch/)].
I however had to make some modifications.

1 - I translated from C, to LSL. This was not too hard; I merely had to replace int by integer and a few more syntax differences.

2 - I had to make the functions 32 compatible. The original function uses 64 bits integers but Second Life supports only 32 bits

When the line " y = (10000*g + 14780)/3652425 " was run it was going over the 32 bits.
I solved this issue by applying and offset of 1600 years. So rather than working with the number of days since March 1st 0001, the functions origin is March 1st 1600.
According to my test the functions work at least from 1600 to 2181.

3 - I added a couple of helper function.

The function gday given integer y, m, d, calculate day number g.

```lsl
integer gday(integer yy, integer mm, integer dd)
{
    // convert date to day number
    integer m = (mm + 9)%12; // mar=0, feb=11
    integer y = yy - 1600 - m/10;   // if Jan/Feb, year--
    return y*365 + y/4 - y/100 + y/400 + (m*306 + 5)/10 + (dd - 1);
}
```

This function does the exact opposite. Given a day number d, it returns a list containing [ year, month, day]

```lsl
list sdate(integer d)
{
    // convert day number to y,m,d format
    integer y = (10000*d + 14780)/3652425;
    integer ddd = d - (y*365 + y/4 - y/100 + y/400);
    if (ddd < 0) {
        y--;
        ddd = d - (y*365 + y/4 - y/100 + y/400);
    }
    integer mi = (52 + 100*ddd)/3060;
    integer dd = ddd - (mi*306 + 5)/10 + 1;
    return [
        1600 + y + (mi + 2)/12,
        (mi + 2)%12 + 1,
        dd];
}
```

Today

```lsl
integer today()
{
    string DateUTC = llGetDate();
    integer year = (integer)llGetSubString(DateUTC, 0, 3);
    integer month = (integer)llGetSubString(DateUTC, 5, 6);
    integer day = (integer)llGetSubString(DateUTC, 8, 9);
    return gday(year,month,day);
}
```

Date differences.
The difference in days between two dates:

```lsl
return gday(y2,m2,d2) - gday(y1,m1,d1);
```

Day offsets.
The date n days from y,m,d:

```lsl
  sdate(gday(y,m,d) + n)
```

Date legality.
To check if a date is on the calendar:

```lsl
integer isLegal(integer yy, integer mm, integer dd)
{
    list dt=sdate(gday(yy,mm,dd));
    return
        llList2Integer(dt,0)==yy
        && llList2Integer(dt,1)==mm
        && llList2Integer(dt,2)==dd;
}
```

Those functions are straight forward formatting function.
They can be adapted for the different languages and date format.

```lsl
list weekDays=["Sun","Mon","Tue","Wed","Thu","Fri","Sat"];

string weekDay(integer g)
{
    return llList2String(weekDays,(g + 3) % 7);
}

list months=["","January","February","March",
    "April","May","June",
    "July","August","September",
    "October","November","December"];

string fullDate(integer g)
{
    list dt = sdate(g);
    string nth;
    integer dd = llList2Integer(dt,2); // day
    if (dd>=10 && dd<=20) nth="th";
    else {
        dd = dd % 10;
        if (dd==1) nth="st";
        else if (dd==2) nth="nd";
        else if (dd==3) nth="rd";
        else nth="th";
    }
    return weekDay(g)
        + " "
        + llList2String(months,llList2Integer(dt,1))
        + " "
        + (string) llList2Integer(dt,2) + nth
        + " "
        + (string) llList2Integer(dt,0);
}
```