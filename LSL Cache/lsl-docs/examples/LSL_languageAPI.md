---
name: "LSL_languageAPI"
category: "example"
type: "example"
language: "LSL"
description: "This is an API that will handle chat messages and HUD menus in multiple languages based on language files in notecards. Included are two LSL files, the API itself, a simple example usage script and two language files ( English and French )"
wiki_url: "https://wiki.secondlife.com/wiki/LSL_languageAPI"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

This is an API that will handle chat messages and HUD menus in multiple languages based on language files in notecards.
Included are two LSL files, the API itself, a simple example usage script and two language files ( English and French )

todo: floating text support is not yet included in this script.



```lsl
// LSL_languageAPI
// License: LGPL
// Version: 0.20
// Author: Gypsy Paz

//==============
//    CONFIG
//==============
integer autoLoad = FALSE;    // load the first notecard on CHANGED_INVENTORY
float menuTimeout = 10;     // Set the blue menu time out ( in seconds )

//================================================================================================
//      LINK CODES:
//================================================================================================
list langLinkCodes = [
    "INIT",     0x88000,     //Initialize
    "INIT_R",   0x88001,     //Confirm Initialized
    "LOAD",     0x88002,     //Load Language            lang file name (blank loads first one)
    "LOAD_R",   0x88003,     //Confirm Lanugage Loaded
    "MENU",     0x88004,     //langMenu                  caption|button1|button2|etc...    avkey
    "MENU_R",   0x88005,     //langMenu Response         button    uuid
    "MENU_C",   0x88006,     //Close the menu (turn off the listener)
    "WHISPER",  0x88007,     //langWhisper               message    uuid
    "SAY",      0x88008,     //langSay                   message uuid
    "SHOUT",    0x88009,     //langShout                 message uuid
    "OSAY",     0x8800A,     //langOwnerSay              message uuid
    "IM",       0x8800B,     //langIM                    message|avkey    uuid
    "FTEXT",    0x8800C,     //floating text             message color alpha
    "DUMP",     0x8800D,     //dump lang from memory to chat (for debugging)
    "ERROR",    0x8800E      // return an error message ( not sure how I'll handle this yet
];

//================================================================================================
//      LANGUAGE FUNCTIONS:
//================================================================================================
integer langGetCode(string langCode){
    integer i = llListFindList(langLinkCodes, [langCode]);
    return llList2Integer(langLinkCodes, i+1);
}

// Language Vars
string Language;
list langData;
list langIndex;
string curLangFile;

// llDialog Vars
string  menuCaption;
list    menuButtons;
key     menuUser;
integer menuChannel;
integer menuListener;

// Data Server Vars
integer lines;
integer line;
key request = NULL_KEY;

string translate(string index, string id){
    string val;
    integer i = llListFindList(langIndex,[index]);
    if ( i != ERR_GENERIC ){
        return parse(llList2String(langData,i),id);
    }
    else{
        return ">>>error<<<";
    }
}


string parse(string val, string id){
    // Memory
    integer i;
    i = llSubStringIndex(val,"<>");
    if ( i != ERR_GENERIC ){
        val = llDeleteSubString(val,i,llStringLength("<>")-1);
        val = llInsertString(val,i,(string)llGetFreeMemory());
    }
    i = llSubStringIndex(val,"<>");
    if ( i != ERR_GENERIC ){
        val = llDeleteSubString(val,i,i+llStringLength("<>"));
        val = llInsertString(val,i,llKey2Name((key)id));
    }
    return val;
}

integer processing = FALSE;
processData(string data){
    if ( processing ){
        if ( data == ">>>STOP<<<" ){
            processing = FALSE;
            return;
        }
        string prefix = llGetSubString(data,0,1);
        if ( ( prefix == "//" ) || ( llStringLength(data) == 0 ) ){
            return;
        }
        list s = llParseString2List(data,["|"],[]);
        string cmd = llStringTrim(llList2String(s,0),STRING_TRIM);
        string val = llStringTrim(llList2String(s,1),STRING_TRIM);

        if ( cmd == "!PRINT" ){
            llSay(PUBLIC_CHANNEL,parse(val,""));
        }
        else if ( cmd == "!SET_LANG" ){
            Language = val;
        }
        else{
            integer i = llListFindList(langIndex,[cmd]);
            if ( i == ERR_GENERIC ) return;          //<<<<<<<<<<<<<< this will silently fail missing indexes
            langData = llListReplaceList(langData,[val],i,i);
        }





    }
    else if ( data == ">>>START<<<" ){
        processing = TRUE;
    }
}

dumpData(){
    integer i;
    for ( i=0; i>>error<<<",id);
        }
        state default;
    }


    timer(){
        llSetTimerEvent(0.0);
        llMessageLinked(LINK_THIS,langGetCode("MENU_R"),">>>timeout<<<", menuUser);
        state default;
    }

    link_message(integer sender, integer num, string str, key id){
        if ( num == langGetCode("MENU_C") ){
            llSetTimerEvent(0.0);
            state default;
        }
    }

    state_exit(){
        llSetTimerEvent(0.0);
    }
}

state prep{
    state_entry(){
        if ( llGetInventoryType(curLangFile) == INVENTORY_NOTECARD ){
            request = llGetNumberOfNotecardLines(curLangFile);
            llSetTimerEvent(5.0);
        }
        else{
            llOwnerSay("Error, Language File Does Not Exist");
        }
    }

    dataserver(key query_id, string data){
        if (query_id == request){
            llSetTimerEvent(0.0);
            lines = (integer)data;
            state read;
        }
    }

    timer(){
        state timeout;
    }
}

state read{
    state_entry(){
        line = 0;
        request = llGetNotecardLine(curLangFile, line);
        llSetTimerEvent(5.0);
    }

    dataserver(key query_id, string data){
        if (query_id == request){
            llSetTimerEvent(0.0);
            processData(data);
            line++;
            if ( line <= lines ){
                request = llGetNotecardLine(curLangFile, line);
                llSetTimerEvent(5);
            }
            else{
                state default;
            }
        }
    }

    timer(){
        state timeout;
    }
}

state timeout{
    state_entry(){
        llSetTimerEvent(0.0);
        llSay(PUBLIC_CHANNEL,"Error, reading the language file timed out");
        llMessageLinked(LINK_THIS,51,"error","timeout");
        state default;
    }

}
```



