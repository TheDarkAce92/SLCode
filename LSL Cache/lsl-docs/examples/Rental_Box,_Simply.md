---
name: "Rental Box, Simply"
category: "example"
type: "example"
language: "LSL"
description: "// warn_owner=0; // only sends messages when rent is overdue integer warn_owner=1; // sends all warnings to admin as well as renter"
wiki_url: "https://wiki.secondlife.com/wiki/RentalBoxv1"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

```lsl
// Configure here:
float linden_per_day=4800.0;
float warning_1_daysleft = 1.000;
float warning_2_daysleft = 3.000;
string warning_1 = "Warning, rent is up in 1 day";
string warning_2 = "Warning, rent is up in 3 days";

// warn_owner=0; // only sends messages when rent is overdue
integer warn_owner=1; // sends all warnings to admin as well as renter

// Below this is the script
integer mystat=0;
string timetil;
list times;
float days_left=0.0;
integer last_time;
key renter;
string renter_name;

string hexc="0123456789ABCDEF";//faster
string float2str(float input)//Doubles Unsupported, LSO Safe, Mono Safe
{//Float2Hex Copyright Strife Onizuka, 2006-2007, LGPL, http://www.gnu.org/copyleft/lesser.html or (cc-by) http://creativecommons.org/licenses/by/3.0/
    if(input != (integer)input)//LL screwed up hex integers support in rotation & vector string typecasting
    {
        float unsigned = llFabs(input);//logs don't work on negatives.
        integer exponent = llFloor((llLog(unsigned) / 0.69314718055994530941723212145818));//floor(log2(b)) + rounding error

        integer mantissa = (integer)((unsigned / (float)("0x1p"+(string)(exponent -= ((exponent >> 31) | 1)))) * 0x4000000);//shift up into integer range
        integer index = (integer)(llLog(mantissa & -mantissa) / 0.69314718055994530941723212145818);//index of first 'on' bit
        string str = "p" + (string)(exponent + index - 26);
        mantissa = mantissa >> index;
        do
            str = llGetSubString(hexc, 15 & mantissa, 15 & mantissa) + str;
        while(mantissa = mantissa >> 4);

        if(input < 0)
            return "-0x" + str;
        return "0x" + str;
    }//integers pack well so anything that qualifies as an integer we dump as such, supports negative zero
    return llDeleteSubString((string)input,-7,-1);//trim off the float portion, return an integer
}

default
{
    state_entry()
    {
        mystat=1;
        llSetText("Rental Script v1", <0,1,0>, 1.0 );
        if( llGetStatus( STATUS_PHYSICS ) == TRUE ) {
            mystat=0;
            days_left = 0.0;
            last_time = llGetUnixTime();
        } else {
            list lStatus = llParseString2List( llGetObjectDesc(), ["~"], [] );
            days_left = llList2Float(lStatus,0);
            last_time = llList2Integer(lStatus,1);
            renter = llList2Key(lStatus,2);

            if( days_left <= 0.0 || last_time <= 0 ) {
                mystat=0;
                days_left = 0.0;
                last_time = llGetUnixTime();
            }
        }

        llSetTimerEvent(0.5);
    }

    timer()
    {
        if( mystat == 0 ) return;
        days_left -= ((float)(last_time=llGetUnixTime())-(float)last_time)/86400.0;
        llSetObjectDesc( float2str(days_left) + "~" + (string)last_time + "~" + (string)renter );
        if( days_left <= 0.0 ) {
            llInstantMessage( llGetOwner(), "Rent is overdue" );
            days_left = 0.0;
            llSetText("Expired", <1,0,0>, 1.0);
            mystat=0;
            return;
        } else if( mystat<3 && days_left <= warning_1_daysleft ) {
            if( warn_owner ) {
                llInstantMessage( llGetOwner(), warning_1 );
            }
            llInstantMessage( renter, warning_1 );
            mystat=3;
        } else if( mystat<2 && days_left <= warning_2_daysleft ) {
            if( warn_owner ) {
                llInstantMessage( llGetOwner(), warning_2 );
            }
            llInstantMessage( renter, warning_2 );
            mystat=2;
        }

        integer daysleft = (integer) llFloor(days_left);
        float hoursleft = 24.0*(days_left-(float)daysleft);

        llSetText(renter_name + ": " + (string)daysleft + " days, " + (string)hoursleft + " hours", <1,1,1>, 0.5);
    }

    money(key giver, integer amt)
    {
        if( mystat == 0 ) {
            renter=giver;
            list lDet = llGetObjectDetails( renter, [ OBJECT_NAME ] );
            renter_name = llList2String(lDet,0);

            llSay(0, "renter is " + renter_name);
            mystat=1;
        }
        llSay(0, "Pushed clock back " + (string)((float)amt/linden_per_day) + " days");
        days_left += (float)amt/linden_per_day;
    }
}
```