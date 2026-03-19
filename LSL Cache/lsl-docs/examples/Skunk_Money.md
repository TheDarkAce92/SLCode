---
name: "Skunk Money"
category: "example"
type: "example"
language: "LSL"
description: "This is the engine of the Skunk Money machine. There are scripts in each \"tile\" and in the numerical display..."
wiki_url: "https://wiki.secondlife.com/wiki/Skunk_Money"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

This is the engine of the Skunk Money machine.  There are scripts in each "tile" and in the numerical display...

- 1 Skunk Money Engine
- 2 Settings Notecard
- 3 Game Tile Script
- 4 Cash Out Button
- 5 Price Display

## Skunk Money Engine

```lsl
//Skunk Money Engine
//by Hank Ramos

//Constants
integer SEND_PLAYER_ID = 962214;
integer GAME_RUNNING   = 953365;
integer GAME_DISABLED  = 953366;
integer PAYOUT_SET     = 253340;
integer PAYOUT_SEND    = 358763;
integer SYSTEM_RESET   = 853324;
integer TILE_ALL_SET   = 122545;
integer PAYOUT_BUTTON  = 632587;
integer ID_REQUEST     = 856621;
integer ID_SEND        = 856621;
integer TILE_RANDOMIZE = 721002;
integer JACKPOT_SET    = 3665222;
integer DISPLAY_POT    = 5321447;
integer DISPLAY_PRICE  = 6324419;
integer SET_STATS      = 8665329;
integer RETRIEVE_STATS = 8662211;

//Default Options
//In case Settings Notecard is missing
integer demoMode             = TRUE; //True will refund all money paid in, and will pay no money out.
list    payouts              = [0, 1, -50, -25, -20, -10, -5, -2, -1, 1, 2, 5, 10, 20, 25, 50];
integer gameCost             = 25;    //Cost to play the Game
float   jackpotOdds          = 0.05;  //% of the time to show progressive tile
integer jackpotInitialValue  = 10;    //Vale of Progressive Jackpot when reset or after win
integer jackpotWinIncrement  = 1;     //Amount Progressive Jackpot is incremented upon a winning pot
integer jackpotLoseIncrement = 5;     //Amount Progressive Jackpot is incrmeneted upon a losing pot
integer maxLosses            = 500;   //Maximum amount of money this machine will lose before shutting down
integer commissionVersion    = FALSE;  //If true, L$1/L$2 of all money deposited is paid to Hank Ramos

//Variables
key     playerID;
string  playerName;
integer currentPayout;
integer payoutCount;
integer jackpotPayout;
integer moneyIn;
integer moneyOut;
integer timesPlayed;
integer highestJackpot;
integer highestPayout;
string  highestPayoutName;
integer count;
integer lineCount;
key     readKey;
integer dialogChatChannel;
integer dialogListen;
integer imCounter;
key     ownerID;
integer commissionHigh;
integer commissionPaid;

dispStats()
{
    llOwnerSay("========================================");
    llOwnerSay("Skunk Money Stats");
    llOwnerSay("-----------------");
    llOwnerSay("Plays: " + (string)timesPlayed);
    llOwnerSay("Highest Jackpot: L$" + (string)highestJackpot);
    llOwnerSay("Highest Payout: L$" + (string)highestPayout + " to " + highestPayoutName);
    llOwnerSay("L$ Collected: L$" + (string)moneyIn);
    llOwnerSay("L$ Dispensed: L$" + (string)moneyOut);
    if (commissionVersion)
    {
        llOwnerSay("L$ Commission (included in L$ Dispensed): L$" + (string)commissionPaid);
    }
    llOwnerSay("Memory Free: " + (string)llGetFreeMemory() + " bytes");
    llOwnerSay("========================================");
}
setStats()
{
    list statValues;
    string csvList;

    //Parse Stats
    statValues += timesPlayed;
    statValues += highestJackpot;
    statValues += highestPayout;
    statValues += highestPayoutName;
    statValues += moneyIn;
    statValues += moneyOut;
    statValues += commissionPaid;
    statValues += jackpotPayout;

    csvList = llDumpList2String(statValues, ",");
    llMessageLinked(LINK_ALL_OTHERS, SET_STATS, csvList, NULL_KEY);
}
checkCommands(key id, string message)
{
    if (message == "Stats")
    {
        //Display stats only for the owner
        dispStats();
    }
    if (message == "Reset JPot")
    {
        jackpotPayout = jackpotInitialValue;
        setStats();
        llMessageLinked(LINK_ALL_OTHERS, JACKPOT_SET, (string)jackpotPayout, NULL_KEY);
        llOwnerSay("Jackpot Reset.");
    }
    if (message == "Reset Stats")
    {
        moneyIn           = 0;
        moneyOut          = 0;
        timesPlayed       = 0;
        highestJackpot    = 0;
        highestPayout     = 0;
        commissionPaid    = 0;
        highestPayoutName = "Nobody";
        setStats();
        llOwnerSay("Stats Reset.");
    }
    if (message == "Reset Script")
    {
        llOwnerSay("Resetting Script...");
        llResetScript();
    }
    if (message == "Play Free")
    {
        playerID = id;
        playerName = llKey2Name(playerID);
        moneyIn += gameCost;
        state playing;
    }
}
default
{
    state_entry()
    {
        integer x;

        ownerID = llGetOwner();
        llSetTexture("4fedf47c-aeda-77d1-a9f2-59e4fc2d809b", 3);

        for (x = 0; x < llGetInventoryNumber(INVENTORY_SOUND); x++)
        {
            llPreloadSound(llGetInventoryName(INVENTORY_SOUND, x));
        }

        state loadSettings;
    }
}
state resetAll
{
    state_entry()
    {
        if (llGetOwner() != ownerID)
        {
            jackpotPayout = jackpotInitialValue;
            moneyIn           = 0;
            moneyOut          = 0;
            timesPlayed       = 0;
            highestJackpot    = 0;
            highestPayout     = 0;
            commissionPaid    = 0;
            highestPayoutName = "Nobody";
            llMessageLinked(LINK_ALL_OTHERS, JACKPOT_SET, (string)jackpotPayout, NULL_KEY);
            setStats();
            llOwnerSay("Reset For New Owner.");
        }
        llResetScript();
    }
}
state loadSettings
{
    state_entry()
    {
        integer found = FALSE;
        integer x;

        count = 0;
        lineCount = 0;

        for (x=0; x < llGetInventoryNumber(INVENTORY_NOTECARD); x += 1)
        {
            if (llGetInventoryName(INVENTORY_NOTECARD, x) == "Settings")
            {
                found = TRUE;
            }
        }
        if (found)
        {
            llOwnerSay("Reading Settings Notecard...");
            readKey = llGetNotecardLine("Settings", lineCount);
        }
        else
        {
            llOwnerSay("Settings Notecard Not Found, using default values...");
            state initialize;
        }
    }
    dataserver(key requested, string data)
    {
        integer integerData;
        float   floatData;
        if (requested == readKey)
        {
            if (data != EOF)
            {
                if ((llSubStringIndex(data, "#") != 0) && (data != "") && (data != " "))
                {
                    integerData = (integer)data;
                    floatData   = (float)data;
                    if (count == 0)
                    {
                        demoMode = TRUE;
                        count = 1;
                    }
                    if (count == 1)
                    {
                        if ((integerData == 25) || (integerData == 10))
                        {
                            gameCost = integerData;
                        }
                    }
                    if (count == 2)
                    {
                        if (gameCost == 25)
                        {
                            payouts  = [0, -50, -25, -20, -10, -5, -2, -1, 1, 2, 5, 10, 20, 25, 50];
                            if (integerData == 0)
                            {
                                payouts += -10;
                            }
                            else if (integerData == 1)
                            {
                                payouts += -5;
                            }
                            else if (integerData == 2)
                            {
                                payouts += -1;
                            }
                            else if (integerData == 3)
                            {
                                payouts += 1;
                            }
                            else if (integerData == 4)
                            {
                                payouts += 2;
                            }
                            else if (integerData == 5)
                            {
                                payouts += 5;
                            }
                            else if (integerData == 6)
                            {
                                payouts += 10;
                            }
                            else if (integerData == 7)
                            {
                                payouts += 20;
                            }
                        }
                        else
                        {
                            payouts  = [0, -20, -10, -5, -5, -2, -2, -1, 1, 2, 2, 5, 5, 10, 20];
                            if (integerData == 0)
                            {
                                payouts += -10;
                            }
                            else if (integerData == 1)
                            {
                                payouts += -5;
                            }
                            else if (integerData == 2)
                            {
                                payouts += -2;
                            }
                            else if (integerData == 3)
                            {
                                payouts += -1;
                            }
                            else if (integerData == 4)
                            {
                                payouts += 1;
                            }
                            else if (integerData == 5)
                            {
                                payouts += 2;
                            }
                            else if (integerData == 6)
                            {
                                payouts += 5;
                            }
                            else if (integerData == 7)
                            {
                                payouts += 10;
                            }
                        }
                    }
                    if (count == 3)
                    {
                        if ((floatData >= 0.004999)&&(floatData <= 5.000001))
                        {
                            jackpotOdds = floatData;
                        }
                    }
                    if (count == 4)
                    {
                        if (integerData >= 10)
                        {
                            jackpotInitialValue = integerData;
                        }
                    }
                    if (count == 5)
                    {
                        if (integerData >= 0)
                        {
                            jackpotWinIncrement = integerData;
                        }
                    }
                    if (count == 6)
                    {
                        if (integerData >= 1)
                        {
                            jackpotLoseIncrement = integerData;
                        }
                    }
                    if (count == 7)
                    {
                        if (integerData >= 1)
                        {
                            maxLosses = integerData;
                        }
                    }
                    count += 1;
                }
                lineCount += 1;
                readKey = llGetNotecardLine("Settings", lineCount);
            }
            else
            {
                llOwnerSay("========================================");
                llOwnerSay("Settings are loaded");
                llOwnerSay("-------------------");
                state initialize;
            }
        }
    }
    state_exit()
    {
        if (demoMode)
        {
            llOwnerSay("DemoMode: TRUE");
        }
        else
        {
            llOwnerSay("DemoMode: FALSE");
        }
        llOwnerSay("GameCost: L$" + (string)gameCost);
        llOwnerSay("Payouts: L$" + llDumpList2String(payouts, ",L$"));
        llOwnerSay("JackpotOdds: " + (string)jackpotOdds);
        llOwnerSay("JackpotWinIncrement: L$" + (string)jackpotWinIncrement);
        llOwnerSay("JackpotLoseIncrement: L$" + (string)jackpotLoseIncrement);
        llOwnerSay("MaxLosses: L$" + (string)maxLosses);
        llOwnerSay("========================================");
        llSetPayPrice(PAY_HIDE, [gameCost, PAY_HIDE, PAY_HIDE, PAY_HIDE]);
    }
}
state initialize
{
    state_entry()
    {
        float payback;
        integer x;

        llOwnerSay("Initializing...");

        count = 0;
        jackpotPayout = jackpotInitialValue;
        highestJackpot = jackpotPayout;

        llMessageLinked(LINK_ALL_OTHERS, RETRIEVE_STATS, "", NULL_KEY);
        llMessageLinked(LINK_ALL_OTHERS, TILE_ALL_SET, "QuestionMarks", NULL_KEY);

        llSleep(2);

        llMessageLinked(LINK_ALL_OTHERS, SYSTEM_RESET, "", NULL_KEY);
        llMessageLinked(LINK_ALL_OTHERS, JACKPOT_SET, (string)jackpotPayout, NULL_KEY);
        if (demoMode)
        {
            llMessageLinked(LINK_ALL_OTHERS, DISPLAY_PRICE, (string)0, NULL_KEY);
        }
        else
        {
            llMessageLinked(LINK_ALL_OTHERS, DISPLAY_PRICE, (string)gameCost, NULL_KEY);
        }
    }
    on_rez(integer start_param)
    {
        state resetAll;
    }
    link_message(integer sender_num, integer num, string str, key id)
    {
        if (num == RETRIEVE_STATS)
        {
            list statValues = llCSV2List(str);
            //Parse Stats
            timesPlayed       = llList2Integer(statValues, 0);
            highestJackpot    = llList2Integer(statValues, 1);
            highestPayout     = llList2Integer(statValues, 2);
            highestPayoutName = llList2String (statValues, 3);
            moneyIn           = llList2Integer(statValues, 4);
            moneyOut          = llList2Integer(statValues, 5);
            commissionPaid    = llList2Integer(statValues, 6);
            jackpotPayout     = llList2Integer(statValues, 7);

            if (jackpotPayout < jackpotInitialValue)
            {
                jackpotPayout = jackpotInitialValue;
            }
            llMessageLinked(LINK_ALL_OTHERS, JACKPOT_SET, (string)jackpotPayout, NULL_KEY);

            dispStats();
        }
        if (num == ID_REQUEST)
        {
            llMessageLinked(sender_num, ID_SEND, (string)count, NULL_KEY);
            count += 1;
            if (count >= 16)
            {
                state idledemo;
            }
        }
    }
    state_exit()
    {
        llOwnerSay("Initialized Successfully...");
    }
}
state broken
{
    state_entry()
    {
        llMessageLinked(LINK_ALL_OTHERS, DISPLAY_PRICE, (string)-1, NULL_KEY);
        llSay(0, "Machine Malfunction.  Please Contact Owner.");
    }
    on_rez(integer start_param)
    {
        state resetAll;
    }
    touch_start(integer num_detected)
    {
        integer x;

        for (x=0; x < num_detected; x += 1)
        {
            if (llDetectedKey(x) == ownerID)
            {
                llSay(0, "Resuming...");
                llRequestPermissions(ownerID, PERMISSION_DEBIT);
                llSleep(10);
                llSay(0, "Resumed.");
                maxLosses += 100;
                llMessageLinked(LINK_ALL_OTHERS, DISPLAY_PRICE, (string)gameCost, NULL_KEY);
                state idledemo;
            }
        }
        llSay(0, "Machine Malfunction.  Please Contact Owner.");
        llSleep(10);
    }
}
state idledemo
{
    state_entry()
    {
        llSetTexture("4fedf47c-aeda-77d1-a9f2-59e4fc2d809b", 3);
        if ((moneyOut - moneyIn) > maxLosses)
        {
            state broken;
        }
        //Check Debit Permissions
        if (!(llGetPermissions() & PERMISSION_DEBIT))
        {
            //state broken;
        }
    }
    changed(integer change)
    {
        //Check Debit Permissions
        if (!(llGetPermissions() & PERMISSION_DEBIT))
        {
            //state broken;
        }
    }
    listen(integer channel, string name, key id, string message)
    {
        llListenRemove(dialogListen);
        checkCommands(id, message);
    }
    on_rez(integer start_param)
    {
        state resetAll;
    }
    touch_start(integer total_number)
    {
        integer x;

        for (x=0; x < total_number; x += 1)
        {
            if (llDetectedKey(x) == ownerID)
            {
                llListenRemove(dialogListen);
                dialogChatChannel = llRound(llFrand(2000000));
                dialogListen = llListen(dialogChatChannel, "", ownerID, "");
                llDialog(ownerID, "Administrative Options", ["Stats", "Reset Stats", "Reset JPot", "Reset Script", "Play Free"], dialogChatChannel);
                return;
            }
            else
            {
                playerID = llDetectedKey(x);
                playerName = llKey2Name(playerID);
                moneyIn += gameCost;
                llSay(0, "Welcome to Skunk Money! This game is for amusement purposes only. No real L$ or item of value can be won with this game. Enjoy!");
                state playing;
            }
        }
    }

    state_exit()
    {
        llListenRemove(dialogListen);
    }
}

state playing
{
    state_entry()
    {
        integer x;
        integer sendPayout;

        //Initialize and Set Variables
        currentPayout = 0;
        payoutCount   = 0;
        timesPlayed   += 1;
        llMessageLinked(LINK_ALL_OTHERS, DISPLAY_POT, (string)currentPayout, NULL_KEY);

        //Setup proximity sensor
        llSensorRepeat("", playerID, AGENT, 25, TWO_PI, 30);

        //Randomize and Setup Tiles
        payouts = llListRandomize(payouts, 1);
        llLoopSound("Randomizing", 0.75);
        llMessageLinked(LINK_ALL_OTHERS, TILE_RANDOMIZE, "", NULL_KEY);
        llMessageLinked(LINK_ALL_OTHERS, SEND_PLAYER_ID, "", playerID);

        //Send Payouts to Tiles
        for (x=0; x < 16; x += 1)
        {
            integer sendPayout = llList2Integer(payouts, x);

            if (sendPayout == 0)
            {
                if (llFrand(1) < jackpotOdds)
                {
                    sendPayout = 999999999;
                }
            }
            llMessageLinked(LINK_ALL_OTHERS, PAYOUT_SET + x, (string)sendPayout, NULL_KEY);
        }
        llSleep(3);

        //Start Game
        llMessageLinked(LINK_ALL_OTHERS, GAME_RUNNING, "", NULL_KEY);
        llStopSound();
    }
    sensor(integer num_detected)
    {
    }
    no_sensor()
    {
        llInstantMessage(playerID, "Cashing Out your Payout since you left the vicinity of the game. Thanks for playing!");
        state payout;
    }
    on_rez(integer start_param)
    {
        state resetAll;
    }
    link_message(integer sender_num, integer num, string str, key id)
    {
        integer amount;

        if (num == PAYOUT_SEND)
        {
            amount = (integer)str;

            if (amount == 0)
            {
                //Skunk was selected
                currentPayout = 0;
                llMessageLinked(LINK_ALL_OTHERS, TILE_ALL_SET, "Skunk", NULL_KEY);
                llPlaySound("Loser", 0.75);
                llSay(0, "You Found the SKUNK!");
                llSleep(3);
                state payout;
            }
            else if (amount == 999999999)
            {
                //Jackpot was selected
                llPlaySound("Jackpot", 0.75);
                llSay(0, "You Got the L$" + (string)jackpotPayout + " JACKPOT!");
                currentPayout += jackpotPayout;
                jackpotPayout = jackpotInitialValue;
                llMessageLinked(LINK_ALL_OTHERS, JACKPOT_SET, (string)jackpotPayout, NULL_KEY);
            }
            else
            {
                //Play sound for positive and negative amounts
                if (amount > 0)
                {
                    llPlaySound("CashRegister", 0.75);
                }
                else
                {
                    llPlaySound("Buzzer", 0.75);
                }
                currentPayout += amount;
            }

            //Kill Game if all are revealed
            payoutCount += 1;
            if (payoutCount >= 16)
            {
                state payout;
            }
            //Update display
            llMessageLinked(LINK_ALL_OTHERS, DISPLAY_POT, (string)currentPayout, NULL_KEY);
        }
        if (num == PAYOUT_BUTTON)
        {
            state payout;
        }
    }
    state_exit()
    {
        llSensorRemove();
    }
}
state payout
{
    on_rez(integer start_param)
    {
        llResetScript();
    }
    state_entry()
    {
        //Shutdown game
        llMessageLinked(LINK_ALL_OTHERS, GAME_DISABLED, "", NULL_KEY);

       //Payout Money
        if (currentPayout > 0)
        {
            //Customer Won!
            llPlaySound("Fanfare", 0.75);
            llSay(0, "You Won L$" + (string)currentPayout + "!");
            jackpotPayout += jackpotWinIncrement;
            llMessageLinked(LINK_ALL_OTHERS, JACKPOT_SET, (string)jackpotPayout, NULL_KEY);
            if (!demoMode)
            {
                //llGiveMoney(playerID, currentPayout);
            }
            moneyOut += currentPayout;
        }
        else
        {
            //Customer Lost
            llPlaySound("NoWin", 0.90);
            llSay(0, "Sorry, better luck next time...");
            jackpotPayout += jackpotLoseIncrement;
            llMessageLinked(LINK_ALL_OTHERS, JACKPOT_SET, (string)jackpotPayout, NULL_KEY);
            currentPayout = 0;
        }

        //Process Statistics
        if (jackpotPayout > highestJackpot)
        {
            highestJackpot = jackpotPayout;
        }
        if (currentPayout > highestPayout)
        {
            highestPayout = currentPayout;
            highestPayoutName = playerName;
        }

         //Display Winnings then reset
        llMessageLinked(LINK_ALL_OTHERS, DISPLAY_POT, (string)currentPayout, NULL_KEY);
        currentPayout = 0;

        //Reset
        setStats();
        state idledemo;
    }
}
```

