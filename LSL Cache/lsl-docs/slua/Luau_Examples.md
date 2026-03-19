---
name: "Luau Examples"
category: "reference"
type: "reference"
language: "SLua"
description: "This script demonstrates how one may create their own vehicle scripts, which don’t rely on the underlying LL vehicle system."
signature: ""
wiki_url: "https://wiki.secondlife.com/wiki/Luau_Example_Scripts"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

## vehicle.lua

This script demonstrates how one may create their own vehicle scripts, which don’t rely on the underlying LL vehicle system.

```lua
-- These two will hold the link numbers for left and right front wheels
local LINK_WHEEL_LEFT = 0
local LINK_WHEEL_RIGHT = 0

-- Integra Type R Engine properties
local Engine = {
    rpm = 800,              -- current engine RPM (starts at idle)
    gear = 0,               -- 0 = neutral; -1 = reverse; 1-5 for forward gears
    idleRPM = 800,          -- idle RPM
    maxRPM = 8300,          -- redline
    throttle = 0.0,         -- throttle value (0.0 to 1.0)
    gearRatios = {          -- Integra Type R gear ratios
        [-1] = 3.727,       -- reverse gear ratio
        [0]  = 0,          -- neutral
        [1]  = 3.727,
        [2]  = 2.256,
        [3]  = 1.729,
        [4]  = 1.416,
        [5]  = 1.194
    }
}

local FINAL_DRIVE = 4.1   -- Final drive ratio
local WHEEL_RADIUS = 0.3  -- in meters

-- Vehicle properties (using realistic Integra Type R mass)
local Vehicle = {
    speed = 0,      -- speed in m/s; negative indicates reverse motion
    mass = 1200,    -- mass in kg
    angle = 0,      -- heading angle in radians
    steering = 0,   -- steering input: -1 (left), 0 (none), 1 (right)
    brake = false   -- flag indicating if brakes are applied
}

-- Engine constants (using realistic Integra Type R values)
local MAX_TORQUE = 200   -- in Nm

-- Brake force constant (for active braking)
local BRAKE_FORCE = 4000  -- in Newtons

-- Define a torque curve function:
local function torqueCurve(rpm)
    local peakRPM = 6000
    if rpm  targetRPM then
        Engine.rpm = math.max(Engine.rpm - changeRate, targetRPM)
    end
end

-- Calculate the engine force delivered to the wheels.
local function getEngineForce()
    if Engine.gear == 0 then
        return 0  -- In neutral, no drive force is transmitted.
    else
        if Engine.throttle == 0 then
            -- Apply engine braking when throttle is released.
            return -ENGINE_BRAKE_FORCE
        else
            local torque = Engine.throttle * MAX_TORQUE * torqueCurve(Engine.rpm)
            local force = (torque * Engine.gearRatios[Engine.gear] * FINAL_DRIVE) / WHEEL_RADIUS
            return force
        end
    end
end

-- Starts the engine by setting it to idle RPM.
local function startEngine()
    Engine.rpm = Engine.idleRPM
    ll.Say(0, "Engine started. RPM: " .. Engine.rpm)
end

-- Shifts the gear if valid.
local function shiftGear(newGear)
    if Engine.gearRatios[newGear] then
        Engine.gear = newGear
        ll.Say(0, "Shifted to gear " .. newGear)
    else
        ll.Say(0, "Invalid gear: " .. newGear)
    end
end

local function findWheels()
    local total = ll.GetNumberOfPrims()
    for i = 1, total do
        local name = ll.GetLinkName(i)
        if name == "WHEEL_LF" then
            LINK_WHEEL_LEFT = i
        elseif name == "WHEEL_RF" then
            LINK_WHEEL_RIGHT = i
        end
    end
end

local castRayCounter = 0
local lastGrounded = false

local function isVehicleOnGround()
    castRayCounter = castRayCounter + 1
    if castRayCounter >= 5 then
        castRayCounter = 0
        local pos = ll.GetPos()
        local rayDistance = 4.5  -- threshold distance (in meters) to consider as "grounded"
        local rayStart = pos
        local rayEnd = pos + vector(0, 0, -rayDistance)
        local hitResult = ll.CastRay(rayStart, rayEnd, {})
        if rawlen(hitResult) == 3 then
            lastGrounded = true
        else
            lastGrounded = false
        end
    end
    return lastGrounded
end

-- Timer event: updates engine, vehicle physics, steering, and rotates the wheels based on steering.
function timer()
    local dt = 0.1  -- time step in seconds

    -- For neutral, update RPM based on throttle.
    if Engine.gear == 0 then
        updateEngineRPMNeutral()
    end

    -- Calculate forces.
    local C_rr = (Engine.gear == 0) and C_rr_neutral or C_rr_inGear
    local F_roll = Vehicle.mass * G * C_rr
    local engineForce = getEngineForce()
    local dragForce = getAerodynamicDrag(math.abs(Vehicle.speed))
    local netForce = engineForce - (F_roll + dragForce)

    -- Apply braking force if brakes are engaged.
    if Vehicle.brake then
        netForce = netForce - BRAKE_FORCE
    end

    local acceleration = netForce / Vehicle.mass
    local vel = ll.GetVel()
    local horizontal_vec = vector(vel.x, vel.y, 0)
    Vehicle.speed = (ll.VecMag(horizontal_vec) + acceleration * dt)

    -- Limit vehicle speed based on gear.
    if Engine.gear ~= 0 then
        if Vehicle.speed  maxSpeed then
            Vehicle.speed = maxSpeed
        end
    end

    -- When in gear, update RPM based on the new speed.
    if Engine.gear ~= 0 then
        Engine.rpm = computeEngineRPMFromSpeed()
    end

    -- Steering update using angular velocity and quaternions:
    local STEERING_RATE = math.rad(6)  -- desired steering rate per tick (radians)
    local yawDelta = Vehicle.steering * STEERING_RATE  -- small rotation for this tick

    if yawDelta ~= 0 then
        local angularSpeed = yawDelta / dt
        local angularVelocity = vector(0, 0, angularSpeed)
        ll.SetAngularVelocity(angularVelocity, 1)
        Vehicle.angle = Vehicle.angle + yawDelta
    else
        ll.SetAngularVelocity(vector(0, 0, 0), 1)
    end

    -- Display engine RPM and speed (converted to mph).
    local speed_mph = math.abs(Vehicle.speed) * 2.23694
    ll.SetText("RPM: " .. math.floor(Engine.rpm) ..
               " | Speed: " .. string.format("%.1f", speed_mph) ..
               " mph", vector(0,0,0), 1)

    -- Only update velocity if the vehicle is near the ground, and we're in gear.
    if isVehicleOnGround() and Engine.gear ~= 0 then
        local velocityVector
        if Engine.gear > 0 then
            velocityVector = vector(Vehicle.speed, 0, 0)
        else
            -- Reverse gear
            velocityVector = vector(-Vehicle.speed, 0, 0)
        end
        ll.SetVelocity(velocityVector, 1)
    end

    -- Update the wheel rotations to visually match the steering.
    local maxWheelTurn = math.rad(30)  -- maximum wheel turn angle in radians
    local wheelAngle = -Vehicle.steering * maxWheelTurn

    if LINK_WHEEL_LEFT > 0 then
        ll.SetLinkPrimitiveParamsFast(
            LINK_WHEEL_LEFT,
            {
                PRIM_ROT_LOCAL,
                ll.Euler2Rot(vector(-4.71239, -wheelAngle, 0))
            }
        )
    end

    if LINK_WHEEL_RIGHT > 0 then
        ll.SetLinkPrimitiveParamsFast(
            LINK_WHEEL_RIGHT,
            {
                PRIM_ROT_LOCAL,
                ll.Euler2Rot(vector(4.71239, wheelAngle, 0))
            }
        )
    end
end

-- Called when the object is touched: starts engine and simulation.
function touch_start(num)
    ll.Say(0, "Touch detected, requesting controls and starting engine.")
    ll.RequestPermissions(ll.GetOwner(), PERMISSION_TAKE_CONTROLS)
    startEngine()
    findWheels()
    ll.SetTimerEvent(0.1)
end

-- Called when runtime permissions are granted.
function run_time_permissions(perm)
    if bit32.btest(perm, PERMISSION_TAKE_CONTROLS) then
        ll.Say(0, "Permissions granted.")
        local controlMask = bit32.bor(CONTROL_FWD, CONTROL_BACK, CONTROL_UP, CONTROL_DOWN, CONTROL_LEFT, CONTROL_RIGHT)
        ll.TakeControls(controlMask, 1, 1)
    end
end

-- Handle control events:
-- • CONTROL_FWD applies throttle.
-- • CONTROL_BACK applies the brakes.
-- • CONTROL_UP and CONTROL_DOWN shift gears.
-- • CONTROL_LEFT and CONTROL_RIGHT steer the vehicle.
function control(avatar_id, level, edge)
    local start = bit32.band(level, edge)
    local held = bit32.band(level, bit32.bnot(edge))

    if bit32.band(held, CONTROL_BACK) ~= 0 then
        Vehicle.brake = true
        Engine.throttle = 0.0
    elseif bit32.band(held, CONTROL_FWD) ~= 0 then
        Vehicle.brake = false
        Engine.throttle = 1.0
        if Engine.gear == 0 then
            updateEngineRPMNeutral()
        end
    else
        Vehicle.brake = false
        Engine.throttle = 0.0
    end

    if bit32.band(start, CONTROL_UP) ~= 0 then
        shiftGear(Engine.gear + 1)
    end

    if bit32.band(start, CONTROL_DOWN) ~= 0 then
        shiftGear(Engine.gear - 1)
    end

    local steeringInput = 0
    if bit32.band(held, CONTROL_LEFT) ~= 0 then
        steeringInput = steeringInput + 1
    end
    if bit32.band(held, CONTROL_RIGHT) ~= 0 then
        steeringInput = steeringInput - 1
    end
    Vehicle.steering = steeringInput
end
```

