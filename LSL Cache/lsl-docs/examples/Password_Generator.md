---
name: "Password Generator"
category: "example"
type: "example"
language: "LSL"
description: "I'm new at contributing content to the wiki, so if I did something wrong, feel free to fix it."
wiki_url: "https://wiki.secondlife.com/wiki/Password_Generator"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

I'm new at contributing content to the wiki, so if I did something wrong, feel free to fix it.

```lsl
//              The most pointless code ever. Completely over-done for such a simple purpose.
//              Syntrax Canucci
//              Attribution — You must attribute the work in the manner specified by the author
//              or licensor (but not in any way that suggests that they endorse you or your use of the work).
//              Noncommercial — You may not use this work for commercial purposes.
//              Share Alike — If you alter, transform, or build upon this work, you may distribute the resulting
//              work only under the same or similar license to this one.
//              http://creativecommons.org/licenses/by-nc-sa/3.0/

list gChars = ["A","B","C","D","E","F","G","H","I","J",
               "K","L","M","N","O","P","Q","R","S","T",
               "U","V","W","X","Y","Z","-","1","2","3",
               "4","5","6","7","8","9","0","-","!","@",
               "#","$","%","^","&","*","(",")","~","_"];
string gPassword;
BuildPassword(){
    integer i;
    integer nLength = llRound(llFrand(20)+5);
    llSetText("Building password...",<1,1,1>,1);
    while(llStringLength(gPassword) < nLength){
        i = llRound(llFrand(1));
        if(i == 1){gPassword = gPassword+llToLower(llList2String(gChars,llRound(llFrand(llGetListLength(gChars)))));}
        else{gPassword = gPassword+llToUpper(llList2String(gChars,llRound(llFrand(llGetListLength(gChars)))));}
    }
    integer churn;
    for(churn=0;churn<5;churn++){ gPassword = gPassword + llStringToBase64(gPassword);}
    gPassword = llStringToBase64(gPassword);
    while(llStringLength(gPassword) > llRound(llFrand(20))){
        integer cut = llRound(llFrand(llStringLength(gPassword)/2));
        gPassword = llDeleteSubString(gPassword,cut,cut+llRound(llFrand(5)));
    }
    list slice;
    while(llStringLength(gPassword) > 0){
        slice = slice+llGetSubString(gPassword,0,0);
        gPassword = llDeleteSubString(gPassword,0,0);
    }
    gPassword = llDumpList2String(llListRandomize(slice,1),"");
    llSetText((string)llStringLength(gPassword)+" characters long\n"+gPassword,<1,1,1>,1);llSay(0,gPassword);gPassword="";
}
default{
   touch_start(integer r){BuildPassword();}
}
```

This does the same thing, just with some extra steps for more randomizing, it also displays what it has built, and what it is building from. I like it better. =D
Password Generator 2.0

```lsl
//              The most pointless code ever. Completely over-done for such a simple purpose.
//              Syntrax Canucci
//              Attribution — You must attribute the work in the manner specified by the author
//              or licensor (but not in any way that suggests that they endorse you or your use of the work).
//              Noncommercial — You may not use this work for commercial purposes.
//              Share Alike — If you alter, transform, or build upon this work, you may distribute the resulting
//              work only under the same or similar license to this one.
//              http://creativecommons.org/licenses/by-nc-sa/3.0/

list gChars = ["A","B","C","D","E","F","G","H","I","J",
               "K","L","M","N","O","P","Q","R","S","T",
               "U","V","W","X","Y","Z","-","1","2","3",
               "4","5","6","7","8","9","0","-","!","@",
               "#","$","%","^","&","*","(",")","~","_"];
list gSlice;
string gPassword;
Text(){llSetText("Building Password...\nCurrent State:\n["+llDumpList2String(gSlice,"],[")+"]\n"+gPassword,<1,1,1>,1);}
BuildPassword(){
    integer i;
    integer nLength = llRound(llFrand(20)+5);
    while(llStringLength(gPassword) < nLength){
        i = llRound(llFrand(1));
        if(i == 1){gPassword = gPassword+llToLower(llList2String(gChars,llRound(llFrand(llGetListLength(gChars)))));}
        else{gPassword = gPassword+llToUpper(llList2String(gChars,llRound(llFrand(llGetListLength(gChars)))));}
        Text();
    }
    integer churn;
    for(churn=0;churn<5;churn++){gPassword = gPassword + llStringToBase64(gPassword);Text();}
    gPassword = llStringToBase64(gPassword);
    while(llStringLength(gPassword) > llRound(llFrand(20))){
        integer cut = llRound(llFrand(llStringLength(gPassword)/2));
        gPassword = llDeleteSubString(gPassword,cut,cut+llRound(llFrand(5)));
        Text();
    }
    gSlice = [];
    while(llStringLength(gPassword) > 0){gSlice = gSlice+llGetSubString(gPassword,0,0);gPassword = llDeleteSubString(gPassword,0,0);Text();}
    gPassword = llStringToBase64(llDumpList2String(llListRandomize(llListRandomize(llListRandomize(gSlice,1),1),1),""));
    while(llStringLength(gPassword) > llRound(llFrand(20))){
        integer cut = llRound(llFrand(llStringLength(gPassword)/2));
        gPassword = llDeleteSubString(gPassword,cut,cut+llRound(llFrand(5)));
        Text();
    }
    gSlice=[];
    while(llStringLength(gPassword) > 0){gSlice = gSlice+llGetSubString(gPassword,0,0);gPassword = llDeleteSubString(gPassword,0,0);Text();}
    gPassword = llDumpList2String(llListRandomize(gSlice,1),"");
    llSetText((string)llStringLength(gPassword)+" characters long\n"+gPassword,<1,1,1>,1);llSay(0,gPassword);gPassword="";
}
default{
   touch_start(integer r){BuildPassword();}
}
```