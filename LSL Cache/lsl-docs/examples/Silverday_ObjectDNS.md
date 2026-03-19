---
name: "Silverday ObjectDNS"
category: "example"
type: "example"
language: "LSL"
description: "Creating client-/server-applications in secondlife using only the assets available in SL can be quite tiresome. Due to the dynamic nature of the object-data used to identify an object (UUID, LSL-URL), which changes either when a sim is restarted or an object is taken and rezzed again, the reliability of those applications is not very high. The changed contact-information needs to be distributed to all object in the network. To create a reliable communication-network in SecondLife requires outside help. And that is where ObjectDNS-Systems come in. Similar to the Domain-Name-System of the internet an ObjectDNS will provide the adress for a registered handle (domain) on request."
wiki_url: "https://wiki.secondlife.com/wiki/Silverday_ObjectDNS"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 Introduction
- 2 The SilverDay Object DNS Plugin
- 3 Example Scripts
- 4 Frequently Asked Questions

## Introduction

Creating client-/server-applications in secondlife using only the assets available in SL can be quite tiresome. Due to the dynamic nature of the object-data used to identify an object (UUID, LSL-URL), which changes either when a sim is restarted or an object is taken and rezzed again, the reliability of those applications is not very high. The changed contact-information needs to be distributed to all object in the network. To create a reliable communication-network in SecondLife requires outside help. And that is where ObjectDNS-Systems come in. Similar to the Domain-Name-System of the internet an ObjectDNS will provide the adress for a registered handle (domain) on request.

The Silverday ObjectDNS provides several options beyond a simple lookup. To secure domains against unauthorized change, each domain is tied to an avatar. Only objects owned by the domain-owner can change the domain-entry. While usually looking up a domain, does not require any special authentication, you have the option of adding a password, that must be supplied when requesting the information for a domain. Also objects communicating by using http-requests don't even need to request the information seperatly. SilverDay ObjectsDNS offers a redirect-service for domains. Just call [http://www.silverday.net/redirect/yourdomain](http://www.silverday.net/redirect/yourdomain) and your call is redirected to the registered URL including any parameters passed using GET or POST. Of course password-protection is available for this option too.

