---
name: "SLua Alpha"
category: "reference"
type: "reference"
language: "SLua"
description: "This functionality is in alpha. Instability is to be expected, and there may be very sharp edges. At this point it is expected that Luau can crash regions and perform other types of undesirable behavior."
signature: ""
wiki_url: "https://wiki.secondlife.com/wiki/SLua_Alpha"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Warning!

This functionality is in alpha. Instability is to be expected, and there may be very sharp edges. At this point it is expected that Luau can crash regions and perform other types of undesirable behavior.

**🚨 PLEASE NOTE Memory and performance characteristics, and API specifics may change! Scripts are currently being run in unoptimized form for development purposes.**

**## Second Life Lua (SLua) Alpha SLua is scripting for Second Life based on [Luau](https://luau.org), a fast, small, safe, and gradually typed embeddable scripting language derived from Lua. It is designed to be backwards compatible with Lua 5.1, incorporating features from future Lua releases and expanding the feature set with type annotations and a state-of-the-art type inference system. Luau is largely implemented from scratch, with the language runtime being a heavily modified version of the Lua 5.1 runtime, featuring a completely rewritten interpreter and other performance innovations. ## Why Lua? The decision to integrate Lua into Second Life was driven by its ability to meet all the requirements for a scripting engine within the platform. Lua offers a high-quality scripting experience to creators, addressing many of the limitations present in the current LSL (Linden Scripting Language) environment. Its lightweight nature and performance optimizations make it an ideal choice for enhancing the scripting capabilities in Second Life. For more information on why Lua was chosen, please see the [Lua FAQ](https://wiki.secondlife.com/wiki/Lua_FAQ). ## How to Get Started with SLua In order to play with SLua, you'll need to download our Lua project viewer, and either log onto our [Aditi beta grid](https://lindenlab.freshdesk.com/support/solutions/articles/31000156725-accessing-aditi) or go to the SLua-enabled beta regions on the main grid. - Access the latest build of the SLua-enabled Second Life Viewer from [here](https://releasenotes.secondlife.com/viewer.html). SLua-enabled regions on the main grid: - SLua Beta Landing - SLua Beta Porridge - SLua Beta Eraserhead - SLua Beta Glass - SLua Beta Void - SLua Beta Anderson - SLua Beta Snausage (Adult) - SLua Beta Nicolse - SLua Beta IsNeat SLua-enabled regions on the beta grid: - SLua Yardang - SLua Tombolo - SLua Mesa - SLua Tideland When editing a script in the new Lua project viewer, you'll notice a new Compiler** drop-down near the save button. This drop-down will allow you to select which compiler will be used, as well as which script runtime will be used (LSO2, Mono, Luau).

