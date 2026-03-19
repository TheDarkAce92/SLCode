---
name: "Speed Tester"
category: "example"
type: "example"
language: "LSL"
description: "The following script is used for testing the speed of LSL snippets. The script was written in LSLEditor. The script should work fine in both mono & LSO."
wiki_url: "https://wiki.secondlife.com/wiki/Speed_Tester"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 Description
- 2 Creator
- 3 Contributors
- 4 License
- 5 Disclaimer
- 6 Directions
- 7 Speed Tester.lsl
- 8 Sample Output
- 9 Other

Description

The following script is used for testing the speed of LSL snippets. The script was written in LSLEditor. The script should work fine in both mono & LSO.

Creator

- Bobbyb30 Swashbuckler

Contributors

Add yourself here if you change this script.

License

This script is released into Public Domain.

Disclaimer

These programs are distributed in the hope that it will be useful, but **WITHOUT ANY WARRANTY**; without even the implied warranty of **MERCHANTABILITY** or **FITNESS FOR A PARTICULAR PURPOSE**.

Directions

Go to an empty/script free private sim and detach any of your scripted attatchments. Create an object and place this script inside. Modify the "test()" and "clearvariables()" with whatever code it is that you want to test. Set the number of trials, the testcounter, and the test name. Save the script. Touch the object to begin the test. (If the script takes too long, reset).

The script provides min, max, avg, median, total time, and standard deviation.

You may need to run multiple trials as the script as all of SL is not always accurate/predictabl

Speed Tester.lsl

