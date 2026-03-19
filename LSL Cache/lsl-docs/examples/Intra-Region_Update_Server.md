---
name: "Intra-Region Update Server"
category: "example"
type: "example"
language: "LSL"
description: "Intra-Region Update Server by Emma Nowhere"
wiki_url: "https://wiki.secondlife.com/wiki/Intra-Region_Update_Server"
author: "Emma Nowhere"
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 About

  - 1.1 Note to Sellers!
- 2 UpdateServer
- 3 UpdateSubscriber

## About

Intra-Region Update Server by Emma Nowhere

This set of scripts allows you to centrally update objects such as Freeview screens or teleport pads within a region that are configured by notecards or contain modifiable objects or media assets.

Place the UpdateServer script inside a prim along with the objects (notecards, etc.) that you want to broadcast as updates to objects containing the UpdateSubscriber script.

To broadcast an update from the server, click on the server prim, and then click on the "Broadcast" button in the dialog.  The "Info" button displays the server's object key and listening channel as well as a list of all registered subscribers.  The "Purge" button removes all contents from the prim so you can drag new updates objects onto it.

Place the UpdateSubscriber script inside any prims that you want to receive object updates from an UpdateServer.  You can have as many prims as you want subscribed to an UpdateServer, for example, all the teleport pads in your region.  You should have your UpdateServer already set up before adding this script to a prim.  At startup the script will broadcast a request for all UpdateServers in the region and output the results to you.

You need to register the subscriber with a specific UpdateServer to enable updates to be received.  To do this, type:

```lsl
/128 UpdateSubscriberRegister subscriberkey serverkey
```

where *subscriberkey* is the key of the prim containing the script and *serverkey* is the key shown next to the UpdateServer name that is displayed when this script displays the available UpdateServers in the region.  The UpdateSubscriber script will output exact text that you can copy and past into your chat line to do this.

To send updates to group-owned objects, both the server and subscriber must belong to the same group (share and deed to group) and you must make your group active for your avatar (so that your group tag is visible).

### Note to Sellers!

Please give some attribution if you use these scripts. Thanks!

## UpdateServer

