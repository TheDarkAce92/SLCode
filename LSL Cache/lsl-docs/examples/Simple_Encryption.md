---
name: "Simple Encryption"
category: "example"
type: "example"
language: "LSL"
description: "Here's a function to pass a secret message from one object to another. Using XOR, this is perhaps the weakest form of encryption. I have taken steps to make it harder to break using random nonce values with the password. If someone is able to decrypt one message, it will be easy for them to decrypt any other message. I've also added version support so that you can upgrade the script later and still have compatibility with older scripts using the same protocol."
wiki_url: "https://wiki.secondlife.com/wiki/Simple_Encryption"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Here's a function to pass a secret message from one object to another. Using XOR, this is perhaps the weakest form of encryption. I have taken steps to make it harder to break using random nonce values with the password. If someone is able to decrypt one message, it will be easy for them to decrypt any other message. I've also added version support so that you can upgrade the script later and still have compatibility with older scripts using the same protocol.

## Encryptor

```lsl
//Chibiusa lings shiz
string ProtocolSignature = "ENC"; // your own signature
float ProtocolVersion = 0.3; // can range from 0.0 to 255.255
string Password = "P@ssw0rd"; // change this to your own password
integer communicationsChannel = PUBLIC_CHANNEL;
string Header;
string strHex = "0123456789ABCDEF";

string hex(integer value)
{
    integer digit = value & 0xF;
    string text = llGetSubString(strHex, digit, digit);
    value = (value >> 4) & 0xfffFFFF;
    integer odd = TRUE;
    while(value)
    {
        digit = value & 0xF;
        text = llGetSubString(strHex, digit, digit) + text;
        odd = !odd;
        value = value >> 4;
    }
    if(odd)
        text = "0" + text;
    return text;
}
string encrypt(string password, string message)
{
    // get a random value
    integer nonce = (integer)llFrand(0x7FFFFFFF);

    // generate digest and prepend it to message
    message = llMD5String(message, nonce) + message;

    // generate one time pad
    string oneTimePad = llMD5String(password, nonce);

    // append pad until length matches or exceeds message
    integer count = (llStringLength(message) - 1) / 32;
    if(count)
        do
            oneTimePad += llMD5String(oneTimePad, nonce);
        while(--count);

    // return the header, nonce and encrypted message
    return Header + llGetSubString("00000000" + hex(nonce), -8, -1) + llXorBase64(llStringToBase64(message), llStringToBase64(oneTimePad));
}
init()
{
    //build the header, it never changes.
    list versions = llParseString2List((string)ProtocolVersion, ["."], []);
    string minor = llList2String(versions, 1);
    integer p = 0;
    while(llGetSubString(minor, --p, p) == "0");
    Header = ProtocolSignature + hex(llList2Integer(versions, 0)) + hex((integer)llGetSubString(minor, 0xFF000000, p));
}

default
{
    state_entry()
    {
        init();
        llSay(communicationsChannel, encrypt(Password, "Hello, Avatar!"));
        llSay(communicationsChannel, encrypt(Password, "This is a very long text that I hope to be able to create a long one time pad to decrypt for it."));
    }

    touch_start(integer total_number)
    {
        llSay(communicationsChannel, encrypt(Password, "Touched."));
    }
}
```

## Decryptor

```lsl
string ProtocolSignature = "ENC"; // your own signature
float ProtocolVersion = 0.3; // can range from 0.0 to 255.255
string Password = "P@ssw0rd"; // change this to your own password
integer communicationsChannel = PUBLIC_CHANNEL;
integer Debug = TRUE; // Set this to false for production
integer listener;

init()
{
    if(listener != 0)
    {
        llListenRemove(listener);
        listener = 0;
    }
    listener = llListen(communicationsChannel, "", NULL_KEY, "");
}
string error(string message)
{
    if(Debug) llSay(DEBUG_CHANNEL, message);
    return "";
}
string decrypt(string password, string message)
{
    integer signatureLength = llStringLength(ProtocolSignature);
    integer headerLength = signatureLength + 12; // version = 4, nonce = 8

    // verify length of encrypted message
    if(llStringLength(message) < signatureLength + 44) // digest = 32 (base64 = 44) + at least one character
        return error("Too small for secret message.");

    // look for protocol signature in message header
    if(llSubStringIndex(message, ProtocolSignature) != 0)
        return error("Unknown protocol.");

    // Parse version information from header
    integer index = signatureLength; // determine where to start parsing
    string major = "0x" + llGetSubString(message, index, ++index);
    string minor = "0x" + llGetSubString(message, ++index, ++index);
    float version = (float)((string)((integer)major) + "." + (string)((integer)minor));

    // verify version is supported
    if(version != ProtocolVersion)
        return error("Unknown version.");

    // parse nonce from header
    integer nonce = (integer)("0x" + llGetSubString(message, ++index, index + 7));

    // remove header from message
    message = llGetSubString(message, headerLength, -1);

    // create one time pad from password and nonce
    string oneTimePad = llMD5String(password, nonce);
    // append pad until length matches or exceeds message
    while(llStringLength(oneTimePad) < (llStringLength(message) / 2 * 3))
        oneTimePad += llMD5String(oneTimePad, nonce);

    // decrypt message
    oneTimePad = llStringToBase64(oneTimePad);
    message = llXorBase64(message, oneTimePad);

    // decode message
    message = llBase64ToString(message);

    // get digest
    string digest = llGetSubString(message, 0, 31);

    // remove digest from message
    message = llGetSubString(message, 32, -1);

    // verify digest is valid
    if(llMD5String(message, nonce) != digest)
        return error("Message digest was not valid.");

    // return decrypted message
    return message;
}
default
{
    state_entry()
    {
        init();
    }
    on_rez(integer start_param)
    {
        init();
    }
    listen(integer channel, string name, key id, string message)
    {
        string message = decrypt(Password, message);
        if(message != "")
            llSay(0, message);
    }
}
```

Note: The Hex and Efficient Hex examples were used to create the hex method.