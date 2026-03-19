#!/usr/bin/env python3
"""SLCode launcher wrapper.

Controls terminal/console behavior and delegates runtime to search-cache.py.
"""

from __future__ import annotations

import os
import runpy
import subprocess
import sys
from pathlib import Path
from typing import Mapping

# ── Console state (established by C bootloader before Python starts) ──────────
# The custom run.exe bootloader (pyi_slcode_console.c) calls FreeConsole()
# when the launch is a silent double-click with no log flags.  For all other
# cases — terminal launch, WT/ConPTY, or double-click with log flags — the
# console is left attached.
#
# Python's CONSOLE-subsystem init automatically wires sys.stdout/stderr to the
# inherited console handles, so no manual redirection is needed here.

CHILD_FLAG = "--slcode-server-child"
import tempfile
_NEW_GROUP = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
FORCE_INLINE_FLAG = "SLCODE_FORCE_INLINE"

NON_SERVE_COMMANDS = {
    "status", "search", "doc", "lookup", "completions", "check", "analyze",
    "debug", "format", "flatten", "fs", "cache", "serve", "run-skill"
}

# Use a fixed AppData path so both parent and child (which has a custom TEMP)
# write to the same log file.
def _log_path() -> Path:
    local = os.environ.get("LOCALAPPDATA", "")
    if local:
        return Path(local) / "SLCode" / "slcode-launcher.log"
    return Path(tempfile.gettempdir()) / "slcode-launcher.log"

_LAUNCHER_LOG = _log_path()


def _diag(msg: str) -> None:
    try:
        _LAUNCHER_LOG.parent.mkdir(parents=True, exist_ok=True)
        with _LAUNCHER_LOG.open("a", encoding="utf-8", errors="replace") as f:
            f.write(msg + "\n")
    except Exception:
        pass


def _is_frozen() -> bool:
    return bool(getattr(sys, "frozen", False))


def _launcher_path() -> Path:
    return Path(sys.executable).resolve() if _is_frozen() else Path(__file__).resolve()


def _search_cache_path() -> Path:
    candidates: list[Path] = []
    if _is_frozen():
        meipass = Path(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent))
        candidates.extend([
            meipass / "_slcode_runtime.py",
            meipass / "search-cache.py",
            Path(sys.executable).resolve().parent / "_slcode_runtime.py",
            Path(sys.executable).resolve().parent / "search-cache.py",
        ])
    candidates.append(Path(__file__).resolve().parent / "search-cache.py")
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def _is_terminal_launch() -> bool:
    """Return True if a console is attached to this process.

    With the CONSOLE-subsystem bootloader:
      - Double-click, no log flags → FreeConsole() was called → no console → False
      - Terminal launch or double-click with log flags → console present → True
    """
    if sys.platform == "win32":
        try:
            import ctypes
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            result = bool(hwnd)
            _diag(f"terminal-detect: GetConsoleWindow={hwnd} -> {result}")
            return result
        except Exception:
            return False
    try:
        return bool(
            (sys.stdin and sys.stdin.isatty())
            or (sys.stdout and sys.stdout.isatty())
            or (sys.stderr and sys.stderr.isatty())
        )
    except Exception:
        return False


def _is_serve_invocation(argv: list[str]) -> bool:
    if not argv:
        return True
    first = argv[0]
    if first in NON_SERVE_COMMANDS:
        return first == "serve"
    return True


def _wants_logs(argv: list[str]) -> bool:
    tokens = set(argv)
    return bool(
        "-browser" in tokens
        or "--as-browser" in tokens
        or "-none" in tokens
        or "--no-open" in tokens
    )


def _set_log_env(env: Mapping[str, str], enabled: bool) -> dict[str, str]:
    out = dict(env)
    out["SLCODE_LOG_ENABLED"] = "1" if enabled else "0"
    return out


def _self_cmd(argv: list[str]) -> list[str]:
    if _is_frozen():
        return [str(_launcher_path()), *argv]
    return [sys.executable, str(_launcher_path()), *argv]


