---
name: "Vigenère Weak Encryption"
category: "example"
type: "example"
language: "LSL"
description: "This is a simple LSL implementation of a Vigenère Cipher. Essentially it works on the principle of taking an input, and substituting or rotating the values within a known alphabet so that the original message cannot be easily distinguished."
wiki_url: "https://wiki.secondlife.com/wiki/Vigen%C3%A8re_Weak_Encryption"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

## Description

This is a simple LSL implementation of a [Vigenère Cipher](http://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher). Essentially it works on the principle of taking an input, and substituting or rotating the values within a known alphabet so that the original message cannot be easily distinguished.

This form of encryption is not cryptographically secure, but is very, very fast. It is most useful for protecting time-sensitive messages where the key is updated fairly regularly using a pseudo-random generator of some kind. Or, if the key is only used a single-time the message can be considered entirely secure provided the attacker knows nothing of the format of your messages.

You should **NOT** use this to protect anything serious such as money transactions, unless the content of the message is guaranteed to be useless after a relatively short time, for example if your message contains a unique, one-time-only key that will be refused if used again.

For more powerful encryption you should use AES which is much stronger and still fairly fast, but may not be fast enough for some applications.

When using the script below, you must first provide a key via the `keyExpand()` method, you can then simply pass in messages to encrypt or decrypt using the `encrypt()` and `decrypt()` methods respectively. Due its use of multilevel XORing and shifting this algorithm is typically more secure than a simple base64 XOR. More rounds increases security, but more than 10 are unlikely to have any real effect due to the relatively weak security of the algorithm as a whole.

## Script

The content of the default `state_entry()` provides you with a basic test-case, and benchmarking of the algorithm. Of note in this implementation is that the llXorBase64StringsCorrect() function provides rudimentary padding, though you may wish to expand this to better protect your messages depending on their typical size. Also used is a "block" XOR which helps to prevent repeated segments. These are however only small aids in strengthening the cipher.

```lsl
integer ROUNDS      = 10; // Increase this value for more passes
list    keyExpanded = [];

keyExpand(string k) {
    integer i = 0; string s = "";
    integer j = 0; integer l = llStringLength(k);
    keyExpanded = [];

    do {
        j = i % l;
        if (j > 0)
            s = llStringToBase64(
                llGetSubString(k, j, -1) + llGetSubString(k, 0, j - 1)
            );
        else s = llStringToBase64(k);

        keyExpanded = (keyExpanded = []) + keyExpanded + [
            llXorBase64StringsCorrect(
                (s = "") + s,
                llStringToBase64((string)i)
            )
        ];
    } while ((++i) < ROUNDS);
}

string encrypt(string text){
    text = llStringToBase64((text = "") + text);

    integer i = 0;
    do {
        text = llXorBase64StringsCorrect(
            (text = "") + text,
            llList2String(keyExpanded, i)
        );
    } while ((++i) < ROUNDS);

    return (text = "") + text;
}

string decrypt(string text){
    integer i = ROUNDS - 1;
    do {
        text = llXorBase64StringsCorrect(
            (text = "") + text,
            llList2String(keyExpanded, i)
        );
    } while ((--i) >= 0);

    return llBase64ToString((text = "") + text);
}

default{
    state_entry(){
        integer i = 0;
        llResetTime();
        do {
            keyExpand("I am a fantastic key!");
        } while ((++i) < 100);
        llOwnerSay("Expand in "+(string)(llGetTime() / 100.0)+" seconds");
        llOwnerSay("Expanded key = ["+llList2CSV(keyExpanded)+"]");

        string s;
        i = 0;
        llResetTime();
        do {
            s = encrypt("Hello world what a lovely day");
        } while ((++i) < 100);
        llOwnerSay("Encrypt in "+(string)(llGetTime() / 100.0)+" seconds");
        llOwnerSay("Encrypted = "+s);

        string k;
        i = 0;
        llResetTime();
        do {
            k = decrypt(s);
        } while ((++i) < 100);
        llOwnerSay("Decrypt in "+(string)(llGetTime() / 100.0)+" seconds");
        llOwnerSay("Decrypted = "+k);
    }
}
```