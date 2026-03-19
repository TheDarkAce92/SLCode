---
name: "Faster XTEA Base16 Base64"
category: "example"
type: "example"
language: "LSL"
description: "Second revision: Added 7 bit base64 cipher."
wiki_url: "https://wiki.secondlife.com/wiki/Faster_XTEA_Base16_Base64"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Second revision: Added 7 bit base64 cipher.

```lsl
///////////////////////////////////////////////////////////////////////////////
//
// Faster XTEA Library for LSL
// ---------------------------
//
// (Also with a sane license [BSD], considering that we can't link shared
//  objects in LSL, lol)
//
// To use it, set your passphrase below.  If you're not as worried about speed
//  and want more security, you may want to set the number of passes to 12 or
//  16 as well.
//
// Base16 (Hex) and Base64 functions are included.  The base64 functions seem
//  usually to be much much faster, but the base64 cipher operates on 32-bit
//  blocks, instead of the entire bitstream, which is technically incorrect,
//  so keep that in mind if you're sending data offworld into some magical
//  base64 XTEA script somewhere.  If you want to correct that and it doesn't
//  slow things down too much, I'll send you a virtual cookie.  It's perfectly
//  safe to delete whichever one you're not using, since LSL isn't smart enough
//  to optimize out unused code.
//
// There's also a 7-bit ASCII base64 function pair included that packs an extra
//  character into each 128bits, but is not 8-bit clean (well neither are the
//  others at the moment, lol).  It is slightly slower than the other base64
//  function pair, but is included in case someone decides to implement base64
//  conversion on the whole bit-stream instead of just 32bit blocks.  The 7-bit
//  encoding only wastes one byte per 72 characters, so it should result in far
//  shorter ciphertext if the base64 encoding is made "proper".
//
// The nonce is provided for timestamping and sequence numbering.  If you don't
//  use it, just pass zero there.
//
// If you want to contact me about this code, or about paying me to script
//  something for you (lol), email ceawlin.creations@gmail.com, IM Liandra
//  Ceawlin on the LL main grid, or do a places search for Ceawlin Creations
//  and visit my freebie store.
//
///////////////////////////////////////////////////////////////////////////////
//
// Oh yea, we can't forget the legalese.  What all the stuff below basically
//  means is: You can use this code however you want, and redistribute it with
//  or without modify permissions, but you have to leave this license here, or
//  if you distribute something no-modify that uses it, the object and/or
//  documentation accompanying it have to say, in a conspicuous place, something
//  along the lines of: "Portions of this program are Copyright (c) 2008 Ceawlin
//  Creations, and the following restrictions apply to those parts", and include
//  the below text.
//
// Anyway, here's the legalese.  Lol.
//
// Copyright (c) 2008, Ceawlin Creations
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
//
//     * Redistributions of source code must retain the above copyright notice,
// this list of conditions and the following disclaimer.
//     * Redistributions in binary form must reproduce the above copyright
// notice, this list of conditions and the following disclaimer in the
// documentation and/or other materials provided with the distribution.
//     * Neither the name of Ceawlin Creations, Liandra Ceawlin, or A. J. Taylor,
// nor the names of its contributors may be used to endorse or promote products
// derived from this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
// AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
// IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
// ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
// LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
// CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
// SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
// INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
// CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
// ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
// POSSIBILITY OF SUCH DAMAGE.
//
///////////////////////////////////////////////////////////////////////////////

string  SECRET = "Put your passphrase here.";
integer PASSES = 6;

list ASCII_TABLE = [    "",  "",  "",  "",  "",  "",  "",  "",
                        "",  "",  "",  "",  "", "\n", "",  "",
                        "",  "",  "",  "",  "",  "",  "",  "",
                        "",  "",  "",  "",  "",  "",  "",  "",
                        " ", "!","\"", "#", "$", "%", "&", "'",
                        "(", ")", "*", "+", ",", "-", ".", "/",
                        "0", "1", "2", "3", "4", "5", "6", "7",
                        "8", "9", ":", ";", "<", "=", ">", "?",
                        "@", "A", "B", "C", "D", "E", "F", "G",
                        "H", "I", "J", "K", "L", "M", "N", "O",
                        "P", "Q", "R", "S", "T", "U", "V", "W",
                        "X", "Y", "Z", "[","\\", "]", "^", "_", /*"/**/
                        "`", "a", "b", "c", "d", "e", "f", "g",
                        "h", "i", "j", "k", "l", "m", "n", "o",
                        "p", "q", "r", "s", "t", "u", "v", "w",
                        "x", "y", "z", "{", "|", "}", "~", ""  ];

