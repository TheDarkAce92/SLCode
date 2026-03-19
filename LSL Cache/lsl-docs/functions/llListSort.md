---
name: "llListSort"
category: "function"
type: "function"
language: "LSL"
description: "Returns a list that is src sorted by stride."
signature: "list llListSort(list src, integer stride, integer ascending)"
return_type: "list"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llListSort'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lllistsort"]
---

Returns a list that is src sorted by stride.


## Signature

```lsl
list llListSort(list src, integer stride, integer ascending);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `list` | `src` | List to be sorted. |
| `integer` | `stride` | number of entries per stride, if less than 1 it is assumed to be 1 |
| `integer` | `ascending` | if TRUE then the sort order is ascending, otherwise the order is descending. |


## Return Value

Returns `list`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llListSort)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llListSort) — scraped 2026-03-18_

Returns a list that is src sorted by stride.

## Caveats

- It uses an unoptimized selection sort algorithm, which is an algorithm with a Big O of N². A JIRA issue exists to improve this function, [SVC-2988](https://jira.secondlife.com/browse/SVC-2988).
- Originally the wiki stated that non-zero values for the "ascending" parameter would produce an ascending sort.  That was incorrect.  For this function, the value must be exactly 1 (or TRUE) for an ascending sort.
- Vectors are sorted by magnitude. [SVC-5643](https://jira.secondlife.com/browse/SVC-5643)
- Rotations are not sorted in any meaningful order. If a list containing only rotations is sorted in ascending order, it will be returned unchanged.
- For descending sort, if there are mixed types, the final order is deterministic (the same input will always produce the same output) but it can be completely useless.

```lsl
llListSort([2, "B", "C", 3, 1, "A"], 1, FALSE) // returns ["A", 3, 1, "C", "B", 2]
```

 If there are no mixed types, however, the descending sort works just fine.
- When the stride is greater than 1, if the list length is not a multiple of the stride, the list will be returned unchanged.
- When strings contain numbers, the numbers are still sorted left-to-right like any other character, which may not necessarily match numeric order:

```lsl
llListSort(["127", "3", "25"], 1, TRUE) // returns ["127", "25", "3"] because the 1 in 127 is before the 2 in 25 which is before the 3
```

 To sort them in numeric order, numbers in strings can be padded with zeros:

```lsl
llListSort(["127", "003", "025"], 1, TRUE) // returns ["003", "025", "127"]
```

  - This order differs from the order of items in a prim's inventory, which is "natural order" (e.g "New Script 2" is sorted before "New Script 11").

## Examples

```lsl
list numbers = [3, "three", 2, "two", 1, "one"];
default
{
    state_entry()
    {
        llOwnerSay(llDumpList2String(numbers, ","));
        // Object: 3,three,2,two,1,one
        numbers = llListSort(numbers, 2, TRUE);
        llOwnerSay(llDumpList2String(numbers, ","));
        // Object: 1,one,2,two,3,three
    }
}
```

### Video Tutorial

<videoflash type="youtube">BNIUHnpeUQs|640|385</videoflash>

## Notes

### Data Types

llListSort really only works on items of the same type. It will work on lists that hold diverse data types -- to be clear, it won't blow up your script -- but the results returned are usually meaningless.

```lsl
list mylist = ["brown", <0.000000, 0.000000, 0.000000>, "house", 17.005, 100, "cat", <3.000000, 3.000000, 3.000000>, 39];
list tmplist = llListSort(mylist, 1, TRUE);
llSay(0, llList2CSV(tmplist));
```

This returns in chat:

```lsl
brown, <0.000000, 0.000000, 0.000000>, cat, 17.004999, 39, house, <3.000000, 3.000000, 3.000000>, 100
```

The same ordered in descending order returns even more meaningless results:

```lsl
list mylist = ["brown", <0.000000, 0.000000, 0.000000>, "house", 17.005, 100, "cat", <3.000000, 3.000000, 3.000000>, 39];
list tmplist = llListSort(mylist, 1, FALSE);
llSay(0, llList2CSV(tmplist));
```

returns in chat:

```lsl
39, <3.000000, 3.000000, 3.000000>, cat, 100, 17.004999, house, <0.000000, 0.000000, 0.000000>, brown
```

### Utilizing the Results

It's important to note that the source list that you are sorting will remain unchanged. Instead, a new, sorted list will be produced. So, it's important that you capture this with a variable (unless you are acting directly on the results.)

```lsl
llListSort(myList, 1, TRUE); // You've wasted cpu time; you didn't capture the results

list newlist = llListSort(myList, 1, TRUE);// Okay. You've captured the results.

llSay(0,llList2CSV(llListSort(myList, 1, TRUE))); // No need to capture, using the results right away.
```

### Stride

Most times, you will want to set "integer stride" to 1 (0 also works) to tell it to sort each item in the list on its own basis. (If you are working with a strided list, though, see the special section below on sorting strides.)

### Sort Order

Setting the parameter "integer ascending" to TRUE returns a sorted list that is in ascending order.

For example: ["Apples", "Bananas", "Oranges"]

Setting the parameter "integer ascending" to FALSE returns a sorted list that is in descending order.

For example: ["Oranges", "Bananas", "Apples"]

### Sorting Strided Lists

If you have a strided list, in which you are keeping related pieces of data together in chunks, letting each list element sort on its own basis would be disastrous.

```lsl
list demographics = ["John Adams", "male", "2007-06-22", "Shirley Bassey", "female", "2005-11-02", "Matt Damon", "male", "2008-05-19"];
```

#### Bad Example

```lsl
list tmplist_1 = llListSort(demographics, 1, TRUE);
//tmplist_1 == ["2005-11-02", "2007-06-22", "2008-05-19", "John Adams", "Matt Damon", "Shirley Bassey", "female", "male", "male"]
//The strides have been destroyed, the sorted data is now useless
```

#### Good Example

Instead, because you have the data grouped (aka "strided") in sets of 3, you need to do this:

```lsl
list tmplist_2 = llListSort(demographics, 3, TRUE);
//templist_2 = ["John Adams", "male", "2007-06-22", "Matt Damon", "male", "2008-05-19", "Shirley Bassey", "female", "2005-11-02"]
```

When storing data in strided lists, it's often worth it down the road to take a moment at the outset to think about how you are most likely to want to sort them, if ever the need arose. Remember, you can only sort on the first element in each group of elements. If you think you're mostly likely to want to sort on gender (to use the above list example), you should make gender the first element in the data grouping.

## See Also

### Functions

- **llListRandomize** — Shuffles the elements of a list.

<!-- /wiki-source -->
