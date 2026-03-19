---
name: "llList2Json"
category: "function"
type: "function"
language: "LSL"
description: 'This function takes a list and returns a JSON string of that list as either a json object or json array.

Returns a string that is either values serialized as a JSON type, or if an error was encountered JSON_INVALID.

To convert a json formatted string into a list use llJson2List.'
signature: "string llList2Json(string type, list values)"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llList2Json'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lllist2json"]
---

This function takes a list and returns a JSON string of that list as either a json object or json array.

Returns a string that is either values serialized as a JSON type, or if an error was encountered JSON_INVALID.

To convert a json formatted string into a list use llJson2List.


## Signature

```lsl
string llList2Json(string type, list values);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `type` |  |
| `list` | `values` |  |


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llList2Json)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llList2Json) — scraped 2026-03-18_

This function takes a list and returns a JSON string of that list as either a json object or json array.Returns a string that is either values serialized as a JSON type, or if an error was encountered JSON_INVALID.

## Caveats

- Note that string **values** items are interpreted as JSON, not LSL strings. Quotation marks, if required, must be added explicitly. For example, `llJson2List(llList2Json(JSON_ARRAY, ["bacon", "true", "false", "null"]))` returns the LSL list `["bacon", JSON_TRUE, JSON_FALSE, JSON_NULL]`, while `llJson2List(llList2Json(JSON_ARRAY, ["\"bacon\"", "\"true\"", "\"false\"", "\"null\""]))` returns the LSL list `["bacon", "true", "false", "null"]`

## Examples

```lsl
default
{
    state_entry()
    {
        list items;
        string json;

        items = ["89556747-24cb-43ed-920b-47caed15465f"];
        json = llList2Json(JSON_ARRAY, items);
        // ["89556747-24cb-43ed-920b-47caed15465f"]

        items = ["pi", 3.14, "set", "[1,2,3]", "status", "ok"];
        json = llList2Json(JSON_OBJECT, items);
        // {"pi":3.140000,"set":[1,2,3],"status":"ok"}

        items = [0, 3.14, "[1,2,3]", "{}"];
        json = llList2Json(JSON_ARRAY, items);
        // [0,3.140000,[1,2,3],{}]
    }
}
```

```lsl
string CSV2Json(string csv)
{
    list li = llCSV2List(csv);
    return llList2Json(JSON_ARRAY, li);
}
// This function converts a comma separated values string to a Json array string.
// CSV strings are often used for link-messages, notecards and they are easier to type as input commands.
// A Json-Array can store multiple of those as a nested list within the same Json-string via JSON_APPEND.
```

- You could store multiple lists that set different particle effects in the same string. Use LlList2Json() to write the string and llJson2List() to read the particle system defining lists from it. The loss in float-accuracy (Json has BAD float-to-string-conversion) does not matter as much for particle effects.

- You could store multiple lists, that set different llSetPrimitiveparamsFast() values for different situation (like different animation key frames), in the same Json String.

## See Also

### Constants

- JSON_ARRAY
- JSON_OBJECT
- JSON_INVALID

### Functions

- llJson2List
- llJsonGetValue
- llJsonSetValue
- llJsonValueType

### Articles

- Typecast

<!-- /wiki-source -->
