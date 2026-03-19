---
name: "Materialization Effects 2"
category: "example"
type: "example"
language: "LSL"
description: "float alpha_increment = 0.01;"
wiki_url: "https://wiki.secondlife.com/wiki/Materialization_Effects_2"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

```lsl
integer links = LINK_SET;

float alpha_increment = 0.01;

nrFadeAlpha(float start_point, float end_point, float speed)
{
    start_point = nrFloatCheck(start_point);
    end_point = nrFloatCheck(end_point);
    speed = nrFloatCheck(speed);
    if(start_point!=end_point)
    {
        if(start_pointend_point);
        }
    }
}

float nrFloatCheck(float src)
{
    if(src<=0)
    {
        return 0.0;
    }
    else if(src>=1)
    {
        return 1.0;
    }
    return src;
}

nrSetGlow(integer link_num, float glow, integer sides)
{
    llSetLinkPrimitiveParamsFast(link_num, [PRIM_GLOW,sides,glow]);
}

default
{
    on_rez(integer a)
    {
        nrSetGlow(LINK_SET, 0.1, ALL_SIDES);
        nrFadeAlpha(0, 1.0, alpha_increment);
        nrSetGlow(LINK_SET, 0.0, ALL_SIDES);
    }
    touch_start(integer num)
    {
        if(llGetAlpha(ALL_SIDES)>0.5)
        {
            nrSetGlow(LINK_SET, 0.1, ALL_SIDES);
            nrFadeAlpha(1.0, 0.0, alpha_increment);
            nrSetGlow(LINK_SET, 0.0, ALL_SIDES);
        }
        else
        {
            nrSetGlow(LINK_SET, 0.1, ALL_SIDES);
            nrFadeAlpha(0.0, 1.0, alpha_increment);
            nrSetGlow(LINK_SET, 0.0, ALL_SIDES);
        }
    }
}
```