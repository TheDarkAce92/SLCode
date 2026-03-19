#!/usr/bin/env python3
# Skill: lsl-syntax-checker
# Version: 0.1.0.5
# Purpose: Check LSL files for syntax errors, unknown identifiers, and anti-patterns
# Usage: python3 ~/.lsl-cache/skills/lsl-syntax-checker.py [file.lsl ...]
#        python3 ~/.lsl-cache/skills/lsl-syntax-checker.py --all  (scan all .lsl from cwd)
#        python3 ~/.lsl-cache/skills/lsl-syntax-checker.py --json [file.lsl ...]  (JSON output)
# Created: 2026-03-10
# Last modified: 2026-03-15

import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

# ─── Cache paths ──────────────────────────────────────────────────────────────
_env_base   = os.environ.get("LSL_CACHE_BASE", "").strip()
CACHE_PATH  = Path(_env_base) if _env_base else Path(__file__).resolve().parents[1]
JYAOMA_DIR  = CACHE_PATH / "lsl-docs/vscode-extension-data/jyaoma"
PYOPT_DIR   = CACHE_PATH / "lsl-docs/vscode-extension-data/pyoptimizer"
KWDB_FILE   = CACHE_PATH / "lsl-docs/vscode-extension-data/kwdb/kwdb.xml"

# ─── LSL built-in keywords / literal constants (always valid, never flag) ─────
LSL_TYPES = {"integer", "float", "string", "key", "vector", "rotation", "list"}

