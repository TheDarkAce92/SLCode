---
name: "transaction_result"
category: "event"
type: "event"
language: "LSL"
description: "Triggered when task receives asynchronous data"
signature: "transaction_result(key id, integer  success, string data)"
wiki_url: 'https://wiki.secondlife.com/wiki/transaction_result'
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
deprecated: "false"
parameters: []
---

Triggered when task receives asynchronous data


## Signature

```lsl
transaction_result(key id, integer  success, string data)
{
    // your code here
}
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `id` | matches the return of the llTransfer* function |
| `integer ` | `success` | TRUE if the transfer succeeded otherwise FALSE. |
| `string` | `data` | On successful transactions this will contain a CSV of information pertaining to the transaction. In failure, a string will be returned matching one of the error tags below. |


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/transaction_result)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/transaction_result) — scraped 2026-03-18_

## Examples

```lsl
/*
* A simple piggy bank, anyone can pay in money and anyone can click it to get money out.
*
* TO DO:
*  - handle different errors differently based upon CSV output
*
* original by Strife Onizuka
*
* modified by Kireji Haiku:
*  - because weird things happen in LSL when using more than one state
*  - one should say thanks when being payed
*  - added 0 L$ payment when bank is empty, to show failed payment notifications
*  - added target UUID and L$ amount into transaction history, too
*
* Note from Traven Sachs (VWR-28201):
* In testing this script using an account with no funds - it has been noted that when the INSUFFICIENT FUNDS
* error occurs on Transaction Results that the Display of L$ on the account attempting to transfer funds will
* read as -1 on some viewers, even if the account has funds less than the transaction amount available to it.
* (i.e. if account has 7L and attempts to pay 10L the viewer display will read -1 L until the next L$ transaction
* occurs that is actually valid.  Don't know if this is a viewer glitch or back end glitch but felt it should
* be mentioned.)
*/

integer hasBeenGrantedDebitPerms;

integer amountGivenAwayOnClick;
integer totalLindenDollarsInBank;

list listOfTransactionRecords;

update_floattext()
{
    string floattext = "I have no L$ to give away :(";

    if (amountGivenAwayOnClick <= totalLindenDollarsInBank
        && hasBeenGrantedDebitPerms)
    {
        floattext = "I have L$ "+ (string)totalLindenDollarsInBank + " to give away!";
    }

    llSetText(floattext, <1.0, 1.0, 1.0>, (float)TRUE);
}

default
{
    on_rez(integer start_param)
    {
        llResetScript();
    }


    changed(integer change)
    {
        if (change & CHANGED_OWNER)
            llResetScript();
    }

    state_entry()
    {
        // how much money to give away each time?

        amountGivenAwayOnClick = 10;

        // how much money do we initially "have" in the bank?

        totalLindenDollarsInBank = 50;

        update_floattext();

        // request permissions to give away money, otherwise this won't work

        key owner = llGetOwner();
        llRequestPermissions(owner, PERMISSION_DEBIT);
    }

    touch_start(integer num_detected)
    {
        // if the script has been granted debit permissions
        if (hasBeenGrantedDebitPerms)
        {
            key id = llDetectedKey(0);

            // if we have at least as much money in the bank as we would be giving away
            if (amountGivenAwayOnClick <= totalLindenDollarsInBank)
            {
                // we add the transaction ID, the target avatar UUID and the L$ amount to a list
                listOfTransactionRecords += [llTransferLindenDollars(id, amountGivenAwayOnClick), id, amountGivenAwayOnClick];

                // we take the money from the bank
                totalLindenDollarsInBank -= amountGivenAwayOnClick;
            }
            else
            {
                // will not work, cause paying 0 L$!
                // will send a "failed payment" notification!
                // only for DEMO purposes, usually you should do something like:
                // llSay(PUBLIC_CHANNEL, "Sorry, no money in the bank!");
                // instead !!!

                listOfTransactionRecords += [llTransferLindenDollars(id, 0), id, 0];
            }
        }

        update_floattext();
    }

    money(key id, integer amount)
    {
        // someone payed the bank!

        totalLindenDollarsInBank += amount;

        // be nice, say thanks
        llInstantMessage(id, "Thanks a bunch!");

        update_floattext();
    }

    transaction_result(key id, integer success, string data)
    {
        integer index = llListFindList(listOfTransactionRecords, [id]);

        //if the ID was found in our list
        if (~index)
        {
            // if payment failed, give notice
            if (!success)
            {
                key targetUUID = llList2Key(listOfTransactionRecords, index + 1);
                integer amountNotPayed = llList2Integer(listOfTransactionRecords, index + 2);

                llSay(PUBLIC_CHANNEL, "\n \nSorry, somehow the transaction has failed!"
                    + "\ntransaction ID: " + (string)id
                    + "\ntarget UUID: " + (string)targetUUID
                    + "\namount not payed: " + (string)amountNotPayed
                    + "\nfailure reason: " + data);

                // if the amount that wasn't payed is more than 0 L$, put the money back into the bank
                if (amountNotPayed)
                    totalLindenDollarsInBank += amountNotPayed;
            }

            // remove the entry again [transaction ID, target UUID, L$ amount]
            listOfTransactionRecords = llDeleteSubList(listOfTransactionRecords, index, index + 2);
        }

        // total amount could have changed again...
        update_floattext();
    }

    run_time_permissions (integer perm)
    {
        // when owner granted debit perms, enable piggy bank functionality
        if(perm & PERMISSION_DEBIT)
            hasBeenGrantedDebitPerms = TRUE;

        update_floattext();
    }
}
```

<!-- /wiki-source -->