## weather_box.lua

This script demonstrates coroutines, as well as working with a JSON-based web API:

```lua
local TEXTBOX_CHANNEL = 323242
-- kludge because we don't have LSL constants in here yet
local HTTP_BODY_MAXLENGTH = integer(2)
local PRIM_TEXT = integer(26)
local PRIM_SIZE = integer(7)

gCityName = ""
gLatLong = nil  -- A table of 2 elems when it's populated
gCityRequestTask = nil
gWeatherRequestTask = nil

-----
-- JSON stuff
-----

-- From https://github.com/rxi/json.lua/blob/master/json.lua

local json = {}

local escape_char_map = {
  [ "\\" ] = "\\",
  [ "\"" ] = "\"",
  [ "\b" ] = "b",
  [ "\f" ] = "f",
  [ "\n" ] = "n",
  [ "\r" ] = "r",
  [ "\t" ] = "t",
}

local escape_char_map_inv = { [ "/" ] = "/" }
for k, v in pairs(escape_char_map) do
  escape_char_map_inv[v] = k
end

local parse

local function create_set(...)
  local res = {}
  for i = 1, select("#", ...) do
    res[ select(i, ...) ] = true
  end
  return res
end

local space_chars   = create_set(" ", "\t", "\r", "\n")
local delim_chars   = create_set(" ", "\t", "\r", "\n", "]", "}", ",")
local escape_chars  = create_set("\\", "/", '"', "b", "f", "n", "r", "t", "u")
local literals      = create_set("true", "false", "null")

local literal_map = {
  [ "true"  ] = true,
  [ "false" ] = false,
  [ "null"  ] = nil,
}

local function next_char(str, idx, set, negate)
  for i = idx, #str do
    if set[str:sub(i, i)] ~= negate then
      return i
    end
  end
  return #str + 1
end

local function decode_error(str, idx, msg)
  local line_count = 1
  local col_count = 1
  for i = 1, idx - 1 do
    col_count = col_count + 1
    if str:sub(i, i) == "\n" then
      line_count = line_count + 1
      col_count = 1
    end
  end
  error( string.format("%s at line %d col %d", msg, line_count, col_count) )
end

local function codepoint_to_utf8(n)
  -- http://scripts.sil.org/cms/scripts/page.php?site_id=nrsi&id=iws-appendixa
  local f = math.floor
  if n  awaited event
    _coros = {},
    running = false
}

function EventLoop:create_task(func)
    local coro = coroutine.create(func)
    -- false has no semantic meaning here, we just want to reserve the space for
    -- the coroutine in the table without saying we're awaiting anything yet.
    self._coros[coro] = false
    self:_run_coro(coro)
    return coro
end

function EventLoop:kill_task(coro)
    self._coros[coro] = nil
    if coroutine.status ~= "dead" then
        coroutine.close(coro)
    end
end

-- (internal) run the event
function EventLoop:_run_coro(coro, ...)
    assert(coroutine.status(coro) ~= "dead")
    -- assert(not self.running)
    local old_running = self.running
    self.running = true

    -- Since we're running, this isn't currently awaiting anything
    self._coros[coro] = false
    local success, ret = coroutine.resume(coro, ...)
    self.running = old_running

    -- If we're not done then ret should be the kind of event we're awaiting.
    -- Otherwise it's an error message or something. Who cares.
    if not success then
        -- Get rid of the coro
        if ret then
            ll.OwnerSay(`Might have an error: {ret}`)
        end
        ret = nil
    end
    self._coros[coro] = ret
end

-- Wake up any tasks that are waiting for this kind of event
function EventLoop:handle_event(name, ...)
    -- We may mutate self._coros, so do a clone
    local coros = table.clone(self._coros)
    ll.OwnerSay(`Handling {name}`)

    for coro, awaited_event in coros do
        if coroutine.status(coro) == "dead" then
            -- Hmm, this coroutine is dead, prune it.
            self._coros[coro] = nil
        end

        if awaited_event == name then
            ll.OwnerSay(`Dispatching {name} to {coro}`)
            self:_run_coro(coro, ...)
        end
    end
end

function EventLoop:create_event_catcher(name)
    local function catcher(...)
        ll.OwnerSay("yay")
        EventLoop:handle_event(name, ...)
    end
    return catcher
end

-- Helper function for waiting and telling the EventLoop what event you want
local function await_event(kind)
    -- You had better do this inside a running event loop
    assert(EventLoop.running)
    -- This will yield, the EventLoop will resume us once it has
    -- an event we might be interested in.
    return coroutine.yield(kind)
end

-----
-- Script-specific functions
-----

local function hide_children()
    for i=2,ll.GetNumberOfPrims() do
        -- Hide all the child prims
        ll.SetLinkAlpha(i, 0, -1)
        ll.SetLinkPrimitiveParamsFast(i, {
            PRIM_SIZE, vector(0.5, 0.5, 0.5),
            PRIM_TEXT, "", vector(1,1,1), 1
        })
    end
end

local function send_textbox(avatar_id, message, channel)
    ll.TextBox(avatar_id, message, channel)

    while true do
        local resp_channel, name, id, resp = await_event("listen")
        if id ~= avatar_id or channel ~= resp_channel then
            -- If this isn't a message we're interested in then wait for the next event
            ll.OwnerSay(`{id}, {avatar_id}, {resp_channel}, {channel}`)
            continue
        end
        return resp
    end
end

local function make_json_request(url)
    local req_id = ll.HTTPRequest(url, {HTTP_BODY_MAXLENGTH, integer(16000)}, "")
    while true do
        local ev_id, status, metadata, body = await_event("http_response")
        if ev_id ~= req_id then
            -- Not a response for the HTTP request we were waiting on, wait for the next event.
            continue
        end
        return status, metadata, body
    end
end

local function request_weather()
    -- And you can use a wrapper like this to make an async function callable within both normal and coroutine contexts.
    -- Normally this sort of thing would not be necessary, but here it is since the EventLoop lives in our own code,
    -- and isn't a property of the actual script engine.
    if gWeatherRequestTask then
        EventLoop:kill_task(gWeatherRequestTask)
    end

    gWeatherRequestTask = EventLoop:create_task(function()
    ll.OwnerSay("Requesting weather")
        local status, metadata, body = make_json_request(`https://api.open-meteo.com/v1/forecast?latitude={gLatLong[1]}&longitude={gLatLong[2]}&current=temperature_2m&daily=temperature_2m_max`)
        if status ~= 200 then
            ll.OwnerSay("Error requesting weather")
            return
        end
        local parsed = json.decode(body)

        local current = parsed["current"]
        ll.OwnerSay(`Temperature is {current["temperature_2m"]}C`)
        ll.SetText(`Temperature in {gCityName} is currently {current["temperature_2m"]}C`, vector(1,1,1), 1)

        -- Show the highs for each day
        local days = parsed["daily"]["temperature_2m_max"]
        for i=1,#days do
            local link_num = i + 1
            -- Higher temps = bigger on Z, negatives are unrepresentable :)
            local z_size = (days[i] / 30) * 2
            ll.SetLinkAlpha(link_num, 1, -1)
            ll.SetLinkPrimitiveParamsFast(link_num, {
                PRIM_SIZE, vector(0.5, 0.5, z_size),
                PRIM_TEXT, `{days[i]}C`, vector(1,1,1), 1
            })
        end
    end)
