---
name: "Merge Sort"
category: "example"
type: "example"
language: "LSL"
description: "Created by Xaviar Czervik. Do whatever you wish with this function: Sell it (good luck), use it, or modify it."
wiki_url: "https://wiki.secondlife.com/wiki/Merge_Sort"
author: "Xaviar Czervik"
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Created by Xaviar Czervik. Do whatever you wish with this function: Sell it (good luck), use it, or modify it.

This code sorts a list through use of a Merge Sort. I have no idea why you would want to use it as it is more than 150 times slower than llListSort(), but it is a good demonstration of how a Merge Sort works.

I realize I shouldn't be using iteration in a recursive method... Sue me.

```lsl
list sort(list l) {
    if (llGetListLength(l) > 1) {
        integer mid = llGetListLength(l)/2;
        list l2 = sort(llList2List(l, 0, mid-1));
        list l3 = sort(llList2List(l, mid, -1));
        return merge(l2, l3);
    }
    return l;
}

list merge(list l, list r) {
    integer lm = llGetListLength(l);
    integer rm = llGetListLength(r);
    integer lc;
    integer rc;
    list ret;
    while (lc < lm || rc < rm) {
        if (lc >= lm) {
            ret += llList2Integer(r, rc);
            rc++;
        } else if (rc >= rm) {
            ret += llList2Integer(l, lc);
            lc++;
        } else {
            if (llList2Integer(l, lc) <= llList2Integer(r, rc)) {
                ret += llList2Integer(l, lc);
                if (lc < lm)
                    lc++;
            } else {
                ret += llList2Integer(r, rc);
                if (rc < rm)
                    rc++;
            }
        }
    }
    return ret;
}
```