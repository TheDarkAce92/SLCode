---
name: "Universal Translator"
category: "example"
type: "example"
language: "LSL"
description: "While the massive codebase generously shared by Hank Ramos illustrates several concepts of advanced LSL programming, as a translation service, it relies upon the Google Translation Service API, which, at the time of posting the code below, was free to use. Google has, over a decade ago, not only changed the API itself — requiring special access keys, unique to each user of the service — but the service is no longer free as before. As such, do not rely upon the code below, which will not work. Replacing the deprecated API calls to Google's servers by modern calls — or even using a different online machine translation service — is left as an exercise to the reader."
wiki_url: "https://wiki.secondlife.com/wiki/Universal_Translator"
author: "Hank Ramos"
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Warning!

While the massive codebase generously shared by Hank Ramos illustrates several concepts of advanced LSL programming, as a translation service, it relies upon the Google Translation Service API, which, at the time of posting the code below, was free to use. Google has, over a decade ago, not only changed the API itself — requiring special access keys, unique to each user of the service — but the service is no longer free as before. As such, do not rely upon the code below, which *will not work*. Replacing the deprecated API calls to Google's servers by modern calls — or even using a different online machine translation service — is left as an exercise to the reader.

This is the complete source code to the widely popular and free "HR Universal Translator" by Hank Ramos.  This device is a dynamic public chat listener that automatically translates between 50+ languages and delivers translations of spoken text to those nearby that don't speak the language of the original speaker.

Please help to further development on this open-source project.

- 1 Future Upgrades Needed
- 2 The Code

  - 2.1 Universal Translator Engine
  - 2.2 HTTP Handler
  - 2.3 Interface Handler

## Future Upgrades Needed

1. Support for Google Spellcheck.  Would be great to be able to spell-check chat first, and automatically do suggested corrections before the translation.

2. Break the engine script into two or more scripts to allow for future expansion and to be able to handle low memory situations better.

3. Support pseudo-instant message.  This could be done with avatars wearing the device within 100m of each others, or could be done world-wide using email or some other communications mechanism. Avatars would chat on a hidden channel, and would be able to communicate with another avatar or group chat.  Would require inworld servers of prims to link translators up together and find one another.

4. Ensure that unicode is supported correctly.  Ensure that Right-to-Left languages are input and output correctly.  May need additional options since the SL client doesn't support this correctly and sometimes people speak backwards into SL chat to get around this.

5. Rework auto-detection of language code. Should only automatically change the avatar's language if it is reliably predicted that they have changed languages.

6. Add in automatic "spam" detection and prevent translation.  Find way to detect gesture "chat spam" and filter that out from the translation.  Filter out bad translations that only return the same or similar input.  Support replacement of common abbreviations or slang so that the google translation system can translate correctly.  May require support of a user-definable dictionary notecard.

7. Handle translation errors from Google and resubmit the translation, rather than just ignoring it.

8. Can you think of other improvements?

The Code

The device consists of 3 key scripts, with several ancillary scripts to function.  The key scripts are listed here...

## Universal Translator Engine

This is the "heart" of the translator.  It handles communications with other translators, handles listening to avatars for chat, and handles most of the HTTP traffic.

How do multiple translators communicate?  There are two chat channels at work...

The heartbeat channel: this channel is fixed and common amongst all Universal Translators.  This is where each translator regularly announces its presence to other translators in the area.  If another one is found, a "master' translator is elected at random (with higher version releases of the translators getting higher values).  The master translator is in charge of listening to all chat, and sending text to be translated and IMed to the recipient to the other "slave" translators.

Unique translator channel: each translator will select it's own channel to listen for incoming translations.  This serves as a unique conduit for the master translator to communicate with each individual slave.  This allows the heartbeat channel to be free for command messages to be sent, since the translated text being passed around can quickly saturate it.

This multi-translator communication might be useful in other scripting projects.

