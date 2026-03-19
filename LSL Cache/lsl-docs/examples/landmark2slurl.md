---
name: "landmark2slurl"
category: "example"
type: "example"
language: "LSL"
description: "Landmarks retrieved via LSL from an object's inventory will only have global coordinates in it (plus the landmark's inventory name, like all assets), which are retrieved through an (expensive) dataserver call. In order to create a SLURL from the landmark (as the viewer does with the Copy to SLURL option), first we need to figure out the region's position in the grid, then look up its name, and use the remainder as local coordinates."
wiki_url: "https://wiki.secondlife.com/wiki/Landmark2slurl"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Landmarks retrieved via LSL from an object's inventory will only have *global* coordinates in it (plus the landmark's inventory name, like all assets), which are retrieved through an (expensive) dataserver call. In order to create a SLURL from the landmark (as the viewer does with the **Copy to SLURL** option), first we need to figure out the region's position in the grid, then look up its name, and use the remainder as local coordinates.

Unfortunately, at the time of writing, there is no LSL function to retrieve the region's name, based on its grid coordinates. The only alternative given by us by Linden Lab is to use a (special) capabilities call instead, which can be used via llHTTPRequest. It was allegedly designed to inject some Javascript on the Map API but works well for our own purposes.

The script below shows how exactly to achieve this and do the calculations right (i.e., without any rounding errors).

```lsl
// Click to print SLURL for every landmark in inventory.
//     Uses llRequestInventoryData() to get coordinates
//     Uses http://wiki.secondlife.com/wiki/Linden_Lab_Official:Map_API_Reference#Region_name_from_global_coordinates to get region name
integer landmarkIndex;
vector  landmarkCoords;
string  landmarkRegion;
string  landmarkSlurl;
key inventoryRequestId;
key mapRequestId;

requestLandmarkInfo(integer inventoryIndex) {
    if (inventoryIndex >= llGetInventoryNumber(INVENTORY_LANDMARK)) return;
    landmarkIndex = inventoryIndex;
    string landmarkName = llGetInventoryName(INVENTORY_LANDMARK, landmarkIndex);
    inventoryRequestId = llRequestInventoryData(landmarkName);
}

default {
    touch_start(integer count) {
        requestLandmarkInfo(0);
    }

    dataserver(key requestId, string data) {
        if (requestId != inventoryRequestId) return;
        if ((vector)data == ZERO_VECTOR) return;
        // landmark request
        landmarkCoords = llGetRegionCorner() + (vector)data;
        // http://wiki.secondlife.com/wiki/Linden_Lab_Official:Map_API_Reference#Region_name_from_global_coordinates
        mapRequestId = llHTTPRequest(
            "https://cap.secondlife.com/cap/0/b713fe80-283b-4585-af4d-a3b7d9a32492?var=region"
            + "&grid_x=" + (string)((integer)landmarkCoords.x / 256)
            + "&grid_y=" + (string)((integer)landmarkCoords.y / 256), [], "");
    }

    http_response(key requestId, integer status, list metadata, string body) {
        if (requestId != mapRequestId) return;
        landmarkRegion = llList2String(llParseString2List(body, ["var region='", "';"], []), 0);
        landmarkSlurl = "http://maps.secondlife.com/secondlife/" + llEscapeURL(landmarkRegion) +
            "/" + (string)((integer)landmarkCoords.x % 256) +
            "/" + (string)((integer)landmarkCoords.y % 256) +
            "/" + (string)((integer)landmarkCoords.z);
        llOwnerSay(llGetInventoryName(INVENTORY_LANDMARK, landmarkIndex) + ": "
            + landmarkSlurl + " " + landmarkSlurl + "");
        requestLandmarkInfo(landmarkIndex + 1);
    }
}
```