list BASE16_TABLE = [   "0","1","2","3","4","5","6","7",
                        "8","9","a","b","c","d","e","f" ];

string XTEAEncryptBase16( string clear, integer nonce )
{
    string  md5 = llMD5String( SECRET, nonce );
    list    k = [   (integer)("0x"+llGetSubString(md5,0,7)),
                    (integer)("0x"+llGetSubString(md5,8,15)),
                    (integer)("0x"+llGetSubString(md5,16,23)),
                    (integer)("0x"+llGetSubString(md5,24,31)) ];
    integer w1;
    integer w2;
    string  cipher;
    integer len = llStringLength( clear );
    integer i;
    integer n;
    integer sum;
    for( i=0; i>5)+w2^sum+llList2Integer(k,(sum&3)));
            w2 = w2+((w1<<4^w1>>5)+w1^sum+llList2Integer(k,((sum+=0x9E3779B9)>>11&3)));
        } while( n = ~-n );
        cipher = cipher +
            llList2String( BASE16_TABLE, ((w1>>28)&0xf) ) +
            llList2String( BASE16_TABLE, ((w1>>24)&0xf) ) +
            llList2String( BASE16_TABLE, ((w1>>20)&0xf) ) +
            llList2String( BASE16_TABLE, ((w1>>16)&0xf) ) +
            llList2String( BASE16_TABLE, ((w1>>12)&0xf) ) +
            llList2String( BASE16_TABLE, ((w1>>8)&0xf) ) +
            llList2String( BASE16_TABLE, ((w1>>4)&0xf) ) +
            llList2String( BASE16_TABLE, ((w1>>0)&0xf) ) +
            llList2String( BASE16_TABLE, ((w2>>28)&0xf) ) +
            llList2String( BASE16_TABLE, ((w2>>24)&0xf) ) +
            llList2String( BASE16_TABLE, ((w2>>20)&0xf) ) +
            llList2String( BASE16_TABLE, ((w2>>16)&0xf) ) +
            llList2String( BASE16_TABLE, ((w2>>12)&0xf) ) +
            llList2String( BASE16_TABLE, ((w2>>8)&0xf) ) +
            llList2String( BASE16_TABLE, ((w2>>4)&0xf) ) +
            llList2String( BASE16_TABLE, ((w2>>0)&0xf) );
    }
    return cipher;
}

string XTEAEncryptBase64( string clear, integer nonce )
{
    string  md5 = llMD5String( SECRET, nonce );
    list    k = [   (integer)("0x"+llGetSubString(md5,0,7)),
                    (integer)("0x"+llGetSubString(md5,8,15)),
                    (integer)("0x"+llGetSubString(md5,16,23)),
                    (integer)("0x"+llGetSubString(md5,24,31)) ];
    integer w1;
    integer w2;
    string  cipher;
    integer len = llStringLength( clear );
    integer i;
    integer n;
    integer sum;
    for( i=0; i>5)+w2^sum+llList2Integer(k,(sum&3)));
            w2 = w2+((w1<<4^w1>>5)+w1^sum+llList2Integer(k,((sum+=0x9E3779B9)>>11&3)));
        } while( n = ~-n );
        cipher = cipher + llGetSubString(llIntegerToBase64(w1),0,5) + llGetSubString(llIntegerToBase64(w2),0,5);
    }
    return cipher;
}

string XTEADecryptBase16( string cipher, integer nonce )
{
    string  md5 = llMD5String( SECRET, nonce );
    list    k = [   (integer)("0x"+llGetSubString(md5,0,7)),
                    (integer)("0x"+llGetSubString(md5,8,15)),
                    (integer)("0x"+llGetSubString(md5,16,23)),
                    (integer)("0x"+llGetSubString(md5,24,31)) ];
    integer w1;
    integer w2;
    string  clear;
    integer i;
    integer len = llStringLength(cipher);
    integer n;
    integer sum;
    integer dc = 0x9E3779B9*PASSES;
    integer ind;
    for( i=0; i>5)+w1^sum+llList2Integer(k,(sum>>11&3)));
            w1 = w1-((w2<<4^w2>>5)+w2^sum+llList2Integer(k,((sum-=0x9E3779B9)&3)));
        } while( n = ~-n );
        clear +=    llList2String(ASCII_TABLE,w1&0x7f) +
                    llList2String(ASCII_TABLE,(w1&0x7f00)>>8) +
                    llList2String(ASCII_TABLE,(w1&0x7f0000)>>16) +
                    llList2String(ASCII_TABLE,(w1&0x7f000000)>>24) +
                    llList2String(ASCII_TABLE,w2&0x7f) +
                    llList2String(ASCII_TABLE,(w2&0x7f00)>>8) +
                    llList2String(ASCII_TABLE,(w2&0x7f0000)>>16) +
                    llList2String(ASCII_TABLE,(w2&0x7f000000)>>24);
    }
    return clear;
}