```lsl
//Universal Translator
//Version 1.9.0
//November 12, 2009
//LSL Script copyright 2006-2009 by Hank Ramos
//Web Server Services powered by Google

//Variables
list agentsInTranslation;
list agentsInTranslationOptions;
list requestList;
integer listenID;

integer isMaster = 1;
integer autoLanguage = TRUE;
integer enabled = FALSE;
integer showTranslation = FALSE;
integer tranObjects = TRUE;

integer lastHeartBeat;
list    languageCodes = [
"zh-CN", "zh-TW", "hr",
"bg", "be", "ca",
"af", "sq", "ar",

"tl", "fr", "gl",
"fi", "en", "et",
"cs", "da", "nl",

"id", "ga", "it",
"hi", "hu", "is",
"de", "el", "iw",

"mt", "no", "fa",
"lt", "mk", "ms",
"ja", "ko", "lv",

"sl", "es", "sw",
"ru", "sr", "sk",
"pl", "pt-PT", "ro",

"yi", "", "",
"uk", "vi", "cy",
"sv","th", "tr"];

list    translators;
list    sayCache;
list    sayCachePrivate;
integer priorityNumber;
integer priorityNumListenID;
integer isInitialized = FALSE;
string  options;

//Options
//integer debug = TRUE;
integer broadcastChannel = -9999999; //note this is not the channel used by the HR Universal Translator
string  password = "password"; //note this is not the password used to encrypt comms of the HR Universal Translator
integer version = 190;
sendIM(key id, string str)
{
    if (llGetParcelFlags(llGetPos()) & PARCEL_FLAG_ALLOW_SCRIPTS)
    {
        llMessageLinked(LINK_ALL_CHILDREN, 85234119, str, id);
    }
    else
    {
        llMessageLinked(LINK_THIS, 85304563, str, id);
    }
}

sendTextBatch(integer channel, string sendText)
{
    sendText = llXorBase64StringsCorrect(llStringToBase64(sendText), llStringToBase64(password));;
    while (llStringLength(sendText) > 508) //If string is 509 characters or longer
    {
        llSay(channel, llGetSubString(sendText, 0, 507)); //send 508 character chunk
        sendText = llGetSubString(sendText, 508, -1);  //delete 508 character chunk
    }
    llSay(channel, sendText);  //send out any remainder chunk or original chunk
    if (llStringLength(sendText) == 508)
        llSay(channel, (string)(channel*4958654));
    llMessageLinked(LINK_ALL_CHILDREN, 6634934, (string)<0.25, 0, 0.25>, "");
}

string receiveTextBatch(key id, string message)
{
    integer listPos;
    string  tempString = "";

    listPos = llListFindList(sayCache, [id]);
    if (listPos >= 0)
    {
        while (listPos >= 0)
        {
            tempString = tempString + llList2String(sayCache, listPos + 1);
            sayCache = llDeleteSubList(sayCache, listPos, listPos + 1);
            listPos = llListFindList(sayCache, [id]);
        }
        message = tempString + message;
    }
    message = llBase64ToString(llXorBase64StringsCorrect(message, llStringToBase64(password)));
    return message;
}
string receiveTextBatchPrivate(key id, string message)
{
    integer listPos;
    string  tempString = "";

    listPos = llListFindList(sayCachePrivate, [id]);
    if (listPos >= 0)
    {
        while (listPos >= 0)
        {
            tempString = tempString + llList2String(sayCachePrivate, listPos + 1);
            sayCachePrivate = llDeleteSubList(sayCachePrivate, listPos, listPos + 1);
            listPos = llListFindList(sayCachePrivate, [id]);
        }
        message = tempString + message;
    }
    message = llBase64ToString(llXorBase64StringsCorrect(message, llStringToBase64(password)));
    return message;
}
updateTranslatorList()
{
    integer x;
    integer listLength;
    list    newList;
    string  tempString;
    integer newMaster;

    //Scan and remove translators not in the area
    for (x = 0; x < llGetListLength(translators); x += 2)
    {
        tempString = llList2String(llGetObjectDetails(llList2Key(translators, x + 1), [OBJECT_POS]), 0);
        if ((llVecDist(llGetPos(), (vector)tempString) <= 20.0) && (tempString != ""))
            newList += llList2List(translators, x, x + 1);
    }
    translators = newList;

    listLength = llGetListLength(translators);
    llMessageLinked(LINK_THIS, 65635544, (string)listLength, "");

    if (listLength == 0)
    {
        newMaster = 1;
    }
    else
    {
        if (enabled)
        {
            newMaster = 2;
            for (x = 0; x < llGetListLength(translators); x += 2)
            {
                //llOwnerSay("Checking Priority Number(" +  (string)priorityNumber + "): " + (string)llList2Integer(translators, x));
                if (llList2Integer(translators, x) > priorityNumber)
                {
                    newMaster = 0;
                }
            }
        }
        else
        {
            newMaster = 0;
        }
    }

    if ((isMaster > 0) && (newMaster == 0))
    {
        //We are being demoted from master to slave
        //Flush agentsInTranslation to master
        if (llGetListLength(agentsInTranslation) > 0)
        {
            //Demotion Dump of agentsInTranslation to Master
            sendTextBatch(broadcastChannel, llList2CSV([1003, llList2CSV(agentsInTranslation)]));
            if (isInitialized == FALSE) return;
            sendTextBatch(broadcastChannel, llList2CSV([1004, options])); //error
        }
        llListenRemove(listenID);
    }
    if ((isMaster == 0) && (newMaster > 0))
    {
        llListenRemove(listenID);
        listenID = llListen(0, "", "", "");
    }
    isMaster = newMaster;
    llMessageLinked(LINK_THIS, 34829304, (string)isMaster, "");
}

sendHeartbeat()
{
    updateTranslatorList();
    sendTextBatch(broadcastChannel, llList2CSV([1001, priorityNumber]));

    //Broadcast agentList to Slaves
    if (isMaster == 2)
    {
        sendTextBatch(broadcastChannel, llList2CSV([1002, llList2CSV(agentsInTranslation)]));
    }

}

//Functions
checkThrottle(integer num, string msg, list params)
{
    integer x;
    integer maxCount;
    float   oldTime;
    float   sleepTime;
    list    newList;
    key     returnValue;
    integer channelToSpeak;

    //loop though list and remove items older than 25 seconds
    for (x = 0; x < llGetListLength(requestList); x += 1)
    {
        oldTime = llList2Float(requestList, x);
        //Construct new list with only times less than 25 seconds
        if ((llGetTime() - oldTime) <= 25.0)
            newList += oldTime;
    }
    requestList = newList;

    x = llGetListLength(requestList);

    //Shunt all translations to linked translators if master
    if (isMaster == 2)
    {
        if (num == 0)
        {
            //Send HTTP request to other translator
            //Send out Request to Random Translator Channel

            channelToSpeak = llList2Integer(llListRandomize(llList2ListStrided(translators, 0, -1, 2), 1), 0);
            if (channelToSpeak > 0)
            {
                sendTextBatch(channelToSpeak, llList2CSV([num, llList2CSV(params)]) + "~" + msg);
                return;
            }
        }
    }

    if (x == 19)
    {
        sleepTime =  25.0 - (llGetTime() - llList2Float(requestList, 0));
        if (sleepTime > 0)
        {
            llSleep(sleepTime);
        }
        requestList = llDeleteSubList(requestList, 0, 0);
    }

    if (num == 0)
    {
        msg = "translate?v=1.0&q=" + msg;
    }
    else
        msg = "detect?v=1.0&q=" + msg;

    requestList += llGetTime();
    returnValue = llHTTPRequest("http://ajax.googleapis.com/ajax/services/language/" + msg, [HTTP_METHOD, "GET", HTTP_MIMETYPE, "plain/text;charset=utf-8"], " ");

    if (returnValue != NULL_KEY)
    {
        if (num == 0)
            llMessageLinked(LINK_THIS, 235365342, llList2CSV(params), returnValue);
        else
            llMessageLinked(LINK_THIS, 235365343, llList2CSV(params), returnValue);
    }
    else
    {
        llSleep(40.0); //Something has gone horribly wrong, sleep 40 seconds to clear throttle
    }
}

string checkLanguage(string tempString)
{
    if      (llGetSubString(tempString, 0, 1) == "zh")    tempString = "zh-CN";
    else if (tempString == "und")   tempString = "el";
    else if (llListFindList(languageCodes, [tempString]) < 0) tempString = "";
    tempString = llGetSubString(tempString, 0, 1);
    return tempString;
}
addAgent(key id, string language, integer recheckLangauge)
{
    integer listPos;
    integer listPosID;
    integer idNum;
    string  tempString;

    listPos = llListFindList(agentsInTranslation, [id]);
    if (listPos < 0)
    {
        while (listPosID >= 0)
        {
            idNum = llRound(llFrand(2000000)) + 1;
            listPosID = llListFindList(agentsInTranslation, [idNum]);
        }
        agentsInTranslation += [id, language, recheckLangauge, idNum];
        llMessageLinked(LINK_THIS, 64562349, language, id);
    }
    else
        agentsInTranslation = llListReplaceList(agentsInTranslation, [language, recheckLangauge], listPos + 1, listPos + 2);
}

string addNewAgent(key id)
{
    string speakerLanguage;

    if (llList2Key(llGetObjectDetails(id, [OBJECT_CREATOR]), 0) == NULL_KEY)
    {
        speakerLanguage  = checkLanguage(llGetAgentLanguage(id));
        if (speakerLanguage == "")
        {
            speakerLanguage = "en";
            addAgent(id, speakerLanguage, TRUE);
        }
        else
        {
            addAgent(id, speakerLanguage, FALSE);
        }
    }
    return speakerLanguage;
}

key getAgentKey(integer agentID)
{
    integer listPos = llListFindList(agentsInTranslation, [agentID]);
    if (listPos < 0)
    {
        return "";
    }
    else
    {
        return llList2Key(agentsInTranslation, listPos - 3);
    }
}
processHTTPResponse(integer type, string body, list params)
{
    integer listPos;
    list    recepientList;
    key     recepientID;
    string  recepientLanguage;
    string  languagePair;
    key     speakerID;
    string  speakerName;
    string  speakerLanguage;
    string  translatedText;
    string  tempString;
    integer x;
    integer speakerLanguageReliable;
    float   speakerLanguageConfidence;
    list    tempList;

    //===================
    //Process Translation
    //===================
    if (type == 0)
    {
        speakerID  = llList2Key(params, 1);
        speakerName = llKey2Name(speakerID);
        if (speakerName == "")
            speakerName = llList2String(llGetObjectDetails(speakerID, [OBJECT_NAME]), 0);

        recepientList = llParseString2List(llList2String(params, 2), ["@"], []);
        tempList = llParseStringKeepNulls(llList2String(params, 3), ["|"],[]);
        recepientLanguage = llList2String(tempList, 1);
        languagePair = llDumpList2String(tempList, ">>");

        //Perform Text Cleanup
        x = llSubStringIndex(body, "\",\"detectedSourceLanguage\":\"");
        if (x >= 0)
        {
            translatedText  = llGetSubString(body,  llSubStringIndex(body, "{\"translatedText\":\"") + 18, x);
            speakerLanguage = checkLanguage(llGetSubString(body, x + 28, llSubStringIndex(body, "\"}, \"responseDetails\":") - 1));

            listPos = llListFindList(agentsInTranslation, [speakerID]);
            if (listPos >= 0)
            {
                if (speakerLanguage != llList2String(agentsInTranslation, listPos + 1))
                    agentsInTranslation = llListReplaceList(agentsInTranslation, [TRUE], listPos + 2, listPos + 2);  //Mark for recheck of actual spoken language.
            }
        }
        else
        {
            translatedText = llGetSubString(body, llSubStringIndex(body, "{\"translatedText\":\"") + 18, llSubStringIndex(body, "\"}, \"responseDetails\""));
        }

        //Reverse order if Recepient Language is Hebrew or Arabic
        if ((recepientLanguage == "iw") || (recepientLanguage == "ar"))
        {
            tempString = "";
            for(x = llStringLength(translatedText);x >= 0; x--)
            {
                tempString += llGetSubString(translatedText, x, x);
            }
            translatedText = tempString;
        }
        tempString = speakerName + "(" + languagePair + "): " + translatedText;
        if (showTranslation)
            sendIM(speakerID, tempString);
        for (x = 0; x < llGetListLength(recepientList); x += 1)
        {
            recepientID = getAgentKey(llList2Integer(recepientList, x));

            if (recepientID != "")
            {
                recepientLanguage = llList2String(agentsInTranslation, llListFindList(agentsInTranslation, [recepientID]) + 1);
                if (recepientLanguage != speakerLanguage)
                    sendIM(recepientID, tempString);
            }
        }
        return;
    }

    //===========================
    //Process Language Detection
    //===========================
    if (type == 1)
    {
        speakerID = llList2Key(params, 1);

        speakerLanguageReliable = llToLower(llGetSubString(body, llSubStringIndex(body, "\",\"isReliable\":") + 15, llSubStringIndex(body, ",\"confidence\":") - 1)) == "true";
        speakerLanguageConfidence = (float)llGetSubString(body, llSubStringIndex(body, ",\"confidence\":") + 14, llSubStringIndex(body, "}, \"responseDetails\":") - 1);

        listPos = llListFindList(agentsInTranslation, [speakerID]);

        if (((listPos < 0) && (speakerLanguageReliable) || (speakerLanguageConfidence >= 0.18)))
        {
            //Analyze Data
            tempString = checkLanguage(llToLower(llGetSubString(body, llSubStringIndex(body, "{\"language\":\"") + 13, llSubStringIndex(body, "\",\"isReliable\":") - 1)));
            if (tempString == "") return;

            if (speakerLanguageConfidence < 0.14)
                addAgent(speakerID, tempString, TRUE);
            else
                addAgent(speakerID, tempString, FALSE);
        }
    }
}

default
{
    state_entry()
    {
        //Multiplexor Initialization
        priorityNumber = version*1000000 + llRound(llFrand(499999) + 50000);
        llListen(broadcastChannel, "", NULL_KEY, "");
        priorityNumListenID = llListen(priorityNumber, "", NULL_KEY, "");

        //Send out initial heartbeat
        lastHeartBeat = llGetUnixTime();
        sendTextBatch(broadcastChannel, llList2CSV([1001, priorityNumber]));

        //Wait for the network to settle down
        llSetTimerEvent(5);
        //llSetTimerEvent(10 + ((1-llGetRegionTimeDilation()) * 1));
    }

    sensor(integer num_detected)
    {
        integer x;
        key     id;

        for (x = 0; x < num_detected; x += 1)
        {
            id = llDetectedKey(x);
            if (llListFindList(agentsInTranslation, [id]) < 0)
            {
                addNewAgent(id);
            }
        }
    }
    link_message(integer sender_num, integer num, string str, key id)
    {
        integer x;
        integer listPos;
        list    tempList;
        integer channelToSpeak;

        //Old Multiplexor
        if (num == 8434532)
        {
            enabled = (integer)str;
        }
        else if (num == 3342976)
        {
            //Send Preferences
            options = str;
            if (isInitialized == FALSE) return;
            tempList = llCSV2List(options);
            showTranslation = llList2Integer(tempList, 0);
            tranObjects = llList2Integer(tempList, 1);
            autoLanguage = llList2Integer(tempList, 2);
            sendTextBatch(broadcastChannel, llList2CSV([1004, options]));

        }
        else if (num == 9384610)
        {
            if (isMaster == 0) //markering
                //llMessageLinked(LINK_THIS, 5598321, llList2CSV([id, str, FALSE]), "");
                sendTextBatch(broadcastChannel, llList2CSV([1003, id, str, FALSE]));
            else
                addAgent(id, str, TRUE);
        }
        else if (num == 345149625)
        {
            //Return Translation
            processHTTPResponse(0, str, llCSV2List(id));
        }
        else if (num == 345149626)
        {
            //Return Detection
            processHTTPResponse(1, str, llCSV2List(id));
        }
    }
    timer()
    {
        integer x;
        string  tempString;
        list    newList;
        integer translatorCount = llGetListLength(translators)/2;

        if (isInitialized == FALSE)
        {
            isInitialized = TRUE;
            enabled = TRUE;
            listenID = llListen(0, "", "", "");
            llListen(777, "", NULL_KEY, "");

            llMessageLinked(LINK_THIS, 6877259, (string)enabled, NULL_KEY);
        }

        llMessageLinked(LINK_THIS, 94558323, llList2CSV(agentsInTranslation), "");
        if (isMaster > 0)
        {
            for (x = 0; x < llGetListLength(agentsInTranslation); x += 4)
            {
                tempString = llList2String(llGetObjectDetails(llList2Key(agentsInTranslation, x), [OBJECT_POS]), 0);
                if ((llVecDist(llGetPos(), (vector)tempString) <= 20.0) && (tempString != ""))
                    newList += llList2List(agentsInTranslation, x, x + 3);
            }

            agentsInTranslation = newList;
            if ((llGetUnixTime() - lastHeartBeat) >= 5)
            {
                //Send heartbeat
                sendHeartbeat();
                lastHeartBeat = llGetUnixTime();
            }
        }
        else
        {
            if ((llGetUnixTime() - lastHeartBeat) >= 0 + llGetListLength(agentsInTranslation)*2 + llPow(translatorCount, 1.4) + translatorCount + ((1-llGetRegionTimeDilation()) * 5))
            {
                //Send heartbeat
                sendHeartbeat();
                lastHeartBeat = llGetUnixTime();
            }
        }

        //turn on and off scanner
        if ((autoLanguage) && (isMaster > 0))
        {
            llSensor("", NULL_KEY, AGENT, 20.0, PI);
        }
        //llSetTimerEvent(4 + ((1-llGetRegionTimeDilation()) * 5));
    }

    listen(integer channel, string name, key id, string message)
    {
        integer x;
        string  speakerLanguage;
        string  recepientLanguage;
        integer recepientID;
        integer listPos;
        string  languagePair;
        list    translationCache;
        list    tempList;
        integer ImessageType;
        string  Imessage;
        string  tempString;
        string  tempString2;

        //Multiplexor Code
        if ((channel == broadcastChannel) || (channel == priorityNumber))
        {
            //==========================
            //Process Proxy HTTP Request
            //==========================

            if (channel == priorityNumber)
            {
                if (llStringLength(message) >= 508)
                {
                    if (((integer)message/channel) != 4958654)
                    {
                        sayCachePrivate += [id, message];
                        return;
                    }
                    message = "";
                }
                message = receiveTextBatchPrivate(id, message);
                //Received packet to translate
                llMessageLinked(LINK_ALL_CHILDREN, 6634934, (string)<0.25, 0.05, 0.25>, "");

                tempList = llParseString2List(message, ["~"], []);
                tempString = llList2String(tempList, 0);
                tempList = llDeleteSubList(tempList, 0, 0);

                tempString2 = llDumpList2String(tempList, "|");
                tempList = llCSV2List(tempString);
                listPos = llList2Integer(tempList, 0);
                tempList = llDeleteSubList(tempList, 0, 0);

                checkThrottle(listPos, tempString2, tempList);

                return;
            }

            //=======================
            //Process Global Messages
            //=======================
            if (llStringLength(message) >= 508)
            {
                if (((integer)message/channel) != 4958654)
                {
                    sayCache += [id, message];
                    return;
                }
                message = "";
            }
            message = receiveTextBatch(id, message);

            tempList = llCSV2List(message);

            if (llGetListLength(tempList) >= 2)
            {
                ImessageType = llList2Integer(tempList, 0);
                tempList = llDeleteSubList(tempList, 0, 0);
                Imessage = llList2CSV(tempList);

                llMessageLinked(LINK_ALL_CHILDREN, 6634934, (string)<0.25, 0, 0.25>, "");
                //Process Message Here
                if (ImessageType == 1001)
                {
                    //Incoming Heartbeat
                    if ((integer)Imessage == priorityNumber)
                    {
                        llOwnerSay("Priority Number Conflict!  Resetting Script...");
                        llResetScript(); //Reset if conflicting priority number
                    }
                    listPos = llListFindList(translators, [id]);
                    if (listPos < 0)
                    {
                        translators += [(integer)Imessage, id];
                        if ((isMaster > 0) && (isInitialized))
                        {
                            sendTextBatch((integer)Imessage, llList2CSV([1002, llList2CSV(agentsInTranslation)]));
                            sendTextBatch((integer)Imessage, llList2CSV([1004, options]));
                        }
                    }
                    else
                    {
                        translators = llListReplaceList(translators, [(integer)Imessage], listPos - 1, listPos - 1);
                    }
                }
                else if (ImessageType == 1002)
                {
                    //Incoming agentsInTranslation Master Broadcast
                    if (isMaster == 0)
                    {
                        //llMessageLinked(LINK_THIS, 9458021, Imessage, "");
                        tempList = llCSV2List(Imessage);
                        agentsInTranslation = [];
                        for (x = 0; x < llGetListLength(tempList); x += 4)
                        {
                            agentsInTranslation += [llList2Key(tempList, x), llList2String(tempList, x + 1), llList2Integer(tempList, x + 2), llList2Integer(tempList, x + 3)];
                        }
                    }
                }
                else if (ImessageType == 1003)
                {
                    //Incoming agentsInTranslation dump from Slave
                    tempList = llCSV2List(Imessage);
                    for (x = 0; x < llGetListLength(tempList); x += 4)
                    {
                        addAgent(llList2Key(tempList, x), llList2String(tempList, x + 1), llList2Integer(tempList, x + 2));
                    }
                }
                else if (ImessageType == 1004)
                {
                    //Incoming Preferences
                    options = Imessage;
                    tempList = llCSV2List(options);
                    showTranslation = llList2Integer(tempList, 0);
                    tranObjects = llList2Integer(tempList, 1);
                    autoLanguage = llList2Integer(tempList, 2);

                    llMessageLinked(LINK_THIS, 3342977, Imessage, "");
                }
            }

            return;
        }

        //Translator Engine Code
        if ((llToLower(message) == "translator") && (isMaster > 0))
        {
            llMessageLinked(LINK_THIS, 2540664, message, id);
            return;
        }
        if ((!enabled) && (isMaster == 1)) return;

        if (!tranObjects)
        {
            if (llList2Key(llGetObjectDetails(id, [OBJECT_CREATOR]), 0) != NULL_KEY) return;
        }

        listPos = llListFindList(agentsInTranslation, [id]);
        if (listPos >= 0)
        {
            speakerLanguage = llList2String(agentsInTranslation, listPos + 1);
        }
        else
        {
            speakerLanguage = addNewAgent(id);
        }

        if (speakerLanguage == "xx") return;  //Agent Opt-Out

        llMessageLinked(LINK_ALL_CHILDREN, 6634934, (string)<1, 1, 0>, "");
        //===============================
        //Formulate Translation Requests
        //===============================
        for (x = 0; x < llGetListLength(agentsInTranslation); x += 4)
        {
            //Loop through translation group and do appropriate translations as needed
            recepientID = llList2Integer(agentsInTranslation, x + 3);
            recepientLanguage =  checkLanguage(llList2Key(agentsInTranslation, x + 1));
            if ((speakerLanguage != recepientLanguage) && (recepientLanguage != "") && (recepientLanguage != "xx"))
            {
                languagePair = speakerLanguage + "|" + recepientLanguage;

                listPos = llListFindList(translationCache, [languagePair]);
                if (listPos < 0)
                  translationCache += [languagePair, recepientID];
                else
                  translationCache = llListReplaceList(translationCache, [llList2String(translationCache, listPos + 1) + "@" + (string)recepientID], listPos + 1, listPos + 1);
            }
        }

        //Process Requests
        if (llGetListLength(translationCache) > 0)
        {
            for (x = 0; x < llGetListLength(translationCache); x += 2)
            {
                //====================================
                //Translation
                //====================================
                //Forumulate and Send Translation Request
                languagePair = "|" + llList2String(llParseStringKeepNulls(llList2String(translationCache, x), ["|"],[]), 1);
                checkThrottle(0, llEscapeURL(message) + "&langpair=" + llEscapeURL(languagePair), [llGetTime(), id , llList2String(translationCache, x + 1), llList2String(translationCache, x)]);
            }
        }
        else
            speakerLanguage = "";

        //====================================
        //Language Detection
        //====================================
        if (llList2Key(llGetObjectDetails(id, [OBJECT_CREATOR]), 0) == NULL_KEY)
        {
            if (((speakerLanguage == "") || (llList2Integer(agentsInTranslation, llListFindList(agentsInTranslation, [id]) + 2) == TRUE)) || (isMaster == 2))
            {
                //Forumulate and Send Language Detect Request
                checkThrottle(1, llEscapeURL(message), [llGetTime(), id]);
            }
        }
    }

    http_response(key request_id, integer status, list metadata, string body)
    {
        string  tempString;

        if (status != 200)
        {
            //llOwnerSay("WWW Error:" + (string)status);
            llMessageLinked(LINK_ALL_CHILDREN, 6634934, (string)<1, 0, 0>, "");
            //llOwnerSay(body);
            return;
        }

        //Process Resonse Code
        tempString = llGetSubString(body, llSubStringIndex(body, "\"responseStatus\":"), -1);
        status = (integer)llGetSubString(tempString, 17, llSubStringIndex(tempString, "}") - 1);
        if (status != 200)
        {
            //llOwnerSay("Language Server Returned Error Code: " + (string)status);
            //llOwnerSay(body);
            llMessageLinked(LINK_ALL_CHILDREN, 6634934, (string)<1, 0, 0>, "");
            return;
        }
        llMessageLinked(LINK_ALL_CHILDREN, 6634934, (string)<0, 0, 1>, "");
        llMessageLinked(LINK_THIS, 345149624, body, request_id);
    }
}
```

