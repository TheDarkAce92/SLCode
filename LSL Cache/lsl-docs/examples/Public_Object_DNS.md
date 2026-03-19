---
name: "Public Object DNS"
category: "example"
type: "example"
language: "LSL"
description: "Sadly the URL used on this page returns 404 from Google. The concept is nice and I think we could all use something like it (SL should provide that maybe). Sadly though, these scripts will not work as they are."
wiki_url: "https://wiki.secondlife.com/wiki/Public_Object_DNS"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Sadly the URL used on this page returns 404 from Google. The concept is nice and I think we could all use something like it (SL should provide that maybe). Sadly though, these scripts will not work as they are.

```lsl
 -- myggen
```



Hey all!

We've set up a public object DNS database on GAE.  It's still pretty beta, and the bells and whistles don't work yet, but it is usable.  Until things get more stable and tested, the DB could be wiped without warning (though that is unlikely) and things may be a bit buggy yet, but please give it a try and let me know of any bugs that you find!  IM Liandra Ceawlin in-world or email support@ceawlin.com

Here's the reference interface implementation.  To use it, paste it into your scripts and call objdnsGet and objdnsSet as appropriate.  Examples follow...

```lsl
///////////////////////////////////////////////////////////////////////////////
//
// ObjDNS - Public Object DNS service for SL.
//          Reference interface, Version 5, Fri Jul 24 13:08:32 EDT 2009
//
// Please report bugs to support@ceawlin.com
//
///////////////////////////////////////////////////////////////////////////////
//
// Copyright (c) 2009, Ceawlin Creations
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
//
//     * Redistributions of source code must retain the above copyright notice,
// this list of conditions and the following disclaimer.
//     * Redistributions in binary form must reproduce the above copyright
// notice, this list of conditions and the following disclaimer in the
// documentation and/or other materials provided with the distribution.
//     * Neither the name of Ceawlin Creations, Liandra Ceawlin, nor the names
// of its contributors may be used to endorse or promote products derived from
// this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
// AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
// IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
// ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
// LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
// CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
// SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
// INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
// CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
// ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
// POSSIBILITY OF SUCH DAMAGE.
//
///////////////////////////////////////////////////////////////////////////////

// Although it is possible to register and update domains using POST requests
// from LSL, that exercise it left to the reader at this juncture.  A better
// library implementation will be forthcoming Soon(tm).  This implementation
// does not do any error checking or anything. >_>  Please visit
// http://objdns.appspot.com/ to register and modify your domains.

// Notes on the way it works.
//
//  Each domain has a password associated with it.  This password is used to
// change the domain information later, update/set name records under the
// domain, and to look up private name records under the domain.
//
//  You don't need to put anything in the email field when you create a domain
// if you don't want to.  It'll be used eventually to send out deletion from
// inactivity warnings and to retrieve your domain password if you forget it.
//
//  Each domain can have many names associated with it.  Each name has a URL
// and a privacy setting associated with it.  If it is marked as private, then
// the domain password must be supplied to look up its URL.

// Notes on the service:
//
//  The service currently has a quota of 1.3 million hits per day. This should
// be plenty for beta testing, but if people actually start using the service,
// it may start hitting quota. If that happens, we'll put up a donate-o-meter
// on the site, and allocate donations towards the quota.
//
//  To help avoid hitting quota, please look up a CAPS URL for a remote object
// once, and cache it, then only look it back up again when a message fails
// to go through. Please do not look up CAPS URLs every time you send a
// message, if you can help it, unless your object sends very, very few
// messages.
//
//  There is also a 1 GB database quota. We don't forsee hitting that any time
// soon, but if it happens, we'll allocate donate-o-meter funds towards the DB
// quota as well.
//
//  Quotas are reset daily at 12AM Pacific time.

key     doSimplePost( string url, list options )
{
    string opts = "";
    integer i;
    for( i=0; i<(options!=[]); i+=2 )
    {
        if( i )
            opts += "&";
        opts += llList2String( options, i ) +
                "=" +
                llEscapeURL( llList2String(options,i+1) );
    }
    return llHTTPRequest(
            url,
            [
                HTTP_METHOD, "POST",
                HTTP_MIMETYPE, "application/x-www-form-urlencoded"
            ],
            opts
        );
}

key     objdnsGet( string domain, string password, string name )
{
    return doSimplePost(
                "http://objdns.appspot.com/objdns",
                [
                    "action",       "get",
                    "domain",       domain,
                    "password",     password,
                    "name",         name
                ]
            );
}

key     objdnsSet( string domain, string password, string name, string url, integer privacy )
{
    return doSimplePost(
                "http://objdns.appspot.com/objdns",
                [
                    "action",       "set",
                    "domain",       domain,
                    "password",     password,
                    "name",         name,
                    "url",          url,
                    "privacy",      privacy
                ]
            );
}
```

