---
name: "HTML HUD Demo"
category: "example"
type: "example"
language: "LSL"
description: "Some of the links/HTML used in this very old script may require updating/adjusting; see also the Discussion page for some hints on what to change and where (notice posted on 2026-03-18)."
wiki_url: "https://wiki.secondlife.com/wiki/HTML_HUD_Demo"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Some of the links/HTML used in this very old script may require updating/adjusting; see also the Discussion page for some hints on what to change and where (notice posted on 2026-03-18).

- 1 TODO:
- 2 HTML HUD Demo:

  - 2.1 Screenshot:
  - 2.2 Tip:
  - 2.3 Source code:

TODO:

- Suggest a `Stop All Animations` button be added to Animations selection frame for convenience.

HTML HUD Demo:

## Screenshot:

screenshots

## Tip:



      **Tip:** This HUD might take a second or two to load when switching from 'closed' to 'open' mode.


## Source code:

```lsl
//  HTML-based, single script HUD
//
//  original by Kelly Linden
//
//  To use:
//  - create a default prim (cube)
//  - wear it as a HUD on top_left (script needs tweaking for other attachment points)
//  - edit the cube while wearing
//  - add animations you want to use
//  - add notecards and objects you want to hand out
//  - add this script
//
//  License:
//    This script itself is free to share, modify and use without restriction.
//    Any linked or referenced files are not included in this license and are
//    licensed by their respective owners under their own respective copyright
//    and other licenses.

key     owner;
string  ownerName;

integer scope;

string  url;

key     currentRequestID;

integer responseStatus;
string  responseBody;

list    lastPath;

string  video_url;

string  header;
string  footer;

string  currentAnimation;

integer isVisible;

string  exceptions;

//  user-function: init
//  - does not return anything
//  - sets initial variable values
//  - sets object's name and textures
//  - request a url to use the HUD

init()
{
    owner     = llGetOwner();
    ownerName = llKey2Name(owner);
    llSetObjectName("HTML HUD");

    scope = AGENT_LIST_PARCEL;

    video_url = "http://www.youtube.com/embed/m7p9IEpPu-c?rel=0";

//  header set in set_link_media(url)
//  footer set in set_link_media(url)

    float   FLOAT_FALSE      = 0.0;
    vector  RATIO_ONE_BY_ONE = <0.98, 0.98, 0.00>;//  fix Second Life ... or try to!

    llSetLinkPrimitiveParamsFast(LINK_THIS, [
        PRIM_TEXTURE, ALL_SIDES, TEXTURE_BLANK,                          RATIO_ONE_BY_ONE, ZERO_VECTOR, FLOAT_FALSE,
        PRIM_TEXTURE, 2,         "0b815b79-c8f5-fc98-91fc-e77b53a468e2", RATIO_ONE_BY_ONE, ZERO_VECTOR, FLOAT_FALSE]);

    toggle_visibility_of_HUD_button();
    request_secure_url();
}

//  user-function: toggle_visibility_of_HUD_button
//  - does not return anything
//  - toggle the visibility of the prim
//  - will rotate, position and scale the prim

toggle_visibility_of_HUD_button()
{
    if (isVisible)
    {
        llSetLinkPrimitiveParamsFast(LINK_THIS, [
            PRIM_POS_LOCAL, <0.0, -0.13, -0.13>,
            PRIM_ROT_LOCAL, <0.0, 0.0, 0.0, 1.0>,
            PRIM_SIZE, <0.01, 0.25, 0.25>]);
    }
    else
    {
        llSetLinkPrimitiveParamsFast(LINK_THIS, [
            PRIM_POS_LOCAL, <0.0, -0.04, -0.04>,
            PRIM_ROT_LOCAL, <0.0, 0.0, -1.0, 0.0>,
            PRIM_SIZE, <0.05, 0.05, 0.05>]);
    }

    isVisible = !isVisible;
}

//  user-function: drop and clear the old url
//  - does not return anything

release_url()
{
    llReleaseURL(url);
    url = "";
}

//  user-function: request secure url
//  - does not return anything
//  - make sure we release the old url before requesting a new one

request_secure_url()
{
    release_url();
    currentRequestID = llRequestSecureURL();
}

//  user-function: set_link_media
//  - does not return anything
//  - set the values for the string variables 'header' and 'footer'
//  - prepare face 4 for media on a prim

set_link_media(string scriptUrl)
{
    url = scriptUrl;

    header = ""
        + ""; footer = "" + "Scan | Anims | " + "Video | Config | Hide" + ""; llSetLinkMedia(LINK_THIS, 4, [ PRIM_MEDIA_AUTO_PLAY, TRUE, PRIM_MEDIA_CURRENT_URL, url, PRIM_MEDIA_HOME_URL, url, PRIM_MEDIA_HEIGHT_PIXELS, 256, PRIM_MEDIA_WIDTH_PIXELS, 256, PRIM_MEDIA_PERMS_CONTROL, PRIM_MEDIA_PERM_NONE]); } // user-function: // - does not return anything // - used if there's not a request to the homepage of our website // - check where on the site we are and prepare variables for the response http_get(key requestID, list path) { currentRequestID = requestID; integer numOfPathsParts = llGetListLength(path); string firstPathPart = llList2String(path, 0); if (firstPathPart == "hide") { toggle_visibility_of_HUD_button(); http_get(requestID, lastPath); return; } lastPath = path; if (firstPathPart == "agent") { if (numOfPathsParts == 1) { prepare_profile_overview_page(requestID, owner); return; } else if (numOfPathsParts == 2) { key id = (key)llList2String(path, 1); prepare_profile_overview_page(requestID, id); return; } else if (numOfPathsParts == 4) { if (llList2String(path, 2) != "give") { return; } key id = (key)llList2String(path, 1); string name = llKey2Name(id); string itemName = llUnescapeURL(llList2String(path, 3)); llOwnerSay("Giving '" + itemName + "' to '" + name + "'."); llGiveInventory(id, itemName); prepare_profile_overview_page(requestID, id); return; } } else if (firstPathPart == "anims") { if (numOfPathsParts == 1) { anims_page(); return; } else if (numOfPathsParts == 2) { play_anim(llList2String(path, 1)); anims_page(); return; } } else if (firstPathPart == "video") { responseStatus = 200; responseBody = header + "" + footer; return; } else if (firstPathPart == "config") { if (numOfPathsParts == 1) { config_page(); return; } else if (llList2String(path, 1) == "set") { string queryString = llGetHTTPHeader(requestID, "x-query-string"); list args = llParseString2List(queryString, ["="], ["&"]); integer index = -llGetListLength(args); while (index) { string variable = llList2String(args, index); string value = llUnescapeURL(llList2String(args, index + 1)); if (variable == "video") { video_url = value; } // because: var, val, &, var, val, &, ... index += 3; } config_page(); } } responseStatus = 404; responseBody = header + "404 Page Not Found." + footer; throw_exception("There has been a HTTP-request to a non-existant page on " + "your HUD's website. Please check the path of the request " + "for mistakes."); } // user-function: prepare_profile_overview_page // - does not return anything // - prepares a response for a page with information about a certain avatar // - includes profile thumbnail, name, script info, give menu prepare_profile_overview_page(key requestID, key id) { list avatarDetails = llGetObjectDetails(id, [ OBJECT_POS, OBJECT_TOTAL_SCRIPT_COUNT, OBJECT_SCRIPT_MEMORY, OBJECT_SCRIPT_TIME]); responseStatus = 200; responseBody = header + "" + "" + html_body_with_formatted_avatar_name(id) + " ## " + llGetUsername(id) + " " + "" + html_body_with_links_for_interaction_with_certain_avatar(id) + "" + html_body_with_inventory_overview_for_give_menu(id) + "" + html_body_avatar_profile_pic_thumbnail(id) + " - Scripts: - " + (string)llList2Integer(avatarDetails, 1) + " total - " + bytes2str(llList2Integer(avatarDetails, 2)) + " - " + (string)((integer)(llList2Float(avatarDetails, 3) * 1000000.0)) + "us " + footer; } // user-function: html_body_with_formatted_avatar_name // - returns the name of the avatar in html format // - removes the lastname if it is Resident // - adds a line-break for long names string html_body_with_formatted_avatar_name(key id) { string stringToReturn = llKey2Name(id); if (llGetSubString(stringToReturn, -9, -1) == " Resident") { stringToReturn = llDeleteSubString(stringToReturn, -9, -1); } if (15 " ); } return stringToReturn; } // user-function: html_body_with_links_for_interaction_with_certain_avatar // - returns html text with links for an avatar to interact with who has a certain uuid string html_body_with_links_for_interaction_with_certain_avatar(key id) { return "Options" + " - IM" + " - Offer Teleport - Map - Share - Pay" + " "; } // user-function: html_body_with_inventory_overview_for_give_menu // - returns html text with inventory item lists string html_body_with_inventory_overview_for_give_menu(key id) { string stringToReturn = "Give - (no objects or notecards found) "; return stringToReturn; } // user-function: bytes2str // - returns a string with script memory info in readable format string bytes2str(integer bytes) { // 1024² = 1048576 if (bytes "; } // user-function: inventory_list_in_html_format_for_give_menu // - returns html text with inventory item list of given type string inventory_list_in_html_format_for_give_menu(key id, integer type) { string stringToReturn; integer index = llGetInventoryNumber(type); while (index) { --index; string name = llGetInventoryName(type, index); stringToReturn += "" + name + ""; } return stringToReturn; } // user-function: anims_page // - does not return anything // - prepares an html text overview page of animations anims_page() { responseStatus = 200; responseBody = header + "Animations ## Choose an animation: " + "" + html_body_animations_overview() + "" + footer; } // user-function: html_body_animations_overview // - returns html text with a list of included animations string html_body_animations_overview() { string stringToReturn = "" + "Animate
- (no animations found)
- " + name + "
";

    return stringToReturn;
}

//  user-function: play_anim
//  - does not return anything
//  - prompts a perms request to animate owner

play_anim(string anim)
{
    llRequestPermissions(owner, PERMISSION_TRIGGER_ANIMATION);
    currentAnimation = llUnescapeURL(anim);
}

//  user-function: config_page
//  - does not return anything
//  - prepares page to configure youtube video link

config_page()
{
    responseStatus = 200;
    responseBody = header + "Options:Video URL: "
                 + footer;
}

//  user-function: throw_exception
//  - does not return anything
//  - logs errors into cache for later viewing and debugging

throw_exception(string inputString)
{
    if (exceptions == "")
    {
        exceptions = "The following un-handled exception(s) occurred that are "
                   + "preventing this device's operation:\n";
    }

    exceptions += "\t"+inputString+"\n";
}

default
{
    on_rez(integer start_param)
    {
        release_url();
        llResetScript();
    }

    changed(integer change)
    {
        if (change & (CHANGED_OWNER | CHANGED_INVENTORY))
        {
            release_url();
            llResetScript();
        }

        if (change & (CHANGED_REGION | CHANGED_REGION_START | CHANGED_TELEPORT))
        {
            request_secure_url();
        }
    }

    state_entry()
    {
        init();
    }

    touch_start(integer num_detected)
    {
        toggle_visibility_of_HUD_button();
    }

    http_request(key id, string method, string body)
    {
        responseStatus = 400;
        responseBody   = "Unsupported method";

        if (method == URL_REQUEST_GRANTED)
        {
            responseStatus = 200;
            responseBody   = "OK";

            set_link_media(body);
        }
        else if (method == URL_REQUEST_DENIED)
        {
            responseBody   = "Bad request";

            throw_exception("The following error occurred while attempting to "
                            + "get a free URL for this device:\n \n" + body);
        }
        else if (method == "GET")
        {
            responseStatus = 200;
            responseBody   = "GET";

            string pathInfoHeader = llGetHTTPHeader(id, "x-path-info");
            list path             = llParseString2List(pathInfoHeader, ["/"], []);

            if (path == [])
            {
                currentRequestID = id;

                list    agents = llGetAgentList(scope, []);
                integer index  = llGetListLength(agents);

                if (!index)
                {
                    responseBody   = header + "

## Scan Results:

- No one "
                                   + "near by.
- Owner: " + ownerName + "
" + footer;
                }
                else
                {
                    responseBody   = header + "

## Scan Results:

- "
                                     + html_body_with_formatted_avatar_name(agent) + "
" + footer;
                }

                lastPath = [];
            }
            else
            {
                http_get(id, path);
            }
        }

        llSetContentType(id, CONTENT_TYPE_HTML);
        llHTTPResponse(id, responseStatus, responseBody);

        if (exceptions != "")
        {
            state error;
        }
    }

    run_time_permissions(integer perm)
    {
        if (perm & PERMISSION_TRIGGER_ANIMATION)
        {
            llStartAnimation(currentAnimation);
        }
        else
        {
            throw_exception("This HUD has tried to animate your avatar WITHOUT "
                            + "having the permissions to do so. You must grant this HUD "
                            + "permissions to animate your avatar for this feature to work.");
        }

        if (exceptions != "")
        {
            state error;
        }
    }

    state_exit()
    {
        release_url();
    }
}

state error
{
    on_rez(integer start_param)
    {
        llResetScript();
    }

    changed(integer change)
    {
        if (change & (CHANGED_OWNER | CHANGED_INVENTORY))
        {
            llResetScript();
        }
    }

    state_entry()
    {
        llOwnerSay("========== ERROR REPORT START ==========");
        llOwnerSay(exceptions);
        llOwnerSay("========== ERROR REPORT END ==========");
        llOwnerSay("Resetting now...");
        llResetScript();
    }
}
```

Go to top!