LSL_BUILTIN_LITERALS = {
    "TRUE", "FALSE", "NULL_KEY", "ZERO_VECTOR", "ZERO_ROTATION",
    "EOF", "PI", "TWO_PI", "PI_BY_TWO", "DEG_TO_RAD", "RAD_TO_DEG",
    "SQRT2", "STRING_EOL", "STRING_NEWLINE",
    "TYPE_INTEGER", "TYPE_FLOAT", "TYPE_STRING", "TYPE_KEY",
    "TYPE_VECTOR", "TYPE_ROTATION", "TYPE_LIST", "TYPE_INVALID",
    "LINK_ROOT", "LINK_SET", "LINK_ALL_OTHERS", "LINK_ALL_CHILDREN",
    "LINK_THIS", "ALL_SIDES", "SIDE_NONE",
    "DEBUG_CHANNEL", "PUBLIC_CHANNEL",
    "ATTACH_CHEST", "ATTACH_HEAD", "ATTACH_LSHOULDER", "ATTACH_RSHOULDER",
    "ATTACH_LHAND", "ATTACH_RHAND", "ATTACH_LFOOT", "ATTACH_RFOOT",
    "ATTACH_BACK", "ATTACH_PELVIS", "ATTACH_MOUTH", "ATTACH_CHIN",
    "ATTACH_LEAR", "ATTACH_REAR", "ATTACH_LEYE", "ATTACH_REYE",
    "ATTACH_NOSE", "ATTACH_RUARM", "ATTACH_RLARM", "ATTACH_LUARM",
    "ATTACH_LLARM", "ATTACH_RHIP", "ATTACH_RULEG", "ATTACH_RLLEG",
    "ATTACH_LHIP", "ATTACH_LULEG", "ATTACH_LLLEG", "ATTACH_BELLY",
    "ATTACH_RPEC", "ATTACH_LPEC", "ATTACH_FACE_TONGUE", "ATTACH_GROIN",
    "ATTACH_HUD_CENTER_2", "ATTACH_HUD_TOP_RIGHT", "ATTACH_HUD_TOP",
    "ATTACH_HUD_TOP_LEFT", "ATTACH_HUD_CENTER_1", "ATTACH_HUD_BOTTOM_LEFT",
    "ATTACH_HUD_BOTTOM", "ATTACH_HUD_BOTTOM_RIGHT",
    "CHANGED_INVENTORY", "CHANGED_COLOR", "CHANGED_SHAPE", "CHANGED_SCALE",
    "CHANGED_TEXTURE", "CHANGED_LINK", "CHANGED_ALLOWED_DROP", "CHANGED_OWNER",
    "CHANGED_REGION", "CHANGED_TELEPORT", "CHANGED_REGION_START",
    "CHANGED_MEDIA", "CHANGED_ANIMATION", "CHANGED_POSITION",
    "CHANGED_GRID", "CHANGED_NEIGHBORING_GRID",
    "PERMISSION_DEBIT", "PERMISSION_TAKE_CONTROLS", "PERMISSION_REMAP_CONTROLS",
    "PERMISSION_TRIGGER_ANIMATION", "PERMISSION_ATTACH", "PERMISSION_RELEASE_OWNERSHIP",
    "PERMISSION_CHANGE_LINKS", "PERMISSION_CHANGE_JOINTS", "PERMISSION_CHANGE_PERMISSIONS",
    "PERMISSION_TRACK_CAMERA", "PERMISSION_CONTROL_CAMERA", "PERMISSION_TELEPORT",
    "PERMISSION_SILENT_ESTATE_MANAGEMENT", "PERMISSION_OVERRIDE_ANIMATIONS",
    "PERMISSION_RETURN_OBJECTS", "PERMISSION_EXPERIENCE",
    "AGENT", "ACTIVE", "PASSIVE", "SCRIPTED",
    "CONTROL_FWD", "CONTROL_BACK", "CONTROL_LEFT", "CONTROL_RIGHT",
    "CONTROL_ROT_LEFT", "CONTROL_ROT_RIGHT", "CONTROL_UP", "CONTROL_DOWN",
    "CONTROL_LBUTTON", "CONTROL_ML_LBUTTON",
    "INVENTORY_TEXTURE", "INVENTORY_SOUND", "INVENTORY_OBJECT",
    "INVENTORY_SCRIPT", "INVENTORY_LANDMARK", "INVENTORY_CLOTHING",
    "INVENTORY_NOTECARD", "INVENTORY_BODYPART", "INVENTORY_ANIMATION",
    "INVENTORY_GESTURE", "INVENTORY_SETTING", "INVENTORY_MATERIAL",
    "INVENTORY_ALL", "INVENTORY_NONE",
    "PRIM_TYPE", "PRIM_MATERIAL", "PRIM_PHYSICS", "PRIM_TEMP_ON_REZ",
    "PRIM_PHANTOM", "PRIM_POSITION", "PRIM_SIZE", "PRIM_ROTATION",
    "PRIM_TEXTURE", "PRIM_COLOR", "PRIM_BUMP_SHINY", "PRIM_FULLBRIGHT",
    "PRIM_FLEXIBLE", "PRIM_POINT_LIGHT", "PRIM_CAST_SHADOWS", "PRIM_GLOW",
    "PRIM_TEXT", "PRIM_NAME", "PRIM_DESC", "PRIM_ROT_LOCAL",
    "PRIM_OMEGA", "PRIM_POS_LOCAL", "PRIM_LINK_TARGET", "PRIM_SLICE",
    "PRIM_SPECULAR", "PRIM_NORMAL", "PRIM_ALPHA_MODE", "PRIM_ALLOW_UNSIT",
    "PRIM_SCRIPTED_SIT_ONLY", "PRIM_SIT_TARGET", "PRIM_PROJECTOR",
    "PRIM_PHYSICS_SHAPE_TYPE", "PRIM_PHYSICS_MATERIAL", "PRIM_MEDIA",
    "PRIM_RENDER_MATERIAL", "PRIM_REFLECTION_PROBE",
    "PRIM_TYPE_BOX", "PRIM_TYPE_CYLINDER", "PRIM_TYPE_PRISM",
    "PRIM_TYPE_SPHERE", "PRIM_TYPE_TORUS", "PRIM_TYPE_TUBE",
    "PRIM_TYPE_RING", "PRIM_TYPE_SCULPT",
    "ANIM_ON", "LOOP", "REVERSE", "PING_PONG", "SMOOTH", "ROTATE",
    "SCALE", "TEXTURE_ANIM_END",
    "STATUS_PHYSICS", "STATUS_ROTATE_X", "STATUS_ROTATE_Y",
    "STATUS_ROTATE_Z", "STATUS_PHANTOM", "STATUS_SANDBOX",
    "STATUS_BLOCK_GRAB", "STATUS_DIE_AT_EDGE", "STATUS_RETURN_AT_EDGE",
    "STATUS_CAST_SHADOWS", "STATUS_BLOCK_GRAB_OBJECT", "STATUS_DIE_AT_NO_ENTRY",
    "PARCEL_MEDIA_COMMAND_STOP", "PARCEL_MEDIA_COMMAND_PAUSE",
    "PARCEL_MEDIA_COMMAND_PLAY", "PARCEL_MEDIA_COMMAND_LOOP",
    "PARCEL_MEDIA_COMMAND_TEXTURE", "PARCEL_MEDIA_COMMAND_URL",
    "PARCEL_MEDIA_COMMAND_TIME", "PARCEL_MEDIA_COMMAND_AGENT",
    "PARCEL_MEDIA_COMMAND_UNLOAD", "PARCEL_MEDIA_COMMAND_AUTO_ALIGN",
    "PARCEL_MEDIA_COMMAND_TYPE", "PARCEL_MEDIA_COMMAND_SIZE",
    "PARCEL_MEDIA_COMMAND_DESC", "PARCEL_MEDIA_COMMAND_LOOP_SET",
    "PAY_HIDE", "PAY_DEFAULT",
    "HTTP_METHOD", "HTTP_MIMETYPE", "HTTP_BODY_MAXLENGTH",
    "HTTP_VERIFY_CERT", "HTTP_VERBOSE_THROTTLE", "HTTP_CUSTOM_HEADER",
    "HTTP_PRAGMA_NO_CACHE", "HTTP_USER_AGENT_ID",
    "OBJECT_NAME", "OBJECT_DESC", "OBJECT_POS", "OBJECT_ROT", "OBJECT_VELOCITY",
    "OBJECT_OWNER", "OBJECT_GROUP", "OBJECT_CREATOR", "OBJECT_RUNNING_SCRIPT_COUNT",
    "OBJECT_TOTAL_SCRIPT_COUNT", "OBJECT_SCRIPT_MEMORY", "OBJECT_SCRIPT_TIME",
    "OBJECT_PRIM_EQUIVALENCE", "OBJECT_SERVER_COST", "OBJECT_STREAMING_COST",
    "OBJECT_PHYSICS_COST", "OBJECT_CHARACTER_TIME", "OBJECT_ROOT",
    "OBJECT_ATTACHED_POINT", "OBJECT_PATHFINDING_TYPE", "OBJECT_PHYSICS",
    "OBJECT_PHANTOM", "OBJECT_TEMP_ON_REZ", "OBJECT_RENDER_WEIGHT",
    "OBJECT_HOVER_HEIGHT", "OBJECT_BODY_SHAPE_TYPE", "OBJECT_LAST_OWNER_ID",
    "OBJECT_CLICK_ACTION", "OBJECT_OMEGA", "OBJECT_PRIM_COUNT",
    "OBJECT_TOTAL_INVENTORY_COUNT", "OBJECT_REZZER_KEY",
    "OBJECT_GROUP_TAG", "OBJECT_TEMP_ATTACHED", "OBJECT_ATTACHED_SLOTS_AVAILABLE",
    "OBJECT_CREATION_TIME", "OBJECT_SELECT_COUNT", "OBJECT_SIT_COUNT",
    "OBJECT_ANIMATED_COUNT", "OBJECT_ANIMATED_SLOTS_AVAILABLE",
    "OBJECT_ACCOUNT_LEVEL", "OBJECT_MATERIAL",
    "LAND_LEVEL", "LAND_RAISE", "LAND_LOWER", "LAND_SMOOTH",
    "LAND_NOISE", "LAND_REVERT",
    "DATA_ONLINE", "DATA_NAME", "DATA_BORN", "DATA_RATING",
    "DATA_PAYINFO", "DATA_SIM_POS", "DATA_SIM_STATUS", "DATA_SIM_RATING",
    "DATA_AGENT_APPEARANCE_SERIALIZED",
    "CLICK_ACTION_NONE", "CLICK_ACTION_TOUCH", "CLICK_ACTION_SIT",
    "CLICK_ACTION_BUY", "CLICK_ACTION_PAY", "CLICK_ACTION_OPEN",
    "CLICK_ACTION_PLAY", "CLICK_ACTION_OPEN_MEDIA", "CLICK_ACTION_ZOOM",
    "TEXTURE_BLANK", "TEXTURE_DEFAULT", "TEXTURE_PLYWOOD",
    "TEXTURE_TRANSPARENT", "TEXTURE_MEDIA",
    "SOUND_VOLUME_DEFAULT",
    "KFM_COMMAND", "KFM_CMD_PLAY", "KFM_CMD_STOP", "KFM_CMD_PAUSE",
    "KFM_MODE", "KFM_FORWARD", "KFM_LOOP", "KFM_PING_PONG",
    "KFM_DATA", "KFM_TRANSLATION", "KFM_ROTATION",
    "PROFILE_NONE", "PROFILE_SCRIPT_MEMORY",
    "RC_REJECT_TYPES", "RC_DETECT_PHANTOM", "RC_DATA_FLAGS",
    "RC_MAX_HITS", "RC_REJECT_AGENTS", "RC_REJECT_PHYSICAL",
    "RC_REJECT_NONPHYSICAL", "RC_REJECT_LAND",
    "RCERR_UNKNOWN", "RCERR_SIM_PERF_LOW", "RCERR_CAST_TIME_EXCEEDED",
    "RCDATA_NORMAL", "RCDATA_TEXTURE",
    "ESTATE_ACCESS_ALLOWED_AGENT_ADD", "ESTATE_ACCESS_ALLOWED_AGENT_REMOVE",
    "ESTATE_ACCESS_ALLOWED_GROUP_ADD", "ESTATE_ACCESS_ALLOWED_GROUP_REMOVE",
    "ESTATE_ACCESS_BANNED_AGENT_ADD", "ESTATE_ACCESS_BANNED_AGENT_REMOVE",
    "JSON_ARRAY", "JSON_OBJECT", "JSON_STRING", "JSON_NUMBER",
    "JSON_INTEGER", "JSON_TRUE", "JSON_FALSE", "JSON_NULL", "JSON_INVALID",
    "DENSITY", "FRICTION", "RESTITUTION", "GRAVITY_MULTIPLIER",
    "CHARACTER_CMD_JUMP", "CHARACTER_CMD_STOP", "CHARACTER_CMD_SMOOTH_STOP",
    "CHARACTER_CMD_PATROL",
    "PURSUIT_FUZZ_FACTOR", "PURSUIT_INTERCEPT", "PURSUIT_GOAL_TOLERANCE",
    "REQUIRE_LINE_OF_SIGHT",
    "TRAVERSAL_TYPE", "TRAVERSAL_TYPE_FAST", "TRAVERSAL_TYPE_SLOW", "TRAVERSAL_TYPE_NONE",
    "CHARACTER_DESIRED_SPEED", "CHARACTER_MAX_SPEED", "CHARACTER_DESIRED_TURN_SPEED",
    "CHARACTER_MAX_ACCEL", "CHARACTER_MAX_DECEL", "CHARACTER_MAX_TURN_RADIUS",
    "CHARACTER_RADIUS", "CHARACTER_LENGTH", "CHARACTER_ORIENTATION",
    "CHARACTER_TYPE", "CHARACTER_TYPE_A", "CHARACTER_TYPE_B",
    "CHARACTER_TYPE_C", "CHARACTER_TYPE_D", "CHARACTER_TYPE_NONE",
    "CHARACTER_STAY_WITHIN_PARCEL", "CHARACTER_AVOIDANCE_MODE",
    "CHARACTER_ACCOUNT_FOR_GRAVITY", "AVOID_CHARACTERS", "AVOID_DYNAMIC_OBSTACLES",
    "AVOID_NONE", "PU_GOAL_REACHED", "PU_FAILURE_INVALID_START",
    "PU_FAILURE_INVALID_GOAL", "PU_FAILURE_UNREACHABLE", "PU_FAILURE_TARGET_GONE",
    "PU_FAILURE_NO_VALID_DESTINATION", "PU_EVADE_HIDDEN", "PU_EVADE_SPOTTED",
    "PU_FAILURE_NO_NAVMESH", "PU_FAILURE_DYNAMIC_PATHFINDING_DISABLED",
    "PU_FAILURE_PARCEL_UNREACHABLE", "PU_FAILURE_OTHER",
    "SMOOTH_NAVIGATION",
    "OBJECT_ANIMATED_SLOTS_AVAILABLE",
    "VEHICLE_TYPE_NONE", "VEHICLE_TYPE_SLED", "VEHICLE_TYPE_CAR",
    "VEHICLE_TYPE_BOAT", "VEHICLE_TYPE_AIRPLANE", "VEHICLE_TYPE_BALLOON",
    "VEHICLE_REFERENCE_FRAME", "VEHICLE_ANGULAR_FRICTION_TIMESCALE",
    "VEHICLE_LINEAR_FRICTION_TIMESCALE", "VEHICLE_ANGULAR_MOTOR_DIRECTION",
    "VEHICLE_LINEAR_MOTOR_DIRECTION", "VEHICLE_LINEAR_MOTOR_OFFSET",
    "VEHICLE_ANGULAR_MOTOR_TIMESCALE", "VEHICLE_ANGULAR_MOTOR_DECAY_TIMESCALE",
    "VEHICLE_LINEAR_MOTOR_TIMESCALE", "VEHICLE_LINEAR_MOTOR_DECAY_TIMESCALE",
    "VEHICLE_ANGULAR_DEFLECTION_EFFICIENCY", "VEHICLE_ANGULAR_DEFLECTION_TIMESCALE",
    "VEHICLE_LINEAR_DEFLECTION_EFFICIENCY", "VEHICLE_LINEAR_DEFLECTION_TIMESCALE",
    "VEHICLE_ANGULAR_BANKING_EFFICIENCY", "VEHICLE_ANGULAR_BANKING_TIMESCALE",
    "VEHICLE_BANKING_MIX", "VEHICLE_BUOYANCY", "VEHICLE_HOVER_HEIGHT",
    "VEHICLE_HOVER_EFFICIENCY", "VEHICLE_HOVER_TIMESCALE",
    "VEHICLE_VERTICAL_ATTRACTION_EFFICIENCY", "VEHICLE_VERTICAL_ATTRACTION_TIMESCALE",
    "VEHICLE_FLAG_NO_FLY_UP", "VEHICLE_FLAG_LIMIT_ROLL_ONLY",
    "VEHICLE_FLAG_HOVER_WATER_ONLY", "VEHICLE_FLAG_HOVER_TERRAIN_ONLY",
    "VEHICLE_FLAG_HOVER_GLOBAL_HEIGHT", "VEHICLE_FLAG_HOVER_UP_ONLY",
    "VEHICLE_FLAG_LIMIT_MOTOR_UP", "VEHICLE_FLAG_MOUSELOOK_STEER",
    "VEHICLE_FLAG_MOUSELOOK_BANK", "VEHICLE_FLAG_CAMERA_DECOUPLED",
    "VEHICLE_FLAG_NO_DEFLECTION_UP", "VEHICLE_FLAG_LOCK_HOVER_HEIGHT",
    "VEHICLE_FLAG_NO_X", "VEHICLE_FLAG_NO_Y", "VEHICLE_FLAG_NO_Z",
    "CAMERA_PITCH", "CAMERA_FOCUS_OFFSET", "CAMERA_FOCUS_OFFSET_X",
    "CAMERA_FOCUS_OFFSET_Y", "CAMERA_FOCUS_OFFSET_Z", "CAMERA_POSITION_LAG",
    "CAMERA_FOCUS_LAG", "CAMERA_DISTANCE", "CAMERA_BEHINDNESS_ANGLE",
    "CAMERA_BEHINDNESS_LAG", "CAMERA_POSITION_THRESHOLD",
    "CAMERA_FOCUS_THRESHOLD", "CAMERA_ACTIVE", "CAMERA_POSITION",
    "CAMERA_POSITION_X", "CAMERA_POSITION_Y", "CAMERA_POSITION_Z",
    "CAMERA_FOCUS", "CAMERA_FOCUS_X", "CAMERA_FOCUS_Y", "CAMERA_FOCUS_Z",
    "CAMERA_POSITION_LOCKED", "CAMERA_FOCUS_LOCKED",
}

