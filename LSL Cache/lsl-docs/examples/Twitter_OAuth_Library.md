---
name: "Twitter OAuth Library"
category: "example"
type: "example"
language: "LSL"
description: "The Twitter OAuth Library allows scripted objects in Second Life to update the Twitter status streams of residents in Second Life interacting with the objects. A dance machine might send an update saying that a resident is dancing at at a particular location in Second Life, a vendor might send an update saying that a resident has bought a particular item, an arena might say that a resident has won or lost a game. These status updates can be seen by the resident's followers on Twitter and can include SLURLs back in to Second Life, allowing followers on Twitter to jump in to Second Life, whether they are a resident or not."
wiki_url: "https://wiki.secondlife.com/wiki/Twitter_OAuth_Library"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 Using the Twitter OAuth Library

  - 1.1 Setting Up Your Twitter Application
  - 1.2 Setting Up The Twitter OAuth Library
  - 1.3 Testing The Twitter OAuth Library
  - 1.4 Next Steps
- 2 Twitter OAuth Example Client
- 3 Twitter OAuth Library

Using the Twitter OAuth Library

The Twitter OAuth Library allows scripted objects in Second Life to update the Twitter status streams of residents in Second Life interacting with the objects. A dance machine might send an update saying that a resident is dancing at at a particular location in Second Life, a vendor might send an update saying that a resident has bought a particular item, an arena might say that a resident has won or lost a game. These status updates can be seen by the resident's followers on Twitter and can include SLURLs back in to Second Life, allowing followers on Twitter to jump in to Second Life, whether they are a resident or not.