def _child_runtime_dir() -> str:
    """Create and return a persistent temp dir for the child's PyInstaller extraction.

    By pointing TMP/TEMP at a dir the parent never uses, the child's _MEIPASS
    extraction lands in a separate location.  When the parent exits and its
    bootloader cleanup removes its own _MEIPASS, the child's copy is untouched.

    Also removes _MEI* dirs from previous builds so old extractions don't
    accumulate (version rotation: new build → new content hash → new _MEI name).
    """
    try:
        local = os.environ.get("LOCALAPPDATA", "")
        base = Path(local) if local else Path.home() / "AppData" / "Local"
        rt = base / "SLCode" / "runtime"
        rt.mkdir(parents=True, exist_ok=True)
        if _is_frozen():
            current_mei = Path(getattr(sys, "_MEIPASS", "")).name  # e.g. "_MEI36762"
            if current_mei:
                import shutil
                for d in rt.iterdir():
                    if d.is_dir() and d.name.startswith("_MEI") and d.name != current_mei:
                        try:
                            shutil.rmtree(str(d), ignore_errors=True)
                            _diag(f"runtime-dir: removed old {d.name}")
                        except Exception:
                            pass
        return str(rt)
    except Exception as _e:
        _diag(f"runtime-dir: setup failed ({_e})")
        return ""


def _kill_own_watcher() -> None:
    """PyInstaller 6.x onefile uses a two-process model on Windows: the exe
    (Watcher) extracts _MEIPASS, spawns the Python child, waits for it, then
    deletes _MEIPASS.  When we TerminateProcess our own Python child, Watcher
    detects the exit and runs cleanup — racing against our newly-spawned Case-3
    child that still needs those files.

    Fix: terminate Watcher before we exit, so it never runs cleanup.  We only
    kill the parent if it is another instance of this executable (safety guard
    so we never accidentally kill the terminal or shell).
    """
    if not _is_frozen() or sys.platform != "win32":
        return
    try:
        import ctypes
        import ctypes.wintypes
        kernel32 = ctypes.windll.kernel32
        parent_pid = os.getppid()
        if not parent_pid:
            return
        _QUERY = 0x1000  # PROCESS_QUERY_LIMITED_INFORMATION
        _TERM  = 0x0001  # PROCESS_TERMINATE
        h = kernel32.OpenProcess(_QUERY | _TERM, False, parent_pid)
        if not h:
            _diag("spawn: could not open parent process (not a watcher?)")
            return
        try:
            buf  = ctypes.create_unicode_buffer(32768)
            size = ctypes.wintypes.DWORD(32768)
            kernel32.QueryFullProcessImageNameW(h, 0, buf, ctypes.byref(size))
            parent_exe  = buf.value.lower()
            current_exe = str(Path(sys.executable).resolve()).lower()
            if parent_exe == current_exe:
                kernel32.TerminateProcess(h, 0)
                _diag(f"spawn: killed watcher pid={parent_pid}")
            else:
                _diag(f"spawn: parent is not SLCode (it is {Path(parent_exe).name}), skipping watcher kill")
        finally:
            kernel32.CloseHandle(h)
    except Exception as _e:
        _diag(f"spawn: kill watcher failed ({_e})")


def _hide_own_console_if_visible() -> None:
    if sys.platform != "win32":
        return
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        user32   = ctypes.windll.user32
        hwnd = kernel32.GetConsoleWindow()
        if hwnd:
            user32.ShowWindow(hwnd, 0)  # SW_HIDE
    except Exception:
        pass