[](https://wiki.secondlife.com/wiki/File:Compiler_dropdown.png)

Compiler drop-down options:

- **LSL: Legacy (LSO2)** - Scripts written in LSL, to be run on the old LSO2 VM
- **LSL: Mono**- Scripts written in LSL, to be run on the Mono VM
- **Lua** - Scripts written in Lua, to be run on the SLua VM
- **LSL: 2025 VM**- Scripts written in LSL, to be run on the SLua VM

### Transitioning from LSL to SLua

- **Function Namespacing:**

  - In SLua, Linden Lab functions have been moved under the **ll** namespace.
  - For example:

  - *llSay* becomes *ll.Say*
  - *llGetPos* becomes *ll.GetPos*
- **Lists**

  - Lua indexes begin from 1, unlike LSL where indexes begin from 0.
  - Lua uses `{}` for *tables*, unlike LSL where `[]` is used for *lists*.
- Types

  - SLua doesn't support the usual vector/rotation syntax ``

  - Instead, these values are created with the functions `vector(x, y, z)`, `rotation(x, y, z, s)`
  - Similar functions exist for **uuid** (key) and **integer** (distinct from the built-in **number** type)

### SLua Libraries

- **Coroutines:**

  - SLua supports coroutines, allowing for cooperative multitasking within scripts.
  - Key functions include:

  - *coroutine.create*
  - *coroutine.status*
  - *coroutine.resume*
  - Refer to the [coroutine library documentation](https://luau.org/library#coroutine-library) for more details.
- **Bitwise Operations:**

  - SLua includes a *bit32* library for bitwise operations, enabling more efficient data manipulation.
  - Refer to the [bit32 library documentation](https://luau.org/library#bit32-library) for more details.
- **JSON to Table Translation:**

  - SLua includes a modified [lua-cjson library](https://github.com/openresty/lua-cjson) that translates tables into JSON objects and arrays and back.
  - Vectors and quaternions are converted to strings, which may be changed back using the *tovector* and *toquaternion* functions, respectfully.
  - Buffers are encoded as Base64 strings. They may be decoded using the *llbase64.decode* function.
  - Functions:

  - `json_text = lljson.encode(some_table)`
  - `some_table = lljson.decode(json_text)`
- **Base64 Encoding:**

  - A Base64 library capable of handling SLua strings and binary buffers, unlike classic *ll* namespace functions.
  - Leveraged by the JSON functionality, but can also be called separately.
  - Functions:

  - `base64string = llbase64.encode(string_or_buffer)`
  - `str = llbase64.decode(base64string)` for strings
  - `buf = llbase64.decode(base64string, true)` for buffers
- **Standard Library:**

  - SLua comes equipped with a standard library of functions designed to manipulate built-in data types.
  - Explore the [Luau Standard Library](https://luau.org/library) for a comprehensive list of available functions.

## Feedback and Support

We encourage all creators to explore the new scripting capabilities and provide feedback. Your insights are invaluable in refining and enhancing this feature. For more information and to share your experiences, please refer to our [Lua FAQ](https://wiki.secondlife.com/wiki/Lua_FAQ).

## Example Scripts

To help you get started, we've assembled some example scripts that demonstrate the capabilities of SLua. These scripts cover various functionalities and can serve as a foundation for your own creations. Please feel free to propose changes to these scripts, or modify them to your heart's desire!

### default_script.lua

This script is roughly equivalent to the default "new script" that gets created for LSL.

```lua
function state_entry()
   ll.Say(0, "Hello, Avatar!")
end

LLEvents:on("touch_start", function(detected: {DetectedEvent})
   ll.Say(0, "Touched.")
end)

-- Simulate the state_entry event
state_entry()
```

### dialog.lua

This script demonstrates how one can interact with dialog menus.

```lua
-- Define the menu buttons and dialog message.
local buttons = {"-", "Red", "Green", "Yellow"}
local dialogInfo = "\nPlease make a choice."

local ToucherID = nil
local dialogChannel = nil
local listenHandle = nil
local timerHandle = nil

-- This function is called when the script first starts.
function state_entry()
    -- Get the object's key and compute a dialog channel number.
    local key = ll.GetKey()
    -- Extract the last 7 characters of the key and convert it from hex.
    dialogChannel = -1 - tonumber(string.sub(tostring(key), -7, -1), 16)
end

-- Called when the object is touched.
LLEvents:on("touch_start", function(detected: {DetectedEvent})
    ToucherID = detected[1]:getKey()
    -- If there is already a listen handle, then remove it
    if listenHandle then
        ll.ListenRemove(listenHandle)
    end
    listenHandle = ll.Listen(dialogChannel, "", ToucherID, "")
    ll.Dialog(ToucherID, dialogInfo, buttons, dialogChannel)
    -- Set a 60-second timer for response.
    if timerHandle then
        LLTimers:off(timerHandle)
    end
    timerHandle = LLTimers:once(60,timeoutListen)
end)

-- Called when a dialog response is received.
LLEvents:on("listen", function(channel, name, sender_id, message)
    if message == "-" then
        -- Redisplay the dialog if the "-" option is selected.
        ll.Dialog(ToucherID, dialogInfo, buttons, dialogChannel)
        return
    end
    -- Stop the timer, and stop the listening handler.
    ll.ListenRemove(listenHandle)
    listenHandle = nil
    if timerHandle then
        LLTimers:off(timerHandle)
    end
    -- Let the user know what they selected
    ll.Say(0, `You selected {message}`)
end)

-- Called when the timer expires.
function timeoutListen()
    -- Stop the timer and clean up the listener.
    if listenHandle then
        ll.ListenRemove(listenHandle)
        ll.Whisper(0, "Sorry. You snooze; you lose.")
    end
end

-- Invoke state_entry on startup, since simulator doesn't invoke 
-- it like it does in LSL
state_entry()
```

### user_input_coroutine.lua

This script demonstrates [coroutines](https://www.lua.org/pil/9.html) and how they can simplify the overarching logic of a script, enabling us to write the bulk of our multi-event code within a centralized function instead of fragmenting across separate event handlers.

```lua
-- Wait for user input mid-function before doing something useful with it.
main = function(toucher)
    local handle = ll.Listen(0, "", toucher, "")
    local event = touch_start   -- save function for later
    touch_start = nil           -- disable touch_start

    ll.RegionSayTo(toucher, 0, "Do you want pants or gloves?")
    local clothing = coroutine.yield() -- pause the routine's execution here
    ll.RegionSayTo(toucher, 0, "For men or women?")
    local gender = coroutine.yield()
    ll.RegionSayTo(toucher, 0, "Favorite color?")
    local color = coroutine.yield()
    ll.RegionSayTo(toucher, 0, "Here's "..color.." "..clothing.." for "..gender)

    ll.ListenRemove(handle)
    touch_start = event -- restore touch_start
end

LLEvents:on("touch_start",function(detected: {DetectedEvent})
    local toucher = detected[1]:getKey()
    routine = coroutine.create(main)    -- new coroutine
    coroutine.resume(routine, toucher)  -- run coroutine (with one argument)
end)

-- When the coroutine is suspended, incoming events can be handled
-- and we can resume() execution of the routine
-- and pass any number of arguments to be returned by yield()
LLEvents:on("listen", function(channel, name, id, message)
    coroutine.resume(routine, message)
end)
```

### multi_user_input_coroutine.lua

Following from the above example, how can we handle multiple users? This is where coroutines shine.

Instead of disabling touches to prevent others from interacting with the object, we can create new copies of the coroutine each time an avatar touches the object. We can then resume whichever coroutine is needed, based on the avatar, while all of them track their own progress separately and automagically.

```lua
-- Key: avatar uuid; Value: coroutine thread
routines = {}

main = function(toucher)
    local handle = ll.Listen(0, "", toucher, "")

    ll.RegionSayTo(toucher, 0, "Do you want pants or gloves?")
    local clothing = coroutine.yield()
    ll.RegionSayTo(toucher, 0, "For men or women?")
    local gender = coroutine.yield()
    ll.RegionSayTo(toucher, 0, "Favorite color?")
    local color = coroutine.yield()
    ll.RegionSayTo(toucher, 0, "Here's "..color.." "..clothing.." for "..gender)

    ll.ListenRemove(handle)
    routines[toucher] = nil -- Remove from collection
end

LLEvents:on("touch_start",function(detected: {DetectedEvent})
    local toucher = detected[1]:getKey()
    local routine = routines[toucher]
    if not routine then -- New user needs new routine
        routine = coroutine.create(main)
        routines[toucher] = routine -- Add to collection
        coroutine.resume(routine, toucher)
    end
end)

LLEvents:on("listen", function(channel, name, id, message)
    coroutine.resume(routines[id], message) -- Resume a specific coroutine
end)
```

### More Examples

- Find more example scripts at [Luau Example Scripts](https://wiki.secondlife.com/wiki/Luau_Example_Scripts)

- [Lua Gotchas, Footguns and Other Hazards](https://roblox.github.io/lua-style-guide/gotchas/)