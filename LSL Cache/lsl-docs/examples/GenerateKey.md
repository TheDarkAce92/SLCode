---
name: "GenerateKey"
category: "example"
type: "example"
language: "LSL"
description: "Generates a key using Type 3 (MD5) UUID generation to create a unique key using region-name, object-key, service and variable."
wiki_url: "https://wiki.secondlife.com/wiki/GenerateKey"
author: "llGenerateKey"
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL


GenerateKeyGenerateKey

- 1 Summary
- 2 Examples
- 3 Implementation
- 4 Optimisation

## Summary

 Function: key **GenerateKey**( string service, string variable );

Generates a key using Type 3 (MD5) UUID generation to create a unique key using region-name, object-key, service and variable.

**NOTE:** this function has been largely superseded by llGenerateKey() which is faster; however, the implementation on this page does have some further uses, as it is able to generate predictable random keys which is useful if you wish to avoid the need to track lists of recent keys. For example, using the optimised form of this function, two scripts using the same URI for key generation can produce the same set of keys using a synchronised variable, useful for generating a new key for each message, that can be predicted ahead of time (rather than keeping a list of recent keys to ignore).Returns a key The generated key

• string

service

–

The service, object, function, or whatever else this key may represent.

• string

variable

–

Any variable(s) relevant to the service that uniquely distinguish it.

## Examples

In a two-prim linked-set put the following script (adding generateKey where noted) into the child-prim:

```lsl
integer requestID = 0;

// Add generateKey here!!

default {
    touch_start(integer x) {
        llMessageLinked(
            LINK_ROOT,
            1234,
            "I am a request",
            generateKey("echo", (string)requestID++)
        );
    }

    link_message(integer x, integer y, string msg, key id) {
        if (y == 1234)
            llOwnerSay("Request: " + (string)id + " = " + msg);
    }
}
```

And the following script in the root-prim:

```lsl
default {
    link_message(integer x, integer y, string msg, key id) {
        if (y == 1234) // Echo, send straight back
            llMessageLinked(x, y, msg, id);
    }
}
```

Simply touch the child-prim to use, enjoy!


Implementation

```lsl
key generateKey(string service, string variable) {
    return (key)llInsertString(
        llInsertString(
            llInsertString(
                llInsertString(
                    llMD5String(
                        "secondlife://" + llGetRegionName()  + "/" +
                            (string)llGetKey() + "/" +
                            (string)llGetLinkNumber() + "/" +
                            llGetScriptName() + "/" +
                            service + "/" + variable,
                        0 // This is reserved by specification, will
                          // be increased with new/different versions.
                    ),
                    8,
                    "-"
                ),
                13,
                "-"
            ),
            18,
            "-"
        ),
        23,
        "-"
    );
}
```

Optimisation

Instead of always calling llGetRegionName(), llGetKey(), llGetLinkNumber(), and llGetScriptName(), you may wish to cache their return values into a `uri` variable, and only dynamically add the service and variable parameters each-time. Remember to update this variable when you know it's components will have changed, using the changed(), on_rez(), and/or attach() events.

Here is an example of the caching version of the function:

```lsl
string uri;
key generateKey(string service, string variable) {
    if (uri == "")
        uri =  "secondlife://" + llGetRegionName()  + "/" +
            (string)llGetKey() + "/" +
            (string)llGetLinkNumber() + "/" +
            llGetScriptName() + "/";
    return (key)llInsertString(
        llInsertString(
            llInsertString(
                llInsertString(
                    llMD5String(
                        uri + service + "/" + variable,
                        0 // This is reserved by specification, will
                          // be increased with new/different versions.
                    ),
                    8,
                    "-"
                ),
                13,
                "-"
            ),
            18,
            "-"
        ),
        23,
        "-"
    );
}

integer counter = 0;
default {
    state_entry() {
        llSetTimerEvent(10.0);
    }

    on_rez(integer x) { uri = ""; }
    attach(key id) { uri = ""; }
    changed(integer changes) {
        if (changes & (CHANGED_REGION | CHANGED_INVENTORY)) uri = "";
    }

     timer() {
        llOwnerSay("Random key of the moment is \"" + (string)generateKey("counter", (string)(counter++)) + "\"");
    }
}
```