end

local function ask_for_city()
    local resp = send_textbox(ll.GetOwner(), "What city do you want the weather for?", TEXTBOX_CHANNEL)
    if not resp then
        ll.OwnerSay("Got no response for city request.")
        return
    end

    ll.OwnerSay(`You want the weather for {resp}.`)
    gLatLong = nil
    gCityName = resp

    hide_children()

    -- request the lat and long for this city
    local status, metadata, body = make_json_request(`https://nominatim.openstreetmap.org/search.php?city={ll.EscapeURL(resp)}&format=jsonv2`)
    local parsed = json.decode(body)
    if not #parsed then
        ll.OwnerSay(`Got no results for {resp}!`)
        return
    end

    local first_result = parsed[1]
    gLatLong = {first_result["lat"], first_result["lon"]}
    ll.OwnerSay(`City Lat: {gLatLong[1]}, Long: {gLatLong[2]}`)

    request_weather()

    -- request weather again in 3 mins
    ll.SetTimerEvent(180)
end

-----
-- Event Handlers
-----

-- If we don't care about conventionally dispatched events, we can just set the event handler to directly send
-- event data to the event loop.
http_response = EventLoop:create_event_catcher("http_response")
listen = EventLoop:create_event_catcher("listen")

-- More conventional event handlers work too.
function touch_start(num)
    for i=0,num-1 do
        if ll.GetOwner() ~= ll.DetectedKey(i) then
            -- Go to next loop if it wasn't the owner touching us.
            continue
        end

        if gCityRequestTask then
            EventLoop:kill_task(gCityRequestTask)
        end

        -- Spin up a task to ask the user for their city
        gCityRequestTask = EventLoop:create_task(ask_for_city)
        break
    end