def _spawn_detached(argv: list[str], log_enabled: bool) -> int:
    env = _set_log_env(os.environ, log_enabled)
    env[FORCE_INLINE_FLAG] = "1"
    env.setdefault("SLCODE_WINDOW_MODE", "webview")
    cwd = str(Path(sys.executable).resolve().parent if _is_frozen() else Path(__file__).resolve().parent)
    if sys.platform == "win32":
        # CREATE_NEW_CONSOLE gives the PyInstaller bootloader a real console to
        # work with (DETACHED_PROCESS breaks it).  STARTUPINFO SW_HIDE keeps
        # the window invisible.  CREATE_NEW_PROCESS_GROUP isolates signals.
        # CREATE_BREAKAWAY_FROM_JOB removes the child from the terminal's
        # Windows Job Object so it is not killed when the parent exits.
        _NEW_CONSOLE = getattr(subprocess, "CREATE_NEW_CONSOLE", 0x00000010)
        _BREAKAWAY = 0x01000000  # CREATE_BREAKAWAY_FROM_JOB
        si = subprocess.STARTUPINFO()
        si.dwFlags = subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = 0  # SW_HIDE
        _flags = _NEW_CONSOLE | _NEW_GROUP | _BREAKAWAY
        _popen_kwargs: dict = dict(
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            startupinfo=si,
            close_fds=True,
            env=env,
            cwd=cwd,
        )
        try:
            subprocess.Popen(_self_cmd(argv), creationflags=_flags, **_popen_kwargs)
            _diag("spawn: breakaway ok")
        except OSError as _be:
            _diag(f"spawn: breakaway failed ({_be}), retrying without")
            try:
                subprocess.Popen(_self_cmd(argv), creationflags=_NEW_CONSOLE | _NEW_GROUP, **_popen_kwargs)
                _diag("spawn: fallback popen ok")
            except OSError as _fe:
                _diag(f"spawn: fallback also failed ({_fe}), returning 1")
                return 1
        os._exit(0)
    else:
        subprocess.Popen(
            _self_cmd(argv),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            close_fds=True,
            env=env,
            cwd=cwd,
        )
    return 0


def _install_thread_excepthook() -> None:
    """Log uncaught exceptions from background threads (e.g. webview, HTTP server)."""
    import threading
    import traceback
    def _hook(args: threading.ExceptHookArgs) -> None:
        if args.exc_type is SystemExit:
            _diag(f"thread-exit: thread={args.thread.name if args.thread else '?'} "
                  f"code={args.exc_value.code if args.exc_value else '?'}")
            return
        tb = "".join(traceback.format_exception(args.exc_type, args.exc_value, args.exc_tb))
        _diag(f"thread-crash: thread={args.thread.name if args.thread else '?'}\n{tb}")
    threading.excepthook = _hook


