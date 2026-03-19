---
name: "llGetAgentLanguage"
category: "function"
type: "function"
language: "LSL"
description: "Returns a string that is the language code of the preferred interface language of the user avatar."
signature: "string llGetAgentLanguage(key avatar)"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetAgentLanguage'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetagentlanguage"]
---

Returns a string that is the language code of the preferred interface language of the user avatar.


## Signature

```lsl
string llGetAgentLanguage(key avatar);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `avatar` | avatar UUID that is in the same region |


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetAgentLanguage)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetAgentLanguage) — scraped 2026-03-18_

Returns a string that is the language code of the preferred interface language of the user avatar.

## Caveats

- If the user has "Share language with objects" disabled then this function returns an empty string.
- During a 1-5 seconds period after which an agent is logging in, this function will return an empty string as well, until the viewer sends the data to the simulator.
- Users may prefer to see the client interface in a language that is not their native language, and some may prefer to use objects in the native language of the creator, or dislike low-quality translations. Consider providing a manual language override when it is appropriate.
- New language/variant values may be added later. Scripts may need to be prepared for unexpected values.
- If the viewer is set to "System Default" the possible return may be outside the list given above. see [List of ISO 639-1 codes](http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) for reference.
- Viewers can specify other arbitrary language strings with the 'InstallLanguage' debug setting.  For example, launching the viewer with "--set InstallLanguage american" results this function returning 'american' for the avatar. [VWR-12222](https://jira.secondlife.com/browse/VWR-12222)

  - If the viewer supplies a multiline value, the simulator will only accept the first line and ignore all others. [SVC-5503](https://jira.secondlife.com/browse/SVC-5503)
- Older viewers may return "en-us" instead of "en".

## Examples

```lsl
default{
    touch_start( integer num_detected ){
        //-- loop through all detected touches
        for (num_detected -= 1; num_detected > -1; num_detected -= 1 ){
            key agent = llDetectedKey( num_detected );
            string name = llGetDisplayName( agent );
            string language = llGetAgentLanguage( agent );

            if (("" == name) || ("???" == name))
                name = llDetectedName( num_detected );

            //-- PUBLIC_CHANNEL is 0
            if (language == "es"){
                llSay( PUBLIC_CHANNEL, "¡Hola, " + name + "!" );
            }else if (language == "fr"){
                llSay( PUBLIC_CHANNEL, "Salut, " + name + " !" );
            }else if (language == "ja"){
                llSay( PUBLIC_CHANNEL, "やあ、　" + name + "！" );
            }else if (language == "de"){
                llSay( PUBLIC_CHANNEL, "Hallo, " + name + "!" );
            }else if (language == "en"){ //-- returned by some TPVs
                llSay( PUBLIC_CHANNEL, "Hello, " + name + "!" );
            }else if (language == "pt"){
                llSay( PUBLIC_CHANNEL, "Olá!, " + name + "!" );
            }else if (language == "ko"){
                llSay( PUBLIC_CHANNEL, "안녕하세요, " + name + "!" );
            }else if (language == "zh"){
                llSay( PUBLIC_CHANNEL, "你好啊， " + name + "！" );
            }else{ //-- Default to 'en-us' if language is unrecognized / not provided.
                llSay( PUBLIC_CHANNEL, "Hi there, " + name + "!" );
            }
        }
    }
}
```

<!-- /wiki-source -->
