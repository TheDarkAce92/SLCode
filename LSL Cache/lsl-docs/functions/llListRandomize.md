---
name: "llListRandomize"
category: "function"
type: "function"
language: "LSL"
description: "Returns a list which is a randomized permutation of src."
signature: "list llListRandomize(list src, integer stride)"
return_type: "list"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llListRandomize'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lllistrandomize"]
---

Returns a list which is a randomized permutation of src.


## Signature

```lsl
list llListRandomize(list src, integer stride);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `list` | `src` | A list you want to randomize. |
| `integer` | `stride` | number of entries per stride, if less than 1 it is assumed to be 1 |


## Return Value

Returns `list`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llListRandomize)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llListRandomize) — scraped 2026-03-18_

Returns a list which is a randomized permutation of src.

## Examples

```lsl
list dice = ["2", "4", "1", "6", "3", "5"];

default
{
    touch_start(integer num_detected) {
        list shuffled = llListRandomize(dice, 1);
        llOwnerSay(llList2CSV(shuffled));
    }
}
```



```lsl
list list01 = ["Cold", "pizza", "in", "the", "early", "morning"];

list list_random = llListRandomize(list01, 2);
```

list_random could be:

1. ["Cold", "pizza", "in", "the", "early", "morning"]
1. ["Cold", "pizza", "early", "morning", "in", "the"]
1. ["in", "the", "Cold", "pizza", "early", "morning"]
1. ["in", "the", "early", "morning", "Cold", "pizza"]
1. ["early", "morning", "Cold", "pizza", "in", "the"]
1. ["early", "morning", "in", "the", "Cold", "pizza"]

Notice that two adjacent elements from the original list are always kept together, because the stride of 2 was specified.

```lsl
list list_random = llListRandomize(list01, 6);
```

list_random in this instance is the original list, exactly in the order it already was, because we told it to keep every set of six elements together, and there are only six elements in the list.

## Notes

Bear in mind that the source list will remain unchanged. Instead, a new list will be produced. So, it's important that you capture this with a variable (unless you are acting directly on the results.)

## See Also

### Functions

- llListSort
- llFrand

<!-- /wiki-source -->