# Anti-patterns: (regex, severity, code, message)
ANTI_PATTERNS = [
    (r'\bllSleep\s*\(',     "WARN",  "AP001",
     "llSleep() blocks the entire script thread -- use llSetTimerEvent() instead"),
    (r'\bllSay\s*\(\s*0\s*,', "WARN", "AP002",
     "llSay(0,...) broadcasts on public channel -- prefer llOwnerSay() or private channel"),
    (r'\bllWhisper\s*\(\s*0\s*,', "INFO", "AP003",
     "llWhisper(0,...) on public channel -- intentional?"),
    (r'\bllShout\s*\(\s*0\s*,', "WARN", "AP004",
     "llShout(0,...) on public channel -- prefer private channel"),
    (r'\bllListen\s*\(\s*666\s*,', "WARN", "AP005",
     "llListen on channel 666 -- debug listener, remove before production"),
    (r'\bllListen\s*\(\s*DEBUG_CHANNEL\s*,', "WARN", "AP005",
     "llListen on DEBUG_CHANNEL -- debug listener, remove before production"),
    (r'while\s*\(\s*TRUE\s*\)\s*\{[^}]*llSleep', "WARN", "AP006",
     "Polling loop with llSleep -- use event-driven approach instead"),
    (r'\bllGetAgentInfo\s*\(.*\)\s*[!=]=\s*0', "INFO", "AP007",
     "llGetAgentInfo result compared to 0 -- compare against specific AGENT_* flags"),
    (r'\bllMessageLinked\s*\(\s*-1\s*,', "INFO", "AP008",
     "llMessageLinked(-1,...) -- consider using named constant LINK_SET instead of -1"),
    (r'\bllSetText\s*\(\s*""\s*,', "INFO", "AP009",
     "llSetText with empty string -- consider using llSetText(\"\", ZERO_VECTOR, 0.0) to clear completely"),
    (r'\bllDie\s*\(\s*\)', "WARN", "AP010",
     "llDie() called -- script will terminate, ensure this is intentional"),
    (r'\bllResetScript\s*\(\s*\)', "WARN", "AP011",
     "llResetScript() called -- script will restart, ensure no data loss"),
]


