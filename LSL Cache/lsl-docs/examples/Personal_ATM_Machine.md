---
name: "Personal ATM Machine"
category: "example"
type: "example"
language: "LSL"
description: "I made this script to allow me to store my Lindens in another account, in order to stop me from spending them so carelessly. Others may find it useful."
wiki_url: "https://wiki.secondlife.com/wiki/Personal_ATM_Machine"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

I made this script to allow me to store my Lindens in another account, in order to stop me from spending them so carelessly. Others may find it useful.

```lsl
// ATM Machine script, Jessikiti Nikitin 2010
//
// Brief instructions for use:
//
// Give this script to your alt, ensuring their balance is L$0 (or setting the balance in the variable below),
// put it in an object and then allow debit permissions when the object requests them.
//
// You can then manage your alt's balance using the object, without the alt having to be logged in.
// To deposit lindens, pay the object. To withdraw lindens, touch the object for a menu.

key managerKey = "00000000-0000-0000-0000-000000000000"; // change this to your main avatar's key

list dialogAmounts = ["50", "100", "250", "500", "1000", "5000", "10000", "50000", "All"];
integer balance = 0;

integer opChannel;
integer listenHandle;

presentDialog()
{
    opChannel = llFloor((llFrand(1000000) * -1)-1000000);   // creates random operation channel to
                                                            // prevent spying on withdrawal amounts
    listenHandle = llListen(opChannel, "", managerKey, "");
    llSetTimerEvent(60);
    llDialog(managerKey, "Balance: L$"+(string)balance+"\n \nChoose amount to withdraw.", validAmounts(), opChannel);
}

list validAmounts()
{
    // this function prevents the script offering money that isn't available,
    // which would result in a silent failure
    list va;
    integer i;
    for(;i