## HTTP Handler

Even though the name of this script is "HTTP Handler", it really just stores the requested translation traffic so that we can match incoming translations from Google with what was requested.  Since this takes a lot of memory for storage, this information is kept out of the engine script.  When an incoming HTTP response comes in, we fetch the data from here.  If the requests didn't come back in a timely fashion, we remove it from the queue.

```lsl
//HTTP Handler
//Copyright 2006-2009 by Hank Ramos

list requestedTranslations;
list requestedDetections;

default
{
    state_entry()
    {
        llSetTimerEvent(5);
    }

    timer()
    {
        integer x;
        list    newList;
        float timeElapsed;

        for (x = 0; x < llGetListLength(requestedDetections); x += 2)
        {
            timeElapsed = llGetTime() - llList2Float(llCSV2List(llList2String(requestedDetections, x + 1)), 0);
            if (timeElapsed < 60.0)
                newList += llList2List(requestedDetections, x, x + 1);
        }
        requestedDetections = newList;
        newList = [];
        for (x = 0; x < llGetListLength(requestedTranslations); x += 2)
        {
            timeElapsed = llGetTime() - llList2Float(llCSV2List(llList2String(requestedTranslations, x + 1)), 0);
            if (timeElapsed < 60.0)
            {
                newList += llList2List(requestedTranslations, x, x + 1);
            }
        }
        requestedTranslations = newList;
    }

    link_message(integer sender_num, integer num, string str, key id)
    {
        integer listPos;

        if (num == 235365342)
        {
            //Translation
            requestedTranslations += [id, str];
        }
        else if (num == 235365343)
        {
            //Detection
            requestedDetections += [id, str];
        }
        else if (num == 345149624)
        {
            listPos = llListFindList(requestedTranslations, [id]);
            if (listPos >= 0)
            {
                llMessageLinked(LINK_THIS, 345149625, str, llList2String(requestedTranslations, listPos + 1));
                requestedTranslations = llDeleteSubList(requestedTranslations, listPos, listPos + 1);
                return;
            }

            listPos = llListFindList(requestedDetections, [id]);
            if (listPos >= 0)
            {
                llMessageLinked(LINK_THIS, 345149626, str, llList2String(requestedDetections, listPos + 1));
                requestedDetections = llDeleteSubList(requestedDetections, listPos, listPos + 1);
            }
        }
    }
}
```

