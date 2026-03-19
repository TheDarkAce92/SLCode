---
name: "llLinksetDataFindKeys"
category: "function"
type: "function"
language: "LSL"
description: "The llLinksetDataFindKeys function returns a list of up to count keys from the datastore that match pattern, starting at the one indicated by start. If count is less than 1, then all keys between start and the end which match pattern are returned. If count minus start exceeds the number of matching "
signature: "list llLinksetDataFindKeys(string pattern, integer start, integer count)"
return_type: "list"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llLinksetDataFindKeys'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

The llLinksetDataFindKeys function returns a list of up to count keys from the datastore that match pattern, starting at the one indicated by start. If count is less than 1, then all keys between start and the end which match pattern are returned. If count minus start exceeds the number of matching keys, the returned list will be shorter than count, down to a zero-length list if start equals or exceeds the number of matching keys. The list is ordered alphabetically.

Returns a list of the keys in the datastore.


## Signature

```lsl
list llLinksetDataFindKeys(string pattern, integer start, integer count);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `pattern` | A regular expression describing which keys to return. |
| `integer` | `start` | The first key to return. |
| `integer` | `count` | The number of keys to return. |


## Return Value

Returns `list`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llLinksetDataFindKeys)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llLinksetDataFindKeys) — scraped 2026-03-18_

The llLinksetDataFindKeys function returns a list of up to count keys from the datastore that match pattern, starting at the one indicated by start. If count is less than 1, then all keys between start and the end which match pattern are returned. If count minus start exceeds the number of matching keys, the returned list will be shorter than count, down to a zero-length list if start equals or exceeds the number of matching keys. The list is ordered alphabetically.Returns a list of the keys in the datastore.

## Caveats

- The maximum length for pattern seems to be 800 characters.
- There seems to be a timing restriction. If the time limit is exceeded, the function fails silently.

  - Returns an empty list and the script continues execution.

## Examples

When pattern matches multiple keys, start can be used to skip over some of the first matches.

```lsl
default
{
    state_entry()
    {
        llLinksetDataWrite("ThingA_config", "value");
        llLinksetDataWrite("ThingA_data",   "value");
        llLinksetDataWrite("ThingB_config", "value");
        llLinksetDataWrite("ThingB_data",   "value");
        llLinksetDataWrite("ThingC_config", "value");
        llLinksetDataWrite("ThingC_data",   "value");
        list keys;

        // Return 1 key starting from the first match.
        keys = llLinksetDataFindKeys("Thing", 0, 1);
        llOwnerSay(llList2CSV(keys)); // ThingA_config

        // Return 1 key after skipping the first 3 matches.
        keys = llLinksetDataFindKeys("Thing", 3, 1);
        llOwnerSay(llList2CSV(keys)); // ThingB_data

        // Return up to 10 keys after skipping the first match.
        keys = llLinksetDataFindKeys("_data", 1, 10);
        llOwnerSay(llList2CSV(keys)); // ThingB_data, ThingC_data
    }
}
```

The following regular expression code can be used to find UUID keys. (Such as those use to identify user UUID)

```lsl
        list keysFound = llLinksetDataFindKeys("(?i)^[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}$",  0, 0);
```

The following code can also be used to find UUID keys in LinksetData memory.

```lsl
        list keysFound = llLinksetDataFindKeys("^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$",  0, 0);
```

*Warning: Keep track of how many UUIDs will be returned, as too many can overwhelm script memory and cause a stack-heap crash.*



The script below uses llLinksetDataFindKeys for blacklist management.

```lsl
integer gDialogChannel;
integer gDialogHandle;
integer gManagingBlocks;

startDialog(key person)
{
    gManagingBlocks = 0;
    gDialogHandle = llListen(gDialogChannel, "", person, "");
    llDialog(person, "\nSelect action", ["List blocks", "Add block", "Remove block"], gDialogChannel);
    llSetTimerEvent(60);
}

