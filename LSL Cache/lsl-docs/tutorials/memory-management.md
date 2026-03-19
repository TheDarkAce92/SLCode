---
name: "Memory Management"
category: "tutorials"
type: "reference"
language: "LSL"
description: "Understanding the 64 KB Mono script memory limit, measuring free memory with llGetFreeMemory, capping usage with llSetMemoryLimit, and avoiding stack-heap collisions"
wiki_url: ""
local_only: true
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
---

# Memory Management

Each LSL script running under Mono has a maximum memory allocation of **64 KB (65,536 bytes)** for its runtime heap and call stack. If a script exhausts this allocation, it crashes with a stack-heap collision error.

## How Memory Is Laid Out

The 64 KB allocation is divided between two areas:

- **Stack** — holds the call stack and local variables; grows as functions are called.
- **Heap** — holds strings, lists, and other dynamically allocated data; grows as data is created.

A **stack-heap collision** occurs when these two regions exhaust the shared allocation. The script immediately stops executing and prints an error to the debug channel. There is no way to recover from a collision — the script must be reset.

## Checking Free Memory

`llGetFreeMemory()` returns the number of bytes of free memory available to the script **before garbage collection runs** — the actual free memory after a GC pass may be higher. `llGetUsedMemory()` returns how many bytes are currently in use:

```lsl
default
{
    touch_end(integer num_detected)
    {
        llSay(0, "Used: "  + (string)llGetUsedMemory()  + " bytes");
        llSay(0, "Free: "  + (string)llGetFreeMemory()  + " bytes");
        llSay(0, "Limit: " + (string)llGetMemoryLimit() + " bytes");
    }
}
```

This is a snapshot — the value fluctuates as strings and lists are created and released. Check it after the script has been running for a while and has allocated its typical working data.

A healthy script should have several thousand bytes free at its high-water mark. If `llGetFreeMemory()` drops below 2–4 KB during normal operation, the script is at risk of collisions.

## Capping Memory Usage with llSetMemoryLimit

`llSetMemoryLimit(integer bytes)` sets a hard ceiling on how much memory the script may use. The script is prevented from using more than this amount, regardless of the 64 KB physical limit.

This is useful when you want to leave headroom for other scripts in the same object, or to intentionally limit a script that should never need more than a certain amount:

```lsl
default
{
    state_entry()
    {
        llSetMemoryLimit(32768);  // cap at 32 KB
        llSay(0, "Memory capped. Free: " + (string)llGetFreeMemory());
    }
}
```

`llGetMemoryLimit()` returns the current limit. If you call `llSetMemoryLimit` with a value lower than the script's current memory usage, the call is silently ignored — the limit does not change.

## Common Causes of High Memory Use

### Large strings

Strings in LSL are copied on assignment. Building strings by concatenation in a loop is expensive:

```lsl
// Avoid — each concatenation allocates a new string
string result = "";
integer i;
for (i = 0; i < 100; i++)
    result += (string)i + ",";
```

Build lists and convert at the end, or process data incrementally rather than accumulating it in one string.

### Large lists

Lists in LSL are immutable value types. Every operation that modifies a list (insert, delete, replace) creates a new copy. A list with many entries, especially string entries, can consume significant heap space.

```lsl
// Each llListReplaceList call allocates a new list
list data = [];
integer i;
for (i = 0; i < 200; i++)
    data += [(string)i];  // growing list — heap grows with it
```

Discard lists when you no longer need them by assigning `[]`:

```lsl
data = [];  // releases the heap memory
```

### Deep call stacks

Recursive functions consume stack space quickly. LSL does not have tail-call optimisation. Avoid deep recursion — use iterative loops instead.

## Practical: Profiling at Startup

Log memory during `state_entry` to establish a baseline, then again after loading configuration or building data structures. Use `llGetUsedMemory()` to measure actual consumption — this is what you need when calling `llSetMemoryLimit` to set a tight cap:

```lsl
default
{
    state_entry()
    {
        llSay(0, "Startup used: " + (string)llGetUsedMemory());
        // ... load notecard, build lists, etc. ...
    }

    dataserver(key id, string data)
    {
        // ... process config ...
        llSay(0, "After load used: " + (string)llGetUsedMemory());
        // Set a tight limit once data is loaded — leave headroom for runtime use
        llSetMemoryLimit(llGetUsedMemory() + 4096);
    }
}
```

## Splitting Scripts Across Prims

If a single script genuinely cannot fit within 64 KB, split its responsibilities across multiple scripts in different prims and use `llMessageLinked` to coordinate them. Each script has its own independent 64 KB allocation.

## Key Numbers

| Value | Meaning |
|---|---|
| 65,536 bytes | Maximum runtime memory allocation per script (heap + stack) |
| `llGetFreeMemory()` | Bytes available before the current limit is hit |
| `llGetUsedMemory()` | Bytes currently in use |
| `llGetMemoryLimit()` | Current allocation cap (default: 65,536) |
| `llSetMemoryLimit(n)` | Set allocation cap to `n` bytes |

## Caveats

- `llGetFreeMemory()` and `llGetUsedMemory()` return snapshots — call them at the point of maximum expected load, not just at startup.
- Calling `llSetMemoryLimit` with a value lower than current usage is silently ignored — the limit does not change.
- Stack size is consumed by function call depth and local variable size; heap is consumed by strings and lists. Both count against the same 64 KB total.
- LSO (the older bytecode format) has a fixed 16 KB total limit for both bytecode and runtime memory. Mono is always preferred for new scripts.
- Memory is not shared between scripts even in the same prim — each script has its own 64 KB.
