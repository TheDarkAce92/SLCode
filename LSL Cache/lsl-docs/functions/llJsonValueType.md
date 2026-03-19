---
name: "llJsonValueType"
category: "function"
type: "function"
language: "LSL"
description: 'Gets the JSON type for the value in json at the location specifiers.

Returns the string specifying the type of the value at specifiers in json.'
signature: "string llJsonValueType(string json, list specifiers)"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llJsonValueType'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lljsonvaluetype"]
---

Gets the JSON type for the value in json at the location specifiers.

Returns the string specifying the type of the value at specifiers in json.


## Signature

```lsl
string llJsonValueType(string json, list specifiers);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `json` | A string serialization of a json object. |
| `list` | `specifiers` | A path to a value in the json parameter. |


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llJsonValueType)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llJsonValueType) — scraped 2026-03-18_

Gets the JSON type for the value in json at the location specifiers.Returns the string specifying the type of the value at specifiers in json.

## Examples

```lsl
//all these functions are untested functions that may have some very strange cases were they acd badly or where the comments are wrong
//see them as buggy PSEUDO-code and consider yourself lucky if there are less than 2 wrong counters and 4 bad pointers/names.
//they are more an example and a concept and unlikely fully functional AS IS.

string JisN(string j){if(llJsonValueType(j,[])==JSON_NUMBER  )return llJsonGetValue(j,[]);return "";}
//return the JSON if "j" is a JSON_NUMBER, like j="10.1234"  j="-0.1234"  j="3.14159"  j="-1" j="123456"   otherwise return "";
//these would be sting representations of a float because j is a string.
//storing floats in a JSON will easily lose you a lot of accuracy. Integers stored in JSON may have a smaller range than 32-bit signed integers.

string JisA(string j){if(llJsonValueType(j,[])==JSON_ARRAY  )return llJsonGetValue(j,[]);return "";}
//return the JSON if "j" is a JSON_ARRAY, like j="[]"   j="[1,2]"  j="[[1],[3,4]]"                        otherwise return "";
//these would be string representations of a (nested) list because j is a string.

string JisS(string j){if(llJsonValueType(j,[])==JSON_STRING )return llJsonGetValue(j,[]);return "";}
//return the string that is stored in "j" if "j" is a JSON_STRING, like j="\"PI\""   j="\"3.14\""   j="\"-1\"" otherwise return "";
//these would be string representations of a string, typecast with \" as that within itself,
//because j is a string that is also able to store numbers and floats and (nested) lists ... as strings.
//this returns the string within "j" if "j" is "A string within a string".

/*the above functions return strings to be used in simple
if(JisN(j)){}
if(JisA(j)){}
if(JisS(j)){}
//conditions as if they are booleans. //the boolean-ish condition works because "" equals FALSE within LSL.
The functions MAY return a JSON_STRING or JSON_ARRAY can be useful recursively as shown below:
*/

JstringPARSED(string j){
    //j="\"PI\"";
    //j="\"3.14\"";
    //j="\"-1\"";
    string JayWeHaveToGoDeeperS = JisS(JisS(j));
    llOwnerSay( JayWeHaveToGoDeeperS ); // says "PI", or ""        , or ""         , because "3.14" is a JSON_NUMBER and "-1" is a JSON_NUMBER but not a JSON_STRING
    string JayWeHaveToGoDeeperN = JisN(JisS(j));
    llOwnerSay( JayWeHaveToGoDeeperN ); // says ""  , or "3.14000" , or "-1.0000",   because "PI" is a JSON_STRING but "PI" is not a JSON_NUMBER


    if (llJsonValueType(j,[])==JSON_INVALID){}//would be TRUE for j="";
}

//==== End of JstringPARSED(j) ===== start of Jnested(j) for  nested/recursive lists =====

Jnested(string j,list rope){//goes trough each value of a nested JSON_ARRAY and says its value and its "position-list"
    //j="[]";
    //j="[[1],[2]]";
    //j="[-1,[2]]";
    //j="[[1],-2]";
    //j="[[-3,-4]]";  //the only true case HERE for = JisA(JisA(j)); below
    string JayWeHaveToGoDeeperA = JisA(JisA(j));

    string subJ=JisA(j);
    if (subJ){
        //here you actually have to loop trough each entry of the subJ JSON_LIST to test its TYPE for each entry (if we want to go deeper recursively)
        //You can go deeper once you know if entry number x is a JSON_LIST (NESTED!!!) or JSON_STRING (for some reason)
        //first see how many list entries there are; we go trough entries of subJ starting on the left until its a JSON_INVALID
        list types;
        integer i = -1;
        while (++i != -1){
             string type=llJsonValueType(j,[i]);//stores the TYPE of "j"'s entry at position i as "type"
             if (type==JSON_INVALID) i=-2; //this exits this the while-loop
             else types += [type];  // the list "types" will store all the JSON types, until the first invalid one is reached. (which which should also be for "out of bounds"
        }

        //this is split in 2 loops to explain 1 task by splitting it in 2 smaller tasks. Actually the loops above and below could be merged easily.

        i=llGetListLength(types);//we now have a list that lists all JSON types of j; lets see how long it is;
        //and we loop trough all types, calling THIS function recursively if the list contains another nested list in it at position i
        while (i--){//I like to go reverse from right to left when ever possible, its faster (??) and costs less memory in LSL (??)
             if (llList2String(types,i)==JSON_ARRAY || llList2String(types,i)==JSON_OBJECT){
                  Jnested(llJsonGetValue(j,[i]));//the function calls itself here, recursively to go trough the nested JSON_ARRAY or JSON_OBJECT
            }
            else{
                llOwnerSay("["+llList2CSV(rope)+"]== "+llJsonGetValue(j,[i]));
                //read from your list what json type is at this position and do something with it.
}}}}
//Jnested(json,[]);//would print each value of the nexted JSN_ARRAY with its "address list", that is building up recursively as "rope" that leads you trough the tree/maze.

//Jnested(j) should be useful to read from large matrices (as in 300x300 fields) that may even contain complex numbers at some places.
//I tried to read very long JSONs with llGetSubString(), but llGetSubString() too easily stack-heap collides on very long strings,
//so you have to go trough the nested list using Jnested(j) to read and print it per entry.
```

## See Also

### Functions

- llList2Json
- llJson2List
- llJsonSetValue
- llJsonGetValue

### Articles

- Typecast

<!-- /wiki-source -->