Here's a pretty crude example implementation of a client-server setup.  Put the server script in a prim in some sim somewhere, then put the client script into an attachment, go to another sim, and click on the attachment.  You should get an IM from the server script confirming that it got a message from your attachment.

Don't forget to paste the API into the top of the scripts.

Server

```lsl
string  DOMAIN      = "Test";
string  PASSWORD    = "test";
string  NAME        = "Foo";
integer PRIVACY     = FALSE;


key qid;

default
{
    state_entry()
    {
        llRequestURL();
    }

    on_rez( integer param )
    {
        llRequestURL();
    }

    changed( integer ch )
    {
        if( ch&CHANGED_REGION||ch&CHANGED_TELEPORT||ch&CHANGED_REGION_START )
            llRequestURL();
    }

    http_request( key id, string method, string body )
    {
        llSay( DEBUG_CHANNEL, "http_request: "+body );
        if( method == URL_REQUEST_GRANTED )
        {
            objdnsSet( DOMAIN, PASSWORD, NAME, body, PRIVACY );
        }
        else if( method == URL_REQUEST_DENIED )
        {
            llSay( DEBUG_CHANNEL, "Error: URL not granted! D:" );
        }
        else
        {
            llInstantMessage( llGetOwner(), "Received: "+body );
            llHTTPResponse( id, 200, "" );
        }
    }
}
```

Client

```lsl
key     qid         = NULL_KEY;
string  server_url  = "";

default
{
    state_entry()
    {
        // Note this will fail if your record is private.
        // Change the "" to PASSWORD to correct that.
        qid = objdnsGet( "Test", "", "Foo" );
    }

    http_response( key id, integer status, list meta, string body )
    {
        llSay( DEBUG_CHANNEL, "http_response: "+body );
        if( id == qid )
        {
            if( llGetSubString(body,0,1) == "OK" )
            {
                body = llDeleteSubString( body, 0, 1 );
                llSay( DEBUG_CHANNEL, "Server URL is: "+body );
                server_url = body;
            }
            else if( llGetSubString(body,0,2) == "ERR" )
            {
                llSay( DEBUG_CHANNEL, "Error: "+llDeleteSubString(body,0,2) );
            }
            else
            {
                llSay( DEBUG_CHANNEL, "Zomg, something bizarre happened. D:" );
            }
        }
        else
        {
            if( status != 200 || !llSubStringIndex(body,"cap not found") )
            {
                // You probably want to cache your messages and resend when
                //  the URL changes, but this code doesn't do that...
                // Alternatively, if you are only sending a message every
                //  few minutes, you could just look up the URL every time.
                llSay( DEBUG_CHANNEL, "Ack, the server URL changed. Looking it up again..." );
                // Note this will fail if your record is private.
                // Change the "" to the domain password to correct that.
                qid = objdnsGet( "Test", "", "Foo" );
            }
        }
    }

    touch_start( integer ndet )
    {
        llOwnerSay( "I'm gonna send a message to the server! :D" );
        if( server_url != "" )
        {
            llHTTPRequest(
                    server_url,
                    [
                        HTTP_METHOD, "POST",
                        HTTP_MIMETYPE, "application/x-www-form-urlencoded"
                    ],
                    "Touched by "+llDetectedName( 0 )
                );
        }
    }
}
```