## Interface Handler

This is the interface, or menu-system of the translator.  It handles all of the numerous dialogs, language selection, etc. of the translator.

```lsl
//Menu System
//Copyright 2006-2009 by Hank Ramos

//Variables
integer randomDialogChannel;
integer lastAttachPoint;
list    detectedAgentKeyList;
list    detectedAgentNameList;
key     agentInDialog;
integer isInitialized = FALSE;
list    agentsInTranslation;
integer translatorCount;

//Options
integer groupAccess    = FALSE;
integer autoLanguage   = TRUE;
integer deviceAttached;
integer enabled        = FALSE;
integer isShowTran     = FALSE;
integer showAgents     = TRUE;
string  displayStringMD5;
integer isMaster = 1;
integer tranObjects = TRUE;

//Constants
list    languages= [
"Chinese-Simple", "Chinese-Trad", "Croatian",
"Bulgarian", "Belarusian", "Catlan",
"Afrikaans", "Albanian", "Arabic",

"Filipino", "French", "Galician",
"Finnish", "English", "Estonian",
"Czech", "Danish", "Dutch",

"Indonesian", "Irish", "Italian",
"Hindi", "Hungarian", "Icelandic",
"German", "Greek", "Hebrew",

"Maltese", "Norwegian", "Persian",
"Lithuanian", "Macedonian", "Malay",
"Japanese", "Korean", "Latvian",

"Slovenian", "Spanish", "Swahili",
"Russian", "Serbian", "Slovak",
"Polish", "Portuguese", "Romanian",

"Yiddish", "\t     ", "\t     ",
"Ukrainian", "Vietnamese", "Welsh",
"Swedish", "Thai", "Turkish"];

list    languageCodes = [
"zh-CN", "zh-TW", "hr",
"bg", "be", "ca",
"af", "sq", "ar",

"tl", "fr", "gl",
"fi", "en", "et",
"cs", "da", "nl",

"id", "ga", "it",
"hi", "hu", "is",
"de", "el", "iw",

"mt", "no", "fa",
"lt", "mk", "ms",
"ja", "ko", "lv",

"sl", "es", "sw",
"ru", "sr", "sk",
"pl", "pt-PT", "ro",

"yi", "", "",
"uk", "vi", "cy",
"sv", "th", "tr"];

//Functions
//Takes in the offsets, and the attach point
vector fn_makePos(integer attach_point, vector offset) {
    if ((attach_point == 31) || (attach_point == 35)) { //center 2 & center
        return <0,0,0>;
    } else if (attach_point == 32) { // Top right
        return ;
    } else if (attach_point == 33) { // Top
        return ;
    } else if (attach_point == 34) { // Top Left
        return ;
    } else if (attach_point == 36) { // Bottom Left
        return ;
    } else if (attach_point == 37) { // Bottom
        return ;
    } else if (attach_point == 38) { // Bottom Right - Baseline
        return offset;
    } else { //Not a HUD point? Then return it's current pos
        return llGetLocalPos();
    }
}

updateDisplay()
{
    string  tempString;
    integer listLength;
    integer x;
    string  agentName;

    if (isInitialized == FALSE) return;
    tempString = "Universal Translator";
    if (isMaster != 1)
        tempString += " (Link-" + (string)(translatorCount + 1) + ")";
    tempString += "\n===============";

    if (enabled)
    {
        listLength = llGetListLength(agentsInTranslation);
        if (((showAgents) && (listLength <= 40)) && (listLength != 0))
        {
            for (x = 0; x < listLength; x += 4)
            {
                agentName = llList2String(llGetObjectDetails(llList2Key(agentsInTranslation, x), [OBJECT_NAME]), 0);
                if (llStringLength(agentName) > 25)
                    agentName = llGetSubString(agentName, 0, 24);
                if (agentName != "")
                    tempString += "\n" + agentName + "(" + llList2String(agentsInTranslation, x + 1) + ")";
            }
        }
        else
        {
            tempString += "\n# Agents Translated: " + (string)llRound(listLength/3);
        }
    }
    else
    {
        tempString += "\n>> Disabled <<";
    }

    if (llMD5String(tempString, 0) != displayStringMD5)
    {
        displayStringMD5 = llMD5String(tempString, 0);
        llSetText(tempString, <1,1,1>, 1);
    }
}

showMainMenu(key id)
{
    if (isInitialized == FALSE) return;
    integer avatarParticipating;
    list buttonList = ["Language", "Help"];
    string dialogMsg = "Main Menu\nLANGUAGE: manually choose your source language. Target languages are detected automatically\nHELP: get help notecard";
    buttonList += "FREE Copy";
    dialogMsg += "\nFREE COPY: receive FREE copy of Universal Translator.";

    if (llList2String(agentsInTranslation, llListFindList(agentsInTranslation, [(string)id]) + 1) != "xx")
    {
        buttonList += "Opt-Out";
        dialogMsg += "\nOPT-OUT: disable receipt of translations";
    }
    else
    {
        buttonList += "Opt-In";
        dialogMsg += "\nOPT-IN: join the translations";
    }

    if (id == llGetOwner())
    {
        buttonList += "Donate";
        dialogMsg += "\nDONATE: donate L$ to the developer of Universal Translator.";
    }
    if ((id == llGetOwner()) || ((groupAccess) && (llSameGroup(id))))
    {
        buttonList += "Reset";
        buttonList += "Options";
        buttonList += "Send Copy";
        dialogMsg += "\nSEND COPY: send FREE copy of Universal Translator.";

        if (enabled)
        {
            buttonList += "Disable";
        }
        else
        {
            buttonList += "Enable";
        }

        dialogMsg += "\nRESET: reset all scripts in translator";
    }

    llDialog(id, dialogMsg, buttonList, randomDialogChannel);
}

showOptionsMenu(key id)
{
    integer avatarParticipating;
    list buttonList = [];
    string dialogMsg = "Options Menu.";
    if (id == llGetOwner())
    {
        if (groupAccess)
        {
            buttonList += "Group OFF";
        }
        else
        {
            buttonList += "Group ON";
        }
        dialogMsg += "\nGROUP: allow group members to admin.";
    }
    if ((id == llGetOwner()) || ((groupAccess) && (llSameGroup(id))))
    {
        buttonList += "Main Menu";
        if (!deviceAttached)
        {
            if (autoLanguage)
            {
                buttonList += "Scan OFF";
            }
            else
            {
                buttonList += "Scan ON";
            }
        }
        dialogMsg += "\nSCAN: scan for Avatars and automatically add to translation matrix.";

        if (isShowTran)
        {
            buttonList += "Echo OFF";
        }
        else
        {
            buttonList += "Echo ON";
        }
        dialogMsg += "\nECHO: show translations of your chat sent to others.";


        if (tranObjects)
        {
            buttonList += "Objects OFF";
        }
        else
        {
            buttonList += "Objects ON";
        }
        dialogMsg += "\nOBJECTS: translate chat of scripted objects";

        if (showAgents)
        {
            buttonList += "Agents OFF";
        }
        else
        {
            buttonList += "Agents ON";
        }
        dialogMsg += "\nAGENTS: show list of agents translated.";
    }

    llDialog(id, dialogMsg, buttonList, randomDialogChannel);
}

showLanguageDialog1(key id)
{
    llDialog(id, "Select your TARGET language...", ["\t", "\t", ">> NEXT"] + llList2List(languages, 0, 8),  randomDialogChannel);
}
showLanguageDialog2(key id)
{
    llDialog(id, "Select your TARGET language..", ["<< BACK", "\t ", ">> NEXT "] + llList2List(languages, 9, 17),  randomDialogChannel);
}
showLanguageDialog3(key id)
{
    llDialog(id, "Select your TARGET language..", ["<< BACK ", "\t  ", ">> NEXT  "] + llList2List(languages, 18, 26),  randomDialogChannel);
}
showLanguageDialog4(key id)
{
    llDialog(id, "Select your TARGET language..", ["<< BACK  ", "\t   ", ">> NEXT   "] + llList2List(languages, 27, 35),  randomDialogChannel);
}
showLanguageDialog5(key id)
{
    llDialog(id, "Select your TARGET language..", ["<< BACK   ", "\t    ", ">> NEXT    "] + llList2List(languages, 36, 44),  randomDialogChannel);
}showLanguageDialog6(key id)
{
    llDialog(id, "Select your TARGET language..", ["<< BACK    ", "\t     ", "\t     "] + llList2List(languages, 45, 53),  randomDialogChannel);
}
processListen(string name, key id, string message)
{
    key listenKey;

    if (llListFindList(languages, [message]) > -1) //Language Selected in Dialog
    {
        if (message != "") llMessageLinked(LINK_THIS, 9384610, llList2String(languageCodes, llListFindList(languages, [message])), id);
    }
    else if (llToLower(message) == "help")
    {
        llGiveInventory(id, "Universal Translator Help");
    }
    else if (message == "Main Menu")
    {
        showMainMenu(id);
    }
    else if (message == "Options")
    {
        showOptionsMenu(id);
    }
    else if (message == "Language")
    {
        showLanguageDialog1(id);
    }
    else if (message == "Opt-In")
    {
        showLanguageDialog1(id);
    }
    else if (message == "Opt-Out")
    {
        llMessageLinked(LINK_THIS, 9384610, "xx", id);
    }
    else if (message == "FREE Copy")
    {
        llMessageLinked(LINK_THIS, 9455209, llKey2Name(id), id);
    }
    if (id == llGetOwner())
    {
        if (message == "Group ON")
        {
            groupAccess = TRUE;
            showMainMenu(id);
        }
        else if (message == "Group OFF")
        {
            groupAccess = FALSE;
            showMainMenu(id);
        }
        else if (message == "Donate")
        {
            llMessageLinked(LINK_THIS, 324235353254, "", llGetOwner());
        }
    }
    if ((id == llGetOwner()) || ((groupAccess) && (llSameGroup(id))))
    {
        if (message == "Reset")
        {
           llResetScript();
        }
        else if (message == "Enable")
        {
            enabled  = TRUE;
            llMessageLinked(LINK_THIS, 8434532, (string)enabled, id);
        }
        else if (message == "Disable")
        {
            enabled  = FALSE;
            llMessageLinked(LINK_THIS, 8434532, (string)enabled, id);
        }
        else if (message == "Echo ON")
        {
            isShowTran = TRUE;
            //llMessageLinked(LINK_THIS, 2734322, (string)isShowTran, id);
        }
        else if (message == "Echo OFF")
        {
            isShowTran = FALSE;
       }
        else if (message == "Objects OFF")
        {
            tranObjects = FALSE;
        }
        else if (message == "Objects ON")
        {
            tranObjects = TRUE;
        }
        else if (message == "Agents OFF")
        {
            showAgents = FALSE;
            llMessageLinked(LINK_THIS, 455832, (string)showAgents, id);
        }
        else if (message == "Agents ON")
        {
            showAgents = TRUE;
            llMessageLinked(LINK_THIS, 455832, (string)showAgents, id);
        }
        else if (message == "Scan ON")
        {
            autoLanguage  = TRUE;
            showMainMenu(id);
        }
        else if (message == "Scan OFF")
        {
            autoLanguage = FALSE;
            showMainMenu(id);
        }
        else if ((message == "Send Copy") || (message == ">>RESCAN<<"))
        {
            agentInDialog = id;
            llSensor("", NULL_KEY, AGENT, 20.0, TWO_PI);
        }
        else
        {
            if (llGetListLength(detectedAgentNameList) > 0)
            {
                listenKey = llList2Key(detectedAgentKeyList, llListFindList(detectedAgentNameList, [message]));
                if (listenKey != "")
                {
                    llMessageLinked(LINK_THIS, 9455209, message, listenKey);
                }
                detectedAgentNameList = [];
            }
        }
    }
    if (message == ">> NEXT")
    {
        showLanguageDialog2(id);
    }
    else if (message == ">> NEXT ")
    {
        showLanguageDialog3(id);
    }
    else if (message == ">> NEXT  ")
    {
        showLanguageDialog4(id);
    }
    else if (message == ">> NEXT   ")
    {
        showLanguageDialog5(id);
    }
    else if (message == ">> NEXT    ")
    {
        showLanguageDialog6(id);
    }
    else if (message == "<< BACK")
    {
        showLanguageDialog1(id);
    }
    else if (message == "<< BACK ")
    {
        showLanguageDialog2(id);
    }
    else if (message == "<< BACK  ")
    {
        showLanguageDialog3(id);
    }
    else if (message == "<< BACK   ")
    {
        showLanguageDialog4(id);
    }
    else if (message == "<< BACK    ")
    {
        showLanguageDialog5(id);
    }
    if (message == "\t")
    {
        showLanguageDialog1(id);
    }
    else if (message == "\t ")
    {
        showLanguageDialog2(id);
    }
    else if (message == "\t  ")
    {
        showLanguageDialog3(id);
    }
    else if (message == "\t   ")
    {
        showLanguageDialog4(id);
    }
    else if (message == "\t    ")
    {
        showLanguageDialog5(id);
    }
    else if (message == "\t     ")
    {
        showLanguageDialog6(id);
    }

    llMessageLinked(LINK_THIS, 3342976, llList2CSV([isShowTran, tranObjects, autoLanguage]), id);
}
checkAttach()
{
    if (llGetAttached() > 0)
    {
        llSetScale(<0.125, 0.125, 0.087>);
        if(lastAttachPoint != llGetAttached())
        {
            llSetPos(fn_makePos(llGetAttached(), <0.00000, 0.13500, 0.15433>));
            llSetRot(<0,0,0,1>);
            lastAttachPoint = llGetAttached();
        }
        llRequestPermissions(llGetOwner(), PERMISSION_TAKE_CONTROLS);
        llMessageLinked(llGetLinkNumber(), 3792114, (string)TRUE, NULL_KEY);
    }
    else
    {
        llSetScale(<0.5, 0.5, 0.750>);
        llReleaseControls();
        llMessageLinked(llGetLinkNumber(), 3792114, (string)FALSE, NULL_KEY);
    }
}

default
{
    run_time_permissions(integer perms)
    {
        //integer hasPerms = llGetPermissions();
        llTakeControls( CONTROL_UP , TRUE, TRUE);
    }
    state_entry()
    {
        //llRequestPermissions(llGetOwner(),PERMISSION_TAKE_CONTROLS );

        string speakerLanguage;
        //llOwnerSay("Welcome to the Universal Translator, the best FREE translator in SL! Please consider making a L$ donation to help with maintenance and further updates. Select DONATE in the translator menu to make a donation.");
        //llSetText("Initializing...", <1,1,1>, 1);

        llSetText("Searching for\nnearby translators...", <1,1,1>, 1);
        checkAttach();

        randomDialogChannel = -(integer)llFrand(2147483647);

        llMessageLinked(LINK_SET, 20957454, "", NULL_KEY);
        llResetOtherScript("Universal Translator Engine");
        llResetOtherScript("HTTP Handler");
        llResetOtherScript("No-Script IM Handler");
        llResetOtherScript("Auto-Update");
        llResetOtherScript("Donation");

        //Other Setup
        llSleep(5);
        llListen(randomDialogChannel, "", NULL_KEY, "");
        llMessageLinked(LINK_THIS, 3342976, llList2CSV([isShowTran, tranObjects, autoLanguage]), "");

        //llOwnerSay("Mem Free=" + (string)llGetFreeMemory());
    }

    on_rez(integer startup_param)
    {
        //checkAttach();
        llResetScript();
    }

    sensor(integer num_detected)
    {
        integer x;
        string  tempString;

        if (num_detected > 11)
            num_detected = 11;

        detectedAgentKeyList = [];
        detectedAgentNameList = [];
        for (x = 0; x < num_detected; x += 1)
        {
             detectedAgentKeyList += llDetectedKey(x);
             tempString = llDetectedName(x);
             if (llStringLength(tempString) > 24) tempString = llGetSubString(tempString, 0, 23);
             detectedAgentNameList += tempString;
        }
        if (llGetListLength(detectedAgentNameList) > 0)
        {
            llDialog(agentInDialog, "Select someone nearby to receive FREE a copy of the Universal Translator...", [">>RESCAN<<"] + detectedAgentNameList, randomDialogChannel);
        }
    }
    link_message(integer sender_num, integer num, string str, key id)
    {
        integer listPos;
        list    tempList;
        string  tempString;

        if (num == 2540664)
        {
            showMainMenu(id);
        }
        else if (num == 3792114)
        {
            deviceAttached = (integer)str;
            if (deviceAttached) autoLanguage = TRUE;
        }
        else if (num == 65635544)
        {
            translatorCount = ((integer)str)/2;
        }
        else if (num == 6877259)
        {
            if (isInitialized == FALSE)
            {
                isInitialized = TRUE;
                //Owner Language Detection
                tempString  = llGetAgentLanguage(llGetOwner());
                if (llGetSubString(tempString, 0, 1) == "en") tempString = "en";

                if (tempString == "")
                {
                    tempString = "en";
                }
                llMessageLinked(LINK_THIS, 9384610, tempString, llGetOwner());
            }

          enabled = (integer)str; //marker
          updateDisplay();
        }
        else if (num == 34829304)
        {
            isMaster = (integer)str;
            updateDisplay();
        }
        else if (num == 455832)
        {
            showAgents = (integer)str;
            updateDisplay();
        }
        else if (num == 94558323)
        {
            agentsInTranslation = llCSV2List(str);
            updateDisplay();
        }
        else if (num == 3342977)
        {
            //Options are Show Tran and tranObjects at this time
            tempList = llCSV2List(str);
            isShowTran = llList2Integer(tempList, 0);
            tranObjects = llList2Integer(tempList, 1);
            autoLanguage = llList2Integer(tempList, 2);
       }
        else if (num == 32364364)
        {
            //Send Options
            llMessageLinked(LINK_THIS, 8434532, (string)enabled, NULL_KEY);
        }
   }

    touch_start(integer num_detected)
    {
        integer x;
        key avatarKey;

        for (x = 0; x < num_detected; x++)
        {
            avatarKey = llDetectedKey(x);
            showMainMenu(avatarKey);
        }
    }

    listen(integer channel, string name, key id, string message)
    {
        processListen(name, id, message);
    }

    attach(key id)
    {
        checkAttach();
        if (id) //tests if it is a valid key and not NULL_KEY
        {
            llRequestPermissions(llGetOwner(),PERMISSION_TAKE_CONTROLS );
        }
    }
    control(key id,integer held, integer change) {
        return;
    }
}
```