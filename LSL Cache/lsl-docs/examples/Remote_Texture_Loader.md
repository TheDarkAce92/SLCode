---
name: "Remote Texture Loader"
category: "example"
type: "example"
language: "LSL"
description: "Remote Texture Loader Description"
source_url: "https://github.com/Outworldz/LSL-Scripts/blob/master/Remote_Texture_Loader/Remote_Texture_Loader/Object/Remote_Texture_Loader_1.lsl"
source_name: "Outworldz LSL Scripts (GitHub) / Remote_Texture_Loader"
source_owner: "Outworldz"
source_repo: "LSL-Scripts"
source_branch: "master"
source_path: "Remote_Texture_Loader/Remote_Texture_Loader/Object/Remote_Texture_Loader_1.lsl"
source_project: "Remote_Texture_Loader"
source_part_total: "5"
first_fetched: "2026-03-18"
last_updated: "2026-03-19"
has_versions: "true"
active_version: "scraped-outworldz-lsl-scripts-github-remote-texture-loader-2026-03-19"
---

```lsl
// === Part 1/5 ===
// :CATEGORY:Texture
// :NAME:Remote_Texture_Loader
// :AUTHOR:Bobbyb30 Swashbuckler
// :CREATED:2010-12-27 12:20:34.060
// :EDITED:2013-09-18 15:39:01
// :ID:691
// :NUM:941
// :REV:1.0
// :WORLD:Second Life
// :DESCRIPTION:
// Remote Texture Loader Description
// 
// These set of scripts allow for a prim to act as a server and load textures onto unlinked prims. The main benefit is that the recieving prims have *no* scripts. This means that the server, which consists of three scripts can load onto 30 prims without needing 20 scripts. Please note there is a 3 second delay for each remote load.
// 
// It's main use would be for billboards, although it could substitute some texture changers.
// 
// 
// They are hereby released into public domain.
// Disclaimer
// 
// These programs are distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
// Directions
// 
// Get the keys of the textures you want to use. Put them into both Remote Load Texture Display(input list).lsl and Main Display.lsl. Now decide on what number you want to use as your pin(you can leave the default of 606 if you choose). Set up the prims you want to use as billboards. Select which billboard you want to use as a server. Get the keys and set the pins for all the billboards except the server using Get key & set pin.lsl. Copy these keys into Remote Loader.lsl. Add Remote Loader.lsl to the server. Add Load Texture Display(input list).lsl to the server. Check Main Display.lsl parameters to make sure they are what you want and add that to the server. Enjoy=D.
// 
// Scripts
// 
// There are 3 scripts that go in the server:
// 
//     * Remote Loader.lsl which remotely loads the 'Remote Load Texture Display(input list).lsl' script.
//     * Remote Load Texture Display(input list).lsl which is remotely loaded and display the texture before deleting itself.
//     * Main Display.lsl which tells the remote loader when to load, and is the only active script most of the time. 
// 
// Two other scripts are:
// 
//     * Print inventory texture keys.lsl which prints the keys of inventory textures
//     * Get key & set pin.lsl which sets the remote load pin on prims and tells the owner the prim key. 
// :CODE:
//***********************************************************************************************************

//                                                                                                          *

//                                            --Remote Loader--                                             *

//                                                                                                          *

//***********************************************************************************************************

// www.lsleditor.org  by Alphons van der Heijden (SL: Alphons Jano)

//Creator: Bobbyb30 Swashbuckler

//Attribution: None required, but it is appreciated.

//Created: November 28, 2009

//Last Modified: November 28, 2009

//Released: Saturday, November 28, 2009

//License: Public Domain

 

//Status: Fully Working/Production Ready

//Version: 1.0.1

 

//Name: Remote Loader.lsl

//Purpose: To remotely load the 'Remote Load Texture Display(input list).lsl' script.

//Technical Overview: This script remotely loads Remote Load Texture Display(input list).lsl into the proper objects.

//Directions: Add object UUID's to targets list. Correct the pin to the one you set.

 

//Compatible: Mono & LSL compatible

//Other items required: Requires the 'Remote Load Texture Display(input list).lsl' & 'Main Display.lsl' scripts.

//Notes: Commented for easier following. This script will shut off after use. Do not rename script. There is a

//       3 second delay between remote loads.

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

 

///////////////////////////////////////////

//user variables...you may change these...

integer pin = 606;//pin

 

//takes 3 seconds per each target

list targets =[//put object UUIDS here

    "ad367823-4e38-fcee-fdeb-f41fdb045149",

    "dac99b54-d23a-e890-2cb9-d57b1f80c6d6"

        ];

 

///////////////

//global variables...do not change

integer targetslistlength;//length of targets list

 

default

{

    state_entry()

    {

        llOwnerSay("'Remote Loader.lsl' (Public Domain 2009)");

        targetslistlength = llGetListLength(targets);//speed hack here

        llSetScriptState(llGetScriptName(),FALSE);//turn off until needed

    }

    link_message(integer sender, integer ch, string msg, key id)

    {

        if(ch == -1)//begin remote loading

        {

            //msg is texture number to load, its bumped up one so that 0 is 1...

            integer counter;

            do

            {

                integer param = ((integer)msg) + 1;

                llRemoteLoadScriptPin(llList2String(targets,counter),"Remote Load Texture Display(input list).lsl",pin, TRUE,param);

            }while(++counter < targetslistlength);

            llSetScriptState(llGetScriptName(),FALSE);//turn off until next time...

        }

    }

}

// === Part 2/5 ===
// :CATEGORY:Texture
// :NAME:Remote_Texture_Loader
// :AUTHOR:Bobbyb30 Swashbuckler
// :CREATED:2010-12-27 12:20:34.060
// :EDITED:2013-09-18 15:39:01
// :ID:691
// :NUM:942
// :REV:1.0
// :WORLD:Second Life
// :DESCRIPTION:
// Remote Load Texture Display(input list).lsl
// :CODE:
//***********************************************************************************************************

//                                                                                                          *

//                            --Remote Load Texture Display(input list)--                                   *

//                                                                                                          *

//***********************************************************************************************************

// www.lsleditor.org  by Alphons van der Heijden (SL: Alphons Jano)

//Creator: Bobbyb30 Swashbuckler

//Attribution: None required, but it is appreciated.

//Created: November 28, 2009

//Last Modified: November 28, 2009

//Released: Saturday, November 28, 2009

//License: Public Domain

 

//Status: Fully Working/Production Ready

//Version: 1.0.1

 

//Name: Remote Load Texture Display(input list).lsl

//Purpose: To be remotely loaded onto a prim and then display the appropriate texture.

//Technical Overview: When this script is remotely loaded to an object, it changes that objects texture and then

//                    deletes itself.

//Directions: Add the appropriate textures to the list. Place the script in the server.

 

//Compatible: Mono & LSL compatible

//Other items required: Requires the 'Remote Loader.lsl' & 'Main Display.lsl' scripts.

//Notes: Commented for easier following. This script will delete itself after use. Do not rename script.

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

 

//Adjustable global variables...you may change these

//texture list...this list should have 2 or more textures

list textures = [//put your texture UUIDs/keys in here

    "f150313b-1f38-8978-b2ed-e0b2ffb62d5c",// black

    "16e92b19-7407-44c6-1f7a-03d75ef3e4a6",// unabletoconnect

    "1c482bda-802d-2991-5a03-4bb128792326"// white

        ];//end of list

 

integer side = ALL_SIDES;//which side(face) to change

// put # of side, or put ALL_SIDES for all sides,-1 equals all sides

 

default

{

    state_entry()

    {

        integer param = llGetStartParameter();;

        if(param != 0)

        {

            --param;//param - 1

            llSetTexture(llList2String(textures,param),side);//set the texture

            llRemoveInventory(llGetScriptName());//remove script from inventory

            llSleep(1.0);

            llRemoveInventory(llGetScriptName());//remove script from inventory

            //if that fails we'll get here

            llInstantMessage(llGetOwner(),"The script '" + (string)llGetScriptName() + "' in object " + llGetObjectName()

                + "at Region " + (string)llGetRegionName() + " loc: " + (string)llGetPos() + " failed to delete.");

            llSetScriptState(llGetScriptName(),FALSE);//shut off script

        }

        else

        {

            llOwnerSay("Bobbyb's 'Remote Load Texture Display(input list).lsl' running (Public Domain 2009)");

            llOwnerSay("This script should be deleted if it is in a remote object...");

            llSetScriptState(llGetScriptName(),FALSE);//shut off

        }

    }

}

// === Part 3/5 ===
// :CATEGORY:Texture
// :NAME:Remote_Texture_Loader
// :AUTHOR:Bobbyb30 Swashbuckler
// :CREATED:2010-12-27 12:20:34.060
// :EDITED:2013-09-18 15:39:01
// :ID:691
// :NUM:943
// :REV:1.0
// :WORLD:Second Life
// :DESCRIPTION:
// Main Display.lsl
// :CODE:
//***********************************************************************************************************

//                                                                                                          *

//                                                    --Main Display --                                     *

//                                                                                                          *

//***********************************************************************************************************

// www.lsleditor.org  by Alphons van der Heijden (SL: Alphons Jano)

//Creator: Bobbyb30 Swashbuckler

//Attribution: None required, but it is appreciated.

//Created: November 28, 2009

//Last Modified: November 28, 2009

//Released: Saturday, November 28, 2009

//License: Public Domain

 

//Status: Fully Working/Production Ready

//Version: 1.0.1

 

//Name: Main Display.lsl

//Purpose: This is the heart of the server. It tells remote loader when to load and changes the pictures on the server.

//Technical Overview:  Tell remote loader when to load using a timer. Also displays texture on server.

//Description: The main display serves as the core of the server telling remote loader when to load and changin the

//             texture on the server.

//Directions: Create a prim. Place the script in prim inventory. Modify the script parameters to suit your needs and

//            save. Copy the textures from here to the 'Remote Load Texture Display(input list).lsl' script.

 

//Compatible: Mono & LSL compatible

//Other items required: Requires the 'Remote Loader.lsl' & 'Remote Load Texture Display(input list).lsl' scripts.

//Notes: Uses a timer event. Should be low lag. Commented for easier following.

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

 

//Adjustable global variables...you may change these

//texture list...this list should have 2 or more textures

list textures = [//put your texture UUIDs/keys in here

    "f150313b-1f38-8978-b2ed-e0b2ffb62d5c",// black

    "16e92b19-7407-44c6-1f7a-03d75ef3e4a6",// unabletoconnect

    "1c482bda-802d-2991-5a03-4bb128792326"// white

        ];//end of list

 

//Please note there is a .2 second delay between prims.

integer side = ALL_SIDES;//which side to change , put #, or put ALL_SIDES for all sides,-1 equals all sides

float frequency = 100.0;//how often to change the texture in seconds. Shouldn't be below 20.0

//This script is meant for longer periods of time such as 1 or 2 minutes for savings to be viable

 

//please note that the last and first texture will be shown less frequently than those in between

integer random = TRUE;//whether to show the textures randomly, or in order

integer duplicatecheck = TRUE;//if random is true, this will check to make sure the random selection is a new texture

 

 

/////////////////////////////////////////////////////////////

//global variables...do not change

integer numberoftextures;//number of textures in inventory

integer currenttexture;//inventory number of current texture

 

changetexture()//user fucntion to change texture

{

    llSetScriptState("Remote Loader.lsl",TRUE);//turn on remote loader

    llMessageLinked(LINK_THIS,-1,(string)currenttexture,"");//tell remote loader which texture to load

    llSetTexture(llList2String(textures,currenttexture),side);//set texture using key

}

 

default

{

    on_rez(integer start_param)//on rez reset...probably not needed.

    {

        llResetScript();

    }

    state_entry()

    {

        llOwnerSay("Bobbyb's 'Main Display.lsl' (Public Domain 2009)");

        llOwnerSay("Because knowledge should be free.");

        numberoftextures = llGetListLength(textures);//speed hack here

        //assume correct

        llOwnerSay("There are " + (string)numberoftextures + " pictures which I will change every "

            + (string)frequency + " seconds on side: " + (string)side);

        llOwnerSay("My current free memory is : " + (string)llGetFreeMemory()

            + " bytes. If it is below 2500 bytes, I may not work properly.");

        llSetTimerEvent(frequency);

    }

    timer()

    {

        if(random)//show pics randomly

        {

            integer randomtexture;

            if(duplicatecheck)//whether to make sure random doesn't repeat itself

            {

                do

                {

                    randomtexture= llRound(llFrand(numberoftextures - 1));

                    //llOwnerSay("r" + (string)randomtexture);//debug

                }while(randomtexture == currenttexture);//make sure the random one isn't the same as the current one

            }

            else//no duplicate check

                randomtexture = llRound(llFrand(numberoftextures - 1));//generate random texture number

            currenttexture = randomtexture;//set the current one to the random one selected

            changetexture();//change the texture

            //llOwnerSay("c" + (string)currenttexture);//debug

        }

        else//not random, go in order

        {

            ++currenttexture;

            if(currenttexture == numberoftextures)//if current texture = number of textures, reset counter

                currenttexture = 0;

            changetexture();//change the texture

            //llOwnerSay("c" + (string)currenttexture);//debug

        }

    }

}

// === Part 4/5 ===
// :CATEGORY:Texture
// :NAME:Remote_Texture_Loader
// :AUTHOR:Bobbyb30 Swashbuckler
// :CREATED:2010-12-27 12:20:34.060
// :EDITED:2013-09-18 15:39:01
// :ID:691
// :NUM:944
// :REV:1.0
// :WORLD:Second Life
// :DESCRIPTION:
// Get key & set pin.lsl 
// :CODE:
//***********************************************************************************************************

//                                                                                                          *

//                                                    -- Get key & set pin --                               *

//                                                                                                          *

//***********************************************************************************************************

// www.lsleditor.org  by Alphons van der Heijden (SL: Alphons Jano)

//Creator: Bobbyb30 Swashbuckler

//Attribution: None required, but it is appreciated.

//Created: November 28, 2009

//Last Modified: November 28, 2009

//Released: Saturday, November 28, 2009

//License: Public Domain

 

//Status: Fully Working/Production Ready

//Version: 1.0.1

 

//Name: Get key & set pin.lsl

//Purpose: To set the pin and print out the UUID of the object.

//Description: Gets the key of the object and sets the object remote load pin.

//Directions: Modify pin to match the one used in remote loader and then drop into prim.

 

//Compatible: Mono & LSL compatible

//Other items required: For use with 'Remote Loader.lsl'

//Notes: Commented for easier following. Removes itself after use.

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

 

 

integer pin = 606;//change the pin to match what you put in remote loader.lsl

default

{

    state_entry()

    {

        llSetRemoteScriptAccessPin(pin);

        llOwnerSay("Pin has been set. My key is:" + (string)llGetKey());

        llRemoveInventory(llGetScriptName());//remove script from inventory

        llSleep(.5);

        //if that fails we'll get here

        llInstantMessage(llGetOwner(),"The script '" + (string)llGetScriptName() + "' in object " + llGetObjectName()

            + "at Region " + (string)llGetRegionName() + " loc: " + (string)llGetPos() + " failed to delete.");

        llSetScriptState(llGetScriptName(),FALSE);//shut off script

    }

}

// === Part 5/5 ===
// :CATEGORY:Texture
// :NAME:Remote_Texture_Loader
// :AUTHOR:Bobbyb30 Swashbuckler
// :CREATED:2010-12-27 12:20:34.060
// :EDITED:2013-09-18 15:39:01
// :ID:691
// :NUM:945
// :REV:1.0
// :WORLD:Second Life
// :DESCRIPTION:
// Print inventory texture keys.lsl
// :CODE:
//***********************************************************************************************************

//                                                                                                          *

//                                       -- Print inventory texture keys--                                  *

//                                                                                                          *

//***********************************************************************************************************

// www.lsleditor.org  by Alphons van der Heijden (SL: Alphons Jano)

//Creator: Bobbyb30 Swashbuckler

//Attribution: None required, but it is appreciated.

//Created: November 28, 2009

//Last Modified: November 28, 2009

//Released: Saturday, November 28, 2009

//License: Public Domain

 

//Status: Fully Working/Production Ready

//Version: 1.0.1

 

//Name: Print inventory texture keys.lsl

//Purpose: Prints out the UUID of inventory textures on chat for use in Main Display and Remote

//         Load texture display.

//Description: Prints out the keys of inventory textures on touch.

//Directions: Create a prim. Add desired texture. Add this script. Touch.

 

//Compatible: Mono & LSL compatible

//Other items required: None

//Notes: Commented for easier following.

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

 

default

{

    state_entry()

    {

        llOwnerSay("Bobbyb's 'Print inventory texture keys.lsl' (Public Domain 2009)");

        llOwnerSay("Touch to readout inventory texture keys.");

    }

    touch_start(integer total_number)

    {

        if(llDetectedKey(0) == llGetOwner())

        {

            integer inventorynumber = llGetInventoryNumber(INVENTORY_TEXTURE);

            integer counter;

            llOwnerSay("Found " + (string)inventorynumber + " textures...");

            llSetObjectName("");

            do

            {

                string inventoryname = llGetInventoryName(INVENTORY_TEXTURE,counter);

                llOwnerSay("/me " + "\"" + (string)llGetInventoryKey(inventoryname) + "\""

                    + ", // " + inventoryname);

            }while(++counter < inventorynumber);

            llSetObjectName("Print out");

            llOwnerSay("Please remove the comma from the last one.");

        }

    }

}
```
