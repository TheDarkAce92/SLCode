---
name: "Switch Statement"
category: pattern
tags: ["firestorm-only", "preprocessor", "control-flow"]
functions_used: []
sources: ["jyaoma/snippets.json"]
memory_impact: unknown
complexity: intermediate
firestorm_preprocessor_required: true
extracted: "2026-03-09"
last_reviewed: "2026-03-09"
has_versions: "true"
active_version: "scraped-unknown-2026-03-19"
---

# Switch Statement

Extracted from: jyaoma/snippets.json

## Code

```lsl
switch (${1:value})
{
	case (${2:case}):
	{
		$0
		break;
	}
	default:
	{
		break;
	}
}
```

> ⚠️ **Firestorm Preprocessor Required:** This pattern uses `switch/case/break` syntax that is **not valid native LSL**. It only works when compiled through the Firestorm viewer's built-in preprocessor. Do not use in projects with `firestorm_preprocessor: false`.

## When to Use

- When you need multi-branch dispatch on a single integer or string value (Firestorm projects only)
- As a more readable alternative to long if/else-if chains — but only when the Firestorm preprocessor is available

## Gotchas

- `switch/case/break` is preprocessor syntax — the SL compiler never sees it; Firestorm rewrites it to if/else before upload
- `break` without a matching `switch` causes a preprocessor error, not a runtime error
- Native LSL has no switch statement; use if/else chains for cross-viewer compatibility

## See Also

- `/lsl-docs/patterns/README.md`