string XTEADecryptBase64( string cipher, integer nonce )
{
    string  md5 = llMD5String( SECRET, nonce );
    list    k = [   (integer)("0x"+llGetSubString(md5,0,7)),
                    (integer)("0x"+llGetSubString(md5,8,15)),
                    (integer)("0x"+llGetSubString(md5,16,23)),
                    (integer)("0x"+llGetSubString(md5,24,31)) ];
    integer w1;
    integer w2;
    string  clear;
    integer i;
    integer len = llStringLength(cipher);
    integer n;
    integer sum;
    integer dc = 0x9E3779B9*PASSES;
    integer ind;
    for( i=0; i>5)+w1^sum+llList2Integer(k,(sum>>11&3)));
            w1 = w1-((w2<<4^w2>>5)+w2^sum+llList2Integer(k,((sum-=0x9E3779B9)&3)));
        } while( n = ~-n );
        clear +=    llList2String(ASCII_TABLE,w1&0x7f) +
                    llList2String(ASCII_TABLE,(w1&0x7f00)>>8) +
                    llList2String(ASCII_TABLE,(w1&0x7f0000)>>16) +
                    llList2String(ASCII_TABLE,(w1&0x7f000000)>>24) +
                    llList2String(ASCII_TABLE,w2&0x7f) +
                    llList2String(ASCII_TABLE,(w2&0x7f00)>>8) +
                    llList2String(ASCII_TABLE,(w2&0x7f0000)>>16) +
                    llList2String(ASCII_TABLE,(w2&0x7f000000)>>24);
    }
    return clear;
}

string XTEAEncrypt7BitBase64( string clear, integer nonce )
{
    string  md5 = llMD5String( SECRET, nonce );
    list    k = [   (integer)("0x"+llGetSubString(md5,0,7)),
                    (integer)("0x"+llGetSubString(md5,8,15)),
                    (integer)("0x"+llGetSubString(md5,16,23)),
                    (integer)("0x"+llGetSubString(md5,24,31)) ];
    integer w1;
    integer w2;
    string  cipher;
    integer len = llStringLength( clear );
    integer i;
    integer n;
    integer sum;
    for( i=0; i>3);
        w2 =
            (llListFindList(ASCII_TABLE,[llGetSubString(clear,i+4,i+4)])<<29) |
            (llListFindList(ASCII_TABLE,[llGetSubString(clear,i+5,i+5)])<<22) |
            (llListFindList(ASCII_TABLE,[llGetSubString(clear,i+6,i+6)])<<15) |
            (llListFindList(ASCII_TABLE,[llGetSubString(clear,i+7,i+7)])<<8) |
            (llListFindList(ASCII_TABLE,[llGetSubString(clear,i+8,i+8)])<<1);
        n = PASSES;
        sum = 0;
        do
        {
            w1 = w1+((w2<<4^w2>>5)+w2^sum+llList2Integer(k,(sum&3)));
            w2 = w2+((w1<<4^w1>>5)+w1^sum+llList2Integer(k,((sum+=0x9E3779B9)>>11&3)));
        } while( n = ~-n );
        cipher = cipher + llGetSubString(llIntegerToBase64(w1),0,5) + llGetSubString(llIntegerToBase64(w2),0,5);
    }
    return cipher;
}

