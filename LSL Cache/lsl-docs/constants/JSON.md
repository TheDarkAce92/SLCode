---
name: "JSON constants"
category: "constant"
type: "constant"
language: "LSL"
description: "Constants for JSON manipulation functions: JSON_APPEND, JSON_ARRAY, JSON_OBJECT, JSON_TRUE, JSON_FALSE, JSON_NULL, JSON_NUMBER, JSON_STRING, JSON_INVALID"
wiki_url: "https://wiki.secondlife.com/wiki/JSON_APPEND"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
---

# JSON Constants

Used with `llJsonGetValue`, `llJsonSetValue`, `llJsonValueType`, `llList2Json`, and `llJson2List`.

## Type Constants (for llJsonValueType return values)

| Constant | Value | Description |
|----------|-------|-------------|
| `JSON_INVALID` | `"\uFDD0"` | Invalid JSON or path not found |
| `JSON_OBJECT` | `"\uFDD1"` | JSON object `{}` |
| `JSON_ARRAY` | `"\uFDD2"` | JSON array `[]` |
| `JSON_NUMBER` | `"\uFDD3"` | JSON number |
| `JSON_STRING` | `"\uFDD4"` | JSON string |
| `JSON_NULL` | `"\uFDD5"` | JSON null |
| `JSON_TRUE` | `"\uFDD6"` | JSON true |
| `JSON_FALSE` | `"\uFDD7"` | JSON false |

## Modifier Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `JSON_APPEND` | -1 | Append to end of JSON array (used with llJsonSetValue) |

## Usage

```lsl
// Build a JSON object
string json = llList2Json(JSON_OBJECT, ["name", "Alice", "age", 30]);
// Result: {"name":"Alice","age":30}

// Build a JSON array
string arr = llList2Json(JSON_ARRAY, ["a", "b", "c"]);
// Result: ["a","b","c"]

// Get a value by path
string val = llJsonGetValue(json, ["name"]);
// Result: "Alice"

// Set a value
json = llJsonSetValue(json, ["score"], "100");

// Append to array
arr = llJsonSetValue(arr, [JSON_APPEND], "d");
// Result: ["a","b","c","d"]

// Check type
string t = llJsonValueType(json, ["age"]);
if (t == JSON_NUMBER) llOwnerSay("age is a number");

// Parse JSON to list
list parsed = llJson2List('{"x":1,"y":2}');
// Result: ["x", 1, "y", 2]

// Full example: HTTP response to JSON
http_response(key id, integer status, list meta, string body)
{
    if (status != 200) return;
    string name = llJsonGetValue(body, ["user", "name"]);
    if (name != JSON_INVALID)
        llOwnerSay("User: " + name);
}
```

## See Also

- `llJsonGetValue` — get a value from a JSON string by path
- `llJsonSetValue` — set a value in a JSON string
- `llJsonValueType` — get the type of a JSON value
- `llList2Json` — convert a list to JSON
- `llJson2List` — convert JSON to a list
