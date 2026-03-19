---
name: "ITunes RPC Email"
category: "example"
type: "example"
language: "LSL"
description: "I made this a long time ago, before HTTP, how l33t is that? >.>"
wiki_url: "https://wiki.secondlife.com/wiki/ITunes_RPC_Email"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

I made this a long time ago, before *HTTP*, how l33t is that? >.>

```lsl
string NOTIFY_EMAIL = "email@domain.tld";

integer USER_ID = 0; // Fox

// I always set constants for different idata commands sent through RPC. Then I just make sure they match the constants
// that I set in my PHP file, and everything works great.
integer RPC_ERROR = 0;
integer SEND_SONG = 1;
integer SEND_LINK = 2;

// Always reamins 99
integer RPC_SUCCESS = 99;

// This will be used as a reference later in case we need to know it.
key rpc_chan;
string rgn_name;

default {

    state_entry()
    {
        rgn_name = llGetRegionName();
        llOpenRemoteDataChannel();
        llListen(1, "Fox Diller", "", "");
        llSetTimerEvent(13);
    }

    timer()
    {
        if (llGetRegionName() != rgn_name)
        {
            llOwnerSay("Changing Sims");
            rgn_name = llGetRegionName();
            llOpenRemoteDataChannel();
        }
    }


    listen(integer chan, string name, key id, string msg)
    {
        if (llDetectedKey(0) == llGetOwner()) {

            if (msg == "key")
            {
                llOwnerSay((string)rpc_chan);
            }

            if (msg == "timeron")
            {
                llSetTimerEvent(13);
                llOwnerSay("Timer Turned On!");
            }

            if (msg == "timeroff")
            {
                llSetTimerEvent(0);
                llOwnerSay("Timer Turned Off!");
            }
            if (msg == "reset") llResetScript();
        }
    }

    remote_data(integer event_type, key channel, key message_id, string sender, integer idata, string sdata)
    {
        // If the RPC channel has just been opened, then we need to send off a notice to the webserver.
        if (event_type == REMOTE_DATA_CHANNEL)
        {
            // We should keep a reference to the RPC channel that has been opened.
            rpc_chan = channel;

            // Here, we can specify extra parameters in the email that we need the webserver to know, such as the RPC channel.
            string msg;
            msg = "Command: updatekey\n";
            msg += "RPC-Chan: "+(string)rpc_chan+"\n";
            msg += "UserID: "+(string)USER_ID+"\n";
            llEmail(NOTIFY_EMAIL, "RPC Chan Updated", msg);

            llOwnerSay("Sent Object ID string to MySQL server.");
        }

        // If an RPC request has been sent from the webserver.
        else if (event_type == REMOTE_DATA_REQUEST)
        {
            // We can check what command is coming through here, and handle them as needed.
            if (idata == SEND_SONG)
            {
                list songData;
                songData = llCSV2List(sdata);
                llSetText("iTunes <-> SecondLife\n-----------------------------------\nAlbum: "+llList2String(songData, 0)+"\nArtist: "+llList2String(songData, 1)+"\nSong: "+llList2String(songData,2), <1,1,1>, 1.0);
                llSay(0, "Fox is currently listening to: "+llList2String(songData, 1)+" - "+llList2String(songData, 2));
                llRemoteDataReply(channel, message_id, "success", RPC_SUCCESS);

            // Just checking for another command.
            }
            else if (idata == SEND_LINK)
            {
                llOwnerSay("Th5s Feat4re Broken");
//                llRemoteDataReply(channel, message_id, "success", RPC_COMMAND2);
             // If it was an unrecognized command, we still have to send some sort of reply back.
            }
            else
            {
                llOwnerSay("WARNING!!!!!!!!!!!!!!!!!!!");
                // llRemoteDataReply(channel, message_id, "", RPC_ERROR);
            }
        }
    }
}
```