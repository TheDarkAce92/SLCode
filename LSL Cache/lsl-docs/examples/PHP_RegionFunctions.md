---
name: "PHP_RegionFunctions"
category: "example"
type: "example"
language: "LSL"
description: "// $coords[0] = Global Grid X coordinate"
wiki_url: "https://wiki.secondlife.com/wiki/PHP_RegionFunctions"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

```lsl
// Three useful PHP functions by Gypsy Paz and Zayne Exonar

// $coords[0] = Global Grid X coordinate

// $coords[1] = Global Grid Y coordinate

function getSimName($coords)
{
    $split = explode('"', file_get_contents("http://slurl.com/get-region-name-by-coords?var=region&grid_x=".$coords[0]."&grid_y=".$coords[1]));
    return $split[1];
}

function getSimCoords($simName)
{
    $query = str_replace(" ", "", file_get_contents("http://slurl.com/get-region-coords-by-name?var=coords&sim_name=".urlencode($simName)));
    $coords = preg_split('/[a-zA-Z=",.:;}{]/', $query, -1, PREG_SPLIT_NO_EMPTY);
    return $coords;
}

function getSimImage($coords)
{
    return "http://map.secondlife.com/map-1-".$coords[0]."-".$coords[1]."-objects.jpg";
}
```