```lsl
//================================================================================================
//   LANGUAGE API:
//------------------------------------------------------------------------------------------------

//================================================================================================
string langName;
list langIndex = [
    "HELLO_WORLD",
    "HELLO_AVATAR",
    "OBJECT_NAME",
    "OWNED_BY",
    "CAPTION",
    "BUTTON_1",
    "BUTTON_2",
    "BUTTON_3",
    "BUTTON_4",
    "BUTTON_5",
    "BUTTON_6"
];

//================================================================================================
//      LINK CODES:
//================================================================================================
list langLinkCodes = [
    "INIT",     0x88000,     //Initialize
    "INIT_R",   0x88001,     //Confirm Initialized
    "LOAD",     0x88002,     //Load Language            lang file name (blank loads first one)
    "LOAD_R",   0x88003,     //Confirm Lanugage Loaded
    "MENU",     0x88004,     //langMenu                  caption|button1|button2|etc...    avkey
    "MENU_R",   0x88005,     //langMenu Response         button    uuid
    "MENU_C",   0x88006,     //Close the menu (turn off the listener)
    "WHISPER",  0x88007,     //langWhisper               message    uuid
    "SAY",      0x88008,     //langSay                   message uuid
    "SHOUT",    0x88009,     //langShout                 message uuid
    "OSAY",     0x8800A,     //langOwnerSay              message uuid
    "IM",       0x8800B,     //langIM                    message|avkey    uuid
    "FTEXT",    0x8800C,     //floating text             message color alpha
    "DUMP",     0x8800D,     //dump lang from memory to chat (for debugging)
    "ERROR",    0x8800E      // return an error message ( not sure how I'll handle this yet
];

//================================================================================================
//      LANGUAGE FUNCTIONS:
//================================================================================================
integer langGetCode(string langCode){
    integer i = llListFindList(langLinkCodes, [langCode]);
    return llList2Integer(langLinkCodes, i+1);
}

langInit(){
    llMessageLinked(LINK_THIS,langGetCode("INIT"),llDumpList2String(langIndex,"|")," ");
}

langLoad(string notecard){
    langName = "";
    llMessageLinked(LINK_THIS,langGetCode("LOAD"),notecard, " ");
}

langWhisper(string msg, key id){
    llMessageLinked(LINK_THIS,langGetCode("WHISPER"),msg,id);
}

langSay(string msg, key id){
    llMessageLinked(LINK_THIS,langGetCode("SAY"),msg,id);
}

langShout(string msg, key id){
    llMessageLinked(LINK_THIS,langGetCode("SHOUT"),msg,id);
}

langMenu(string caption, list buttons, key id){
    llMessageLinked(LINK_THIS,langGetCode("MENU"),caption+"|"+llDumpList2String(buttons,"|"),id);
}

default{
    state_entry(){
        langInit();
    }

    link_message(integer sender, integer num, string msg, key id){
        // Language is initialized
        if ( num == langGetCode("INIT_R") ){
            if ( msg == "ok" ){
                // load the default language (first notecard)
                langLoad("");
            }
            else if ( msg == "error" ){
                // something went wrong
                llOwnerSay((string)id);
            }
        }

        // Language is loaded
        else if ( num == langGetCode("LOAD_R") ){
            if ( msg == "ok" ){
                // load the default language (first notecard)
                langName = (string)id;
            }
            else if ( msg == "error" ){
                // something went wrong
                llOwnerSay((string)id);
            }
llMessageLinked(LINK_THIS,langGetCode("DUMP"),"dump data"," ");
        }

        // Blue Menu Response
        else if ( num == langGetCode("MENU_R") ){
            if ( msg == "BUTTON_1" ){
                langSay("HELLO_AVATAR", id);
            }
            else if ( msg == "BUTTON_2" ){
                langSay("OBJECT_NAME", llGetKey());
            }
            else if ( msg == "BUTTON_3" ){
                langSay("OWNED_BY", llGetOwner());
            }
            else if ( msg == "BUTTON_4" ){
                llMessageLinked(LINK_THIS,langGetCode("DUMP"),"dump"," ");
            }
            else if ( msg == "BUTTON_5" ){
                langLoad("language - ENGLISH");
            }
            else if ( msg == "BUTTON_6" ){
                langLoad("language - FRENCH");
            }
        }
    }

    touch_start(integer n){
        langMenu("CAPTION", ["BUTTON_1", "BUTTON_2", "BUTTON_3", "BUTTON_4", "BUTTON_5", "BUTTON_6"], llDetectedKey(0));

    }

}
```





