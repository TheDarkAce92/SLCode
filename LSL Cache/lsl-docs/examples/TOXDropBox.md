---
name: "TOXDropBox"
category: "example"
type: "example"
language: "LSL"
description: "//CONFIG // string templatename=\"\"; // give a template? leave blank for no"
wiki_url: "https://wiki.secondlife.com/wiki/TOXDropBox"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL

```lsl
//:TOX: DropBox
//Script Name: :TOX: Dropbox.lsl
//By: Dimentox Travanti
//
// This is a Drop box which allows people to drop in items it can have a required prefix on the items
//      And has the abilility to hand out a template / instructions
//      Also you can set the color and if it notifies you.
//

//CONFIG //
string templatename=""; // give a template? leave blank for no

integer allowed = INVENTORY_NOTECARD; /// the type of item allowed

string rname = "dcs"; //name to be allowed it will check for the item must be named this to start

string inst ="INSTRUCTIONS HERE"; // instructions that are given. blank for no instructions

integer showhover = 1; //Show hover text

string title = ""; //leave blank to display the objects name;

vector color = <1,1,1>; //hover color

float alpha = 1.0; // the brightness of the hover 1.0 is full 0.0 is not visable

integer showtotal = 0; //1 for yes 0 for no

integer protect = 1; //Protect against other scripts runing when droped in?

integer notify = 0; // Notify of new additions.

///////////////NOTHING UNDER HERE SHOULD NEED TO BE CHANGED!///////////

//Needed vars//
list items;
integer ctotal=0;
list ids;
list types = [INVENTORY_TEXTURE, INVENTORY_SOUND, INVENTORY_LANDMARK,
    INVENTORY_CLOTHING, INVENTORY_OBJECT, INVENTORY_SCRIPT,INVENTORY_NOTECARD,
    INVENTORY_BODYPART, INVENTORY_ANIMATION, INVENTORY_GESTURE];

//functions
set()
{
    if (showhover == 1)
    {
    string temp = title + "\n";
    if (templatename != "")
    {
           temp  += "Touch for Template\n";
    }
    if (inst != "")
    {
        temp += "Touch for Instructions\n";
    }
    if (showtotal == 1)
    {
        temp +="Total: "+(string)ctotal;
    }
 llSetText(temp, color, alpha);
    }
}
string genslurl()
{
        string sim = llEscapeURL(llGetRegionName());
        vector pos = llGetPos();
        integer x = (integer)pos.x;
        integer y = (integer)pos.y;
        integer z = (integer)pos.z;

        return "http:///slurl.com/secondlife/"+sim+"/"+(string)x+"/"+(string)y+"/"+(string)z+"/";

}
sprotect()
{
    integer num = llGetInventoryNumber(INVENTORY_SCRIPT);
    integer x;
    for (x = 0; x< num; x++)
    {
        string name = llGetInventoryName(INVENTORY_SCRIPT, x);
        if (name != llGetScriptName())
        {
            llSetScriptState(name, FALSE);
        }
    }
}
integer remove()
{

    //textures
    integer removed = 0;
    integer tcount = llGetListLength(types);
    integer x = 0;
    while (x < tcount)
    {
        integer type = llList2Integer(types, x);
       // llOwnerSay((string)type);
        if (type != allowed) // make sure its not an allowed thing.
        {
            integer num =  llGetInventoryNumber(type);
            integer z = 0;
            while (z < num)
            {
                string name = llGetInventoryName(type, z);
              //  llOwnerSay(name);
                if (name == llGetScriptName() || name == templatename)
                {
                    //do nothing
                } else {


                        llSay(0, "I am sorry this type of item is not allowed to be given in this box. \n"+inst);
                    llRemoveInventory(llGetInventoryName(type, z));
                    removed = 1;
                }
                z++;

            }

        }
        x++;

    }
    return removed;
}
default
{
    state_entry()
    {
        llSay(0, genslurl());
        sprotect();
        if (title == "")
        {
         title = llGetObjectName();
        }
        integer tot = llGetInventoryNumber(allowed);
        ctotal = llGetInventoryNumber(allowed);
        integer i = 0;
        for(i;i < tot;++i)
        {
            string name = llGetInventoryName(allowed,i);
            key id = llGetInventoryKey(name);
            integer index = llListFindList((list)name,items);
            if(index = -1 )
            {
                items += name;
                ids += id;
                llOwnerSay("Added named: " + name);
            }
        }
        set();
    }
     touch_start(integer total_number)
    {
        if (templatename != "")
        {
        llGiveInventory(llDetectedKey(0), templatename);
        }
        if (inst != "")
        {
        llSay(0, inst);
        }
    }
    changed(integer change)
    {
        if(change & CHANGED_INVENTORY)
        {
            sprotect();
            llSay(0, "Please Wait Proccessing your submission");
            if (llGetInventoryNumber(allowed) != ctotal)
            {
                integer tot = llGetInventoryNumber(allowed);
                integer i = 0;
                for(i;i < tot;++i)
                {
                    string name = llGetInventoryName(allowed,i);

                    key id = llGetInventoryKey(name);
                    integer index = llListFindList(items,(list)name);
                    if(index == -1)
                    {
                        if (name != templatename || name != llGetScriptName())
                        {
                        integer rlen = llStringLength(rname) - 1;
                        if (llToLower(llGetSubString(name, 0, rlen)) != llToLower(rname))
                        {
                            llSay(0, "This item is not named properly and will be removed\n" + inst);
                            llRemoveInventory(name);

                        } else {
                                items += name;
                            ids += id;
                            llSay(0, "Thanks for the submission of " + name);
                            if (notify == 1)
                            {

                                string msg = "You have a new item named " + name + " waiting for you!\nLocation: "+ genslurl();
    llInstantMessage(llGetOwner(), msg);
                            }
                        }
                        }
                    }

                }

            }else {
                    remove();
            }
            set();

        }

    }

}
```