# ─── Data loading ──────────────────────────────────────────────────────────────

def load_known_functions():
    """Return dict: name → {param_count, return_type, sleep, experimental, broken}"""
    funcs = {}

    # pyoptimizer/builtins.txt -- C-style declarations, reliable for existence + return type
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
                        "experimental": False,
                        "broken": False,
                    }

    # jyaoma/functions.json -- richer metadata, augments pyoptimizer
    jyaoma_path = JYAOMA_DIR / "functions.json"
    if jyaoma_path.exists():
        with open(jyaoma_path, encoding="utf-8") as f:
            jdata = json.load(f)
        for fname, fdata in jdata.items():
            params = fdata.get("parameters", [])
            entry = funcs.get(fname, {})
            entry.update({
                "return_type":  fdata.get("returnType", entry.get("return_type", "")),
                "param_count":  len(params),
                "param_types":  [p.get("type", "?") for p in params],
                "sleep":        fdata.get("sleep", entry.get("sleep", 0.0)),
                "experimental": fdata.get("experimental", entry.get("experimental", False)),
                "broken":       fdata.get("broken", entry.get("broken", False)),
                "godMode":      fdata.get("godMode", False),
                "experience":   fdata.get("experience", False),
            })
            funcs[fname] = entry

    # kwdb.xml -- additional functions not in other sources
    if KWDB_FILE.exists():
        try:
            tree = ET.parse(KWDB_FILE)
            root = tree.getroot()
            for elem in root.iter("function"):
                fname = elem.get("name")
                if fname and fname not in funcs:
                    params = list(elem.iter("param"))
                    funcs[fname] = {
                        "return_type":  elem.get("type", ""),
                        "param_count":  len(params),
                        "param_types":  [p.get("type", "?") for p in params],
                        "sleep":        0.0,
                        "experimental": False,
                        "broken":       False,
                    }
        except ET.ParseError:
            pass

    return funcs


def load_known_events():
    """Return dict: name → {param_count, param_types}"""
    events = {}
    events_path = JYAOMA_DIR / "events.json"
    if events_path.exists():
        with open(events_path, encoding="utf-8") as f:
            edata = json.load(f)
        for ename, einfo in edata.items():
            params = einfo.get("parameters", [])
            events[ename] = {
                "param_count": len(params),
                "param_types": [p.get("type", "?") for p in params],
            }
    # Add from kwdb.xml
    if KWDB_FILE.exists():
        try:
            tree = ET.parse(KWDB_FILE)
            root = tree.getroot()
            for elem in root.iter("event"):
                ename = elem.get("name")
                if ename and ename not in events:
                    params = list(elem.iter("param"))
                    events[ename] = {
                        "param_count": len(params),
                        "param_types": [p.get("type", "?") for p in params],
                    }
        except ET.ParseError:
            pass
    return events


def load_known_constants():
    """Return set of all known LSL constant names."""
    consts = set(LSL_BUILTIN_LITERALS)

    # jyaoma/constants.json
    consts_path = JYAOMA_DIR / "constants.json"
    if consts_path.exists():
        with open(consts_path, encoding="utf-8") as f:
            cdata = json.load(f)
        consts.update(cdata.keys())

    # kwdb.xml constants
    if KWDB_FILE.exists():
        try:
            tree = ET.parse(KWDB_FILE)
            root = tree.getroot()
            for elem in root.iter("constant"):
                name = elem.get("name")
                if name:
                    consts.add(name)
        except ET.ParseError:
            pass

    return consts


