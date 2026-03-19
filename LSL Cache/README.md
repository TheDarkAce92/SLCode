# LSL Cache (Project Copy)

This folder is a **project-local copy** of the shared LSL cache, included to make this repository portable and easy to share.

## What this contains

- `cache-manifest.json` — cache state/version metadata
- `lsl-docs/` — cached LSL documentation, extension data, and pattern library
- `skills/` — shared automation/analysis skills used by the workflow

## Why it exists in this repo

Normally, the cache lives at `~/.lsl-cache` on a local machine. Including a copy here allows collaborators to:

- browse docs and patterns immediately
- run project tooling without re-fetching everything first
- start from a known baseline cache snapshot

## Intended usage

- Keep this folder as read-mostly reference data.
- Update it only when intentionally refreshing docs/extension sources.
- If refreshed, update `cache-manifest.json` and document changes in project logs.

## Notes for maintainers

- This cache can be large and change frequently.
- If repository size becomes a concern, consider publishing cache snapshots as release assets instead of keeping every update in main history.
