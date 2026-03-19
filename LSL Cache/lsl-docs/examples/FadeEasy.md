---
name: "FadeEasy"
category: "example"
type: "example"
language: "LSL"
description: "FadeEasy makes object fading easier for you to make an object fade in or out simply by entering a one-line code. Example: llFade(LINK_SET, 0.0, 1.0, ALL_SIDES, 0.05); Or llFade(LINK_SET, 1.0, 0.0, ALL_SIDES, 0.05);"
wiki_url: "https://wiki.secondlife.com/wiki/FadeEasy"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

**FadeEasy**

- 1 Introduction
- 2 Usage
- 3 Function Code
- 4 Entire Example Code

## Introduction

FadeEasy makes object fading easier for you to make an object fade in or out simply by entering a one-line code.**Example:** `llFade(LINK_SET, 0.0, 1.0, ALL_SIDES, 0.05);` Or `llFade(LINK_SET, 1.0, 0.0, ALL_SIDES, 0.05);`



## Usage

Function: `llFade(integer linknumber, float AlphaStart, float AlphaEnd, integer faces, float speed);`

`integer linknumber` – Link number (0: unlinked, 1: root prim, >1: child prims) or a `LINK_*` flag

`float AlphaStart` – from 0.0 (clear) to 1.0 (solid), This is the starting opacity of your object

`float AlphaEnd` – from 0.0 (clear) to 1.0 (solid), This is the ending opacity of your object

`integer faces` - LINK_THIS, LINK_ROOT, LINK_SET, LINK_ALL_OTHERS, LINK_ALL_CHILDREN

`float speed` - How much opacity to gain or decrease by

## Function Code

```lsl
// Leave this part alone!
llFade(integer linknumber, float AlphaStart, float AlphaEnd, integer faces, float speed)
{
    if(AlphaStartAlphaEnd)
    {
        for(;AlphaStart>AlphaEnd;)
        {
            AlphaStart-=speed;
            llSetLinkAlpha(linknumber, AlphaStart, faces);
        }
        return;
    }
}
```

## Entire Example Code

```lsl
// Leave this part alone!
llFade(integer linknumber, float AlphaStart, float AlphaEnd, integer faces, float speed)
{
    if(AlphaStartAlphaEnd)
    {
        for(;AlphaStart>AlphaEnd;)
        {
            AlphaStart-=speed;
            llSetLinkAlpha(linknumber, AlphaStart, faces);
        }
        return;
    }
}

// Global Integer Varibles
integer faded;

//====
default
{
    on_rez(integer params)
    {
        llFade(LINK_SET, 0.0,1.0,ALL_SIDES,0.05);
        faded = TRUE;
    }
    touch_end(integer num_detected)
    {
        if(faded == TRUE)
        {
            faded = FALSE;
            llFade(LINK_SET, 1.0,0.0, ALL_SIDES, 0.05);
        }
    }
}
```