string XTEADecrypt7BitBase64( string cipher, integer nonce )
{
    string  md5 = llMD5String( SECRET, nonce );
    list    k = [   (integer)("0x"+llGetSubString(md5,0,7)),
                    (integer)("0x"+llGetSubString(md5,8,15)),
                    (integer)("0x"+llGetSubString(md5,16,23)),
                    (integer)("0x"+llGetSubString(md5,24,31)) ];
    integer w1;
    integer w2;
    string  clear;
    integer i;
    integer len = llStringLength(cipher);
    integer n;
    integer sum;
    integer dc = 0x9E3779B9*PASSES;
    integer ind;
    for( i=0; i>5)+w1^sum+llList2Integer(k,(sum>>11&3)));
            w1=w1-((w2<<4^w2>>5)+w2^sum+llList2Integer(k,((sum-=0x9E3779B9)&3)));
        } while( n = ~-n );
        clear +=
            llList2String( ASCII_TABLE, (w1&0xfe000000)>>25 ) +
            llList2String( ASCII_TABLE, (w1&0x1fc0000)>>18 ) +
            llList2String( ASCII_TABLE, (w1&0x3f800)>>11 ) +
            llList2String( ASCII_TABLE, (w1&0x7f0)>>4 ) +
            llList2String(ASCII_TABLE,((w1&0xf)<<3)|(((w2&0xe0000000)>>29)&0x7))+
            llList2String( ASCII_TABLE, (w2&0x1fc00000)>>22 ) +
            llList2String( ASCII_TABLE, (w2&0x3f8000)>>15 ) +
            llList2String( ASCII_TABLE, (w2&0x7f00)>>8 ) +
            llList2String( ASCII_TABLE, (w2&0xfe)>>1 );
    }
    return clear;
}

default
{
    state_entry()
    {
        llListen( 0, "", llGetOwner(), "" );
        llSetText( "Touch me to run a speed test, or say something in chat.", <0,1,0>, 1 );
    }
    touch_start( integer ndet )
    {
        state speed_test;
    }
    listen( integer ch, string n, key id, string msg )
    {
        string s="";
        string e="";
//        s += "O:"+msg+"\n";
        s += "O:"+(string)llStringLength(msg)+"\n";
        e = XTEAEncryptBase64( msg, 0 );
//        s += "64e:"+e+" Len:"+(string)llStringLength(e)+"\n";
        s += "64e:"+(string)llStringLength(e)+"\n";
//        s += "64d:"+XTEADecryptBase64( e, 0 )+"\n";
        e = XTEAEncryptBase16( msg, 0 );
//        s += "16e:"+e+" Len:"+(string)llStringLength(e)+"\n";
        s += "16e:"+(string)llStringLength(e)+"\n";
//        s += "16d:"+XTEADecryptBase16( e, 0 )+"\n";
        e = XTEAEncrypt7BitBase64( msg, 0 );
//        s += "64e7b:"+e+" Len:"+(string)llStringLength(e)+"\n";
        s += "64e7b:"+(string)llStringLength(e)+"\n";
//        s += "64d7b:"+XTEADecrypt7BitBase64( e, 0 )+"\n";
        llSetText( s, <1,1,1>, 1 );
    }
}

state speed_test
{
    state_entry()
    {
        llSetText( "Running speed test. Please wait...", <1,0,0>, 1 );
        llSay( 0, "Preparing speed test. Please wait..." );
        string  tclear = "xxxxxxxxxx";
        string  tcipher;
        float   stime;
        float   etime;
        integer passes;
        integer pby5;
        integer i;
        integer n;
        // The first test seems to be abnormally slow unless we peg the VM
        //  beforehand. O_o
        for( i=0; i<20; i++ )
        {
            tcipher = XTEAEncryptBase64( tclear, 42 );
            tclear = XTEADecryptBase64( tcipher, 42 );
            tcipher = XTEAEncryptBase16( tclear, 42 );
            tclear = XTEADecryptBase16( tcipher, 42 );
        }
        for( n=0; n<3; n++ )
        {
            if( n==0 )
            {
                passes = 1000;
                pby5 = passes/5;
                tclear = "tiny";
                llSay( 0, "Running short string speed test..." );
            }
            else if( n == 1 )
            {
                passes = 250;
                pby5 = passes/5;
                tclear = "Here is a string of moderate length for a test.";
                llSay( 0, "Running medium string speed test..." );
            }
            else if( n == 2 )
            {
                passes = 100;
                pby5 = passes/5;
                tclear = "OMG it's a big ol huuuuge string.OMG it's a big ol huuuuge string.OMG it's a big ol huuuuge string.OMG it's a big ol huuuuge string.OMG it's a big ol huuuuge string.OMG it's a big ol huuuuge string.OMG it's a big ol huuuuge string.OMG it's a big ol huuuuge string.OMG it's a big ol huuuuge string.OMG it's a big ol huuuuge string.";
                llSay( 0, "Running long string speed test..." );
            }
            stime = llGetTime();
            for( i=0; i

, 1 );
        state default;
    }
}
```