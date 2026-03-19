---
name: "Client Specific Contents Giver"
category: "example"
type: "example"
language: "LSL"
description: "This prim will allow you to give the contents of itself to any user that clicks on it while using the preset specified client. Currently this script is setup to work with the Phoenix Client. But could very quickly and easily be converted to work with other clients as well."
wiki_url: "https://wiki.secondlife.com/wiki/Client_Specific_Contents_Giver"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

This prim will allow you to give the contents of itself to any user that clicks on it while using the preset specified client. Currently this script is setup to work with the Phoenix Client. But could very quickly and easily be converted to work with other clients as well.

It shows how to use media testing to read browser headers to get the details about the users clients. Similar to the closed source ban system CDS. this Script will allow you to detect Clients.

```lsl
//vendor by Damian Darkwyr
//you MUST deed this item to the group that owns the parcel. unless you own the parcel alone.

key newurl_request;//key fetch for urlgetter
string currenturl = "";//our current url
string busytexture = "f660fcf7-4636-b3cd-ea6f-d5fe44bbb192";//the texture that says we are busy
string producttexture = "ebb6d25a-7192-a65c-7a39-903468df57ca";//the texture that represents the product we are giving away
string text = "Click here to recieve this item free if you are using Phoenix Client.";//the text to display over the prim
integer touchok = TRUE;//is it ok to touch and test?
string phoenixclient = "SecondLife/1.5.1.373 (Snowglobe Test Build; default skin)";//the clients user-agent we want
give(key id)//gather inventory and give all at once in a folder
{
    list out = [];
    integer i = 0;
    do
    {
        if(llGetInventoryName(INVENTORY_ALL,i) != llGetScriptName())
        {
            out += [llGetInventoryName(INVENTORY_ALL,i)];
        }
        i++;
    }while(i < llGetInventoryNumber(INVENTORY_ALL));
    if(out != [])
    {
        llGiveInventoryList(id,llGetObjectName(),out);
    }
}
default
{
    state_entry()
    {
        llSetTexture(busytexture,ALL_SIDES);//hide the product texture for now we need to setup first
        llSetText("",<1,1,1>,1);//clear text for now untill we are all setup
        llReleaseURL(currenturl);//clear the current url if any
        newurl_request = llRequestURL();//request a new url to read data from users
    }
    changed(integer c)//if anything changes reset this script now
    {
        llResetScript();
    }
    http_request(key id, string method, string body)
    {
        if ((method == URL_REQUEST_GRANTED) && (id == newurl_request) )//we got an all clear new url
        {
            currenturl = body;//set the current url to the returned body
            newurl_request = NULL_KEY;//clear our request key
            llSetTexture(producttexture,ALL_SIDES);
            llSetText(text,<1,1,1>,1);
        }
        else if ((method == URL_REQUEST_DENIED) && (id == newurl_request))//we were denied a url maybe it failed maybe urls are full?
        {
            llReleaseURL(currenturl);//clear the url again
            newurl_request = llRequestURL();//try again see if it was a fluke?
        }else
        {
            list headers = ["x-path-info","user-agent"];//reading sl browser headers... we need path for key and user-agent for the client version stuff
            integer pos = ~llGetListLength(headers);
            string info;
            while(++pos)
            {
                string header = llList2String(headers, pos);
                info=info+"["+llGetHTTPHeader(id, header)+"]|";//add the header detail to a string to parse
            }
            list pi = llParseString2List(info,["|"],[]);//break the string into a list easier to deal with i think.
            string target = llList2String(pi,0);    target = llDeleteSubString(target,0,1);    target = llDeleteSubString(target,-1,-1);//get the users key here
            string useragent = llList2String(pi,1);    useragent = llDeleteSubString(useragent,0,0);    useragent = llDeleteSubString(useragent,-1,-1);//get the users client
            string b = useragent;
            list browserbreak = llParseString2List(b,[" "],[]);//this
            browserbreak = llDeleteSubList(browserbreak,0,10);//just
            browserbreak = llDeleteSubList(browserbreak,-1,-1);//deletes useless crap
            b = llDumpList2String(browserbreak," ");//from the user-agent return and gives us the details we actually want.
            if(b==phoenixclient)//this is what phoenix client's user-agent looks like.
            {
                //most likely a phoenix user. this could be spoofed but 9 times out of 10 its pretty spot on.
                llInstantMessage((key)target,"Hey thanks for using the latest version of Phoenix. Fetching your free item now....");//tell the user thanks and
                give((key)target);//give them the item
            }else
            {
                llInstantMessage((key)target,"I'm sorry but you are not using the latest version of Phoenix. Please download and install the newest version of Phoenix.");//if they arent on phoenix tell them to get it.
            }
            llHTTPResponse(id,500,"Internal Server Error");//stop the media test.
            llSetTexture(producttexture,ALL_SIDES);//now that we are done reset the product texture.
            llSetText(text,<1,1,1>,1);//set the text back to default
            touchok = TRUE;//open touches again
        }
    }
    touch_start(integer x)
    {
        if(touchok == TRUE)//thank you  raglegumm Aeon
        {
            touchok = FALSE;//stop others from touching this prim.
            key id = llDetectedKey(0);//the key of the user we are going to test.
            llInstantMessage(id,"checking to see if you are using Phoenix Client...Please make sure you have media streaming enabled. if not do so now and click on me again.");//tell them to make sure they have media turned on.
            string url=currenturl+"/"+(string)id;//set a url with the currenturl and the users key.so we know who just got tested. lol.
            llSetTexture(busytexture,ALL_SIDES);//hide the texture and show we are busy right now so other noobs dont click yet.
            llSetText("Currently Busy with "+llDetectedName(0),<1,1,1>,1);//show others who is using the vendor.
            llParcelMediaCommandList([PARCEL_MEDIA_COMMAND_AGENT,id,
                PARCEL_MEDIA_COMMAND_URL,url,
                PARCEL_MEDIA_COMMAND_TYPE,"image/png",
                PARCEL_MEDIA_COMMAND_TIME,0.0,
                PARCEL_MEDIA_COMMAND_PLAY]); //do the actual media streaming test on the user.
        }
    }
}
```