def _run_search_cache_inproc(argv: list[str]) -> int:
    _install_thread_excepthook()
    if _is_frozen():
        # Strategy 1: frozen hidden-import module
        try:
            import slcode_runtime  # type: ignore
            _diag(f"inproc: meipass={getattr(sys, '_MEIPASS', 'NONE')}")
            _diag(f"inproc: cache_base={slcode_runtime.CACHE_BASE}")
            _diag(f"inproc: cache_root={slcode_runtime.CACHE_ROOT} exists={slcode_runtime.CACHE_ROOT.exists()}")
            old_argv = sys.argv[:]
            try:
                sys.argv = [str(_launcher_path()), *argv]
                _diag("inproc: calling main()")
                rc = slcode_runtime.main()
                _diag(f"inproc: main() returned rc={rc}")
                return int(rc) if isinstance(rc, int) else 0
            except SystemExit as se:
                _diag(f"inproc: main() raised SystemExit({se.code})")
                return int(se.code) if isinstance(se.code, int) else 0
            except BaseException as be:
                import traceback as _tb
                _diag(f"inproc: main() raised {type(be).__name__}: {be}\n"
                      + "".join(_tb.format_exc()))
                raise
            finally:
                sys.argv = old_argv
        except SystemExit as se:
            _diag(f"child-warning: SystemExit({se.code}) during import, trying file fallback")
        except Exception as exc:
            _diag(f"child-warning: slcode_runtime import failed ({exc}), trying file fallback")

        # Strategy 2: runpy on the bundled add-data copy
        meipass = Path(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent))
        for candidate in [meipass / "_slcode_runtime.py", meipass / "search-cache.py"]:
            if candidate.exists():
                try:
                    module_globals = runpy.run_path(str(candidate), run_name="slcode_search_cache")
                    main_fn = module_globals.get("main")
                    if callable(main_fn):
                        old_argv = sys.argv[:]
                        try:
                            sys.argv = [str(_launcher_path()), *argv]
                            _diag(f"inproc-fallback: calling main() from {candidate.name}")
                            rc = main_fn()
                            _diag(f"inproc-fallback: main() returned rc={rc}")
                            return int(rc) if isinstance(rc, int) else 0
                        except SystemExit as se:
                            _diag(f"inproc-fallback: SystemExit({se.code})")
                            return int(se.code) if isinstance(se.code, int) else 0
                        finally:
                            sys.argv = old_argv
                except Exception as exc2:
                    _diag(f"child-error: runpy fallback failed on {candidate}: {exc2}")

        _diag("child-error: all frozen runtime strategies failed")
        return 1

    # Non-frozen: runpy on search-cache.py directly
    script = _search_cache_path()
    if not script.exists():
        _diag(f"child-error: search-cache missing at {script}")
        return 1
    try:
        module_globals = runpy.run_path(str(script), run_name="slcode_search_cache")
    except Exception as exc:
        _diag(f"child-error: runpy failed: {exc}")
        return 1
    main_fn = module_globals.get("main")
    if not callable(main_fn):
        _diag("child-error: search-cache main() not found")
        return 1
    old_argv = sys.argv[:]
    try:
        sys.argv = [str(script), *argv]
        rc = main_fn()
        return int(rc) if isinstance(rc, int) else 0
    finally:
        sys.argv = old_argv


def main() -> int:
    argv = list(sys.argv[1:])
    _diag(f"launcher-main argv={argv}")

    # Detached re-entry (Case 3 child): run server in-process immediately
    if os.environ.get(FORCE_INLINE_FLAG, "") == "1":
        _diag(f"launcher-force-inline argv={argv}")
        _hide_own_console_if_visible()
        _diag("launcher-force-inline: starting runtime")
        try:
            rc = _run_search_cache_inproc(argv)
            _diag(f"launcher-force-inline: runtime returned rc={rc}")
            return rc
        except SystemExit as se:
            _diag(f"launcher-force-inline: SystemExit({se.code})")
            return int(se.code) if isinstance(se.code, int) else 0
        except BaseException as exc:
            import traceback as _tb
            _diag(f"launcher-force-inline: runtime raised {type(exc).__name__}: {exc}\n"
                  + "".join(_tb.format_exc()))
            return 1

    # Legacy child flag — kept for compatibility; should not appear in normal flow
    if CHILD_FLAG in argv:
        child_argv = [a for a in argv if a != CHILD_FLAG]
        _diag(f"child-start argv={child_argv}")
        return _run_search_cache_inproc(child_argv)

    is_serve = _is_serve_invocation(argv)
    wants_logs = _wants_logs(argv) if is_serve else False

    from_terminal = _is_terminal_launch()

    _diag(f"parent-start terminal={from_terminal} wants_logs={wants_logs} argv={argv}")

    if is_serve and from_terminal and not wants_logs:
        # Case 3: console present, no logs → detach so the prompt returns immediately.
        return _spawn_detached(argv, log_enabled=False)

    if is_serve and not from_terminal and not wants_logs:
        # Case 1: no console (FreeConsole was called in C) → silent GUI launch.
        _hide_own_console_if_visible()
        return _run_search_cache_inproc(argv)

    # Case 4: console present + log flags (terminal or double-click shortcut),
    # or any non-serve command.  sys.stdout/stderr are already live.
    return _run_search_cache_inproc(argv)


if __name__ == "__main__":
    raise SystemExit(main())