By using OAuth, the Twitter OAuth Library avoids the need for residents to share their Twitter username and password with anyone other than twitter.com ([the password anti-pattern](http://adactio.com/journal/1357)) and gives them fine-grained control over which Second Life objects are able to send updates to twitter. The Twitter OAuth Library also uses the HTTP-In and HTTP-Out facilities to communicate directly with Twitter, avoiding the need to use a web server to intermediate communication between Second Life and Twitter. If you have an object in Second Life, you can use theTwitter OAuth library to make it send updates to Twitter. A video of the Twitter OAuth Library in use is here: [http://www.youtube.com/watch?v=_19cl8qOZKA](http://www.youtube.com/watch?v=_19cl8qOZKA)

The Twitter OAuth Library is designed to be easy to integrate with existing Second Life objects even for those with little scripting experience. To add Twitter integration to your Second Life object, follow these instructions:

## Setting Up Your Twitter Application

1. Set up a Twitter account and log in to Twitter.
1. Go to [http://twitter.com/oauth_clients](http://twitter.com/oauth_clients)
1. Click the *Register a new application* link to the **Register an Application** page
1. Set *Application Type* to *"Browser"*.
1. Set *Callback URL* to [http://example.com/we-use-dynamic-urls/](http://example.com/we-use-dynamic-urls/)
1. Set *Default Access type* to *"Read & Write"*.
1. Leave *Use Twitter for login* unchecked.
1. Make sure you fill in the rest of the form, or your application may not work.
1. Once you have successfully registered your application, Twitter will take you to the **Application Details** page for your new application.

## Setting Up The Twitter OAuth Library

1. Get a copy of the Twitter OAuth Library from [Ambleside](http://maps.secondlife.com/secondlife/Ambleside/208/31/31) or the [SL Marketplace](http://marketplace.secondlife.com/p/Marketplace/977083).
1. Drag the Twitter OAuth Library in from your inventory onto your land.
1. Right-click on the Twitter OAuth Library, edit it and click on the Content tab.
1. Drag the scripts from the Twitter OAuth Library box to your inventory.
1. Rez your Second Life object in world.
1. Right-click on your object, Edit it, and click on on the Content tab.
1. Drag the Twitter OAuth scripts from your inventory into your Second Life object.
1. Double-click on the TwitterOAuthClient script to edit it.
1. Replace YOUR CONSUMER KEY HERE with the Consumer key from your Twitter **Application Details** page.
1. Replace YOUR CONSUMER SECRET HERE with the Consumer secret from your Twitter **Application Details** page.
1. Replace *I did something amazing in Second Life here* with the message you would like to send from your Second Life object.
1. Click the Save button, close the script editor and close the edit floater.

## Testing The Twitter OAuth Library

1. Touch your Second Life object to test your Twitter application settings.
1. A popup should appear asking you to "Authorise Twitter access"; click the "Go to page" button.
1. You should be directed back to a page on Twitter saying "An application would like to connect to your account".
1. Fill in your Twitter user name and password if you are not already signed in to Twitter (note these details only go to twitter.com) then click the green "Allow" button.
1. Check that your Twitter stream now contains the message you wanted to send, followed by a SLURL from your Twitter application.
1. Once you have authorized the application to use Twitter, touching the box again will send a new update to Twitter (but be aware, multiple identical status updates will not appear).
1. If the test fails at any point, touch the Twitter OAuth Library box again to retry.

## Next Steps

Rather than sending updates to Twitter every time your object is touched, you will probably want to send updates when other interactions take place. To do this, just copy the first part of TwitterOAuthClient script up to "// STOP COPYING HERE" to the top of your script, then call TwitterOAuthInit when your script is initialized in state_entry and on_rez and TwitterOAuthUpdateStatus whenever you want your script to send an update to Twitter. Note that you should always ask a resident whether it's OK to post an update to Twitter before calling TwitterOAuthUpdateStatus. Although the Twitter OAuth library is designed to talk to Twitter out of the box, it is a fully compliant OAuth 1.0a consumer library and so can be easily modified to talk to any web service that supports OAuth integration.

Twitter OAuth Example Client

```lsl
//////////////////////////////////////////////////////////////////////////////////////
//
//    Twitter OAuth Client 1.0: An example client that uses the LSL OAuth 1.0a
//    Library for Twitter by Babbage Linden.
//
//    Released under the Creative Commons Creative Commons Attribution-Share Alike 3.0
//    license http://creativecommons.org/licenses/by-sa/3.0/
//
//////////////////////////////////////////////////////////////////////////////////////

// Application constants generated by Twitter.
// Set up a new Twitter application here: http://twitter.com/oauth_clients
string TWITTER_OAUTH_CONSUMER_KEY = "YOUR CONSUMER KEY HERE";
string TWITTER_OAUTH_CONSUMER_SECRET = "YOUR CONSUMER SECRET HERE";

// Message constants defined by Twitter OAuth library.
integer TWITTER_OAUTH_SET_CONSUMER_KEY = 999000;
integer TWITTER_OAUTH_SET_CONSUMER_SECRET = 999001;
integer TWITTER_OAUTH_SET_MAX_RETRIES = 999002;
integer TWITTER_OAUTH_UPDATE_STATUS = 999003;

TwitterOAuthInit()
{
    // Set up Twitter OAuth library, using application consumer key and secret generated by Twitter.
    llMessageLinked(LINK_THIS, TWITTER_OAUTH_SET_CONSUMER_KEY, TWITTER_OAUTH_CONSUMER_KEY, NULL_KEY);
    llMessageLinked(LINK_THIS, TWITTER_OAUTH_SET_CONSUMER_SECRET, TWITTER_OAUTH_CONSUMER_SECRET, NULL_KEY);
    llMessageLinked(LINK_THIS, TWITTER_OAUTH_SET_MAX_RETRIES, "10", NULL_KEY);
}

string TwitterOAuthGetSLURL()
{
    string globe = "http://maps.secondlife.com/secondlife";
    string region = llGetRegionName();
    vector pos = llGetPos();
    string posx = (string) llRound(pos.x);
    string posy = (string) llRound(pos.y);
    string posz = (string) llRound(pos.z);
    return globe + "/" + llEscapeURL(region) +"/" + posx + "/" + posy + "/" + posz;
}

string TwitterOAuthBuildMessage()
{
    // Example message, change this as appropriate.
    return "I did something amazing in Second Life here " + TwitterOAuthGetSLURL() + " #inSL";
}

TwitterOAuthUpdateStatus(string message, key avatar)
{
    llMessageLinked(LINK_THIS, TWITTER_OAUTH_UPDATE_STATUS, message, avatar);
}

// STOP COPYING HERE

default
{
    state_entry()
    {
        TwitterOAuthInit();
    }

    on_rez(integer param)
    {
        TwitterOAuthInit();
    }

    touch_start(integer total_number)
    {
        TwitterOAuthUpdateStatus(TwitterOAuthBuildMessage(), llDetectedKey(0));
    }
}
```

Twitter OAuth Library

```lsl
//////////////////////////////////////////////////////////////////////////////////////
//
//    Twitter OAuth Lib 1.0: An LSL OAuth 1.0a Library for Twitter by Babbage Linden.
//    Built with Cale Flanagan's LSL HMAC-SHA1 implementation and Strife Onizuka's
//    LGPL Combined Library and with help from Latif Khalifa.
//
//    This library is free software; you can redistribute it and/or
//    modify it under the terms of the GNU Lesser General Public License
//    as published by the Free Software Foundation;
//    version 3 of the License.
//
//    This library is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU Lesser General Public License for more details.
//
//    You should have received a copy of the GNU Lesser General Public License
//    along with this library.  If not, see
//    or write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330,
//    Boston, MA  02111-1307  USA
//
//////////////////////////////////////////////////////////////////////////////////////

// Library protocol constants.
integer TWITTER_OAUTH_SET_CONSUMER_KEY = 999000;
integer TWITTER_OAUTH_SET_CONSUMER_SECRET = 999001;
integer TWITTER_OAUTH_SET_MAX_RETRIES = 999002;
integer TWITTER_OAUTH_UPDATE_STATUS = 999003;

// Library state.
string gConsumerKey = "";
string gConsumerSecret = "";
integer gMaxRetries = 10;

// Request state.
key gAvatarKey;
string gMessage;
key gRequestTokenKey;
string gRequestToken;
string gRequestTokenSecret;
key gAccessTokenKey;
string gVerifier;
string gAuthorizeUrl = "oob";
integer gRetries;

string TrimRight(string src, string chrs)//LSLEditor Unsafe, LSL Safe
{
    integer i = llStringLength(src);
    do ; while(~llSubStringIndex(chrs, llGetSubString(src, i = ~-i, i)) && i);
    return llDeleteSubString(src, -~(i), 0x7FFFFFF0);
}

string WriteBase64Integer(string data, integer index, integer value)
{

    integer S = 12 - ((index % 3) << 1);
    return  llDeleteSubString(
        llInsertString(
        data,
        index = ((index << 4) / 3),
            llInsertString(
                llIntegerToBase64(
                    (llBase64ToInteger(llGetSubString((data = llGetSubString(data, index, index+7)) + "AAAAAA", 0, 5)) & (0xFFF00000 << S)) |
                    ((value >> (12 - S)) & ~(0xFFF00000 << S))
                ), 2,
                llIntegerToBase64(
                    (llBase64ToInteger(llGetSubString((llDeleteSubString(data, 0, 1)) + "AAAAAA", 0, 5)) & ~(0xFFFFFFFF << S)) |
                    (value << S)
        )    )    ), index+7, index + 22);//insert it then remove the old and the extra.
}

string DwordListToBase64(list a)
{
    integer len = (a != []);
    integer i = -1;
    string out;
    while((i = -~i) < len)
        out = WriteBase64Integer(out, i, llList2Integer(a, i));
    return TrimRight(out,"A");
}

// Takes a dwordblock, adds a string and puts it padded for blocksize into a dwordlist
// returns sha1blocks
list PrepareShortkey(string s)
{
    integer v = 0;
    integer cnt = llStringLength(s);
    integer n = cnt;
    list dw_skey;

    for (n = 0; n < cnt; n++)
    {
        v = v | 0xFF & llBase64ToInteger("AAAA" + llStringToBase64(llGetSubString(s, n, n)));
        if (n % 4 == 3)
        {
            dw_skey += [v];
            v = 0;
        }
        else
        {
            v = v << 8;
        }
    }

    //pad 0s (could be done dword-wise, after filling up to boundary, later, maybe...)
    for ( ; n < 64; n++)
    {
        if (n % 4 == 3)
        {
            dw_skey += [v];
            v = 0;
        }
        else
        {
            v = v << 8;
        }
    }
    dw_skey += [v];

    return dw_skey;
}

// Takes a dwordblock, adds a string and puts it padded for blocksize into a dwordlist
// returns sha1blocks
list PrepareSha1Blocks(list dwords, string s)
{
    integer v = 0;
    integer cnt = llStringLength(s);
    integer n = cnt;
    integer mcnt = cnt;
    list shablocks = dwords;

    mcnt = cnt + (dwords != []) * 4; // add up the dword-data (total message length)

    for (n = 0; n < cnt; n++)
    {
        v = v | 0xFF & llBase64ToInteger("AAAA" + llStringToBase64(llGetSubString(s, n, n)));
        if (n % 4 == 3)
        {
            shablocks += [v];
            v = 0;
        }
        else
        {
            v = v << 8;
        }
    }

    // pad a 1 and seven 0's
    v = v | 0x80;
    if (n % 4 == 3)
    {
        shablocks += [v];
        v = 0;
    }
    else
    {
        v = v << 8;
    }
    n++;

    //we ignored the dwords silently, but now we have to take them into account

    //how many bytes do we need to fill blocks and have 8 bytes left...
    cnt = ((mcnt + 8) / 64 + 1) * 64 - 9;

    //pad 0s (could be done dword-wise, after filling up to boundary, later, maybe...)
    for (n += (dwords != []) * 4 ; n < cnt; n++)
    {
        if (n % 4 == 3)
        {
            shablocks += [v];
            v = 0;
        }
        else
        {
            v = v << 8;
        }
    }
    shablocks += [v];

    // pad message length
    shablocks += [0]; // we assume not to have more as 16M messagesize (roughly)
    shablocks += [8 * mcnt];

    return shablocks;
}

// Inner core of sha1 calculation, based on FIPS 180-1
// http://www.itl.nist.gov/fipspubs/fip180-1.htm
// and some help from http://www.herongyang.com/crypto/message_digest_sha1.html
// and a bit from lkalif specialized on dwordlists
//
// Takes a dwordlist as input and returns hash as dwordlist
list ProcessSha1(list dwblocks)
{
    integer block;
    integer blocks = (dwblocks != []) / 16;
    integer H0 = 0x67452301;
    integer H1 = 0xEFCDAB89;
    integer H2 = 0x98BADCFE;
    integer H3 = 0x10325476;
    integer H4 = 0xC3D2E1F0;

    for (block = 0; block < blocks; block++)
    {
        list W;
        integer t;
        integer A = H0;
        integer B = H1;
        integer C = H2;
        integer D = H3;
        integer E = H4;

        for (t = 0; t < 16; t++)
        {
            W += [llList2Integer(dwblocks, t + block * 16)];
        }
        for ( ; t < 80; t++)
        {
            integer x = llList2Integer(W, t - 3) ^ llList2Integer(W, t - 8) ^ llList2Integer(W, t - 14) ^ llList2Integer(W, t - 16);
            W += [(x << 1) |!!(x & 0x80000000)]; // borrowed from lkalif
        }

        for (t = 0; t < 20; t++)
        {
            integer TEMP = ((A << 5) | ((A >> 27) & 0x1F)) + ((B & C) | ((~B) & D)) + E + llList2Integer(W, t) + 0x5A827999;
            E = D; D = C; C = ((B << 30) | ((B >> 2) & 0x3FFFFFFF)); B = A; A = TEMP;
        }
        for (; t < 40; t++)
        {
            integer TEMP = ((A << 5) | ((A >> 27) & 0x1F)) + (B ^ C ^ D) + E + llList2Integer(W, t) + 0x6ED9EBA1;
            E = D; D = C; C = ((B << 30) | ((B >> 2) & 0x3FFFFFFF)); B = A; A = TEMP;
        }
        for (; t < 60; t++)
        {
            integer TEMP = ((A << 5) | ((A >> 27) & 0x1F)) + ((B & C) | (B & D) | (C & D)) + E + llList2Integer(W, t) + 0x8F1BBCDC;
            E = D; D = C; C = ((B << 30) | ((B >> 2) & 0x3FFFFFFF)); B = A; A = TEMP;
        }
        for (; t < 80; t++)
        {
            integer TEMP = ((A << 5) | ((A >> 27) & 0x1F)) + (B ^ C ^ D) + E + llList2Integer(W, t) + 0xCA62C1D6;
            E = D; D = C; C = ((B << 30) | ((B >> 2) & 0x3FFFFFFF)); B = A; A = TEMP;
        }

        H0 += A;
        H1 += B;
        H2 += C;
        H3 += D;
        H4 += E;
    }

    return [H0, H1, H2, H3, H4];
}

//Caveats: Handling of unicode undefined and no message longer 16M allowed
list Sha1DWord(list dw, string message)
{
    list sha1blocks = PrepareSha1Blocks(dw, message);
    list digest = ProcessSha1(sha1blocks);
    return digest;
}

list dw_key;
list dw_ipad;
list dw_opad;

// xor the 64bytes (16 dwords) with value
list PreparePad(integer val)
{
    list r;
    integer i;

    for (i = 0; i < 16; )
    {
        r += [llList2Integer(dw_key, i++) ^ val];
    }

    return r;
}

// 2 step design, for simple re-use of key-data
HmacInit(string secretkey)
{
    if (llStringLength(secretkey) > 64) // sha1 only if blocksize exceeded
        dw_key = Sha1DWord([], secretkey) + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    else
        dw_key = PrepareShortkey(secretkey);

    dw_ipad = PreparePad(0x36363636);
    dw_opad = PreparePad(0x5c5c5c5c);
}

list HmacUpdate(string message)
{
    list dw_ihash = Sha1DWord(dw_ipad, message);
    list dw_opad2 = dw_opad + dw_ihash;

    return Sha1DWord(dw_opad2, "");
}

integer cacheSize = 25;
list tokenCache = [];

string GetAccessToken(key avatarId)
{
    string result = "";
    integer index = llListFindList(tokenCache, [avatarId]);
    if(index != -1)
    {
        result = llList2String(tokenCache, index + 1);
    }
    return result;
}

string GetAccessTokenSecret(key avatarId)
{
    string result = "";
    integer index = llListFindList(tokenCache, [avatarId]);
    if(index != -1)
    {
        result = llList2String(tokenCache, index + 2);
    }
    return result;
}

SetAccessToken(key avatarId, string accessToken, string accessTokenSecret)
{
    integer stride = 3;
    integer maxLength = (cacheSize * stride) - stride;
    if(llGetListLength(tokenCache) > maxLength)
    {
        tokenCache = llDeleteSubList(tokenCache, maxLength, -1);
    }
    tokenCache = [avatarId, accessToken, accessTokenSecret] + tokenCache;
}

string OAuthUrlEncodeString(string s)
{
    string result = "";
    integer count = llStringLength(s);
    integer i;
    for (i = 0; i < count; ++i)
    {
        string c = llGetSubString(s, i, i);
        if(c != "-" && c != "_" && c != "." && c != "," && c != "~")
        {
            c = llEscapeURL(c);
        }
        result += c;
    }
    return result;
}

list OAuthUrlEncodeList(list l)
{
    list result = [];
    integer c = llGetListLength(l);
    integer i;
    for(i = 0; i < c; ++i)
    {
        result += OAuthUrlEncodeString(llList2String(l, i));
    }
    return result;
}

string OAuthConcatenate(list l)
{
    string result = "";
    integer count = llGetListLength(l);
    integer i = 0;
    while (i < count)
    {
        result += llList2String(l, i) + "=" + llList2String(l, i + 1);
        i += 2;
        if (i < count)
        {
            result += "&";
        }
    }
    return result;
}

string Sign(string method, string url, string consumerSecret, string tokenSecret, list parameters)
{
    string signatureBase = OAuthUrlEncodeString(method) + "&" + OAuthUrlEncodeString(url) + "&" +
        OAuthUrlEncodeString(OAuthConcatenate(parameters));
    //llOwnerSay(signatureBase);

    list keyList = [];
    keyList += consumerSecret;
    keyList += tokenSecret;
    string keyString = consumerSecret + "&" + tokenSecret;
    //llOwnerSay(keyString);

    HmacInit(keyString);
    list dwSig = HmacUpdate(signatureBase);

    return DwordListToBase64(dwSig) + "=";
}

string OAuthUrl(string method, string url, string consumerKey, string consumerSecret, string token,
                        string tokenSecret, list additionalParams)
{
    integer nonce = (integer)llFrand(1000000);
    list parameters = ["oauth_version","1.0a",
                         "oauth_nonce", (string)nonce,
                         "oauth_consumer_key", consumerKey,
                         "oauth_signature_method", "HMAC-SHA1",
                         "oauth_timestamp", (string)llGetUnixTime()];

    if(token != "")
    {
        parameters += "oauth_token";
        parameters += token;
    }

    parameters += additionalParams;

    parameters = OAuthUrlEncodeList(parameters);
    parameters = llListSort(parameters, 2, 1);

    string sig = Sign(method, url, consumerSecret, tokenSecret, parameters);
    parameters += "oauth_signature";
    parameters += sig;

    url = url + "?" + OAuthConcatenate(parameters);
    //llOwnerSay(url);
    return url;
}

string FindOAuthResponseValue(string name, list tokens)
{
    //llOwnerSay("Looking for " + name + " in:" + llList2CSV(tokens));
    integer index = llListFindList(tokens, [name]);
    if (index != -1)
    {
        return llList2String(tokens, index + 1);
    }
    return "";
}

list TokenizeOAuthResponse(string response)
{
    return llParseString2List(response, ["=", "&"], []);
}

ResetTimeout()
{
    // Time out HTTP requests and input requests after a minute of inactivity.
    llSetTimerEvent(60);
}

Reset()
{
    gAvatarKey = NULL_KEY;
    gMessage = "";
    gRequestTokenKey = NULL_KEY;
    gRequestToken = "";
    gRequestTokenSecret = "";
    gAccessTokenKey = NULL_KEY;
    gVerifier = "";
    gRetries = 0;
    llSetTimerEvent(0);
}

RequestAccessToken()
{
    list parameters = ["oauth_verifier", gVerifier];
    string url = OAuthUrl("POST", "http://twitter.com/oauth/access_token",
                            gConsumerKey, gConsumerSecret, gRequestToken, gRequestTokenSecret, parameters);
    ResetTimeout();
    gAccessTokenKey = llHTTPRequest(url, [HTTP_METHOD, "POST"], "");
}

RequestRequestToken()
{
    string url = OAuthUrl("GET", "http://twitter.com/oauth/request_token", gConsumerKey, gConsumerSecret, "", "",
                          ["oauth_callback", gAuthorizeUrl]);
    ResetTimeout();
    gRequestTokenKey = llHTTPRequest(url, [], "");
}

RequestTokens(key avatar, string message)
{
    string accessToken = GetAccessToken(avatar);
    string accessTokenSecret = GetAccessTokenSecret(avatar);

    if(accessToken != "" && accessTokenSecret != "")
    {
        // Have access token, update immediately.
        UpdateStatus(accessToken, accessTokenSecret, message);
    }
    else
    {
        if(gRequestTokenKey != NULL_KEY ||
           gAccessTokenKey != NULL_KEY)
        {
            // Currently requesting access token, drop this request on the floor.
            // TODO: babbage: queue request for later, handle paralell requests, or signal failure to caller...
            llOwnerSay("OAuth request in progress, please wait.");
            return;
        }

        // Access token unknown and no request in progress, request access token.
        Reset();
        gAvatarKey = avatar;
        gMessage = message;
        RequestRequestToken();
    }
}

UpdateStatus(string accessToken, string accessTokenSecret, string message)
{
    list parameters = ["status", message];
    string url = OAuthUrl("POST", "http://twitter.com/statuses/update.xml",
                            gConsumerKey, gConsumerSecret, accessToken, accessTokenSecret, parameters);
    llHTTPRequest(url, [HTTP_METHOD, "POST"], "");
}

default
{
    state_entry()
    {
        llRequestURL();
        Reset();
    }

    on_rez(integer param)
    {
        llRequestURL();
        Reset();
    }

    changed(integer changes)
    {
        if((changes & CHANGED_REGION_START) != 0)
        {
            llRequestURL();
        }
    }

    link_message(integer sender_num, integer num, string message, key avatar)
    {
        if(num == TWITTER_OAUTH_SET_CONSUMER_KEY)
        {
            gConsumerKey = message;
        }
        else if(num == TWITTER_OAUTH_SET_CONSUMER_SECRET)
        {
            gConsumerSecret = message;
        }
        else if(num == TWITTER_OAUTH_SET_MAX_RETRIES)
        {
            gMaxRetries = (integer) message;
        }
        else if(num == TWITTER_OAUTH_UPDATE_STATUS)
        {
            if(gConsumerKey == "")
            {
                llOwnerSay("Consumer key must be set before status update.");
                return;
            }
            if(gConsumerSecret == "")
            {
                llOwnerSay("Consumer secret must be set before status update.");
                return;
            }
            RequestTokens(avatar, message);
        }
    }

    http_response(key id, integer status, list meta, string body)
    {
        //llOwnerSay("status:" + (string)status);
        //llOwnerSay("body:" + body);

        if (id == gRequestTokenKey)
        {
            if(status != 200)
            {
                if(gRetries++ < gMaxRetries)
                {
                    llOwnerSay("Failed to obtain oauth request token, retrying...");
                    RequestRequestToken();
                }
                else
                {
                    llOwnerSay("Failed to obtain oauth request token");
                    llOwnerSay("Status:" + (string)status);
                    llOwnerSay("Body:" + body);
                    Reset();
                }
                return;
            }

            gRetries = 0;
            list responseTokens = TokenizeOAuthResponse(body);
            gRequestToken = FindOAuthResponseValue("oauth_token", responseTokens);
            gRequestTokenSecret = FindOAuthResponseValue("oauth_token_secret", responseTokens);

            string url = "http://twitter.com/oauth/authorize?" +
                OAuthConcatenate(["oauth_token", gRequestToken]);
            ResetTimeout();
            llLoadURL(gAvatarKey, "Please authorise Twitter access", url);

            if(gAuthorizeUrl == "oob")
            {
                llListen(3, "", NULL_KEY, "");
                llOwnerSay("Please chat PIN on channel 3 (eg \"/3 12345678\")");
            }
        }
        else if (id == gAccessTokenKey)
        {
            if(status != 200)
            {
                if(gRetries++ < gMaxRetries)
                {
                    llOwnerSay("Failed to obtain oauth access token, retrying...");
                    RequestAccessToken();
                }
                else
                {
                    llOwnerSay("Failed to obtain oauth access token");
                    llOwnerSay("Status:" + (string)status);
                    llOwnerSay("Body:" + body);
                    Reset();
                }
                return;
            }

            gRetries = 0;
            list responseTokens = TokenizeOAuthResponse(body);
            string accessToken = FindOAuthResponseValue("oauth_token", responseTokens);
            string accessTokenSecret = FindOAuthResponseValue("oauth_token_secret", responseTokens);
            string screenName = FindOAuthResponseValue("screen_name", responseTokens);
            SetAccessToken(gAvatarKey, accessToken, accessTokenSecret);
            UpdateStatus(accessToken, accessTokenSecret, gMessage);
            llLoadURL(gAvatarKey, "Show status update?", "http://twitter.com/" + screenName);
            Reset();
        }
        else
        {
            // NOTE: babbage: status update always fail as http out cannot accept XML or JSON
            // TODO: babbage: allow http out to accept XML or JSON, so we can actually check for errors here...
            return;
        }
    }

    listen(integer channel, string name, key id, string message)
    {
        if(id == gAvatarKey && channel == 3)
        {
            // PIN based authorization flow.
            gVerifier = message;
            RequestAccessToken();
        }
    }

    http_request(key id, string method, string body)
    {
        if(method == "URL_REQUEST_GRANTED")
        {
            // NOTE: babbage: need trailing / path...
            gAuthorizeUrl = body + "/";
        }
        else if(method == "URL_REQUEST_DENIED")
        {
            llOwnerSay("No URLs available, using PIN based flow.");
            gAuthorizeUrl = "oob";
        }
        else if(method == "GET")
        {
            list responseTokens = TokenizeOAuthResponse(llGetHTTPHeader(id, "x-query-string"));
            gVerifier = FindOAuthResponseValue("oauth_verifier", responseTokens);

            RequestAccessToken();

            // TODO: babbage: allow HTML response body, so we can show something more useful than a blank web page here...
            llHTTPResponse(id, 200, "");
        }
    }

    timer()
    {
        llOwnerSay("Request timeout, resetting...");
        Reset();
    }
}
```