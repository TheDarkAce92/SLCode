#!/usr/bin/env python3
"""
Build the custom SLCode bootloader for PyInstaller.

Patches the PyInstaller console bootloader (run.exe) so that SLCode can decide
at runtime — in C, before Python starts — whether to keep or free the console
window (FreeConsole for silent double-click launches, do nothing for terminal
or log-flag launches).

Requirements:
    - MinGW-w64 (gcc) in PATH
      winget install MSYS2.MSYS2  →  then in MSYS2: pacman -S mingw-w64-x86_64-gcc
      Add C:\\msys64\\mingw64\\bin to your PATH
    - WAF build tool (auto-installed from PyPI if missing)
    - PyInstaller must already be installed in the active venv

Usage:
    python build-bootloader.py              # build and install
    python build-bootloader.py --check      # check requirements only
    python build-bootloader.py --clean      # wipe WAF build cache then build

The built runw.exe is installed into the active venv's PyInstaller bootloader
directory, replacing the stock one.  Run build.py afterwards to produce a new
SLCode.exe that uses the custom bootloader.

Source repo is expected at:
    ../pyinstaller-src   (sibling of this project's directory)
Override with: python build-bootloader.py --src-dir /path/to/pyinstaller
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────

SCRIPT_DIR   = Path(__file__).resolve().parent
PATCH_DIR    = SCRIPT_DIR / "bootloader-patch"

# PyInstaller source tree (cloned separately)
_default_src = SCRIPT_DIR.parent / "pyinstaller-src"
SRC_DIR      = Path(
    next((sys.argv[i + 1] for i, a in enumerate(sys.argv)
          if a == "--src-dir" and i + 1 < len(sys.argv)), str(_default_src))
)
BOOT_DIR     = SRC_DIR / "bootloader"

# Where WAF installs the built bootloaders (relative to bootloader/ dir)
PYI_INSTALL  = SRC_DIR / "PyInstaller" / "bootloader"

# Active venv's PyInstaller bootloader directory
import site as _site
_pyi_pkg = None
for _sp in _site.getsitepackages() + [_site.getusersitepackages()]:
    _candidate = Path(_sp) / "PyInstaller" / "bootloader"
    if _candidate.exists():
        _pyi_pkg = _candidate
        break
if _pyi_pkg is None:
    # Fallback: walk venv
    for _sp in sys.path:
        _candidate = Path(_sp) / "PyInstaller" / "bootloader"
        if _candidate.exists():
            _pyi_pkg = _candidate
            break

VENV_BOOT    = _pyi_pkg
ARCH_DIR     = "Windows-64bit-intel"   # adjust for ARM if needed

CHECK_ONLY   = "--check" in sys.argv
CLEAN_BUILD  = "--clean" in sys.argv


# ── Helpers ───────────────────────────────────────────────────────────────────

def die(msg: str) -> None:
    print(f"\n[FATAL] {msg}", flush=True)
    sys.exit(1)


def run(cmd: list, cwd: Path = None, check: bool = True) -> subprocess.CompletedProcess:
    print(f"  $ {' '.join(str(c) for c in cmd)}", flush=True)
    return subprocess.run(
        [str(c) for c in cmd],
        cwd=str(cwd) if cwd else None,
        check=check,
    )


# ── Requirement checks ────────────────────────────────────────────────────────

def check_requirements() -> bool:
    ok = True

    # PyInstaller source tree
    if not BOOT_DIR.exists():
        print(f"  [FAIL] PyInstaller source not found at {SRC_DIR}")
        print(f"         Clone with:")
        print(f"           git clone --depth 1 --branch v6.19.0 "
              f"https://github.com/pyinstaller/pyinstaller.git {SRC_DIR}")
        ok = False
    else:
        print(f"  [ OK ] PyInstaller source: {SRC_DIR}")

    # Patch directory
    if not PATCH_DIR.exists():
        print(f"  [FAIL] Patch directory not found: {PATCH_DIR}")
        ok = False
    else:
        for f in ("pyi_slcode_console.h", "pyi_slcode_console.c"):
            if not (PATCH_DIR / f).exists():
                print(f"  [FAIL] Missing patch file: {PATCH_DIR / f}")
                ok = False
            else:
                print(f"  [ OK ] Patch file: {f}")

    # gcc / MinGW-w64
    gcc = shutil.which("gcc")
    if not gcc:
        print("  [FAIL] gcc not found in PATH")
        print("         Install MinGW-w64:")
        print("           winget install MSYS2.MSYS2")
        print("           # then in MSYS2 shell:")
        print("           pacman -S mingw-w64-x86_64-gcc")
        print("           # add C:\\msys64\\mingw64\\bin to PATH")
        ok = False
    else:
        print(f"  [ OK ] gcc: {gcc}")

    # WAF (bundled with PyInstaller source)
    waf_script = BOOT_DIR / "waf"
    if waf_script.exists():
        print(f"  [ OK ] WAF: bundled at {waf_script}")
    else:
        print(f"  [WARN] WAF script not found at {waf_script} — may fail at build step")

    # Venv PyInstaller
    if VENV_BOOT is None:
        print("  [FAIL] PyInstaller not found in active Python environment")
        ok = False
    else:
        print(f"  [ OK ] PyInstaller bootloader dir: {VENV_BOOT}")

    return ok


# ── Patch application ─────────────────────────────────────────────────────────

MAIN_C_MARKER  = "/* SLCode: console setup */"
MAIN_C_INCLUDE = '#include "pyi_slcode_console.h"'
MAIN_C_CALL    = "    pyi_slcode_setup_console();"

# wWinMain block (WINDOWS subsystem / runw.exe — the variant we build).
# Ends with "#else /* defined(WINDOWED) */" which is unique to this block.
_WINDOWED_BLOCK_UNPATCHED = (
    "    return pyi_main(global_pyi_ctx);\n"
    "}\n"
    "\n"
    "#else /* defined(WINDOWED) */"
)
_WINDOWED_BLOCK_OLD_CALL = "    pyi_slcode_setup_console(__argc, __wargv);\n"
_WINDOWED_BLOCK_REPLACEMENT = (
    "    " + MAIN_C_MARKER + "\n"
    "    pyi_slcode_setup_console();\n"
    "    return pyi_main(global_pyi_ctx);\n"
    "}\n"
    "\n"
    "#else /* defined(WINDOWED) */"
)

# wmain block (CONSOLE subsystem — not built, but patch for completeness).
# Ends with "#endif /* defined(WINDOWED) */" which is unique to this block.
_CONSOLE_BLOCK_TARGET = (
    "    return pyi_main(global_pyi_ctx);\n"
    "}\n"
    "\n"
    "#endif /* defined(WINDOWED) */"
)
_CONSOLE_BLOCK_REPLACEMENT = (
    "    " + MAIN_C_MARKER + "\n"
    "    pyi_slcode_setup_console();\n"
    "    return pyi_main(global_pyi_ctx);\n"
    "}\n"
    "\n"
    "#endif /* defined(WINDOWED) */"
)


def _patch_main_c(main_c: Path) -> None:
    """Insert our console-setup call into both entry points in main.c.

    Patches wWinMain (WINDOWS subsystem, runw.exe — the primary build target)
    and wmain (CONSOLE subsystem — not compiled, patched for completeness).
    """
    src = main_c.read_text(encoding="utf-8")

    # Add #include after the existing pyi_main.h include (idempotent).
    if MAIN_C_INCLUDE not in src:
        src = src.replace(
            '#include "pyi_main.h"',
            '#include "pyi_main.h"\n' + MAIN_C_INCLUDE + "  " + MAIN_C_MARKER,
        )

    # ── Patch wWinMain block ──────────────────────────────────────────────────
    if _WINDOWED_BLOCK_REPLACEMENT in src:
        print("  main.c wWinMain already patched — skipping")
    elif _WINDOWED_BLOCK_OLD_CALL in src:
        # Fix leftover old-signature call from a prior session.
        src = src.replace(_WINDOWED_BLOCK_OLD_CALL, "    pyi_slcode_setup_console();\n", 1)
        print("  main.c wWinMain old-signature call updated")
    elif _WINDOWED_BLOCK_UNPATCHED in src:
        src = src.replace(_WINDOWED_BLOCK_UNPATCHED, _WINDOWED_BLOCK_REPLACEMENT, 1)
        print("  main.c wWinMain patched successfully")
    else:
        die(
            "Could not find expected wWinMain return pattern in main.c.\n"
            "The PyInstaller source may have changed — check main.c manually."
        )

    # ── Patch wmain block ─────────────────────────────────────────────────────
    if _CONSOLE_BLOCK_REPLACEMENT in src:
        print("  main.c wmain already patched — skipping")
    elif _CONSOLE_BLOCK_TARGET in src:
        src = src.replace(_CONSOLE_BLOCK_TARGET, _CONSOLE_BLOCK_REPLACEMENT, 1)
        print("  main.c wmain patched successfully")
    else:
        print("  main.c wmain block not found — skipping (may already be patched)")

    main_c.write_text(src, encoding="utf-8")


def apply_patches() -> None:
    print("\nApplying patches to bootloader source...")

    # Copy our C files into bootloader/src/
    for fname in ("pyi_slcode_console.h", "pyi_slcode_console.c"):
        src  = PATCH_DIR / fname
        dest = BOOT_DIR / "src" / fname
        shutil.copyfile(src, dest)
        print(f"  Copied {fname} -> bootloader/src/")

    # Patch main.c
    _patch_main_c(BOOT_DIR / "src" / "main.c")


# ── WAF build ─────────────────────────────────────────────────────────────────

def ensure_waf() -> None:
    # WAF is bundled with the PyInstaller source at bootloader/waf — no install needed.
    waf_script = BOOT_DIR / "waf"
    if not waf_script.exists():
        die(f"WAF script not found at {waf_script}\nIs the PyInstaller source at {SRC_DIR} complete?")


def build_bootloader() -> None:
    print("\nConfiguring bootloader build (MinGW-w64, 64-bit)...")

    if CLEAN_BUILD:
        build_cache = BOOT_DIR / "build"
        if build_cache.exists():
            shutil.rmtree(build_cache)
            print("  Cleaned build cache")

    waf = [sys.executable, str(BOOT_DIR / "waf")]

    run(waf + ["configure", "--gcc", "--target-arch=64bit"], cwd=BOOT_DIR)

    print("\nBuilding console release variant (run.exe)...")
    run(waf + ["build_release"], cwd=BOOT_DIR)

    print("\nInstalling into PyInstaller source tree...")
    run(waf + ["install_release"], cwd=BOOT_DIR)


# ── Install into venv ─────────────────────────────────────────────────────────

def install_to_venv() -> None:
    if VENV_BOOT is None:
        die("Cannot locate PyInstaller in the active Python environment.")

    src_run   = PYI_INSTALL / ARCH_DIR / "run.exe"
    dest_dir  = VENV_BOOT / ARCH_DIR
    dest_run  = dest_dir / "run.exe"

    if not src_run.exists():
        die(f"Built run.exe not found at {src_run}\nCheck WAF build output above.")

    dest_dir.mkdir(parents=True, exist_ok=True)

    # Back up stock bootloader
    backup = dest_dir / "run.exe.stock"
    if not backup.exists() and dest_run.exists():
        shutil.copyfile(dest_run, backup)
        print(f"\n  Backed up stock run.exe -> run.exe.stock")

    shutil.copyfile(src_run, dest_run)
    print(f"  Installed custom run.exe -> {dest_run}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    print("SLCode Bootloader Builder")
    print("=" * 50)

    print("\nChecking requirements...")
    ok = check_requirements()

    if CHECK_ONLY:
        sys.exit(0 if ok else 1)

    if not ok:
        die("Requirements not met — fix the issues above and re-run.")

    ensure_waf()
    apply_patches()
    build_bootloader()
    install_to_venv()

    print("\n" + "=" * 50)
    print("Custom bootloader installed successfully.")
    print("Run  python build.py  to produce a new SLCode.exe.")


if __name__ == "__main__":
    main()
