---
name: "Lame Object DNS and Cross Sim Messaging"
category: "example"
type: "example"
language: "LSL"
description: "This is a really simple object DNS service written in PHP, and some associated LSL functions to send messages between objects anywhere on the grid using that service and HTTP requests with HTTP-in."
wiki_url: "https://wiki.secondlife.com/wiki/Lame_Object_DNS_and_Cross_Sim_Messaging"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

This is a really simple object DNS service written in PHP, and some associated LSL functions to send messages between objects anywhere on the grid using that service and HTTP requests with HTTP-in.

To install the object DNS stuff, put these two scripts in the same place on your web server.  It doesn't use a database or anything, just creates some files in a "urls" directory that store the URLs.  Yea, it's pretty lame, but it works.  Lol.

get.php:

```lsl
<?php
///////////////////////////////////////////////////////////////////////////////
//
// CCHTTP - Cross Sim object communications module with external object DNS.
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

// Set this to the same thing in both PHP files. Then pass this same string
//	as the "secret" parameter to cchttpInitialize().
$SECRET = "my password";

    if( $_POST['secret'] == $SECRET )
    {
        $name = "urls/".ereg_replace( "[^[:alnum:]+]", "", $_POST['name'] );
        if( file_exists($name) )
            echo file_get_contents( $name );
    }
?>
```

set.php:

```lsl
<?php
///////////////////////////////////////////////////////////////////////////////
//
// CCHTTP - Cross Sim object communications module with external object DNS.
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

// Set this to the same thing in both PHP files. Then pass this same string
//	as the "secret" parameter to cchttpInitialize().
$SECRET = "my password";

    if( $_POST['secret'] == $SECRET )
    {
        if( !file_exists("urls") )
            mkdir( "urls" );
        $name = ereg_replace( "[^[:alnum:]+]", "", $_POST['name'] );
        file_put_contents( "urls/".$name, $_POST['url'] );
    }
?>
```

Alrighty!  Now that that is set up, here is the LSL portion.

