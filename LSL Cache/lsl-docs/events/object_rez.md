---
name: "object_rez"
category: "event"
type: "event"
language: "LSL"
description: "Triggered when the object rezzes an object."
signature: "object_rez(key id)"
wiki_url: 'https://wiki.secondlife.com/wiki/object_rez'
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
deprecated: "false"
parameters: []
---

Triggered when the object rezzes an object.


## Signature

```lsl
object_rez(key id)
{
    // your code here
}
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `id` | UUID of object rezzed. |


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/object_rez)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/object_rez) — scraped 2026-03-18_

## Caveats

- Triggers in all running scripts with an object_rez event, AND in the same **prim** as the script calling llRezObject or llRezAtRoot.

  - Does NOT trigger in linked prims.
- A message sent to the rezzed object may arrive before the object has had a chance to opened a listen channel and is ready to receive listen events unless you provide for a communication handshake between the rezzer and the new object.

  - Objects that have opened a listen channel before being rezzed (for example in state_entry) will be able to receive messages as soon as object_rez is triggered.

## Examples

#### Rez with handshake communication

The rezzer script will create a new object ("rezzee") and wait for a message from it before sending inventory items to the new object. Once all inventory items have been sent, the rezzer will send a message to the new object, letting it know the process is finished.

```lsl
// The rezzer and rezzee must use the same communication channel.
integer COM_CHANNEL = -17974594;
string REZZEE_NAME = "Rezzee";

// These are expected messages between rezzer and rezzee.
string CMD_REZZEE_READY = "REZZEE_READY";
string CMD_REZZER_DONE = "REZZER_DONE";

key rezzee_key;

default
{
	touch_start(integer num_detected)
	{
		// A separate state is used to disable touch-events and remove listens.
		// This prevents multiple objects from being rezzed until the previous one
		// has finished receiving everything it needs.
		state rez_new_object;
	}
}

state rez_new_object
{
	state_entry()
	{
		// Listen for messages on the shared channel, from objects with the correct name.
		llListen(COM_CHANNEL, REZZEE_NAME, "", "");

		// Rez the object with the shared channel as the rez-parameter.
		vector position = llGetPos() + <0, 0, 1>;
		llRezObject(REZZEE_NAME, position, ZERO_VECTOR, ZERO_ROTATION, COM_CHANNEL);
	}

	object_rez(key id)
	{
		// The object has rezzed in-world. It may not have called llListen yet,
		// so we'll save its UUID and wait for a message from it.
		rezzee_key = id;
	}

	listen(integer channel, string name, key id, string message)
	{
		// Check that the 'ready' message was sent by the object we rezzed last.
		if (message == CMD_REZZEE_READY && id == rezzee_key)
		{
			// Send inventory to the new object.
			integer i = llGetInventoryNumber(INVENTORY_NOTECARD);
			while (i--)
			{
				string name = llGetInventoryName(INVENTORY_NOTECARD, i);
				llGiveInventory(id, name);
			}

			// Let the new object know it's ready, and return to original state.
			llRegionSayTo(id, COM_CHANNEL, CMD_REZZER_DONE);
			state default;
		}
	}
}
```

The script in the new object ("rezzee") will let the rezzer know when it's prepared to receive communications.

```lsl
// These are expected messages between rezzer and rezzee.
string CMD_REZZEE_READY = "REZZEE_READY";
string CMD_REZZER_DONE = "REZZER_DONE";

// These will be determined after this object is created by another object.
integer com_channel;
key rezzer_key;

default
{
	on_rez(integer start_param)
	{
		// A separate state is used to prevent other functionality from happening
		// while this object waits for its rezzer to finish sending everything it needs.
		com_channel = start_param;
		state wait_for_configuration;
	}
}

state wait_for_configuration
{
	state_entry()
	{
		// Get the key of the object which rezzed this object.
		list details = llGetObjectDetails(llGetKey(), [OBJECT_REZZER_KEY]);
		rezzer_key = llList2Key(details, 0);

		// Listen for messages on the shared channel, from only the rezzer.
		llListen(com_channel, "", rezzer_key, "");

		// Prepare to receive inventory, then tell the rezzer we're ready.
		llAllowInventoryDrop(TRUE);
		llRegionSayTo(rezzer_key, com_channel, CMD_REZZEE_READY);
	}

	listen( integer channel, string name, key id, string message )
	{
		// Check that the 'done' message was sent by the rezzer.
		if (message == CMD_REZZER_DONE && id == rezzer_key)
		{
			// Return to the original state to continue normal functionality.
			state default;
		}
	}

	state_exit()
	{
		// Turn off inventory drop. Changing state will also remove listens.
		llAllowInventoryDrop(FALSE);
	}
}
```

#### Rez and communicate without handshake

If the new object has already opened a listen channel before being rezzed, a handshake is not necessary because the object_rez event will not trigger until the object is fully initialized.

This is how a script in the new object can pre-open a listen channel:

```lsl
// The rezzer and rezzee must use the same communication channel.
integer COM_CHANNEL = -17974594;

default
{
    // This event is triggered when the script starts
    // and doesn't trigger again when this object is rezzed,
    // which means the listener will be open as soon as a new copy is rezzed.
    state_entry()
    {
        llListen(COM_CHANNEL, "", "", "");
    }

    listen(integer channel, string name, key id, string message)
    {
        // Get the key of the object which rezzed this object.
        list details = llGetObjectDetails(llGetKey(), [OBJECT_REZZER_KEY]);
        key rezzer_key = llList2Key(details, 0);

        if (id == rezzer_key)
        {
            // The message could be anything useful, such as
            // position data, sound/texture/avatar UUID, etc.
            llOwnerSay("I heard: " + message);
        }
    }
}
```

And this is how it would simplify the rezzer script:

```lsl
// The rezzer and rezzee must use the same communication channel.
integer COM_CHANNEL = -17974594;
string REZZEE_NAME = "Rezzee";

default
{
    touch_start(integer num_detected)
    {
        // Rez the object. The shared channel isn't included
        // because the new object is already listening to it.
        vector position = llGetPos() + <0, 0, 1>;
        llRezObject(REZZEE_NAME, position, ZERO_VECTOR, ZERO_ROTATION, 0);
    }

    object_rez(key id)
    {
        // The object has rezzed in-world.
        // We can message it directly because we know it's listening.
        llRegionSayTo(id, COM_CHANNEL, "Are you there?");
    }
}
```

## See Also

### Events

- **on_rez** — Triggered when the object the script is in is rezzed

### Functions

- **llRezObject** — Used to rez an object at the center of mass
- **llRezAtRoot** — Used to rez an object at the root

<!-- /wiki-source -->
