---
name: "llJsonSetValue"
category: "function"
type: "function"
language: "LSL"
description: 'Returns, if successful, a new JSON text string which is json with the value indicated by the specifiers list set to value.

If unsuccessful (usually because of specifying an out of bounds array index) it returns JSON_INVALID.

An 'out of bounds array index' is defined to be any Integer specifiers gr'
signature: "string llJsonSetValue(string json, list specifiers, string value)"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llJsonSetValue'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lljsonsetvalue"]
---

Returns, if successful, a new JSON text string which is json with the value indicated by the specifiers list set to value.

If unsuccessful (usually because of specifying an out of bounds array index) it returns JSON_INVALID.

An "out of bounds array index" is defined to be any Integer specifiers greater than the length of an existing array at that level within the Json text or greater than 0 (zero) at a level an array doesn't exist.

A special specifiers, JSON_APPEND, is accepted which appends the value to the end of the array at the specifiers level. Care should be taken- if that level is not an array, the existing Value there will be overwritten and replaced with an array containing value at it's first (0) index.

Contrary to lists and strings, negative indexing of Json arrays is not supported.

If an existing "Key" is specifiers at that level, its Value will be overwritten by value unless value is the magic value JSON_DELETE. If a value does not exist at specifiers, a new Key:Value pair will be formed within the Json object.

To delete an existing value at specifiers, use JSON_DELETE as the value. Note it will not prune empty objects or arrays at higher levels.

If value is JSON_TRUE, JSON_FALSE or JSON_NULL, the Value set will be the bare words 'true', 'false' or 'null', respectively, at the specifiers location within json.

specifiers does not support negative indexes.


## Signature

```lsl
string llJsonSetValue(string json, list specifiers, string value);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `json` | source JSON data |
| `list` | `specifiers` | location of the of the value to be added, updated or deleted. |
| `string` | `value` | new value or JSON_DELETE flag. |


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llJsonSetValue)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llJsonSetValue) — scraped 2026-03-18_

Returns, if successful, a new JSON text string which is json with the value indicated by the specifiers list set to value.

## Caveats

| ⚠️ | Warning: The below comment in regards to speed is unverified on modern simulator versions, and thus cannot be assumed to be true. Always test execution speed claims for yourself. |
| --- | --- |

- llListReplaceList() is roughly 2.8x as fast in replacing a single value of a list than llJsonSetValue() is to replace a single value in a json.

The length of the list/json are irrelevant here.

## Examples

```lsl
string TEST_STRING_JSON;

init()
{
    TEST_STRING_JSON = "[9,\"<1,1,1>\",false,{\"A\":8,\"Z\":9}]";

//  [9,"<1,1,1>",false,{"A":8,"Z":9}]
    say("Original TEST_STRING_JSON: " + TEST_STRING_JSON);
}

