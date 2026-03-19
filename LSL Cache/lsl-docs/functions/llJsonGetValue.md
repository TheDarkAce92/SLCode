---
name: "llJsonGetValue"
category: "function"
type: "function"
language: "LSL"
description: 'Gets the value indicated by specifiers from the json string.

Returns a string made by parsing json, a string representing json and traversing as specified by specifiers.

When the input is invalid or no result can be found this function returns JSON_INVALID. If the result is null the function retur'
signature: "string llJsonGetValue(string json, list specifiers)"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llJsonGetValue'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lljsongetvalue"]
---

Gets the value indicated by specifiers from the json string.

Returns a string made by parsing json, a string representing json and traversing as specified by specifiers.

When the input is invalid or no result can be found this function returns JSON_INVALID. If the result is null the function returns JSON_NULL.


## Signature

```lsl
string llJsonGetValue(string json, list specifiers);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `json` |  |
| `list` | `specifiers` |  |


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llJsonGetValue)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llJsonGetValue) — scraped 2026-03-18_

Gets the value indicated by specifiers from the json string.Returns a string made by parsing json, a string representing json and traversing as specified by specifiers.

## Caveats

- Manual definition of JSON syntax within LSL does not always parse in the expected way, so be careful to avoid using syntax characters anywhere other than where needed (for example, inside a string.); alternately escape the syntax character and use llUnescapeURL on the retrieved string to convert it back - See #bugs.

| ⚠️ | Warning: The below comment in regards to speed cannot be assumed to be true on all server versions and in all environments. Always test execution speed claims for yourself. |
| --- | --- |

- As of Second Life Server 2024-06-11.9458617693, benchmark testing in a 99%+ scripts run environment resulted in the following conclusions with a 3-element array cast to either JSON or CSV:

  - llJsonGetValue takes approximately 2-3 ms per call to execute regardless of depth, making it a faster option for reading a single element from a dataset.
  - llParseStringKeepNulls takes approximately 5 ms to execute, while each subsequent llList2String takes approximately 0.5 ms to execute, making it a faster option for reading more than 2 elements from a dataset.
- This function will convert the occurrence of a `\n` to a line feed and a `\t` to `U+0009`.

## Examples

```lsl
default {
    state_entry() {

     //below is an example of a JSON=string with a key called "key" and a value "val"
     string json1 = "{\"key\":\"val\"}";
     llSay(0, llJsonGetValue( json1, ["key"]));//returns "val" in localchat

     string json2 = "{\"mansBestFriend\":\"dog\"}";
     llSay(0, llJsonGetValue( json2, ["mansBestFriend"]));//returns "dog" in localchat
    }
}
```

```lsl
JGetValTest(){
    string j="[[1,2],[4,5,6]]";            //JSON may be written directly as a string like this in sl.
    string k;                              //this will change with each command below;
    k=llJsonGetValue(j,[]);                //returns the whole array of a JSON. It might just be one entry or a whole nested array or whole nested object.
    //if "j" is a single JSON_STRING, this may return what the string represents as a JSON within a string; a JSON_NUMBER , JSON_TRUE, TRUE ...

    k=llJsonGetValue("\"3.14\"",[]);       //==k="3,14" (float that was stored in a JSON_STRING within a JSON. and not as JSON_NUMBER for no good reason)
    k=llJsonGetValue("\"TRUE\""     ,[]);  //==k="TRUE" (the value was stored as a JSON_STRING and is thus returned verbatim)
    k=llJsonGetValue(j,[0]);               //returns only the first entry (at offset 0). An entry can be any JSON type,
                                           //each entry being separated by a comma from other entries.
                                           //array and object entries may contain multiple comma separated entries within them.
    k=llJsonGetValue(j,[1]);//returns only the second entry... (all the above still applies) k="[4,5,6]";
    k=llJsonGetValue(llJsonGetValue(j,[1]),[2]);
                                           //instead of getting an entry from "j" we get a sub-entry from llJsonGetValue(j,[1]),
                                           //assuming the sub-entry is a JSON_ARRAY. It returns the 3rd sub-entry of the second entry,
                                           //that is an array with 3 entries. it would make k="6".
                                           //it will return JSON_INVALID if there is no 3rd entry in the 2nd sub-array,
                                           //or no 2nd sub-array.
    k=llJsonGetValue(j,[1,2]);             //Shorter way to do the same as in the previous example.
    k=llJsonGetValue("true",[]);           //Sets k to JSON_TRUE
    k=llJsonGetValue("True",[]);           //Sets k to JSON_INVALID because the JSON constant for 'true' is all lower case
    k=llJsonGetValue("TRUE",[]);           //Sets k to JSON_INVALID because the JSON constant for 'true' is all lower case
    k=llJsonGetValue(JSON_TRUE,[]);        //Sets k to JSON_INVALID. The JSON_xxxx constants are not supposed to be part of
                                           // a JSON string, just values to test against.
}
```

See also llJsonValueType for examples where the value type is checked before getting the value as that type.

## See Also

### Functions

- llList2Json
- llJson2List
- llJsonSetValue
- llJsonValueType

### Articles

- Typecast

<!-- /wiki-source -->