```lsl
//***********************************************************************************************************
//                                                                                                          *
//                                            --Speed Tester--                                              *
//                                                                                                          *
//***********************************************************************************************************
// www.lsleditor.org  by Alphons van der Heijden (SL: Alphons Jano)
//Creator: Bobbyb30 Swashbuckler
//Attribution: none
//Created: December 1, 2008
//Last Modified:  March 19, 2010
//Released: Wed, March 17, 2010
//License: Public Domain
//Status: Fully Working/Production Ready
//Version: 1.2.1
//LSLWiki: https://wiki.secondlife.com/wiki/Speed_Tester

//Name: Speed Tester.lsl
//Purpose: To test the speed of certain LSL snippets.
//Technical Overview: Uses 2 loops, one for trials, one for the test counter
//Directions: This is meant to be used by scripters, it should be easy to use. Modify the test() with your snippet, and touch to begin the test.

//Compatible: Mono & LSL compatible
//Other items required: None
//Notes: If it takes too long, simply reset.
//       Do the test in an empty region, with as few script as possible to prevent contamination. (Make sure you aren't
//       wearing scripted attatchments).
//       This test is not 100% accurate, but it should give you a good idea as to whether or not something is faster.
//       Anymore than 50 trials may not get printed out in the csv due to charactar limit.
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


//User modifiable variables
integer trials = 20;//how many trials to conduct
integer testcounter = 200000;//how many times to conduct the test
string testname = "speed";//what to call your test, optional
integer discardfirsttrial = FALSE;//whether or not to discard the first trial...this can be slower as the script is loaded into the VM for the 1st time following a save

////
//declare any of your global variables here
integer x;

test()//in here goes the test
{
    ++x;
}

//insert the variables you want to clear after each trial
clearvariables()
{
    x = 0;
}

//which variables to use(but not reset) for the duration of all trials.
initializevariables()
{

}
///////////////////////////////////////////////////////////////////////////////////////

//do not modify below
//////////////////////////
//global variables...do not modify, except to change whether or not to round
list times;//the list of times, do not modify this one

default
{
    state_entry()
    {
        llOwnerSay("Speed Tester.lsl' released into Public Domain by Bobbyb30 Swashbuckler (C) 2009");
        initializevariables();
        if(llStringTrim(testname,STRING_TRIM) != "")//if testname isn't empty, print out test name
            llOwnerSay("Touch to begin the '" + testname + "' test.");
    }

    touch_start(integer total_number)
    {
        //print out the headers
        llOwnerSay("\n \n=================================================================================");//break
        if(llStringTrim(testname,STRING_TRIM) != "")//if testname isn't empty, print out test name
            llOwnerSay("Running the '" + testname + "' test in Region: " + (string)llGetRegionName());
        else
            llOwnerSay("Running the test.");

        llOwnerSay("Start Time:" + llGetTimestamp());

        times = [];//reset the times


        ///////
        //the actual test loop
        integer counter;
        integer trialscounter;

        do//the trial loop
        {

            clearvariables();//clear user variables before each test
            counter = 0;//reset counter for testcounter before each trial
            llResetTime();//Reset time before each trial
            do//the test counter loop
            {
                test();//the test to perform
            }while(++counter < testcounter);//the test counter loop
            times += (llGetTime()/testcounter);//add the trial time to the list
            //above you can determine whether to add llRound, (integer) before llGetTime(), or leave as float for more accuracy


        }while(++trialscounter < trials);//the trial loop
        /////////////

        if(discardfirsttrial)//whether or not to delete the first trial
        {
            times = llDeleteSubList(times,0,0);//delete from list
            --trials;//one less trial
        }

        llOwnerSay("---------");
        llOwnerSay("Test: " + testname + " Complete.");
        llOwnerSay("Number of trials: " + (string)trials);
        if(discardfirsttrial)//whether or not to delete the first trial
            llOwnerSay("...First trial was deleted.");
        llOwnerSay("Testcounter: " + (string)testcounter);
        llOwnerSay("Trial times: " + llList2CSV(times));
        llOwnerSay("----------");

        //print out results
        llOwnerSay("End Time:" + llGetTimestamp());
        llOwnerSay("Total test time: " + (string)(llListStatistics(LIST_STAT_SUM,times) * testcounter) + " seconds.");
        llOwnerSay("Min: " + (string)llListStatistics(LIST_STAT_MIN,times));//minimum time
        llOwnerSay("Avg: " + (string)llListStatistics(LIST_STAT_MEAN,times));//average time
        llOwnerSay("Median: " + (string)llListStatistics(LIST_STAT_MEDIAN,times));//median time
        llOwnerSay("Max: " + (string)llListStatistics(LIST_STAT_MAX,times));//maximum time
        llOwnerSay("Range: " + (string)llListStatistics(LIST_STAT_RANGE,times));//average time
        llOwnerSay("Standard Deviation official: " + (string)llListStatistics(LIST_STAT_STD_DEV,times));//average time
        if(llStringTrim(testname,STRING_TRIM) != "")//if testname isn't empty, print out test name
            llOwnerSay("END OF '"+ testname + "' TEST");
        else
            llOwnerSay("END OF TEST");
        llOwnerSay("=========================================================================");
    }
}
```

Sample Output

```lsl
[11:05]  Object:

=================================================================================
[11:05]  Object: Running the 'speed' test in Region: Sandbox Admicile
[11:05]  Object: Start Time:2010-03-18T18:05:23.087809Z
[11:06]  Object: ---------
[11:06]  Object: Test: speed Complete.
[11:06]  Object: Number of trials: 20
[11:06]  Object: Testcounter: 200000
[11:06]  Object: Trial times: 0.000017, 0.000014, 0.000014, 0.000014, 0.000014, 0.000014, 0.000014, 0.000014, 0.000014, 0.000014, 0.000014, 0.000014, 0.000015, 0.000014, 0.000014, 0.000015, 0.000014, 0.000014, 0.000014, 0.000014
[11:06]  Object: ----------
[11:06]  Object: End Time:2010-03-18T18:06:20.075339Z
[11:06]  Object: Total test time: 56.965070 seconds.
[11:06]  Object: Min: 0.000014
[11:06]  Object: Avg: 0.000014
[11:06]  Object: Median: 0.000014
[11:06]  Object: Max: 0.000017
[11:06]  Object: Range: 0.000003
[11:06]  Object: Standard Deviation: 0.000001
[11:06]  Object: END OF 'speed' TEST
[11:06]  Object: =========================================================================
```

Other

If you find this script of use, please do let me know=D.