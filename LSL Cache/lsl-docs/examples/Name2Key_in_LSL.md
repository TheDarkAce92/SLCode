---
name: "Name2Key in LSL"
category: "example"
type: "example"
language: "LSL"
description: "Still missing Name2Key functions in your code? Still relying on external databases that are not always up to date with latest SL subscribers?"
wiki_url: "https://wiki.secondlife.com/wiki/Name2Key_in_LSL"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

## Name2Key

Still missing Name2Key functions in your code? Still relying on external databases that are not always up to date with latest SL subscribers?

Well now you can solve this by yourself, within your LSL script! All you have to do is to rely on LL Search engine!

I put a kind of "library" and a sample of usage for your convenience

Takat Su: I placed an alternate implementation up that does not depend on the babelfish proxy nor having your own proxy here: User:Takat Su/Name2Key

## Library

```lsl
integer SERVICE_NAME2KEY     = 19790;
integer SERVICE_NAME2KEY_RET = 19791;

string proxy     = "http://66.196.80.202/babelfish/translate_url_content?&intl=us&lp=ko_en&trurl=";
string search    = "http://vwrsearch.secondlife.com/client_search.php?session=00000000-0000-0000-0000-000000000000&q=";
string result    = "secondlife:///app/agent/";
string profile   = "Resident profile";
string notfound  = "There were no matches for ";

list    requests;

default
{
    on_rez(integer i) { llResetScript(); }

    state_entry()
    {
        requests = [];
    }

    link_message(integer s, integer n, string m, key i)
    {
        if (n == SERVICE_NAME2KEY) {
            if(llListFindList(requests,[m]) == -1) {
                list Args=llParseString2List(m, [" "], []);

                string FirstName = llList2String(Args, 0);
                string LastName = llList2String(Args, 1);

                string url = proxy+llEscapeURL(search)+FirstName+"%2520"+LastName;;
                key id = llHTTPRequest(url, [], "");
                requests += [id,m];
            }
        }
    }

    http_response(key request_id, integer status, list metadata, string body)
    {
        integer p = llListFindList(requests,[request_id]);
        if (p != -1) {
            string name = llList2String(requests,p+1);
            integer find = llSubStringIndex(body,result);
            if(find == -1) {
                find = llSubStringIndex(body,notfound);
                if(find == -1)
                    llMessageLinked(LINK_SET,SERVICE_NAME2KEY_RET,"Error with lookup!",NULL_KEY);
                else
                    llMessageLinked(LINK_SET,SERVICE_NAME2KEY_RET,name+" not found.",NULL_KEY);
            }
            else
            {
                find += llStringLength(result);
                string avKey = llGetSubString(body,find,find+35);
                integer namePos = llSubStringIndex(body,profile)+17;
                string foundName = llGetSubString(body, namePos+1,
                    namePos + llSubStringIndex(llGetSubString(body,namePos+1, llStringLength(body)-1),"<"));
                if(llToLower(name) == llToLower(foundName))
                    llMessageLinked(LINK_SET,SERVICE_NAME2KEY_RET,foundName,(key)avKey);
                else
                    llMessageLinked(LINK_SET,SERVICE_NAME2KEY_RET,name+" failed: Wrong found.",NULL_KEY);
            }
            requests = llDeleteSubList(requests,p,p+1);
        }
    }
}
```



## Usage sample

```lsl
integer SERVICE_NAME2KEY        =   19790;
integer SERVICE_NAME2KEY_RET    =   19791;

default
{
    on_rez(integer i) { llResetScript(); }

    state_entry()
    {
        llListen(1, "", "", "");
    }

    listen(integer c, string n, key i, string m)
    {
        llSay(0,"Requesting key for "+m);
        llMessageLinked(LINK_THIS, SERVICE_NAME2KEY, m, "");
    }

    link_message(integer f, integer n, string s, key i)
    {
        if(n == SERVICE_NAME2KEY_RET) {
            if(i == NULL_KEY)
                llSay(0,"Lookup failed.  Returned: "+s);
            else
                llSay(0,s+": "+(string)i);
        }
    }
}
```



## Comments

Hope this helps !
Maeva Anatine

EDIT : Looks like the Lindens have either broken or blocked this function. It works from my browser, however from LSL I get an error page containing this message "Access control configuration prevents your request from
being allowed at this time.  Please contact your service provider if
you feel this is incorrect." - Darling Brody.

EDIT : Yes you're right Darling. It seems they've blocked this access from within the world... I still wonder why, especially as there are some workarounds to this...
Anyway I discovered there is a JIRA issue for this. Please vote for the unblock !
[https://jira.secondlife.com/browse/SVC-3122](https://jira.secondlife.com/browse/SVC-3122)
- Mae

EDIT : OK after having read this article from LL: SearchAPI, it seems proxy usage is allowed. So I modified the upper code in order to go through a proxy machine and it works again :)
- Mae

EDIT: After review, it appears the Yahoo Babelfish proxy you are using above does not return the results expected.  I rewrote this to allow different proxies by a simple configuration.  This now uses Google instead of Babelfish by default.  This does not, however, work for any avatars that do not have a Profile filled out (this is due to a limitation of the Googly proxy we're using here).  I'm researching this and trying to see if there is a better proxy to use.

This version can handle multiple requests at once.  Replies have changed slightly, as the found key is returned in the "key" field instead of the message field.  In addition, failure of any kind results in a NULL_KEY being returned, and status information is returned in the message field. - Sensei Schism

EDIT 2009-Mar-08: Sensei, I reused your version here above and took back BabelFish as Google one is unable to retrieve all links (doesn't recognized correctly the secondlife:/// link). In addition, I made some slight changes as LL recently changed their search engine. This version now works properly.

EDIT 2009-Aug-27: LL changed the search URL from **search**.secondlife.com/client_search.php to **vwrsearch**.secondlife.com/client_search.php
ab Vanmoer

EDIT 2009-Sep-04: The problem with the proxy you have there is that it translates the name as a french name, and if it happens to be a real french word, then the name gets changed to that.  for example the last name of Vella got changed to Calved, so no match was made.  PS. I also found some names had been surrounded by bold tags.  So, since i have a few websites i can run PHP on i got [PHP Web Proxy](http://sourceforge.net/projects/php-proxy/) and point to it.  Also, I used: body = llDumpList2String(llParseStringKeepNulls(body, ["**", "**"], []), ""); to remove the bold tags.
-Spritely Pixel

EDIT 2009-Sep-19: Changed the translation from French to Korean on the theory that there are very few names that contain valid Korean characters, thus the translation should just pass straight through.  Changes were: 1. Change the proxy URL to use ko_en instead of fr_en.  2. Change the profile search string from "Resident profiles" to "Resident profile" (note change from plural to singular) and changed the name offset to account for the (now missing) 's'. Also note that Babel will sometimes return an advertising page instead of the translation.  Thus, you should be prepared to retry the search a few times if you get a page that doesn't make sense.Takat Su

EDIT 2009-Sep-20: Got fed up with the babel translation thing.  Apparently, if you make too many requests, Yahoo throttles you for between 2 and 24 hours.  So I made a relay for the Google appspot engine and replicated this page with the new code here: User:Takat Su/Name2Key Takat Su

Maeva Anatine