For more information about this service please visit [SilverDay ObjectDNS](http://www.silverday.net/sqndns). If you want to use the optional Web-Interface, to administrate your domains, you must create an account at the [SilverDay Productions Website](http://www.silverday.net).

## The SilverDay Object DNS Plugin

The API it self is heavily commented with all available options explained:

```lsl
// ************************************************
// SDNDNS-Plugin for SecondLife Objects
// Version: 1.0
// Author:  Till Stirling
//
// Copyright 2010 SilverDay Productions
// ************************************************
// The SDNDNS-Plugin will handle the administration of an
// object's dns-entry at SilverDay ObjectDNS. The entry
// can either be an email-adress for mail based systems or
// an URL. If an URL is used objects can take advantage of
// SQN-redirect, which makes requesting the current real URL
// unnecessary.
//
// To use SDN-redirect register a domain using either this
// plugin or the website http://www.silverday.net. To redirect a
// request to the current URL call the following URL, replacing
// your_domain with your registered domain:
//
// http://www.silverday.net/redirect/your_domain
//
// If your domain is password-protected add ?sqn_pwd=password
// (replace password with the domain's password).
// Parameters passed with the URL either by GET or by POST will
// be passed through using GET (POST-parameters will be converted).
//
// If a domain is not accessed for 30 days either by update or
// lookup will be automatically deleted. For a monthly fee you can
// get an exception from this rule.
//
// Usage: Just drop this plugin into your object. Communication
// with your scripts is done using linkmesssages. The integer of
// the linkmessage indicates the 'channel' the message is sent on,
// the string contains the actual command/message with the different
// parameters delimited by |
//
// Commands are sent on channel 84000, responses are received on
// channel 84001. A rsponse always consists of two parts also
// delimited by |. The first part is always a status-message.
// For a successfully completed action it will always be OK.
// In case of an error the status-message will either be ERROR!
// or NOT FOUND. The second part of the response will either be
// the url for the domain (in case of a lookup) or a description
// of the status-message.
//
// Action: Domain-Registration / -update (domain-owner only)
// Command:  update
// Syntax :  update|domain|url[|password]
// Reply  :  OK|msg
//           ERROR!|msg
// The update-command will either register a domain or update it with
// SQN-DNS. If a password is provided during registration the domain
// can only be looked up or redirected if the password is supplied
// with the request. Passwords can be changed or reset with the
// password-command. Domains not accessed for 30 days will be deleted.
//
// Action: Delete registered domain (domain-owner only)
// Command: delete
// Syntax : delete|handle
// Reply  :  OK|msg
//           ERROR!|msg
//           NOT FOUND|msg
// The delete-command will delete a registered domain from the
// SQN-DNS-database.
//
// Action: lock / unlock registered domain (domain-owner only)
// Command: lock / unlock
// Syntax : lock|handle
//          unlock|handle
// Reply  :  OK|msg
//           ERROR!|msg
//           NOT FOUND|msg
// The delete-command will delete a registered domain from the
// SQN-DNS-database.
//
// Action: set/change of a registered domain (domain-owner only)
// Command: password
// Syntax : password|domain|password
// Reply  :  OK|msg
//           ERROR!|msg
//           NOT FOUND|msg
// To secure a registered domain against unauthorized lookup
// you can set a password. To lookup a password-protected domain
// the correct password must be provided in the call. Setting the
// password to '' (empty string) protection is disabled.
//
// Action: lookup of a registered domain (everybody)
// Command: lookup
// Syntax : lookup|domain[|password]
// Reply  :  OK|url
//           ERROR!|msg
//           NOT FOUND|msg
// The lookup-command will return the current url for the domain. If the
// domain is password-protectd, the correct password must be provided with
// the request, in order for it to succeed.
//

integer cmdChannel = 84000;
integer msgChannel = 84001;
string sqndnsURL = "http://www.silverday.net/odns/";

list validCmd = ["register","password","delete","lookup","lock","unlock"];
key reqID;

default {

    on_rez(integer i) {
        llResetScript();
    }

    link_message(integer sender_num,integer num,string str,key id) {
        if ((num == cmdChannel)) {
            list cmd = llParseString2List(str,["|"],[]);
            string command = llList2String(cmd,0);
            string par1 = llList2String(cmd,1);
            string par2 = llList2String(cmd,2);
            string par3 = llList2String(cmd,3);
            if ((llListFindList(validCmd,[command]) > (-1))) {
                string par = "";
                if ((command == "register")) {
                    (par = ((("update?domain=" + par1) + "&url=") + par2));
                    if ((par3 != "")) (par = ((par + "&password=") + par3));
                }
                else  if ((command == "delete")) {
                    (par = ("delete?domain=" + par1));
                }
                else  if ((command == "lock")) {
                    (par = ("lock?domain=" + par1));
                }
                else  if ((command == "unlock")) {
                    (par = ("unlock?domain=" + par1));
                }
                else  if ((command == "password")) {
                    (par = ((("password?domain=" + par1) + "&password=") + par2));
                }
                else  if ((command == "lookup")) {
                    (par = ("lookup?domain=" + par1));
                    if ((par2 != "")) (par = ((par + "&password=") + par2));
                }
                reqID = llHTTPRequest((sqndnsURL + par),[HTTP_METHOD,"GET",HTTP_MIMETYPE,"text/plain;charset=utf-8"],"");
            }
            else  {
                llMessageLinked(LINK_SET,msgChannel,"ERROR!|Unknown Command!",NULL_KEY);
            }
        }
    }

    http_response(key request_id,integer status,list metadata,string body) {
        if ((request_id == reqID)) {
            llMessageLinked(LINK_SET,msgChannel,body,NULL_KEY);
        }
    }
}
```

## Example Scripts

the following is an example how a server can register/update its domain with the SilverDay ObjectDNS:

```lsl
// Samplescript from http://wiki.secondlife.com/wiki/LSL_http_server/examples
// adapted to make use of the SilverDay Object DNS to make its url persistent.

string url;
integer hits;
integer cmdChannel = 84000;
integer msgChannel = 84001;
string myDomain = "sdndns-test-counter";

setup(){
    llSetObjectName("HTTP Server");
    (url = "");
    llRequestURL();
    (hits = ((integer)llGetObjectDesc()));
    llSetText((((string)hits) + " visitors."),<1,1,0>,1);
}

default {

    state_entry() {
        setup();
    }

    on_rez(integer n) {
        setup();
    }

    changed(integer c) {
        if ((c & ((CHANGED_REGION | CHANGED_REGION_START) | CHANGED_TELEPORT))) {
            setup();
        }
    }

    touch_start(integer n) {
        llSay(0,("My url is: " + url));
    }

    http_request(key id,string method,string body) {
        if ((method == URL_REQUEST_GRANTED)) {
            (url = body);
            llMessageLinked(LINK_THIS,cmdChannel,((("register|" + myDomain) + "|") + url),NULL_KEY);
        }
        else  if ((method == URL_REQUEST_DENIED)) {
            llSay(0,("Something went wrong, no url. " + body));
        }
        else  if ((method == "GET")) {
            (++hits);
            llSetObjectDesc(((string)hits));
            llSetText((((string)hits) + " visitors."),<1,1,0>,1);
            llHTTPResponse(id,200,(("Hello!  You are visitor " + ((string)hits)) + "."));
        }
        else  {
            llHTTPResponse(id,405,"Method unsupported");
        }
    }

    link_message(integer sender_num,integer num,string str,key id) {
        if ((num == msgChannel)) {
            list result = llParseString2List(str,["|"],[]);
            if ((llList2String(result,0) == "OK")) {
                llOwnerSay("Domain successfully registered!!");
            }
            else  {
                llOwnerSay(("the following error occurred: " + llList2String(result,1)));
            }
        }
    }
}
```

This script makes use of the SilverDay ObjectDNS-Redirect (the API-Plugin is not needed for this!):

```lsl
// This script demonstrate the URL-persistence by using the
// redirect-Service of the SilverDay ObjectDNS. This does
// not require the SDNDNS-plugin.

string srvDomain = "sdndns-test-counter";
string sdndns = "http://www.silverday.net/redirect/";
key http;

default {

    state_entry() {
        llOwnerSay("Touch me to contact the server!");
    }

    touch_start(integer num_detected) {
        llOwnerSay("Sending request to server...");
        (http = llHTTPRequest((sdndns + srvDomain),[HTTP_METHOD,"GET"],"test"));
    }

    http_response(key request_id,integer status,list metadata,string body) {
        if ((request_id == http)) {
            llOwnerSay(("Server said: " + body));
        }
    }
}
```

If for some reason you do not want to use the redirect-service, this script shows how to lookup the domain:

```lsl
// This script demonstrates the URL-persistence by looking up the URL
// using the sdndns-plugin

integer cmdChannel = 84000;
integer msgChannel = 84001;
string srvDomain = "sdndns-test-counter";
key http;

default {

    state_entry() {
        llOwnerSay("Touch me to contact the server!");
    }

    touch_start(integer num_detected) {
        llOwnerSay("Sending request to server...");
        llMessageLinked(LINK_THIS,cmdChannel,("lookup|" + srvDomain),NULL_KEY);
    }

    http_response(key request_id,integer status,list metadata,string body) {
        if ((request_id == http)) {
            llOwnerSay(("Server said: " + body));
        }
    }

    link_message(integer sender_num,integer num,string str,key id) {
        if ((num == msgChannel)) {
            list result = llParseString2List(str,["|"],[]);
            if ((llList2String(result,0) == "OK")) {
                llOwnerSay(("Received this url:" + llList2String(result,1)));
                llOwnerSay("Sending request to server...");
                (http = llHTTPRequest(llList2String(result,1),[HTTP_METHOD,"GET"],"test"));
            }
            else  {
                llOwnerSay(("the following error occurred: " + llList2String(result,1)));
            }
        }
    }
}
```

## Frequently Asked Questions

**How much does this thing cost?**
Basically the service is free. However, you are limited to 10,000 requests each month. If you reach the limit, your domain will be deactivated for the rest of the month. If you need more requests per month, or maybe even unlimited requests, please contact Till Stirling.

**Can I see how many requests I have left?**
In the web-interface on our Website you can see an overview over all domains regeistered by objects you own, and how many requests the have left. Eventually I will provide an API-call with that funtionality.

**Do I have to signup at your webpage to use this?**
No you certainly do not have to signup. However, signing up for a free account gives you access to a web-interface, where you can administrate your domains. You can do everything using the webapi.

**Can I sell my products using your system?**
But of course you can! All LSL-scripts come with full permissions. All I ask is that you mention us somewhere (i.e. Powered by SilverDay ObjectDNS). If you feel esp. generous, you can give us a free version of your product. We will maintain a list of objects using our system on our site. If you do not want users to change a domain created by your object through the web-interface, you can write-protect your domain. The user will see the domain, your object registered under his name, but he will not be able to change it (and thus possibly breaking the object).

**When I try to use your example script, it says it can't update it, since I am not the owner of the domain.**
Each domain is tied to the owner of the object that registered that domain. So the domain in the example script is tied to my avatar. Just change the domain to a name of your choice, and you are all set.

**Can my domain contain special characters?**
Yes and no. The system is setup so that it will convert special characters. But I would advise not to use special characters (including space!).

**All of a sudden my domain stopped working!**
This can have several reasons. Most likely you have used all of your available requests for this month. If you require more requests per month, please contact Till Stirling. Another (hopefully rare) reason could be, that if you used our service for illegal or abusive purposes (spamming, etc.), your domain was deactivated by me.

**I still have problems or my question is not listed here!**
Please contact Till Stirling inWorld.

**Can I get the server-side php-scripts?**
Plainly spoken: no. If you make me a convincing offer I might change my mind, though.