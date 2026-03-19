---
name: "Sim Map Particle Projector"
category: "example"
type: "example"
language: "LSL"
description: "Subnova's Map API does not work any longer, so don't rely on this script!"
wiki_url: "https://wiki.secondlife.com/wiki/Sim_Map_Particle_Projector"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- Click Here  To see my page and more of my scripts

Warning!

Subnova's Map API does not work any longer, so don't rely on this script!



Fun little script. Drop it in a prim to see how it works. Demonstrates how to work with the map api.

```lsl
string URL = "http://www.subnova.com/secondlife/api/map.php?sim=";

key httpRequestId;

float mapSize = 3.0;

mapParticle(key mapTexture)
{
    llParticleSystem([PSYS_PART_FLAGS, 0,
                      PSYS_SRC_PATTERN, 4,
                      PSYS_PART_START_ALPHA, 0.5,
                      PSYS_PART_END_ALPHA, 0.5,
                      PSYS_PART_START_COLOR, <1.0, 1.0, 1.0>,
                      PSYS_PART_END_COLOR, <1.0, 1.0, 1.0>,
                      PSYS_PART_START_SCALE, ,
                      PSYS_PART_END_SCALE, ,
                      PSYS_PART_MAX_AGE, 1.2,
                      PSYS_SRC_MAX_AGE, 0.0,
                      PSYS_SRC_ACCEL, <0.0, 0.0, 0.0>,
                      PSYS_SRC_ANGLE_BEGIN, 0.0,
                      PSYS_SRC_ANGLE_END, 0.0,
                      PSYS_SRC_BURST_PART_COUNT, 8,
                      PSYS_SRC_BURST_RADIUS, mapSize,
                      PSYS_SRC_BURST_RATE, 0.1,
                      PSYS_SRC_BURST_SPEED_MIN, 0.0,
                      PSYS_SRC_BURST_SPEED_MAX, 0.0,
                      PSYS_SRC_OMEGA, <0.0, 0.0, 0.0>,
                      PSYS_SRC_TEXTURE, mapTexture]);
}

default
{
    on_rez(integer param)
    {
        llResetScript();
    }
    state_entry()
    {
        httpRequestId = llHTTPRequest(URL + llEscapeURL(llGetRegionName()), [], "");
    }
    http_response(key request_id, integer status, list metadata, string body)
    {
        if((request_id == httpRequestId) && (status == 200))
            mapParticle(body);
    }
}
```