run_json_test(string input)
{
    string output;

//  changing values within the json string

//  change the first value in the array to 10
    output = llJsonSetValue(input, [0], "10");

//  [10,"<1,1,1>",false,{"A":8,"Z":9}]
    say("( 1): " + output);

//  change the third value in the array to 'true'
    output = llJsonSetValue(input, [2], JSON_TRUE);

//  [9,"<1,1,1>",true,{"A":8,"Z":9}]
    say("( 2): " + output);

//  change the value of "A" within the Json object to 3
    output = llJsonSetValue(input, [3, "A"], "3");

//  [9,"<1,1,1>",false,{"A":3,"Z":9}]
    say("( 3): " + output);

//  adding a value or new key-value-pair within the input

//  add the value "Hello" to the end of the array
//      NOTE: One cannot insert, only add to the end
    output = llJsonSetValue(input, [JSON_APPEND], "Hello");

//  [9,"<1,1,1>",false,{"A":8,"Z":9},"Hello"]
    say("( 4): " + output);

//  add the key-value-pair "B":10 to the object
    output = llJsonSetValue(input, [3, "B"], "10");

//  [9,"<1,1,1>",false,{"A":8,"B":10,"Z":9}]
    say("( 5): " + output);

//  Things to look out for when modifying Json text
//      ~!~ Be careful when using this function ~!~

//  out of bounds array assignment:
//      defined as attempting to add a value to a position ...
//      ...greater than the length of the array (which may be 0)
//      JSON_APPEND is ALWAYS the preferred way to add to an array
    output = llJsonSetValue(input, [5], "10");

//  %EF%B7%90 (URL escaped JSON_INVALID)
    say("( 6): " + llEscapeURL(output));

//  BUT, this works, since it is in bounds
//      (eqivalent to JSON_APPEND in this case)
    output = llJsonSetValue(input, [4], "10");

//  [9,"<1,1,1>",false,{"A":8,"Z":9},10]
    say("( 7): " + output);

//  careless formation of new arrays
//      ( the 4 and all subsequent 0's are all in bounds.)
    output = llJsonSetValue(input, [4, 0, 0, 0], "10");

//  [9,"<1,1,1>",false,{"A":8,"Z":9},[[[10]]]]
    say("( 8): " + output);

//  overwriting an object with an array:
//      ~!~ mistaken use of JSON_APPEND on an object ~!~
    output = llJsonSetValue(input, [3, JSON_APPEND], "10");

//  [9,"<1,1,1>",false,[10]]
    say("( 9): " + output);

//  careless formation of new objects
//      NOTE: "Key" assignemts will NEVER result in a return of JSON_INVALID!
    output = llJsonSetValue(input, [3, "W", "X"], "10");

//  [9,"<1,1,1>",false,{"A":8,"W":{"X":10},"Z":9}]
    say("(10): " + output);

    output = llJsonSetValue(input, [3, "W", "X", "Y"], "10");

//  [9,"<1,1,1>",false,{"A":8,"W":{"X":{"Y":10}},"Z":9}]
    say("(11): " + output);

//  overwriting an array with an object
    output = llJsonSetValue(input, ["X"], "10");

//  {"X":10}
    say("(12): " + output);

//  special case considerations:

//  BUG-3692: (NOTE: Corrected in release 13.09.21.281328!)
//      a bug where, instead of JSON_INVALID being returned, if the out of
//      bounds index is at a lower level than the topmost (root) level, a
//      non-compliant JSON text would be formed
    output = llJsonSetValue(input, [1, 7], "Disappearing Text");

//  Note the "empty" second position that resulted in the returned array
//  [9,,false,{"A":8,"Z":9}]
// (But now correctly shows JSON_INVALID)
    say("(13): " + output);

//  though there is no way to directly delete a key-value-pair
//  nor remove a value from an array,
//  the use of JSON_NULL may prove adequate
    output = llJsonSetValue(input, [3, "A"], JSON_NULL);

//  [9,"<1,1,1>",false,{"A":null,"Z":9}]
    say("(14): " + output);

//  if a JSON text object has been formed with llList2Json()
//  that contains one or more duplicated "Keys", (allowable
//  but NOT recommended!) ANY change
//  made to that object will correct the condition,
//  with all but the last such "Key" being removed
    output = llList2Json(JSON_OBJECT, ["A", 1, "A", 2, "A", 3, "B", 4, "B", 4]);

//  both Keys "A" and "B" are duplicated
//  {"A":1,"A":2,"A":3,"B":4,"B":4}
    say("(15): " + output);

//  only the last value of the duplications is accessable though

//  3
    say("(16): " + llJsonGetValue(output, ["A"]));

//  condition corrected by adding a key-value-pair...

//  {"A":3,"B":4,"Z":5}
    say("(17): " + llJsonSetValue(output, ["Z"], "5"));

//  ... or by changing a value

// {"A":5,"B":4}
    say("(18): " + llJsonSetValue(output, ["A"], "5"));
}

say(string message)
{
    llOwnerSay(message);
//  llRegionSayTo(llGetOwner(), PUBLIC_CHANNEL, message);
//  llWhisper(PUBLIC_CHANNEL, message);
}

default
{
    on_rez(integer start_param)
    {
        llResetScript();
    }

    state_entry()
    {
        init();
    }

    touch_end(integer num_detected)
    {
//      copy 'TEST_STRING_JSON' from the following function call
//      to the string 'input' in the function declaration
//      and run a test on 'input' to not (!) modify 'TEST_STRING_JSON'
//      but its copy instead
        run_json_test(TEST_STRING_JSON);
    }
}
```

Double-quotes in string values are escaped. The following script inserts literal `string \"with\" quote` instead of `string "with" quotes` as the JSON value.

```lsl
default
{
    state_entry()
    {
        string test = "[\"a\"]";
        string add = "string \"with\" quotes";
        llOwnerSay(llJsonSetValue(test, [JSON_APPEND], add));
    }
}
```

## See Also

### Functions

- llList2Json
- llJson2List
- llJsonGetValue
- llJsonValueType

### Articles

- Typecast

<!-- /wiki-source -->
