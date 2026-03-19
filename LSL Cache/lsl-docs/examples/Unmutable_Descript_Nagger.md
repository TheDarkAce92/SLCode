---
name: "Unmutable Descript Nagger"
category: "example"
type: "example"
language: "LSL"
description: "Unmutable Descript Nagger - Linden Scripting Language (LSL) Version 1.0"
wiki_url: "https://wiki.secondlife.com/wiki/Unmutable_Descript_Nagger"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 Creator
- 2 Contributors
- 3 License
- 4 Disclaimer
- 5 Purpose
- 6 Documentation
- 7 Code

  - 7.1 Scripted Attatchment Detector
  - 7.2 Settings Notecard
  - 7.3 Nagger

Unmutable Descript Nagger - Linden Scripting Language (LSL)
Version 1.0

Creator

- Bobbyb30 Zohari -- Devolper

If you wish to request special rights,ask for assistance in setting it up, or donate, feel free to IM me.

Contributors

If you modify/improve upon the script, please add your name here.

License

This work is licensed under a [Creative Commons Attribution 3.0 Unported License](http://creativecommons.org/licenses/by/3.0/)

You are free:

- **to Share** — to copy, distribute and transmit the work
- **to Remix** — to adapt the work

Under the following conditions

- **Attribution.** You must attribute the work in the manner specified by the author or licensor (but not in any way that suggests that they endorse you or your use of the work).

1. For any reuse or distribution, you must make clear to others the license terms of this work. The best way to do this is with [a link to this web page](http://creativecommons.org/licenses/by/3.0/).
1. Any of the above conditions can be waived if you get permission from the copyright holder.
1. Nothing in this license impairs or restricts the author's moral rights.

Disclaimer

This program is distributed in the hope that it will be useful, but **WITHOUT ANY WARRANTY**; without even the implied warranty of **MERCHANTABILITY** or **FITNESS FOR A PARTICULAR PURPOSE**.

Purpose

- To nag avatars to take off their scripted attatchments.

Documentation

This will nag avatars to off their scripted attatchments. It is fairly low lag.

Assembly

**Part 1**

1. Create a prim(any shape, it doesn't matter.)
1. Name it "Descript Nagger".
1. Create a new script in the prim and call it "Scripted Attatchment Detector"(without the " ").
1. Create a new script in the sphere and paste the "Scripted Attatchment Detector" lsl code into it and save.

**Part 2**

1. Create a new notecard and name it "!Settings"(without the " ").
1. Paste the "Settings" code into it and save.
1. Place the !Settings notecard into the prim with the "Descript Nagger" script.

**Part 3**

1. Create a sphere.
1. Name the sphere "nag"(without the " ").
1. Create a new script in the sphere and paste the "nagger" lsl code into it and save.
1. Make the sphere .01x.01x.01 and transparent.
1. Take the sphere into your inventory.
1. Put the "nag" object from your inventory into the prim containing the "Descript Nagger" script.

Now you adjust the settings--for a description of the setting please see the Settings Section.

Code

## Scripted Attatchment Detector

```lsl
// www.lsleditor.org  by Alphons van der Heijden (SL: Alphons Jano)
//Script Detector by Bobbyb30 Zohari (C) 2008
//Created: July 25, 2008
//Last Modified: July 26, 2008
//             :12-11-09, added so it can be worn
//////////////////////
//http://creativecommons.org/licenses/by/3.0/

///////////
//notecard setup
//Range:
//Interval:
//IgnoreGroup: Yes/no
//Display HoverText: Yes/No
//Dialog Warning:
//Message Warning:
//Enable Dialog: Yes/No
//Enable Message: Yes/No
//Check if on myland:
//List the people whom to ignore on the next line...one per line...CaSe doesn't matter

list ignore;

integer displayhovertext;
integer range;//how far to scan
float interval;//how often to scan

integer ignoregroup;//if true ignore group, else warn them to.

string dialogwarning;
integer dialogwarn;

string messagewarning;
integer messagewarn;

integer checklandowner;
key landowner;

integer rez;//if both are no rez, then

integer line;
//link message on ch -1 nonscripted av

integer debug = TRUE;
txt(string input)
{
	llSetText("Loading...Please Wait\n \n" + input,<0.2, 1.0, 1.0>,1);
	if(debug)
		llOwnerSay("DEBUG: Loading: " +input);
}

default
{
	on_rez(integer start_param)
	{
		llResetScript();
	}
	state_entry()
	{
		llOwnerSay("Loading Settings");
		llGetNotecardLine("!Settings",line);
	}
	dataserver(key requested, string data)
	{
		if(data != EOF)
		{
			llGetNotecardLine("!Settings",++line);
			string text;
			if(llGetSubString(data,0,5) == "Range:")
			{
				range = (integer)llGetSubString(data,6,-1);
				txt("Range set to " + (string)range);
			}
			else if(llGetSubString(data,0,8) == "Interval:")
			{
				interval = (integer)llGetSubString(data,9,-1);
				txt("Interval set to " + (string)interval);
			}
			else if(llGetSubString(data,0,12) == "Ignore Group:")
			{
				text = llToLower(llStringTrim(llGetSubString(data,13,-1),STRING_TRIM));
				if(text == "yes")
				{
					ignoregroup = TRUE;
					txt("Ignoring Group");
				}
				else
				{
					ignoregroup = FALSE;
					txt("Not Ignoring Group");
				}
			}
			else if(llGetSubString(data,0,17) == "Display HoverText:")
			{
				text = llToLower(llStringTrim(llGetSubString(data,18,-1),STRING_TRIM));
				if(text == "yes")
				{
					displayhovertext = TRUE;
					txt("Displaying HoverText");
				}
				else
				{
					ignoregroup = FALSE;
					txt("Hiding HoverText");
				}
			}
			else if(llGetSubString(data,0,14) == "Dialog Warning:")
			{
				dialogwarning = llStringTrim(llGetSubString(data,15,-1),STRING_TRIM_HEAD);
				txt("Dialog Warning set to:\n " + dialogwarning);
			}
			else if(llGetSubString(data,0,13) == "Enable Dialog:")
			{
				text = llToLower(llStringTrim(llGetSubString(data,14,-1),STRING_TRIM));
				if(text == "yes")
				{
					dialogwarn = TRUE;
					txt("Enabling Dialog Warning");
				}
				else
				{
					dialogwarn = FALSE;
					txt("Disabling Dialog Warning");
				}
			}
			else if(llGetSubString(data,0,15) == "Message Warning:")
			{
				messagewarning = llStringTrim(llGetSubString(data,16,-1),STRING_TRIM_HEAD);
				txt("Message Warning set to:\n " + dialogwarning);
			}
			else if(llGetSubString(data,0,14) == "Enable Message:")
			{
				text = llToLower(llStringTrim(llGetSubString(data,15,-1),STRING_TRIM));
				if(text == "yes")
				{
					messagewarn = TRUE;
					txt("Enabling Message Warning");
				}
				else
				{
					messagewarn = FALSE;
					txt("Disabling Message Warning");
				}
			}
			else if(llGetSubString(data,0,19) == "Check if on my land:")
			{
				text = llToLower(llStringTrim(llGetSubString(data,20,-1),STRING_TRIM));
				if(text == "yes")
				{
					checklandowner = TRUE;
					txt("Enabling landchecking");
					landowner = llGetLandOwnerAt(llGetPos());
					if(llGetOwner() == landowner)
						return;
					else if(llList2Key(llGetObjectDetails(llGetKey(),[OBJECT_GROUP]),0) == landowner)
						return;
					else
						llOwnerSay("You must be the landowner or set the group of this object to the landowner group to use it.");
				}
				else
				{
					checklandowner = FALSE;
					txt("Disabling landchecking");
				}
			}

			else if(data == "List the people whom to ignore on the next line...one per line...CaSe doesn't matter")
				return;
			else
			{
				//add avatar name to list
				ignore = (ignore=[]) + ignore + llStringTrim(llToLower(data),STRING_TRIM_TAIL);
				txt("Added " + data + " to ignorelist");
				if(llGetFreeMemory() < 3000)
				{
					llOwnerSay("Ran out of memmory on " + data);
					state scan;
				}
			}
		}
		else
			state scan;
	}
	changed(integer change)
	{
		if(change & CHANGED_INVENTORY)
			llResetScript();
	}
	moving_end()
	{
		if(!llGetAttached())//if attatched, don't reset
			llResetScript();
	}
}
state scan
{
	on_rez(integer start_param)
	{
		llResetScript();
	}
	changed(integer change)
	{
		if(change & CHANGED_INVENTORY)
			llResetScript();
	}
	moving_end()
	{
		if(!llGetAttached())//if attatched, don't reset
			llResetScript();
	}
	state_entry()
	{
		llSetText("Setup complete...",<1,1,1>,1);
		llOwnerSay("Setup complete...");
		llSensor("","",AGENT,range,TWO_PI);
		llSensorRepeat("","",AGENT,range,TWO_PI,interval);
		if((dialogwarn == FALSE) & (messagewarn == FALSE))
			rez = FALSE;
		else
			rez = TRUE;
	}
	sensor(integer total_number)
	{
		if(debug)
			llOwnerSay("Detected:" + (string)total_number + " avatars");
		integer counter;
		string scriptedavatars;
		do
		{
			integer avatarscripted = FALSE;
			key avatar = llDetectedKey(counter);
			string avname = llKey2Name(avatar);
			if(avatar != llGetOwner())//if owner, ignore
			{
				//                if(llSameGroup(avatar))
				//                {
				//                    if(!ignoregroup)//if it is, no need to check
				//                    {
				//                        integer randomch = (integer)llFrand(90000000) + 500;
				//                        llRezAtRoot("nag",llGetPos(),ZERO_VECTOR,ZERO_ROTATION,randomch);
				//                        avatarscripted = TRUE;
				//                        llWhisper(randomch,(string)avatar);
				//                        if(checklandowner)
				//                        {
				//                            if(llGetLandOwnerAt(llDetectedPos(counter)) == landowner)//wrong landowner, don't bug them
				//                            {
				//                                if(messagewarn)
				//                                    llWhisper(randomch,messagewarning);
				//                                if(dialogwarn)
				//                                    llWhisper(randomch,dialogwarning);
				//                            }
				//                        }
				//                        else
				//                        {
				//                            if(messagewarn)
				//                                llWhisper(randomch,messagewarning);
				//                            if(dialogwarn)
				//                                llWhisper(randomch,dialogwarning);
				//                        }
				//                    }
				//                }

				if (llGetAgentInfo(avatar) & AGENT_SCRIPTED)
				{
					if(debug)
						llOwnerSay("DEBUG: AGENT SCRIPTED:" + avname);
					//if(!ignoregroup)//if it is, no need to check

					if(llSameGroup(avatar))
					{
						if(debug)
							llOwnerSay("DEBUG: GROUP: " + avname);
						if(!ignoregroup)
						{
							avatarscripted = TRUE;
							if(rez)
							{
								integer randomch = (integer)llFrand(90000000) + 500;
								llRezAtRoot("nag",llGetPos(),ZERO_VECTOR,ZERO_ROTATION,randomch);
								llWhisper(randomch,(string)avatar);
								if(checklandowner)
								{
									if(llGetLandOwnerAt(llDetectedPos(counter)) == landowner)//wrong landowner, don't bug them
									{
										if(messagewarn)
											llWhisper(randomch,messagewarning);
										if(dialogwarn)
											llWhisper(randomch,dialogwarning);
									}
								}
								else
								{
									if(messagewarn)
										llWhisper(randomch,messagewarning);
									if(dialogwarn)
										llWhisper(randomch,dialogwarning);
								}
							}
						}
					}
					llOwnerSay("avname:" + avname);//
					if(llListFindList(ignore,[llToLower(avname)]) == -1)
					{
						if(debug)
							llOwnerSay("DEBUG: LIST FAIL: " + avname);
						avatarscripted = TRUE;
						if(rez)
						{
							integer randomch = (integer)llFrand(90000000) + 500;
							llRezAtRoot("nag",llGetPos(),ZERO_VECTOR,ZERO_ROTATION,randomch);
							llWhisper(randomch,(string)avatar);
							if(checklandowner)
							{
								if(llGetLandOwnerAt(llDetectedPos(counter)) == landowner)//wrong landowner, don't bug them
								{
									if(messagewarn)
										llWhisper(randomch,messagewarning);
									if(dialogwarn)
										llWhisper(randomch,dialogwarning);
								}
							}
							else
							{
								if(messagewarn)
									llWhisper(randomch,messagewarning);
								if(dialogwarn)
									llWhisper(randomch,dialogwarning);
							}
						}
					}
				}
				integer space = 0;//just a break in the if statements
				if(avatarscripted)//if scripted, add to list
				{
					if(debug)
						llOwnerSay("DEBUG: AV Scripted: " + avname + "||" + scriptedavatars);
					scriptedavatars = scriptedavatars + avname + "\n";
					llMessageLinked(LINK_ALL_OTHERS,-1,avname,"");//take off list
				}
				else
					llMessageLinked(LINK_ALL_OTHERS,-1,avname,"");
			}
		}while(++counter < total_number);
		if(displayhovertext)
		{
			if(debug)
				llOwnerSay("Following avatars were scripted:" + scriptedavatars);
			if(scriptedavatars == "")
				llSetText("*Scripted Avatars*\n \nNone Detected",<1.0, 0.0, 0.0>,1.0);
			else
				llSetText("*Scripted Avatars*\n" + scriptedavatars,<1.0, 0.0, 0.0>,1.0);
		}
	}
	no_sensor()
	{
		if(debug)
			llOwnerSay("Detected: no avatars");
		if(displayhovertext)
			llSetText("*Scripted Avatars*\n \nNone Detected",<1.0, 0.0, 0.0>,1.0);
		llMessageLinked(LINK_ALL_OTHERS,-3,"none","");//no one detected
	}
}

//permanant ejector
//bring to ground car script when too high
//[16:56]  Amber Linden: Hello everyone... Montly Mentors meeting fixing to start in 5 mins.. Join Vteam at the SL Volunteer Island Center Stage!
```

## Settings Notecard

The notecard should be named "!Settings" without the "".
Here's a description of what it does...

- Range: How far to scan, enter a value from 1-96
- Integer: How often to scan in seconds, enter a value from 20-500
- Ignore Group: if yes, it will ignore group members, if no, it will not
- Display HoverText: if yes, it will display hovertext, if no, it will not
- Dialog Warning: the warning that will go in the dialog
- Message Warning: the warning that will go into the message
- Enable Dialog: if yes, it will show a dialog, if no, it will not
- Enable Message: if yes, it will IM them, if no it will not
- Check if on my land: if yes, it will check whether the avatar is on your land, if no, it will
- List the people whom to ignore on the next line...one per line...CaSe doesn't matter
- Anyone listed here or below will be ignored if they are scripted

```lsl
Range: 96
Interval: 60
Ignore Group: Yes
Display HoverText: Yes
Dialog Warning: warning remove your stuff
Message Warning: Warning, remove your stuff
Enable Dialog: Yes
Enable Message: Yes
Check if on my land: Yes
List the people whom to ignore on the next line...one per line...CaSe doesn't matter
Bobbyb30 Zohari
Madsen Toodle
Stroodle Noodle
```

At  Sassy1 Fizzle's request....
You may also use it as an hud alone...this will scan 96m around and display who is scripted. You only need to include this in the notecard "!Settings" and the "Scripted Attatchment Detector". You do not need the nagger script.

```lsl
Range: 96
Interval: 30
Ignore Group: No
Display HoverText: Yes
Dialog Warning: warning remove your stuff
Message Warning: Warning, remove your stuff
Enable Dialog: No
Enable Message: No
Check if on my land: No
List the people whom to ignore on the next line...one per line...CaSe doesn't matter
Madsen Toodle
Stroodle Noodle
```

## Nagger

```lsl
// www.lsleditor.org  by Alphons van der Heijden (SL: Alphons Jano)
//Script Detector by Bobbyb30 Zohari (C) 2008
//Created: July 26, 2008
//Last Modified: July 26, 2008
//////////////////////
////http://creativecommons.org/licenses/by/3.0/

key avatar;
integer counter;
string message;
string dialog;
default
{
	on_rez(integer channel)
	{
		llListen(channel,"","","");
	}
	listen(integer ch, string name, key id, string msg)
	{
		if(counter == 0)
			avatar = msg;
		else if(counter == 1)
			message = msg;
		else if(counter == 2)
		{
			llSetObjectName("Script Remover Nagger" + (string)((integer)llFrand(50000)));
			dialog = msg;
			if(msg != "")
				llInstantMessage(avatar,message);
			if(dialog != "")
				llDialog(avatar,"\n" + dialog + "\n \n \nScripted Attatchment Nagger\nBobbyb30 Zohari (C) 2008",[],-1);
			llDie();
			llDie();
		}
		++counter;
	}
}
```

[https://wiki.secondlife.com/wiki/User:Bobbyb30_Zohari](https://wiki.secondlife.com/wiki/User:Bobbyb30_Zohari)

<a rel="license" href="[http://creativecommons.org/licenses/by/3.0/](http://creativecommons.org/licenses/by/3.0/)">
<img alt="Creative Commons License" style="border-width:0" src="[http://i.creativecommons.org/l/by/3.0/88x31.png](http://i.creativecommons.org/l/by/3.0/88x31.png)" />
</a>


Unmutable Descript Nagger by
<a xmlns:cc="[http://creativecommons.org/ns#](http://creativecommons.org/ns#)" href="[http://wiki.secondlife.com/wiki/Unmutable_Descript_Nagger](http://wiki.secondlife.com/wiki/Unmutable_Descript_Nagger)" property="cc:attributionName" rel="cc:attributionURL">Bobbyb30 Zohari</a> is licensed under a
<a rel="license" href="[http://creativecommons.org/licenses/by/3.0/](http://creativecommons.org/licenses/by/3.0/)">Creative Commons Attribution 3.0 Unported License</a>.

Based on a work at
<a xmlns:dc="[http://purl.org/dc/elements/1.1/](http://purl.org/dc/elements/1.1/)" href="[http://wiki.secondlife.com/wiki/Unmutable_Descript_Nagger](http://wiki.secondlife.com/wiki/Unmutable_Descript_Nagger)" rel="dc:source">wiki.secondlife.com</a>.