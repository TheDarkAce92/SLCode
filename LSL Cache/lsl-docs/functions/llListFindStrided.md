---
name: "llListFindStrided"
category: "function"
type: "function"
language: "LSL"
description: 'Returns the integer index of the first instance of test in src matching conditions.

If test matching range and stride conditions is not found in src, -1 is returned.
The length of test may be equal to or less than stride in order to generate a match.
The index of the first entry in the list is 0
If'
signature: "integer llListFindStrided(list src, list test, integer start, integer end, integer stride)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llListFindStrided'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Returns the integer index of the first instance of test in src matching conditions.

If test matching range and stride conditions is not found in src, -1 is returned.
The length of test may be equal to or less than stride in order to generate a match.
The index of the first entry in the list is 0
If test is found at the last index in src the positive index is returned (5th entry of 5 returns 4).
If start or end is negative, it is counted from the end list. The last element in the list is -1, the first is -list_length


## Signature

```lsl
integer llListFindStrided(list src, list test, integer start, integer end, integer stride);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `list` | `src` | what to search in (haystack) |
| `list` | `test` | what to search for (needle) |
| `integer` | `start` | Start of range to search |
| `integer` | `end` | End of range to search |
| `integer` | `stride` | Number of entries per stride within src |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llListFindStrided)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llListFindStrided) — scraped 2026-03-18_

Returns the integer index of the first instance of test in src matching conditions.

## Caveats

- Strict type matching and case sensitivity is enforced.

  - "1" != 1
  - "1.0" != 1.0
  - 1 != 1.0
  - "a822ff2b-ff02-461d-b45d-dcd10a2de0c2" != (key)"a822ff2b-ff02-461d-b45d-dcd10a2de0c2"
  - "Justice" != "justice"
- If test is an empty list the value returned is 0 rather than -1.

## Examples

```lsl
list mylist = ["a",0,"b",1,"c",2,"b",1];

integer result_a = llListFindStrided(mylist, ["b"], 0, -1, 1); //Stride 1 full range functionally equivalent to llListFindList(mylist,"b");
//result_a = 2

integer result_b = llListFindStrided(mylist, ["b",1], 2, -1, 1); //Inclusive range for start and end will find 2nd list in list
//result_b = 2

integer result_c = llListFindStrided(mylist, ["b"], 3, -1, 1); //The first "b" is at index 2 and will be skipped by starting at 3
//result_c = 6

integer result_d = llListFindStrided(mylist, ["b",1], 2, -1, 1); //Inclusive range for start and end will find 2nd item in list
//result_d = 2

integer result_e = llListFindStrided(mylist, ["b",1], 3, -1, 1); //The first "b",1 series is at index 2 and will be skipped by starting at 3
//result_e = 6

integer result_f = llListFindStrided(mylist, ["b",1], 3, -2, 1); //The first "b",1 series is at index 2 and will be skipped by starting at 3.  The second ["b",1] set exceeds the range criteria of the search.
//result_f = -1

integer result_g = llListFindStrided(mylist, ["b",2], 0, -1, 1); //No consecutive elements match ["b",2]
//result_g = -1

integer result_h = llListFindStrided(mylist, ["c"], 0, -1, 2); //With a stride of 2, "c" will be found.
//result_h = 4

integer result_i = llListFindStrided(mylist, ["c"], 0, -1, 3); //With a stride of 3, "c" won't be found.
//result_i = -1

integer result_j = llListFindStrided(mylist, ["c"], 0, -1, 4); //With a stride of 4, "c" will be found.
//result_j = 4

integer result_k = llListFindStrided(mylist, ["c"], 1, -1, 2); //While the stride is even, starting at the 2nd element will miss this stride.
//result_k = -1
```

```lsl
list numbers = [1, 2, 3, 4, 5];
default
{
    state_entry()
    {
        integer index = llListFindStrided(numbers, [3], 0, -1, 1);  //Functionally identical to llListFindList(numbers, [3]);
        if (index != -1)
        {
            list three_four = llList2List(numbers, index, index + 1);
            llOwnerSay(llDumpList2String(three_four, ","));
            // Object: 3,4
        }
    }
}
```

```lsl
//You can also search for two items at once to find a pattern in a list
list avatarsWhoFoundMagicLeaves = ["Water Duck", "Green Ham", "Fire Centaur","Red Leaf"];
default
{
    state_entry()
    {
        integer index = llListFindStrided(avatarsWhoFoundMagicLeaves, ["Fire Centaur","Red Leaf"],0,-1,2);
        if (index != -1)
        {
            list output = llList2List(avatarsWhoFoundMagicLeaves, index, index + 1);
            llOwnerSay(llDumpList2String(output, ","));
            // Object: Fire Centaur, Red Leaf
        }
    }
}
```

```lsl
//It's nearly a database
list food_db = ["FIRSTNAME", "LASTNAME", "FAVORITE FOOD", "ALLERGIES",
                                   "Awesome", "Resident","Apples",0,
                                   "Charlie", "Kites", "Peanuts", "dogs",
                                   "Cool", "McLastname", "Burgers","peanuts"];
default
{
    state_entry()
    {
        list potential_allergen = ["peanuts"];
        integer any_allergies = llListFindStrided(food_db, potential_allergen,4,-1,4);
        if (any_allergies != -1)
        {
            llOwnerSay("Every can eat it");
        }
        else
        {
            list output = llList2List(food_db, any_allergens - 3, any_allergens - 2);
            llOwnerSay(llDumpList2String(output, " ")+" is allergic to it!");
            // Object: Cool McLastName is allergic to peanuts
        }
    }
}
```

## See Also

### Functions

- **llSubStringIndex** — Find a string in another string

<!-- /wiki-source -->