# ─── Tokenizer ─────────────────────────────────────────────────────────────────

def tokenize(src):
    """
    Tokenize LSL source into list of (type, value, line_number).
    Token types: IDENT, NUMBER, STRING, OP, PUNCT
    Comments and whitespace are consumed (not emitted).
    Line numbers are 1-based.
    """
    tokens = []
    i = 0
    line = 1
    n = len(src)

    while i < n:
        c = src[i]

        # Newline
        if c == '\n':
            line += 1
            i += 1
            continue

        # Whitespace
        if c in ' \t\r':
            i += 1
            continue

        # Block comment
        if src[i:i+2] == '/*':
            end = src.find('*/', i + 2)
            if end == -1:
                break  # unterminated block comment -- stop tokenizing
            line += src[i:end+2].count('\n')
            i = end + 2
            continue

        # Line comment
        if src[i:i+2] == '//':
            while i < n and src[i] != '\n':
                i += 1
            continue

        # String literal
        if c == '"':
            j = i + 1
            while j < n:
                if src[j] == '\\':
                    if src[j:j+2] == '\\n':
                        pass  # escaped newline -- doesn't increment line counter in LSL
                    j += 2
                elif src[j] == '"':
                    j += 1
                    break
                elif src[j] == '\n':
                    line += 1
                    j += 1
                else:
                    j += 1
            tokens.append(('STRING', src[i:j], line))
            i = j
            continue

        # Hex number
        if src[i:i+2] in ('0x', '0X') and i + 2 < n:
            j = i + 2
            while j < n and src[j] in '0123456789abcdefABCDEF':
                j += 1
            tokens.append(('NUMBER', src[i:j], line))
            i = j
            continue

        # Decimal / float
        if c.isdigit():
            j = i
            while j < n and src[j].isdigit():
                j += 1
            if j < n and src[j] == '.':
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
            i = j
            continue

        # Identifier / keyword
        if c.isalpha() or c == '_':
            j = i
            while j < n and (src[j].isalnum() or src[j] == '_'):
                j += 1
            tokens.append(('IDENT', src[i:j], line))
            i = j
            continue

        # Two-character operators
        two = src[i:i+2]
        if two in ('++', '--', '==', '!=', '<=', '>=', '&&', '||',
                   '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=',
                   '<<', '>>', '...'):
            tokens.append(('OP', two, line))
            i += 2
            continue

        # Single-character tokens
        tokens.append(('PUNCT', c, line))
        i += 1

    return tokens


# ─── Declaration extraction ────────────────────────────────────────────────────

def extract_declarations(tokens):
    """
    Extract user-defined function names and global variable names from a token stream.
    Returns:
        user_funcs: dict  name → {line, param_count}
        global_vars: set  of names
        state_names: set  of names (not 'default')
    """
    user_funcs = {}
    global_vars = set()
    state_names = set()

    LSL_TYPE_TOKENS = LSL_TYPES | {"void"}

    # We look for patterns at brace depth 0:
    # Type IDENT ( ...  )  {   →  function declaration
    # Type IDENT [= or ;]       →  global variable
    # state IDENT {             →  state declaration
    # default {                 →  default state

    depth = 0
    i = 0
    while i < len(tokens):
        ttype, tval, tline = tokens[i]

        if tval == '{':
            depth += 1
            i += 1
            continue
        if tval == '}':
            if depth > 0:
                depth -= 1
            i += 1
            continue

        if depth > 0:
            i += 1
            continue

        # At depth 0 -- look for declarations

        # state NAME { or default {
        if ttype == 'IDENT' and tval in ('state', 'default'):
            if tval == 'default':
                state_names.add('default')
                i += 1
                continue
            if i + 1 < len(tokens) and tokens[i+1][0] == 'IDENT':
                state_names.add(tokens[i+1][1])
                i += 2
                continue
            i += 1
            continue

        # Void user function: IDENT '(' at depth 0 (no leading type keyword)
        # e.g.  refresh() { ... }   or   doSomething(integer x) { ... }
        _NON_FUNC_KW = LSL_TYPE_TOKENS | {'state', 'default', 'jump', 'return',
                                           'if', 'else', 'while', 'for', 'do'}
        if (ttype == 'IDENT' and tval not in _NON_FUNC_KW
                and i + 1 < len(tokens) and tokens[i+1][1] == '('):
            # Confirm it's a declaration by looking for a matching '{' eventually
            # (as opposed to a call, which ends with ';')
            # Scan forward past the parameter list to find ')' then check next token
            j = i + 2
            pdepth = 1
            while j < len(tokens) and pdepth > 0:
                if tokens[j][1] == '(':
                    pdepth += 1
                elif tokens[j][1] == ')':
                    pdepth -= 1
                j += 1
            # After closing ')': skip any optional whitespace tokens, next should be '{'
            if j < len(tokens) and tokens[j][1] == '{':
                name = tval
                # Count params
                param_count = 0
                k = i + 2
                if k < len(tokens) and tokens[k][1] != ')':
                    param_count = 1
                    kdepth = 1
                    while k < len(tokens):
                        if tokens[k][1] in ('(', '['):
                            kdepth += 1
                        elif tokens[k][1] in (')', ']'):
                            kdepth -= 1
                            if kdepth == 0:
                                break
                        elif tokens[k][1] == ',' and kdepth == 1:
                            param_count += 1
                        k += 1
                user_funcs[name] = {"line": tline, "param_count": param_count}
                i += 1
                continue

        # type IDENT ...
        if ttype == 'IDENT' and tval in LSL_TYPE_TOKENS:
            if i + 1 < len(tokens) and tokens[i+1][0] == 'IDENT':
                name = tokens[i+1][1]
                # Look at what follows the name
                if i + 2 < len(tokens):
                    next_val = tokens[i+2][1]
                    if next_val == '(':
                        # function declaration -- count params
                        param_count = 0
                        j = i + 3
                        if j < len(tokens) and tokens[j][1] != ')':
                            param_count = 1
                            pdepth = 1
                            while j < len(tokens):
                                if tokens[j][1] in ('(', '['):
                                    pdepth += 1
                                elif tokens[j][1] in (')', ']'):
                                    pdepth -= 1
                                    if pdepth == 0:
                                        break
                                elif tokens[j][1] == ',' and pdepth == 1:
                                    param_count += 1
                                j += 1
                        user_funcs[name] = {"line": tline, "param_count": param_count}
                        i += 2
                        continue
                    elif next_val in ('=', ';', ','):
                        global_vars.add(name)
                        i += 2
                        continue
                    # list type can have initialiser like list name = [...];
                    else:
                        global_vars.add(name)
                        i += 2
                        continue
        i += 1

    return user_funcs, global_vars, state_names


