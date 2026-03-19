---
name: "JSON Web Token in LSL"
category: "example"
type: "example"
language: "LSL"
description: "A JSON Web Token a.k.a. JWT (commonly pronounced \"jot\") is a popular standard for sending authenticated (but not secret!) information in an HTTP request. The JWT string is embedded in a custom http header and is validated by a web service. The example script below shows how to build and use a JWT via LSL:"
wiki_url: "https://wiki.secondlife.com/wiki/JSON_Web_Token_in_LSL"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL

A [JSON Web Token](https://jwt.io/introduction) a.k.a. JWT (commonly pronounced "jot") is a popular standard for sending authenticated (but not secret!) information in an HTTP request.  The JWT string is embedded in a custom http header and is validated by a web service.  The example script below shows how to build and use a JWT via LSL:

```lsl
// jwt.lsl -- build a JWT in LSL (and use it in an HTTP request)

// The unencrypted private_key must be a PEM-formated string.
string private_key = "-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCTXme8TuUfClUA
qavdVnyIhQaYcPmDxZ2QzfK3f3NO3TL0C+MXLVIFRsTjdnOk12ZSQz1DTQji1Mbk
7Tg1vsEVG91TE2CtO1/XtSjotJ27UbjNg+f5S+856ahv6gTVQDEHLLItmb8YdM0X
Jkcv/1QOzQiieimSj9J45vxw+G62q28oz9FV8UGcCpWnkHTeAH+aB1SRx2YbWvRB
z70u+8gYL/LItp6TH6WI1t9uUSH7gxwdJGllyfCzi+i8YXPr3v6D/tkj6nxxYXgE
MpCwEDUbouM4OiZb4a52E3mdDrttGvKI+jS8s8bqv31FR+Sz2/4kCkBmXVhxnVZl
rlKivyRDAgMBAAECggEACeXSTnnMtmFURN91ypTkzP/aPzd/RVQVeW9Lo6VsvNmV
yCxa4T31qfhkgD5+v+MzsnIPqvXWk0g6ijpLMdjmUPZLztOYr6ndjbhTehBUyQr7
wC82z63uRaklhfa6wl6LAcdaZD5U8QiPPxnJYuDhkr4/Ro0Gk8W9xh8FdMpKwqag
5llYQ0p4XuhvMiNcuFLGzWMcwySQ0DoRJrF4hKp65c+Z4BeWYfl4YF80PURCSMle
aOH6xgi4xYuCtgi9GNbWL/w4mvMq9mpVsLw89sjK8K3ye/P+NBUpeK/zWKGeU1Dl
JgOMMC1wF3Qu1eGOyLMoVcvh5qfPY0p8v1MTyBuPeQKBgQDCpQKHi2zoZlqq0yoN
sDF7pkt3Qd35MFZBVU8YnvIHbnLsoIGf4CoBV8Mc+TEUr5ejzenWJ/FoVjUysoWQ
U+mMNex2yLyg7iWSN55J1XDIL4gR71Ur5BxgeeOsZSooDgJw2/Lhrx3JoHlcy6mD
z7ffxrVhkDYYjOss+Lx1T4vKXQKBgQDB0nBpBlIeO6tp4CKdyjXQtCuPtk/n0l2V
eFwqEfeX5T7f1AXbnYvAMfRgPK5lInPhy/V7YDptSRA032o3wYcJzVwdqNXsyntY
BVjpwhzkZM/v3Pr0JLd4Gf+G7W5W3qWOSFBDsgt033oCCM35ALhnlyYqlmNiYE/o
h7pVzUv/HwKBgDvIdMNu9m9W6KgpHXSA1mH1DJ6/c08TIpsEebvFLe9MZC37inSx
ZBVvgDUI8KM632dnWlf1grcaK1K79DwFGel/snY1Z4JCQvXq8UoaLX6+4psnmFBX
ysNzDJOpqs4Mp4FEfRAGOi7wg/YVc6ZRiVdI7/LcWVEnDyCL8U5StUvdAoGAMF52
5Q7JwXe8oFBp8xy6b1n3IQcrS7wI1LtTrMANHN/939fGmnbnoFAXH0klcGG3r5q5
qU9rZUh9feRfWoi2TXDtUw2GTXB+dYnoFXX2xdyOs9pe2jyreJJsXVy1U4J+qFJN
jYdKKqF2jjlqRYCzhE6JHMmpBazpZCszCiSQmZsCgYAcP8BLQe8xNltPsQ+rVQZp
6F+33LUPMh1rImvuXXhyOuYhrqjLNXD9SqWQeW2+XMqqEI9//lA7UJWTlXbv2Lim
nNDyBPwuZKI3ihVHP6fK1frWfWEDJGJxZ4o4stERcxXg08GhvrBAywfimWRMgy3m
PM5RQOPboW3Hmflau1/mXA==
-----END PRIVATE KEY-----";

key request_id;

// Conversion from base64 to base64URL is done in three steps
//  (1) remove all equal-signs
//  (2) replace 'slash' with 'underscore'
//  (3) replace 'plus' with 'minus'
string base64URL(string input)
{
    integer ALL_INSTANCES = 0;
    string result = llReplaceSubString(input, "=", "", ALL_INSTANCES);
    result = llReplaceSubString(result, "/", "_", ALL_INSTANCES);
    return llReplaceSubString(result, "+", "-", ALL_INSTANCES);
}

// JWT consists of three base64URL-encoded strings separated by dots:
//     header.payload.signature
// where 'signature' is the RSA signature of 'header.payload'
string createJwt(string secret, string header, string payload)
{
    string header_and_payload = base64URL(llStringToBase64(header)) + "." + base64URL(llStringToBase64(payload));
    return header_and_payload + "." + base64URL(llSignRSA(secret, header_and_payload, "sha256"));
}

default
{
    state_entry()
    {
        llOwnerSay("Touch to generate JWT");
    }

    touch_start(integer touch_count)
    {
        // Build a hypothetical JWT which contains: owner_id and expiry
        string algorithm = "RSA256";
        integer expiry_duration = 300; // seconds
        integer expiry = llGetUnixTime() + expiry_duration;
        key owner_id = llGetOwner();
        string header = "{\"alg\":\"RS256\",\"typ\":\"JWT\"}";
        string payload = "{\"sub\":\"" + (string)owner_id + "\",\"exp\":" + (string)expiry + "}";
        string jwt = createJwt(private_key, header, payload);
        llOwnerSay("jwt=" + jwt);

        // Send to a hypothetical web service
        string url = "https://your_web_service_here.com/some/path/here";
        list parameters = [HTTP_METHOD, "GET", HTTP_CUSTOM_HEADER, "Authorization", "Bearer " + jwt];
        request_id = llHTTPRequest(url, parameters, "");
    }

    http_response(key id, integer status, list metadata, string body)
    {
        if (id == request_id)
        {
            llOwnerSay("status=" + (string)status + " body='" + body + "'");
        }
    }
}
```