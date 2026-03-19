# Skill: doc-format-reference
# Version: 0.1.0.0
# Purpose: YAML front matter format reference for all LSL doc file types
# Usage: Read this file only when creating or updating a doc file in lsl-docs/
# Created: 2026-03-09
# Last modified: 2026-03-09

---

# Doc File Format Reference

This file defines the required YAML front matter for every file saved to `~/.lsl-cache/lsl-docs/`.
Only read this file when creating or merging a doc file — do not load it for code or lookup queries.

---

## Function Doc — Full Example

```yaml
---
name: "llSay"
category: "functions"
type: "function"
language: "LSL"
description: "Broadcasts a message on the specified channel within 20m."
wiki_url: "https://wiki.secondlife.com/wiki/LlSay"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "llSay(integer channel, string msg)"
parameters:
  - name: "channel"
    type: "integer"
    description: "Channel to speak on. 0 = public chat."
  - name: "msg"
    type: "string"
    description: "The message to broadcast."
return_type: "void"
energy_cost: 10.0
sleep_time: 0.0
deprecated: false
see_also: ["llWhisper", "llShout", "llRegionSay", "llOwnerSay"]
patterns: []
---
```

**Required fields:** `name`, `category`, `type`, `language`, `description`, `wiki_url`, `first_fetched`, `last_updated`
**Optional but strongly encouraged:** `signature`, `parameters`, `return_type`, `energy_cost`, `sleep_time`, `deprecated`, `see_also`
**Added after pattern analysis:** `patterns` (list of pattern file stems that use this function)

---

## Event Doc — Full Example

```yaml
---
name: "touch_start"
category: "events"
type: "event"
language: "LSL"
description: "Triggered when an agent begins touching the object."
wiki_url: "https://wiki.secondlife.com/wiki/Touch_start"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "touch_start(integer num_detected)"
parameters:
  - name: "num_detected"
    type: "integer"
    description: "Number of agents detected touching the object (1–16)."
see_also: ["touch", "touch_end", "llDetectedKey", "llDetectedName"]
---
```

---

## Constant Doc — Full Example

```yaml
---
name: "PRIM_TYPE"
category: "constants"
type: "constant"
language: "LSL"
description: "Parameter flag for llSetPrimitiveParams/llGetPrimitiveParams to set/get prim shape type."
wiki_url: "https://wiki.secondlife.com/wiki/PRIM_TYPE"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
value: "9"
value_type: "integer"
see_also: ["llSetPrimitiveParams", "llGetPrimitiveParams", "PRIM_TYPE_BOX", "PRIM_TYPE_SPHERE"]
---
```

---

## Reference Doc (types, operators, flow-control, etc.) — Full Example

```yaml
---
name: "LSL Types"
category: "reference"
type: "reference"
language: "LSL"
description: "All LSL data types: integer, float, string, key, vector, rotation, list."
wiki_url: "https://wiki.secondlife.com/wiki/LSL_Types"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
---
```

---

## Tutorial Doc — Full Example

```yaml
---
name: "LSL Hello Avatar"
category: "tutorials"
type: "tutorial"
language: "LSL"
description: "Introductory tutorial: detecting a touch and greeting the toucher by name."
wiki_url: "https://wiki.secondlife.com/wiki/LSL_Tutorial/Hello_Avatar"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
functions_used: ["llSay", "llDetectedName", "llDetectedKey"]
difficulty: "beginner"
---
```

---

## Merge Policy (applies to all doc types)

When re-fetching a doc that already exists:
1. **Never overwrite** existing content.
2. Update only `last_updated` in the front matter.
3. Append changed or new content below a dated update block:

```markdown
---
### 📝 Update — YYYY-MM-DD
_Changes detected from re-fetch. Original content preserved above._
<new or changed content here>
---
```

4. If a page was removed from the source, retain content and add:

```markdown
> ⚠️ **Archival note (YYYY-MM-DD):** This content was no longer present at the source URL. Retained for historical reference.
```