# ─── Individual checks ─────────────────────────────────────────────────────────

def check_unknown_functions(tokens, known_funcs, user_funcs):
    """Flag calls to identifiers that are neither built-in nor user-defined."""
    issues = []
    n = len(tokens)
    for i, (ttype, tval, tline) in enumerate(tokens):
        if ttype == 'IDENT' and i + 1 < n and tokens[i+1][1] == '(':
            # Looks like a function call
            if tval in known_funcs or tval in user_funcs:
                continue
            # Skip LSL type casts like (integer), (string), etc.
            if tval in LSL_TYPES:
                continue
            # Skip keywords used as type casts / flow control
            if tval in ('state', 'default', 'jump', 'return', 'if', 'else',
                        'while', 'for', 'do'):
                continue
            issues.append(("ERROR", "E001", tline,
                f"Unknown function '{tval}' -- not a built-in or user-defined function"))
    return issues


def check_unknown_events(tokens, known_events, user_funcs):
    """Flag event handlers whose names are not valid LSL events."""
    issues = []
    # Events appear as: IDENT '(' ... ')' '{' inside a state block
    # We detect them as identifiers immediately followed by '(' at brace depth 1
    # (depth 1 = inside a state block, not inside a function body)
    # We only flag if the IDENT directly precedes '(' AND the ')' is followed by '{'
    # (i.e. it's a declaration, not a call)
    _FLOW_KW = {'if', 'else', 'while', 'for', 'do', 'return', 'jump',
                'state', 'default', 'integer', 'float', 'string', 'key',
                'vector', 'rotation', 'list', 'void'}
    depth = 0
    n = len(tokens)
    for i, (ttype, tval, tline) in enumerate(tokens):
        if tval == '{':
            depth += 1
        elif tval == '}':
            if depth > 0:
                depth -= 1
        if depth != 1:
            continue
        if ttype != 'IDENT' or tval in _FLOW_KW:
            continue
        if i + 1 >= n or tokens[i+1][1] != '(':
            continue
        if tval in known_events or tval in user_funcs:
            continue
        # Check this is a declaration (ends with ')' '{') not a call (ends with ')' ';')
        j = i + 2
        pdepth = 1
        while j < n and pdepth > 0:
            if tokens[j][1] == '(':
                pdepth += 1
            elif tokens[j][1] == ')':
                pdepth -= 1
            j += 1
        # j now points to the token after ')'
        is_declaration = j < n and tokens[j][1] == '{'
        if is_declaration and re.match(r'^[a-z][a-z0-9_]*$', tval):
            issues.append(("WARN", "E002", tline,
                f"Unknown event handler '{tval}' -- not a valid LSL event name"))
    return issues


def check_unknown_constants(tokens, known_constants, user_funcs, global_vars):
    """Flag UPPERCASE identifiers that are not known constants or user declarations."""
    issues = []
    all_known = known_constants | set(user_funcs.keys()) | global_vars
    n = len(tokens)
    for i, (ttype, tval, tline) in enumerate(tokens):
        if ttype != 'IDENT':
            continue
        # Only check identifiers that look like constants: UPPER_CASE, len > 1
        if not re.match(r'^[A-Z][A-Z0-9_]{2,}$', tval):
            continue
        if tval in all_known:
            continue
        # Skip if this is a variable/function declaration (preceded by a type keyword)
        if i > 0 and tokens[i-1][0] == 'IDENT' and tokens[i-1][1] in LSL_TYPES:
            continue
        # Skip if this is followed by '(' -- it's a function call (checked elsewhere)
        if i + 1 < n and tokens[i+1][1] == '(':
            continue
        issues.append(("WARN", "E003", tline,
            f"Unknown constant or identifier '{tval}' -- not in LSL constant database"))
    return issues


def check_experimental_functions(tokens, known_funcs):
    """Warn about calls to experimental or broken built-in functions."""
    issues = []
    n = len(tokens)
    for i, (ttype, tval, tline) in enumerate(tokens):
        if ttype == 'IDENT' and i + 1 < n and tokens[i+1][1] == '(':
            info = known_funcs.get(tval)
            if not info:
                continue
            if info.get("broken"):
                issues.append(("WARN", "E004", tline,
                    f"'{tval}' is flagged as broken/non-functional in the LSL database"))
            elif info.get("experimental"):
                issues.append(("INFO", "E005", tline,
                    f"'{tval}' is experimental -- behaviour may change or be unavailable"))
            if info.get("godMode"):
                issues.append(("INFO", "E006", tline,
                    f"'{tval}' requires god-mode privileges -- will silently fail for normal scripts"))
    return issues


def check_sleep_functions(tokens, known_funcs):
    """Warn about functions with forced delays (sleep > 0)."""
    issues = []
    n = len(tokens)
    for i, (ttype, tval, tline) in enumerate(tokens):
        if ttype == 'IDENT' and i + 1 < n and tokens[i+1][1] == '(':
            info = known_funcs.get(tval)
            if not info:
                continue
            sleep = info.get("sleep", 0)
            if sleep and float(sleep) > 0 and tval != "llSleep":
                issues.append(("INFO", "E007", tline,
                    f"'{tval}' has a forced delay of {sleep}s -- script is paused during this time"))
    return issues


def check_brace_balance(tokens, filepath):
    """Check that all braces and parentheses are matched."""
    issues = []
    brace_stack = []
    paren_stack = []
    bracket_stack = []

    for ttype, tval, tline in tokens:
        if tval == '{':
            brace_stack.append(tline)
        elif tval == '}':
            if brace_stack:
                brace_stack.pop()
            else:
                issues.append(("ERROR", "B001", tline, "Unexpected '}' -- no matching '{'"))
        elif tval == '(':
            paren_stack.append(tline)
        elif tval == ')':
            if paren_stack:
                paren_stack.pop()
            else:
                issues.append(("ERROR", "B002", tline, "Unexpected ')' -- no matching '('"))
        elif tval == '[':
            bracket_stack.append(tline)
        elif tval == ']':
            if bracket_stack:
                bracket_stack.pop()
            else:
                issues.append(("ERROR", "B003", tline, "Unexpected ']' -- no matching '['"))

    for open_line in brace_stack:
        issues.append(("ERROR", "B001", open_line, f"Unclosed '{{' -- no matching '}}'"))
    for open_line in paren_stack:
        issues.append(("ERROR", "B002", open_line, f"Unclosed '(' -- no matching ')'"))
    for open_line in bracket_stack:
        issues.append(("ERROR", "B003", open_line, f"Unclosed '[' -- no matching ']'"))

    return issues


