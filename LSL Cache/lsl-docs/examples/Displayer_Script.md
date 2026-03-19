---
name: "Displayer Script"
category: "example"
type: "example"
language: "LSL"
description: "I went ahead and way over complicated this script, but allows for a lot more functionality. You can use way more than seven lines."
wiki_url: "https://wiki.secondlife.com/wiki/Displayer_Script"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

## Overcomplicated C-c-c-c-ombo breaker.

I went ahead and way over complicated this script, but allows for a lot more functionality.
You can use way more than seven lines.

llSetText is always limited to **254 bytes** and will be truncated as such. Be weary of this when using this script.
Essentially unlimited lines *(until script memory runs out)* is irrelevant due to SetText limits.

Whatever, enjoy. -- User:Niles Argus

```lsl
//Created by Niles Argus 2011. The safeParseToTokens(string String) function, is hella useful.

string activationTrigger = "."; //Used to activate the command line. Blank for none.

string DEFAULT_SEPARATOR            =   " : ";

integer ENC_PADDING                 =    0x0;
integer ENC_SQUARE_BRACKETS         =    0x1;
integer ENC_SQUIGLY_BRACKETS        =    0x4;
integer ENC_PARENTHESES             =    0x2;
integer ENC_ARROWS                  =    0x3;

list encapsulatorReference = [
    0x0,    " ",    " ",
    0x1,    "[",     "]",
    0x2,    "(",    ")",
    0x3,    "<",    ">",
    0x4,    "{",    "}"];

string buildEncapsulatorList(){
    string Title = "Encapsulators\n";
    string Lines = "";
    integer L = llGetListLength(encapsulatorReference)/3;
    while(~--L){
        Lines = "\t"+llList2String(encapsulatorReference, L*3)+"\t=>\t"+llList2CSV(llList2List(encapsulatorReference, L*3+1, L*3+2))+"\n"+Lines;
    }
    return Title+Lines;
}

integer registerNewEncapsulator(string Left, string Right){
    if(!~llListFindList(encapsulatorReference, [Left,Right])){
        integer nextInteger = (integer)llListStatistics(LIST_STAT_MAX, llList2ListStrided(encapsulatorReference, 0, -1, 3))+1;
        encapsulatorReference += [nextInteger, Left, Right];
        return nextInteger;
    }
    return 0;
}
string encapsulateString(integer Encapsulator, string String){
    integer    F;
    if(~(F=llListFindList(encapsulatorReference, [Encapsulator]))){
        return llList2String(encapsulatorReference, F+1)+String+llList2String(encapsulatorReference, F+2);
    }
    return String;
}

list displayStrings = [
    //Title, String, Seperator, EncapsulatorId
];
integer displayStride = 4;

editLine(integer Line, string Title, string String, string Sep, integer Enc){
    editLineTitle(Line, Title);
    editLineString(Line, String);
    editLineSeparator(Line, Sep);
    editLineEncapsulator(Line, Enc);
}

addLine(string Title, string String, string Sep, integer Enc){
    displayStrings += [Title, String, Sep, Enc];
}
editLineTitle(integer Line, string Title){
    displayStrings = llListReplaceList(displayStrings, [Title], Line*displayStride, Line*displayStride);
}
editLineString(integer Line, string String){
    displayStrings = llListReplaceList(displayStrings, [String], Line*displayStride+1, Line*displayStride+1);
}
editLineSeparator(integer Line, string Sep){
    displayStrings = llListReplaceList(displayStrings, [Sep], Line*displayStride+2, Line*displayStride+2);
}
editLineEncapsulator(integer Line, integer Enc){
    displayStrings = llListReplaceList(displayStrings, [Enc], Line*displayStride+3, Line*displayStride+3);
}
deleteLine(integer Line){
    displayStrings = llDeleteSubList(displayStrings, Line*displayStride,Line*displayStride+displayStride-1);
}
integer validLine(integer Line){
    return (Line >= 0 && Line < llGetListLength(displayStrings)/displayStride);
}

string buildDisplay(){
    string builtDisplay = "";
    integer Lines = llGetListLength(displayStrings)/displayStride;
    while(~--Lines){
        builtDisplay = encapsulateString(llList2Integer(displayStrings,Lines*displayStride+3),
            llDumpList2String(llList2List(displayStrings,Lines*displayStride,Lines*displayStride+1),llList2String(displayStrings,Lines*displayStride+2))) +
                "\n" + builtDisplay;
    }
    return builtDisplay;
}

updateDisplay(){
    llSetLinkPrimitiveParamsFast(LINK_THIS, [PRIM_TEXT, buildDisplay(), <1,1,1>, 0.9]);
}

list safeParseToTokens(string input){ // Used to parse a string that can handle string interpretation
    list tokens = llParseString2List(input, [" "], ["\"",";"]); // - Used to concatenate two strings
    integer nextQuote = llListFindList( tokens, ["\""] );
    integer termChar = nextQuote + 1 + llListFindList( llList2List( tokens, nextQuote + 1, -1 ), [ ";" ] );
    integer endQuote = nextQuote + 1 + llListFindList( llList2List( tokens, nextQuote + 1, -1 ), [ "\"" ] );
    do{
        if(~nextQuote && !~(endQuote-nextQuote-1)){ //Fault: Quotes don't match up.
            return [-1, "Fault: No end quote."];
        } else if(~nextQuote && ~(termChar-nextQuote-1) && termChar < endQuote && ~(endQuote-nextQuote-1) ){
            // Fault. Read error message.
            return [-1, "Fault: Terminator character before end of string."];
        } else if(nextQuote < endQuote){
            string newString = llDumpList2String( llList2List( tokens, nextQuote+1, endQuote-1), " " );
            if( !(nextQuote+1 < endQuote) )
                newString = "";
            tokens = llListReplaceList( tokens,  [newString], nextQuote, endQuote );
        } else {
            //Something broke.
        }
        nextQuote = llListFindList( tokens, ["\""] );
        termChar = nextQuote + 1 + llListFindList( llList2List( tokens, nextQuote + 1, -1 ), [ ";" ] );
        endQuote = nextQuote + 1 + llListFindList( llList2List( tokens, nextQuote + 1, -1 ), [ "\"" ] );
    }
    while(~nextQuote);
    return tokens;
}

/*
    Commands

    .add "Title of line" "Line String" "Seperator" EncapsulatorId
    .add "Title" "String"
        -Adds a new line with the default seperator and square bracket encapsulators.

    .edit Line# title "New Title"
    .edit Line# string "New String"
    .edit Line# sep "New Seperator"
    .edit Line# enc newEncapsulatorId
    .edit Line# "New Title" "New String" "New Seperator" newEncapsulatorId


    .clear
        -Clears the display

    .delete Line#

    .reg_enc "Left" "Right"
        -Registers a new encapsulator.

    .list_enc
        -List all registered encapsulators.

    .list_display
        -For debugging purposes.


    You can change the activator at the top of the script. Or set it blank.
    In which case either exclude it from your queries entirely, or if it was changed,
    use the new activator in place of the period in the examples.


*/
default{
    on_rez(integer Start){
        //Probably shouldn't reset to prevent data loss.
        //But your choice.
        //llResetScript();
    }
    state_entry(){
        llListen(0, "", llGetOwner(), "");//Will only listen to the owner on channel 0.
    }
    listen(integer Chanenl, string Name, key Uuid, string Data){
        if(activationTrigger == "" || llGetSubString(Data, 0, 0) == activationTrigger){
            list Tokens = safeParseToTokens(llDeleteSubString(Data,0,0));
            if(llList2Integer(Tokens, 0) == -1){
                llOwnerSay("Parse Error: "+llList2String(Tokens, 1));
                return;
            }
            string Command = llToLower(llList2String(Tokens, 0));
            integer Line = (integer)llList2String(Tokens, 1);
            if(Command == "add"){
                if(llGetListLength(Tokens) == 5)
                    addLine(llList2String(Tokens, 1), llList2String(Tokens, 2), llList2String(Tokens, 3), (integer)llList2String(Tokens, 4));
                else
                    addLine(llList2String(Tokens, 1), llList2String(Tokens, 2), DEFAULT_SEPARATOR, ENC_SQUARE_BRACKETS);
            }
            else if(Command == "edit"){
                if(!validLine(Line))return;
                string subCmd = llToLower(llList2String(Tokens, 2));
                if(subCmd == "title")
                    editLineTitle(Line, llList2String(Tokens, 3));
                else if(subCmd == "string")
                    editLineString(Line, llList2String(Tokens, 3));
                else if(subCmd == "sep")
                    editLineSeparator(Line, llList2String(Tokens, 3));
                else if(subCmd == "enc")
                    editLineEncapsulator(Line, (integer)llList2String(Tokens, 3));
                else if(llGetListLength(Tokens) == 6)
                    editLine(Line, llList2String(Tokens, 2), llList2String(Tokens, 3), llList2String(Tokens, 4), (integer)llList2String(Tokens, 5));
                else
                    llOwnerSay("Invalid edit query.");
            }
            else if(Command == "delete"){
                if(!validLine(Line))return;
                deleteLine(Line);
                llOwnerSay("Deleted line number "+(string)Line+".");
            }
            else if(Command == "clear"){
                displayStrings = [];
            }
            else if(Command == "reg_enc"){
                integer Id = 0;
                if((Id=registerNewEncapsulator(llList2String(Tokens,1), llList2String(Tokens,2))) != 0){
                    llOwnerSay("Encapsulator registered with ID '"+(string)Id+"'.");
                }
                else{
                    llOwnerSay("Encapsulator failed to register. Already exists in the reference.");
                }
            }
            else if(Command == "list_display"){
                llOwnerSay(buildDisplay());
            }
            else if(Command == "list_enc"){
                llOwnerSay(buildEncapsulatorList());
            }

            updateDisplay();
        }
    }
}
```