## Settings Notecard

This is just a notecard with settings, this is not a script...

```lsl
#Skunk Money Settings Notecard
#All lines that begin with "#" are comments, and are ignored.
#Do not change the order of the settings in this card.

#Game Cost
#Cost to play the game in L$. Must be either 25 or 10 L$
#Note: this game is for amusement only.  This machine does not accept nor payout any real L$ or item of value.
10

#Payout Tightness Setting
#Select a Value between 0 and 7 (Other values will default to 4)
#0 is very Tight and 7 is very Loose.
#Higher values favor the player. Lower values favor the house.
#Refer to the Payout Table Notecard to see payout percentages determined through actual testing.
5

#Jackpot Odds
#% of the time to show jackpot tile, replacing the skunk. This setting will affect the average size of the Jackpot.
#Valid values are 0.005 to 0.5 (0.5% - 5%). Recommend setting to 0.02 (2%)
0.02

#Jackpot Initial Value
#Value of  Jackpot when reset or after win.
#Higher settings will increase the payback percentage slightly.
#Recommend setting to 2x the Game Cost
#Cannot be less than 10 L$
50

#Jackpot Increment on Win
#Amount  Jackpot is incremented upon a winning pot (<= L$0)
#Recommend setting to 0 for L$10 game and 1 for L$25 game
#Cannot be less than 0 L$
1

#Jackpot Increment on Lose
#Amount  Jackpot is incrmeneted upon a losing pot  (> L$0)
#Recommend setting to 2 for L$10 game and 5 for L$25 game
#Cannot be less than 1L$
5

#Max Loss
#Maximum amount of L$ money this machine will lose before shutting down.
#When owner clicks the machine, it will reset the max loss. An anti-hacking/anti-exploit preventative measure
#Cannot be less than L$500
750
```

