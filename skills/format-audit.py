#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_FIELDS = ("name", "category", "type", "language", "description")
DOC_KINDS_WITH_FENCE = {"script", "notecard", "config", "license"}
DOC_KINDS = DOC_KINDS_WITH_FENCE | {"user-doc"}
KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):")
DOC_KIND_RE = re.compile(r'^source_doc_kind:\s*"?([^"\n]+)"?\s*$', re.M)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit lsl-docs markdown front matter and doc-kind body layout."
    )
    parser.add_argument(
        "--root",
        default="LSL Cache/lsl-docs/examples",
        help="Root folder to scan (default: LSL Cache/lsl-docs/examples)",
    )
    parser.add_argument(
        "--max-errors",
        type=int,
        default=20,
        help="Maximum examples to print per error category (default: 20)",
    )
    return parser.parse_args()


def read_front_matter(text: str) -> tuple[str, str] | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        return None
    front_matter = text[4:end]
    body = text[end + 5 :]
    return front_matter, body


def collect_fields(front_matter: str) -> set[str]:
    fields: set[str] = set()
    for line in front_matter.splitlines():
        match = KEY_RE.match(line)
        if match:
            fields.add(match.group(1))
    return fields


def is_examples_doc(file_path: Path) -> bool:
    return "examples" in {part.lower() for part in file_path.parts}


def main() -> int:
    args = parse_args()
    root = Path(args.root)

    if not root.exists():
        print(f"ERROR: root not found: {root}")
        return 2

    files = sorted(root.rglob("*.md"))

    invalid_front_matter: list[tuple[Path, str]] = []
    missing_required: list[tuple[Path, list[str]]] = []
    bad_doc_kind: list[tuple[Path, str]] = []
    layout_issues: list[tuple[Path, str]] = []
    doc_kind_counts: dict[str, int] = {}

    scanned = 0
    for file_path in files:
        text = file_path.read_text(encoding="utf-8", errors="replace")
        parsed = read_front_matter(text)
        if parsed is None:
            invalid_front_matter.append((file_path, "missing or unterminated front matter"))
            continue

        scanned += 1
        front_matter, body = parsed
        fields = collect_fields(front_matter)

        if is_examples_doc(file_path):
            missing = [key for key in REQUIRED_FIELDS if key not in fields]
            if missing:
                missing_required.append((file_path, missing))

        kind_match = DOC_KIND_RE.search(front_matter)
        if kind_match:
            doc_kind = kind_match.group(1).strip()
            doc_kind_counts[doc_kind] = doc_kind_counts.get(doc_kind, 0) + 1

            if doc_kind not in DOC_KINDS:
                bad_doc_kind.append((file_path, doc_kind))
            else:
                has_fence = "```" in body
                if doc_kind in DOC_KINDS_WITH_FENCE and not has_fence:
                    layout_issues.append((file_path, f"expected fenced code/text block for {doc_kind}"))
                if doc_kind == "user-doc" and has_fence:
                    layout_issues.append((file_path, "user-doc should be plain text (no fenced block)"))

    print(f"TOTAL_MD={len(files)}")
    print(f"SCANNED_WITH_VALID_FRONT_MATTER={scanned}")
    print(f"INVALID_FRONT_MATTER={len(invalid_front_matter)}")
    print(f"MISSING_REQUIRED_FIELDS={len(missing_required)}")
    print(f"INVALID_SOURCE_DOC_KIND={len(bad_doc_kind)}")
    print(f"LAYOUT_ISSUES={len(layout_issues)}")

    if doc_kind_counts:
        pairs = ", ".join(f"{key}:{value}" for key, value in sorted(doc_kind_counts.items()))
        print(f"SOURCE_DOC_KIND_COUNTS={pairs}")

    limit = max(args.max_errors, 0)

    if invalid_front_matter:
        print("\nINVALID_FRONT_MATTER_EXAMPLES:")
        for file_path, reason in invalid_front_matter[:limit]:
            print(f" - {file_path} :: {reason}")

    if missing_required:
        print("\nMISSING_REQUIRED_FIELDS_EXAMPLES:")
        for file_path, missing in missing_required[:limit]:
            print(f" - {file_path} :: missing={','.join(missing)}")

    if bad_doc_kind:
        print("\nINVALID_SOURCE_DOC_KIND_EXAMPLES:")
        for file_path, kind in bad_doc_kind[:limit]:
            print(f" - {file_path} :: source_doc_kind={kind}")

    if layout_issues:
        print("\nLAYOUT_ISSUE_EXAMPLES:")
        for file_path, reason in layout_issues[:limit]:
            print(f" - {file_path} :: {reason}")

    has_errors = any(
        (
            invalid_front_matter,
            missing_required,
            bad_doc_kind,
            layout_issues,
        )
    )
    return 1 if has_errors else 0


if __name__ == "__main__":
    sys.exit(main())
