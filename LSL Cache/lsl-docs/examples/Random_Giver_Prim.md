---
name: "Random Giver Prim"
category: "example"
type: "example"
language: "LSL"
description: "This prim will randomly choose an item from inside its contents and present users with multiple randomized ways of getting that item. the item is never shown and is completely hidden from the users. guess right or match up and win."
wiki_url: "https://wiki.secondlife.com/wiki/Random_Giver_Prim"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

This prim will randomly choose an item from inside its contents and present users with multiple randomized ways of getting that item. the item is never shown and is completely hidden from the users. guess right or match up and win.

```lsl
//*THE ADVANCE MYSTERY PRIM IS A RANDOM GAME/GIVER SCRIPT WRITTEN BY DAMIAN DARKWYR.*//

//*NOTECARD STUFFS*//
string note = "_config";//the name of the notecard we will fetch our setting from.
key read;//we need this to read the notecard
integer line = 0;//which line of the notecard we are reading

dodata(string data)//function to read the data card
{
    list break = llParseString2List(data,["="],[]);//break the string on the line into a list so we can use it
    string a1a = llList2String(break,0);//eveything before the =
    string b2b = llList2String(break,1);//everything after the =
    if(a1a == "use_random_number")
    {
        use_random_number = (integer)b2b;
    }else if(a1a == "use_random_letter")
    {
        use_random_letter = (integer)b2b;
    }else if(a1a == "use_random_sequence")
    {
        use_random_sequence = (integer)b2b;
    }else if(a1a == "use_numerology")
    {
        use_numerology = (integer)b2b;
    }else if(a1a == "use_channel_output")
    {
        use_channel_output = (integer)b2b;
    }else if(a1a == "channel")
    {
        channel = (integer)b2b;
    }else if(a1a == "use_notify_owner")
    {
        use_notify_owner = (integer)b2b;
    }else if(a1a == "time_reset_minutes")
    {
        time_reset_minutes = (integer)b2b;
    }else if(a1a == "amount_per_guess")
    {
        amount_per_guess = (integer)b2b;
    }
}
//*NOTECARD STUFFS*//

dotouch(key id)//function for when someone touches this prim
{
    integer winner = 0;//we currently do not have a winner
    string out = "\n";//text output for user
    if(use_random_letter==1)//if we are using the random letter game
    {
        if(llToUpper(llGetSubString(llKey2Name(id),0,0))==name || llToUpper(llGetSubString(llKey2Name(id),-1,-1))==name)
        {//if the person who touched this prim has a first name that starts with the random letter or a last name that ends with the random letter we have a winner
            winner = 1;
        }else
        {
            out += "your name does not start with or end with "+name+"\n";
        }
    }

    if(use_random_sequence==1)//if we are using the random sequence game
    {//if the person who touched this prim has a name that contains the random sequence of letters we have a winner.
        if(llSubStringIndex(llToUpper(llKey2Name(id)),castcount)!=-1)
        {
            winner = 1;
        }else
        {
            out += "your name does not contain "+castcount+"\n";
        }
    }

    if(use_numerology==1)//if we are using teh random numerology game
    {//if the person who touched this prims name adds up numerologically to the random number we chose we have a winner.
        if(get_numerics(llToLower(llKey2Name(id))) == numericnumber)
        {
            winner = 1;
        }else
        {
            out += "your numerology number is "+(string)get_numerics(llToLower(llKey2Name(id)))+" not "+(string)numericnumber+"\n";
        }
    }
    if(winner == 1)//if we have a winner
    {
        llSay(0,"CONGRATZ!!!!!!!!!!! YOU WIN");//tell the world
        payout(id);//give out the prize
        if(1==1)state get_rand;//refresh our credentials
    }else//if not tell the user they didnt win and why
    {
        if(use_random_number)
        {
            out += "if you still want this prize you can always pay me "+(string)amount_per_guess+"L and try to guess my hidden number.";
        }
        llSay(0,"sorry but\n"+out);
    }
}

integer use_random_number = 1;//do we want to use random number guessing game?
integer use_random_letter = 1;//do we want to use the random letter lucky chair type game?
integer use_random_sequence = 1;//do we want to use the random sequence of characters?
integer use_numerology = 1;//do we want to use numerology to pick winners?
integer use_channel_output = 1;//do we want to shout on channels when someone wins a prize?
integer channel = -999;//the channel we will shout on IF we are shouting on channels
integer use_notify_owner = 1;//do we want to tell our owner when we give out prizes?
integer time_reset_minutes = 15;//how often do we need to reset and pick new random credentials?
integer amount_per_guess = 1;//how much money does it cost per guess for the random number guessing game?

dorandletter()//function to pick a random character
{
    integer purely_random = 0;
    integer i = 0;
    if(use_random_letter == 1)
    {
        do{
            llSetText("PICKING A RANDOM LETTER....\n["+llGetSubString(charmap,purely_random,purely_random)+"]",<1,1,1>,1);
            purely_random = llFloor(llFrand(llStringLength(charmap)));
            i++;
        }while(i < 100);
        name = llGetSubString(charmap,purely_random,purely_random);
    }
}
dorandsequence()//function to pick a random sequence of characters.
{
    integer purely_random = 0;
    integer i = 0;
    if(use_random_sequence == 1)
    {
        i=0;
        castcount = "";
        purely_random=0;
        do{
            llSetText("PICKING A CHAR SEQUENCE ",<1,1,1>,1);
            purely_random = llFloor(llFrand(llStringLength(charmap)));
            castcount += llGetSubString(charmap,purely_random,purely_random);
            i++;
        }while(i<3);
    }
}
dorandomnumber()//function to pick a random number 0 - 100
{
    integer purely_random = 0;
    integer i = 0;
    if(use_random_number == 1)
    {
        llSetPayPrice(PAY_HIDE,[amount_per_guess,PAY_HIDE,PAY_HIDE,PAY_HIDE]);
        i=0;
        do{
            llSetText("PICKING A RANDOM GUESSING NUMBER \n["+(string)llFloor(llFrand(100))+"]",<1,1,1>,1);
            randomnumber = llFloor(llFrand(100));
            i++;
        }while(i < 100);
    }else
    {
        llSetPayPrice(PAY_HIDE,[PAY_HIDE,PAY_HIDE,PAY_HIDE,PAY_HIDE]);
    }
}
dorandomnumerology()//function to pick a random number 0-9 for the numerology game
{
    integer purely_random = 0;
    integer i = 0;
    if(use_numerology == 1)
    {
        i=0;
        do{
            llSetText("PICKING A RANDOM NUMEROLOGY NUMBER \n["+(string)llFloor(llFrand(llGetListLength(numbers)))+"]",<1,1,1>,1);
            numericnumber = llFloor(llFrand(llGetListLength(numbers)));
            i++;
        }while(i < 100);
    }
}
dorandominventory()//function to pick a random inventory item to give out.
{
    integer purely_random = 0;
    integer i = 0;
    do{
        purely_random = llFloor(llFrand(llGetInventoryNumber(INVENTORY_ALL)));
        string n = llGetInventoryName(INVENTORY_ALL,purely_random);
        if(n!=llGetScriptName() && n!="_config")
        {
            llSetText("PICKING A RANDOM ITEM \n["+n+"]",<1,1,1>,1);
            item = n;
        }
        i++;
    }while(i < 100);
}
string name;//the letter we have picked at random
string castcount;//the sequence of letters we picked at random
string item;//the random inventory item we are giving away
integer randomnumber;//the random number we picked for the guessing game
integer numericnumber;//the randomly picked numerology number
integer lis;//listen even handler
integer chan = 0;//channel to listen on for user input on the guessing game
key listenid;//the user who paid us to play the guessing game we need to listen to that person only
string charmap = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";//list of characters in the form of a string. i like this.
list numbers = [0,1,2,3,4,5,6,7,8,9];//list of numerology numbers
list letters = ["aku","blv","cmw","dnx","eoy","fpz","gq","hr","is","jt"];//list of numerologically ordered letters. numbers get converted to teh actuall number later
random_contains()//fetch all our randomness
{
    dorandletter();//get the letter
    dorandsequence();//get the letters
    dorandomnumber();//get teh number
    dorandomnumerology();//get the mystical stuff
    dorandominventory();//grab an item
    string sep = "\n";
    string line1 = "If your Name Starts OR Ends with the Letter "+name;
    string line2 = "Or your name contains the partial phrase "+castcount;
    string line3 = "OR if your numerology number for your avatar matches "+(string)numericnumber;
    string line4 = "Touch me for the Mystery Prize inside.";
    string line5 = "OR pay me "+(string)amount_per_guess+"L and guess my random number.\nhint it is between 0 and 100";
    string out;
    if(use_random_letter == 1)
    {
        out += line1+sep;
    }
    if(use_random_sequence == 1)
    {
        out += line2+sep;
    }
    if(use_numerology == 1)
    {
        out += line3+sep;
    }
    out += line4+sep;
    if(use_random_number == 1)
    {
        out += line5;
    }
    //create teh text and float it
    llSetText(out,<1,1,1>,1);
}
relis()//function to remove and reset a listener for chat
{
    llListenRemove(lis);
    lis = llListen(chan,"","","");
}
payout(key id)//function to give out the item to the winner.
{
    llParticleSystem([
    PSYS_PART_FLAGS, 0 | PSYS_PART_EMISSIVE_MASK |
    PSYS_PART_INTERP_COLOR_MASK | PSYS_PART_INTERP_SCALE_MASK |
    PSYS_PART_FOLLOW_SRC_MASK | PSYS_PART_FOLLOW_VELOCITY_MASK,
    PSYS_SRC_PATTERN,PSYS_SRC_PATTERN_EXPLODE,
    PSYS_PART_MAX_AGE,10.0,
    PSYS_PART_START_COLOR,<1.00,1.00,1.00>,
    PSYS_PART_END_COLOR,<0.15,0.15,0.15>,
    PSYS_PART_START_SCALE,<0.04,0.04,0.04>,
    PSYS_PART_END_SCALE,<1.11,1.11,1.11>,
    PSYS_SRC_BURST_RATE,0.01,
    PSYS_SRC_ACCEL,<0.0,0.0,0.0>,
    PSYS_SRC_BURST_PART_COUNT,9000,
    PSYS_SRC_BURST_RADIUS,0.0,
    PSYS_SRC_BURST_SPEED_MIN,1.0,
    PSYS_SRC_BURST_SPEED_MAX,1.0,
    PSYS_SRC_TARGET_KEY,(key)"",
    PSYS_SRC_INNERANGLE,1.55,
    PSYS_SRC_OUTERANGLE,1.54,
    PSYS_SRC_OMEGA,<2,2,2>,
    PSYS_SRC_MAX_AGE,10.0,
    PSYS_SRC_TEXTURE,"11f44bae-9a98-5ede-102e-26b3910d4062",//diamond texture use it for otehr stuff if ya want
    PSYS_PART_START_ALPHA,1.0,
    PSYS_PART_END_ALPHA,0.0
    ]);//do the big ole particle explosion full of diamonds
    llGiveInventory(id,item);//give the item to the winner
    llSleep(3.0);//take a short break
    llParticleSystem([]);//kill the particles
    if(use_channel_output == 1)//if we are allowed to talk on channels do that now
    {
        llSay(channel,"MYSTERY_PAYOUT|"+(string)id);
    }

    if(use_notify_owner)//if we are allowed to tell our owner about the winner do that now
    {
        llInstantMessage(llGetOwner(),"gave "+item+" to "+llKey2Name(id));
    }
}
integer get_numerics(string name)//function to convert a name to a number numerologically
{
    //this is based on the 0-9 setup
    //0123456789
    //abcdefghij
    //klmnopqrst
    //uvwxyz
    integer your_number;
    integer i = 0;
    do
    {
        string l = llGetSubString(name,i,i);
        integer x = 0;
        while(x < llGetListLength(letters))
        {
            integer ficl = llSubStringIndex(llList2String(letters,x),l);
            if(ficl != -1)
            {
                your_number = your_number + llList2Integer(numbers,x);
            }else
            {
                your_number = your_number + (integer)l;
            }
            x++;
        }
        //llOwnerSay("yournum:"+(string)your_number);
        i++;
    }while(i 1)
    {
        integer trueout = 0;
        integer a = 0;
        do
        {
            trueout = trueout + (integer)llGetSubString((string)your_number,a,a);
            a++;
        }while(a < llStringLength((string)your_number));
        your_number = 0;
        your_number = your_number + trueout;
        //llOwnerSay("yournum:"+(string)your_number);
    }else
    {
        jump done;
    }
    jump makesingle;
    @done;
    return your_number;
}

//*Color Gradient code from Eric Quine's Color Shifter v4.5 with light script*//
vector color = <1, 0, 0>;
float colorStep = 0.03;
getNextColor()
{
    // red -> yellow
    if (color.x >= 1 && color.y < 1 && color.z <= 0) {
        color.y += colorStep;
    }
    // yellow -> green
    else if (color.x > 0 && color.y >= 1 && color.z <= 0) {
        color.x -= colorStep;
    }
    // green -> cyon
    else if (color.x <= 0 && color.y >= 1 && color.z < 1) {
        color.z += colorStep;
    }
    // cyan -> blue
    else if (color.x <= 0 && color.y > 0 && color.z >= 1) {
        color.y -= colorStep;
    }
    // blue -> violet
    else if (color.x < 1 && color.y <= 0 && color.z >= 1) {
        color.x += colorStep;
    }
    // violet -> red
    else if (color.x >= 1 && color.y <= 0 && color.z > 0) {
        color.z -= colorStep;
    }
}
//*Color Gradient code from Eric Quine's Color Shifter v4.5 with light script*//
default
{
    on_rez(integer sp)
    {
        llResetScript();
    }
    changed(integer c)
    {
        if(c & CHANGED_INVENTORY)
        {
            llResetScript();
        }
    }
    state_entry()
    {
        llSetTexture("75514350-0a83-9207-a6ce-9e4d174b10b9",ALL_SIDES);//? texture mysterious ooooooo lol this is a question mark texture that is the default myster prim texture. you can change that here if you like
        llSetText("CONFIGURING MYSTERY SYSTEM...",<1,1,1>,1);
        line = 0;
        read = llGetNotecardLine(note,line);
    }
    dataserver(key id,string data)
    {
        if(id == read)
        {
            if(data != EOF)
            {
                if(llGetSubString(data,0,0)!="#" && llGetSubString(data,0,1)!="//" && data != "" && data!=" ")
                {
                    dodata(data);
                }
                read = llGetNotecardLine(note,++line);
            }else
            {
                state get_rand;
            }
        }
    }
}
state get_rand
{
    on_rez(integer sp)
    {
        llResetScript();
    }
    changed(integer c)
    {
        if(c & CHANGED_INVENTORY)
        {
            llResetScript();
        }
    }
    state_entry()
    {
        llListenRemove(lis);
        random_contains();
        state running;
    }
}
state running
{
    on_rez(integer sp)
    {
        llResetScript();
    }
    changed(integer c)
    {
        if(c & CHANGED_INVENTORY)
        {
            llResetScript();
        }
    }
    state_entry()
    {
        llResetTime();
        llSetTimerEvent(1.0);
    }
    money(key id,integer amount)
    {
        llSay(0,"type your guess in chat and lets see if you win!!!! good luck.");
        listenid = id;
        relis();
    }
    listen(integer c,string n,key id,string m)
    {
        if(id == listenid)
        {
            if(m == (string)randomnumber)
            {
                llSay(0,"CONGRATZ!!!!!!!!!!! YOU WIN");
                payout(id);
                state get_rand;
            }else
            {
                //this is to help the player guess the number. over under and what not so they can guess again and try to get closer to the real number
                string outout = "";
                integer in = (integer)m;
                if(in > randomnumber)outout = "OVER";
                else if(in < randomnumber)outout = "UNDER";
                llSay(0,"SORRY, THAT'S NOT MY NUMBER. TRY AGAIN IF YOU WANT. YOUR NUMBER WAS "+outout+" MY NUMBER");
                llListenRemove(lis);
            }
        }
    }
    timer()
    {
        float time = llGetTime();
        if((integer)time % (60*time_reset_minutes) == 0)
        {
            state get_rand;
        }else if((integer)time % 1 == 0)
        {
            getNextColor();
            llSetColor(color, ALL_SIDES);//this uses Eric Quine's Color Shifter
        }
    }
    touch_start(integer total_number)
    {
        dotouch(llDetectedKey(0));
    }
}
```



and for the notecard. name the note card _config and add....

use_random_number=1
use_random_letter=1
use_random_sequence=1
use_numerology=1
use_channel_output=1
channel=-999
use_notify_owner=1
time_reset_minutes=5
amount_per_guess=1