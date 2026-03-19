---
name: "Common LSL Constants"
category: "constant"
type: "constant"
language: "LSL"
description: "Commonly used LSL constants: TRUE, FALSE, NULL_KEY, ZERO_VECTOR, ZERO_ROTATION, math constants, channel constants, and EOF"
wiki_url: "https://wiki.secondlife.com/wiki/Category:LSL_Constants"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
---

# Common LSL Constants

## Boolean Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `TRUE` | 1 | Boolean true |
| `FALSE` | 0 | Boolean false |

## Key Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `NULL_KEY` | `"00000000-0000-0000-0000-000000000000"` | Invalid/empty UUID |

## Vector and Rotation Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `ZERO_VECTOR` | `<0.0, 0.0, 0.0>` | Zero vector |
| `ZERO_ROTATION` | `<0.0, 0.0, 0.0, 1.0>` | Identity rotation (no rotation) |

## Mathematical Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `PI` | 3.14159265... | π (180 degrees in radians) |
| `TWO_PI` | 6.28318530... | 2π (360 degrees in radians) |
| `PI_BY_TWO` | 1.57079632... | π/2 (90 degrees in radians) |
| `DEG_TO_RAD` | 0.01745329... | Multiply degrees by this to get radians |
| `RAD_TO_DEG` | 57.2957795... | Multiply radians by this to get degrees |
| `SQRT2` | 1.41421356... | √2 |

```lsl
// Convert degrees to radians
float radians = 45.0 * DEG_TO_RAD;

// Convert radians to degrees
float degrees = PI_BY_TWO * RAD_TO_DEG;  // = 90.0
```

## Chat Channel Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `PUBLIC_CHANNEL` | 0 | Open chat channel (channel 0) |
| `DEBUG_CHANNEL` | 0x7FFFFFFF (2147483647) | Script debug output |

## Inventory Type Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `INVENTORY_ALL` | -1 | All inventory types |
| `INVENTORY_NONE` | -1 | No inventory type |
| `INVENTORY_TEXTURE` | 0 | Texture |
| `INVENTORY_SOUND` | 1 | Sound |
| `INVENTORY_LANDMARK` | 3 | Landmark |
| `INVENTORY_CLOTHING` | 5 | Clothing |
| `INVENTORY_OBJECT` | 6 | Object |
| `INVENTORY_NOTECARD` | 7 | Notecard |
| `INVENTORY_SCRIPT` | 10 | Script |
| `INVENTORY_BODYPART` | 13 | Body part |
| `INVENTORY_ANIMATION` | 20 | Animation |
| `INVENTORY_GESTURE` | 21 | Gesture |
| `INVENTORY_SETTING` | 56 | Environment settings |
| `INVENTORY_MATERIAL` | 57 | GLTF material |

## EOF Constant

| Constant | Value | Description |
|----------|-------|-------------|
| `EOF` | `"\n\n\n"` | Returned by `llGetNotecardLine` when end of file reached |

## ALL_SIDES Constant

| Constant | Value | Description |
|----------|-------|-------------|
| `ALL_SIDES` | -1 | Target all faces of a prim in texture/colour operations |

## Agent Type Constants (for llSensor and llGetAgentInfo)

| Constant | Value | Description |
|----------|-------|-------------|
| `AGENT` | 0x1 | Human-controlled avatar |
| `ACTIVE` | 0x2 | Scripted and active (moving) object |
| `PASSIVE` | 0x4 | Non-scripted or stationary object |
| `SCRIPTED` | 0x8 | Object with active script |

## Usage Examples

```lsl
// Check for null key
key k = llDetectedKey(0);
if (k == NULL_KEY) return;

// Use math constants
rotation rot = llEuler2Rot(<0.0, 0.0, 45.0 * DEG_TO_RAD>);

// Sensor for all agents
llSensor("", NULL_KEY, AGENT, 10.0, TWO_PI);

// Set texture on all faces
llSetTexture("texture-uuid", ALL_SIDES);

// Check inventory count
integer count = llGetInventoryNumber(INVENTORY_NOTECARD);
```