def check_listen_without_remove(src, tokens):
    """Warn if llListen is called without a corresponding llListenRemove."""
    issues = []
    has_listen = bool(re.search(r'\bllListen\s*\(', src))
    has_remove = bool(re.search(r'\bllListenRemove\s*\(', src))
    if has_listen and not has_remove:
        # Find line of first llListen
        for ttype, tval, tline in tokens:
            if ttype == 'IDENT' and tval == 'llListen':
                issues.append(("WARN", "L001", tline,
                    "llListen() used without llListenRemove() -- listener handle is never released"))
                break
    return issues


def check_anti_patterns(src):
    """Run regex-based anti-pattern checks on the raw source."""
    issues = []
    lines = src.split('\n')
    for pattern, severity, code, message in ANTI_PATTERNS:
        for lineno, line in enumerate(lines, 1):
            # Strip comments from the line before matching
            stripped = re.sub(r'//.*$', '', line)
            stripped = re.sub(r'"[^"]*"', '""', stripped)  # blank strings
            if re.search(pattern, stripped):
                issues.append((severity, code, lineno, message))
    return issues


def check_missing_default_state(tokens):
    """Error if no 'default' state is defined."""
    for ttype, tval, tline in tokens:
        if ttype == 'IDENT' and tval == 'default':
            return []
    return [("ERROR", "S001", 1, "No 'default' state found -- every LSL script must have a default state")]


def check_non_ascii(src):
    """Error on non-ASCII characters that the SL compiler rejects.
    The SL compiler accepts U+2500 (box-drawing dash used in comment headers)
    and Latin-1 art chars (U+00A1, U+00AF, U+00B0) found in FURWARE, but
    rejects all other code points above 0x7F.
    Common offenders: → (U+2192), — (U+2014), … (U+2026), – (U+2013),
                      × (U+00D7), ≤ (U+2264), ← (U+2190).
    Suggested ASCII replacements: -> -- ... - x <= <-
    Non-ASCII characters inside // and /* */ comments are ignored — the SL
    compiler strips comments before parsing, so they never reach the lexer.
    """
    ALLOWED = {'\u2500', '\u00A1', '\u00AF', '\u00B0'}
    issues = []
    in_block = False
    for lineno, line in enumerate(src.splitlines(), 1):
        i = 0
        n = len(line)
        while i < n:
            ch = line[i]
            if in_block:
                # Inside /* */ block comment — skip everything
                if ch == '*' and i + 1 < n and line[i + 1] == '/':
                    in_block = False
                    i += 2
                else:
                    i += 1
                continue
            # String literal — non-ASCII inside strings IS a real error
            if ch == '"':
                i += 1
                while i < n:
                    c2 = line[i]
                    i += 1
                    if c2 == '\\':
                        i += 1  # skip escape
                    elif c2 == '"':
                        break
                    elif ord(c2) > 127 and c2 not in ALLOWED:
                        issues.append(("ERROR", "E010", lineno,
                            f"Non-ASCII character U+{ord(c2):04X} {repr(c2)} at col {i}"
                            f" -- SL compiler rejects this (replace with ASCII equivalent)"))
                continue
            # Line comment — rest of line is safe to skip
            if ch == '/' and i + 1 < n and line[i + 1] == '/':
                break
            # Block comment open
            if ch == '/' and i + 1 < n and line[i + 1] == '*':
                in_block = True
                i += 2
                continue
            # Regular code character
            if ord(ch) > 127 and ch not in ALLOWED:
                issues.append(("ERROR", "E010", lineno,
                    f"Non-ASCII character U+{ord(ch):04X} {repr(ch)} at col {i + 1}"
                    f" -- SL compiler rejects this (replace with ASCII equivalent)"))
            i += 1
    return issues


def check_implicit_string_concat(tokens):
    """Error on adjacent string literals with no '+' between them.
    LSL does not support C-style implicit concatenation -- 'foo' 'bar' is a syntax error.
    """
    issues = []
    n = len(tokens)
    for i, (ttype, tval, tline) in enumerate(tokens):
        if ttype == 'STRING' and i + 1 < n and tokens[i + 1][0] == 'STRING':
            issues.append(("ERROR", "E011", tline,
                "Implicit string concatenation -- LSL requires '+' between adjacent string literals"))
    return issues


def check_deprecated_functions(tokens, known_funcs):
    """Warn about calls to deprecated built-in functions."""
    issues = []
    n = len(tokens)
    for i, (ttype, tval, tline) in enumerate(tokens):
        if ttype == 'IDENT' and i + 1 < n and tokens[i+1][1] == '(':
            info = known_funcs.get(tval)
            if not info:
                continue
            # Check for known deprecated functions
            deprecated_funcs = {
                "llSound": "Use llPlaySound() or llLoopSound() instead",
                "llStopSound": "Use llStopSound() on the sound source instead",
                "llSoundPreload": "Preloading is automatic in modern viewers",
                "llRemoteLoadScript": "Deprecated and may not work reliably",
                "llGiveInventory": "Use llGiveInventoryList() for multiple items",
            }
            if tval in deprecated_funcs:
                issues.append(("WARN", "DP001", tline,
                    f"'{tval}' is deprecated -- {deprecated_funcs[tval]}"))
    return issues


