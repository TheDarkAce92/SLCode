---
name: "Name2Key"
category: "example"
type: "example"
language: "LSL"
description: "Usage sample"
source_url: "https://github.com/Outworldz/LSL-Scripts/blob/master/Name2Key/Name2Key/Object/Name2Key_1.lsl"
source_name: "Outworldz LSL Scripts (GitHub) / Name2Key"
source_owner: "Outworldz"
source_repo: "LSL-Scripts"
source_branch: "master"
source_path: "Name2Key/Name2Key/Object/Name2Key_1.lsl"
source_project: "Name2Key"
source_part_total: "4"
first_fetched: "2026-03-18"
last_updated: "2026-03-19"
has_versions: "true"
active_version: "scraped-outworldz-lsl-scripts-github-name2key-2026-03-19"
---

```lsl
// === Part 1/4 ===
// :CATEGORY:Owner Key
// :NAME:Name2Key
// :AUTHOR:Takat Su
// :CREATED:2011-10-16 19:28:26.180
// :EDITED:2013-09-18 15:38:58
// :ID:551
// :NUM:749
// :REV:1.0
// :WORLD:Second Life
// :DESCRIPTION:
// Usage sample 
// :CODE:
integer cmdName2Key = 19790;

integer cmdName2KeyResponse = 19791;

 

default {

    state_entry() {

        llMessageLinked( LINK_SET, cmdName2Key, "Test Name", NULL_KEY );

    }

 

    link_message( integer inFromPrim, integer inCommand, string inKeyData, key inReturnedKey ) {

        if( inCommand == cmdName2KeyResponse ) {

            list lParts = llParseString2List( inKeyData, [":"], [] );

            string lName = llList2String( lParts, 0 );

            key lKey = (key)llList2String(lParts, 1 );

        }

    }

}

// === Part 2/4 ===
// :CATEGORY:Owner Key
// :NAME:Name2Key
// :AUTHOR:Takat Su
// :CREATED:2011-10-16 19:28:26.180
// :EDITED:2013-09-18 15:38:58
// :ID:551
// :NUM:750
// :REV:1.0
// :WORLD:Second Life
// :DESCRIPTION:
// Google App Python Code - not needed unless you want to make your own app engine
// :CODE:
rom google.appengine.ext import webapp

from google.appengine.ext.webapp.util import run_wsgi_app

import urllib, urlparse

 

kURL = 'http://vwrsearch.secondlife.com/client_search.php?session=00000000-0000-0000-0000-000000000000&q='

kProfile = "Resident profile"

kResult = "secondlife:///app/agent/"

 

class MainPage( webapp.RequestHandler ):

    def get(self):

        inName = self.request.get("name").upper()

        name = inName.replace(" ", "%20")

        data = urllib.urlopen(kURL + name).read()

        start = data.index( kProfile )

        foundName = data[start+18:start+18+len(inName)]

	key = '00000000-0000-0000-0000-000000000000'

        if foundName.upper() == inName:

            start = data.index( kResult )

            key = data[start+len(kResult):start+len(kResult)+36]

        else:

            foundName =	inName

 

        self.response.out.write("%s:%s" % (foundName, key))

 

 

application = webapp.WSGIApplication(

    [('/', MainPage)],

    debug = True)

 

def main():

    run_wsgi_app(application)

 

if __name__ == "__main__":

    main()

// === Part 3/4 ===
// :CATEGORY:Owner Key
// :NAME:Name2Key
// :AUTHOR:Takat Su
// :CREATED:2011-10-16 19:28:26.180
// :EDITED:2013-09-18 15:38:58
// :ID:551
// :NUM:751
// :REV:1.0
// :WORLD:Second Life
// :DESCRIPTION:
// app.yaml file  - not needed unless you want to make your own app engine
// :CODE:
application: name2key

version: 1

runtime: python

api_version: 1

 

handlers:

- url: .*

  script: name2key.py

// === Part 4/4 ===
// :CATEGORY:Owner Key
// :NAME:Name2Key
// :AUTHOR:Takat Su
// :CREATED:2011-10-16 19:28:26.180
// :EDITED:2013-09-18 15:38:58
// :ID:551
// :NUM:752
// :REV:1.0
// :WORLD:Second Life
// :DESCRIPTION:
// Library 
// :CODE:
integer cmdName2Key = 19790;

integer cmdName2KeyResponse = 19791;

 

list gRequests;

 

key requestName2Key( string inName ) {

    list lNameParts = llParseString2List( inName, [" "], [] );

    string lFirstName = llList2String( lNameParts, 0 );

    string lLastName = llList2String( lNameParts, 1 );

    return llHTTPRequest( "http://name2key.appspot.com/?name=" + lFirstName + "%20" + lLastName, [], "" );

}

 

default {

    link_message( integer inFromPrim, integer inCommand, string inName, key inKey ) {

        if( inCommand == cmdName2Key )

            gRequests += [requestName2Key( inName ), inKey ];

    }

 

    http_response(key inKey, integer inStatus, list inMetaData, string inBody ) {

        integer lPosition = llListFindList( gRequests, [inKey]);

        if( lPosition != -1 ) {

            llMessageLinked( LINK_SET, cmdName2KeyResponse, inBody, llList2Key( gRequests, lPosition+1 ) );

            gRequests = llDeleteSubList( gRequests, lPosition, lPosition + 1 );

        }

    }

}
```