end

function timer()
    request_weather()
end

-- Not strictly necessary, but I like having the main function have its own scope.
-- Rather than just have top-level logic.
local function main()
    ll.Listen(TEXTBOX_CHANNEL, "", "", "")
    ll.SetText("", vector(1,1,1), 1)
    hide_children()
    ll.OwnerSay("Weatherbox operational!")
end

main()
```

## dialog_coroutine.lua

This script demonstrates how one could use coroutines to handle dialog responses, with multi-user support.

```lua
-------------------------
-- Minimal EventLoop
-------------------------
local EventLoop = {
    -- Coroutine -> eventName it’s waiting for
    _coros = {},
    running = false
}

function EventLoop:create_task(func)
    local coro = coroutine.create(func)
    self._coros[coro] = false
    self:_run_coro(coro)
    return coro
end

function EventLoop:kill_task(coro)
    self._coros[coro] = nil
    if coroutine.status(coro) ~= "dead" then
        coroutine.close(coro)
    end
end

-- Internal helper: resumes a coroutine
function EventLoop:_run_coro(coro, ...)
    if coroutine.status(coro) == "dead" then
        return
    end

    local old_running = self.running
    self.running = true

    self._coros[coro] = false
    local ok, eventAwaited = coroutine.resume(coro, ...)
    self.running = old_running

    if not ok then
        ll.OwnerSay(`Coroutine error: {eventAwaited}`)
        self._coros[coro] = nil
        return
    end

    -- If still alive, 'eventAwaited' is the next event it wants
    self._coros[coro] = eventAwaited
