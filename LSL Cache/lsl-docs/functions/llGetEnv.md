---
name: "llGetEnv"
category: "function"
type: "function"
language: "LSL"
description: "Returns regional environment data by string key, such as sim_version, chat_range, agent_limit, etc."
wiki_url: "https://wiki.secondlife.com/wiki/llGetEnv"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "string llGetEnv(string name)"
parameters:
  - name: "name"
    type: "string"
    description: "The name of the environment variable to query"
return_type: "string"
energy_cost: "0.0"
sleep_time: "0.0"
patterns: ["llgetenv"]
deprecated: "false"
---

# llGetEnv

```lsl
string llGetEnv(string name)
```

Returns a string containing requested data about the current region. All returned values are strings — cast as needed.

## Valid Parameter Strings

| Name | Description | Cast To |
|------|-------------|---------|
| `"agent_limit"` | Max avatars normally allowed | integer |
| `"agent_limit_max"` | Max configurable agent setting | integer |
| `"chat_range"` | Normal chat range in metres | float |
| `"whisper_range"` | Whisper range in metres | float |
| `"shout_range"` | Shout range in metres | float |
| `"dynamic_pathfinding"` | `"enabled"` or `"disabled"` | string |
| `"estate_id"` | Estate numeric ID (`"1"` = mainland) | integer |
| `"estate_name"` | Estate name | string |
| `"frame_number"` | Current simulator frame number | integer |
| `"region_idle"` | `"1"` if idle, `"0"` if not | integer |
| `"region_product_name"` | Region type description | string |
| `"region_start_time"` | Last restart time (Unix epoch) | integer |
| `"sim_channel"` | Channel string (e.g., `"Second Life Server"`) | string |
| `"sim_version"` | Version (e.g., `"10.11.30.215699"`) | string |
| `"simulator_hostname"` | Simulator host name | string |
| `"region_max_prims"` | Maximum prims allowed | integer |
| `"region_object_bonus"` | Object bonus factor | float |
| `"region_rating"` | Maturity rating | string |
| `"grid"` | Grid name | string |
| `"allow_damage_adjust"` | Scripts can adjust damage | integer |
| `"restore_health"` | Health reset on death | integer |
| `"death_action"` | Action on death (0–3) | integer |

## Examples

```lsl
default
{
    state_entry()
    {
        llOwnerSay("Channel: " + llGetEnv("sim_channel"));
        llOwnerSay("Version: " + llGetEnv("sim_version"));
        llOwnerSay("Chat range: " + llGetEnv("chat_range") + "m");
        llOwnerSay("Agent limit: " + llGetEnv("agent_limit"));

        // Parse version components
        list ver = llParseString2List(llGetEnv("sim_version"), ["."], []);
        llOwnerSay("Build: " + llList2String(ver, 3));
    }
}
```

## See Also

- `llGetRegionName` — region name
- `llGetSimulatorHostname` — simulator hostname
- `llGetRegionFlags` — region feature flags
- `llGetRegionFPS` — frames per second
- `llGetRegionTimeDilation` — time dilation factor


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetEnv) — scraped 2026-03-18_

Returns a string with the requested data about the region.

## Examples

```lsl
default
{
    touch_start(integer total_number)
    {
        string version = llGetEnv("sim_version");
        llOwnerSay("Region " + llGetRegionName() + " is running "
                   + llGetEnv("sim_channel") + " version " + version );

        list ver = llParseString2List(version, ["."], []);

        llOwnerSay("Build: "+llList2String(ver, 3));
        llOwnerSay("Build Date: "+llList2String(ver, 2)+"-"+llList2String(ver, 1)+"-20"+llList2String(ver, 0));
    }
}
```

## Notes

- Region idling lowers a region's framerate when no avatars are currently on or looking into the region.  Scripts measuring time dilation with llGetRegionTimeDilation may report significant time dilation if the region is idle.

## See Also

### Functions

- llRequestSimulatorData
- llGetSimulatorHostname
- llGetRegionFlags

<!-- /wiki-source -->