## Game Tile Script

This is the script in each individual game tile on the screen...

```lsl
//Game Tile
//by Hank Ramos

//Constants
integer SEND_PLAYER_ID = 962214;
integer GAME_RUNNING   = 953365;
integer GAME_DISABLED  = 953366;
integer PAYOUT_SET     = 253340;
integer PAYOUT_SEND    = 358763;
integer SYSTEM_RESET   = 853324;
integer TILE_ALL_SET   = 122545;
integer ID_REQUEST     = 856621;
integer ID_SEND        = 856621;
integer TILE_RANDOMIZE = 721002;

//Settings
integer tileID = -1;
integer debugMode = FALSE;

//Variables
key     playerID;
integer payout;

debug(string debugMSG)
{
    if (debugMode)
    {
        llSay(0, debugMSG);
    }
}
revealTile(integer dim)
{
    if (dim)
    {
        llSetColor(<0.1,0.1,0.1>, 3);
    }
    else
    {
        llSetColor(<1,1,1>, 3);
    }
    if (payout == 0)
    {
        llSetTexture("Skunk", 3);
    }
    else if (payout == 999999999)
    {
        llSetTexture("XJackpot", 3);
    }
    else
    {
        if (payout > 0)
        {
            llSetTexture("SM+" + (string)payout, 3);
        }
        else
        {
            llSetTexture("SM" + (string)payout, 3);
        }
    }
}
default
{
    state_entry()
    {
       llSleep(llFrand(5));
       llMessageLinked(0, ID_REQUEST, "", NULL_KEY);
    }
    link_message(integer sender_num, integer num, string str, key id)
    {
        if (num == ID_SEND)
        {
            tileID = (integer)str;
            llSetTexture(llGetInventoryName(INVENTORY_TEXTURE, tileID), 1);
            state disabled;
        }
        if (num == SYSTEM_RESET)
        {
            llResetScript();
        }
    }
}
state enabled
{
    state_entry()
    {
        llSetColor(<1,1,1>, 3);
        llSetTexture("QuestionMarks", 3);
    }
    link_message(integer sender_num, integer num, string str, key id)
    {
        if (num == GAME_DISABLED)
        {
            revealTile(TRUE);
            state disabled;
        }
        if (num == SYSTEM_RESET)
        {
            llResetScript();
        }
        if (num == TILE_ALL_SET)
        {
            llSetTexture(str, 3);
        }
    }
    touch_start(integer total_number)
    {
        integer x;
        for (x=0; x < total_number; x += 1)
        {
            if (llDetectedKey(x) == playerID)
            {
                llMessageLinked(0, PAYOUT_SEND, (string)payout, NULL_KEY);
                revealTile(FALSE);
                state disabled;
            }
        }
    }
}
state disabled
{
    link_message(integer sender_num, integer num, string str, key id)
    {
        if (num == SEND_PLAYER_ID)
        {
            playerID = id;
            debug("receiving player ID: " + (string)id);
        }
        if (num == (PAYOUT_SET + tileID))
        {
             payout = (integer)str;
             debug("payout set to " + str);
        }
        if (num == TILE_RANDOMIZE)
        {
            llSetTexture("QuestionMarks", 3);
            llSetColor(<1,1,1>, 3);
            llSetTimerEvent(0.75 + llFrand(0.75));
        }
        if (num == GAME_RUNNING)
        {
            debug("game being enabled " + str);
            state enabled;
        }
        if (num == SYSTEM_RESET)
        {
            llResetScript();
        }
        if (num == GAME_DISABLED)
        {
            revealTile(TRUE);
            state disabled;
        }
        if (num == TILE_ALL_SET)
        {
            llSetTexture(str, 3);
        }
    }
    timer()
    {
        llSetTexture(llGetInventoryName(INVENTORY_TEXTURE, (integer)llFrand((float)llGetInventoryNumber(INVENTORY_TEXTURE))), 3);
    }
    state_exit()
    {
        llSetTimerEvent(0);
    }
}
```

