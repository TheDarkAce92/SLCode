---
name: "Google_Translator"
category: "example"
type: "example"
language: "LSL"
description: "Google Translator by Ugleh Ulrik"
wiki_url: "https://wiki.secondlife.com/wiki/Google_Translator"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Google Translator by Ugleh Ulrik

Google Translator keeps their translated data in a Array. You can see this by looking at the HTTPRequests.

The URL is this

[http://translate.google.com/translate_a/t?client=t&text=words](http://translate.google.com/translate_a/t?client=t&text=words) here&hl=en&sl=es

This will make it go from Spanish to English. Then all you need to do is do a string replacement.



```lsl
key http_request_id;
string transtring = "";
string nothing = "";
string name;
string somestring;
string strReplace(string str, string search, string replace) {
    return llDumpList2String(llParseStringKeepNulls((str = "") + str, [search], []), replace);
}
default
{
    state_entry()
    {
        llListen(0, "", NULL_KEY, "");
    }

    http_response(key request_id, integer status, list metadata, string body)
    {
        if (request_id == http_request_id)
        {
            list trans1 = llParseString2List(body, ["\"orig\""], []);
            transtring = strReplace(llList2String(trans1,0), "{\"sentences\":[{\"trans\":\"", "");
            nothing = strReplace(transtring, "\",", "");
            nothing = strReplace(nothing, ",", "");
            nothing =  strReplace(nothing, "\\" + "\"", "\"");
            if (somestring != nothing){
            llSay(0, nothing);
        }
            llSetObjectName("es2en Translator");
        }
    }
     listen(integer channel, string name, key id, string message)
    {
        somestring = message;
         if (name == llKey2Name(llGetOwner())){
        transtring =  llEscapeURL(message);
         http_request_id = llHTTPRequest("http://translate.google.com/translate_a/t?client=t&text=" + transtring + "&hl=en&sl=es&tl=en&pc=0", [], "");
    llSetObjectName(name);
    }
    }


}
```