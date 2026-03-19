---
name: "llSetPayPrice"
category: "function"
type: "function"
language: "LSL"
description: "Suggest default amounts for the pay text field and pay buttons of the appearing dialog when someone chooses to pay this object."
signature: "void llSetPayPrice(integer price, list quick_pay_buttons)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetPayPrice'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsetpayprice"]
---

Suggest default amounts for the pay text field and pay buttons of the appearing dialog when someone chooses to pay this object.


## Signature

```lsl
void llSetPayPrice(integer price, list quick_pay_buttons);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `price` | PAY_* constant or positive value (including zero) |
| `list` | `quick_pay_buttons` | Four PAY_* constants and/or positive integer values (zero is not shown) |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetPayPrice)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetPayPrice) — scraped 2026-03-18_

Suggest default amounts for the pay text field and pay buttons of the appearing dialog when someone chooses to pay this object.

## Caveats

- This function should not be trusted to limit the values of money payable to the object; *always* verify the amount paid is the amount expected.
- Use only one call to this function in all the scripts on an object to prevent confusion about which values are used.   You still need to check in the money event that the amount is as expected.
- This function only works when called from the root prim of an object. Its effect applies to all the prims in the object. Calling it from a child prim has no effect.

  - There is currently a [viewer bug](https://feedback.secondlife.com/slua-alpha/p/child-prim-in-linkset-cannot-be-paid-if-previously-a-root-prim-with-llsetpaypric) where calls from child prims will **prevent** payment to the object.
- Payment to a prim can be blocked by the llSetPayPrice() setting in the prim, which persists even if the script with llSetPayPrice() is removed.
- **Caution:** Calling this function will enable payment on the prim (or the whole object if it is the root prim) for the current state, even when this state has no money event.
- Otherwise, the pay option will only be shown in prims having a running script with a money event (or in all the prims of the object if the root has a running script with a money event).
- The effect seems to persist even if the script is recompiled with out the llSetPayPrice function, even if the script is replaced with another one which includes a money event, but not llSetPayPrice.
- Money cannot be paid to an attachment; "Pay" will go directly to the wearer instead.
- If **quick_pay_buttons** contains a negative value or zero, the button will not be shown at all.

  - However, zero is allowed for **price**, which is used to set the custom text field's value within the Pay window.
- If *price* is PAY_HIDE and a payment is made that does not match any value in *quick_pay_buttons*, then the simulator will block the payment and the payer will receive an error message.

## Examples

This will give the user a dialog box without the **price** field and only one button with a value of 150.

```lsl
llSetPayPrice(PAY_HIDE, [150,PAY_HIDE,PAY_HIDE,PAY_HIDE])
```

```lsl
integer price = 10;

default
{
    state_entry()
    {
        llSetPayPrice(PAY_HIDE, [PAY_HIDE ,PAY_HIDE, PAY_HIDE, PAY_HIDE]);
        llRequestPermissions(llGetOwner(), PERMISSION_DEBIT);
    }
    run_time_permissions(integer perm)
    {
        if(perm & PERMISSION_DEBIT)
            state cash;
    }
}

state cash
{
    state_entry()
    {
        llSetPayPrice(price, [price ,PAY_HIDE, PAY_HIDE, PAY_HIDE]);
    }
    money(key id, integer amount)
    {
        if(amount != price)
        {
            llGiveMoney(id, amount);
            llInstantMessage(id, "You paid "+(string)amount+", which is the wrong price, the price is: "+(string)price);
        }
        else
        {
            //insert your give code here.
            llInstantMessage(id, "You paid the right price");
        }
    }
}
```

## See Also

### Events

- money

### Functions

- llGiveMoney

<!-- /wiki-source -->