This stuff is written in LSL+ ([http://lslplus.sourceforge.net/index.html](http://lslplus.sourceforge.net/index.html)), but if you're just using standard LSL, just paste the stuff from the .lslm file into the top of your scripts and all will be groovy.

CCHTTP.lslm:

```lsl
$module ()

///////////////////////////////////////////////////////////////////////////////
//
// CCHTTP - Cross Sim object communications module with external object DNS.
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

// This is how long we sleep between error retries, to prevent the "Too many
//	HTTP requests too fast" error.
float	RETRY_DELAY			= 3.0;

///////////////////////////////////////////////////////////////////////////////

key		cchttp_reg_qid		= NULL_KEY;
string	cchttp_reg_name 	= "";
string	cchttp_reg_secret	= "";
string	cchttp_url			= "";

list	cchttp_dns_pending	= [];
list	cchttp_sent_pending	= [];

cchttpInitialize( string name, string url, string secret )
{
	cchttp_reg_name = name;
	cchttp_url = url;
	cchttp_reg_secret = secret;
	cchttpReinitialize();
}

cchttpReinitialize()
{
	llRequestURL();
}

cchttpSendMessage( string dest, string type, string data )
{
	key k = llHTTPRequest(
			cchttp_url+"/get.php",
			[
				HTTP_METHOD, "POST",
				HTTP_MIMETYPE, "application/x-www-form-urlencoded"
			],
			"name="+llEscapeURL(dest)+"&secret="+llEscapeURL(cchttp_reg_secret)
		);
	cchttp_dns_pending += [ k, dest, type, data ];
}

cchttpProcessHTTPResponse( key id, integer status, list meta, string body )
{
	integer i;
	for( i=0; i<(cchttp_dns_pending!=[]); )
	{
		if( llList2Key(cchttp_dns_pending,i) == id )
		{
			if( status != 200 )
			{
				llSay( DEBUG_CHANNEL, "Error: CAPSDNS HTTP "+(string)status+". Retrying." );
				cchttpSendMessage( llList2String(cchttp_dns_pending,i+1), llList2String(cchttp_dns_pending,i+2), llList2String(cchttp_dns_pending,i+3) );
				llSleep( RETRY_DELAY );
			}
			else
			{
				key k = llHTTPRequest(
						llStringTrim(body,STRING_TRIM),
						[
							HTTP_METHOD, "POST",
							HTTP_MIMETYPE, "application/x-www-form-urlencoded"
						],
						llDumpList2String( [cchttp_reg_name]+llList2List(cchttp_dns_pending,i+2,i+3), ":" )
					);
				cchttp_sent_pending += [k] + llList2List(cchttp_dns_pending,i+1,i+3);
			}
			cchttp_dns_pending = llDeleteSubList( cchttp_dns_pending, i, i+3 );
		}
		else
			i += 4;
	}
	for( i=0; i<(cchttp_sent_pending!=[]); )
	{
		if( llList2Key(cchttp_sent_pending,i) == id )
		{
			if( status != 200 || llSubStringIndex(body,"cap not found:") == 0 )
			{
				llSay( DEBUG_CHANNEL, "Error: Message to "+llList2String(cchttp_sent_pending,i+2)+" returned HTTP "+(string)status+", "+llStringTrim(body,STRING_TRIM)+". Retrying." );
				cchttpSendMessage( llList2String(cchttp_sent_pending,i+1), llList2String(cchttp_sent_pending,i+2), llList2String(cchttp_sent_pending,i+3) );
				llSleep( RETRY_DELAY );
			}
			cchttp_sent_pending = llDeleteSubList( cchttp_sent_pending, i, i+3 );
		}
		else
			i += 4;
	}
}

list	cchttpProcessHTTPRequest( key id, string method, string body )
{
	list rval = [];
	if( method == URL_REQUEST_GRANTED )
	{
		cchttp_reg_qid = llHTTPRequest(
				cchttp_url+"/set.php",
				[
					HTTP_METHOD, "POST",
					HTTP_MIMETYPE, "application/x-www-form-urlencoded"
				],
				"name="+llEscapeURL(cchttp_reg_name)+"&url="+llEscapeURL(body)+"&secret="+llEscapeURL(cchttp_reg_secret)
			);
	}
	else if( method == URL_REQUEST_DENIED )
	{
		llSay( DEBUG_CHANNEL, "Error: URL not granted! D:" );
	}
	else
	{
		integer i;
		for( i=0; i<2; i++ )
		{
			integer ind;
			ind = llSubStringIndex( body, ":" );
			if( ind == -1 )
				return [];
			else if( ind == 0 )
				rval += "";
			else
			{
				rval += llGetSubString( body, 0, ind-1 );
				body = llDeleteSubString( body, 0, ind );
			}
		}
		rval += llStringTrim(body,STRING_TRIM);
		llHTTPResponse( id, 200, "" );
		return rval;
	}
	return [];
}
```

Here are a couple of scripts that show how to use the thing.  You'll notice that the only difference between the two is the name that the object registers as and the name that it sends the message to.  Put these scripts into a couple of prims, attach one, go to another sim, and try it out.  Yay!

Object1.lslp

```lsl
$import ccHTTP.ccHTTP.lslm();

default
{
    state_entry()
    {
    	// Pass the string to register as with the PHP DNS stuff, the
    	//	URL to the PHP DNS stuff, and the secret phrase in the PHP files.
    	cchttpInitialize( "TestObject1", "http://www.yourhost.com/CAPSDNS", "my password" );
    }

    on_rez( integer i )
    {
    	cchttpReinitialize();
    }

    changed( integer ch )
    {
    	if( ch&CHANGED_REGION || ch&CHANGED_TELEPORT || ch&CHANGED_REGION_START )
    		cchttpReinitialize();
    }

    http_request( key id, string method, string body )
    {
    	list data = cchttpProcessHTTPRequest( id, method, body );
    	if( (data!=[]) )
    	{
    		// "data" is a three-element list: sender, message type, message.
    		// YOUR CODE HERE.
    		llInstantMessage( llGetOwner(), llList2String(data,0)+" sent a message of type "+llList2String(data,1)+": "+llList2String(data,2) );
    	}
    }

    http_response(key id, integer status, list meta, string body)
    {
    	cchttpProcessHTTPResponse( id, status, meta, body );
    }

    touch_start( integer ndet )
    {
    	// YOUR CODE HERE.
    	// Send a message to whatever object has registered as "TestObject1",
    	//	with the message type "Test", and message data containing the
    	//	toucher's name.
    	cchttpSendMessage( "TestObject2", "TEST", llDetectedName(0) );
    }
}
```

Object2.lslp

```lsl
$import ccHTTP.ccHTTP.lslm();

default
{
    state_entry()
    {
    	// Pass the string to register as with the PHP DNS stuff, the
    	//	URL to the PHP DNS stuff, and the secret phrase in the PHP files.
    	cchttpInitialize( "TestObject2", "http://www.yourhost.com/CAPSDNS", "my password" );
    }

    on_rez( integer i )
    {
    	cchttpReinitialize();
    }

    changed( integer ch )
    {
    	if( ch&CHANGED_REGION || ch&CHANGED_TELEPORT || ch&CHANGED_REGION_START )
    		cchttpReinitialize();
    }

    http_request( key id, string method, string body )
    {
    	list data = cchttpProcessHTTPRequest( id, method, body );
    	if( (data!=[]) )
    	{
    		// "data" is a three-element list: sender, message type, message.
    		// YOUR CODE HERE.
    		llInstantMessage( llGetOwner(), llList2String(data,0)+" sent a message of type "+llList2String(data,1)+": "+llList2String(data,2) );
    	}
    }

    http_response(key id, integer status, list meta, string body)
    {
    	cchttpProcessHTTPResponse( id, status, meta, body );
    }

    touch_start( integer ndet )
    {
    	// YOUR CODE HERE.
    	// Send a message to whatever object has registered as "TestObject1",
    	//	with the message type "Test", and message data containing the
    	//	toucher's name.
    	cchttpSendMessage( "TestObject1", "TEST", llDetectedName(0) );
    }
}
```