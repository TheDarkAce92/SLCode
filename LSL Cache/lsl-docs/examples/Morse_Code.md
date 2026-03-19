---
name: "Morse Code"
category: "example"
type: "example"
language: "LSL"
description: "The following is a script which you can use to convert to and from morse code. In addition, the script can play morse code. The script was written in LSLEditor. The script should work fine in both mono & LSO."
wiki_url: "https://wiki.secondlife.com/wiki/Morse_Code"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 Description
- 2 Creator
- 3 Contributors
- 4 License
- 5 Disclaimer
- 6 Directions
- 7 Morse Code

Description

The following is a script which you can use to convert to and from morse code. In addition, the script can play morse code. The script was written in LSLEditor. The script should work fine in both mono & LSO.

Creator

- Bobbyb30 Swashbuckler

Contributors

- Stephen C Phillips
- Michael R Ditto

where I based my script off [java source](http://www.omnicron.com/~ford/java/NMorse.java)
If you modify/improve upon the script, please add your name here.

License

The following script is licensed under the GNU GPL V3 license.

```lsl
//    Bobbyb30 Swashbuckler (C) 2009
//    This program is free software: you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation, either version 3 of the License, or
//    (at your option) any later version.
//
//    This program is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License for more details.
//
//    You should have received a copy of the GNU General Public License
//    along with this program.  If not, see .
```

Disclaimer

These programs are distributed in the hope that it will be useful, but **WITHOUT ANY WARRANTY**; without even the implied warranty of **MERCHANTABILITY** or **FITNESS FOR A PARTICULAR PURPOSE**.

Directions

Create a prim and drop the script in. Aside from that it has 3 functions:

- tomorsecode which converts to morse code
- frommorsecode which converts morse code to english
- playmorsecode which plays the morse code

The script should be fairly easy to follow...Enjoy.

Morse Code

```lsl
//***********************************************************************************************************
//                                                                                                          *
//                                            --Morse Code--                                                *
//                                                                                                          *
//***********************************************************************************************************
// www.lsleditor.org  by Alphons van der Heijden (SL: Alphons Jano)
//Creator: Bobbyb30 Swashbuckler
//Attribution: Original java work by Stephen C Phillips (C) 1999 and Michael R Ditto (C) 2001
//Created: March 9, 2007
//Last Modified:  December 3, 2009
//Released: Wed, December 2, 2009
//License: GNU GPL V3
//    Bobbyb30 Swashbuckler (C) 2009
//    This program is free software: you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation, either version 3 of the License, or
//    (at your option) any later version.
//
//    This program is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License for more details.
//
//    You should have received a copy of the GNU General Public License
//    along with this program.  If not, see .
//Some parts taken from http://www.omnicron.com/~ford/java/NMorse.java

//Status: Fully Working/Production Ready
//Version: 1.2.7

//Name: Morse Code.lsl
//Purpose: To be able to convert to and from morse code and be able to play morse code in sound.
//Technical Overview: Uses a list and a string of characters to determine morse code. Uses 2 sounds to play.
//Description: This script will convert to and from morse code and can play morse code.
//Directions: This is meant to be used by scripters...the script has 3 functions which you can use...

//Compatible: Mono & LSL compatible
//Other items required: Correct sound UUIDs for dit and dah.
//Notes: Uses more than standard characters, commented for fellow scripters. Morse code is always capital.
//       Sounds dit and dah made in audacity using tone generator and sin wave
//       dit: Tone generator->frequency:800hz, amplitude:.5, length.05 @ 44.KHz
//       dah: Tone generator->frequency:800hz, amplitude:.5, length.15 @ 44.KHz
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//you may use a period . or a raised dot · or a bullet •
//you may use a dash,(hyphen, or minus) - or underscore _

//from http://www.omnicron.com/~ford/java/NMorse.java
string inputcharacters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.!,:?\\`'-/()\"=+;_$@&  ";

//string characters = "abcdefghijklmnopqrstuvwxyz0123456789.!,?'/()&:;=+-_\"$@";
list morsecodecharacters = [
    ".-",//A
    "-...",//B
    "-.-.",//c
    "-..",//D
    ".",//E
    "..-.",//F
    "--.",//G
    "....",//H
    "..",//I
    ".---",//J
    "-.-",//K
    ".-..",//L
    "--",//M
    "-.",//N
    "---",//O
    ".--.",//P
    "--.-",//Q
    ".-.",//R
    "...",//S
    "-",//T
    "..-",//U
    "...-",//V
    ".--",//W
    "-..-",//X
    "-.--",//Y
    "--..",//Z
    "-----",//0
    ".----",//1
    "..---",//2
    "...--",//3
    "....-",//4
    ".....",//5
    "-....",//6
    "--...",//7
    "---..",//8
    "----.",//9
    ".-.-.-",//. (period)
    "-.-.--",//! -this may not be a standard
    "--..--",//, -comma
    "---...",//: -colon
    "..--..",//? -question mark
    ".----.",//\ -backslash
    ".----.",//` treat ` as '
    ".----.",//' apostrophe
    "-....-",//-
    "-..-.",// /-foward slash , fraction bar
    "-.--.-",//( -Parenthesis open [(]-please note these are the same
    "-.--.-",//) - Parenthesis close [)]
    ".-..-.",//"-quotes
    "-...-",//=
    ".-.-.",//+
    "-.-.-.",//;
    "..--.-",//_
    "...-..-",//$
    ".--.-.",//@
    ".-...",//& Ampersand -http://en.wikipedia.org/wiki/Morse_code
    "/ ",//space //you may rerange the bottom these two spaces so that your morse code does have space for /
    "/"//space-this second space doesn't have a space and is used for converting from morose code
        ];

string tomorsecode(string input)//converts to morse code from english
{
    input = llToUpper(input);//convert to upper as Morse code is in uppper case
    integer counter;
    integer inputlength = llStringLength(input);//speed hack here
    string morsecode;
    do
    {
        integer index = llSubStringIndex(inputcharacters,llGetSubString(input,counter,counter));//get a character
        if(index != -1)//speed hack here
        {//this means the character can be converted to morse code

            //pull out morse character from list and append a space
            morsecode += llList2String(morsecodecharacters,index) + " ";//mem hack here,
        }
        else//unknown character
        {
            morsecode += "?";//add question for unknown character
        }
    }while(++counter  or :\n "
            + "english : this will translate morse code to english\n"
            + "morsecode : this will translate english to morse code\n"
            + "play english : this will play the english in morse code\n"
            + "play morse : this will play the morse code.");
        llOwnerSay("Please input morse code using . (periods) and dashes as -");
        llOwnerSay("I only support the following english characters and their morse code counterparts:\n" + inputcharacters);
        llOwnerSay("Enjoy!");
        llListen(0,"",llGetOwner(),"");//i advise against a 0 listener...but I didn't optimize this part
    }
    listen(integer channel, string name, key id, string msg)//not optimized...for example use
    {
        string cleanmsg = llStringTrim(llToLower(msg),STRING_TRIM);//trim head and tail
        //english
        //012345678
        if(llSubStringIndex(cleanmsg,"english ") == 0)
            llOwnerSay(frommorsecode(llGetSubString(cleanmsg,8,-1)));
        //morsecode
        //01234567891
        else if(llSubStringIndex(cleanmsg,"morsecode ") == 0)
            llOwnerSay(tomorsecode(llGetSubString(cleanmsg,10,-1)));
        //play english
        //01234567891123
        else if(llSubStringIndex(cleanmsg,"play english ") == 0)
            playmorsecode(tomorsecode(llGetSubString(cleanmsg,13,-1)));
        //play morse
        //012345678911
        else if(llSubStringIndex(cleanmsg,"play morse ") == 0)
            playmorsecode(llGetSubString(cleanmsg,11,-1));
    }
    changed(integer change)
    {
        if(change & CHANGED_OWNER)
        {
            llOwnerSay("Under new management...resetting.");
            llResetScript();
        }
    }
}
```