## Cash Out Button

Just the script in that button...

```lsl
//Cash Out Button
//by Hank Ramos

//Constants
integer SEND_PLAYER_ID = 962214;
integer GAME_RUNNING   = 953365;
integer GAME_DISABLED  = 953366;
integer PAYOUT_SET     = 253340;
integer PAYOUT_SEND    = 358763;
integer SYSTEM_RESET   = 853324;
integer TILE_ALL_SET   = 122545;
integer PAYOUT_BUTTON  = 632587;

//Variables
key     playerID;

default
{
    state_entry()
    {
        llSetTexture("XJackpot", 1);
        state disabled;
    }
}
state enabled
{
    state_entry()
    {
        llSetColor(<1,0,0>, 3);
    }
    link_message(integer sender_num, integer num, string str, key id)
    {
        if (num == GAME_DISABLED)
        {
            state disabled;
        }
        if (num == SYSTEM_RESET)
        {
            llResetScript();
        }
    }
    touch_start(integer total_number)
    {
        integer x;
        for (x=0; x < total_number; x += 1)
        {
            if (llDetectedKey(x) == playerID)
            {
                llMessageLinked(LINK_ALL_OTHERS, PAYOUT_BUTTON, "", NULL_KEY);
            }
        }
    }
}
state disabled
{
    state_entry()
    {
        llSetColor(<0.4,0.4,0.4>, 3);
    }
    link_message(integer sender_num, integer num, string str, key id)
    {
        if (num == SEND_PLAYER_ID)
        {
            playerID = id;
        }
        if (num == SYSTEM_RESET)
        {
            llResetScript();
        }
        if (num == GAME_RUNNING)
        {
            state enabled;
        }
    }
}
```

## Price Display

The script in the price display...

```lsl
//Price Display
//by Hank Ramos

//Constants
integer DISPLAY_PRICE  = 6324419;
integer SET_STATS      = 8665329;
integer RETRIEVE_STATS = 8662211;

default
{
    link_message(integer sender_num, integer num, string str, key id)
    {
        if (num == DISPLAY_PRICE)
        {
            if (str == "-1")
            {
                llSetTexture("OutOfService", 3);
            }
            else if (str == "0")
            {
                llSetTexture("Free", 3);
            }
            else
            {
                llSetTexture("SM+" + str, 3);
            }
        }
        if (num == SET_STATS)
        {
            llSetObjectDesc(str);
        }
        if (num == RETRIEVE_STATS)
        {
            llMessageLinked(sender_num, RETRIEVE_STATS, llGetObjectDesc(), NULL_KEY);
        }
    }
}
```