end

function EventLoop:handle_event(eventName, ...)
    ll.OwnerSay(`Handling event {eventName}`)
    local snapshot = table.clone(self._coros)
    for coro, waitingFor in pairs(snapshot) do
        if coroutine.status(coro) == "dead" then
            self._coros[coro] = nil
        elseif waitingFor == eventName then
            ll.OwnerSay(`Dispatching event {eventName} to {coro}`)
            self:_run_coro(coro, ...)
        end
    end
end

-- Coroutines use this to yield until an event
local function await_event(name)
    assert(EventLoop.running, "await_event called outside a coroutine!")
    return coroutine.yield(name)
end

-------------------------
-- Script Logic
-------------------------
local buttons = {"-", "Red", "Green", "Yellow"}
local dialogInfo = "\nPlease make a choice."

-- Use the chat listener to feed the event-loop
function listen(channel, name, sender_id, message)
    -- We handle all 'listen' events via the event-loop
    EventLoop:handle_event(`listen_{channel}`, channel, name, sender_id, message)
end

-- Called when the script starts
function state_entry()
    -- Seed math.random so each new script run doesn’t repeat the same channels
    math.randomseed(ll.GetUnixTime())
    ll.OwnerSay("Script started with random channels for each user.")
end

-- A coroutine function for a single user's dialog flow
local function handle_dialog_for_user(userId)
    -- Use a random channel
    local channel = math.random(0x1, 0xFFFF)
    -- Create a listener for that channel
    local listenHandle = ll.Listen(channel, "", "", "")

    while true do
        -- Show the user a dialog
        ll.Dialog(userId, dialogInfo, buttons, channel)

        -- Wait for the next 'listen' event (channel, name, sender_id, message)
        local c, n, sid, msg = await_event(`listen_{channel}`)

        -- If this "listen" event isn't for our channel/user, ignore it
        if c == channel and sid == userId then
            -- If user pressed "-", re-display the menu, else they picked a final color
            if msg ~= "-" then
                ll.Say(0, `{n} selected {msg}`)
                -- Now that they've chosen something else, remove the listener and finish
                ll.ListenRemove(listenHandle)
                return
            end
        end
    end
end

-- Called when the object is touched
function touch_start(num_detected)
    for i=0, num_detected-1 do
        local toucherId = ll.DetectedKey(i)
        -- Create a separate coroutine for each person who touches
        EventLoop:create_task(function()
            handle_dialog_for_user(toucherId)
        end)
    end
end

-- Run state_entry on load:
state_entry()
```