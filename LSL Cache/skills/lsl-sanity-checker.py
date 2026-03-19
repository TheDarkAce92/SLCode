#!/usr/bin/env python3
# Skill: lsl-sanity-checker
# Version: 0.1.2.1
# Purpose: Deep sanity checks for LSL scripts — argument counts, jump/label
#          consistency, state transitions, duplicate declarations, llDialog
#          button constraints, and HypnoVisor link-message protocol.
#          Now includes lslint validation for enhanced syntax checking.
# Usage:   python3 ~/.lsl-cache/skills/lsl-sanity-checker.py [file.lsl ...]
#          python3 ~/.lsl-cache/skills/lsl-sanity-checker.py --all [dir]
#          python3 ~/.lsl-cache/skills/lsl-sanity-checker.py --project  (HV protocol checks)
#          python3 ~/.lsl-cache/skills/lsl-sanity-checker.py --json [file.lsl ...]  (JSON output)
# Created: 2026-03-10
# Last modified: 2026-03-15

import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from collections import defaultdict
import subprocess

# ─── Cache paths ──────────────────────────────────────────────────────────────
_env_base  = os.environ.get("LSL_CACHE_BASE", "").strip()
CACHE_PATH = Path(_env_base) if _env_base else Path(__file__).resolve().parents[1]
JYAOMA_DIR = CACHE_PATH / "lsl-docs/vscode-extension-data/jyaoma"
PYOPT_DIR  = CACHE_PATH / "lsl-docs/vscode-extension-data/pyoptimizer"
KWDB_FILE  = CACHE_PATH / "lsl-docs/vscode-extension-data/kwdb/kwdb.xml"

LSL_TYPES = {"integer", "float", "string", "key", "vector", "rotation", "list"}
FLOW_KW   = {"if", "else", "while", "for", "do", "return", "jump",
             "state", "default", "void"}

# Functions whose documented param count in the cache is wrong — override here.
# Values are the TRUE param count as per the SL wiki.
PARAM_COUNT_OVERRIDES = {
    "llAdjustSoundVolume":   1,   # llAdjustSoundVolume(float volume)
    "llSetSoundRadius":      1,   # llSetSoundRadius(float radius)
    "llSetSoundQueueing":    1,   # llSetSoundQueueing(integer queue)
    "llSetSoundVolume":      2,   # llSetSoundVolume(float volume, key id)  — keep cache
    "llGetLinkKey":          1,   # llGetLinkKey(integer link) — jyaoma data has wrong 2-param entry
    "llLinksetDataRead":     1,   # llLinksetDataRead(string key) — jyaoma incorrectly includes pass param
    "llLinksetDataWrite":    2,   # llLinksetDataWrite(string key, string value) — jyaoma incorrectly includes pass param
    "llLinksetDataDelete":   1,   # llLinksetDataDelete(string key) — jyaoma incorrectly includes pass param
}

# Functions whose argument count is variadic or otherwise not checkable
VARIADIC_FUNCS = {
    "llList2List", "llSetPrimitiveParams", "llGetPrimitiveParams",
    "llSetLinkPrimitiveParams", "llSetLinkPrimitiveParamsFast",
    "llParseString2List", "llParseStringKeepNulls",
    "llDumpList2String", "llCSV2List", "llList2CSV",
    "llListSort", "llListRandomize",
    "llSetPrimMediaParams", "llGetPrimMediaParams",
    "llSetPrimMediaParamsFast",
    "llDetectedTouchUV", "llDetectedTouchST",
    "llRequestAgentData",
    "llSetKeyframedMotion",
    "llSetPhysicsMaterial",
    "llCreateCharacter", "llUpdateCharacter",
    "llNavigateTo", "llPatrolPoints", "llEvade", "llFleeFrom",
    "llWander", "llPursue",
    "llSetMemoryLimit",
    "llGetEnvironment",
    "llSetEnvironment",
    "llScaleByFactor",
    # HV-project string-building helpers that wrap built-ins
}

# Known HV link-message key tags and string prefixes for protocol consistency
HV_STR_PREFIXES = {
    "fw_data", "fw_conf",         # FURWARE
    "overlay|",                    # Overlay Handler
    "audio|",                      # Audio Handler
    "image|",                      # Image Layer
    "cDA-Set|", "cDA-Reply|",      # childDeltaAlpha
    "overlay-Reply|", "audio-Reply|", "image-Reply|", "sfx-Reply|",  # gate replies
    "sfx|",                        # SFX Handler
    "hud|",                        # HUD Presence (show/hide)
    "TS_CHAN|", "TS_CHAN:",         # Text Sequencer channel broadcast
    "hs|",                         # HypnoSpec Loader
    "play",                        # Files.lsl session broadcast
    "notecard|",                   # Text Sequencer notecard load
}

# llMessageLinked key values that indicate special routing
HV_KEY_TAGS = {
    "fw_data", "fw_conf",
    "",                            # empty string key = general broadcast
}


# ══════════════════════════════════════════════════════════════════════════════
# Cache loading (mirrors syntax-checker; kept self-contained)
# ══════════════════════════════════════════════════════════════════════════════