```lsl
 //////////////////////////////////////////////////////////////////////////////////////
 //
 //    UpdateServer
 //    Version 1.01 Release
 //    Copyright (C) 2007, Emma Nowhere
 //    emma.nowhere@yahoo.com
 //
 //    Place inside a prim along with the objects (notecards, etc.) that you
 //    want to broadcast as updates to objects containing the UpdateSubscriber
 //    script.
 //
 //    To broadcast an update, click on the prim, and then click on the "Broadcast"
 //    button in the dialog.
 //
 //    The "Info" button displays the server's object key and listening channel.
 //
 //    The "Purge" button removes all contents from the prim so you can drag new
 //    updates objects onto it.
 //
 //    License:
 //
 //    This library is free software; you can redistribute it and/or
 //    modify it under the terms of the GNU Lesser General Public License
 //    as published by the Free Software Foundation; either
 //    version 2.1 of the License, or (at your option) any later version.
 //
 //    This library is distributed in the hope that it will be useful,
 //    but WITHOUT ANY WARRANTY; without even the implied warranty of
 //    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 //    GNU Lesser General Public License for more details.
 //
 //    You should have received a copy of the GNU Lesser General Public License
 //    along with this library; if not, write to the Free Software
 //    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 //
 //////////////////////////////////////////////////////////////////////////////////////

 integer listenChannel = 128;
 integer listenHandle = 0;
 integer dialogChannel = 52;
 integer dialogHandle = 0;
 string scriptName;
 key serverKey;

 list mainMenu = ["Info", "Broadcast", "Purge"];

 deleteAllItems() {

     integer total = llGetInventoryNumber(INVENTORY_ALL);
     integer i;
     //for (i = 0; i < total; i++) {  // <- This does not remove all items ;-) !
     for (i = total-1; i >= 0; i--) { // Work arround (EDIT: LV Wildmist)
         string name = llGetInventoryName(INVENTORY_ALL, i);
         if (name != scriptName) llRemoveInventory(name);
     }
 }

 integer containsItem(string itemName) {

     integer total = llGetInventoryNumber(INVENTORY_ALL);
     integer i;
     for (i = 0; i < total; i++) {
         string name = llGetInventoryName(INVENTORY_ALL, i);
         if ((name != scriptName) && (itemName == name)) return TRUE;
     }
     return FALSE;

 }

 broadcastAvailableUpdates() {

     llSay(0, "Broadcasting available updates...");

     integer total = llGetInventoryNumber(INVENTORY_ALL);
     integer i;
     for (i = 0; i < total; i++) {
         string name = llGetInventoryName(INVENTORY_ALL, i);
         if (name != scriptName) {
             llRegionSay(listenChannel, "UpdateAvailable " + llEscapeURL(name));
             llSay(0, "UpdateAvailable item: " + name);
         }
     }

     llSay(0, "Broadcasting complete");

 }

 showServerInfo() {

     llSay(0, "Update Server key: " + (string)serverKey);

     llSay(0, "Update Server listening on channel #" + (string)listenChannel);

     llRegionSay(listenChannel, "UpdateSubscribersQuery " + (string)serverKey);

 }

 default {

     state_entry() {
         scriptName = llGetScriptName();
         serverKey = llGetKey();

         llSetText("Update Server\n" + llGetObjectName() + "\n" + (string)serverKey, <1,0,0>, 1.0);

         listenHandle = llListen(listenChannel, "", NULL_KEY, "");

         showServerInfo();
     }

     touch_start(integer num_detected) {
         llListenRemove(dialogHandle);
         dialogChannel = llFloor(llFrand(-99899.0) - 100);
         dialogHandle = llListen(dialogChannel, "", NULL_KEY, "");

         integer group = llDetectedGroup(0);
         key agent = llDetectedKey(0);
         key objectowner = llGetOwner();
         if ((objectowner == agent) || group)  {
             llDialog(agent, "Update Server v1.0a", mainMenu, dialogChannel);
         }
     }

     listen(integer channel, string name, key id, string message)
     {

         if (channel == dialogChannel) {

             llListenRemove(dialogHandle);

             if (message == "Broadcast") broadcastAvailableUpdates();

             if (message == "Purge") deleteAllItems();

             if (message == "Info") showServerInfo();

             return;
         }

         list parsed = llParseString2List(message, [" "], []);
         integer l = llGetListLength(parsed);
         if (l == 0) return;

         string command = llList2String(parsed, 0);

         if ((l == 4) && (command == "UpdateRequest")) {

             string itemName = llUnescapeURL(llList2String(parsed, 1));
             key destination = (key)llList2String(parsed, 2);
             key requestServer = (key)llList2String(parsed, 3);

             if (requestServer != serverKey) return;

             if (containsItem(itemName)) {
                 llSay(0, "Giving item " + itemName + " to object " + llKey2Name(destination) + " (" + (string)destination + ")");
                 llGiveInventory(destination, itemName);
             }
         }
         else if (command == "UpdateServersQuery") {

             llRegionSay(listenChannel, "UpdateServerAvailable " + (string)serverKey);

         }
         else if ((l == 3) && (command == "UpdateSubscriberRegistered")) {

             key subscriberUpdateServer = (key)llList2String(parsed, 1);
             key subscriberKey = (key)llList2String(parsed, 2);

             if (subscriberUpdateServer != serverKey) return;

             if (subscriberUpdateServer == serverKey) {

                 string msg = "UpdateSubscriber " + llKey2Name(subscriberKey) +
                 " (" + (string)subscriberKey + ") registered to UpdateServer " +
                 llKey2Name(subscriberUpdateServer) + " (" + (string)subscriberUpdateServer + ")";

                 llSay(0, msg);
             }

         }
     }

 }
```

## UpdateSubscriber