stopDialog()
{
    llSetTimerEvent(0);
    llListenRemove(gDialogHandle);
}

default
{

    on_rez(integer sp)
    {
        llResetScript();
    }

    state_entry()
    {
        gDialogChannel = (integer)(llFrand(-10000000)-10000000);
        llListen(PUBLIC_CHANNEL, "", NULL_KEY, "");;
    }

    timer()
    {
        stopDialog();
    }

    touch_start(integer nd)
    {
        key toucherKey = llDetectedKey(0);
        if (toucherKey == llGetOwner())
        {
            startDialog(toucherKey);
        }
    }

    listen(integer channel, string name, key id, string message)
    {

        if (llGetAgentSize(id) == ZERO_VECTOR)
        {
            return;
        }

        if (channel == gDialogChannel)
        {
            stopDialog();
            if (gManagingBlocks)
            {
                message = llStringTrim(message, STRING_TRIM);
                if ((key)message)
                {
                    if (gManagingBlocks == 1)
                    {
                        llOwnerSay("Addition request has been sent to the blacklist storage");
                        llLinksetDataWrite("blocklist:" + message, "1");
                    }
                    else
                    {
                        llOwnerSay("Removal request has been sent to the blacklist storage.");
                        llLinksetDataDelete("blocklist:" + message);
                    }
                }
                else
                {
                    llOwnerSay("The UUID '" + message + "' appears to be invalid.");
                }
                startDialog(id);
            }
            else if (message == "List blocks")
            {
                list blocks = llLinksetDataFindKeys("^blocklist:", 0, 0);
                integer listLength = llGetListLength(blocks);
                llOwnerSay("Blacklist items: " + (string)listLength);
                integer i;
                while (i < listLength)
                {
                    string record = llGetSubString(llList2String(blocks, i), 10, -1);
                    llOwnerSay("- secondlife:///app/agent/" + record + "/about" + " - " + record);
                    ++i;
                }
                blocks = [];
                startDialog(id);
            }
            else if (message == "Add block" || message == "Remove block")
            {
                string label = "add to";
                gManagingBlocks = 1;
                if (message == "Remove block")
                {
                    gManagingBlocks = 2;
                    label = "remove from";
                }
                gDialogHandle = llListen(gDialogChannel, "", id, "");
                llTextBox(id, "\nPlease specify one single avatar UUID you'd like to " + label + " the blacklist storage.", gDialogChannel);
                llSetTimerEvent(60);
            }
            return;
        }

        if (llGetListLength(llLinksetDataFindKeys("blocklist:" + (string)id, 0, 1)) > 0)
        {
            llRegionSayTo(id, 0, "You're blacklisted.");
            return;
        }

        llRegionSayTo(id, 0, "Hello there, secondlife:///app/agent/" + (string)id + "/about - your message: " + message);

    }

    linkset_data(integer action, string name, string value)
    {
        if (action == LINKSETDATA_RESET || action == LINKSETDATA_DELETE || action == LINKSETDATA_UPDATE)
        {
            llOwnerSay("Blacklist storage modified.");
        }
    }

}
```

## Notes

### Regular Expression Cheat Sheet

| Wildcard |  |  |
| --- | --- | --- |
| . | Matches any character |  |
| Anchors |  |  |
| ^ | Matches the beginning of the string. |  |
| $ | Matches the end of the string. |  |
| Expression Prefixes |  |  |
| (?i) | Makes search string case insensitive. | This must be the first thing that appears in the search string. "(?i)apple" will match "apple", "APPLE", "ApPlE", and any other combination of upper and lower case characters. |
| $ | Matches the end of the string. |  |
| Repeats |  |  |
| * | Matches the preceding atom 0 or more times. |  |
| + | Matches the preceding atom 1 or more times. |  |
| ? | Matches the preceding atom 0 or 1 times. |  |
| {n} {n,} {n, m} | Matches the preceding atom n, n or more, or between n and m times. |  |
| Sub-expressions |  |  |
| (expression) | Text enclosed in parentheses is a marked sub-expression. Text matched as part of a sub-expressions is split out and may be repeated. |  |
| Alternation |  |  |
| a \| b | Match either a or b. |  |
| Character Sets |  |  |
| [abc] | Matches any one of the enumerated characters. |  |
| [a-c] | Matches any character in the specified range. |  |
| [^abc] | Matches any character other than the enumerated characters. |  |
| [[:name:]] | Matches any character of the named class. |  |
|  | Any of the above character set definitions may be combined. |  |
| Escape Sequences |  |  |
|  | Specific Characters |  |
| \e | ASCII 0x1B, ESC |  |
| \n | New line |  |
| \r | Carriage return |  |
| \t | Tab |  |
| \xdd | Matches an ASCII character with the code dd |  |
|  | Single character classes |  |
| \d \D | Any decimal digit. | - **\d** → [[:digit:]] or [0-9] - **\D** → [^[:digit:]] or [^0-9] |
| \l \L | Any lower case character. | - **\l** → [[:lower:]] or [a-z] - **\L** → [^[:lower:]] or [^a-z] |
| \s \S | Any whitespace character. | - **\s** → [[:space:]] or [ \t\r\n] - **\S** → [^[:space:]] or [^ \t\r\n] |
| \u \U | Any upper case character. | - **\u** → [[:upper:]] or [A-Z] - **\U** → [^[:upper:]] or [^A-Z] |
| \w \W | Any "word" character. Alphanumeric plus underscore | - **\w** → [[:upper:][:lower:][:digit:]_] or [A-Za-z0-9_] - **\W** → [^[:upper:][:lower:][:digit:]_] or [^A-Za-z0-9_] |
|  | Word boundaries |  |
| \< | Start of word. |  |
| \> | End of word |  |
| \b |  |  |
| \B | Not a word boundary. |  |
| *Note* LSL uses '\' as an escape character in strings. The escape characters above must be double escaped. So "\d" needs to be written in LSL as "\\d" Please see LSL Strings, Escape Codes |  |  |
| Named Character Classes |  |  |
| alnum | Any alpha-numeric character. | - [[:alnum:]] → [0-9a-zA-Z] - [^[:alnum:]] → [^0-9a-zA-Z] |
| alpha | Any alphabetic character. | - [[:alpha:]] → [a-zA-Z] - [^[:alpha:]] → [^a-zA-Z] |
| blank | Any whitespace character that is not a line separator. |  |
| cntrl | Any control character | - [[:cntrl:]] → [\x01-\x31] - [^[:cntrl:]] → [^\x01-\x31] |
| digit d | Any decimal digit | - [[:digit:]] → [0-9] - [^[:digit:]] → [^0-9] |
| lower l | Any lower case character. | - [[:lower:]] → [a-z] - [^[:lower:]] → [^a-z] |
| print | Any printable character. |  |
| punct | Any punctiation character. |  |
| space s | Any whitespace character. |  |
| upper u | Any upper case character. | - [[:upper:]] → [A-Z] - [^[:upper:]] → [^A-Z] |
| word w | Any control character | - [[:word:]] → [0-9a-zA-Z_] - [^[:word:]] → [^0-9a-zA-Z_] |
| xdigit | Any hexadecimal digit character | - [[:xdigit:]] → [0-9a-fA-F] - [^[:xdigit:]] → [^0-9a-fA-F] |

## See Also

### Functions

- llLinksetDataAvailable
- llLinksetDataCountKeys
- llLinksetDataDelete
- llLinksetDataDeleteProtected
- llLinksetDataListKeys
- llLinksetDataRead
- llLinksetDataReadProtected
- llLinksetDataReset
- llLinksetDataWrite
- llLinksetDataWriteProtected

<!-- /wiki-source -->
