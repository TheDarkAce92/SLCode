---
name: "money"
category: "event"
type: "event"
language: "LSL"
description: "Fires when an avatar pays the object using the Pay button"
wiki_url: "https://wiki.secondlife.com/wiki/Money"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "money(key giver, integer amount)"
parameters:
  - name: "giver"
    type: "key"
    description: "UUID of the avatar who paid"
  - name: "amount"
    type: "integer"
    description: "Amount of Linden dollars paid"
deprecated: "false"
---

# money

```lsl
money(key giver, integer amount)
{
    llOwnerSay(llKey2Name(giver) + " paid L$" + (string)amount);
}
```

Fires when an avatar pays the object. Requires the object's Pay button to be enabled (`llSetPayPrice`).

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `giver` | key | UUID of paying avatar |
| `amount` | integer | Linden dollars paid |

## Notes

- The object receives the money — the script does not need `PERMISSION_DEBIT` to receive payments.
- Use `llSetPayPrice` to configure the pay dialog.
- Use `PERMISSION_DEBIT` only if the script needs to *send* money.

## Example

```lsl
integer PRICE = 100;

default
{
    state_entry()
    {
        llSetPayPrice(PRICE, [PRICE, PAY_HIDE, PAY_HIDE, PAY_HIDE]);
    }

    money(key giver, integer amount)
    {
        if (amount >= PRICE)
        {
            llGiveInventory(giver, "Product");
            llOwnerSay("Sold to " + llKey2Name(giver));
        }
        else
        {
            llGiveMoney(giver, amount);  // refund (requires PERMISSION_DEBIT)
            llOwnerSay("Payment too small — refunded");
        }
    }
}
```

## See Also

- `llSetPayPrice` — configure pay button options
- `llGiveMoney` — send money (requires PERMISSION_DEBIT)
- `llGiveInventory` — give item to avatar
- `PERMISSION_DEBIT` — permission to debit L$


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/money) — scraped 2026-03-18_

## Caveats

- This event cannot be triggered by a call to llGiveMoney because llGiveMoney cannot be used by one object to pay another object.
- Money cannot be paid to an attachment.
- **Money() does not check if it is running on the Testing Grid!** If you are writing a vendor that does networking, be sure to check that it was not payed aditi grid by doing `if(llSubStringIndex(llGetEnv("simulator_hostname"), ".aditi.") == -1)` or by checking if llHTTPRequest's `X-SecondLife-Shard` header does not equal "Testing".

## Examples

This example shows the simplest tip-jar and shows how little code is needed to receive unverified amounts of money.

```lsl
default
{
    money(key id, integer amount)      // Some money has been received (and has been paid into the owner's account)
    {
        // Thank the giver for their tip
        llInstantMessage(id, "Thanks for the L$"  + (string) amount + " tip!");
    }
}
```

Next level of tip jar, advising owner, keeping a running total, and with floating text to show status.

```lsl
integer Total;
string  OwnerName;

default
{
    on_rez( integer sparam )
    {
        llResetScript();
    }
    state_entry()
    {
        OwnerName = llKey2Name( llGetOwner() );
        llSetText( OwnerName + "'s Tip Jar.\nAny tips gratefully received!\nL$0 Donated so far", <.2, 1, .6>, 1);
    }

    money(key id, integer amount)
    {
        Total += amount;
        // Shortcut 'cheat' to avoid multiple casts when constructing a message including non-string items
        string str = (string) [OwnerName, "'s Tip Jar.\nPlease tip if you are so inclined!\nL$", amount, " Was donated last!\nL$", Total, " Donated so far" ];
        llSetText(str, <1,1,1>, 1);
        llInstantMessage(id,"Thanks for the tip!");
        llInstantMessage(llGetOwner(), llKey2Name(id) + " donated L$" + (string) amount );
    }
}
```

An elementary vendor with money validation and refund capability

```lsl
// Give the first item in this object's inventory to anyone who pays the price

integer price = 10;      // The price needed to purchase the item

default
{
    state_entry()
    {
        // Turn off pay options so no money can be received until we are ready
        llSetPayPrice(PAY_HIDE, [PAY_HIDE ,PAY_HIDE, PAY_HIDE, PAY_HIDE]);
        // Request Debit Permissions from the owner so refunds can be given
        llRequestPermissions(llGetOwner(), PERMISSION_DEBIT);
    }
    on_rez(integer p)
    {
        llResetScript();                // Reset script on rezzing. Will thus register any change of owner.
    }
    money(key id, integer amount)        // Some money has been received and has gone to this object's owner
    {
        if (amount < price)
        {   // Customer has not paid enough
            llInstantMessage(id, "That's not enough money.");
            llGiveMoney(id, amount);   // Refund the money they paid
            return;
        }
        if (amount > price)
        {   // Customer paid too much. Refund the excess
            integer change = amount - price;
            llInstantMessage(id, "You paid more than L$" + (string)price
                + "  your change is L$" + (string)change );
            llGiveMoney(id, change);
        }
        // Customer has paid at least the right amount. Give them the item.
        string ItemName = llGetInventoryName(INVENTORY_OBJECT, 0);
        llGiveInventory(id, ItemName);
        llInstantMessage(id, "Please accept your purchase worth L$" + (string) price );
    }
    run_time_permissions(integer perm)
    {
        // If Debit permissions are granted, set up the pay price for this single-price vendor
        if(perm & PERMISSION_DEBIT)
            llSetPayPrice(price, [PAY_HIDE ,PAY_HIDE, PAY_HIDE, PAY_HIDE]);

        // In practice, the following line would be preferable and almost fully guards against a wrong amount being paid
        // - except in the rare event that the price is changed while a transaction is in progress, or a user with a hacked viewer
        //  llSetPayPrice(PAY_HIDE, [price ,PAY_HIDE, PAY_HIDE, PAY_HIDE]);
    }
}
```

## See Also

### Functions

- **llTransferLindenDollars** — Give money to another avatar with transaction confirmation
- **llGiveMoney** — Give money to another avatar
- **llSetPayPrice** — Configure the pay buttons

<!-- /wiki-source -->