```lsl
 //////////////////////////////////////////////////////////////////////////////////////
 //
 //    UpdateSubscriber
 //    Version 1.01 Release
 //    Copyright (C) 2007, Emma Nowhere
 //    emma.nowhere@yahoo.com
 //
 //    Place inside a prim that you want to receive object updates from an
 //    UpdateServer.  You should have your UpdateServer already set up
 //    before adding this script to a prim.
 //
 //    At startup the script will broadcast a request for all UpdateServers
 //    in the region and output the results to you.
 //
 //    You need to register with a specific UpdateServer to enable updates
 //    to be received.
 //
 //    To lock onto a specific UpdateServer, type:
 //
 //    /128 UpdateSubscriberRegister
 //
 //    where  is the key of the prin containing the script
 //    and  is the key shown next to the UpdateServer name that is
 //    displayed when this script displays the available UpdateServers in
 //    the region.
 //
 //    License:
 //
 //    This library is free software; you can redistribute it and/or
 //    modify it under the terms of the GNU Lesser General Public License
 //    as published by the Free Software Foundation; either
 //    version 2.1 of the License, or (at your option) any later version.
 //
 //    This library is distributed in the hope that it will be useful,
 //    but WITHOUT ANY WARRANTY; without even the implied warranty of
 //    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 //    GNU Lesser General Public License for more details.
 //
 //    You should have received a copy of the GNU Lesser General Public License
 //    along with this library; if not, write to the Free Software
 //    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 //
 //////////////////////////////////////////////////////////////////////////////////////

 integer listenChannel = 128;
 integer listenHandle = 0;
 string scriptName;
 key subscriberKey;
 key serverKey;
 integer registered = FALSE;

 integer containsItem(string itemName) {

     integer total = llGetInventoryNumber(INVENTORY_ALL);
     integer i;
     for (i = 0; i < total; i++) {
         string name = llGetInventoryName(INVENTORY_ALL, i);
         if ((name != scriptName) && (itemName == name)) return TRUE;
     }
     return FALSE;
 }

 default {

     state_entry() {

         scriptName = llGetScriptName();
         subscriberKey = llGetKey();

         llSay(0, "UpdateSubscriber installed in object " + llGetObjectName() + " (" + (string)subscriberKey + ")");
         listenHandle = llListen(listenChannel, "", NULL_KEY, "");

         llSay(0, "UpdateSubscriber listening on channel #" + (string)listenChannel);
         llRegionSay(listenChannel, "UpdateServersQuery");
     }

     listen(integer channel, string name, key id, string message) {

         list parsed = llParseString2List(message, [" "], []);
         integer l = llGetListLength(parsed);
         if (l == 0) return;

         string command = llList2String(parsed, 0);

         if (!registered) {

                 if ((l == 3) && (command == "UpdateSubscriberRegister")) {

                     if ((key)llList2String(parsed, 1) != subscriberKey) return;

                     serverKey = (key)llList2String(parsed, 2);

                     llListenRemove(listenHandle);

                     listenHandle = llListen(listenChannel, "", serverKey, "");

                     llSay(0, "Registered to Update Server " + llKey2Name(serverKey) + " (" + (string)serverKey + ")");

                     registered = TRUE;
                 }
                 else if ((l == 2) && (command == "UpdateServerAvailable")) {

                     key serverKey = (key)llList2String(parsed, 1);

                     string msg = "Update Server available:\n" + llKey2Name(serverKey) + " (" + (string)serverKey + ")\n\n" +
                     "Copy and paste the following line to register to this server:\n\n" +
                     "/128 UpdateSubscriberRegister " + (string)subscriberKey + " " + (string)serverKey + "\n\n";

                     llSay(0, msg);
                 }


                 return;
         }


         if ((l == 2) && (command == "UpdateAvailable")) {

             string itemName = llUnescapeURL(llList2String(parsed, 1));

             if (containsItem(itemName)) {

                 llSay(0, "Deleting old version of item " + itemName);
                 llRemoveInventory(itemName);

                 llSay(0, "Requesting new version of item " + itemName);
                 llRegionSay(listenChannel, "UpdateRequest " + llEscapeURL(itemName) + " " + (string)subscriberKey + " " + (string)serverKey);
             }
         }
         else if ((l == 2) && (command == "UpdateSubscribersQuery")) {

             key serverKey = (key)llList2String(parsed, 1);

             llRegionSay(listenChannel, "UpdateSubscriberRegistered " + (string)serverKey + " " + (string)subscriberKey);
         }

     }

 }
```