```lsl
Instructions go up here

>>>START<<<
// start processing the notecard
!SET_LANG   |  Engilish
!PRINT | Loading Language File...

HELLO_WORLD | Hello, I'm a multi-lingual api
HELLO_AVATAR | Hello <>
OBJECT_NAME | I am a <>
OWNED_BY | I belong to <>
CAPTION | Language API Sample, choose your option
BUTTON_1 | Avatar
BUTTON_2 | Object
BUTTON_3 | Owner
BUTTON_4 | Dump
BUTTON_5 | ENGLISH
BUTTON_6 | FRENCH

!PRINT | Language file loaded.
!PRINT | <> bytes free

>>>STOP<<<
```



```lsl
Mettez vos instructions ici

>>>START<<<
// commencez à traiter le notecard
!SET_LANG   |  Francais
!PRINT | Chargement du Dossier de Langue...

HELLO_WORLD | Bonjour, je suis api multilingue
HELLO_AVATAR | Bonjour <>
OBJECT_NAME | Je suis <>
OWNED_BY | J'appartiens à <>
CAPTION | L'Échantillon d'API de langue, choisissez votre option
BUTTON_1 | Avatar
BUTTON_2 | Objet
BUTTON_3 | Propriétaire
BUTTON_4 | Décharge publique

!PRINT | Le dossier de langue a chargé.
!PRINT | octets de <> libres

>>>STOP<<
```