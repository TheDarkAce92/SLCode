---
name: "llJson2List"
category: "function"
type: "function"
language: "LSL"
description: 'This function takes a string representing JSON, and returns a list of the top level.

Returns a list made by parsing src, a string representing json.

To convert a list into a json formatted string use llList2Json.'
signature: "list llJson2List(string json)"
return_type: "list"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llJson2List'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lljson2list"]
---

This function takes a string representing JSON, and returns a list of the top level.

Returns a list made by parsing src, a string representing json.

To convert a list into a json formatted string use llList2Json.


## Signature

```lsl
list llJson2List(string json);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `src` |  |


## Return Value

Returns `list`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llJson2List)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llJson2List) — scraped 2026-03-18_

This function takes a string representing JSON, and returns a list of the top level.Returns a list made by parsing src, a string representing json.

## Examples

```lsl
default
{
    state_entry()
    {
        list items;

        string value = "89556747-24cb-43ed-920b-47caed15465f";
        items = llJson2List(value);
        // ["89556747-24cb-43ed-920b-47caed15465f"]

        string object = "{\"pi\": 3.14, \"set\": [1,2,3], \"status\": \"ok\"}";
        items = llJson2List(object);
        // ["pi", 3.140000, "set", "[1,2,3]", "status", "ok"]

        string array = "[0, 3.14, [1,2,3], {}]";
        items = llJson2List(array);
        // [0, 3.140000, "[1,2,3]", "{}"]
    }
}
```

## See Also

### Functions

- llList2Json
- llJsonGetValue
- llJsonSetValue
- llJsonValueType

### Articles

- Typecast

<!-- /wiki-source -->