def load_known_functions():
    funcs = {}

    builtins_path = PYOPT_DIR / "builtins.txt"
    if builtins_path.exists():
        with open(builtins_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("//") or line.startswith("#"):
                    continue
                m = re.match(r'(\w+)\s+(\w+)\s*\(([^)]*)\)', line)
                if m:
                    ret_type, fname, params_str = m.groups()
                    params = [p.strip() for p in params_str.split(",") if p.strip()]
                    funcs[fname] = {
                        "return_type": ret_type,
                        "param_count": len(params),
                        "param_types": [p.split()[0] if p.split() else "?" for p in params],
                        "sleep": 0.0,
                    }

    jyaoma_path = JYAOMA_DIR / "functions.json"
    if jyaoma_path.exists():
        with open(jyaoma_path, encoding="utf-8") as f:
            jdata = json.load(f)
        for fname, fdata in jdata.items():
            params = fdata.get("parameters", [])
            entry = funcs.get(fname, {})
            entry.update({
                "return_type": fdata.get("returnType", entry.get("return_type", "")),
                "param_count": len(params),
                "param_types": [p.get("type", "?") for p in params],
                "sleep":       fdata.get("sleep", entry.get("sleep", 0.0)),
            })
            funcs[fname] = entry

    if KWDB_FILE.exists():
        try:
            tree = ET.parse(KWDB_FILE)
            root = tree.getroot()
            for elem in root.iter("function"):
                fname = elem.get("name")
                if fname and fname not in funcs:
                    params = list(elem.iter("param"))
                    funcs[fname] = {
                        "return_type": elem.get("type", ""),
                        "param_count": len(params),
                        "param_types": [p.get("type", "?") for p in params],
                        "sleep": 0.0,
                    }
        except ET.ParseError:
            pass

    # Apply manual overrides (correct cache errors)
    for fname, correct_count in PARAM_COUNT_OVERRIDES.items():
        if fname in funcs:
            funcs[fname]["param_count"] = correct_count

    return funcs


# ══════════════════════════════════════════════════════════════════════════════
# Tokenizer (same as syntax-checker, reproduced here for standalone use)
# ══════════════════════════════════════════════════════════════════════════════

def tokenize(src):
    tokens = []
    i = 0
    line = 1
    n = len(src)
    while i < n:
        c = src[i]
        if c == '\n':
            line += 1; i += 1; continue
        if c in ' \t\r':
            i += 1; continue
        if src[i:i+2] == '/*':
            end = src.find('*/', i + 2)
            if end == -1:
                break
            line += src[i:end+2].count('\n')
            i = end + 2; continue
        if src[i:i+2] == '//':
            while i < n and src[i] != '\n':
                i += 1
            continue
        if c == '"':
            j = i + 1
            while j < n:
                if src[j] == '\\':
                    j += 2
                elif src[j] == '"':
                    j += 1; break
                elif src[j] == '\n':
                    line += 1; j += 1
                else:
                    j += 1
            tokens.append(('STRING', src[i:j], line))
            i = j; continue
        if src[i:i+2] in ('0x', '0X') and i + 2 < n:
            j = i + 2
            while j < n and src[j] in '0123456789abcdefABCDEF':
                j += 1
            tokens.append(('NUMBER', src[i:j], line))
            i = j; continue
        if c.isdigit():
            j = i
            while j < n and src[j].isdigit():
                j += 1
            is_float = j < n and src[j] == '.'
            if is_float:
                j += 1
                while j < n and src[j].isdigit():
                    j += 1
                if j < n and src[j] in 'eE':
                    j += 1
                    if j < n and src[j] in '+-':
                        j += 1
                    while j < n and src[j].isdigit():
                        j += 1
                tokens.append(('FLOAT', src[i:j], line))
            else:
                tokens.append(('INTEGER', src[i:j], line))
            i = j; continue
        if c.isalpha() or c == '_':
            j = i
            while j < n and (src[j].isalnum() or src[j] == '_'):
                j += 1
            tokens.append(('IDENT', src[i:j], line))
            i = j; continue
        two = src[i:i+2]
        if two in ('++', '--', '==', '!=', '<=', '>=', '&&', '||',
                   '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=',
                   '<<', '>>', '...'):
            tokens.append(('OP', two, line)); i += 2; continue
        tokens.append(('PUNCT', c, line)); i += 1
    return tokens


# ══════════════════════════════════════════════════════════════════════════════
# Declaration extraction
# ══════════════════════════════════════════════════════════════════════════════

def extract_declarations(tokens):
    """
    Returns:
        user_funcs  : dict  name → {line, param_count, return_type, start_tok, end_tok}
        global_vars : dict  name → line
        state_names : set
    """
    user_funcs  = {}
    global_vars = {}
    state_names = set()

    LSL_TYPE_TOKENS = LSL_TYPES | {"void"}

    depth = 0
    i = 0
    n = len(tokens)
    while i < n:
        ttype, tval, tline = tokens[i]

        if tval == '{':
            depth += 1; i += 1; continue
        if tval == '}':
            if depth > 0: depth -= 1
            i += 1; continue

        if depth > 0:
            i += 1; continue

        # state NAME
        if ttype == 'IDENT' and tval == 'state' and i + 1 < n:
            if tokens[i+1][0] == 'IDENT':
                state_names.add(tokens[i+1][1])
            i += 2; continue
        if ttype == 'IDENT' and tval == 'default':
            state_names.add('default')
            i += 1; continue

        # void-return user function:  IDENT  (  ...  )  {
        _NON_FUNC = LSL_TYPE_TOKENS | FLOW_KW
        if (ttype == 'IDENT' and tval not in _NON_FUNC
                and i + 1 < n and tokens[i+1][1] == '('):
            j, pcnt = _scan_params(tokens, i + 2, n)
            if j < n and tokens[j][1] == '{':
                body_start, body_end = _find_body(tokens, j, n)
                user_funcs[tval] = {
                    "line": tline, "param_count": pcnt,
                    "return_type": "void",
                    "start_tok": body_start, "end_tok": body_end,
                }
                # Skip past the entire function (params + body) so that
                # parameter declarations are not mistaken for global vars.
                i = body_end + 1; continue

        # typed function or global variable:  TYPE  IDENT  ...
        if ttype == 'IDENT' and tval in LSL_TYPE_TOKENS:
            if i + 1 < n and tokens[i+1][0] == 'IDENT':
                name  = tokens[i+1][1]
                rtype = tval
                if i + 2 < n and tokens[i+2][1] == '(':
                    j, pcnt = _scan_params(tokens, i + 3, n)
                    if j < n and tokens[j][1] == '{':
                        body_start, body_end = _find_body(tokens, j, n)
                        if name in user_funcs:
                            user_funcs[name + "_DUP"] = user_funcs[name]  # mark dupe
                        user_funcs[name] = {
                            "line": tline, "param_count": pcnt,
                            "return_type": rtype,
                            "start_tok": body_start, "end_tok": body_end,
                        }
                        # Skip past the entire function so params aren't
                        # mistaken for global variable declarations.
                        i = body_end + 1; continue
                else:
                    if name in global_vars:
                        global_vars[name + "_DUP"] = tline
                    else:
                        global_vars[name] = tline
                    i += 2; continue
        i += 1

    return user_funcs, global_vars, state_names


def _scan_params(tokens, start, n):
    """Skip past parameter list starting after '('. Returns (index_after_close_paren, param_count)."""
    if start >= n or tokens[start][1] == ')':
        return start + (1 if start < n else 0), 0
    param_count = 1
    depth = 1
    j = start
    while j < n:
        v = tokens[j][1]
        if v in ('(', '['):
            depth += 1
        elif v in (')', ']'):
            depth -= 1
            if depth == 0:
                return j + 1, param_count
        elif v == ',' and depth == 1:
            param_count += 1
        j += 1
    return j, param_count


def _find_body(tokens, open_brace_idx, n):
    """Find matching closing brace. Returns (open_brace_idx, close_brace_idx)."""
    depth = 0
    for j in range(open_brace_idx, n):
        if tokens[j][1] == '{':
            depth += 1
        elif tokens[j][1] == '}':
            depth -= 1
            if depth == 0:
                return open_brace_idx, j
    return open_brace_idx, n - 1


def get_func_body_tokens(tokens, func_info):
    """Return token slice for a function's body (between braces, exclusive)."""
    s = func_info.get("start_tok", 0)
    e = func_info.get("end_tok", len(tokens))
    return tokens[s:e+1]


# ══════════════════════════════════════════════════════════════════════════════
# Check: argument count at call sites
# ══════════════════════════════════════════════════════════════════════════════

def check_arg_counts(tokens, known_funcs, user_funcs):
    """
    Verify every call site passes the correct number of arguments.
    Skips variadic functions and user-defined functions (param count from
    source is authoritative, call count is checked against it).
    """
    issues = []
    n = len(tokens)
    all_funcs = {}
    for fname, info in known_funcs.items():
        all_funcs[fname] = info.get("param_count", -1)
    for fname, info in user_funcs.items():
        all_funcs[fname] = info.get("param_count", -1)

    i = 0
    while i < n:
        ttype, tval, tline = tokens[i]
        # Candidate call: IDENT immediately followed by '('
        if ttype == 'IDENT' and i + 1 < n and tokens[i+1][1] == '(':
            # Skip declarations (at depth 0 followed by '{' after params)
            # Simple heuristic: if the previous token is a type keyword → declaration
            prev_val = tokens[i-1][1] if i > 0 else ""
            if prev_val in (LSL_TYPES | {"void"}):
                i += 1; continue
            # Skip type-cast syntax like (integer)(expr)
            if prev_val == '(':
                i += 1; continue
            # Skip flow keywords
            if tval in FLOW_KW:
                i += 1; continue

            expected = all_funcs.get(tval, -2)  # -2 = unknown function
            if expected == -2 or tval in VARIADIC_FUNCS:
                i += 1; continue

            # Count actual args
            j = i + 2  # skip IDENT and '('
            actual, j_after = _count_call_args(tokens, j, n)

            if actual != expected:
                issues.append(("ERROR", "A001", tline,
                    f"'{tval}' called with {actual} arg(s), expected {expected}"))
        i += 1
    return issues


def _count_call_args(tokens, start, n):
    """Count comma-separated args in a call (starting after the opening '(').
    Returns (arg_count, index_after_closing_paren).
    '<' and '>' are treated as depth markers for vector/rotation literals
    so that <0.4, 1.0, 0.4> is counted as one argument, not three."""
    if start >= n:
        return 0, start
    # Immediate close paren → 0 args
    if tokens[start][1] == ')':
        return 0, start + 1
    count = 1
    depth = 1
    j = start
    while j < n:
        v = tokens[j][1]
        if v in ('(', '[', '<'):
            depth += 1
        elif v in (')', ']'):
            depth -= 1
            if depth == 0:
                return count, j + 1
        elif v == '>' and depth > 1:
            # Only decrement on '>' if we are inside a nested scope —
            # avoids treating comparison operators as closing brackets.
            depth -= 1
        elif v == ',' and depth == 1:
            count += 1
        j += 1
    return count, j


# ══════════════════════════════════════════════════════════════════════════════
# Check: jump / @label consistency within each function
# ══════════════════════════════════════════════════════════════════════════════

def check_jump_labels(tokens, user_funcs, state_names):
    """
    For each function body, collect all @label definitions and all `jump target`
    calls. Flag jumps whose target label is not defined in the same function.
    Also flag defined labels that are never jumped to (INFO).
    """
    issues = []
    n = len(tokens)

    # Build state bodies: scan at depth 0 for state blocks, then depth 1 for
    # event bodies, then depth 2+ for the function bodies themselves.
    # For simplicity, analyse each user_func body independently.

    for fname, info in user_funcs.items():
        if fname.endswith("_DUP"):
            continue
        body = get_func_body_tokens(tokens, info)
        labels_defined = {}   # label_name → line
        labels_jumped  = {}   # label_name → line (first jump to it)

        bi = 0
        bn = len(body)
        while bi < bn:
            btype, bval, bline = body[bi]
            # @label definition
            if bval == '@' and bi + 1 < bn and body[bi+1][0] == 'IDENT':
                lname = body[bi+1][1]
                if lname in labels_defined:
                    issues.append(("WARN", "J002", bline,
                        f"Duplicate label '@{lname}' in function '{fname}'"))
                else:
                    labels_defined[lname] = bline
                bi += 2; continue
            # jump target
            if btype == 'IDENT' and bval == 'jump' and bi + 1 < bn:
                target = body[bi+1][1]
                if target not in labels_jumped:
                    labels_jumped[target] = bline
                bi += 2; continue
            bi += 1

        for target, jline in labels_jumped.items():
            if target not in labels_defined:
                issues.append(("ERROR", "J001", jline,
                    f"'jump {target}' in '{fname}' — label '@{target}' not defined in this function"))
        for lname, lline in labels_defined.items():
            if lname not in labels_jumped:
                issues.append(("INFO", "J003", lline,
                    f"Label '@{lname}' in '{fname}' is defined but never jumped to"))

    return issues


# ══════════════════════════════════════════════════════════════════════════════
# Check: state transitions reference declared states
# ══════════════════════════════════════════════════════════════════════════════

def check_state_transitions(tokens, state_names):
    """Flag 'state X' where X is not a declared state in this file.
    Requires the next token to be an IDENT so that 'state' used as a
    local variable name (e.g. 'integer state = 0') is not misread."""
    issues = []
    n = len(tokens)
    for i, (ttype, tval, tline) in enumerate(tokens):
        if ttype == 'IDENT' and tval == 'state' and i + 1 < n:
            next_ttype, target, _ = tokens[i+1]
            # Only a genuine state transition has an IDENT immediately after 'state'
            if next_ttype != 'IDENT':
                continue
            if target in ('default', 'entry'):
                continue
            if target not in state_names:
                issues.append(("ERROR", "ST01", tline,
                    f"'state {target}' — state '{target}' is not declared in this file"))
    return issues


# ══════════════════════════════════════════════════════════════════════════════
# Check: duplicate global / function declarations
# ══════════════════════════════════════════════════════════════════════════════

def check_duplicates(user_funcs, global_vars):
    issues = []
    for name in list(user_funcs.keys()):
        if name.endswith("_DUP"):
            real = name[:-4]
            line = user_funcs[real]["line"]
            issues.append(("ERROR", "D001", line,
                f"Duplicate function declaration '{real}'"))
    for name in list(global_vars.keys()):
        if name.endswith("_DUP"):
            real = name[:-4]
            line = global_vars[real]
            issues.append(("ERROR", "D002", line,
                f"Duplicate global variable declaration '{real}'"))
    return issues


# ══════════════════════════════════════════════════════════════════════════════
# Check: llDialog / llTextBox button constraints
# ══════════════════════════════════════════════════════════════════════════════

def check_dialog_buttons(tokens):
    """
    Look for  llDialog(id, msg, [...], chan)  calls where the button list
    is a literal [...] immediately in the source. Check:
      - No more than 12 buttons
      - Each button string ≤ 24 characters
    Also check llTextBox message arg for obvious issues.
    """
    issues = []
    n = len(tokens)

    i = 0
    while i < n:
        ttype, tval, tline = tokens[i]
        if ttype != 'IDENT' or tval not in ('llDialog', 'llTextBox'):
            i += 1; continue

        fname = tval
        # Expect '(' next
        if i + 1 >= n or tokens[i+1][1] != '(':
            i += 1; continue

        # Collect the full argument token list
        arg_tokens, end_idx = _extract_call_args_tokens(tokens, i + 2, n)
        i = end_idx

        if fname == 'llDialog':
            # args: id, msg, list, chan  → list is arg index 2
            if len(arg_tokens) < 3:
                continue
            list_arg = arg_tokens[2]

            # list_arg is a list of token slices (all tokens of that argument).
            # Check if it's a literal [...] list.
            if not list_arg:
                continue
            if list_arg[0][1] != '[':
                continue  # dynamic list expression — can't check statically

            # Extract string literals from the list
            buttons = []
            for tok in list_arg:
                if tok[0] == 'STRING':
                    # Strip surrounding quotes
                    s = tok[1][1:-1]
                    # Unescape \" sequences
                    s = s.replace('\\"', '"').replace('\\\\', '\\')
                    buttons.append((s, tok[2]))

            if len(buttons) > 12:
                issues.append(("ERROR", "UI01", tline,
                    f"llDialog has {len(buttons)} buttons — LSL maximum is 12"))
            for btn_text, btn_line in buttons:
                if len(btn_text) > 24:
                    issues.append(("WARN", "UI02", btn_line,
                        f"llDialog button '{btn_text[:20]}…' is {len(btn_text)} chars "
                        f"— buttons are truncated at 24 chars in-world"))

    return issues


def _extract_call_args_tokens(tokens, start, n):
    """
    From position `start` (after the opening '(' of a call), extract
    each argument as a list of tokens.
    Returns (list_of_arg_token_lists, index_after_close_paren).
    """
    args = []
    current = []
    depth = 1  # we are inside the outer '('
    j = start

    while j < n:
        ttype, tval, tline = tokens[j]
        if tval in ('(', '['):
            depth += 1
            current.append(tokens[j])
        elif tval in (')', ']'):
            depth -= 1
            if depth == 0:
                args.append(current)
                return args, j + 1
            current.append(tokens[j])
        elif tval == ',' and depth == 1:
            args.append(current)
            current = []
        else:
            current.append(tokens[j])
        j += 1

    args.append(current)
    return args, j


# ══════════════════════════════════════════════════════════════════════════════
# Check: integer literal overflow
# ══════════════════════════════════════════════════════════════════════════════

def check_integer_overflow(tokens):
    """Flag integer literals larger than 2^31-1 (LSL max positive int)."""
    issues = []
    MAX_INT = 2**31 - 1
    for ttype, tval, tline in tokens:
        if ttype == 'INTEGER':
            try:
                v = int(tval, 0)  # handles 0x prefix
                if v > MAX_INT:
                    issues.append(("WARN", "N001", tline,
                        f"Integer literal {tval} exceeds LSL max ({MAX_INT}) "
                        f"— will overflow to negative at runtime"))
            except ValueError:
                pass
    return issues


# ══════════════════════════════════════════════════════════════════════════════
# Check: unused globals (heuristic)
# ══════════════════════════════════════════════════════════════════════════════

def check_unused_globals(tokens, global_vars):
    """
    Flag global variables that appear only once in the token stream
    (i.e. their declaration) and never used.
    This is a heuristic: false negatives possible for dynamically-constructed names.
    """
    issues = []
    # Count mentions of each global name
    counts = defaultdict(int)
    for ttype, tval, _ in tokens:
        if ttype == 'IDENT':
            counts[tval] += 1

    for name, decl_line in global_vars.items():
        if name.endswith("_DUP"):
            continue
        # Declaration accounts for 1 mention; if total == 1, never used
        if counts.get(name, 0) <= 1:
            issues.append(("INFO", "U001", decl_line,
                f"Global variable '{name}' appears to be declared but never used"))
    return issues


# Check: missing return in non-void functions
# ══════════════════════════════════════════════════════════════════════════════

def check_missing_return(tokens, user_funcs):
    """
    For non-void user-defined functions, check that the token stream
    contains at least one 'return' with a following value expression.
    (Heuristic: can't do full control-flow analysis.)
    """
    issues = []
    for fname, info in user_funcs.items():
        if fname.endswith("_DUP"):
            continue
        rtype = info.get("return_type", "void")
        if rtype in ("void", ""):
            continue
        body = get_func_body_tokens(tokens, info)
        has_return_value = False
        bi = 0
        bn = len(body)
        while bi < bn:
            btype, bval, bline = body[bi]
            if btype == 'IDENT' and bval == 'return':
                if bi + 1 < bn and body[bi+1][1] != ';':
                    has_return_value = True
                    break
            bi += 1
        if not has_return_value:
            issues.append(("WARN", "R003", info["line"],
                f"Non-void function '{fname}' (returns {rtype}) has no 'return <value>' statement"))
    return issues


# ══════════════════════════════════════════════════════════════════════════════
# Check: potential memory leaks from unclosed listeners/timers
# ══════════════════════════════════════════════════════════════════════════════

def check_resource_leaks(tokens):
    """
    Check for potential resource leaks:
    - llListen without corresponding llListenRemove
    - llSetTimerEvent without llSetTimerEvent(0.0) to clear
    - Large string literals that might cause memory issues
    """
    issues = []
    n = len(tokens)

    # Track resource allocations
    listens_active = False
    timer_active = False
    listen_line = 0
    timer_line = 0

    for i, (ttype, tval, tline) in enumerate(tokens):
        if ttype == 'IDENT':
            if tval == 'llListen' and i + 1 < n and tokens[i+1][1] == '(':
                if not listens_active:
                    listens_active = True
                    listen_line = tline
            elif tval == 'llListenRemove' and i + 1 < n and tokens[i+1][1] == '(':
                listens_active = False
            elif tval == 'llSetTimerEvent' and i + 1 < n and tokens[i+1][1] == '(':
                # Check if it's setting a non-zero timer
                if i + 2 < n and tokens[i+2][1] != ')':
                    # Look for a numeric argument
                    j = i + 2
                    while j < n and tokens[j][1] != ')':
                        if tokens[j][0] in ('NUMBER', 'FLOAT', 'INTEGER'):
                            try:
                                val = float(tokens[j][1])
                                if val > 0:
                                    timer_active = True
                                    timer_line = tline
                                else:
                                    timer_active = False
                                break
                            except ValueError:
                                pass
                        j += 1
            elif tval == 'llSetTimerEvent' and timer_active:
                # Check if clearing timer
                if i + 2 < n and tokens[i+2][1] != ')':
                    j = i + 2
                    while j < n and tokens[j][1] != ')':
                        if tokens[j][0] in ('NUMBER', 'FLOAT', 'INTEGER'):
                            try:
                                val = float(tokens[j][1])
                                if val == 0:
                                    timer_active = False
                                break
                            except ValueError:
                                pass
                        j += 1

    if listens_active:
        issues.append(("WARN", "R001", listen_line,
            "llListen() called without llListenRemove() -- listener handle may leak"))
    if timer_active:
        issues.append(("INFO", "R002", timer_line,
            "llSetTimerEvent() called without clearing -- timer may remain active"))

    return issues


# Check: suspicious string operations
# ══════════════════════════════════════════════════════════════════════════════

def check_string_operations(tokens):
    """Check for potentially problematic string operations."""
    issues = []
    n = len(tokens)

    for i, (ttype, tval, tline) in enumerate(tokens):
        if ttype == 'IDENT' and tval == 'llStringToBase64':
            # Check for very long strings being base64 encoded
            # This can cause URI length issues or memory problems
            if i > 0 and tokens[i-1][0] == 'STRING':
                str_content = tokens[i-1][1]
                # Rough estimate: base64 is ~33% larger
                if len(str_content) > 500:  # arbitrary threshold
                    issues.append(("INFO", "S001", tline,
                        f"Very long string ({len(str_content)} chars) passed to llStringToBase64 -- "
                        f"may exceed PRIM_MEDIA_CURRENT_URL limit (1024 chars)"))

        elif ttype == 'IDENT' and tval in ('llList2String', 'llDumpList2String'):
            # Check for large lists being converted to strings
            issues.append(("INFO", "S002", tline,
                f"'{tval}' may create very long strings -- consider memory limits"))

    return issues


# ══════════════════════════════════════════════════════════════════════════════
# Check: ternary operator usage
# ══════════════════════════════════════════════════════════════════════════════

def check_ternary_operators(tokens):
    """Flag ternary operator '?:' — LSL does not support ternary; this is a compile error."""
    issues = []
    for ttype, tval, tline in tokens:
        if ttype == 'PUNCT' and tval == '?':
            issues.append(("ERROR", "T001", tline,
                "Ternary operator '?:' is not valid LSL — rewrite as if/else"))
    return issues


# ══════════════════════════════════════════════════════════════════════════════
# Check: float equality
# ══════════════════════════════════════════════════════════════════════════════

def check_float_equality(tokens):
    """Warn when a float literal is directly compared with == or !=.

    Floats rarely compare exactly due to IEEE 754 precision; suggest epsilon.
    """
    issues = []
    n = len(tokens)
    for i, (ttype, tval, tline) in enumerate(tokens):
        if ttype == 'OP' and tval in ('==', '!='):
            left  = tokens[i - 1] if i > 0 else None
            right = tokens[i + 1] if i + 1 < n else None
            if (left and left[0] == 'FLOAT') or (right and right[0] == 'FLOAT'):
                issues.append(("WARN", "FP01", tline,
                    f"Direct float comparison '{tval}' — floats rarely compare exactly; "
                    f"consider llFabs(a - b) < epsilon"))
    return issues


# ══════════════════════════════════════════════════════════════════════════════
# Check: division by literal zero
# ══════════════════════════════════════════════════════════════════════════════

def check_division_by_zero(tokens):
    """Flag integer division or modulo by literal zero — runtime error in LSL."""
    issues = []
    n = len(tokens)
    for i, (ttype, tval, tline) in enumerate(tokens):
        if ttype == 'PUNCT' and tval in ('/', '%') and i + 1 < n:
            nxt = tokens[i + 1]
            if nxt[0] in ('INTEGER', 'NUMBER'):
                try:
                    if int(nxt[1], 0) == 0:
                        op_name = "Division" if tval == '/' else "Modulo"
                        issues.append(("ERROR", "Z001", tline,
                            f"{op_name} by literal zero — this is a runtime error in LSL"))
                except ValueError:
                    pass
    return issues


# ══════════════════════════════════════════════════════════════════════════════
# Check: llMessageLinked protocol consistency (HV-specific)
# ══════════════════════════════════════════════════════════════════════════════

def check_hv_protocol(tokens):
    """
    For every llMessageLinked call, verify that:
    - LINK_SET is used (not a raw integer other than 0)
    - The `str` arg (index 2), when a literal, uses a known HV prefix
    - The `key` arg (index 3), when a literal, is a known HV key tag
    This is project-specific to HypnoVisor.
    """
    issues = []
    n = len(tokens)
    i = 0
    while i < n:
        ttype, tval, tline = tokens[i]
        if ttype != 'IDENT' or tval != 'llMessageLinked':
            i += 1; continue
        if i + 1 >= n or tokens[i+1][1] != '(':
            i += 1; continue

        arg_lists, end_idx = _extract_call_args_tokens(tokens, i + 2, n)
        i = end_idx

        if len(arg_lists) < 4:
            continue  # arg count checked separately

        # Arg 0: link target — should be LINK_SET or LINK_ROOT
        link_arg = arg_lists[0]
        if len(link_arg) == 1:
            la_val = link_arg[0][1]
            la_line = link_arg[0][2]
            if link_arg[0][0] == 'INTEGER' and la_val not in ('0',):
                issues.append(("WARN", "HV01", la_line,
                    f"llMessageLinked: link target is raw integer '{la_val}' "
                    f"— use LINK_SET, LINK_ROOT, or LINK_ALL_CHILDREN"))

        # Arg 2: str — check known HV prefix when literal string
        str_arg = arg_lists[2]
        if len(str_arg) == 1 and str_arg[0][0] == 'STRING':
            raw = str_arg[0][1][1:-1]  # strip quotes
            sa_line = str_arg[0][2]
            # Check against known prefixes
            matched = (
                raw in HV_STR_PREFIXES
                or any(raw.startswith(p) for p in HV_STR_PREFIXES if p.endswith("|"))
                or raw.startswith("fw_data:")
                or raw.startswith("TS_CHAN:")
            )
            if not matched and raw != "":
                issues.append(("INFO", "HV02", sa_line,
                    f"llMessageLinked: str arg '{raw[:40]}' is not a recognised HV protocol prefix"))

        # Arg 3: key — should be "", llGetOwner(), a prim name string, or known tag
        key_arg = arg_lists[3]
        if len(key_arg) == 1 and key_arg[0][0] == 'STRING':
            raw = key_arg[0][1][1:-1]
            ka_line = key_arg[0][2]
            known_key = (
                raw == ""
                or raw in HV_KEY_TAGS
                or raw.startswith("fw_")
                or raw.startswith("dist-line-")
                or raw.startswith("focus-line")
            )
            if not known_key:
                issues.append(("INFO", "HV03", ka_line,
                    f"llMessageLinked: key arg (string) '{raw[:40]}' — is this a prim name or tag?"))

    return issues


# ══════════════════════════════════════════════════════════════════════════════
# Cross-file project checks
# ══════════════════════════════════════════════════════════════════════════════

def check_project(files):
    """
    Cross-file checks for the HypnoVisor project:
    - Map every llMessageLinked `str` literal sent across all files
    - Check there is at least one receiver that handles each prefix
    - Detect dead senders (sends a prefix nobody listens for)
    - Detect missing gate replies (|wait without a gate handler)
    """
    issues = []

    # Collect sent prefixes and received prefixes per file
    # "sent"     → set of str prefixes sent via llMessageLinked
    # "received" → set of str prefixes handled in link_message events
    sent_by_file     = defaultdict(set)  # filepath → set of str literals sent
    received_by_file = defaultdict(set)  # filepath → set of str prefixes handled

    WAIT_COMMANDS = {
        "overlay|fade", "overlay|tween", "overlay|crossfade",
        "audio|fade_in", "audio|fade_out",
        "image|fade", "image|crossfade",
        "cDA-Set",
    }

    for filepath in files:
        try:
            with open(filepath, encoding="utf-8", errors="replace") as f:
                src = f.read()
        except OSError:
            continue

        toks = tokenize(src)
        n    = len(toks)

        # Sent: llMessageLinked calls with literal str arg
        i = 0
        while i < n:
            ttype, tval, tline = toks[i]
            if ttype == 'IDENT' and tval == 'llMessageLinked' and i+1 < n and toks[i+1][1] == '(':
                args, end = _extract_call_args_tokens(toks, i+2, n)
                i = end
                if len(args) >= 3:
                    sa = args[2]
                    if len(sa) == 1 and sa[0][0] == 'STRING':
                        raw = sa[0][1][1:-1]
                        prefix = raw.split('|')[0] + ("|" if "|" in raw else "")
                        sent_by_file[filepath].add(raw[:60])
            else:
                i += 1

        # Received: string comparisons in link_message — look for == "literal" patterns
        # that appear inside link_message event handler bodies.
        # Heuristic: scan all == "literal" in the file
        for i2 in range(len(toks) - 2):
            if toks[i2][1] == '==' and toks[i2+1][0] == 'STRING':
                raw = toks[i2+1][1][1:-1]
                received_by_file[filepath].add(raw[:60])
            # Also llGetSubString comparisons
            if toks[i2][1] == 'llGetSubString' or (
                    toks[i2][0] == 'STRING' and toks[i2][1][0] != '"'):
                pass  # too complex to trace statically

    # Cross-file: check each sent literal has at least one receiver
    all_received = set()
    for rs in received_by_file.values():
        all_received.update(rs)

    for filepath, sent_set in sent_by_file.items():
        rel = os.path.relpath(filepath)
        for msg in sorted(sent_set):
            # Check if any file handles it (exact or prefix match)
            handled = (
                msg in all_received
                or msg.rstrip("|") in all_received
                or any(r.startswith(msg.rstrip("|")) for r in all_received)
                or any(msg.startswith(r.rstrip("|")) for r in all_received)
            )
            if not handled:
                # Only report for known HV prefixes, skip generic
                is_hv = any(msg.startswith(p.rstrip("|")) for p in HV_STR_PREFIXES)
                if is_hv:
                    issues.append(("INFO", "XF01", 0,
                        f"{rel}: sends '{msg}' — no matching handler found in project"))

    return issues


# ══════════════════════════════════════════════════════════════════════════════
# File checker
# ══════════════════════════════════════════════════════════════════════════════

LSL_RESERVED = LSL_TYPES | FLOW_KW | {
    "event", "in", "case", "switch", "break", "continue", "this", "goto",
}

def check_reserved_word_identifiers(tokens):
    """Error when an LSL reserved word (type name or keyword) is used as a
    variable or parameter name. e.g. 'string key' as a parameter declaration
    is a compile error because 'key' is a type name in LSL."""
    issues = []
    n = len(tokens)
    for i, (ttype, tval, tline) in enumerate(tokens):
        # Looking for:  <type> <reserved_word>  where the second token is used
        # as an identifier (followed by , ) = ; or is a function parameter)
        if ttype != "IDENT" or tval not in LSL_TYPES:
            continue
        j = i + 1
        if j >= n:
            continue
        ntype, nval, nline = tokens[j]
        if ntype == "IDENT" and nval in LSL_RESERVED and nval != tval:
            # Check it's being used as a name (next token is , ) = ; { or another type)
            k = j + 1
            if k < n and tokens[k][1] in {",", ")", "=", ";", "{"}:
                issues.append(("ERROR", "S001", nline,
                    f"Reserved word '{nval}' used as variable/parameter name -- "
                    f"this is a compile error in LSL"))
    return issues


def check_file(filepath, known_funcs, run_hv_protocol=True):
    try:
        with open(filepath, encoding="utf-8", errors="replace") as f:
            src = f.read()
    except OSError as e:
        return [("ERROR", "IO01", 0, f"Could not read file: {e}")]

    tokens = tokenize(src)
    user_funcs, global_vars, state_names = extract_declarations(tokens)

    issues = []
    issues += check_reserved_word_identifiers(tokens)
    issues += check_arg_counts(tokens, known_funcs, user_funcs)
    issues += check_jump_labels(tokens, user_funcs, state_names)
    issues += check_state_transitions(tokens, state_names)
    issues += check_duplicates(user_funcs, global_vars)
    issues += check_dialog_buttons(tokens)
    issues += check_integer_overflow(tokens)
    issues += check_unused_globals(tokens, global_vars)
    issues += check_missing_return(tokens, user_funcs)
    issues += check_resource_leaks(tokens)
    issues += check_string_operations(tokens)
    issues += check_ternary_operators(tokens)
    issues += check_float_equality(tokens)
    issues += check_division_by_zero(tokens)
    if run_hv_protocol:
        issues += check_hv_protocol(tokens)
    
    # Add lslint validation
    issues += run_lslint(filepath)

    issues.sort(key=lambda x: (x[2], x[0]))
    return issues


# ══════════════════════════════════════════════════════════════════════════════
# Reporter
# ══════════════════════════════════════════════════════════════════════════════

SEVERITY_COLOUR = {
    "ERROR": "\033[91m",
    "WARN":  "\033[93m",
    "INFO":  "\033[96m",
}
RESET = "\033[0m"

def use_colour():
    return sys.stdout.isatty()

def report(filepath, issues):
    col = use_colour()
    rel = os.path.relpath(filepath)
    if not issues:
        c = f"{SEVERITY_COLOUR['INFO']}OK{RESET}" if col else "OK"
        print(f"  {c}  {rel}")
        return 0, 0, 0

    errors = sum(1 for s, *_ in issues if s == "ERROR")
    warns  = sum(1 for s, *_ in issues if s == "WARN")
    infos  = sum(1 for s, *_ in issues if s == "INFO")
    print(f"\n  {rel}  ({errors}E {warns}W {infos}I)")
    for severity, code, lineno, msg in issues:
        loc = f":{lineno}" if lineno else ""
        c = SEVERITY_COLOUR.get(severity, "") if col else ""
        r = RESET if col else ""
        print(f"    {c}[{severity}]{r} {code}  {rel}{loc}  {msg}")
    return errors, warns, infos


def report_project(issues, label="project"):
    col = use_colour()
    if not issues:
        c = f"{SEVERITY_COLOUR['INFO']}OK{RESET}" if col else "OK"
        print(f"\n  {c}  {label} (cross-file checks)")
        return 0, 0, 0
    errors = sum(1 for s, *_ in issues if s == "ERROR")
    warns  = sum(1 for s, *_ in issues if s == "WARN")
    infos  = sum(1 for s, *_ in issues if s == "INFO")
    print(f"\n  {label} — cross-file  ({errors}E {warns}W {infos}I)")
    for severity, code, lineno, msg in issues:
        c = SEVERITY_COLOUR.get(severity, "") if col else ""
        r = RESET if col else ""
        print(f"    {c}[{severity}]{r} {code}  {msg}")
    return errors, warns, infos


# ══════════════════════════════════════════════════════════════════════════════
# LSLint integration
# ══════════════════════════════════════════════════════════════════════════════

def _lslint_known_identifiers():
    """Return a set of all known-good LSL function, event, and constant names for false-positive filtering."""
    known = set()

    # Functions from pyoptimizer builtins.txt
    builtins_path = PYOPT_DIR / "builtins.txt"
    if builtins_path.exists():
        fn_re = re.compile(r'^\w+\s+(\w+)\s*\(')
        const_re = re.compile(r'^const\s+\w+\s+(\w+)\s*=')
        for line in builtins_path.read_text(encoding="utf-8", errors="replace").splitlines():
            m = fn_re.match(line.strip()) or const_re.match(line.strip())
            if m:
                known.add(m.group(1))

    # Functions + events + constants from jyaoma JSON
    for fname in ("functions.json", "events.json", "constants.json"):
        p = JYAOMA_DIR / fname
        if p.exists():
            try:
                known.update(json.load(p.open(encoding="utf-8")).keys())
            except Exception:
                pass

    # kwdb.xml
    if KWDB_FILE.exists():
        try:
            root = ET.parse(KWDB_FILE).getroot()
            for tag in ("function", "event", "constant"):
                for elem in root.iter(tag):
                    n = elem.get("name")
                    if n:
                        known.add(n)
        except ET.ParseError:
            pass

    return known


def run_lslint(filepath):
    """
    Run lslint on the given file and parse its output into our issue format.
    Known-good linkset-data functions, events, and constants are filtered so
    that stale lslint "is undeclared" false positives are suppressed.
    Returns a list of (severity, code, line, message) tuples.
    """
    issues = []

    # Build suppress set once — covers functions, events, constants that lslint
    # doesn't know about but ARE valid LSL identifiers in our cache databases.
    known_ids = _lslint_known_identifiers()

    # Patterns for "undeclared" false positives from lslint
    _undecl_re = re.compile(r"`(\w+)'(?:\s+is undeclared|\s+is not a valid event name)", re.IGNORECASE)

    # lslint output line format:  LEVEL:: ( line,  col): message
    _line_re = re.compile(r'(ERROR|WARN(?:ING)?):: \(\s*(\d+),\s*(\d+)\):\s*(.+)', re.IGNORECASE)

    def _parse_lslint_stream(text):
        """Parse lslint output lines, suppressing known-good false positives."""
        for raw in text.splitlines():
            raw = raw.strip()
            if not raw or raw.startswith('lslint v') or raw.startswith('TOTAL::'):
                continue
            m = _line_re.match(raw)
            if not m:
                continue
            level, line_num, _col, message = m.groups()
            # Suppress "X is undeclared / not a valid event" if X is in our DB
            fp_match = _undecl_re.search(message)
            if fp_match and fp_match.group(1) in known_ids:
                continue
            sev  = 'ERROR' if level.upper() == 'ERROR' else 'WARN'
            code = 'LSL01' if sev == 'ERROR' else 'LSL02'
            issues.append((sev, code, int(line_num), f"lslint: {message}"))

    try:
        result = subprocess.run(
            ['lslint', filepath],
            capture_output=True,
            text=True,
            timeout=30,
        )
        # lslint writes diagnostics to stdout on some builds, stderr on others
        _parse_lslint_stream(result.stdout)
        _parse_lslint_stream(result.stderr)

    except subprocess.TimeoutExpired:
        issues.append(('ERROR', 'LSL00', 1, "lslint timed out"))
    except FileNotFoundError:
        pass  # lslint not installed — silently skip
    except Exception as e:
        issues.append(('ERROR', 'LSL00', 1, f"lslint integration error: {e}"))

    return issues


# ══════════════════════════════════════════════════════════════════════════════
# Entry point
# ══════════════════════════════════════════════════════════════════════════════

def find_lsl_files(root="."):
    result = []
    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            if fname.lower().endswith(".lsl"):
                result.append(os.path.join(dirpath, fname))
    return sorted(result)


def main():
    args = sys.argv[1:]
    run_project = "--project" in args
    args = [a for a in args if a != "--project"]
    run_hv = "--hv" in args or run_project
    args = [a for a in args if a != "--hv"]
    json_output = "--json" in args
    args = [a for a in args if a != "--json"]

    if not args:
        print("Usage: lsl-sanity-checker.py [--project] [--json] [--all [dir]] [file.lsl ...]")
        print("  --project  also run cross-file HV protocol consistency checks")
        print("  --json     output results as JSON instead of human-readable text")
        sys.exit(1)

    if "--all" in args:
        remaining = [a for a in args if a != "--all"]
        root = remaining[0] if remaining else "."
        files = find_lsl_files(root)
    else:
        files = [a for a in args if not a.startswith("--")]

    if not files:
        print("No .lsl files found.")
        sys.exit(0)

    print("Loading LSL cache data...") if not json_output else None
    known_funcs = load_known_functions()
    print(f"  {len(known_funcs)} functions loaded\n") if not json_output else None

    total_errors = total_warns = total_infos = 0
    results = {}

    for filepath in files:
        issues = check_file(filepath, known_funcs, run_hv_protocol=True)
        e, w, i = len([x for x in issues if x[0] == "ERROR"]), len([x for x in issues if x[0] == "WARN"]), len([x for x in issues if x[0] == "INFO"])
        total_errors += e; total_warns += w; total_infos += i

        if json_output:
            results[filepath] = {
                "errors": e,
                "warnings": w,
                "infos": i,
                "issues": [{"severity": s, "code": c, "line": l, "message": m} for s, c, l, m in issues]
            }
        else:
            report(filepath, issues)

    if run_project and len(files) > 1:
        proj_issues = check_project(files)
        e, w, i = len([x for x in proj_issues if x[0] == "ERROR"]), len([x for x in proj_issues if x[0] == "WARN"]), len([x for x in proj_issues if x[0] == "INFO"])
        total_errors += e; total_warns += w; total_infos += i

        if json_output:
            results["project"] = {
                "errors": e,
                "warnings": w,
                "infos": i,
                "issues": [{"severity": s, "code": c, "line": l, "message": m} for s, c, l, m in proj_issues]
            }
        else:
            report_project(proj_issues)

    if json_output:
        import json
        output = {
            "summary": {
                "files_checked": len(files),
                "total_errors": total_errors,
                "total_warnings": total_warns,
                "total_infos": total_infos
            },
            "results": results
        }
        print(json.dumps(output, indent=2))
    else:
        col = use_colour()
        ec = SEVERITY_COLOUR["ERROR"] if col else ""
        wc = SEVERITY_COLOUR["WARN"]  if col else ""
        ic = SEVERITY_COLOUR["INFO"]  if col else ""
        rc = RESET if col else ""
        print(f"\n{'-'*60}")
        print(f"Checked {len(files)} file(s) -- "
              f"{ec}{total_errors} error(s){rc}, "
              f"{wc}{total_warns} warning(s){rc}, "
              f"{ic}{total_infos} note(s){rc}")

    sys.exit(1 if total_errors > 0 else 0)


if __name__ == "__main__":
    main()
