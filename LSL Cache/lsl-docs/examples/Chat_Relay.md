---
name: "Chat Relay"
category: "example"
type: "example"
language: "LSL"
description: "llShout is limited to 100m and sometimes you need to send a message farther. This script is designed to resend the message without getting stuck in a loop. To use"
wiki_url: "https://wiki.secondlife.com/wiki/Chat_Relay"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL

llShout is limited to 100m and sometimes you need to send a message farther.
This script is designed to resend the message without getting stuck in a loop.
**To use**1. Place in a prim 1. Change the channel number. 1. place them as needed changing the prim's description to a unique letter or number to set its node name. The concept is similar to the "path" part of an email message in that it modifies the message by adding its name to the message. When it hears a message it parses it to get the first field. The first field is used for performance reasons. This script currently uses the pipe symbol but you can change the field separator as needed. It then does a string search of the path field using ",n," where n is its number or letter. The "Path" is started with "," and the repeater adds its number and reshouts it if it has not heard it before. The message goes like this ```lsl pipe message ,1,pipe message ,2,1,pipe message ``` Trouble shooting**This script can deal with grids or loops in any direction as long as each one is uniquely named. If multiple relays exist with the same name some messages will get lost. Improvements**The script could be improved using a string search instead of llParseString2List since it only adds its name to the start of the message. Currently a message with a length of 255 characters when sent through the relay will be shortened. Because of this it is recommended to send messages with a maximum length of 200 characters to allow for 55 characters of path. Chat Relay

```lsl
//Chat relay
//Released into the public domain by grumble Loudon
//
// Pipe is the section separator
// commas are used to separate path ID's
//
integer g_Channel = 1234;	//change this to your channel

//********************************************************************************************
default
{
    //********************************************************************************************8
    state_entry()
    {

        llListen(g_Channel,"",NULL_KEY,"");
    }
//********************************************************************************************8
    listen(integer channel, string name, key id, string message)
    {
	//Path|address|protocol|data
        list mList = llParseStringKeepNulls(message,["|"],[]);
        string path = llList2String( mList,0); 		//get route path

        list pathList = [];
        if (llStringLength(path) > 0)
        {
		pathList  = llParseString2List(path,[","],[]);
        };
        string MyName = llGetObjectDesc();
        if (llStringLength(MyName) > 0)		//prevent infinite loops if description is blank
	{
	        list MyNameList;
        	MyNameList += MyName;

	        if (llListFindList(pathList, MyNameList) == -1){   // Returns -1 if not found

	            string Msg =  MyName + "," + message;   //add me to the path

	            llShout(g_Channel,Msg);

	        }; //route path
	};// No description
    } // listen
    //********************************************************************************************8
}//default
```

#### See also

llShout