def check_unsupported_cisms(tokens):
    """Flag C/C++/JS constructs that are not valid in standard LSL.

    Checks for: ternary ?:, switch/case, break, continue, foreach,
    and lowercase true/false/null which are not LSL keywords.
    """
    issues = []
    n = len(tokens)
    _TYPES = LSL_TYPES | {"void"}
    for i, (ttype, tval, tline) in enumerate(tokens):
        prev_val = tokens[i - 1][1] if i > 0 else ""
        next_val = tokens[i + 1][1] if i + 1 < n else ""

        # Ternary operator ?: — not supported in LSL; compile error
        if ttype == 'PUNCT' and tval == '?':
            issues.append(("ERROR", "CS001", tline,
                "Ternary operator '?:' is not valid LSL — rewrite as if/else"))

        elif ttype == 'IDENT':
            # switch() — not a valid LSL keyword
            if tval == 'switch' and next_val == '(':
                issues.append(("ERROR", "CS002", tline,
                    "'switch' is not a valid LSL keyword — use if/else chains"))

            # break; as standalone statement — not valid in LSL (use jump)
            elif tval == 'break' and next_val == ';' and prev_val not in _TYPES:
                issues.append(("ERROR", "CS003", tline,
                    "'break' is not a valid LSL keyword — use 'jump' with a label to exit a loop"))

            # continue; as standalone statement — not valid in LSL (use jump)
            elif tval == 'continue' and next_val == ';' and prev_val not in _TYPES:
                issues.append(("ERROR", "CS004", tline,
                    "'continue' is not a valid LSL keyword — use 'jump' with a label"))

            # foreach() — not supported in LSL
            elif tval == 'foreach' and next_val == '(':
                issues.append(("ERROR", "CS005", tline,
                    "'foreach' is not supported in LSL — use a for/while loop with an index variable"))

            # lowercase true — undefined in LSL, should be TRUE
            elif tval == 'true' and prev_val not in _TYPES and next_val != '(':
                issues.append(("WARN", "CS006", tline,
                    "'true' is not defined in LSL — use 'TRUE' (integer 1)"))

            # lowercase false — undefined in LSL, should be FALSE
            elif tval == 'false' and prev_val not in _TYPES and next_val != '(':
                issues.append(("WARN", "CS007", tline,
                    "'false' is not defined in LSL — use 'FALSE' (integer 0)"))

            # null — not a keyword in LSL
            elif tval == 'null' and prev_val not in _TYPES and next_val != '(':
                issues.append(("WARN", "CS008", tline,
                    "'null' is not defined in LSL — use NULL_KEY for keys, 0 for integers, or \"\" for strings"))

    return issues


def check_float_equality(tokens):
    """Warn when a float literal is directly compared with == or !=.

    Floats rarely compare exactly due to IEEE 754 precision. Suggest epsilon comparison.
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


# ─── File checker ─────────────────────────────────────────────────────────────

def check_file(filepath, known_funcs, known_events, known_constants):
    """Run all checks on a single .lsl file. Returns list of (severity, code, line, msg)."""
    try:
        with open(filepath, encoding="utf-8", errors="replace") as f:
            src = f.read()
    except OSError as e:
        return [("ERROR", "IO01", 0, f"Could not read file: {e}")]

    tokens = tokenize(src)
    user_funcs, global_vars, state_names = extract_declarations(tokens)

    issues = []
    issues += check_non_ascii(src)
    issues += check_implicit_string_concat(tokens)
    issues += check_brace_balance(tokens, filepath)
    issues += check_missing_default_state(tokens)
    issues += check_unknown_functions(tokens, known_funcs, user_funcs)
    issues += check_unknown_events(tokens, known_events, user_funcs)
    issues += check_unknown_constants(tokens, known_constants, user_funcs, global_vars)
    issues += check_experimental_functions(tokens, known_funcs)
    issues += check_sleep_functions(tokens, known_funcs)
    issues += check_deprecated_functions(tokens, known_funcs)
    issues += check_listen_without_remove(src, tokens)
    issues += check_anti_patterns(src)
    issues += check_unsupported_cisms(tokens)
    issues += check_float_equality(tokens)
    issues += check_division_by_zero(tokens)

    # Sort by line number
    issues.sort(key=lambda x: (x[2], x[0]))
    return issues


# ─── Reporter ──────────────────────────────────────────────────────────────────

SEVERITY_COLOUR = {
    "ERROR": "\033[91m",  # red
    "WARN":  "\033[93m",  # yellow
    "INFO":  "\033[96m",  # cyan
}
RESET = "\033[0m"

def use_colour():
    return sys.stdout.isatty()

def report(filepath, issues):
    col = use_colour()
    rel = os.path.relpath(filepath)
    if not issues:
        prefix = f"{SEVERITY_COLOUR['INFO']}OK{RESET}" if col else "OK"
        print(f"  {prefix}  {rel}")
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


# ─── Entry point ──────────────────────────────────────────────────────────────

def find_lsl_files(root="."):
    result = []
    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            if fname.lower().endswith(".lsl"):
                result.append(os.path.join(dirpath, fname))
    return sorted(result)


def main():
    args = sys.argv[1:]

    if not args or args == ["--help"]:
        print(__doc__)
        sys.exit(0)

    json_output = "--json" in args
    args = [a for a in args if a != "--json"]

    # Determine files to check
    if "--all" in args:
        root = "."
        remaining = [a for a in args if a != "--all"]
        if remaining:
            root = remaining[0]
        files = find_lsl_files(root)
        if not files:
            print(f"No .lsl files found under '{root}'")
            sys.exit(0)
    else:
        files = [a for a in args if not a.startswith("--")]
        if not files:
            print("Usage: lsl-syntax-checker.py [--all [dir]] [--json] [file.lsl ...]")
            sys.exit(1)

    # Load cache data
    print("Loading LSL cache data...") if not json_output else None
    known_funcs     = load_known_functions()
    known_events    = load_known_events()
    known_constants = load_known_constants()
    print(f"  {len(known_funcs)} functions, {len(known_events)} events, "
          f"{len(known_constants)} constants loaded\n") if not json_output else None

    # Check files
    total_errors = total_warns = total_infos = 0
    results = {}

    for filepath in files:
        issues = check_file(filepath, known_funcs, known_events, known_constants)
        e, w, i = len([x for x in issues if x[0] == "ERROR"]), len([x for x in issues if x[0] == "WARN"]), len([x for x in issues if x[0] == "INFO"])
        total_errors += e
        total_warns += w
        total_infos += i

        if json_output:
            results[filepath] = {
                "errors": e,
                "warnings": w,
                "infos": i,
                "issues": [{"severity": s, "code": c, "line": l, "message": m} for s, c, l, m in issues]
            }
        else:
            report(filepath, issues)

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
        # Summary
        total_files = len(files)
        col = use_colour()
        ec = SEVERITY_COLOUR["ERROR"] if col else ""
        wc = SEVERITY_COLOUR["WARN"]  if col else ""
        ic = SEVERITY_COLOUR["INFO"]  if col else ""
        rc = RESET if col else ""
        print(f"\n{'-' * 60}")
        print(f"Checked {total_files} file(s) -- "
              f"{ec}{total_errors} error(s){rc}, "
              f"{wc}{total_warns} warning(s){rc}, "
              f"{ic}{total_infos} note(s){rc}")

    sys.exit(1 if total_errors > 0 else 0)


if __name__ == "__main__":
    main()
