---
name: "XTEA Strong Encryption Implementation"
category: "example"
type: "example"
language: "LSL"
description: "XTEA Strong Encryption Implementation - Linden Scripting Language (LSL) Version 1.0"
wiki_url: "https://wiki.secondlife.com/wiki/XTEA_Strong_Encryption_Implementation"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 Contributors
- 2 License
- 3 Disclaimer
- 4 Documentation

  - 4.1 About TEA
  - 4.2 About this implementation
  - 4.3 Changes

  - 4.3.1 Version 1.1
  - 4.3.2 Version 1.0a - Alpha
  - 4.3.3 Version 1.0
  - 4.4 Future Recommendations
- 5 Code

  - 5.1 Original
  - 5.2 Usage Example
  - 5.3 Optimized
  - 5.4 XTEA LSL <-> PHP
- 6 Test Vectors

  - 6.1 Bouncy Castle C# API
  - 6.2 Test Vectors for TEA and XTEA
  - 6.3 LSL Test

XTEA Strong Encryption Implementation - Linden Scripting Language (LSL)
Version 1.0

Contributors

- [Morse Dillon](http://morsedillon.com/), Author, (morseATmorsedillon.com)
- Strife Onizuka (blindwandererATgmail.com)
- [Dedric Mauriac](http://dedricmauriac.wordpress.com/), Contributor (dedric.mauriacATgmail.com)
- JB_Kraft (php 5 class)

License

This work is licensed under a [Creative Commons Attribution 3.0 Unported License](http://creativecommons.org/licenses/by/3.0/)

You are free:

- **to Share** — to copy, distribute and transmit the work
- **to Remix** — to adapt the work

Under the following conditions

- **Attribution.** You must attribute the work in the manner specified by the author or licensor (but not in any way that suggests that they endorse you or your use of the work).

1. For any reuse or distribution, you must make clear to others the license terms of this work. The best way to do this is with [a link to this web page](http://creativecommons.org/licenses/by/3.0/).
1. Any of the above conditions can be waived if you get permission from the copyright holder.
1. Nothing in this license impairs or restricts the author's moral rights.

Disclaimer

This program is distributed in the hope that it will be useful, but **WITHOUT ANY WARRANTY**; without even the implied warranty of **MERCHANTABILITY** or **FITNESS FOR A PARTICULAR PURPOSE**.

**IF YOU READ ONE THING IN HERE, READ THIS**

It is VERY important to remember that there is no such thing as *cookbook cryptography*!  Simply using this cypher does not guarantee security.  Security is an end-to-end concern and responsibility lies with you to thoroughly examine your project from all possible angles if valuable data is at risk.  If you doubt this, ask any thief how they'd rather break into your house - futzing about with picking a high-security deadbolt on the front door or walking in through the back door that you left open.

Documentation

Included at the end of this source listing is a small bit of example  code that shows the usage.  If you wish to include this implementation in your own work, just replace the example code with your own.  Also, please do not reuse or redistribute this work without including the above text attributing this code to its author Morse Dillon, the above GPL statement, and this documentation.

This is an implementation of the XTEA (eXtended Tiny Encryption Algorithm) block cypher.  (X)TEA is a very good choice of cipher when security is important but computational power is limited.  Although I did a lot of work on this implementation, enormous amounts of credit must be given to the creators of the algorithm and those who came before me to implement it in other languages and computing environments.

*If you do decide to use this code in a project, I'd appreciate hearing about it. You can reach me by e-mail at: morseATmorsedillon.com*

## About TEA

The Tiny Encryption Algorithm ([TEA](http://en.wikipedia.org/wiki/Tiny_Encryption_Algorithm)), was originally designed by David Wheeler and Roger Needham of the Cambridge Computer Laboratory.  The [algorithm](http://www.ftp.cl.cam.ac.uk/ftp/papers/djw-rmn/djw-rmn-tea.html) itself is not subject to any patents.  While the original TEA was found to have some minor weaknesses, the eXtended Tiny Encryption Algorithm ([XTEA](http://en.wikipedia.org/wiki/XTEA)) implemented herein addresses these.

*NOTE: XTEA has been superseded by Corrected Block TEA (XXTEA)*

TEA and its derivatives consist of 64-bit block [Feistel network](http://en.wikipedia.org/wiki/Feistel_cipher) with a 128-bit key.  This implementation uses six cycles, or rounds, which is less than one would like but still provides a reasonable level of security (16 is sufficient while 8 is enough for most applications).  Six is said to achieve theoretically good dispersion, but should more security be desired the number of cycles can easily be modified by changing the CYCLES global variable.  Due to the low execution speed of LSL scripts, it's suggested to make this as low as your comfort level allows.  Encryption time scales linearly with the number of cycles.

## About this implementation

This is a bare bones implementation, and is meant to be included in the body of the script needing encryption facilities or wrapped in a link message handler.  If the latter approach is desired, care should be taken to only send link messages to the prim containing this implementation.  If ALL_PRIMS is used as the destination, one could link a link message listener to the object and intercept clear-text communications.

If you plan to place this code into the same script as that needing encryption facilities, you need only call the following functions:

```lsl
string Encrypt(string clearText)
string Decrypt(string cypherText)
```

Simple as that.

This implementation does not provide any secure key exchange, so in terms of key generation and exchange you're on your own.

The 128-bit key is contained in four LSL integers:  KEY1, KEY2, KEY3, and KEY4.  These are global variables at the beginning of the source and can be set using a method that works for you.

## Changes

### Version 1.1

- Changed to treat Right Shift as if integers were unsigned

### Version 1.0a - Alpha

- General optimization to run faster and use less bytecode.
- Encrypt: Pad works differently, no longer extra characters appended to the output.
- TEAEncrypt: Changed the return type
- ord: Added null support.

### Version 1.0

- Initial Release

## Future Recommendations

- Support UTF-8
- Output to Base64 instead of Hex strings
- Append hash to the message to verify integrity of data
- Hash clear-text passwords into 128 bit keys
- Upgrade to XXTEA

Code

## Original

```lsl

//XTEA Strong Encryption Implementation - Linden Scripting Language (LSL)
//Version 1.0
//Copyright (C) 2007 by Morse Dillon (morseATmorsedillon.com)
//
//This program is free software; you can redistribute it and/or
//modify it under the terms of the GNU General Public License
//as published by the Free Software Foundation; either version 2
//of the License, or (at your option) any later version.
//
//This program is distributed in the hope that it will be useful,
//but WITHOUT ANY WARRANTY; without even the implied warranty of
//MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//GNU General Public License for more details.
//
//You should have received a copy of the GNU General Public License
//along with this program; if not, write to the Free Software
//Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
//02110-1301, USA.
//========================================================================
//
//Included at the end of this source listing is a small bit of example
//code that shows the usage.  If you wish to include this implementation
//in your own work, just replace the example code with your own.  Also,
//please do not reuse or redistribute this work without including the
//above text attributing this code to its author Morse Dillon, the above
//GPL statement, and this documentation.
//
//This is an implentation of the XTEA (eXtended Tiny Encryption Algorithm)
//block cypher.  (X)TEA is a very good choice of cipher when security
//is important but computational power is limited.  Although I did a
//lot of work on this implementation, enormous amounts of credit must
//be given to the creators of the algorithm and those who came before
//me to implement it in other languages and computing environments.
//
//***If you do decide to use this code in a project, I'd appreciate
//hearing about it.  You can reach me by e-mail at:
//morseATmorsedillon.com
//
//
//ABOUT TEA AND XTEA
//------------------
//TEA was originally designed by David Wheeler and Roger Needham
//of the Cambridge Computer Laboratory.  The algorithm itself is not
//subject to any patents.  While the original TEA was found to have
//some minor weaknesses, XTEA (implemented herein) addresses these.
//
//TEA and its derivatives consist of 64-bit block Feistel network
//with a 128-bit key.  This implementation uses six cycles, or rounds,
//which is less than one would like but still provides a reasonable
//level of security (16 is sufficient while 8 is enough for most
//applications).  Six is said to achieve theoretically good dispersion,
//but should more security be desired the number of cycles can easily be
//modified by changing the CYCLES global variable.  Due to the low
//execution speed of LSL scripts, it's suggested to make this as low as
//your comfort level allows.  Encryption time scales linearly with the
//number of cycles.
//
//For more information about XTEA, see the following:
//
//Original Paper by Walker and Needham
//http://www.ftp.cl.cam.ac.uk/ftp/papers/djw-rmn/djw-rmn-tea.html
//
//Wikipedia on TEA
//http://en.wikipedia.org/wiki/Tiny_Encryption_Algorithm
//
//
//ABOUT THIS IMPLEMENTATION
//-------------------------
//This is a barebones implementation, and is meant to be included in
//the body of the script needing encryption facilities or wrapped
//in a link message handler.  If the latter approach is desired, care
//should be taken to only send link messages to the prim containing
//this implementation.  If ALL_PRIMS is used as the destination,
//one could link a link message listener to the object and intercept
//cleartext communications.
//
//If you plan to place this code into the same script as that needing
//encryption facilities, you need only call the following functions:
//
//string Encrypt(string cleartext)
//string Decrypt(string cyphertext)
//
//Simple as that.
//
//This implementation does not provide any secure key exchange, so in
//terms of key generation and exchange you're on your own.
//
//The 128-bit key is contained in four LSL integers:  KEY1, KEY2, KEY3,
//and KEY4.  These are global variables at the beginning of the source
//and can be set using a method that works for you.
//
//
//**************IF YOU READ ONE THING IN HERE, READ THIS*******************
//It is VERY important to remember that there is no such thing as
//'cookbook cryptography'!  Simply using this cypher does not guarantee
//security.  Security is an end-to-end concern and responsibility lies
//with you to thoroughly examine your project from all possible angles
//if valuable data is at risk.  If you doubt this, ask any thief how they'd
//rather break into your house - futzing about with picking a high-security
//deadbolt on the front door or walking in through the back door that you
//left open.

//******************USER-CONFIGURABLE GLOBALS BEGIN HERE*******************

//ENCRYPTION KEYS KEY[1-4]
//These together make up the 128-bit XTEA encryption key.  See the above
//documentation for details.  Whatever you do, don't leave them as the default.
integer KEY1 = 11111111;
integer KEY2 = 22222222;
integer KEY3 = 33333333;
integer KEY4 = 44444444;

//DEBUG_FLAG
//If set to 1, will cause debug text to be printed containing some
//intermediate cleartext/cyphertext and the resultant cyphertext/cleartext.
//Do not leave this enabled in production environments!!!!
integer DEBUG_FLAG = 0;

//COMM_CHANNEL
//Specifies which channel should be used for debug and test harness communication.
integer COMM_CHANNEL = 0;

//CYCLES
//Specifies the number of rounds to be used.  See the above documentation for
//details.
integer CYCLES = 6;

//******************USER-CONFIGURABLE GLOBALS END HERE*********************

//Other Globals
list cypherkey = [];
integer delta = 0x9E3779B9;

//Function: ord
//Returns the index of an ASCII character
integer ord(string chr)
{
    string ASCII = "             \n                    !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~";
    if(llStringLength(chr) != 1) return -1;
    if(chr == " ") return 32;
    return llSubStringIndex(ASCII, chr);
}

//Function: chr
//Returns the ASCII character correspondent to index i
string chr(integer i)
{
    string ASCII = "             \n                    !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~";
    i %= 127;
    return llGetSubString(ASCII, i, i);
}



//Function:  DWord2Hex
//Converts a dword containted in a LSL integer to hexadecimal format.
string DWord2Hex(integer m){

    string result;
    integer i = 0;
    integer index = 0;

    //Define character string [0-F] for use in building the hex.
    string characters = "0123456789ABCDEF";

    //Step through 8 times, for a total of 32 bits, 8 nibbles, and 8 hexadecimal digits.
    for (i = 0; i < 8; i++){
        //Get a nibble by right-shifting and masking off 4 bits.
        index  = (m >> (i * 4)) & 0xF;
        //Grab character from the characters string at index position and add it to the result string.
        result = llInsertString(result, 0, llGetSubString(characters,index,index));
    }

    return result;
}

//Function:  Hex2DWword
//Converts a string containing a hexadecimal number to a dword contained in a LSL integer.
integer Hex2DWord(string m){
    integer result = 0;
    integer i = 0;
    string digit;
    integer value;
    integer index;

    string characters = "0123456789ABCDEF";

    for (i = 0; i < 8; i++){

        index = 8 - (i + 1);
        digit = llGetSubString(m,index,index);

        value = llSubStringIndex(characters, digit);

        result = result | value << (i * 4);

    }

    return result;
}

//Function: Encrypt
//Takes cleartext string, pads and bitpacks it, then encrypts it using TEAEncrypt().
string Encrypt(string cleartext){

        //Initialize variables.
        integer dword1 = 0;
        integer dword2 = 0;
        integer cyphertext_numeric;
        list cypherblock;
        string cyphertext = "";

        //Pad cleartext string to the nearest multiple of 8.
        while(llStringLength(cleartext) & 0x7) {
            cleartext += " ";
        }

        //Define more variables pertaining to while loop.
        integer stringlength = llStringLength(cleartext);
        integer i=0;
        integer character;

        //Step through cleartext string, encrypting it in 64-bit (8 character) blocks.
        while (i < stringlength){

            //Pack dword1 with 4 bytes.  Do so by bit-shifting in each character.
            //4th byte winds up in the most-significant position.
            dword1 =  ord(llGetSubString(cleartext,i,i));
            i++;
            dword1 =  dword1 | (ord(llGetSubString(cleartext,i,i)) << 8);
            i++;
            dword1 =  dword1 | (ord(llGetSubString(cleartext,i,i)) << 16);
            i++;
            dword1 =  dword1 | (ord(llGetSubString(cleartext,i,i)) << 24);
            i++;

            //Do it again, this time for dword2
            dword2 =  ord(llGetSubString(cleartext,i,i));
            i++;
            dword2 =  dword2 | ord(llGetSubString(cleartext,i,i)) << 8;
            i++;
            dword2 =  dword2 | ord(llGetSubString(cleartext,i,i)) << 16;
            i++;
            dword2 =  dword2 | ord(llGetSubString(cleartext,i,i)) << 24;
            i++;

            //Call TEAencrypt() with dword1, dword2, and the cypher key and store result in cypherblock.
            cypherblock = TEAEncrypt(dword1,dword2,cypherkey);

            //Convert dword values from cypherblock to hex and append to cyphertext.
            cyphertext = cyphertext + DWord2Hex(llList2Integer(cypherblock,0)) + DWord2Hex(llList2Integer(cypherblock,1));

            //Reset variables for the next round, just to be safe.
            dword1 = 0;
            dword2 = 0;
            cypherblock = [];

            if(DEBUG_FLAG){
                llOwnerSay("Pre-Crypt DWords: " + (string)dword1 + "," + (string)dword2);
                llOwnerSay("Post-Crypt DWords: " + (string)llList2Integer(cypherblock,1) + "," + (string)llList2Integer(cypherblock,2));
                llOwnerSay("Post-Crypt Hex: " + DWord2Hex(llList2Integer(cypherblock,1)) + "," + DWord2Hex(llList2Integer(cypherblock,2)));
            }

        }

        return cyphertext;
}

//Function: Decrypt
//Takes cyphertext, decrypts it with TEADecrypt(), and unpacks it into a string.
string Decrypt(string cyphertext){

        //Initialize variables.
        string hexvalue1 = "";
        string hexvalue2 = "";
        integer dword1 = 0;
        integer dword2 = 0;
        list clearblock = []; //res
        string cleartext = "";
        integer i;


        //Step through cyphertext string, descrypting it block by block.
        while (i < llStringLength(cyphertext)){

            //Pull first 32 bits worth of hexadecimal into hexvalue1
            hexvalue1 += llGetSubString(cyphertext,i,i + 7);
            i = i + 8;

            //Pull second 32 bits worth of hexadecimal into hexvalue2
            hexvalue2 += llGetSubString(cyphertext,i,i + 7);
            i = i + 8;

            //Convert hexvalues to dwords contained in LSL integers.
            dword1 = Hex2DWord(hexvalue1);
            dword2 = Hex2DWord(hexvalue2);

            //Call TEADecrypt() with dword1, dword2, and the cypher key and store result in clearblock list.
            clearblock = TEADecrypt(dword1, dword2, cypherkey);

            //Append first 4 characters of ASCII to cleartext string.
            //This is done by pulling the decrypted dwords from the clearblock list and looking up their ASCII values.
            cleartext += chr( llList2Integer(clearblock,0) & 0x000000FF);
            cleartext += chr( (llList2Integer(clearblock,0) & 0x0000FF00)  >> 8);
            cleartext += chr( (llList2Integer(clearblock,0) & 0x00FF0000)  >> 16);
            cleartext += chr( (llList2Integer(clearblock,0) & 0xFF000000)  >> 24);

            //Append second 4 characters of ASCII to cleartext string.
            cleartext += chr( llList2Integer(clearblock,1) & 0x000000FF);
            cleartext += chr( (llList2Integer(clearblock,1) & 0x0000FF00)  >> 8);
            cleartext += chr( (llList2Integer(clearblock,1) & 0x00FF0000)  >> 16);
            cleartext += chr( (llList2Integer(clearblock,1) & 0xFF000000)  >> 24);

            //Reset variables for the next two blocks of decrypt.
            hexvalue1 = "";
            hexvalue2 = "";
            dword1 = 0;
            dword2 = 0;
            clearblock = [];

            if(DEBUG_FLAG){
                llOwnerSay("Pre-Decrypt Hex: " + hexvalue1 + "," + hexvalue2);
                llOwnerSay("Pre-Decrypt DWords: " + (string)dword1 + "," + (string)dword2);
                llOwnerSay("Post-Decrypt DWords: " + (string)llList2Integer(clearblock,1) + "," + (string)llList2Integer(clearblock,2));
            }

        }

        return cleartext;
}

//Function: TEAEncrypt
//This is the implementation of XTEA proper.  It takes a block of cleartext
//consisting of two dwords contained in LSL integers and a 128-bit key
//contained in an LSL list of 4 integers.  The function then returns
//the cyphertext in an LSL list of two integers.
list TEAEncrypt(integer dword1, integer dword2,list cypherkey){

            list cryptlist = [];

            //Set n to the number of cycles given in the CYCLES global variable
            integer n = CYCLES;

            integer sum = 0;

            //Operate for the specified number of cycles.
            while (n-- > 0){
                dword1 = dword1 + ( ( dword2 << 4 ^ ((dword2 >> 5) & 0x07FFFFFF) ) + dword2 ^ sum + llList2Integer(cypherkey, (sum & 3) ) );
                sum += delta;
                dword2 = dword2 + ( ( dword1 << 4 ^ ((dword1 >> 5) & 0x07FFFFFF) ) + dword1 ^ sum + llList2Integer(cypherkey, ((sum >> 11) & 3) ) );
            }

            cryptlist = [dword1,dword2];

            return cryptlist;
}

//Function: TEADecrypt
//This is the implementation of XTEA proper.  It takes a block of cyphertext
//consisting of two dwords contained in LSL integers and a 128-bit key
//contained in an LSL list of 4 integers.  The function then returns
//the cleartext in an LSL list of two integers.
list TEADecrypt(integer dword1, integer dword2,list cypherkey){

            list cryptlist = [];

            //Set n to the number of cycles given in the CYCLES global variable
            integer n = CYCLES;

            integer sum = delta * CYCLES;

            //Operate for the specified number of cycles.
            while (n-- > 0){
                dword2 = dword2 - ( ( dword1 << 4 ^ ((dword1 >> 5) & 0x07FFFFFF) ) + dword1 ^ sum + llList2Integer(cypherkey, ((sum >> 11) & 3) ) );
                sum -= delta;
                dword1 = dword1 - ( ( dword2 << 4 ^ ((dword2 >> 5) & 0x07FFFFFF) ) + dword2 ^ sum + llList2Integer(cypherkey, (sum & 3) ) );
            }

            cryptlist = [dword1,dword2];
            return cryptlist;
}
```

## Usage Example

Listens on COMM_CHANNEL for a message and encrypts it, then turns around and decrypts the resultant cypher-text. Object than says the encrypted and decrypted messages to the owner.

```lsl
default
{
    state_entry()
    {
        llListen(COMM_CHANNEL, "", NULL_KEY, "");
        cypherkey = [KEY1,KEY2,KEY3,KEY4];
    }

    listen(integer channel, string name, key id, string message)
    {
        string temp_cyphertext = Encrypt(message);

        string temp_cleartext = Decrypt(temp_cyphertext);

        llOwnerSay("\nOriginal Cleartext: " + message + "\nCyphertext: " + temp_cyphertext + "\nDecrypted Cleartext: " + temp_cleartext);
    }
}
```

## Optimized

This version is untested but if it works should run faster (and be able to handle larger strings).

```lsl
// Include the documentation comments from above (separated here only for easier management)

//XTEA Strong Encryption Implementation - Linden Scripting Language (LSL)
//Version 1.0a Alpha
//Copyright (C) 2007 by Strife Onizuka (blindwandererATgmail.com)
//
//Version 1.0
//Copyright (C) 2007 by Morse Dillon (morseATmorsedillon.com)
//
//This program is free software; you can redistribute it and/or
//modify it under the terms of the GNU General Public License
//as published by the Free Software Foundation; either version 2
//of the License, or (at your option) any later version.
//
//This program is distributed in the hope that it will be useful,
//but WITHOUT ANY WARRANTY; without even the implied warranty of
//MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//GNU General Public License for more details.
//
//You should have received a copy of the GNU General Public License
//along with this program; if not, write to the Free Software
//Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
//02110-1301, USA.
//========================================================================
//
//Included at the end of this source listing is a small bit of example
//code that shows the usage.  If you wish to include this implementation
//in your own work, just replace the example code with your own.  Also,
//please do not reuse or redistribute this work without including the
//above text attributing this code to its author Morse Dillon, the above
//GPL statement, and this documentation.
//
//This is an implentation of the XTEA (eXtended Tiny Encryption Algorithm)
//block cypher.  (X)TEA is a very good choice of cipher when security
//is important but computational power is limited.  Although I did a
//lot of work on this implementation, enormous amounts of credit must
//be given to the creators of the algorithm and those who came before
//me to implement it in other languages and computing environments.
//
//***If you do decide to use this code in a project, I'd appreciate
//hearing about it.  You can reach me by e-mail at:
//morseATmorsedillon.com
//
//
//ABOUT TEA AND XTEA
//------------------
//TEA was originally designed by David Wheeler and Roger Needham
//of the Cambridge Computer Laboratory.  The algorithm itself is not
//subject to any patents.  While the original TEA was found to have
//some minor weaknesses, XTEA (implemented herein) addresses these.
//
//TEA and its derivatives consist of 64-bit block Feistel network
//with a 128-bit key.  This implementation uses six cycles, or rounds,
//which is less than one would like but still provides a reasonable
//level of security (16 is sufficient while 8 is enough for most
//applications).  Six is said to achieve theoretically good dispersion,
//but should more security be desired the number of cycles can easily be
//modified by changing the CYCLES global variable.  Due to the low
//execution speed of LSL scripts, it's suggested to make this as low as
//your comfort level allows.  Encryption time scales linearly with the
//number of cycles.
//
//For more information about XTEA, see the following:
//
//Original Paper by Walker and Needham
//http://www.ftp.cl.cam.ac.uk/ftp/papers/djw-rmn/djw-rmn-tea.html
//
//Wikipedia on TEA
//http://en.wikipedia.org/wiki/Tiny_Encryption_Algorithm
//
//
//ABOUT THIS IMPLEMENTATION
//-------------------------
//This is a barebones implementation, and is meant to be included in
//the body of the script needing encryption facilities or wrapped
//in a link message handler.  If the latter approach is desired, care
//should be taken to only send link messages to the prim containing
//this implementation.  If ALL_PRIMS is used as the destination,
//one could link a link message listener to the object and intercept
//cleartext communications.
//
//If you plan to place this code into the same script as that needing
//encryption facilities, you need only call the following functions:
//
//string Encrypt(string cleartext)
//string Decrypt(string cyphertext)
//
//Simple as that.
//
//This implementation does not provide any secure key exchange, so in
//terms of key generation and exchange you're on your own.
//
//The 128-bit key is contained in four LSL integers:  KEY1, KEY2, KEY3,
//and KEY4.  These are global variables at the beginning of the source
//and can be set using a method that works for you.
//
//
//CHANGES
//-------
//
//1.0a - Alpha
//*General optimization to run faster and use less bytecode.
//*Encrypt: Pad works differently, no longer extra characters appended to the output.
//*TEAEncrypt: Changed the return type
//*ord: Added null support.
//
//1.0
//*Initial Release
//
//
//FUTURE CHANGES
//--------------
//
//It would be nice if it supported UTF-8; but adding that would be alot
//of work. The main issue is the decoding, the bytes would have to be
//reassembled into characters. It would be time consuming. Another possibility
//would be to implement XTEA to output to BASE64 instead of hex strings (also
//time consuming to implement).
//
//
//**************IF YOU READ ONE THING IN HERE, READ THIS*******************
//It is VERY important to remember that there is no such thing as
//'cookbook cryptography'!  Simply using this cypher does not guarantee
//security.  Security is an end-to-end concern and responsibility lies
//with you to thoroughly examine your project from all possible angles
//if valuable data is at risk.  If you doubt this, ask any thief how they'd
//rather break into your house - futzing about with picking a high-security
//deadbolt on the front door or walking in through the back door that you
//left open.

//******************USER-CONFIGURABLE GLOBALS BEGIN HERE*******************

//ENCRYPTION KEYS KEY[1-4]
//These together make up the 128-bit XTEA encryption key.  See the above
//documentation for details.  Whatever you do, don't leave them as the default.
//Don't be stupid and make it obvious like your av's key.
integer KEY1 = 11111111;
integer KEY2 = 22222222;
integer KEY3 = 33333333;
integer KEY4 = 44444444;

//COMM_CHANNEL
//Specifies which channel should be used for debug and test harness communication.
integer COMM_CHANNEL = 0;

//CYCLES
//Specifies the number of rounds to be used.  See the above documentation for
//details.
integer CYCLES = 6;

//******************USER-CONFIGURABLE GLOBALS END HERE*********************

//Other Globals
list cypherkey = [];
integer delta = 0x9E3779B9;

string ASCII = "             \n                    !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~";
string characters = "0123456789ABCDEF";

//Function: ord
//Returns the index of an ASCII character
integer ord(string chr)
{
    if(chr)
    {
        if(llStringLength(chr) > 1) return -1;
        if(chr == " ") return 32;
        return llSubStringIndex(ASCII, chr);
    }
    return 0;
}

//Function: chr
//Returns the ASCII character correspondent to index i
string chr(integer i)
{
    if(i)
        return llGetSubString(ASCII, i %= 127, i);
    return "";
}

//Function:  DWord2Hex
//Converts a dword contained in a LSL integer to hexadecimal format.
string DWord2Hex(integer m)
{
    string result;
    integer i = 0;

    //Define character string [0-F] for use in building the hex.
    //Step through 8 times, for a total of 32 bits, 8 nibbles, and 8 hexadecimal digits.
    do{
        integer index = (m >> i) & 0xF;
        result = llGetSubString(characters, index, index) + result;
    }while((i += 4) < 32);
    return result;
}

//Function: Encrypt
//Takes cleartext string, pads and bitpacks it, then encrypts it using TEAEncrypt().
string Encrypt(string cleartext)
{
    string cyphertext = "";
    integer i = llStringLength(cleartext);
    if((i += (0x7 & -i)))//Pad cleartext string to the nearest multiple of 8.
    {
        //Step through cleartext string backwords, encrypting it in 64-bit (8 character) blocks.
        do{
            //i=~-i is the same as --i, just a bit faster and lighter on bytecode; requires one less stack manipulation.
            //Pack dword1 with 4 bytes.  Do so by bit-shifting in each character.
            //4th byte winds up in the most-significant position.
            integer dword2 =    (    ord(llGetSubString(cleartext,i=~-i,i))      )    |
                                (    ord(llGetSubString(cleartext,i=~-i,i)) << 8 )    |
                                (    ord(llGetSubString(cleartext,i=~-i,i)) << 16)    |
                                (    ord(llGetSubString(cleartext,i=~-i,i)) << 24)    ;

            //Do it again, this time for dword1
            integer dword1 =    (    ord(llGetSubString(cleartext,i=~-i,i))      )    |
                                (    ord(llGetSubString(cleartext,i=~-i,i)) << 8 )    |
                                (    ord(llGetSubString(cleartext,i=~-i,i)) << 16)    |
                                (    ord(llGetSubString(cleartext,i=~-i,i)) << 24)    ;

            //Call TEAencrypt() with dword1, dword2, and the cypher key and store result in cypherblock.

            //Convert dword values from cypherblock to hex and append to cyphertext.
            cyphertext = TEAEncrypt(dword1,dword2,cypherkey) + cyphertext;
        }while(i);
    }
    return cyphertext;
}

//Function: Decrypt
//Takes cyphertext, decrypts it with TEADecrypt(), and unpacks it into a string.
string Decrypt(string cyphertext){

    //Initialize variables.
    string cleartext = "";
    integer i = -llStringLength(cyphertext);

    //Step through cyphertext string, decrypting it block by block.
    if((i -= (0xF & i)))//Pad cyphertext string to the nearest multiple of 16.
    {
        do
        {

            //Convert hexvalues to dwords contained in LSL integers.
            //Call TEADecrypt() with dword1, dword2, and the cypher key and store result in clearblock list.
            list clearblock = TEADecrypt((integer)("0x"+llGetSubString(cyphertext,i, ~-(i -= 8))),
                                         (integer)("0x"+llGetSubString(cyphertext,i, ~-(i -= 8))), cypherkey);

            //Append first 4 characters of ASCII to cleartext string.
            //This is done by pulling the decrypted dwords from the clearblock list and looking up their ASCII values.
            integer t = llList2Integer(clearblock,1);
            cleartext += chr( (t      ) & 0xFF) +
                         chr( (t >> 8 ) & 0xFF) +
                         chr( (t >> 16) & 0xFF) +
                         chr( (t = llList2Integer(clearblock,0) >> 24) & 0xFF) +
                         chr( (t      ) & 0xFF) +
                         chr( (t >> 8 ) & 0xFF) +
                         chr( (t >> 16) & 0xFF) +
                         chr( (t >> 24) & 0xFF) ;
        }while(i);
    }
    return cleartext;
}

//Function: TEADecrypt
//This is the implementation of XTEA proper.  It takes a block of cleartext
//consisting of two dwords contained in LSL integers and a 128-bit key
//contained in an LSL list of 4 integers.  The function then returns
//the cyphertext in an LSL list of two integers.
string TEAEncrypt(integer dword1, integer dword2, list cypherkey_)
{
    if(CYCLES > 0)//$[E20011] /*lslint ignore*/
    {
        //Set n to the number of cycles given in the CYCLES global variable
        integer n = CYCLES;
        integer sum = 0;
        //Operate for the specified number of cycles.
        do{
            dword1 = dword1 + ( ( dword2 << 4 ^ dword2 >> 5 ) + dword2 ^ sum + llList2Integer(cypherkey_, (sum & 3) ) );
            dword2 = dword2 + ( ( dword1 << 4 ^ dword1 >> 5 ) + dword1 ^ sum + llList2Integer(cypherkey_, ((sum += delta) >> 11 & 3) ) );
        }while (n = ~-n);
    }
    return DWord2Hex(dword1) + DWord2Hex(dword2);
}

//Function: TEADecrypt
//This is the implementation of XTEA proper.  It takes a block of cyphertext
//consisting of two dwords contained in LSL integers and a 128-bit key
//contained in an LSL list of 4 integers.  The function then returns
//the cleartext in an LSL list of two integers.
list TEADecrypt(integer dword1, integer dword2,list cypherkey_)
{
    if(CYCLES > 0)//$[E20011] /*lslint ignore*/
    {
        //Set n to the number of cycles given in the CYCLES global variable
        integer n = CYCLES;
        integer sum = delta * CYCLES;
        //Operate for the specified number of cycles.
        do{
            dword2 = dword2 - ( ( dword1 << 4 ^ dword1 >> 5 ) + dword1 ^ sum + llList2Integer(cypherkey_, (sum >> 11 & 3) ) );
            dword1 = dword1 - ( ( dword2 << 4 ^ dword2 >> 5 ) + dword2 ^ sum + llList2Integer(cypherkey_, ((sum -= delta) & 3) ) );
        }while (n = ~-n);
    }
    return [dword1,dword2];
}

//XTEA Usage Example
//Listens on COMM_CHANNEL for a message and encrypts it, then turns around and decrypts the resultant cyphertext.
//Object than says the encrypted and decrypted messages to the owner.
default
{
    state_entry()
    {
        llListen(COMM_CHANNEL, "", NULL_KEY, "");
        cypherkey = [KEY1,KEY2,KEY3,KEY4];
    }

    listen(integer channel, string name, key id, string message)
    {
        string temp_cyphertext = Encrypt(message);

        string temp_cleartext = Decrypt(temp_cyphertext);

        llOwnerSay("\nOriginal Cleartext: " + message + "\nCyphertext: " + temp_cyphertext + "\nDecrypted Cleartext: " + temp_cleartext);
    }
}
```

## XTEA LSL <-> PHP

This is an XTEA implementation that has both LSL and PHP scripts to allow strong encryption not only inside LSL but also between LSL and a PHP serverscript.

For those who want to see this in action with your Web server try these. Be sure that if you  edit these that Rounds and Key Phrase are the same in both LSL and PHP versions.

LSL - PLACE IN PRIM -- Edit to change URL and tosend text.

```lsl
//************************************************//
//* Masa's XTEA encryption/decryption v3         *//
//* Modified by SleightOf Hand for Stability and *//
//* intercommunication with PHP version          *//
//************************************************//
// NOTE: This version only encodes 60 bits per 64-bit block!
// This code is public domain.
// Sleight was here 20070522
// masa was here 20070315
// so was strife 20070315
// so was adz 20070812
//
// This was Modified by SleightOf Hand to allow
// Strong encryption between LSL and PHP.
//************************************************//
//* XTEA IMPLEMENTATION                          *//
//************************************************//

integer XTEA_DELTA      = 0x9E3779B9; // (sqrt(5) - 1) * 2^31
integer xtea_num_rounds = 6;
list    xtea_key        = [0, 0, 0, 0];

// Converts any string to a 32 char MD5 string and then to a list of
// 4 * 32 bit integers = 128 bit Key. MD5 ensures always a specific
// 128 bit key is generated for any string passed.
list xtea_key_from_string( string str )
{
    str = llMD5String(str,0); // Use Nonce = 0
    return [    hexdec(llGetSubString(  str,  0,  7)),
                hexdec(llGetSubString(  str,  8,  15)),
                hexdec(llGetSubString(  str,  16,  23)),
                hexdec(llGetSubString(  str,  24,  31))];
}

// Encipher two integers and return the result as a 12-byte string
// containing two base64-encoded integers.
string xtea_encipher( integer v0, integer v1 )
{
    integer num_rounds = xtea_num_rounds;
    integer sum = 0;
    do {
        // LSL does not have unsigned integers, so when shifting right we
        // have to mask out sign-extension bits.
        v0  += (((v1 << 4) ^ ((v1 >> 5) & 0x07FFFFFF)) + v1) ^ (sum + llList2Integer(xtea_key, sum & 3));
        sum +=  XTEA_DELTA;
        v1  += (((v0 << 4) ^ ((v0 >> 5) & 0x07FFFFFF)) + v0) ^ (sum + llList2Integer(xtea_key, (sum >> 11) & 3));

    } while( --num_rounds );
    //return only first 6 chars to remove "=="'s and compact encrypted text.
    return llGetSubString(llIntegerToBase64(v0),0,5) +
           llGetSubString(llIntegerToBase64(v1),0,5);
}

// Decipher two base64-encoded integers and return the FIRST 30 BITS of
// each as one 10-byte base64-encoded string.
string xtea_decipher( integer v0, integer v1 )
{
    integer num_rounds = xtea_num_rounds;
    integer sum = XTEA_DELTA*xtea_num_rounds;
    do {
        // LSL does not have unsigned integers, so when shifting right we
        // have to mask out sign-extension bits.
        v1  -= (((v0 << 4) ^ ((v0 >> 5) & 0x07FFFFFF)) + v0) ^ (sum + llList2Integer(xtea_key, (sum>>11) & 3));
        sum -= XTEA_DELTA;
        v0  -= (((v1 << 4) ^ ((v1 >> 5) & 0x07FFFFFF)) + v1) ^ (sum + llList2Integer(xtea_key, sum  & 3));
    } while ( --num_rounds );

    return llGetSubString(llIntegerToBase64(v0), 0, 4) +
           llGetSubString(llIntegerToBase64(v1), 0, 4);
}

// Encrypt a full string using XTEA.
string xtea_encrypt_string( string str )
{
    // encode string
    str = llStringToBase64(str);
    // remove trailing =s so we can do our own 0 padding
    integer i = llSubStringIndex( str, "=" );
    if ( i != -1 )
        str = llDeleteSubString( str, i, -1 );

    // we don't want to process padding, so get length before adding it
    integer len = llStringLength(str);

    // zero pad
    str += "AAAAAAAAAA=";

    string result;
    i = 0;

    do {
        // encipher 30 (5*6) bits at a time.
        result += xtea_encipher(
            llBase64ToInteger(llGetSubString(str,   i, i += 4) + "A="),
            llBase64ToInteger(llGetSubString(str, ++i, i += 4) + "A=")
        );
    } while ( ++i < len );

    return result;
}

// Decrypt a full string using XTEA
string xtea_decrypt_string( string str ) {
    integer len = llStringLength(str);
    integer i;
    string result;
    do {
        result += xtea_decipher(
            llBase64ToInteger(llGetSubString(str,   i, i += 5) + "=="),
            llBase64ToInteger(llGetSubString(str, ++i, i += 5) + "==")
        );
    } while ( ++i < len );

    // Replace multiple trailing zeroes with a single one
    i = llStringLength(result) - 1;
    while ( llGetSubString(result, --i, i+1) == "AA" )
        result = llDeleteSubString(result, i+1, i+1);
    return llBase64ToString( result + "====" );
}

key requestid; // just to check if we're getting the result we've asked for; all scripts in the same object get the same replies
string base64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" +

                          "abcdefghijklmnopqrstuvwxyz" +

                          "0123456789+/";
string url = "http:///test-script.php";

default
{
    touch_start(integer number)
    {
        string tosend = "this is a message to send";
        llWhisper(0, "Message to Send = " + tosend);
        xtea_key = xtea_key_from_string("this is a test key");
        string message = xtea_encrypt_string(tosend);
        llWhisper(0, "Message to Server = " + message);
        requestid = llHTTPRequest(url,
            [HTTP_METHOD, "POST",
             HTTP_MIMETYPE, "application/x-www-form-urlencoded"],
            "parameter1=" + llEscapeURL(message));
    }

    http_response(key request_id, integer status, list metadata, string body)
    {
        if (request_id == requestid) {
            llWhisper(0, "Web server sent: " + body);
            integer clean = 0;
            string cleanbody = "";
            while(~llSubStringIndex(base64,llGetSubString(body,clean,clean))){
                cleanbody += llGetSubString(body,clean,clean++);
            }
            llWhisper(0, "Cleaned : " + cleanbody);
            llWhisper(0, "Web server said: " + xtea_decrypt_string( cleanbody ));
        }
    }
}
```

PHP Code - Place on web server at location that LSL URL will be looking for.

```lsl
//************************************************//
//* Sleight's PHP XTEA encryption/decryption v3  *//
//* Modified by SleightOf Hand for Stability and *//
//* intercommunication between PHP & LSL         *//
//************************************************//
// NOTE: This version only encodes 60 bits per 64-bit block!
// This code is public domain.
// Sleight was here 20070522
// masa was here 20070315
// so was strife 20070315
// so was adz 20080812
//
// This was converted from the LSL version by
// SleightOf Hand to allow Strong encryption
// between LSL and PHP. If you find this useful
// any donations appreciated.
//************************************************//
//* XTEA IMPLEMENTATION                          *//
//************************************************//

$_XTEA_DELTA      = 0x9E3779B9; // (sqrt(5) - 1) * 2^31
$_xtea_num_rounds = 6;
$_xtea_key        = array(0, 0, 0, 0);
$_base64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".
           "abcdefghijklmnopqrstuvwxyz".
           "0123456789+/";

// Returns Integer based on 8 byte Base64 Code XXXXXX== (llBase64ToInteger)
function base64_integer($str){
 global $_base64;
 if(strlen($str) != 8) return 0;
 return ((strpos($_base64,$str{0}) << 26)|
 (strpos($_base64,$str{1}) << 20)|
 (strpos($_base64,$str{2}) << 14)|
 (strpos($_base64,$str{3}) << 8) |
 (strpos($_base64,$str{4}) << 2) |
 (strpos($_base64,$str{5}) >> 4));
}

// Returns 8 Byte Base64 code based on 32 bit integer ((llIntegerToBase64)
function integer_base64($int){
 global $_base64;
 if($int != (integer) $int) return 0;
 return  $_base64{($int >> 26 & 0x3F)} .
 $_base64{($int >> 20 & 0x3F)} .
 $_base64{($int >> 14 & 0x3F)} .
 $_base64{($int >> 8 & 0x3F)}  .
 $_base64{($int >> 2 & 0x3F)}  .
 $_base64{($int << 4 & 0x3F)} . "==";
}

//strict 32 bit addition using logic
function binadd($val1 , $val2){
 $tc = $val1 & $val2;
 $ta = $val1 ^ $val2;
 do{
  $tac = ($tc << 1) & 0x0FFFFFFFF;
  $tc = $ta & $tac;
  $ta = $ta ^ $tac;
 }while($tc);
 return $ta; // $ta will now be the result so return it
}

// Converts any string to a 32 char MD5 string and then to a list of
// 4 * 32 bit integers = 128 bit Key.
function xtea_key_from_string( $str ) {
 global $_xtea_key;
 $str = md5($str . ":0"); // Use nonce = 0 in LSL for same output
 $_xtea_key[0] = hexdec(substr($str,0,8));
 $_xtea_key[1] = hexdec(substr($str,8,8));
 $_xtea_key[2] = hexdec(substr($str,16,8));
 $_xtea_key[3] = hexdec(substr($str,24,8));
}

// Encipher two integers and return the result as a 12-byte string
// containing two base64-encoded integers.
function xtea_encipher( $v0 , $v1 ) {
 global  $_xtea_num_rounds , $_xtea_key , $_XTEA_DELTA;
 $num_rounds = $_xtea_num_rounds;
 $sum = 0;
 do {
  // LSL only has 32 bit integers. However PHP automatically changes
  // 32 bit integers to 64 bit floats as necessary. This causes
  // incompatibilities between the LSL Encryption and the PHP
  // counterpart. I got round this by changing all addition to
  // binary addition using logical & and ^ and loops to handle bit
  // carries. This forces the 32 bit integer to remain 32 bits as
  // I mask out any carry over 32 bits. this bring the output of the
  // encrypt routine to conform with the output of its LSL counterpart.

  // LSL does not have unsigned integers, so when shifting right we
  // have to mask out sign-extension bits.

  // calculate ((($v1 << 4) ^ (($v1 >> 5) & 0x07FFFFFF)) + $v1)
  $v0a = binadd((($v1 << 4) ^ (($v1 >> 5) & 0x07FFFFFF)) , $v1);
  // calculate ($sum + $_xtea_key[$sum & 3])
  $v0b = binadd($sum , $_xtea_key[$sum & 3]);
  // Calculate ($v0 + ((($v1 << 4) ^ (($v1 >> 5) & 0x07FFFFFF)) + $v1)
  //            ^ ($sum + $_xtea_key[$sum & 3]))
  $v0 = binadd($v0 , ($v0a  ^ $v0b));

  //Calculate ($sum + $_XTEA_DELTA)
  $sum = binadd($sum , $_XTEA_DELTA);

  //Calculate ((($v0 << 4) ^ (($v0 >> 5) & 0x07FFFFFF)) + $v0)
  $v1a = binadd((($v0 << 4) ^ (($v0 >> 5) & 0x07FFFFFF))  , $v0);
  // Calculate ($sum + $_xtea_key[($sum >>11) & 3])
  $v1b = binadd($sum , $_xtea_key[($sum >>11) & 3]);
  //Calculate ($v1 + ((($v0 << 4) ^ (($v0 >> 5) & 0x07FFFFFF)) + $v0
  //           ^ ($sum & $_xtea_key[($sum >>11) & 3]))
  $v1 = binadd($v1 , ($v1a  ^ $v1b));
 } while( $num_rounds = ~-$num_rounds );
 //return only first 6 chars to remove "=="'s and compact encrypted text.
 return substr(integer_base64($v0),0,6) . substr(integer_base64($v1),0,6);
}

// Decipher two base64-encoded integers and return the FIRST 30 BITS of
// each as one 10-byte base64-encoded string.
function xtea_decipher( $v0, $v1 ) {
 global  $_xtea_num_rounds , $_xtea_key , $_XTEA_DELTA;
 $num_rounds = $_xtea_num_rounds;
 $sum = 0; // $_XTEA_DELTA * $_xtea_num_rounds;
 $tda = $_XTEA_DELTA;
 do{ // Binary multiplication using binary manipulation
  if($num_rounds & 1){
   $sum = binadd($sum , $tda);
  }
  $num_rounds = $num_rounds >> 1;
  $tda = ($tda << 1) & 0x0FFFFFFFF;
 }while($num_rounds);
 $num_rounds = $_xtea_num_rounds; // reset $num_rounds back to its proper setting;

 do {
  // LSL only has 32 bit integers. However PHP automatically changes
  // 32 bit integers to 64 bit floats as necessary. This causes
  // incompatibilities between the LSL Encryption and the PHP
  // counterpart. I got round this by changing all addition to
  // binary addition using logical & and ^ and loops to handle bit
  // carries. This forces the 32 bit integer to remain 32 bits as
  // I mask out any carry over 32 bits. this bring the output of the
  // decrypt routine to conform with the output of its LSL counterpart.
  // Subtractions are handled by using 2's compliment

  // LSL does not have unsigned integers, so when shifting right we
  // have to mask out sign-extension bits.

  // calculate ((($v0 << 4) ^ (($v0 >> 5) & 0x07FFFFFF)) + $v0)
  $v1a = binadd((($v0 << 4) ^ (($v0 >> 5) & 0x07FFFFFF)) , $v0);
  // calculate ($sum + $_xtea_key[($sum>>11) & 3])
  $v1b = binadd($sum , $_xtea_key[($sum>>11) & 3]);
  //Calculate 2's compliment of ($v1a ^ $v1b) for subtraction
  $v1c = binadd((~($v1a ^ $v1b)) , 1);
  //Calculate ($v1 - ((($v0 << 4) ^ (($v0 >> 5) & 0x07FFFFFF)) + $v0)
  //            ^ ($sum + $_xtea_key[($sum>>11) & 3]))
  $v1 = binadd($v1 , $v1c);

  // Calculate new $sum based on $num_rounds - 1
  $tnr = $num_rounds - 1;  // Temp $num_rounds
  $sum = 0; // $_XTEA_DELTA * ($num_rounds - 1);
  $tda = $_XTEA_DELTA;
  do{ // Binary multiplication using binary manipulation
   if($tnr & 1){
    $sum = binadd($sum , $tda);
   }
   $tnr = $tnr >> 1;
   $tda = ($tda << 1) & 0x0FFFFFFFF;
  }while($tnr);

  //Calculate ((($v1 << 4) ^ (($v1 >> 5) & 0x07FFFFFF)) + $v1)
  $v0a = binadd((($v1 << 4) ^ (($v1 >> 5) & 0x07FFFFFF)) , $v1);
  //Calculate ($sum + $_xtea_key[$sum & 3])
  $v0b = binadd($sum , $_xtea_key[$sum & 3]);
  //Calculate 2's compliment of ($v0a ^ $v0b) for subtraction
  $v0c = binadd((~($v0a ^ $v0b)) , 1);
  //Calculate ($v0 - ((($v1 << 4) ^ (($v1 >> 5) & 0x07FFFFFF)) + $v1
  //           ^ ($sum + $_xtea_key[$sum & 3]))
  $v0 = binadd($v0 , $v0c);
 } while ( $num_rounds = ~-$num_rounds );

 return substr(integer_base64($v0), 0, 5) . substr(integer_base64($v1), 0, 5);
}

// Encrypt a full string using XTEA.
function xtea_encrypt_string( $str ) {
 // encode Binany string to Base64
 $str = base64_encode($str);

 // remove trailing =s so we can do our own 0 padding
 $i = strpos($str, '=', 0);
 if ( $i !== FALSE  ){
  $str = substr( $str, 0, $i);
 }
 // we don't want to process padding, so get length before adding it
 $len = strlen($str);
 // zero pad
 $str .= "AAAAAAAAAA=";
 $result = "";
 $i = 0;

 do {
  // encipher 30 (5*6) bits at a time.
  $enc1 = base64_integer(substr($str , $i , 5) . "A==");
  $i += 5;
  $enc2 = base64_integer(substr($str , $i , 5) . "A==");
  $i += 5;
  $result .= xtea_encipher($enc1, $enc2);
 } while ( $i < $len );
 return $result; //Return Encrypted string
}

// Decrypt a full string using XTEA
function xtea_decrypt_string( $str ) {
 global $_base64 ;

 $len = strlen($str);
 $i;
 $result;
 do {
  $dec1 = base64_integer(substr($str , $i , 6)."==");
  $i += 6;
  $dec2 = base64_integer(substr($str , $i , 6)."==");
  $i += 6;
  $result .= xtea_decipher( $dec1, $dec2);
 } while ( $i < $len );

 // Replace multiple trailing zeroes with a single one
 $result = rtrim($result, "A");
 $i = strlen($result);
 $mod = $i%4; //Depending on encoded length different appends are needed
 if($mod == 1) $result .= "A==";
 else if($mod == 2 ) $result .= "==";
 else if($mod == 3) $result .= "=";

 return base64_decode( $result );
}

// Only works with PHP compiled as an Apache module
$headers = apache_request_headers();

$objectName = $headers["X-SecondLife-Object-Name"];
$objectKey     = $headers["X-SecondLife-Object-Key"];
$ownerKey     = $headers["X-SecondLife-Owner-Key"];
$ownerName = $headers["X-SecondLife-Owner-Name"];
$region        = $headers["X-SecondLife-Region"];
// and so on for getting all the other variables ...

//to pull out this headers in other kinds of installations, use this (Adz)
/*
$objectName    = $_SERVER['HTTP_X_SECONDLIFE_OBJECT_NAME'];
$objectKey     = $_SERVER['HTTP_X_SECONDLIFE_OBJECT_KEY'];
$region        = $_SERVER['HTTP_X_SECONDLIFE_REGION'];
$ownerName     = $_SERVER['HTTP_X_SECONDLIFE_OWNER_NAME'];
$ownerKey      = $_SERVER['HTTP_X_SECONDLIFE_OWNER_KEY'];
*/

xtea_key_from_string("this is a test key");
// get things from $_POST[]
// Naturally enough, if this is empty, you won't get anything
$parameter1 = xtea_decrypt_string($_POST["parameter1"]);

echo xtea_encrypt_string($ownerName . " just said " . $parameter1) . "\n";
```

This should result in the following output.

Object whispers: Message to Send = this is a message to send

Object whispers: Message to Server = JSdgCA0FDyhgLlUnSgqMQWkAxz1AzA1vr9zwSEDnCgwJ6GNQ

Object whispers: Web server sent: SVbqNQ5XdkngeUI3bgP+s6eAT6GM4AWnYCYApcfxagrPbxmwiY7WXA4J+gEQ1AYhRQNvcnEwfZSo/AuKVtIw

Object whispers: Cleaned : SVbqNQ5XdkngeUI3bgP+s6eAT6GM4AWnYCYApcfxagrPbxmwiY7WXA4J+gEQ1AYhRQNvcnEwfZSo/AuKVtIw

Object whispers: Web server said: SleightOf Hand just said this is a message to send

PHP 5 class of XTEA

```lsl
<?php
// http://wiki.secondlife.com/wiki/XTEA_Strong_Encryption_Implementation
//************************************************//
//* Sleight's PHP XTEA encryption/decryption v3  *//
//* Modified by SleightOf Hand for Stability and *//
//* intercommunication between PHP & LSL         *//
//************************************************//
// NOTE: This version only encodes 60 bits per 64-bit block!
// This code is public domain.
// Sleight was here 20070522
// masa was here 20070315
// so was strife 20070315
// so was adz 20080812
// gave this some class 20080201 JB Kraft
//
// This was converted from the LSL version by
// SleightOf Hand to allow Strong encryption
// between LSL and PHP. If you find this usefull
// any donations apreciated.
//************************************************//
//* XTEA IMPLEMENTATION                          *//
//************************************************//

/**
 * PHP 5 class to do XTEA crypting
 *
 * $xtea = new XTEA( "mypassword" );
 * $crypted = $xtea->encrypt( "Some bogus string" );
 * echo "Encrypted: " . bin2hex($crypted);
 * echo "Decrypted: " . $xtea->decrypt( $crypted );
 *
 * @package whatevah
 * @author JB Kraft
 **/
class XTEA
{

  private $_XTEA_DELTA      = 0x9E3779B9; // (sqrt(5) - 1) * 2^31
  private $_xtea_num_rounds = 6;
  private $_xtea_key        = array(0, 0, 0, 0);
  private $_base64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

  /**
   * CTOR
   *
   * @param  $passwd the password to use for crypting
   * @author JB Kraft
   **/
  public function __construct( $passwd )
  {
    $this->xtea_key_from_string( $passwd );
  }

  /**
   * Encrypt a full string using XTEA.
   *
   * @param $str the string to encrypt
   * @return the encrypted string
   * @author JB Kraft
   **/
  public function encrypt( $str )
  {
   // encode Binany string to Base64
   $str = base64_encode($str);

   // remove trailing =s so we can do our own 0 padding
   $i = strpos($str, '=', 0);
   if ( $i !== FALSE  ){
    $str = substr( $str, 0, $i);
   }
   // we don't want to process padding, so get length before adding it
   $len = strlen($str);
   // zero pad
   $str .= "AAAAAAAAAA=";
   $result = "";
   $i = 0;

   do {
    // encipher 30 (5*6) bits at a time.
    $enc1 = $this->base64_integer(substr($str , $i , 5) . "A==");
    $i += 5;
    $enc2 = $this->base64_integer(substr($str , $i , 5) . "A==");
    $i += 5;
    $result .= $this->xtea_encipher($enc1, $enc2);
   } while ( $i < $len );
   return $result; //Return Encrypted string
  }

  /**
   * Decrypt a full string using XTEA
   *
   * @param $str the string to decrypt
   * @return the decrypted string
   * @author JB Kraft
   **/
  public function decrypt( $str )
  {
   $len = strlen($str);
   $i = 0;
   $result = '';
   do {
    $dec1 = $this->base64_integer(substr($str , $i , 6)."==");
    $i += 6;
    $dec2 = $this->base64_integer(substr($str , $i , 6)."==");
    $i += 6;
    $result .= $this->xtea_decipher( $dec1, $dec2);
   } while ( $i < $len );

   // Replace multiple trailing zeroes with a single one
   $i = strlen($result);
   while ( substr($result, --$i, 1) == "A" );
   $result = substr($result, 0, $i+1);
   $i = strlen($result);
   $mod = $i%4; //Depending on encoded length diffrent appends are needed
   if($mod == 1) $result .= "A==";
   else if($mod == 2 ) $result .= "==";
   else if($mod == 3) $result .= "=";

   return base64_decode( $result );
  }

  // -----------------------------
  // stuff below here is protected
  // -----------------------------

  // Returns Integer based on 8 byte Base64 Code XXXXXX== (llBase64ToInteger)
  protected function base64_integer($str)
  {
   if(strlen($str) != 8) return 0;
   return ((strpos($this->_base64,$str{0}) << 26)|
   (strpos($this->_base64,$str{1}) << 20)|
   (strpos($this->_base64,$str{2}) << 14)|
   (strpos($this->_base64,$str{3}) << 8) |
   (strpos($this->_base64,$str{4}) << 2) |
   (strpos($this->_base64,$str{5}) >> 4));
  }

  // Returns 8 Byte Base64 code based on 32 bit integer ((llIntegerToBase64)
  protected function integer_base64($int)
  {
   if($int != (integer) $int) return 0;
   return  $this->_base64{($int >> 26 & 0x3F)} .
   $this->_base64{($int >> 20 & 0x3F)} .
   $this->_base64{($int >> 14 & 0x3F)} .
   $this->_base64{($int >> 8 & 0x3F)}  .
   $this->_base64{($int >> 2 & 0x3F)}  .
   $this->_base64{($int << 4 & 0x3F)} . "==";
  }

  //strict 32 bit addition using logic
  protected function binadd($val1 , $val2)
  {
   $tc = $val1 & $val2;
   $ta = $val1 ^ $val2;
   do{
    $tac = ($tc << 1) & 0x0FFFFFFFF;
    $tc = $ta & $tac;
    $ta = $ta ^ $tac;
   }while($tc);
   return $ta; // $ta will now be the result so return it
  }

  // Convers any string to a 32 char MD5 string and then to a list of
  // 4 * 32 bit integers = 128 bit Key.
  protected function xtea_key_from_string( $str )
  {
   $str = md5($str . ":0"); // Use nonce = 0 in LSL for same output
   $this->_xtea_key[0] = hexdec(substr($str,0,8));
   $this->_xtea_key[1] = hexdec(substr($str,8,8));
   $this->_xtea_key[2] = hexdec(substr($str,16,8));
   $this->_xtea_key[3] = hexdec(substr($str,24,8));
  }

  // Encipher two integers and return the result as a 12-byte string
  // containing two base64-encoded integers.
  protected function xtea_encipher( $v0 , $v1 )
  {
   $num_rounds = $this->_xtea_num_rounds;
   $sum = 0;
   do {
    // LSL only has 32 bit integers. However PHP automatically changes
    // 32 bit integers to 64 bit floats as necessary. This causes
    // incompatibilities between the LSL Encryption and the PHP
    // counterpart. I got round this by changing all addition to
    // binary addition using logical & and ^ and loops to handle bit
    // carries. This forces the 32 bit integer to remain 32 bits as
    // I mask out any carry over 32 bits. this bring the output of the
    // encrypt routine to conform with the output of its LSL counterpart.

    // LSL does not have unsigned integers, so when shifting right we
    // have to mask out sign-extension bits.

    // calculate ((($v1 << 4) ^ (($v1 >> 5) & 0x07FFFFFF)) + $v1)
    $v0a = $this->binadd((($v1 << 4) ^ (($v1 >> 5) & 0x07FFFFFF)) , $v1);
    // calculate ($sum + $this->_xtea_key[$sum & 3])
    $v0b = $this->binadd($sum , $this->_xtea_key[$sum & 3]);
    // Calculate ($v0 + ((($v1 << 4) ^ (($v1 >> 5) & 0x07FFFFFF)) + $v1)
    //            ^ ($sum + $this->_xtea_key[$sum & 3]))
    $v0 = $this->binadd($v0 , ($v0a  ^ $v0b));

    //Calculate ($sum + $this->_XTEA_DELTA)
    $sum = $this->binadd($sum , $this->_XTEA_DELTA);

    //Calculate ((($v0 << 4) ^ (($v0 >> 5) & 0x07FFFFFF)) + $v0)
    $v1a = $this->binadd((($v0 << 4) ^ (($v0 >> 5) & 0x07FFFFFF))  , $v0);
    // Calculate ($sum + $this->_xtea_key[($sum >>11) & 3])
    $v1b = $this->binadd($sum , $this->_xtea_key[($sum >>11) & 3]);
    //Calculate ($v1 + ((($v0 << 4) ^ (($v0 >> 5) & 0x07FFFFFF)) + $v0
    //           ^ ($sum & $this->_xtea_key[($sum >>11) & 3]))
    $v1 = $this->binadd($v1 , ($v1a  ^ $v1b));
   } while( $num_rounds = ~-$num_rounds );
   //return only first 6 chars to remove "=="'s and compact encrypted text.
   return substr($this->integer_base64($v0),0,6) . substr($this->integer_base64($v1),0,6);
  }

  // Decipher two base64-encoded integers and return the FIRST 30 BITS of
  // each as one 10-byte base64-encoded string.
  protected function xtea_decipher( $v0, $v1 )
  {
   $num_rounds = $this->_xtea_num_rounds;
   $sum = 0; // $this->_XTEA_DELTA * $this->_xtea_num_rounds;
   $tda = $this->_XTEA_DELTA;
   do{ // Binary multiplication using binary manipulation
    if($num_rounds & 1){
     $sum = $this->binadd($sum , $tda);
    }
    $num_rounds = $num_rounds >> 1;
    $tda = ($tda << 1) & 0x0FFFFFFFF;
   }while($num_rounds);
   $num_rounds = $this->_xtea_num_rounds; // reset $num_rounds back to its propper setting;

   do {
    // LSL only has 32 bit integers. However PHP automatically changes
    // 32 bit integers to 64 bit floats as necessary. This causes
    // incompatibilities between the LSL Encryption and the PHP
    // counterpart. I got round this by changing all addition to
    // binary addition using logical & and ^ and loops to handle bit
    // carries. This forces the 32 bit integer to remain 32 bits as
    // I mask out any carry over 32 bits. this bring the output of the
    // decrypt routine to conform with the output of its LSL counterpart.
    // Subtractions are handled by using 2's compliment

    // LSL does not have unsigned integers, so when shifting right we
    // have to mask out sign-extension bits.

    // calculate ((($v0 << 4) ^ (($v0 >> 5) & 0x07FFFFFF)) + $v0)
    $v1a = $this->binadd((($v0 << 4) ^ (($v0 >> 5) & 0x07FFFFFF)) , $v0);
    // calculate ($sum + $this->_xtea_key[($sum>>11) & 3])
    $v1b = $this->binadd($sum , $this->_xtea_key[($sum>>11) & 3]);
    //Calculate 2's compliment of ($v1a ^ $v1b) for subtraction
    $v1c = $this->binadd((~($v1a ^ $v1b)) , 1);
    //Calculate ($v1 - ((($v0 << 4) ^ (($v0 >> 5) & 0x07FFFFFF)) + $v0)
    //            ^ ($sum + $this->_xtea_key[($sum>>11) & 3]))
    $v1 = $this->binadd($v1 , $v1c);

    // Calculate new $sum based on $num_rounds - 1
    $tnr = $num_rounds - 1;  // Temp $num_rounds
    $sum = 0; // $this->_XTEA_DELTA * ($num_rounds - 1);
    $tda = $this->_XTEA_DELTA;
    do{ // Binary multiplication using binary manipulation
     if($tnr & 1){
      $sum = $this->binadd($sum , $tda);
     }
     $tnr = $tnr >> 1;
     $tda = ($tda << 1) & 0x0FFFFFFFF;
    }while($tnr);

    //Calculate ((($v1 << 4) ^ (($v1 >> 5) & 0x07FFFFFF)) + $v1)
    $v0a = $this->binadd((($v1 << 4) ^ (($v1 >> 5) & 0x07FFFFFF)) , $v1);
    //Calculate ($sum + $this->_xtea_key[$sum & 3])
    $v0b = $this->binadd($sum , $this->_xtea_key[$sum & 3]);
    //Calculate 2's compliment of ($v0a ^ $v0b) for subtraction
    $v0c = $this->binadd((~($v0a ^ $v0b)) , 1);
    //Calculate ($v0 - ((($v1 << 4) ^ (($v1 >> 5) & 0x07FFFFFF)) + $v1
    //           ^ ($sum + $this->_xtea_key[$sum & 3]))
    $v0 = $this->binadd($v0 , $v0c);
   } while ( $num_rounds = ~-$num_rounds );

   return substr($this->integer_base64($v0), 0, 5) . substr($this->integer_base64($v1), 0, 5);
  }

}

?>
```

Test Vectors

These are test vectors to verify that the implementation is working correctly. Although the LSL implementation is for six rounds only, it can easily be changed to verify that the implementation is working as expected. Having a proper implementation allows other systems to communicate using the LSL implementation of XTEA.

## Bouncy Castle C# API

These test vectors are taken from [The Bouncy Castle C# API](http://www.bouncycastle.org/csharp/).

Rounds

Data

Key

Vector

32

0x00000000 0x00000000

0x00000000 0x00000000 0x00000000 0x00000000

0xDEE9D4D8 0xF7131ED9

32

0x01020304 0x05060708

0x00000000 0x00000000 0x00000000 0x00000000

0x065C1B89 0x75C6A816

32

0x00000000 0x00000000

0x01234567 0x12345678 0x23456789 0x3456789A

0x1FF9A026 0x1AC64264

32

0x01020304 0x05060708

0x01234567 0x12345678 0x23456789 0x3456789A

0x8C67155B 0x2EF91EAD

## Test Vectors for TEA and XTEA

These test vectors used are from [Test Vectors for TEA and XTEA](http://www.cix.co.uk/~klockstone/teavect.htm).
They are made by starting with a vector of 6 zeroes, data followed by key, and coding with one cycle then moving the six cyclically so that n becomes n-1 modulo 6.

Round

vector

1

0x00000000
0x9E3779B9
0x00000000
0x00000000
0x00000000
0x00000000

2

0xEC01A1DE
0xAAA0256D
0x00000000
0x00000000
0x00000000
0x00000000

4

0xBC3A7DE2
0x4E238EB9
0x00000000
0x00000000
0xEC01A1DE
0x114F6D74

8

0x31C5FA6C
0x241756D6
0xBC3A7DE2
0x845846CF
0x2794A127
0x6B8EA8B8

16

0x1D8E6992
0x9A478905
0x6A1D78C8
0x08C86D67
0x2A65BFBE
0xB4BD6E46

32

0xD26428AF
0x0A202283
0x27F917B1
0xC1DA8993
0x60E2ACAA
0xA6EB923D

64

0x7A01CBC9
0xB03D6068
0x62EE209F
0x069B7AFC
0x376A8936
0xCDC9E923

## LSL Test

The following code has been imported to LSL to test the vectors with an XTEA implementation. It also makes use of a modified version of the Hex method on this wiki to display the data. Right Shift of signed integers is handed by techniques introduced in the Right_Shift method on this wiki.

```lsl
// XTEA is a version of slightly improved TEA
// The plain or cypher text is in v[0], v[1]
// The key is in k[n], where n = 0 - 3
// The number of coding cycles is given by N and
// the number of decoding cycles is given by -N

list XTEA(list v, list k, integer N) // Replaces TEA's Code and Decode
{
    integer y = llList2Integer(v, 0);
    integer z = llList2Integer(v, 1);
    integer DELTA = 0x9E3779B9;
    integer limit = DELTA * N;
    integer sum = 0;

    if(N > 0) // encrypt
    {
        while(sum != limit)
        {
            y   += (z << 4 ^ ((z >> 5) & 0x07FFFFFF)) + z ^ sum + llList2Integer(k, sum & 3);
            sum += DELTA;
            z   += (y << 4 ^ ((y >> 5) & 0x07FFFFFF)) + y ^ sum + llList2Integer(k, (sum >> 11) & 3);
        }
    }
    else // decrypt
    {
         for(sum = -limit; sum; )
         {   z   -= (y << 4 ^ ((y >> 5) & 0x07FFFFFF)) + y ^ sum + llList2Integer(k, (sum >> 11) & 3);
             sum -= DELTA;
             y   -= (z << 4 ^ ((z >> 5) & 0x07FFFFFF)) + z ^ sum + llList2Integer(k, sum & 3);
         }
    }

    return [y,z];
}
string hex(integer value)
{
    string h = "";
    while (value)
    {
        string c = llGetSubString("0123456789ABCDEF", value & 0xF, value & 0xF);
        h = c + h;
        value = (value >> 4) & 0x0FFFFFFF;
    }
    return "0x" + llGetSubString("00000000" + h, -8, -1);
}
default
{
    state_entry()
    {

        // Bouncy Castle C# API Test Vectors
        list v;
        v = XTEA([0x00000000, 0x00000000], [0x00000000, 0x00000000, 0x00000000, 0x00000000], 32);
        llSay(DEBUG_CHANNEL, hex(llList2Integer(v, 0)) + "\t" + hex(llList2Integer(v, 1)) + "\texpected\t0xDEE9D4D8\t0xF7131ED9");

        v = XTEA([0x01020304, 0x05060708], [0x00000000, 0x00000000, 0x00000000, 0x00000000], 32);
        llSay(DEBUG_CHANNEL, hex(llList2Integer(v, 0)) + "\t" + hex(llList2Integer(v, 1)) + "\texpected\t0x065C1B89\t0x75C6A816");

        v = XTEA([0x00000000, 0x00000000], [0x01234567, 0x12345678, 0x23456789, 0x3456789A], 32);
        llSay(DEBUG_CHANNEL, hex(llList2Integer(v, 0)) + "\t" + hex(llList2Integer(v, 1)) + "\texpected\t0x1FF9A026\t0x1AC64264");

        v = XTEA([0x01020304, 0x05060708], [0x01234567, 0x12345678, 0x23456789, 0x3456789A], 32);
        llSay(DEBUG_CHANNEL, hex(llList2Integer(v, 0)) + "\t" + hex(llList2Integer(v, 1)) + "\texpected\t0x8C67155B\t0x2EF91EAD");

        // Test Vectors for XTEA

        list pz = [0,0,0,0,0,0,0];
        integer n;
        for (n = 1; n < 65; n++)
        {

            list a = XTEA(llList2List(pz, n, n + 1), llList2List(pz, n + 2, n + 5), n);

            pz = llListReplaceList(pz, a, n, n + 1);

            if (n == (n & -n))                         // if n power of 2
                llSay(DEBUG_CHANNEL,
                    (string)n
                    + "\t" + hex(llList2Integer(pz, n + 0))
                    + "\t" + hex(llList2Integer(pz, n + 1))
                    + "\t" + hex(llList2Integer(pz, n + 2))
                    + "\t" + hex(llList2Integer(pz, n + 3))
                    + "\t" + hex(llList2Integer(pz, n + 4))
                    + "\t" + hex(llList2Integer(pz, n + 5))
                );
            pz = llListReplaceList(pz, llList2List(pz, n, n + 5), n + 6, n + 11);
        }
    }
}
```