This is a simple 7 line displayer script that is easy to use and if you ask me very useful

<source lang="lsl2">
//Scripting By Akinori Kimagawa feel free to change the titles and commands...enjoy this script

string title;
string line1t;
string line2t;
string line3t;
string line4t;
string line5t;
string line6t;
string line1;
string line2;
string line3;
string line4;
string line5;
string line6;
update()
{
llSetText("["+title+"+]
"+"["+line1t+":"+line1+"]
"+"["+line2t+":"+line2+"]
"+"["+line3t+":"+line3+"]
"+"["+line4t+":"+line4+"]
"+"["+line5t+":"+line5+"]
"+"["+line6t+":"+line6+"]"
,<1,1,1>,50);
}
default
{

```lsl
   state_entry()
   {
       llListen(0,"","","");
       llListen(11,"","","");
       llSetTimerEvent(-0.1);
   }
   timer()
   {
       update();
```

}

```lsl
   listen(integer chnl,string name2,key id,string msg)
```

{

```lsl
   if(chnl == 0)
   {
   if(id == llGetOwner())
   {
    list parse = llParseString2List(msg,["."],[]);
```

string cmnd = llList2String(parse,0);
string part = llList2String(parse,1);

if(cmnd == "stitle")
{

```lsl
   title = part;
```

}
if(cmnd == "sline1")
{

```lsl
   line1 = part;
   llSetObjectName(part);
```

}
if(cmnd == "sline2")
{

```lsl
   line2 = part;
```

}
if(cmnd == "sline3")
{

```lsl
   line3 = part;
```

}
if(cmnd == "sline4")
{

```lsl
   line4 = part;
```

}
if(cmnd == "sline5")
{

```lsl
   line5 = part;
```

}
if(cmnd == "sline6")
{

```lsl
   line6 = part;
```

}
if(cmnd == "sline1t")
{

```lsl
   line1t = part;
```

}
if(cmnd == "sline2t")
{

```lsl
   line2t = part;
```

}
if(cmnd == "sline3t")
{

```lsl
   line3t = part;
```

}
if(cmnd == "sline4t")
{

```lsl
   line4t = part;
```

}
if(cmnd == "sline5t")
{

```lsl
   line5t = part;
```

}
if(cmnd == "sline6t")
{

```lsl
   line6t = part;
   }
  }
 }
}
```

state help
}
state help
{

```lsl
   changed(integer change)
   {
       if(change&CHANGED_OWNER)
       {
           llGiveInventory(llGetOwner(),"HELP NOTE NAME");
       }
   }
```

}