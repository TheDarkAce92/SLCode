---
name: "llTransferLindenDollars"
category: "function"
type: "function"
language: "LSL"
description: 'Transfer amount of L$ money from script owner to destination avatar.

Returns a key used in a matching transaction_result event for the success or failure of the transfer. If the transaction is successful, this key will show in the transaction history.

If you aren't going to use the return value or'
signature: "key llTransferLindenDollars(key destination, integer amount)"
return_type: "key"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llTransferLindenDollars'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lltransferlindendollars"]
---

Transfer amount of L$ money from script owner to destination avatar.

Returns a key used in a matching transaction_result event for the success or failure of the transfer. If the transaction is successful, this key will show in the transaction history.

If you aren't going to use the return value or the resulting transaction_result event consider using llGiveMoney instead of this function.


## Signature

```lsl
key llTransferLindenDollars(key destination, integer amount);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `destination` | avatar UUID |
| `integer` | `amount` | number of L$, must be greater than zero, (amount > 0) |


## Return Value

Returns `key`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llTransferLindenDollars)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llTransferLindenDollars) — scraped 2026-03-18_

Transfer amount of L$ money from script owner to destination avatar.Returns a key used in a matching transaction_result event for the success or failure of the transfer. If the transaction is successful, this key will show in the transaction history.

## Caveats

| Permissions |
| --- |
| - Do not depend upon the auto-grant status of permissions. **Always** use the run_time_permissions event. - If the script lacks the permission PERMISSION_DEBIT, the script will shout an error on DEBUG_CHANNEL and the operation fails (but the script continues to run). - If PERMISSION_DEBIT is granted by anyone other than the owner, then when the function is called an error will be shouted on DEBUG_CHANNEL. - Once the PERMISSION_DEBIT permission is granted there is no way to revoke it except from inside the script (for example, with a new llRequestPermissions call) or the script is reset or deleted. |

- An object cannot pay another object.
- Objects deeded to groups cannot give money (the permission cannot be granted).
- Use is limited to 30 payments in a 30 second interval for all scripts owned by that resident on a region. Sustained overage will produce a script error and halt payments while the rate remains excessive. Historically, faster payments have failed intermittently.
- Once a script has the PERMISSION_DEBIT permission it can empty an account of L$.

  - Fraud & theft are both [Linden Lab](https://lindenlab.com) violations and crimes. Misuse this function and you risk being banned and legal action. In addition LL may freeze the accounts of anyone the money is transferred to and restore it to it's rightful owners. This may involve retrieving it from third party exchanges and accounts on those exchanges being frozen. The system is not designed to be friendly towards fraud.

## Examples

```lsl
// Pay 100 L$ to Fred Bloggs when he touches this prim
// Die if the transfer of funds was successful, else keep running

string  Recipient = "Fred Bloggs";      // Authorised recipient
integer Amount = 100;                   // Amount to pay Fred when he touches the prim

integer DebitPerms;
key     TransactionID=NULL_KEY;

default
{
    state_entry()
    {
        // Ask the owner for permission to debit their account
        llRequestPermissions(llGetOwner(), PERMISSION_DEBIT);
    }

    run_time_permissions (integer perm)
    {
        if  (perm & PERMISSION_DEBIT)
            DebitPerms = TRUE;
    }

    touch_start(integer num_detected)
    {
        if (!DebitPerms)
            return;  // Cannot proceed - debit permissions not granted
        if (llDetectedName(0) != Recipient)
            return;  // unauthorised person is touching - ignore
        if (TransactionID != NULL_KEY)
            return;  // waiting on previous transaction to complete/fail

        key id = llDetectedKey(0);
        TransactionID = llTransferLindenDollars(id, Amount);
    }

    transaction_result(key id, integer success, string data)
    {
        if (id != TransactionID)
            return;          // Ignore if not the expected transaction

        if (success)
        {
            llOwnerSay( "Transfer of L$ to " + Recipient + " was successful");
            llSleep(1.0);
            llDie();          // Die so Fred can't keep taking money
        }
        else
        {
            llOwnerSay( "Transfer of L$ failed");
            TransactionID = NULL_KEY;
            // Keep the script running so Fred can try again, clear TransactionID to allow a new attempt
        }
    }
}
```

### Complex Examples

- Simple Piggy Bank

## Notes

- released on main server channel on 3-Dec-2011

## See Also

### Events

- **run_time_permissions** — Permission receiving event
- transaction_result
- money

### Functions

- **llGetPermissions** — Get the permissions granted
- **llGetPermissionsKey** — Get the agent who granted permissions
- **llRequestPermissions** — Request permissions
- llGiveMoney
- llSetPayPrice

### Articles

- Script permissions

<!-- /wiki-source -->
