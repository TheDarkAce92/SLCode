#!/usr/bin/env python3
# Skill: search-cache
# Version: 0.1.0.7
# Purpose: SLCode — LSL documentation browser and IDE
# Usage: python3 search-cache.py [serve|status|search|doc] [options]
# Created: 2026-03-09
# Last modified: 2026-03-11

"""
Starts a local HTTP server and opens a browser UI for searching the LSL cache.
No external dependencies — uses only Python stdlib.
"""

import importlib.util
import argparse
import json
import os
import re
import signal
import subprocess
import sys
import tempfile
import time
import threading
import uuid
import webbrowser
from collections import deque
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs, unquote

# ── Config ──────────────────────────────────────────────────────────────────

APP_ROOT = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
BUNDLE_ROOT = Path(getattr(sys, "_MEIPASS", APP_ROOT))
LOCAL_CACHE_BASE = APP_ROOT / "LSL Cache"
BUNDLED_CACHE_BASE = BUNDLE_ROOT / "LSL Cache"

def _set_splash_event(name: str) -> None:
  """Set a named splash event created by the C stub for the current PID.
 
  The stub creates SLCode<Name>_<pid> events before launching Python.
  Setting a status event (auto-reset) updates the splash label.
  Setting SLCodeReady (manual-reset) closes the splash.
  Safe no-op when not running under the GUI stub.
  """

  stub_pid = os.environ.get("SLCODE_STUB_PID", "")
  if not stub_pid or sys.platform != "win32":
    return
  try:
    import ctypes
    kernel32 = ctypes.windll.kernel32
    ev = kernel32.OpenEventW(0x0002, False, f"{name}_{stub_pid}")
    if ev:
      kernel32.SetEvent(ev)
      kernel32.CloseHandle(ev)
  except Exception:
    pass

def _signal_splash_seeding()  -> None: _set_splash_event("SLCodeSeeding")
def _signal_splash_server()   -> None: _set_splash_event("SLCodeServer")
def _signal_splash_webview()  -> None: _set_splash_event("SLCodeWebview")
def _signal_splash_pageload() -> None: _set_splash_event("SLCodePageLoad")
def _signal_splash_ready()    -> None: _set_splash_event("SLCodeReady")


_WINDOW_RESTORE_BOUNDS = None
_WINDOW_MANUAL_MAXIMIZED = False
_WINDOW_NATIVE_FRAME_APPLIED = False
_WINDOW_WNDPROC = None
_WINDOW_OLD_WNDPROC = None
_USE_FRAMELESS_WINDOW = False


def _get_pywebview_hwnd() -> int:
  if sys.platform != "win32":
    return 0
  try:
    import ctypes
    user32 = ctypes.windll.user32
    hwnd = user32.GetForegroundWindow()
    if hwnd:
      return hwnd
    return user32.FindWindowW(None, "SLCode")
  except Exception:
    return 0


def _apply_native_window_frame() -> None:
  global _WINDOW_NATIVE_FRAME_APPLIED, _WINDOW_WNDPROC, _WINDOW_OLD_WNDPROC
  if _WINDOW_NATIVE_FRAME_APPLIED or sys.platform != "win32":
    return
  try:
    import ctypes

    class RECT(ctypes.Structure):
      _fields_ = [("left", ctypes.c_long), ("top", ctypes.c_long),
                  ("right", ctypes.c_long), ("bottom", ctypes.c_long)]

    hwnd = _get_pywebview_hwnd()
    if not hwnd:
      return

    user32 = ctypes.windll.user32
    dwmapi = ctypes.windll.dwmapi

    GWL_STYLE = -16
    GWL_EXSTYLE = -20
    GWLP_WNDPROC = -4
    WS_BORDER = 0x00800000
    WS_CAPTION = 0x00C00000
    WS_POPUP = 0x80000000
    WS_CLIPCHILDREN = 0x02000000
    WS_THICKFRAME = 0x00040000
    WS_MINIMIZEBOX = 0x00020000
    WS_MAXIMIZEBOX = 0x00010000
    WS_SYSMENU = 0x00080000
    WS_EX_COMPOSITED = 0x02000000
    WM_ERASEBKGND = 0x0014
    WM_NCHITTEST = 0x0084
    HTCLIENT = 1
    HTLEFT = 10
    HTRIGHT = 11
    HTTOP = 12
    HTTOPLEFT = 13
    HTTOPRIGHT = 14
    HTBOTTOM = 15
    HTBOTTOMLEFT = 16
    HTBOTTOMRIGHT = 17
    SWP_NOMOVE = 0x0002
    SWP_NOSIZE = 0x0001
    SWP_NOZORDER = 0x0004
    SWP_FRAMECHANGED = 0x0020
    SWP_NOACTIVATE = 0x0010
    DWMWA_WINDOW_CORNER_PREFERENCE = 33
    DWMWA_BORDER_COLOR = 34
    DWMWA_CAPTION_COLOR = 35
    DWMWA_TEXT_COLOR = 36
    DWMWCP_ROUND = 2
    resize_margin = 16

    get_style = getattr(user32, "GetWindowLongPtrW", user32.GetWindowLongW)
    set_style = getattr(user32, "SetWindowLongPtrW", user32.SetWindowLongW)
    call_window_proc = getattr(user32, "CallWindowProcW")

    if _USE_FRAMELESS_WINDOW:
      style = get_style(hwnd, GWL_STYLE)
      style &= ~WS_POPUP
      style |= (WS_CAPTION | WS_BORDER | WS_THICKFRAME | WS_MINIMIZEBOX |
                WS_MAXIMIZEBOX | WS_SYSMENU | WS_CLIPCHILDREN)
      set_style(hwnd, GWL_STYLE, style)

      ex_style = get_style(hwnd, GWL_EXSTYLE)
      ex_style |= WS_EX_COMPOSITED
      set_style(hwnd, GWL_EXSTYLE, ex_style)

      user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0,
                          SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER |
                          SWP_NOACTIVATE | SWP_FRAMECHANGED)

    pref = ctypes.c_int(DWMWCP_ROUND)
    try:
      dwmapi.DwmSetWindowAttribute(
        hwnd,
        DWMWA_WINDOW_CORNER_PREFERENCE,
        ctypes.byref(pref),
        ctypes.sizeof(pref),
      )
    except Exception:
      pass

    try:
      # Theme native frame to match CSS vars:
      # --border:  #2a2d3e
      # --surface: #1a1d27
      # --text:    #d4d8f0
      border_color = ctypes.c_uint(0x003E2D2A)
      dwmapi.DwmSetWindowAttribute(
        hwnd,
        DWMWA_BORDER_COLOR,
        ctypes.byref(border_color),
        ctypes.sizeof(border_color),
      )
    except Exception:
      pass

    try:
      caption_color = ctypes.c_uint(0x00271D1A)
      text_color = ctypes.c_uint(0x00F0D8D4)
      dwmapi.DwmSetWindowAttribute(
        hwnd,
        DWMWA_CAPTION_COLOR,
        ctypes.byref(caption_color),
        ctypes.sizeof(caption_color),
      )
      dwmapi.DwmSetWindowAttribute(
        hwnd,
        DWMWA_TEXT_COLOR,
        ctypes.byref(text_color),
        ctypes.sizeof(text_color),
      )
    except Exception:
      pass

    if _USE_FRAMELESS_WINDOW:
      WNDPROC = ctypes.WINFUNCTYPE(ctypes.c_longlong, ctypes.c_void_p, ctypes.c_uint,
                                   ctypes.c_ulonglong, ctypes.c_longlong)

      def _wndproc(sub_hwnd, msg, wparam, lparam):
        if msg == WM_ERASEBKGND:
          return 1

        if msg == WM_NCHITTEST and not user32.IsZoomed(sub_hwnd):
          result = call_window_proc(_WINDOW_OLD_WNDPROC, sub_hwnd, msg, wparam, lparam)
          if result == HTCLIENT:
            rect = RECT()
            user32.GetWindowRect(sub_hwnd, ctypes.byref(rect))
            x = ctypes.c_short(lparam & 0xFFFF).value
            y = ctypes.c_short((lparam >> 16) & 0xFFFF).value
            on_left = rect.left <= x < rect.left + resize_margin
            on_right = rect.right - resize_margin <= x < rect.right
            on_top = rect.top <= y < rect.top + resize_margin
            on_bottom = rect.bottom - resize_margin <= y < rect.bottom

            if on_top and on_left:
              return HTTOPLEFT
            if on_top and on_right:
              return HTTOPRIGHT
            if on_bottom and on_left:
              return HTBOTTOMLEFT
            if on_bottom and on_right:
              return HTBOTTOMRIGHT
            if on_left:
              return HTLEFT
            if on_right:
              return HTRIGHT
            if on_top:
              return HTTOP
            if on_bottom:
              return HTBOTTOM
            return result
        return call_window_proc(_WINDOW_OLD_WNDPROC, sub_hwnd, msg, wparam, lparam)

      _WINDOW_WNDPROC = WNDPROC(_wndproc)
      _WINDOW_OLD_WNDPROC = set_style(hwnd, GWLP_WNDPROC, _WINDOW_WNDPROC)

    _WINDOW_NATIVE_FRAME_APPLIED = True
  except Exception:
    pass


def _resolve_cache_base() -> Path:
  """Resolve the active cache directory.

  Priority:
    1. LSL_CACHE_BASE env var — explicit user/team override.
    2. %LOCALAPPDATA%/SLCode/LSL Cache — persistent, writable location.
       Seeded from the bundled _MEIPASS copy on first run so the app works
       out-of-the-box. All tool writes go here and survive app updates.
    3. Next to the script — dev-mode fallback only.
  """
  env_base = os.environ.get("LSL_CACHE_BASE", "").strip()
  if env_base:
    return Path(env_base).expanduser()

  local = os.environ.get("LOCALAPPDATA", "")
  persistent = (Path(local) if local else Path.home() / "AppData" / "Local") / "SLCode" / "LSL Cache"

  # Seed the persistent cache from the bundle if cache-manifest.json is absent.
  # The manifest is always written during a proper cache build, so its presence
  # is a reliable indicator that the cache is populated — more robust than
  # checking lsl-docs/ alone, which can exist due to leftover files (.gh-token etc.)
  if not (persistent / "cache-manifest.json").exists() and BUNDLED_CACHE_BASE.exists():
    print("[slcode] Seeding cache from bundle…", flush=True)
    _signal_splash_seeding()
    try:
      import shutil
      # Skills live in the app bundle (SLCode-app/) and are always loaded from
      # BUNDLED_SKILLS_PATH — don't copy them to the persistent cache so they
      # stay up-to-date with each app update.
      ignore = shutil.ignore_patterns("skills")
      persistent.parent.mkdir(parents=True, exist_ok=True)
      if not persistent.exists():
        shutil.copytree(str(BUNDLED_CACHE_BASE), str(persistent), ignore=ignore)
      else:
        # Directory exists but has no docs (e.g. only a .gh-token) — merge bundle in.
        shutil.copytree(str(BUNDLED_CACHE_BASE), str(persistent),
                        ignore=ignore, dirs_exist_ok=True)
    except Exception as _seed_err:
      print(f"[slcode] Warning: failed to seed cache from bundle: {_seed_err}", flush=True)

  if persistent.exists():
    return persistent

  # Dev/unfrozen fallback — prefer source tree copy so edits are live.
  if LOCAL_CACHE_BASE.exists():
    return LOCAL_CACHE_BASE
  if BUNDLED_CACHE_BASE.exists():
    return BUNDLED_CACHE_BASE
  return persistent  # return target even if absent so tool writes land correctly


CACHE_BASE          = _resolve_cache_base()
CACHE_ROOT          = CACHE_BASE / "lsl-docs"
SKILLS_PATH         = CACHE_BASE / "skills"
BUNDLED_SKILLS_PATH = BUNDLED_CACHE_BASE / "skills"  # always in _MEIPASS — used by run-skill

# marked.js bundled inline so the doc viewer works offline (no CDN required)
import base64 as _b64
MARKED_JS = _b64.b64decode(
    b"LyoqCiAqIG1hcmtlZCB2MTUuMC4xMiAtIGEgbWFya2Rvd24gcGFyc2VyCiAqIENvcHlyaWdodCAo"
    b"YykgMjAxMS0yMDI1LCBDaHJpc3RvcGhlciBKZWZmcmV5LiAoTUlUIExpY2Vuc2VkKQogKiBodHRw"
    b"czovL2dpdGh1Yi5jb20vbWFya2VkanMvbWFya2VkCiAqLwoKLyoqCiAqIERPIE5PVCBFRElUIFRI"
    b"SVMgRklMRQogKiBUaGUgY29kZSBpbiB0aGlzIGZpbGUgaXMgZ2VuZXJhdGVkIGZyb20gZmlsZXMg"
    b"aW4gLi9zcmMvCiAqLwooZnVuY3Rpb24oZyxmKXtpZih0eXBlb2YgZXhwb3J0cz09Im9iamVjdCIm"
    b"JnR5cGVvZiBtb2R1bGU8InUiKXttb2R1bGUuZXhwb3J0cz1mKCl9ZWxzZSBpZigiZnVuY3Rpb24i"
    b"PT10eXBlb2YgZGVmaW5lICYmIGRlZmluZS5hbWQpe2RlZmluZSgibWFya2VkIixmKX1lbHNlIHtn"
    b"WyJtYXJrZWQiXT1mKCl9fSh0eXBlb2YgZ2xvYmFsVGhpcyA8ICJ1IiA/IGdsb2JhbFRoaXMgOiB0"
    b"eXBlb2Ygc2VsZiA8ICJ1IiA/IHNlbGYgOiB0aGlzLGZ1bmN0aW9uKCl7dmFyIGV4cG9ydHM9e307"
    b"dmFyIF9fZXhwb3J0cz1leHBvcnRzO3ZhciBtb2R1bGU9e2V4cG9ydHN9OwoidXNlIHN0cmljdCI7"
    b"dmFyIEg9T2JqZWN0LmRlZmluZVByb3BlcnR5O3ZhciBiZT1PYmplY3QuZ2V0T3duUHJvcGVydHlE"
    b"ZXNjcmlwdG9yO3ZhciBUZT1PYmplY3QuZ2V0T3duUHJvcGVydHlOYW1lczt2YXIgd2U9T2JqZWN0"
    b"LnByb3RvdHlwZS5oYXNPd25Qcm9wZXJ0eTt2YXIgeWU9KGwsZSk9Pntmb3IodmFyIHQgaW4gZSlI"
    b"KGwsdCx7Z2V0OmVbdF0sZW51bWVyYWJsZTohMH0pfSxSZT0obCxlLHQsbik9PntpZihlJiZ0eXBl"
    b"b2YgZT09Im9iamVjdCJ8fHR5cGVvZiBlPT0iZnVuY3Rpb24iKWZvcihsZXQgcyBvZiBUZShlKSkh"
    b"d2UuY2FsbChsLHMpJiZzIT09dCYmSChsLHMse2dldDooKT0+ZVtzXSxlbnVtZXJhYmxlOiEobj1i"
    b"ZShlLHMpKXx8bi5lbnVtZXJhYmxlfSk7cmV0dXJuIGx9O3ZhciBTZT1sPT5SZShIKHt9LCJfX2Vz"
    b"TW9kdWxlIix7dmFsdWU6ITB9KSxsKTt2YXIga3Q9e307eWUoa3Qse0hvb2tzOigpPT5MLExleGVy"
    b"OigpPT54LE1hcmtlZDooKT0+RSxQYXJzZXI6KCk9PmIsUmVuZGVyZXI6KCk9PiQsVGV4dFJlbmRl"
    b"cmVyOigpPT5fLFRva2VuaXplcjooKT0+UyxkZWZhdWx0czooKT0+dyxnZXREZWZhdWx0czooKT0+"
    b"eixsZXhlcjooKT0+aHQsbWFya2VkOigpPT5rLG9wdGlvbnM6KCk9Pml0LHBhcnNlOigpPT5wdCxw"
    b"YXJzZUlubGluZTooKT0+Y3QscGFyc2VyOigpPT51dCxzZXRPcHRpb25zOigpPT5vdCx1c2U6KCk9"
    b"Pmx0LHdhbGtUb2tlbnM6KCk9PmF0fSk7bW9kdWxlLmV4cG9ydHM9U2Uoa3QpO2Z1bmN0aW9uIHoo"
    b"KXtyZXR1cm57YXN5bmM6ITEsYnJlYWtzOiExLGV4dGVuc2lvbnM6bnVsbCxnZm06ITAsaG9va3M6"
    b"bnVsbCxwZWRhbnRpYzohMSxyZW5kZXJlcjpudWxsLHNpbGVudDohMSx0b2tlbml6ZXI6bnVsbCx3"
    b"YWxrVG9rZW5zOm51bGx9fXZhciB3PXooKTtmdW5jdGlvbiBOKGwpe3c9bH12YXIgST17ZXhlYzoo"
    b"KT0+bnVsbH07ZnVuY3Rpb24gaChsLGU9IiIpe2xldCB0PXR5cGVvZiBsPT0ic3RyaW5nIj9sOmwu"
    b"c291cmNlLG49e3JlcGxhY2U6KHMsaSk9PntsZXQgcj10eXBlb2YgaT09InN0cmluZyI/aTppLnNv"
    b"dXJjZTtyZXR1cm4gcj1yLnJlcGxhY2UobS5jYXJldCwiJDEiKSx0PXQucmVwbGFjZShzLHIpLG59"
    b"LGdldFJlZ2V4OigpPT5uZXcgUmVnRXhwKHQsZSl9O3JldHVybiBufXZhciBtPXtjb2RlUmVtb3Zl"
    b"SW5kZW50Oi9eKD86IHsxLDR9fCB7MCwzfVx0KS9nbSxvdXRwdXRMaW5rUmVwbGFjZTovXFwoW1xb"
    b"XF1dKS9nLGluZGVudENvZGVDb21wZW5zYXRpb246L14oXHMrKSg/OmBgYCkvLGJlZ2lubmluZ1Nw"
    b"YWNlOi9eXHMrLyxlbmRpbmdIYXNoOi8jJC8sc3RhcnRpbmdTcGFjZUNoYXI6L14gLyxlbmRpbmdT"
    b"cGFjZUNoYXI6LyAkLyxub25TcGFjZUNoYXI6L1teIF0vLG5ld0xpbmVDaGFyR2xvYmFsOi9cbi9n"
    b"LHRhYkNoYXJHbG9iYWw6L1x0L2csbXVsdGlwbGVTcGFjZUdsb2JhbDovXHMrL2csYmxhbmtMaW5l"
    b"Oi9eWyBcdF0qJC8sZG91YmxlQmxhbmtMaW5lOi9cblsgXHRdKlxuWyBcdF0qJC8sYmxvY2txdW90"
    b"ZVN0YXJ0Oi9eIHswLDN9Pi8sYmxvY2txdW90ZVNldGV4dFJlcGxhY2U6L1xuIHswLDN9KCg/Oj0r"
    b"fC0rKSAqKSg/PVxufCQpL2csYmxvY2txdW90ZVNldGV4dFJlcGxhY2UyOi9eIHswLDN9PlsgXHRd"
    b"Py9nbSxsaXN0UmVwbGFjZVRhYnM6L15cdCsvLGxpc3RSZXBsYWNlTmVzdGluZzovXiB7MSw0fSg/"
    b"PSggezR9KSpbXiBdKS9nLGxpc3RJc1Rhc2s6L15cW1sgeFhdXF0gLyxsaXN0UmVwbGFjZVRhc2s6"
    b"L15cW1sgeFhdXF0gKy8sYW55TGluZTovXG4uKlxuLyxocmVmQnJhY2tldHM6L148KC4qKT4kLyx0"
    b"YWJsZURlbGltaXRlcjovWzp8XS8sdGFibGVBbGlnbkNoYXJzOi9eXHx8XHwgKiQvZyx0YWJsZVJv"
    b"d0JsYW5rTGluZTovXG5bIFx0XSokLyx0YWJsZUFsaWduUmlnaHQ6L14gKi0rOiAqJC8sdGFibGVB"
    b"bGlnbkNlbnRlcjovXiAqOi0rOiAqJC8sdGFibGVBbGlnbkxlZnQ6L14gKjotKyAqJC8sc3RhcnRB"
    b"VGFnOi9ePGEgL2ksZW5kQVRhZzovXjxcL2E+L2ksc3RhcnRQcmVTY3JpcHRUYWc6L148KHByZXxj"
    b"b2RlfGtiZHxzY3JpcHQpKFxzfD4pL2ksZW5kUHJlU2NyaXB0VGFnOi9ePFwvKHByZXxjb2RlfGti"
    b"ZHxzY3JpcHQpKFxzfD4pL2ksc3RhcnRBbmdsZUJyYWNrZXQ6L148LyxlbmRBbmdsZUJyYWNrZXQ6"
    b"Lz4kLyxwZWRhbnRpY0hyZWZUaXRsZTovXihbXiciXSpbXlxzXSlccysoWyciXSkoLiopXDIvLHVu"
    b"aWNvZGVBbHBoYU51bWVyaWM6L1tccHtMfVxwe059XS91LGVzY2FwZVRlc3Q6L1smPD4iJ10vLGVz"
    b"Y2FwZVJlcGxhY2U6L1smPD4iJ10vZyxlc2NhcGVUZXN0Tm9FbmNvZGU6L1s8PiInXXwmKD8hKCNc"
    b"ZHsxLDd9fCNbWHhdW2EtZkEtRjAtOV17MSw2fXxcdyspOykvLGVzY2FwZVJlcGxhY2VOb0VuY29k"
    b"ZTovWzw+IiddfCYoPyEoI1xkezEsN318I1tYeF1bYS1mQS1GMC05XXsxLDZ9fFx3Kyk7KS9nLHVu"
    b"ZXNjYXBlVGVzdDovJigjKD86XGQrKXwoPzojeFswLTlBLUZhLWZdKyl8KD86XHcrKSk7Py9pZyxj"
    b"YXJldDovKF58W15cW10pXF4vZyxwZXJjZW50RGVjb2RlOi8lMjUvZyxmaW5kUGlwZTovXHwvZyxz"
    b"cGxpdFBpcGU6LyBcfC8sc2xhc2hQaXBlOi9cXFx8L2csY2FycmlhZ2VSZXR1cm46L1xyXG58XHIv"
    b"ZyxzcGFjZUxpbmU6L14gKyQvZ20sbm90U3BhY2VTdGFydDovXlxTKi8sZW5kaW5nTmV3bGluZTov"
    b"XG4kLyxsaXN0SXRlbVJlZ2V4Omw9Pm5ldyBSZWdFeHAoYF4oIHswLDN9JHtsfSkoKD86WwkgXVte"
    b"XFxuXSopPyg/OlxcbnwkKSlgKSxuZXh0QnVsbGV0UmVnZXg6bD0+bmV3IFJlZ0V4cChgXiB7MCwk"
    b"e01hdGgubWluKDMsbC0xKX19KD86WyorLV18XFxkezEsOX1bLildKSgoPzpbIAldW15cXG5dKik/"
    b"KD86XFxufCQpKWApLGhyUmVnZXg6bD0+bmV3IFJlZ0V4cChgXiB7MCwke01hdGgubWluKDMsbC0x"
    b"KX19KCg/Oi0gKil7Myx9fCg/Ol8gKil7Myx9fCg/OlxcKiAqKXszLH0pKD86XFxuK3wkKWApLGZl"
    b"bmNlc0JlZ2luUmVnZXg6bD0+bmV3IFJlZ0V4cChgXiB7MCwke01hdGgubWluKDMsbC0xKX19KD86"
    b"XGBcYFxgfH5+filgKSxoZWFkaW5nQmVnaW5SZWdleDpsPT5uZXcgUmVnRXhwKGBeIHswLCR7TWF0"
    b"aC5taW4oMyxsLTEpfX0jYCksaHRtbEJlZ2luUmVnZXg6bD0+bmV3IFJlZ0V4cChgXiB7MCwke01h"
    b"dGgubWluKDMsbC0xKX19PCg/OlthLXpdLio+fCEtLSlgLCJpIil9LCRlPS9eKD86WyBcdF0qKD86"
    b"XG58JCkpKy8sX2U9L14oKD86IHs0fXwgezAsM31cdClbXlxuXSsoPzpcbig/OlsgXHRdKig/Olxu"
    b"fCQpKSopPykrLyxMZT0vXiB7MCwzfShgezMsfSg/PVteYFxuXSooPzpcbnwkKSl8fnszLH0pKFte"
    b"XG5dKikoPzpcbnwkKSg/OnwoW1xzXFNdKj8pKD86XG58JCkpKD86IHswLDN9XDFbfmBdKiAqKD89"
    b"XG58JCl8JCkvLE89L14gezAsM30oKD86LVtcdCBdKil7Myx9fCg/Ol9bIFx0XSopezMsfXwoPzpc"
    b"KlsgXHRdKil7Myx9KSg/OlxuK3wkKS8semU9L14gezAsM30oI3sxLDZ9KSg/PVxzfCQpKC4qKSg/"
    b"OlxuK3wkKS8sRj0vKD86WyorLV18XGR7MSw5fVsuKV0pLyxpZT0vXig/IWJ1bGwgfGJsb2NrQ29k"
    b"ZXxmZW5jZXN8YmxvY2txdW90ZXxoZWFkaW5nfGh0bWx8dGFibGUpKCg/Oi58XG4oPyFccyo/XG58"
    b"YnVsbCB8YmxvY2tDb2RlfGZlbmNlc3xibG9ja3F1b3RlfGhlYWRpbmd8aHRtbHx0YWJsZSkpKz8p"
    b"XG4gezAsM30oPSt8LSspICooPzpcbit8JCkvLG9lPWgoaWUpLnJlcGxhY2UoL2J1bGwvZyxGKS5y"
    b"ZXBsYWNlKC9ibG9ja0NvZGUvZywvKD86IHs0fXwgezAsM31cdCkvKS5yZXBsYWNlKC9mZW5jZXMv"
    b"ZywvIHswLDN9KD86YHszLH18fnszLH0pLykucmVwbGFjZSgvYmxvY2txdW90ZS9nLC8gezAsM30+"
    b"LykucmVwbGFjZSgvaGVhZGluZy9nLC8gezAsM30jezEsNn0vKS5yZXBsYWNlKC9odG1sL2csLyB7"
    b"MCwzfTxbXlxuPl0rPlxuLykucmVwbGFjZSgvXHx0YWJsZS9nLCIiKS5nZXRSZWdleCgpLE1lPWgo"
    b"aWUpLnJlcGxhY2UoL2J1bGwvZyxGKS5yZXBsYWNlKC9ibG9ja0NvZGUvZywvKD86IHs0fXwgezAs"
    b"M31cdCkvKS5yZXBsYWNlKC9mZW5jZXMvZywvIHswLDN9KD86YHszLH18fnszLH0pLykucmVwbGFj"
    b"ZSgvYmxvY2txdW90ZS9nLC8gezAsM30+LykucmVwbGFjZSgvaGVhZGluZy9nLC8gezAsM30jezEs"
    b"Nn0vKS5yZXBsYWNlKC9odG1sL2csLyB7MCwzfTxbXlxuPl0rPlxuLykucmVwbGFjZSgvdGFibGUv"
    b"ZywvIHswLDN9XHw/KD86WzpcLSBdKlx8KStbXDpcLSBdKlxuLykuZ2V0UmVnZXgoKSxRPS9eKFte"
    b"XG5dKyg/OlxuKD8haHJ8aGVhZGluZ3xsaGVhZGluZ3xibG9ja3F1b3RlfGZlbmNlc3xsaXN0fGh0"
    b"bWx8dGFibGV8ICtcbilbXlxuXSspKikvLFBlPS9eW15cbl0rLyxVPS8oPyFccypcXSkoPzpcXC58"
    b"W15cW1xdXFxdKSsvLEFlPWgoL14gezAsM31cWyhsYWJlbClcXTogKig/OlxuWyBcdF0qKT8oW148"
    b"XHNdW15cc10qfDwuKj8+KSg/Oig/OiArKD86XG5bIFx0XSopP3wgKlxuWyBcdF0qKSh0aXRsZSkp"
    b"PyAqKD86XG4rfCQpLykucmVwbGFjZSgibGFiZWwiLFUpLnJlcGxhY2UoInRpdGxlIiwvKD86Iig/"
    b"OlxcIj98W14iXFxdKSoifCdbXidcbl0qKD86XG5bXidcbl0rKSpcbj8nfFwoW14oKV0qXCkpLyku"
    b"Z2V0UmVnZXgoKSxFZT1oKC9eKCB7MCwzfWJ1bGwpKFsgXHRdW15cbl0rPyk/KD86XG58JCkvKS5y"
    b"ZXBsYWNlKC9idWxsL2csRikuZ2V0UmVnZXgoKSx2PSJhZGRyZXNzfGFydGljbGV8YXNpZGV8YmFz"
    b"ZXxiYXNlZm9udHxibG9ja3F1b3RlfGJvZHl8Y2FwdGlvbnxjZW50ZXJ8Y29sfGNvbGdyb3VwfGRk"
    b"fGRldGFpbHN8ZGlhbG9nfGRpcnxkaXZ8ZGx8ZHR8ZmllbGRzZXR8ZmlnY2FwdGlvbnxmaWd1cmV8"
    b"Zm9vdGVyfGZvcm18ZnJhbWV8ZnJhbWVzZXR8aFsxLTZdfGhlYWR8aGVhZGVyfGhyfGh0bWx8aWZy"
    b"YW1lfGxlZ2VuZHxsaXxsaW5rfG1haW58bWVudXxtZW51aXRlbXxtZXRhfG5hdnxub2ZyYW1lc3xv"
    b"bHxvcHRncm91cHxvcHRpb258cHxwYXJhbXxzZWFyY2h8c2VjdGlvbnxzdW1tYXJ5fHRhYmxlfHRi"
    b"b2R5fHRkfHRmb290fHRofHRoZWFkfHRpdGxlfHRyfHRyYWNrfHVsIixLPS88IS0tKD86LT8+fFtc"
    b"c1xTXSo/KD86LS0+fCQpKS8sQ2U9aCgiXiB7MCwzfSg/Ojwoc2NyaXB0fHByZXxzdHlsZXx0ZXh0"
    b"YXJlYSlbXFxzPl1bXFxzXFxTXSo/KD86PC9cXDE+W15cXG5dKlxcbit8JCl8Y29tbWVudFteXFxu"
    b"XSooXFxuK3wkKXw8XFw/W1xcc1xcU10qPyg/OlxcPz5cXG4qfCQpfDwhW0EtWl1bXFxzXFxTXSo/"
    b"KD86Plxcbip8JCl8PCFcXFtDREFUQVxcW1tcXHNcXFNdKj8oPzpcXF1cXF0+XFxuKnwkKXw8Lz8o"
    b"dGFnKSg/OiArfFxcbnwvPz4pW1xcc1xcU10qPyg/Oig/OlxcblsgCV0qKStcXG58JCl8PCg/IXNj"
    b"cmlwdHxwcmV8c3R5bGV8dGV4dGFyZWEpKFthLXpdW1xcdy1dKikoPzphdHRyaWJ1dGUpKj8gKi8/"
    b"Pig/PVsgXFx0XSooPzpcXG58JCkpW1xcc1xcU10qPyg/Oig/OlxcblsgCV0qKStcXG58JCl8PC8o"
    b"PyFzY3JpcHR8cHJlfHN0eWxlfHRleHRhcmVhKVthLXpdW1xcdy1dKlxccyo+KD89WyBcXHRdKig/"
    b"OlxcbnwkKSlbXFxzXFxTXSo/KD86KD86XFxuWyAJXSopK1xcbnwkKSkiLCJpIikucmVwbGFjZSgi"
    b"Y29tbWVudCIsSykucmVwbGFjZSgidGFnIix2KS5yZXBsYWNlKCJhdHRyaWJ1dGUiLC8gK1thLXpB"
    b"LVo6X11bXHcuOi1dKig/OiAqPSAqIlteIlxuXSoifCAqPSAqJ1teJ1xuXSonfCAqPSAqW15ccyIn"
    b"PTw+YF0rKT8vKS5nZXRSZWdleCgpLGxlPWgoUSkucmVwbGFjZSgiaHIiLE8pLnJlcGxhY2UoImhl"
    b"YWRpbmciLCIgezAsM30jezEsNn0oPzpcXHN8JCkiKS5yZXBsYWNlKCJ8bGhlYWRpbmciLCIiKS5y"
    b"ZXBsYWNlKCJ8dGFibGUiLCIiKS5yZXBsYWNlKCJibG9ja3F1b3RlIiwiIHswLDN9PiIpLnJlcGxh"
    b"Y2UoImZlbmNlcyIsIiB7MCwzfSg/OmB7Myx9KD89W15gXFxuXSpcXG4pfH57Myx9KVteXFxuXSpc"
    b"XG4iKS5yZXBsYWNlKCJsaXN0IiwiIHswLDN9KD86WyorLV18MVsuKV0pICIpLnJlcGxhY2UoImh0"
    b"bWwiLCI8Lz8oPzp0YWcpKD86ICt8XFxufC8/Pil8PCg/OnNjcmlwdHxwcmV8c3R5bGV8dGV4dGFy"
    b"ZWF8IS0tKSIpLnJlcGxhY2UoInRhZyIsdikuZ2V0UmVnZXgoKSxJZT1oKC9eKCB7MCwzfT4gPyhw"
    b"YXJhZ3JhcGh8W15cbl0qKSg/OlxufCQpKSsvKS5yZXBsYWNlKCJwYXJhZ3JhcGgiLGxlKS5nZXRS"
    b"ZWdleCgpLFg9e2Jsb2NrcXVvdGU6SWUsY29kZTpfZSxkZWY6QWUsZmVuY2VzOkxlLGhlYWRpbmc6"
    b"emUsaHI6TyxodG1sOkNlLGxoZWFkaW5nOm9lLGxpc3Q6RWUsbmV3bGluZTokZSxwYXJhZ3JhcGg6"
    b"bGUsdGFibGU6SSx0ZXh0OlBlfSxyZT1oKCJeICooW15cXG4gXS4qKVxcbiB7MCwzfSgoPzpcXHwg"
    b"Kik/Oj8tKzo/ICooPzpcXHwgKjo/LSs6PyAqKSooPzpcXHwgKik/KSg/OlxcbigoPzooPyEgKlxc"
    b"bnxocnxoZWFkaW5nfGJsb2NrcXVvdGV8Y29kZXxmZW5jZXN8bGlzdHxodG1sKS4qKD86XFxufCQp"
    b"KSopXFxuKnwkKSIpLnJlcGxhY2UoImhyIixPKS5yZXBsYWNlKCJoZWFkaW5nIiwiIHswLDN9I3sx"
    b"LDZ9KD86XFxzfCQpIikucmVwbGFjZSgiYmxvY2txdW90ZSIsIiB7MCwzfT4iKS5yZXBsYWNlKCJj"
    b"b2RlIiwiKD86IHs0fXwgezAsM30JKVteXFxuXSIpLnJlcGxhY2UoImZlbmNlcyIsIiB7MCwzfSg/"
    b"OmB7Myx9KD89W15gXFxuXSpcXG4pfH57Myx9KVteXFxuXSpcXG4iKS5yZXBsYWNlKCJsaXN0Iiwi"
    b"IHswLDN9KD86WyorLV18MVsuKV0pICIpLnJlcGxhY2UoImh0bWwiLCI8Lz8oPzp0YWcpKD86ICt8"
    b"XFxufC8/Pil8PCg/OnNjcmlwdHxwcmV8c3R5bGV8dGV4dGFyZWF8IS0tKSIpLnJlcGxhY2UoInRh"
    b"ZyIsdikuZ2V0UmVnZXgoKSxPZT17Li4uWCxsaGVhZGluZzpNZSx0YWJsZTpyZSxwYXJhZ3JhcGg6"
    b"aChRKS5yZXBsYWNlKCJociIsTykucmVwbGFjZSgiaGVhZGluZyIsIiB7MCwzfSN7MSw2fSg/Olxc"
    b"c3wkKSIpLnJlcGxhY2UoInxsaGVhZGluZyIsIiIpLnJlcGxhY2UoInRhYmxlIixyZSkucmVwbGFj"
    b"ZSgiYmxvY2txdW90ZSIsIiB7MCwzfT4iKS5yZXBsYWNlKCJmZW5jZXMiLCIgezAsM30oPzpgezMs"
    b"fSg/PVteYFxcbl0qXFxuKXx+ezMsfSlbXlxcbl0qXFxuIikucmVwbGFjZSgibGlzdCIsIiB7MCwz"
    b"fSg/OlsqKy1dfDFbLildKSAiKS5yZXBsYWNlKCJodG1sIiwiPC8/KD86dGFnKSg/OiArfFxcbnwv"
    b"Pz4pfDwoPzpzY3JpcHR8cHJlfHN0eWxlfHRleHRhcmVhfCEtLSkiKS5yZXBsYWNlKCJ0YWciLHYp"
    b"LmdldFJlZ2V4KCl9LEJlPXsuLi5YLGh0bWw6aChgXiAqKD86Y29tbWVudCAqKD86XFxufFxccyok"
    b"KXw8KHRhZylbXFxzXFxTXSs/PC9cXDE+ICooPzpcXG57Mix9fFxccyokKXw8dGFnKD86IlteIl0q"
    b"InwnW14nXSonfFxcc1teJyIvPlxcc10qKSo/Lz8+ICooPzpcXG57Mix9fFxccyokKSlgKS5yZXBs"
    b"YWNlKCJjb21tZW50IixLKS5yZXBsYWNlKC90YWcvZywiKD8hKD86YXxlbXxzdHJvbmd8c21hbGx8"
    b"c3xjaXRlfHF8ZGZufGFiYnJ8ZGF0YXx0aW1lfGNvZGV8dmFyfHNhbXB8a2JkfHN1YnxzdXB8aXxi"
    b"fHV8bWFya3xydWJ5fHJ0fHJwfGJkaXxiZG98c3Bhbnxicnx3YnJ8aW5zfGRlbHxpbWcpXFxiKVxc"
    b"dysoPyE6fFteXFx3XFxzQF0qQClcXGIiKS5nZXRSZWdleCgpLGRlZjovXiAqXFsoW15cXV0rKVxd"
    b"OiAqPD8oW15ccz5dKyk+Pyg/OiArKFsiKF1bXlxuXStbIildKSk/ICooPzpcbit8JCkvLGhlYWRp"
    b"bmc6L14oI3sxLDZ9KSguKikoPzpcbit8JCkvLGZlbmNlczpJLGxoZWFkaW5nOi9eKC4rPylcbiB7"
    b"MCwzfSg9K3wtKykgKig/OlxuK3wkKS8scGFyYWdyYXBoOmgoUSkucmVwbGFjZSgiaHIiLE8pLnJl"
    b"cGxhY2UoImhlYWRpbmciLGAgKiN7MSw2fSAqW14KXWApLnJlcGxhY2UoImxoZWFkaW5nIixvZSku"
    b"cmVwbGFjZSgifHRhYmxlIiwiIikucmVwbGFjZSgiYmxvY2txdW90ZSIsIiB7MCwzfT4iKS5yZXBs"
    b"YWNlKCJ8ZmVuY2VzIiwiIikucmVwbGFjZSgifGxpc3QiLCIiKS5yZXBsYWNlKCJ8aHRtbCIsIiIp"
    b"LnJlcGxhY2UoInx0YWciLCIiKS5nZXRSZWdleCgpfSxxZT0vXlxcKFshIiMkJSYnKCkqKyxcLS4v"
    b"Ojs8PT4/QFxbXF1cXF5fYHt8fX5dKS8sdmU9L14oYCspKFteYF18W15gXVtcc1xTXSo/W15gXSlc"
    b"MSg/IWApLyxhZT0vXiggezIsfXxcXClcbig/IVxzKiQpLyxEZT0vXihgK3xbXmBdKSg/Oig/PSB7"
    b"Mix9XG4pfFtcc1xTXSo/KD86KD89W1xcPCFcW2AqX118XGJffCQpfFteIF0oPz0gezIsfVxuKSkp"
    b"LyxEPS9bXHB7UH1ccHtTfV0vdSxXPS9bXHNccHtQfVxwe1N9XS91LGNlPS9bXlxzXHB7UH1ccHtT"
    b"fV0vdSxaZT1oKC9eKCg/IVsqX10pcHVuY3RTcGFjZSkvLCJ1IikucmVwbGFjZSgvcHVuY3RTcGFj"
    b"ZS9nLFcpLmdldFJlZ2V4KCkscGU9Lyg/IX4pW1xwe1B9XHB7U31dL3UsR2U9Lyg/IX4pW1xzXHB7"
    b"UH1ccHtTfV0vdSxIZT0vKD86W15cc1xwe1B9XHB7U31dfH4pL3UsTmU9L1xbW15bXF1dKj9cXVwo"
    b"KD86XFwufFteXFxcKFwpXXxcKCg/OlxcLnxbXlxcXChcKV0pKlwpKSpcKXxgW15gXSo/YHw8W148"
    b"Pl0qPz4vZyx1ZT0vXig/OlwqKyg/OigoPyFcKilwdW5jdCl8W15ccypdKSl8Xl8rKD86KCg/IV8p"
    b"cHVuY3QpfChbXlxzX10pKS8samU9aCh1ZSwidSIpLnJlcGxhY2UoL3B1bmN0L2csRCkuZ2V0UmVn"
    b"ZXgoKSxGZT1oKHVlLCJ1IikucmVwbGFjZSgvcHVuY3QvZyxwZSkuZ2V0UmVnZXgoKSxoZT0iXlte"
    b"XypdKj9fX1teXypdKj9cXCpbXl8qXSo/KD89X18pfFteKl0rKD89W14qXSl8KD8hXFwqKXB1bmN0"
    b"KFxcKispKD89W1xcc118JCl8bm90UHVuY3RTcGFjZShcXCorKSg/IVxcKikoPz1wdW5jdFNwYWNl"
    b"fCQpfCg/IVxcKilwdW5jdFNwYWNlKFxcKispKD89bm90UHVuY3RTcGFjZSl8W1xcc10oXFwqKyko"
    b"PyFcXCopKD89cHVuY3QpfCg/IVxcKilwdW5jdChcXCorKSg/IVxcKikoPz1wdW5jdCl8bm90UHVu"
    b"Y3RTcGFjZShcXCorKSg/PW5vdFB1bmN0U3BhY2UpIixRZT1oKGhlLCJndSIpLnJlcGxhY2UoL25v"
    b"dFB1bmN0U3BhY2UvZyxjZSkucmVwbGFjZSgvcHVuY3RTcGFjZS9nLFcpLnJlcGxhY2UoL3B1bmN0"
    b"L2csRCkuZ2V0UmVnZXgoKSxVZT1oKGhlLCJndSIpLnJlcGxhY2UoL25vdFB1bmN0U3BhY2UvZyxI"
    b"ZSkucmVwbGFjZSgvcHVuY3RTcGFjZS9nLEdlKS5yZXBsYWNlKC9wdW5jdC9nLHBlKS5nZXRSZWdl"
    b"eCgpLEtlPWgoIl5bXl8qXSo/XFwqXFwqW15fKl0qP19bXl8qXSo/KD89XFwqXFwqKXxbXl9dKyg/"
    b"PVteX10pfCg/IV8pcHVuY3QoXyspKD89W1xcc118JCl8bm90UHVuY3RTcGFjZShfKykoPyFfKSg/"
    b"PXB1bmN0U3BhY2V8JCl8KD8hXylwdW5jdFNwYWNlKF8rKSg/PW5vdFB1bmN0U3BhY2UpfFtcXHNd"
    b"KF8rKSg/IV8pKD89cHVuY3QpfCg/IV8pcHVuY3QoXyspKD8hXykoPz1wdW5jdCkiLCJndSIpLnJl"
    b"cGxhY2UoL25vdFB1bmN0U3BhY2UvZyxjZSkucmVwbGFjZSgvcHVuY3RTcGFjZS9nLFcpLnJlcGxh"
    b"Y2UoL3B1bmN0L2csRCkuZ2V0UmVnZXgoKSxYZT1oKC9cXChwdW5jdCkvLCJndSIpLnJlcGxhY2Uo"
    b"L3B1bmN0L2csRCkuZ2V0UmVnZXgoKSxXZT1oKC9ePChzY2hlbWU6W15cc1x4MDAtXHgxZjw+XSp8"
    b"ZW1haWwpPi8pLnJlcGxhY2UoInNjaGVtZSIsL1thLXpBLVpdW2EtekEtWjAtOSsuLV17MSwzMX0v"
    b"KS5yZXBsYWNlKCJlbWFpbCIsL1thLXpBLVowLTkuISMkJSYnKisvPT9eX2B7fH1+LV0rKEApW2Et"
    b"ekEtWjAtOV0oPzpbYS16QS1aMC05LV17MCw2MX1bYS16QS1aMC05XSk/KD86XC5bYS16QS1aMC05"
    b"XSg/OlthLXpBLVowLTktXXswLDYxfVthLXpBLVowLTldKT8pKyg/IVstX10pLykuZ2V0UmVnZXgo"
    b"KSxKZT1oKEspLnJlcGxhY2UoIig/Oi0tPnwkKSIsIi0tPiIpLmdldFJlZ2V4KCksVmU9aCgiXmNv"
    b"bW1lbnR8XjwvW2EtekEtWl1bXFx3Oi1dKlxccyo+fF48W2EtekEtWl1bXFx3LV0qKD86YXR0cmli"
    b"dXRlKSo/XFxzKi8/PnxePFxcP1tcXHNcXFNdKj9cXD8+fF48IVthLXpBLVpdK1xcc1tcXHNcXFNd"
    b"Kj8+fF48IVxcW0NEQVRBXFxbW1xcc1xcU10qP1xcXVxcXT4iKS5yZXBsYWNlKCJjb21tZW50IixK"
    b"ZSkucmVwbGFjZSgiYXR0cmlidXRlIiwvXHMrW2EtekEtWjpfXVtcdy46LV0qKD86XHMqPVxzKiJb"
    b"XiJdKiJ8XHMqPVxzKidbXiddKid8XHMqPVxzKlteXHMiJz08PmBdKyk/LykuZ2V0UmVnZXgoKSxx"
    b"PS8oPzpcWyg/OlxcLnxbXlxbXF1cXF0pKlxdfFxcLnxgW15gXSpgfFteXFtcXVxcYF0pKj8vLFll"
    b"PWgoL14hP1xbKGxhYmVsKVxdXChccyooaHJlZikoPzooPzpbIFx0XSooPzpcblsgXHRdKik/KSh0"
    b"aXRsZSkpP1xzKlwpLykucmVwbGFjZSgibGFiZWwiLHEpLnJlcGxhY2UoImhyZWYiLC88KD86XFwu"
    b"fFteXG48PlxcXSkrPnxbXiBcdFxuXHgwMC1ceDFmXSovKS5yZXBsYWNlKCJ0aXRsZSIsLyIoPzpc"
    b"XCI/fFteIlxcXSkqInwnKD86XFwnP3xbXidcXF0pKid8XCgoPzpcXFwpP3xbXilcXF0pKlwpLyku"
    b"Z2V0UmVnZXgoKSxrZT1oKC9eIT9cWyhsYWJlbClcXVxbKHJlZilcXS8pLnJlcGxhY2UoImxhYmVs"
    b"IixxKS5yZXBsYWNlKCJyZWYiLFUpLmdldFJlZ2V4KCksZ2U9aCgvXiE/XFsocmVmKVxdKD86XFtc"
    b"XSk/LykucmVwbGFjZSgicmVmIixVKS5nZXRSZWdleCgpLGV0PWgoInJlZmxpbmt8bm9saW5rKD8h"
    b"XFwoKSIsImciKS5yZXBsYWNlKCJyZWZsaW5rIixrZSkucmVwbGFjZSgibm9saW5rIixnZSkuZ2V0"
    b"UmVnZXgoKSxKPXtfYmFja3BlZGFsOkksYW55UHVuY3R1YXRpb246WGUsYXV0b2xpbms6V2UsYmxv"
    b"Y2tTa2lwOk5lLGJyOmFlLGNvZGU6dmUsZGVsOkksZW1TdHJvbmdMRGVsaW06amUsZW1TdHJvbmdS"
    b"RGVsaW1Bc3Q6UWUsZW1TdHJvbmdSRGVsaW1VbmQ6S2UsZXNjYXBlOnFlLGxpbms6WWUsbm9saW5r"
    b"OmdlLHB1bmN0dWF0aW9uOlplLHJlZmxpbms6a2UscmVmbGlua1NlYXJjaDpldCx0YWc6VmUsdGV4"
    b"dDpEZSx1cmw6SX0sdHQ9ey4uLkosbGluazpoKC9eIT9cWyhsYWJlbClcXVwoKC4qPylcKS8pLnJl"
    b"cGxhY2UoImxhYmVsIixxKS5nZXRSZWdleCgpLHJlZmxpbms6aCgvXiE/XFsobGFiZWwpXF1ccypc"
    b"WyhbXlxdXSopXF0vKS5yZXBsYWNlKCJsYWJlbCIscSkuZ2V0UmVnZXgoKX0saj17Li4uSixlbVN0"
    b"cm9uZ1JEZWxpbUFzdDpVZSxlbVN0cm9uZ0xEZWxpbTpGZSx1cmw6aCgvXigoPzpmdHB8aHR0cHM/"
    b"KTpcL1wvfHd3d1wuKSg/OlthLXpBLVowLTlcLV0rXC4/KStbXlxzPF0qfF5lbWFpbC8sImkiKS5y"
    b"ZXBsYWNlKCJlbWFpbCIsL1tBLVphLXowLTkuXystXSsoQClbYS16QS1aMC05LV9dKyg/OlwuW2Et"
    b"ekEtWjAtOS1fXSpbYS16QS1aMC05XSkrKD8hWy1fXSkvKS5nZXRSZWdleCgpLF9iYWNrcGVkYWw6"
    b"Lyg/OltePyEuLDo7Kl8nIn4oKSZdK3xcKFteKV0qXCl8Jig/IVthLXpBLVowLTldKzskKXxbPyEu"
    b"LDo7Kl8nIn4pXSsoPyEkKSkrLyxkZWw6L14ofn4/KSg/PVteXHN+XSkoKD86XFwufFteXFxdKSo/"
    b"KD86XFwufFteXHN+XFxdKSlcMSg/PVtefl18JCkvLHRleHQ6L14oW2B+XSt8W15gfl0pKD86KD89"
    b"IHsyLH1cbil8KD89W2EtekEtWjAtOS4hIyQlJicqK1wvPT9fYHtcfH1+LV0rQCl8W1xzXFNdKj8o"
    b"PzooPz1bXFw8IVxbYCp+X118XGJffGh0dHBzPzpcL1wvfGZ0cDpcL1wvfHd3d1wufCQpfFteIF0o"
    b"Pz0gezIsfVxuKXxbXmEtekEtWjAtOS4hIyQlJicqK1wvPT9fYHtcfH1+LV0oPz1bYS16QS1aMC05"
    b"LiEjJCUmJyorXC89P19ge1x8fX4tXStAKSkpL30sbnQ9ey4uLmosYnI6aChhZSkucmVwbGFjZSgi"
    b"ezIsfSIsIioiKS5nZXRSZWdleCgpLHRleHQ6aChqLnRleHQpLnJlcGxhY2UoIlxcYl8iLCJcXGJf"
    b"fCB7Mix9XFxuIikucmVwbGFjZSgvXHsyLFx9L2csIioiKS5nZXRSZWdleCgpfSxCPXtub3JtYWw6"
    b"WCxnZm06T2UscGVkYW50aWM6QmV9LFA9e25vcm1hbDpKLGdmbTpqLGJyZWFrczpudCxwZWRhbnRp"
    b"Yzp0dH07dmFyIHN0PXsiJiI6IiZhbXA7IiwiPCI6IiZsdDsiLCI+IjoiJmd0OyIsJyInOiImcXVv"
    b"dDsiLCInIjoiJiMzOTsifSxmZT1sPT5zdFtsXTtmdW5jdGlvbiBSKGwsZSl7aWYoZSl7aWYobS5l"
    b"c2NhcGVUZXN0LnRlc3QobCkpcmV0dXJuIGwucmVwbGFjZShtLmVzY2FwZVJlcGxhY2UsZmUpfWVs"
    b"c2UgaWYobS5lc2NhcGVUZXN0Tm9FbmNvZGUudGVzdChsKSlyZXR1cm4gbC5yZXBsYWNlKG0uZXNj"
    b"YXBlUmVwbGFjZU5vRW5jb2RlLGZlKTtyZXR1cm4gbH1mdW5jdGlvbiBWKGwpe3RyeXtsPWVuY29k"
    b"ZVVSSShsKS5yZXBsYWNlKG0ucGVyY2VudERlY29kZSwiJSIpfWNhdGNoe3JldHVybiBudWxsfXJl"
    b"dHVybiBsfWZ1bmN0aW9uIFkobCxlKXtsZXQgdD1sLnJlcGxhY2UobS5maW5kUGlwZSwoaSxyLG8p"
    b"PT57bGV0IGE9ITEsYz1yO2Zvcig7LS1jPj0wJiZvW2NdPT09IlxcIjspYT0hYTtyZXR1cm4gYT8i"
    b"fCI6IiB8In0pLG49dC5zcGxpdChtLnNwbGl0UGlwZSkscz0wO2lmKG5bMF0udHJpbSgpfHxuLnNo"
    b"aWZ0KCksbi5sZW5ndGg+MCYmIW4uYXQoLTEpPy50cmltKCkmJm4ucG9wKCksZSlpZihuLmxlbmd0"
    b"aD5lKW4uc3BsaWNlKGUpO2Vsc2UgZm9yKDtuLmxlbmd0aDxlOyluLnB1c2goIiIpO2Zvcig7czxu"
    b"Lmxlbmd0aDtzKyspbltzXT1uW3NdLnRyaW0oKS5yZXBsYWNlKG0uc2xhc2hQaXBlLCJ8Iik7cmV0"
    b"dXJuIG59ZnVuY3Rpb24gQShsLGUsdCl7bGV0IG49bC5sZW5ndGg7aWYobj09PTApcmV0dXJuIiI7"
    b"bGV0IHM9MDtmb3IoO3M8bjspe2xldCBpPWwuY2hhckF0KG4tcy0xKTtpZihpPT09ZSYmIXQpcysr"
    b"O2Vsc2UgaWYoaSE9PWUmJnQpcysrO2Vsc2UgYnJlYWt9cmV0dXJuIGwuc2xpY2UoMCxuLXMpfWZ1"
    b"bmN0aW9uIGRlKGwsZSl7aWYobC5pbmRleE9mKGVbMV0pPT09LTEpcmV0dXJuLTE7bGV0IHQ9MDtm"
    b"b3IobGV0IG49MDtuPGwubGVuZ3RoO24rKylpZihsW25dPT09IlxcIiluKys7ZWxzZSBpZihsW25d"
    b"PT09ZVswXSl0Kys7ZWxzZSBpZihsW25dPT09ZVsxXSYmKHQtLSx0PDApKXJldHVybiBuO3JldHVy"
    b"biB0PjA/LTI6LTF9ZnVuY3Rpb24gbWUobCxlLHQsbixzKXtsZXQgaT1lLmhyZWYscj1lLnRpdGxl"
    b"fHxudWxsLG89bFsxXS5yZXBsYWNlKHMub3RoZXIub3V0cHV0TGlua1JlcGxhY2UsIiQxIik7bi5z"
    b"dGF0ZS5pbkxpbms9ITA7bGV0IGE9e3R5cGU6bFswXS5jaGFyQXQoMCk9PT0iISI/ImltYWdlIjoi"
    b"bGluayIscmF3OnQsaHJlZjppLHRpdGxlOnIsdGV4dDpvLHRva2VuczpuLmlubGluZVRva2Vucyhv"
    b"KX07cmV0dXJuIG4uc3RhdGUuaW5MaW5rPSExLGF9ZnVuY3Rpb24gcnQobCxlLHQpe2xldCBuPWwu"
    b"bWF0Y2godC5vdGhlci5pbmRlbnRDb2RlQ29tcGVuc2F0aW9uKTtpZihuPT09bnVsbClyZXR1cm4g"
    b"ZTtsZXQgcz1uWzFdO3JldHVybiBlLnNwbGl0KGAKYCkubWFwKGk9PntsZXQgcj1pLm1hdGNoKHQu"
    b"b3RoZXIuYmVnaW5uaW5nU3BhY2UpO2lmKHI9PT1udWxsKXJldHVybiBpO2xldFtvXT1yO3JldHVy"
    b"biBvLmxlbmd0aD49cy5sZW5ndGg/aS5zbGljZShzLmxlbmd0aCk6aX0pLmpvaW4oYApgKX12YXIg"
    b"Uz1jbGFzc3tvcHRpb25zO3J1bGVzO2xleGVyO2NvbnN0cnVjdG9yKGUpe3RoaXMub3B0aW9ucz1l"
    b"fHx3fXNwYWNlKGUpe2xldCB0PXRoaXMucnVsZXMuYmxvY2submV3bGluZS5leGVjKGUpO2lmKHQm"
    b"JnRbMF0ubGVuZ3RoPjApcmV0dXJue3R5cGU6InNwYWNlIixyYXc6dFswXX19Y29kZShlKXtsZXQg"
    b"dD10aGlzLnJ1bGVzLmJsb2NrLmNvZGUuZXhlYyhlKTtpZih0KXtsZXQgbj10WzBdLnJlcGxhY2Uo"
    b"dGhpcy5ydWxlcy5vdGhlci5jb2RlUmVtb3ZlSW5kZW50LCIiKTtyZXR1cm57dHlwZToiY29kZSIs"
    b"cmF3OnRbMF0sY29kZUJsb2NrU3R5bGU6ImluZGVudGVkIix0ZXh0OnRoaXMub3B0aW9ucy5wZWRh"
    b"bnRpYz9uOkEobixgCmApfX19ZmVuY2VzKGUpe2xldCB0PXRoaXMucnVsZXMuYmxvY2suZmVuY2Vz"
    b"LmV4ZWMoZSk7aWYodCl7bGV0IG49dFswXSxzPXJ0KG4sdFszXXx8IiIsdGhpcy5ydWxlcyk7cmV0"
    b"dXJue3R5cGU6ImNvZGUiLHJhdzpuLGxhbmc6dFsyXT90WzJdLnRyaW0oKS5yZXBsYWNlKHRoaXMu"
    b"cnVsZXMuaW5saW5lLmFueVB1bmN0dWF0aW9uLCIkMSIpOnRbMl0sdGV4dDpzfX19aGVhZGluZyhl"
    b"KXtsZXQgdD10aGlzLnJ1bGVzLmJsb2NrLmhlYWRpbmcuZXhlYyhlKTtpZih0KXtsZXQgbj10WzJd"
    b"LnRyaW0oKTtpZih0aGlzLnJ1bGVzLm90aGVyLmVuZGluZ0hhc2gudGVzdChuKSl7bGV0IHM9QShu"
    b"LCIjIik7KHRoaXMub3B0aW9ucy5wZWRhbnRpY3x8IXN8fHRoaXMucnVsZXMub3RoZXIuZW5kaW5n"
    b"U3BhY2VDaGFyLnRlc3QocykpJiYobj1zLnRyaW0oKSl9cmV0dXJue3R5cGU6ImhlYWRpbmciLHJh"
    b"dzp0WzBdLGRlcHRoOnRbMV0ubGVuZ3RoLHRleHQ6bix0b2tlbnM6dGhpcy5sZXhlci5pbmxpbmUo"
    b"bil9fX1ocihlKXtsZXQgdD10aGlzLnJ1bGVzLmJsb2NrLmhyLmV4ZWMoZSk7aWYodClyZXR1cm57"
    b"dHlwZToiaHIiLHJhdzpBKHRbMF0sYApgKX19YmxvY2txdW90ZShlKXtsZXQgdD10aGlzLnJ1bGVz"
    b"LmJsb2NrLmJsb2NrcXVvdGUuZXhlYyhlKTtpZih0KXtsZXQgbj1BKHRbMF0sYApgKS5zcGxpdChg"
    b"CmApLHM9IiIsaT0iIixyPVtdO2Zvcig7bi5sZW5ndGg+MDspe2xldCBvPSExLGE9W10sYztmb3Io"
    b"Yz0wO2M8bi5sZW5ndGg7YysrKWlmKHRoaXMucnVsZXMub3RoZXIuYmxvY2txdW90ZVN0YXJ0LnRl"
    b"c3QobltjXSkpYS5wdXNoKG5bY10pLG89ITA7ZWxzZSBpZighbylhLnB1c2gobltjXSk7ZWxzZSBi"
    b"cmVhaztuPW4uc2xpY2UoYyk7bGV0IHA9YS5qb2luKGAKYCksdT1wLnJlcGxhY2UodGhpcy5ydWxl"
    b"cy5vdGhlci5ibG9ja3F1b3RlU2V0ZXh0UmVwbGFjZSxgCiAgICAkMWApLnJlcGxhY2UodGhpcy5y"
    b"dWxlcy5vdGhlci5ibG9ja3F1b3RlU2V0ZXh0UmVwbGFjZTIsIiIpO3M9cz9gJHtzfQoke3B9YDpw"
    b"LGk9aT9gJHtpfQoke3V9YDp1O2xldCBkPXRoaXMubGV4ZXIuc3RhdGUudG9wO2lmKHRoaXMubGV4"
    b"ZXIuc3RhdGUudG9wPSEwLHRoaXMubGV4ZXIuYmxvY2tUb2tlbnModSxyLCEwKSx0aGlzLmxleGVy"
    b"LnN0YXRlLnRvcD1kLG4ubGVuZ3RoPT09MClicmVhaztsZXQgZz1yLmF0KC0xKTtpZihnPy50eXBl"
    b"PT09ImNvZGUiKWJyZWFrO2lmKGc/LnR5cGU9PT0iYmxvY2txdW90ZSIpe2xldCBUPWcsZj1ULnJh"
    b"dytgCmArbi5qb2luKGAKYCkseT10aGlzLmJsb2NrcXVvdGUoZik7cltyLmxlbmd0aC0xXT15LHM9"
    b"cy5zdWJzdHJpbmcoMCxzLmxlbmd0aC1ULnJhdy5sZW5ndGgpK3kucmF3LGk9aS5zdWJzdHJpbmco"
    b"MCxpLmxlbmd0aC1ULnRleHQubGVuZ3RoKSt5LnRleHQ7YnJlYWt9ZWxzZSBpZihnPy50eXBlPT09"
    b"Imxpc3QiKXtsZXQgVD1nLGY9VC5yYXcrYApgK24uam9pbihgCmApLHk9dGhpcy5saXN0KGYpO3Jb"
    b"ci5sZW5ndGgtMV09eSxzPXMuc3Vic3RyaW5nKDAscy5sZW5ndGgtZy5yYXcubGVuZ3RoKSt5LnJh"
    b"dyxpPWkuc3Vic3RyaW5nKDAsaS5sZW5ndGgtVC5yYXcubGVuZ3RoKSt5LnJhdyxuPWYuc3Vic3Ry"
    b"aW5nKHIuYXQoLTEpLnJhdy5sZW5ndGgpLnNwbGl0KGAKYCk7Y29udGludWV9fXJldHVybnt0eXBl"
    b"OiJibG9ja3F1b3RlIixyYXc6cyx0b2tlbnM6cix0ZXh0Oml9fX1saXN0KGUpe2xldCB0PXRoaXMu"
    b"cnVsZXMuYmxvY2subGlzdC5leGVjKGUpO2lmKHQpe2xldCBuPXRbMV0udHJpbSgpLHM9bi5sZW5n"
    b"dGg+MSxpPXt0eXBlOiJsaXN0IixyYXc6IiIsb3JkZXJlZDpzLHN0YXJ0OnM/K24uc2xpY2UoMCwt"
    b"MSk6IiIsbG9vc2U6ITEsaXRlbXM6W119O249cz9gXFxkezEsOX1cXCR7bi5zbGljZSgtMSl9YDpg"
    b"XFwke259YCx0aGlzLm9wdGlvbnMucGVkYW50aWMmJihuPXM/bjoiWyorLV0iKTtsZXQgcj10aGlz"
    b"LnJ1bGVzLm90aGVyLmxpc3RJdGVtUmVnZXgobiksbz0hMTtmb3IoO2U7KXtsZXQgYz0hMSxwPSIi"
    b"LHU9IiI7aWYoISh0PXIuZXhlYyhlKSl8fHRoaXMucnVsZXMuYmxvY2suaHIudGVzdChlKSlicmVh"
    b"aztwPXRbMF0sZT1lLnN1YnN0cmluZyhwLmxlbmd0aCk7bGV0IGQ9dFsyXS5zcGxpdChgCmAsMSlb"
    b"MF0ucmVwbGFjZSh0aGlzLnJ1bGVzLm90aGVyLmxpc3RSZXBsYWNlVGFicyxaPT4iICIucmVwZWF0"
    b"KDMqWi5sZW5ndGgpKSxnPWUuc3BsaXQoYApgLDEpWzBdLFQ9IWQudHJpbSgpLGY9MDtpZih0aGlz"
    b"Lm9wdGlvbnMucGVkYW50aWM/KGY9Mix1PWQudHJpbVN0YXJ0KCkpOlQ/Zj10WzFdLmxlbmd0aCsx"
    b"OihmPXRbMl0uc2VhcmNoKHRoaXMucnVsZXMub3RoZXIubm9uU3BhY2VDaGFyKSxmPWY+ND8xOmYs"
    b"dT1kLnNsaWNlKGYpLGYrPXRbMV0ubGVuZ3RoKSxUJiZ0aGlzLnJ1bGVzLm90aGVyLmJsYW5rTGlu"
    b"ZS50ZXN0KGcpJiYocCs9ZytgCmAsZT1lLnN1YnN0cmluZyhnLmxlbmd0aCsxKSxjPSEwKSwhYyl7"
    b"bGV0IFo9dGhpcy5ydWxlcy5vdGhlci5uZXh0QnVsbGV0UmVnZXgoZiksdGU9dGhpcy5ydWxlcy5v"
    b"dGhlci5oclJlZ2V4KGYpLG5lPXRoaXMucnVsZXMub3RoZXIuZmVuY2VzQmVnaW5SZWdleChmKSxz"
    b"ZT10aGlzLnJ1bGVzLm90aGVyLmhlYWRpbmdCZWdpblJlZ2V4KGYpLHhlPXRoaXMucnVsZXMub3Ro"
    b"ZXIuaHRtbEJlZ2luUmVnZXgoZik7Zm9yKDtlOyl7bGV0IEc9ZS5zcGxpdChgCmAsMSlbMF0sQztp"
    b"ZihnPUcsdGhpcy5vcHRpb25zLnBlZGFudGljPyhnPWcucmVwbGFjZSh0aGlzLnJ1bGVzLm90aGVy"
    b"Lmxpc3RSZXBsYWNlTmVzdGluZywiICAiKSxDPWcpOkM9Zy5yZXBsYWNlKHRoaXMucnVsZXMub3Ro"
    b"ZXIudGFiQ2hhckdsb2JhbCwiICAgICIpLG5lLnRlc3QoZyl8fHNlLnRlc3QoZyl8fHhlLnRlc3Qo"
    b"Zyl8fFoudGVzdChnKXx8dGUudGVzdChnKSlicmVhaztpZihDLnNlYXJjaCh0aGlzLnJ1bGVzLm90"
    b"aGVyLm5vblNwYWNlQ2hhcik+PWZ8fCFnLnRyaW0oKSl1Kz1gCmArQy5zbGljZShmKTtlbHNle2lm"
    b"KFR8fGQucmVwbGFjZSh0aGlzLnJ1bGVzLm90aGVyLnRhYkNoYXJHbG9iYWwsIiAgICAiKS5zZWFy"
    b"Y2godGhpcy5ydWxlcy5vdGhlci5ub25TcGFjZUNoYXIpPj00fHxuZS50ZXN0KGQpfHxzZS50ZXN0"
    b"KGQpfHx0ZS50ZXN0KGQpKWJyZWFrO3UrPWAKYCtnfSFUJiYhZy50cmltKCkmJihUPSEwKSxwKz1H"
    b"K2AKYCxlPWUuc3Vic3RyaW5nKEcubGVuZ3RoKzEpLGQ9Qy5zbGljZShmKX19aS5sb29zZXx8KG8/"
    b"aS5sb29zZT0hMDp0aGlzLnJ1bGVzLm90aGVyLmRvdWJsZUJsYW5rTGluZS50ZXN0KHApJiYobz0h"
    b"MCkpO2xldCB5PW51bGwsZWU7dGhpcy5vcHRpb25zLmdmbSYmKHk9dGhpcy5ydWxlcy5vdGhlci5s"
    b"aXN0SXNUYXNrLmV4ZWModSkseSYmKGVlPXlbMF0hPT0iWyBdICIsdT11LnJlcGxhY2UodGhpcy5y"
    b"dWxlcy5vdGhlci5saXN0UmVwbGFjZVRhc2ssIiIpKSksaS5pdGVtcy5wdXNoKHt0eXBlOiJsaXN0"
    b"X2l0ZW0iLHJhdzpwLHRhc2s6ISF5LGNoZWNrZWQ6ZWUsbG9vc2U6ITEsdGV4dDp1LHRva2Vuczpb"
    b"XX0pLGkucmF3Kz1wfWxldCBhPWkuaXRlbXMuYXQoLTEpO2lmKGEpYS5yYXc9YS5yYXcudHJpbUVu"
    b"ZCgpLGEudGV4dD1hLnRleHQudHJpbUVuZCgpO2Vsc2UgcmV0dXJuO2kucmF3PWkucmF3LnRyaW1F"
    b"bmQoKTtmb3IobGV0IGM9MDtjPGkuaXRlbXMubGVuZ3RoO2MrKylpZih0aGlzLmxleGVyLnN0YXRl"
    b"LnRvcD0hMSxpLml0ZW1zW2NdLnRva2Vucz10aGlzLmxleGVyLmJsb2NrVG9rZW5zKGkuaXRlbXNb"
    b"Y10udGV4dCxbXSksIWkubG9vc2Upe2xldCBwPWkuaXRlbXNbY10udG9rZW5zLmZpbHRlcihkPT5k"
    b"LnR5cGU9PT0ic3BhY2UiKSx1PXAubGVuZ3RoPjAmJnAuc29tZShkPT50aGlzLnJ1bGVzLm90aGVy"
    b"LmFueUxpbmUudGVzdChkLnJhdykpO2kubG9vc2U9dX1pZihpLmxvb3NlKWZvcihsZXQgYz0wO2M8"
    b"aS5pdGVtcy5sZW5ndGg7YysrKWkuaXRlbXNbY10ubG9vc2U9ITA7cmV0dXJuIGl9fWh0bWwoZSl7"
    b"bGV0IHQ9dGhpcy5ydWxlcy5ibG9jay5odG1sLmV4ZWMoZSk7aWYodClyZXR1cm57dHlwZToiaHRt"
    b"bCIsYmxvY2s6ITAscmF3OnRbMF0scHJlOnRbMV09PT0icHJlInx8dFsxXT09PSJzY3JpcHQifHx0"
    b"WzFdPT09InN0eWxlIix0ZXh0OnRbMF19fWRlZihlKXtsZXQgdD10aGlzLnJ1bGVzLmJsb2NrLmRl"
    b"Zi5leGVjKGUpO2lmKHQpe2xldCBuPXRbMV0udG9Mb3dlckNhc2UoKS5yZXBsYWNlKHRoaXMucnVs"
    b"ZXMub3RoZXIubXVsdGlwbGVTcGFjZUdsb2JhbCwiICIpLHM9dFsyXT90WzJdLnJlcGxhY2UodGhp"
    b"cy5ydWxlcy5vdGhlci5ocmVmQnJhY2tldHMsIiQxIikucmVwbGFjZSh0aGlzLnJ1bGVzLmlubGlu"
    b"ZS5hbnlQdW5jdHVhdGlvbiwiJDEiKToiIixpPXRbM10/dFszXS5zdWJzdHJpbmcoMSx0WzNdLmxl"
    b"bmd0aC0xKS5yZXBsYWNlKHRoaXMucnVsZXMuaW5saW5lLmFueVB1bmN0dWF0aW9uLCIkMSIpOnRb"
    b"M107cmV0dXJue3R5cGU6ImRlZiIsdGFnOm4scmF3OnRbMF0saHJlZjpzLHRpdGxlOml9fX10YWJs"
    b"ZShlKXtsZXQgdD10aGlzLnJ1bGVzLmJsb2NrLnRhYmxlLmV4ZWMoZSk7aWYoIXR8fCF0aGlzLnJ1"
    b"bGVzLm90aGVyLnRhYmxlRGVsaW1pdGVyLnRlc3QodFsyXSkpcmV0dXJuO2xldCBuPVkodFsxXSks"
    b"cz10WzJdLnJlcGxhY2UodGhpcy5ydWxlcy5vdGhlci50YWJsZUFsaWduQ2hhcnMsIiIpLnNwbGl0"
    b"KCJ8IiksaT10WzNdPy50cmltKCk/dFszXS5yZXBsYWNlKHRoaXMucnVsZXMub3RoZXIudGFibGVS"
    b"b3dCbGFua0xpbmUsIiIpLnNwbGl0KGAKYCk6W10scj17dHlwZToidGFibGUiLHJhdzp0WzBdLGhl"
    b"YWRlcjpbXSxhbGlnbjpbXSxyb3dzOltdfTtpZihuLmxlbmd0aD09PXMubGVuZ3RoKXtmb3IobGV0"
    b"IG8gb2Ygcyl0aGlzLnJ1bGVzLm90aGVyLnRhYmxlQWxpZ25SaWdodC50ZXN0KG8pP3IuYWxpZ24u"
    b"cHVzaCgicmlnaHQiKTp0aGlzLnJ1bGVzLm90aGVyLnRhYmxlQWxpZ25DZW50ZXIudGVzdChvKT9y"
    b"LmFsaWduLnB1c2goImNlbnRlciIpOnRoaXMucnVsZXMub3RoZXIudGFibGVBbGlnbkxlZnQudGVz"
    b"dChvKT9yLmFsaWduLnB1c2goImxlZnQiKTpyLmFsaWduLnB1c2gobnVsbCk7Zm9yKGxldCBvPTA7"
    b"bzxuLmxlbmd0aDtvKyspci5oZWFkZXIucHVzaCh7dGV4dDpuW29dLHRva2Vuczp0aGlzLmxleGVy"
    b"LmlubGluZShuW29dKSxoZWFkZXI6ITAsYWxpZ246ci5hbGlnbltvXX0pO2ZvcihsZXQgbyBvZiBp"
    b"KXIucm93cy5wdXNoKFkobyxyLmhlYWRlci5sZW5ndGgpLm1hcCgoYSxjKT0+KHt0ZXh0OmEsdG9r"
    b"ZW5zOnRoaXMubGV4ZXIuaW5saW5lKGEpLGhlYWRlcjohMSxhbGlnbjpyLmFsaWduW2NdfSkpKTty"
    b"ZXR1cm4gcn19bGhlYWRpbmcoZSl7bGV0IHQ9dGhpcy5ydWxlcy5ibG9jay5saGVhZGluZy5leGVj"
    b"KGUpO2lmKHQpcmV0dXJue3R5cGU6ImhlYWRpbmciLHJhdzp0WzBdLGRlcHRoOnRbMl0uY2hhckF0"
    b"KDApPT09Ij0iPzE6Mix0ZXh0OnRbMV0sdG9rZW5zOnRoaXMubGV4ZXIuaW5saW5lKHRbMV0pfX1w"
    b"YXJhZ3JhcGgoZSl7bGV0IHQ9dGhpcy5ydWxlcy5ibG9jay5wYXJhZ3JhcGguZXhlYyhlKTtpZih0"
    b"KXtsZXQgbj10WzFdLmNoYXJBdCh0WzFdLmxlbmd0aC0xKT09PWAKYD90WzFdLnNsaWNlKDAsLTEp"
    b"OnRbMV07cmV0dXJue3R5cGU6InBhcmFncmFwaCIscmF3OnRbMF0sdGV4dDpuLHRva2Vuczp0aGlz"
    b"LmxleGVyLmlubGluZShuKX19fXRleHQoZSl7bGV0IHQ9dGhpcy5ydWxlcy5ibG9jay50ZXh0LmV4"
    b"ZWMoZSk7aWYodClyZXR1cm57dHlwZToidGV4dCIscmF3OnRbMF0sdGV4dDp0WzBdLHRva2Vuczp0"
    b"aGlzLmxleGVyLmlubGluZSh0WzBdKX19ZXNjYXBlKGUpe2xldCB0PXRoaXMucnVsZXMuaW5saW5l"
    b"LmVzY2FwZS5leGVjKGUpO2lmKHQpcmV0dXJue3R5cGU6ImVzY2FwZSIscmF3OnRbMF0sdGV4dDp0"
    b"WzFdfX10YWcoZSl7bGV0IHQ9dGhpcy5ydWxlcy5pbmxpbmUudGFnLmV4ZWMoZSk7aWYodClyZXR1"
    b"cm4hdGhpcy5sZXhlci5zdGF0ZS5pbkxpbmsmJnRoaXMucnVsZXMub3RoZXIuc3RhcnRBVGFnLnRl"
    b"c3QodFswXSk/dGhpcy5sZXhlci5zdGF0ZS5pbkxpbms9ITA6dGhpcy5sZXhlci5zdGF0ZS5pbkxp"
    b"bmsmJnRoaXMucnVsZXMub3RoZXIuZW5kQVRhZy50ZXN0KHRbMF0pJiYodGhpcy5sZXhlci5zdGF0"
    b"ZS5pbkxpbms9ITEpLCF0aGlzLmxleGVyLnN0YXRlLmluUmF3QmxvY2smJnRoaXMucnVsZXMub3Ro"
    b"ZXIuc3RhcnRQcmVTY3JpcHRUYWcudGVzdCh0WzBdKT90aGlzLmxleGVyLnN0YXRlLmluUmF3Qmxv"
    b"Y2s9ITA6dGhpcy5sZXhlci5zdGF0ZS5pblJhd0Jsb2NrJiZ0aGlzLnJ1bGVzLm90aGVyLmVuZFBy"
    b"ZVNjcmlwdFRhZy50ZXN0KHRbMF0pJiYodGhpcy5sZXhlci5zdGF0ZS5pblJhd0Jsb2NrPSExKSx7"
    b"dHlwZToiaHRtbCIscmF3OnRbMF0saW5MaW5rOnRoaXMubGV4ZXIuc3RhdGUuaW5MaW5rLGluUmF3"
    b"QmxvY2s6dGhpcy5sZXhlci5zdGF0ZS5pblJhd0Jsb2NrLGJsb2NrOiExLHRleHQ6dFswXX19bGlu"
    b"ayhlKXtsZXQgdD10aGlzLnJ1bGVzLmlubGluZS5saW5rLmV4ZWMoZSk7aWYodCl7bGV0IG49dFsy"
    b"XS50cmltKCk7aWYoIXRoaXMub3B0aW9ucy5wZWRhbnRpYyYmdGhpcy5ydWxlcy5vdGhlci5zdGFy"
    b"dEFuZ2xlQnJhY2tldC50ZXN0KG4pKXtpZighdGhpcy5ydWxlcy5vdGhlci5lbmRBbmdsZUJyYWNr"
    b"ZXQudGVzdChuKSlyZXR1cm47bGV0IHI9QShuLnNsaWNlKDAsLTEpLCJcXCIpO2lmKChuLmxlbmd0"
    b"aC1yLmxlbmd0aCklMj09PTApcmV0dXJufWVsc2V7bGV0IHI9ZGUodFsyXSwiKCkiKTtpZihyPT09"
    b"LTIpcmV0dXJuO2lmKHI+LTEpe2xldCBhPSh0WzBdLmluZGV4T2YoIiEiKT09PTA/NTo0KSt0WzFd"
    b"Lmxlbmd0aCtyO3RbMl09dFsyXS5zdWJzdHJpbmcoMCxyKSx0WzBdPXRbMF0uc3Vic3RyaW5nKDAs"
    b"YSkudHJpbSgpLHRbM109IiJ9fWxldCBzPXRbMl0saT0iIjtpZih0aGlzLm9wdGlvbnMucGVkYW50"
    b"aWMpe2xldCByPXRoaXMucnVsZXMub3RoZXIucGVkYW50aWNIcmVmVGl0bGUuZXhlYyhzKTtyJiYo"
    b"cz1yWzFdLGk9clszXSl9ZWxzZSBpPXRbM10/dFszXS5zbGljZSgxLC0xKToiIjtyZXR1cm4gcz1z"
    b"LnRyaW0oKSx0aGlzLnJ1bGVzLm90aGVyLnN0YXJ0QW5nbGVCcmFja2V0LnRlc3QocykmJih0aGlz"
    b"Lm9wdGlvbnMucGVkYW50aWMmJiF0aGlzLnJ1bGVzLm90aGVyLmVuZEFuZ2xlQnJhY2tldC50ZXN0"
    b"KG4pP3M9cy5zbGljZSgxKTpzPXMuc2xpY2UoMSwtMSkpLG1lKHQse2hyZWY6cyYmcy5yZXBsYWNl"
    b"KHRoaXMucnVsZXMuaW5saW5lLmFueVB1bmN0dWF0aW9uLCIkMSIpLHRpdGxlOmkmJmkucmVwbGFj"
    b"ZSh0aGlzLnJ1bGVzLmlubGluZS5hbnlQdW5jdHVhdGlvbiwiJDEiKX0sdFswXSx0aGlzLmxleGVy"
    b"LHRoaXMucnVsZXMpfX1yZWZsaW5rKGUsdCl7bGV0IG47aWYoKG49dGhpcy5ydWxlcy5pbmxpbmUu"
    b"cmVmbGluay5leGVjKGUpKXx8KG49dGhpcy5ydWxlcy5pbmxpbmUubm9saW5rLmV4ZWMoZSkpKXts"
    b"ZXQgcz0oblsyXXx8blsxXSkucmVwbGFjZSh0aGlzLnJ1bGVzLm90aGVyLm11bHRpcGxlU3BhY2VH"
    b"bG9iYWwsIiAiKSxpPXRbcy50b0xvd2VyQ2FzZSgpXTtpZighaSl7bGV0IHI9blswXS5jaGFyQXQo"
    b"MCk7cmV0dXJue3R5cGU6InRleHQiLHJhdzpyLHRleHQ6cn19cmV0dXJuIG1lKG4saSxuWzBdLHRo"
    b"aXMubGV4ZXIsdGhpcy5ydWxlcyl9fWVtU3Ryb25nKGUsdCxuPSIiKXtsZXQgcz10aGlzLnJ1bGVz"
    b"LmlubGluZS5lbVN0cm9uZ0xEZWxpbS5leGVjKGUpO2lmKCFzfHxzWzNdJiZuLm1hdGNoKHRoaXMu"
    b"cnVsZXMub3RoZXIudW5pY29kZUFscGhhTnVtZXJpYykpcmV0dXJuO2lmKCEoc1sxXXx8c1syXXx8"
    b"IiIpfHwhbnx8dGhpcy5ydWxlcy5pbmxpbmUucHVuY3R1YXRpb24uZXhlYyhuKSl7bGV0IHI9Wy4u"
    b"LnNbMF1dLmxlbmd0aC0xLG8sYSxjPXIscD0wLHU9c1swXVswXT09PSIqIj90aGlzLnJ1bGVzLmlu"
    b"bGluZS5lbVN0cm9uZ1JEZWxpbUFzdDp0aGlzLnJ1bGVzLmlubGluZS5lbVN0cm9uZ1JEZWxpbVVu"
    b"ZDtmb3IodS5sYXN0SW5kZXg9MCx0PXQuc2xpY2UoLTEqZS5sZW5ndGgrcik7KHM9dS5leGVjKHQp"
    b"KSE9bnVsbDspe2lmKG89c1sxXXx8c1syXXx8c1szXXx8c1s0XXx8c1s1XXx8c1s2XSwhbyljb250"
    b"aW51ZTtpZihhPVsuLi5vXS5sZW5ndGgsc1szXXx8c1s0XSl7Yys9YTtjb250aW51ZX1lbHNlIGlm"
    b"KChzWzVdfHxzWzZdKSYmciUzJiYhKChyK2EpJTMpKXtwKz1hO2NvbnRpbnVlfWlmKGMtPWEsYz4w"
    b"KWNvbnRpbnVlO2E9TWF0aC5taW4oYSxhK2MrcCk7bGV0IGQ9Wy4uLnNbMF1dWzBdLmxlbmd0aCxn"
    b"PWUuc2xpY2UoMCxyK3MuaW5kZXgrZCthKTtpZihNYXRoLm1pbihyLGEpJTIpe2xldCBmPWcuc2xp"
    b"Y2UoMSwtMSk7cmV0dXJue3R5cGU6ImVtIixyYXc6Zyx0ZXh0OmYsdG9rZW5zOnRoaXMubGV4ZXIu"
    b"aW5saW5lVG9rZW5zKGYpfX1sZXQgVD1nLnNsaWNlKDIsLTIpO3JldHVybnt0eXBlOiJzdHJvbmci"
    b"LHJhdzpnLHRleHQ6VCx0b2tlbnM6dGhpcy5sZXhlci5pbmxpbmVUb2tlbnMoVCl9fX19Y29kZXNw"
    b"YW4oZSl7bGV0IHQ9dGhpcy5ydWxlcy5pbmxpbmUuY29kZS5leGVjKGUpO2lmKHQpe2xldCBuPXRb"
    b"Ml0ucmVwbGFjZSh0aGlzLnJ1bGVzLm90aGVyLm5ld0xpbmVDaGFyR2xvYmFsLCIgIikscz10aGlz"
    b"LnJ1bGVzLm90aGVyLm5vblNwYWNlQ2hhci50ZXN0KG4pLGk9dGhpcy5ydWxlcy5vdGhlci5zdGFy"
    b"dGluZ1NwYWNlQ2hhci50ZXN0KG4pJiZ0aGlzLnJ1bGVzLm90aGVyLmVuZGluZ1NwYWNlQ2hhci50"
    b"ZXN0KG4pO3JldHVybiBzJiZpJiYobj1uLnN1YnN0cmluZygxLG4ubGVuZ3RoLTEpKSx7dHlwZToi"
    b"Y29kZXNwYW4iLHJhdzp0WzBdLHRleHQ6bn19fWJyKGUpe2xldCB0PXRoaXMucnVsZXMuaW5saW5l"
    b"LmJyLmV4ZWMoZSk7aWYodClyZXR1cm57dHlwZToiYnIiLHJhdzp0WzBdfX1kZWwoZSl7bGV0IHQ9"
    b"dGhpcy5ydWxlcy5pbmxpbmUuZGVsLmV4ZWMoZSk7aWYodClyZXR1cm57dHlwZToiZGVsIixyYXc6"
    b"dFswXSx0ZXh0OnRbMl0sdG9rZW5zOnRoaXMubGV4ZXIuaW5saW5lVG9rZW5zKHRbMl0pfX1hdXRv"
    b"bGluayhlKXtsZXQgdD10aGlzLnJ1bGVzLmlubGluZS5hdXRvbGluay5leGVjKGUpO2lmKHQpe2xl"
    b"dCBuLHM7cmV0dXJuIHRbMl09PT0iQCI/KG49dFsxXSxzPSJtYWlsdG86IituKToobj10WzFdLHM9"
    b"bikse3R5cGU6ImxpbmsiLHJhdzp0WzBdLHRleHQ6bixocmVmOnMsdG9rZW5zOlt7dHlwZToidGV4"
    b"dCIscmF3Om4sdGV4dDpufV19fX11cmwoZSl7bGV0IHQ7aWYodD10aGlzLnJ1bGVzLmlubGluZS51"
    b"cmwuZXhlYyhlKSl7bGV0IG4scztpZih0WzJdPT09IkAiKW49dFswXSxzPSJtYWlsdG86IituO2Vs"
    b"c2V7bGV0IGk7ZG8gaT10WzBdLHRbMF09dGhpcy5ydWxlcy5pbmxpbmUuX2JhY2twZWRhbC5leGVj"
    b"KHRbMF0pPy5bMF0/PyIiO3doaWxlKGkhPT10WzBdKTtuPXRbMF0sdFsxXT09PSJ3d3cuIj9zPSJo"
    b"dHRwOi8vIit0WzBdOnM9dFswXX1yZXR1cm57dHlwZToibGluayIscmF3OnRbMF0sdGV4dDpuLGhy"
    b"ZWY6cyx0b2tlbnM6W3t0eXBlOiJ0ZXh0IixyYXc6bix0ZXh0Om59XX19fWlubGluZVRleHQoZSl7"
    b"bGV0IHQ9dGhpcy5ydWxlcy5pbmxpbmUudGV4dC5leGVjKGUpO2lmKHQpe2xldCBuPXRoaXMubGV4"
    b"ZXIuc3RhdGUuaW5SYXdCbG9jaztyZXR1cm57dHlwZToidGV4dCIscmF3OnRbMF0sdGV4dDp0WzBd"
    b"LGVzY2FwZWQ6bn19fX07dmFyIHg9Y2xhc3MgbHt0b2tlbnM7b3B0aW9ucztzdGF0ZTt0b2tlbml6"
    b"ZXI7aW5saW5lUXVldWU7Y29uc3RydWN0b3IoZSl7dGhpcy50b2tlbnM9W10sdGhpcy50b2tlbnMu"
    b"bGlua3M9T2JqZWN0LmNyZWF0ZShudWxsKSx0aGlzLm9wdGlvbnM9ZXx8dyx0aGlzLm9wdGlvbnMu"
    b"dG9rZW5pemVyPXRoaXMub3B0aW9ucy50b2tlbml6ZXJ8fG5ldyBTLHRoaXMudG9rZW5pemVyPXRo"
    b"aXMub3B0aW9ucy50b2tlbml6ZXIsdGhpcy50b2tlbml6ZXIub3B0aW9ucz10aGlzLm9wdGlvbnMs"
    b"dGhpcy50b2tlbml6ZXIubGV4ZXI9dGhpcyx0aGlzLmlubGluZVF1ZXVlPVtdLHRoaXMuc3RhdGU9"
    b"e2luTGluazohMSxpblJhd0Jsb2NrOiExLHRvcDohMH07bGV0IHQ9e290aGVyOm0sYmxvY2s6Qi5u"
    b"b3JtYWwsaW5saW5lOlAubm9ybWFsfTt0aGlzLm9wdGlvbnMucGVkYW50aWM/KHQuYmxvY2s9Qi5w"
    b"ZWRhbnRpYyx0LmlubGluZT1QLnBlZGFudGljKTp0aGlzLm9wdGlvbnMuZ2ZtJiYodC5ibG9jaz1C"
    b"LmdmbSx0aGlzLm9wdGlvbnMuYnJlYWtzP3QuaW5saW5lPVAuYnJlYWtzOnQuaW5saW5lPVAuZ2Zt"
    b"KSx0aGlzLnRva2VuaXplci5ydWxlcz10fXN0YXRpYyBnZXQgcnVsZXMoKXtyZXR1cm57YmxvY2s6"
    b"QixpbmxpbmU6UH19c3RhdGljIGxleChlLHQpe3JldHVybiBuZXcgbCh0KS5sZXgoZSl9c3RhdGlj"
    b"IGxleElubGluZShlLHQpe3JldHVybiBuZXcgbCh0KS5pbmxpbmVUb2tlbnMoZSl9bGV4KGUpe2U9"
    b"ZS5yZXBsYWNlKG0uY2FycmlhZ2VSZXR1cm4sYApgKSx0aGlzLmJsb2NrVG9rZW5zKGUsdGhpcy50"
    b"b2tlbnMpO2ZvcihsZXQgdD0wO3Q8dGhpcy5pbmxpbmVRdWV1ZS5sZW5ndGg7dCsrKXtsZXQgbj10"
    b"aGlzLmlubGluZVF1ZXVlW3RdO3RoaXMuaW5saW5lVG9rZW5zKG4uc3JjLG4udG9rZW5zKX1yZXR1"
    b"cm4gdGhpcy5pbmxpbmVRdWV1ZT1bXSx0aGlzLnRva2Vuc31ibG9ja1Rva2VucyhlLHQ9W10sbj0h"
    b"MSl7Zm9yKHRoaXMub3B0aW9ucy5wZWRhbnRpYyYmKGU9ZS5yZXBsYWNlKG0udGFiQ2hhckdsb2Jh"
    b"bCwiICAgICIpLnJlcGxhY2UobS5zcGFjZUxpbmUsIiIpKTtlOyl7bGV0IHM7aWYodGhpcy5vcHRp"
    b"b25zLmV4dGVuc2lvbnM/LmJsb2NrPy5zb21lKHI9PihzPXIuY2FsbCh7bGV4ZXI6dGhpc30sZSx0"
    b"KSk/KGU9ZS5zdWJzdHJpbmcocy5yYXcubGVuZ3RoKSx0LnB1c2gocyksITApOiExKSljb250aW51"
    b"ZTtpZihzPXRoaXMudG9rZW5pemVyLnNwYWNlKGUpKXtlPWUuc3Vic3RyaW5nKHMucmF3Lmxlbmd0"
    b"aCk7bGV0IHI9dC5hdCgtMSk7cy5yYXcubGVuZ3RoPT09MSYmciE9PXZvaWQgMD9yLnJhdys9YApg"
    b"OnQucHVzaChzKTtjb250aW51ZX1pZihzPXRoaXMudG9rZW5pemVyLmNvZGUoZSkpe2U9ZS5zdWJz"
    b"dHJpbmcocy5yYXcubGVuZ3RoKTtsZXQgcj10LmF0KC0xKTtyPy50eXBlPT09InBhcmFncmFwaCJ8"
    b"fHI/LnR5cGU9PT0idGV4dCI/KHIucmF3Kz1gCmArcy5yYXcsci50ZXh0Kz1gCmArcy50ZXh0LHRo"
    b"aXMuaW5saW5lUXVldWUuYXQoLTEpLnNyYz1yLnRleHQpOnQucHVzaChzKTtjb250aW51ZX1pZihz"
    b"PXRoaXMudG9rZW5pemVyLmZlbmNlcyhlKSl7ZT1lLnN1YnN0cmluZyhzLnJhdy5sZW5ndGgpLHQu"
    b"cHVzaChzKTtjb250aW51ZX1pZihzPXRoaXMudG9rZW5pemVyLmhlYWRpbmcoZSkpe2U9ZS5zdWJz"
    b"dHJpbmcocy5yYXcubGVuZ3RoKSx0LnB1c2gocyk7Y29udGludWV9aWYocz10aGlzLnRva2VuaXpl"
    b"ci5ocihlKSl7ZT1lLnN1YnN0cmluZyhzLnJhdy5sZW5ndGgpLHQucHVzaChzKTtjb250aW51ZX1p"
    b"ZihzPXRoaXMudG9rZW5pemVyLmJsb2NrcXVvdGUoZSkpe2U9ZS5zdWJzdHJpbmcocy5yYXcubGVu"
    b"Z3RoKSx0LnB1c2gocyk7Y29udGludWV9aWYocz10aGlzLnRva2VuaXplci5saXN0KGUpKXtlPWUu"
    b"c3Vic3RyaW5nKHMucmF3Lmxlbmd0aCksdC5wdXNoKHMpO2NvbnRpbnVlfWlmKHM9dGhpcy50b2tl"
    b"bml6ZXIuaHRtbChlKSl7ZT1lLnN1YnN0cmluZyhzLnJhdy5sZW5ndGgpLHQucHVzaChzKTtjb250"
    b"aW51ZX1pZihzPXRoaXMudG9rZW5pemVyLmRlZihlKSl7ZT1lLnN1YnN0cmluZyhzLnJhdy5sZW5n"
    b"dGgpO2xldCByPXQuYXQoLTEpO3I/LnR5cGU9PT0icGFyYWdyYXBoInx8cj8udHlwZT09PSJ0ZXh0"
    b"Ij8oci5yYXcrPWAKYCtzLnJhdyxyLnRleHQrPWAKYCtzLnJhdyx0aGlzLmlubGluZVF1ZXVlLmF0"
    b"KC0xKS5zcmM9ci50ZXh0KTp0aGlzLnRva2Vucy5saW5rc1tzLnRhZ118fCh0aGlzLnRva2Vucy5s"
    b"aW5rc1tzLnRhZ109e2hyZWY6cy5ocmVmLHRpdGxlOnMudGl0bGV9KTtjb250aW51ZX1pZihzPXRo"
    b"aXMudG9rZW5pemVyLnRhYmxlKGUpKXtlPWUuc3Vic3RyaW5nKHMucmF3Lmxlbmd0aCksdC5wdXNo"
    b"KHMpO2NvbnRpbnVlfWlmKHM9dGhpcy50b2tlbml6ZXIubGhlYWRpbmcoZSkpe2U9ZS5zdWJzdHJp"
    b"bmcocy5yYXcubGVuZ3RoKSx0LnB1c2gocyk7Y29udGludWV9bGV0IGk9ZTtpZih0aGlzLm9wdGlv"
    b"bnMuZXh0ZW5zaW9ucz8uc3RhcnRCbG9jayl7bGV0IHI9MS8wLG89ZS5zbGljZSgxKSxhO3RoaXMu"
    b"b3B0aW9ucy5leHRlbnNpb25zLnN0YXJ0QmxvY2suZm9yRWFjaChjPT57YT1jLmNhbGwoe2xleGVy"
    b"OnRoaXN9LG8pLHR5cGVvZiBhPT0ibnVtYmVyIiYmYT49MCYmKHI9TWF0aC5taW4ocixhKSl9KSxy"
    b"PDEvMCYmcj49MCYmKGk9ZS5zdWJzdHJpbmcoMCxyKzEpKX1pZih0aGlzLnN0YXRlLnRvcCYmKHM9"
    b"dGhpcy50b2tlbml6ZXIucGFyYWdyYXBoKGkpKSl7bGV0IHI9dC5hdCgtMSk7biYmcj8udHlwZT09"
    b"PSJwYXJhZ3JhcGgiPyhyLnJhdys9YApgK3MucmF3LHIudGV4dCs9YApgK3MudGV4dCx0aGlzLmlu"
    b"bGluZVF1ZXVlLnBvcCgpLHRoaXMuaW5saW5lUXVldWUuYXQoLTEpLnNyYz1yLnRleHQpOnQucHVz"
    b"aChzKSxuPWkubGVuZ3RoIT09ZS5sZW5ndGgsZT1lLnN1YnN0cmluZyhzLnJhdy5sZW5ndGgpO2Nv"
    b"bnRpbnVlfWlmKHM9dGhpcy50b2tlbml6ZXIudGV4dChlKSl7ZT1lLnN1YnN0cmluZyhzLnJhdy5s"
    b"ZW5ndGgpO2xldCByPXQuYXQoLTEpO3I/LnR5cGU9PT0idGV4dCI/KHIucmF3Kz1gCmArcy5yYXcs"
    b"ci50ZXh0Kz1gCmArcy50ZXh0LHRoaXMuaW5saW5lUXVldWUucG9wKCksdGhpcy5pbmxpbmVRdWV1"
    b"ZS5hdCgtMSkuc3JjPXIudGV4dCk6dC5wdXNoKHMpO2NvbnRpbnVlfWlmKGUpe2xldCByPSJJbmZp"
    b"bml0ZSBsb29wIG9uIGJ5dGU6ICIrZS5jaGFyQ29kZUF0KDApO2lmKHRoaXMub3B0aW9ucy5zaWxl"
    b"bnQpe2NvbnNvbGUuZXJyb3Iocik7YnJlYWt9ZWxzZSB0aHJvdyBuZXcgRXJyb3Iocil9fXJldHVy"
    b"biB0aGlzLnN0YXRlLnRvcD0hMCx0fWlubGluZShlLHQ9W10pe3JldHVybiB0aGlzLmlubGluZVF1"
    b"ZXVlLnB1c2goe3NyYzplLHRva2Vuczp0fSksdH1pbmxpbmVUb2tlbnMoZSx0PVtdKXtsZXQgbj1l"
    b"LHM9bnVsbDtpZih0aGlzLnRva2Vucy5saW5rcyl7bGV0IG89T2JqZWN0LmtleXModGhpcy50b2tl"
    b"bnMubGlua3MpO2lmKG8ubGVuZ3RoPjApZm9yKDsocz10aGlzLnRva2VuaXplci5ydWxlcy5pbmxp"
    b"bmUucmVmbGlua1NlYXJjaC5leGVjKG4pKSE9bnVsbDspby5pbmNsdWRlcyhzWzBdLnNsaWNlKHNb"
    b"MF0ubGFzdEluZGV4T2YoIlsiKSsxLC0xKSkmJihuPW4uc2xpY2UoMCxzLmluZGV4KSsiWyIrImEi"
    b"LnJlcGVhdChzWzBdLmxlbmd0aC0yKSsiXSIrbi5zbGljZSh0aGlzLnRva2VuaXplci5ydWxlcy5p"
    b"bmxpbmUucmVmbGlua1NlYXJjaC5sYXN0SW5kZXgpKX1mb3IoOyhzPXRoaXMudG9rZW5pemVyLnJ1"
    b"bGVzLmlubGluZS5hbnlQdW5jdHVhdGlvbi5leGVjKG4pKSE9bnVsbDspbj1uLnNsaWNlKDAscy5p"
    b"bmRleCkrIisrIituLnNsaWNlKHRoaXMudG9rZW5pemVyLnJ1bGVzLmlubGluZS5hbnlQdW5jdHVh"
    b"dGlvbi5sYXN0SW5kZXgpO2Zvcig7KHM9dGhpcy50b2tlbml6ZXIucnVsZXMuaW5saW5lLmJsb2Nr"
    b"U2tpcC5leGVjKG4pKSE9bnVsbDspbj1uLnNsaWNlKDAscy5pbmRleCkrIlsiKyJhIi5yZXBlYXQo"
    b"c1swXS5sZW5ndGgtMikrIl0iK24uc2xpY2UodGhpcy50b2tlbml6ZXIucnVsZXMuaW5saW5lLmJs"
    b"b2NrU2tpcC5sYXN0SW5kZXgpO2xldCBpPSExLHI9IiI7Zm9yKDtlOyl7aXx8KHI9IiIpLGk9ITE7"
    b"bGV0IG87aWYodGhpcy5vcHRpb25zLmV4dGVuc2lvbnM/LmlubGluZT8uc29tZShjPT4obz1jLmNh"
    b"bGwoe2xleGVyOnRoaXN9LGUsdCkpPyhlPWUuc3Vic3RyaW5nKG8ucmF3Lmxlbmd0aCksdC5wdXNo"
    b"KG8pLCEwKTohMSkpY29udGludWU7aWYobz10aGlzLnRva2VuaXplci5lc2NhcGUoZSkpe2U9ZS5z"
    b"dWJzdHJpbmcoby5yYXcubGVuZ3RoKSx0LnB1c2gobyk7Y29udGludWV9aWYobz10aGlzLnRva2Vu"
    b"aXplci50YWcoZSkpe2U9ZS5zdWJzdHJpbmcoby5yYXcubGVuZ3RoKSx0LnB1c2gobyk7Y29udGlu"
    b"dWV9aWYobz10aGlzLnRva2VuaXplci5saW5rKGUpKXtlPWUuc3Vic3RyaW5nKG8ucmF3Lmxlbmd0"
    b"aCksdC5wdXNoKG8pO2NvbnRpbnVlfWlmKG89dGhpcy50b2tlbml6ZXIucmVmbGluayhlLHRoaXMu"
    b"dG9rZW5zLmxpbmtzKSl7ZT1lLnN1YnN0cmluZyhvLnJhdy5sZW5ndGgpO2xldCBjPXQuYXQoLTEp"
    b"O28udHlwZT09PSJ0ZXh0IiYmYz8udHlwZT09PSJ0ZXh0Ij8oYy5yYXcrPW8ucmF3LGMudGV4dCs9"
    b"by50ZXh0KTp0LnB1c2gobyk7Y29udGludWV9aWYobz10aGlzLnRva2VuaXplci5lbVN0cm9uZyhl"
    b"LG4scikpe2U9ZS5zdWJzdHJpbmcoby5yYXcubGVuZ3RoKSx0LnB1c2gobyk7Y29udGludWV9aWYo"
    b"bz10aGlzLnRva2VuaXplci5jb2Rlc3BhbihlKSl7ZT1lLnN1YnN0cmluZyhvLnJhdy5sZW5ndGgp"
    b"LHQucHVzaChvKTtjb250aW51ZX1pZihvPXRoaXMudG9rZW5pemVyLmJyKGUpKXtlPWUuc3Vic3Ry"
    b"aW5nKG8ucmF3Lmxlbmd0aCksdC5wdXNoKG8pO2NvbnRpbnVlfWlmKG89dGhpcy50b2tlbml6ZXIu"
    b"ZGVsKGUpKXtlPWUuc3Vic3RyaW5nKG8ucmF3Lmxlbmd0aCksdC5wdXNoKG8pO2NvbnRpbnVlfWlm"
    b"KG89dGhpcy50b2tlbml6ZXIuYXV0b2xpbmsoZSkpe2U9ZS5zdWJzdHJpbmcoby5yYXcubGVuZ3Ro"
    b"KSx0LnB1c2gobyk7Y29udGludWV9aWYoIXRoaXMuc3RhdGUuaW5MaW5rJiYobz10aGlzLnRva2Vu"
    b"aXplci51cmwoZSkpKXtlPWUuc3Vic3RyaW5nKG8ucmF3Lmxlbmd0aCksdC5wdXNoKG8pO2NvbnRp"
    b"bnVlfWxldCBhPWU7aWYodGhpcy5vcHRpb25zLmV4dGVuc2lvbnM/LnN0YXJ0SW5saW5lKXtsZXQg"
    b"Yz0xLzAscD1lLnNsaWNlKDEpLHU7dGhpcy5vcHRpb25zLmV4dGVuc2lvbnMuc3RhcnRJbmxpbmUu"
    b"Zm9yRWFjaChkPT57dT1kLmNhbGwoe2xleGVyOnRoaXN9LHApLHR5cGVvZiB1PT0ibnVtYmVyIiYm"
    b"dT49MCYmKGM9TWF0aC5taW4oYyx1KSl9KSxjPDEvMCYmYz49MCYmKGE9ZS5zdWJzdHJpbmcoMCxj"
    b"KzEpKX1pZihvPXRoaXMudG9rZW5pemVyLmlubGluZVRleHQoYSkpe2U9ZS5zdWJzdHJpbmcoby5y"
    b"YXcubGVuZ3RoKSxvLnJhdy5zbGljZSgtMSkhPT0iXyImJihyPW8ucmF3LnNsaWNlKC0xKSksaT0h"
    b"MDtsZXQgYz10LmF0KC0xKTtjPy50eXBlPT09InRleHQiPyhjLnJhdys9by5yYXcsYy50ZXh0Kz1v"
    b"LnRleHQpOnQucHVzaChvKTtjb250aW51ZX1pZihlKXtsZXQgYz0iSW5maW5pdGUgbG9vcCBvbiBi"
    b"eXRlOiAiK2UuY2hhckNvZGVBdCgwKTtpZih0aGlzLm9wdGlvbnMuc2lsZW50KXtjb25zb2xlLmVy"
    b"cm9yKGMpO2JyZWFrfWVsc2UgdGhyb3cgbmV3IEVycm9yKGMpfX1yZXR1cm4gdH19O3ZhciAkPWNs"
    b"YXNze29wdGlvbnM7cGFyc2VyO2NvbnN0cnVjdG9yKGUpe3RoaXMub3B0aW9ucz1lfHx3fXNwYWNl"
    b"KGUpe3JldHVybiIifWNvZGUoe3RleHQ6ZSxsYW5nOnQsZXNjYXBlZDpufSl7bGV0IHM9KHR8fCIi"
    b"KS5tYXRjaChtLm5vdFNwYWNlU3RhcnQpPy5bMF0saT1lLnJlcGxhY2UobS5lbmRpbmdOZXdsaW5l"
    b"LCIiKStgCmA7cmV0dXJuIHM/JzxwcmU+PGNvZGUgY2xhc3M9Imxhbmd1YWdlLScrUihzKSsnIj4n"
    b"KyhuP2k6UihpLCEwKSkrYDwvY29kZT48L3ByZT4KYDoiPHByZT48Y29kZT4iKyhuP2k6UihpLCEw"
    b"KSkrYDwvY29kZT48L3ByZT4KYH1ibG9ja3F1b3RlKHt0b2tlbnM6ZX0pe3JldHVybmA8YmxvY2tx"
    b"dW90ZT4KJHt0aGlzLnBhcnNlci5wYXJzZShlKX08L2Jsb2NrcXVvdGU+CmB9aHRtbCh7dGV4dDpl"
    b"fSl7cmV0dXJuIGV9aGVhZGluZyh7dG9rZW5zOmUsZGVwdGg6dH0pe3JldHVybmA8aCR7dH0+JHt0"
    b"aGlzLnBhcnNlci5wYXJzZUlubGluZShlKX08L2gke3R9PgpgfWhyKGUpe3JldHVybmA8aHI+CmB9"
    b"bGlzdChlKXtsZXQgdD1lLm9yZGVyZWQsbj1lLnN0YXJ0LHM9IiI7Zm9yKGxldCBvPTA7bzxlLml0"
    b"ZW1zLmxlbmd0aDtvKyspe2xldCBhPWUuaXRlbXNbb107cys9dGhpcy5saXN0aXRlbShhKX1sZXQg"
    b"aT10PyJvbCI6InVsIixyPXQmJm4hPT0xPycgc3RhcnQ9IicrbisnIic6IiI7cmV0dXJuIjwiK2kr"
    b"citgPgpgK3MrIjwvIitpK2A+CmB9bGlzdGl0ZW0oZSl7bGV0IHQ9IiI7aWYoZS50YXNrKXtsZXQg"
    b"bj10aGlzLmNoZWNrYm94KHtjaGVja2VkOiEhZS5jaGVja2VkfSk7ZS5sb29zZT9lLnRva2Vuc1sw"
    b"XT8udHlwZT09PSJwYXJhZ3JhcGgiPyhlLnRva2Vuc1swXS50ZXh0PW4rIiAiK2UudG9rZW5zWzBd"
    b"LnRleHQsZS50b2tlbnNbMF0udG9rZW5zJiZlLnRva2Vuc1swXS50b2tlbnMubGVuZ3RoPjAmJmUu"
    b"dG9rZW5zWzBdLnRva2Vuc1swXS50eXBlPT09InRleHQiJiYoZS50b2tlbnNbMF0udG9rZW5zWzBd"
    b"LnRleHQ9bisiICIrUihlLnRva2Vuc1swXS50b2tlbnNbMF0udGV4dCksZS50b2tlbnNbMF0udG9r"
    b"ZW5zWzBdLmVzY2FwZWQ9ITApKTplLnRva2Vucy51bnNoaWZ0KHt0eXBlOiJ0ZXh0IixyYXc6bisi"
    b"ICIsdGV4dDpuKyIgIixlc2NhcGVkOiEwfSk6dCs9bisiICJ9cmV0dXJuIHQrPXRoaXMucGFyc2Vy"
    b"LnBhcnNlKGUudG9rZW5zLCEhZS5sb29zZSksYDxsaT4ke3R9PC9saT4KYH1jaGVja2JveCh7Y2hl"
    b"Y2tlZDplfSl7cmV0dXJuIjxpbnB1dCAiKyhlPydjaGVja2VkPSIiICc6IiIpKydkaXNhYmxlZD0i"
    b"IiB0eXBlPSJjaGVja2JveCI+J31wYXJhZ3JhcGgoe3Rva2VuczplfSl7cmV0dXJuYDxwPiR7dGhp"
    b"cy5wYXJzZXIucGFyc2VJbmxpbmUoZSl9PC9wPgpgfXRhYmxlKGUpe2xldCB0PSIiLG49IiI7Zm9y"
    b"KGxldCBpPTA7aTxlLmhlYWRlci5sZW5ndGg7aSsrKW4rPXRoaXMudGFibGVjZWxsKGUuaGVhZGVy"
    b"W2ldKTt0Kz10aGlzLnRhYmxlcm93KHt0ZXh0Om59KTtsZXQgcz0iIjtmb3IobGV0IGk9MDtpPGUu"
    b"cm93cy5sZW5ndGg7aSsrKXtsZXQgcj1lLnJvd3NbaV07bj0iIjtmb3IobGV0IG89MDtvPHIubGVu"
    b"Z3RoO28rKyluKz10aGlzLnRhYmxlY2VsbChyW29dKTtzKz10aGlzLnRhYmxlcm93KHt0ZXh0Om59"
    b"KX1yZXR1cm4gcyYmKHM9YDx0Ym9keT4ke3N9PC90Ym9keT5gKSxgPHRhYmxlPgo8dGhlYWQ+CmAr"
    b"dCtgPC90aGVhZD4KYCtzK2A8L3RhYmxlPgpgfXRhYmxlcm93KHt0ZXh0OmV9KXtyZXR1cm5gPHRy"
    b"Pgoke2V9PC90cj4KYH10YWJsZWNlbGwoZSl7bGV0IHQ9dGhpcy5wYXJzZXIucGFyc2VJbmxpbmUo"
    b"ZS50b2tlbnMpLG49ZS5oZWFkZXI/InRoIjoidGQiO3JldHVybihlLmFsaWduP2A8JHtufSBhbGln"
    b"bj0iJHtlLmFsaWdufSI+YDpgPCR7bn0+YCkrdCtgPC8ke259PgpgfXN0cm9uZyh7dG9rZW5zOmV9"
    b"KXtyZXR1cm5gPHN0cm9uZz4ke3RoaXMucGFyc2VyLnBhcnNlSW5saW5lKGUpfTwvc3Ryb25nPmB9"
    b"ZW0oe3Rva2VuczplfSl7cmV0dXJuYDxlbT4ke3RoaXMucGFyc2VyLnBhcnNlSW5saW5lKGUpfTwv"
    b"ZW0+YH1jb2Rlc3Bhbih7dGV4dDplfSl7cmV0dXJuYDxjb2RlPiR7UihlLCEwKX08L2NvZGU+YH1i"
    b"cihlKXtyZXR1cm4iPGJyPiJ9ZGVsKHt0b2tlbnM6ZX0pe3JldHVybmA8ZGVsPiR7dGhpcy5wYXJz"
    b"ZXIucGFyc2VJbmxpbmUoZSl9PC9kZWw+YH1saW5rKHtocmVmOmUsdGl0bGU6dCx0b2tlbnM6bn0p"
    b"e2xldCBzPXRoaXMucGFyc2VyLnBhcnNlSW5saW5lKG4pLGk9VihlKTtpZihpPT09bnVsbClyZXR1"
    b"cm4gcztlPWk7bGV0IHI9JzxhIGhyZWY9IicrZSsnIic7cmV0dXJuIHQmJihyKz0nIHRpdGxlPSIn"
    b"K1IodCkrJyInKSxyKz0iPiIrcysiPC9hPiIscn1pbWFnZSh7aHJlZjplLHRpdGxlOnQsdGV4dDpu"
    b"LHRva2VuczpzfSl7cyYmKG49dGhpcy5wYXJzZXIucGFyc2VJbmxpbmUocyx0aGlzLnBhcnNlci50"
    b"ZXh0UmVuZGVyZXIpKTtsZXQgaT1WKGUpO2lmKGk9PT1udWxsKXJldHVybiBSKG4pO2U9aTtsZXQg"
    b"cj1gPGltZyBzcmM9IiR7ZX0iIGFsdD0iJHtufSJgO3JldHVybiB0JiYocis9YCB0aXRsZT0iJHtS"
    b"KHQpfSJgKSxyKz0iPiIscn10ZXh0KGUpe3JldHVybiJ0b2tlbnMiaW4gZSYmZS50b2tlbnM/dGhp"
    b"cy5wYXJzZXIucGFyc2VJbmxpbmUoZS50b2tlbnMpOiJlc2NhcGVkImluIGUmJmUuZXNjYXBlZD9l"
    b"LnRleHQ6UihlLnRleHQpfX07dmFyIF89Y2xhc3N7c3Ryb25nKHt0ZXh0OmV9KXtyZXR1cm4gZX1l"
    b"bSh7dGV4dDplfSl7cmV0dXJuIGV9Y29kZXNwYW4oe3RleHQ6ZX0pe3JldHVybiBlfWRlbCh7dGV4"
    b"dDplfSl7cmV0dXJuIGV9aHRtbCh7dGV4dDplfSl7cmV0dXJuIGV9dGV4dCh7dGV4dDplfSl7cmV0"
    b"dXJuIGV9bGluayh7dGV4dDplfSl7cmV0dXJuIiIrZX1pbWFnZSh7dGV4dDplfSl7cmV0dXJuIiIr"
    b"ZX1icigpe3JldHVybiIifX07dmFyIGI9Y2xhc3MgbHtvcHRpb25zO3JlbmRlcmVyO3RleHRSZW5k"
    b"ZXJlcjtjb25zdHJ1Y3RvcihlKXt0aGlzLm9wdGlvbnM9ZXx8dyx0aGlzLm9wdGlvbnMucmVuZGVy"
    b"ZXI9dGhpcy5vcHRpb25zLnJlbmRlcmVyfHxuZXcgJCx0aGlzLnJlbmRlcmVyPXRoaXMub3B0aW9u"
    b"cy5yZW5kZXJlcix0aGlzLnJlbmRlcmVyLm9wdGlvbnM9dGhpcy5vcHRpb25zLHRoaXMucmVuZGVy"
    b"ZXIucGFyc2VyPXRoaXMsdGhpcy50ZXh0UmVuZGVyZXI9bmV3IF99c3RhdGljIHBhcnNlKGUsdCl7"
    b"cmV0dXJuIG5ldyBsKHQpLnBhcnNlKGUpfXN0YXRpYyBwYXJzZUlubGluZShlLHQpe3JldHVybiBu"
    b"ZXcgbCh0KS5wYXJzZUlubGluZShlKX1wYXJzZShlLHQ9ITApe2xldCBuPSIiO2ZvcihsZXQgcz0w"
    b"O3M8ZS5sZW5ndGg7cysrKXtsZXQgaT1lW3NdO2lmKHRoaXMub3B0aW9ucy5leHRlbnNpb25zPy5y"
    b"ZW5kZXJlcnM/LltpLnR5cGVdKXtsZXQgbz1pLGE9dGhpcy5vcHRpb25zLmV4dGVuc2lvbnMucmVu"
    b"ZGVyZXJzW28udHlwZV0uY2FsbCh7cGFyc2VyOnRoaXN9LG8pO2lmKGEhPT0hMXx8IVsic3BhY2Ui"
    b"LCJociIsImhlYWRpbmciLCJjb2RlIiwidGFibGUiLCJibG9ja3F1b3RlIiwibGlzdCIsImh0bWwi"
    b"LCJwYXJhZ3JhcGgiLCJ0ZXh0Il0uaW5jbHVkZXMoby50eXBlKSl7bis9YXx8IiI7Y29udGludWV9"
    b"fWxldCByPWk7c3dpdGNoKHIudHlwZSl7Y2FzZSJzcGFjZSI6e24rPXRoaXMucmVuZGVyZXIuc3Bh"
    b"Y2Uocik7Y29udGludWV9Y2FzZSJociI6e24rPXRoaXMucmVuZGVyZXIuaHIocik7Y29udGludWV9"
    b"Y2FzZSJoZWFkaW5nIjp7bis9dGhpcy5yZW5kZXJlci5oZWFkaW5nKHIpO2NvbnRpbnVlfWNhc2Ui"
    b"Y29kZSI6e24rPXRoaXMucmVuZGVyZXIuY29kZShyKTtjb250aW51ZX1jYXNlInRhYmxlIjp7bis9"
    b"dGhpcy5yZW5kZXJlci50YWJsZShyKTtjb250aW51ZX1jYXNlImJsb2NrcXVvdGUiOntuKz10aGlz"
    b"LnJlbmRlcmVyLmJsb2NrcXVvdGUocik7Y29udGludWV9Y2FzZSJsaXN0Ijp7bis9dGhpcy5yZW5k"
    b"ZXJlci5saXN0KHIpO2NvbnRpbnVlfWNhc2UiaHRtbCI6e24rPXRoaXMucmVuZGVyZXIuaHRtbChy"
    b"KTtjb250aW51ZX1jYXNlInBhcmFncmFwaCI6e24rPXRoaXMucmVuZGVyZXIucGFyYWdyYXBoKHIp"
    b"O2NvbnRpbnVlfWNhc2UidGV4dCI6e2xldCBvPXIsYT10aGlzLnJlbmRlcmVyLnRleHQobyk7Zm9y"
    b"KDtzKzE8ZS5sZW5ndGgmJmVbcysxXS50eXBlPT09InRleHQiOylvPWVbKytzXSxhKz1gCmArdGhp"
    b"cy5yZW5kZXJlci50ZXh0KG8pO3Q/bis9dGhpcy5yZW5kZXJlci5wYXJhZ3JhcGgoe3R5cGU6InBh"
    b"cmFncmFwaCIscmF3OmEsdGV4dDphLHRva2Vuczpbe3R5cGU6InRleHQiLHJhdzphLHRleHQ6YSxl"
    b"c2NhcGVkOiEwfV19KTpuKz1hO2NvbnRpbnVlfWRlZmF1bHQ6e2xldCBvPSdUb2tlbiB3aXRoICIn"
    b"K3IudHlwZSsnIiB0eXBlIHdhcyBub3QgZm91bmQuJztpZih0aGlzLm9wdGlvbnMuc2lsZW50KXJl"
    b"dHVybiBjb25zb2xlLmVycm9yKG8pLCIiO3Rocm93IG5ldyBFcnJvcihvKX19fXJldHVybiBufXBh"
    b"cnNlSW5saW5lKGUsdD10aGlzLnJlbmRlcmVyKXtsZXQgbj0iIjtmb3IobGV0IHM9MDtzPGUubGVu"
    b"Z3RoO3MrKyl7bGV0IGk9ZVtzXTtpZih0aGlzLm9wdGlvbnMuZXh0ZW5zaW9ucz8ucmVuZGVyZXJz"
    b"Py5baS50eXBlXSl7bGV0IG89dGhpcy5vcHRpb25zLmV4dGVuc2lvbnMucmVuZGVyZXJzW2kudHlw"
    b"ZV0uY2FsbCh7cGFyc2VyOnRoaXN9LGkpO2lmKG8hPT0hMXx8IVsiZXNjYXBlIiwiaHRtbCIsImxp"
    b"bmsiLCJpbWFnZSIsInN0cm9uZyIsImVtIiwiY29kZXNwYW4iLCJiciIsImRlbCIsInRleHQiXS5p"
    b"bmNsdWRlcyhpLnR5cGUpKXtuKz1vfHwiIjtjb250aW51ZX19bGV0IHI9aTtzd2l0Y2goci50eXBl"
    b"KXtjYXNlImVzY2FwZSI6e24rPXQudGV4dChyKTticmVha31jYXNlImh0bWwiOntuKz10Lmh0bWwo"
    b"cik7YnJlYWt9Y2FzZSJsaW5rIjp7bis9dC5saW5rKHIpO2JyZWFrfWNhc2UiaW1hZ2UiOntuKz10"
    b"LmltYWdlKHIpO2JyZWFrfWNhc2Uic3Ryb25nIjp7bis9dC5zdHJvbmcocik7YnJlYWt9Y2FzZSJl"
    b"bSI6e24rPXQuZW0ocik7YnJlYWt9Y2FzZSJjb2Rlc3BhbiI6e24rPXQuY29kZXNwYW4ocik7YnJl"
    b"YWt9Y2FzZSJiciI6e24rPXQuYnIocik7YnJlYWt9Y2FzZSJkZWwiOntuKz10LmRlbChyKTticmVh"
    b"a31jYXNlInRleHQiOntuKz10LnRleHQocik7YnJlYWt9ZGVmYXVsdDp7bGV0IG89J1Rva2VuIHdp"
    b"dGggIicrci50eXBlKyciIHR5cGUgd2FzIG5vdCBmb3VuZC4nO2lmKHRoaXMub3B0aW9ucy5zaWxl"
    b"bnQpcmV0dXJuIGNvbnNvbGUuZXJyb3IobyksIiI7dGhyb3cgbmV3IEVycm9yKG8pfX19cmV0dXJu"
    b"IG59fTt2YXIgTD1jbGFzc3tvcHRpb25zO2Jsb2NrO2NvbnN0cnVjdG9yKGUpe3RoaXMub3B0aW9u"
    b"cz1lfHx3fXN0YXRpYyBwYXNzVGhyb3VnaEhvb2tzPW5ldyBTZXQoWyJwcmVwcm9jZXNzIiwicG9z"
    b"dHByb2Nlc3MiLCJwcm9jZXNzQWxsVG9rZW5zIl0pO3ByZXByb2Nlc3MoZSl7cmV0dXJuIGV9cG9z"
    b"dHByb2Nlc3MoZSl7cmV0dXJuIGV9cHJvY2Vzc0FsbFRva2VucyhlKXtyZXR1cm4gZX1wcm92aWRl"
    b"TGV4ZXIoKXtyZXR1cm4gdGhpcy5ibG9jaz94LmxleDp4LmxleElubGluZX1wcm92aWRlUGFyc2Vy"
    b"KCl7cmV0dXJuIHRoaXMuYmxvY2s/Yi5wYXJzZTpiLnBhcnNlSW5saW5lfX07dmFyIEU9Y2xhc3N7"
    b"ZGVmYXVsdHM9eigpO29wdGlvbnM9dGhpcy5zZXRPcHRpb25zO3BhcnNlPXRoaXMucGFyc2VNYXJr"
    b"ZG93bighMCk7cGFyc2VJbmxpbmU9dGhpcy5wYXJzZU1hcmtkb3duKCExKTtQYXJzZXI9YjtSZW5k"
    b"ZXJlcj0kO1RleHRSZW5kZXJlcj1fO0xleGVyPXg7VG9rZW5pemVyPVM7SG9va3M9TDtjb25zdHJ1"
    b"Y3RvciguLi5lKXt0aGlzLnVzZSguLi5lKX13YWxrVG9rZW5zKGUsdCl7bGV0IG49W107Zm9yKGxl"
    b"dCBzIG9mIGUpc3dpdGNoKG49bi5jb25jYXQodC5jYWxsKHRoaXMscykpLHMudHlwZSl7Y2FzZSJ0"
    b"YWJsZSI6e2xldCBpPXM7Zm9yKGxldCByIG9mIGkuaGVhZGVyKW49bi5jb25jYXQodGhpcy53YWxr"
    b"VG9rZW5zKHIudG9rZW5zLHQpKTtmb3IobGV0IHIgb2YgaS5yb3dzKWZvcihsZXQgbyBvZiByKW49"
    b"bi5jb25jYXQodGhpcy53YWxrVG9rZW5zKG8udG9rZW5zLHQpKTticmVha31jYXNlImxpc3QiOnts"
    b"ZXQgaT1zO249bi5jb25jYXQodGhpcy53YWxrVG9rZW5zKGkuaXRlbXMsdCkpO2JyZWFrfWRlZmF1"
    b"bHQ6e2xldCBpPXM7dGhpcy5kZWZhdWx0cy5leHRlbnNpb25zPy5jaGlsZFRva2Vucz8uW2kudHlw"
    b"ZV0/dGhpcy5kZWZhdWx0cy5leHRlbnNpb25zLmNoaWxkVG9rZW5zW2kudHlwZV0uZm9yRWFjaChy"
    b"PT57bGV0IG89aVtyXS5mbGF0KDEvMCk7bj1uLmNvbmNhdCh0aGlzLndhbGtUb2tlbnMobyx0KSl9"
    b"KTppLnRva2VucyYmKG49bi5jb25jYXQodGhpcy53YWxrVG9rZW5zKGkudG9rZW5zLHQpKSl9fXJl"
    b"dHVybiBufXVzZSguLi5lKXtsZXQgdD10aGlzLmRlZmF1bHRzLmV4dGVuc2lvbnN8fHtyZW5kZXJl"
    b"cnM6e30sY2hpbGRUb2tlbnM6e319O3JldHVybiBlLmZvckVhY2gobj0+e2xldCBzPXsuLi5ufTtp"
    b"ZihzLmFzeW5jPXRoaXMuZGVmYXVsdHMuYXN5bmN8fHMuYXN5bmN8fCExLG4uZXh0ZW5zaW9ucyYm"
    b"KG4uZXh0ZW5zaW9ucy5mb3JFYWNoKGk9PntpZighaS5uYW1lKXRocm93IG5ldyBFcnJvcigiZXh0"
    b"ZW5zaW9uIG5hbWUgcmVxdWlyZWQiKTtpZigicmVuZGVyZXIiaW4gaSl7bGV0IHI9dC5yZW5kZXJl"
    b"cnNbaS5uYW1lXTtyP3QucmVuZGVyZXJzW2kubmFtZV09ZnVuY3Rpb24oLi4ubyl7bGV0IGE9aS5y"
    b"ZW5kZXJlci5hcHBseSh0aGlzLG8pO3JldHVybiBhPT09ITEmJihhPXIuYXBwbHkodGhpcyxvKSks"
    b"YX06dC5yZW5kZXJlcnNbaS5uYW1lXT1pLnJlbmRlcmVyfWlmKCJ0b2tlbml6ZXIiaW4gaSl7aWYo"
    b"IWkubGV2ZWx8fGkubGV2ZWwhPT0iYmxvY2siJiZpLmxldmVsIT09ImlubGluZSIpdGhyb3cgbmV3"
    b"IEVycm9yKCJleHRlbnNpb24gbGV2ZWwgbXVzdCBiZSAnYmxvY2snIG9yICdpbmxpbmUnIik7bGV0"
    b"IHI9dFtpLmxldmVsXTtyP3IudW5zaGlmdChpLnRva2VuaXplcik6dFtpLmxldmVsXT1baS50b2tl"
    b"bml6ZXJdLGkuc3RhcnQmJihpLmxldmVsPT09ImJsb2NrIj90LnN0YXJ0QmxvY2s/dC5zdGFydEJs"
    b"b2NrLnB1c2goaS5zdGFydCk6dC5zdGFydEJsb2NrPVtpLnN0YXJ0XTppLmxldmVsPT09ImlubGlu"
    b"ZSImJih0LnN0YXJ0SW5saW5lP3Quc3RhcnRJbmxpbmUucHVzaChpLnN0YXJ0KTp0LnN0YXJ0SW5s"
    b"aW5lPVtpLnN0YXJ0XSkpfSJjaGlsZFRva2VucyJpbiBpJiZpLmNoaWxkVG9rZW5zJiYodC5jaGls"
    b"ZFRva2Vuc1tpLm5hbWVdPWkuY2hpbGRUb2tlbnMpfSkscy5leHRlbnNpb25zPXQpLG4ucmVuZGVy"
    b"ZXIpe2xldCBpPXRoaXMuZGVmYXVsdHMucmVuZGVyZXJ8fG5ldyAkKHRoaXMuZGVmYXVsdHMpO2Zv"
    b"cihsZXQgciBpbiBuLnJlbmRlcmVyKXtpZighKHIgaW4gaSkpdGhyb3cgbmV3IEVycm9yKGByZW5k"
    b"ZXJlciAnJHtyfScgZG9lcyBub3QgZXhpc3RgKTtpZihbIm9wdGlvbnMiLCJwYXJzZXIiXS5pbmNs"
    b"dWRlcyhyKSljb250aW51ZTtsZXQgbz1yLGE9bi5yZW5kZXJlcltvXSxjPWlbb107aVtvXT0oLi4u"
    b"cCk9PntsZXQgdT1hLmFwcGx5KGkscCk7cmV0dXJuIHU9PT0hMSYmKHU9Yy5hcHBseShpLHApKSx1"
    b"fHwiIn19cy5yZW5kZXJlcj1pfWlmKG4udG9rZW5pemVyKXtsZXQgaT10aGlzLmRlZmF1bHRzLnRv"
    b"a2VuaXplcnx8bmV3IFModGhpcy5kZWZhdWx0cyk7Zm9yKGxldCByIGluIG4udG9rZW5pemVyKXtp"
    b"ZighKHIgaW4gaSkpdGhyb3cgbmV3IEVycm9yKGB0b2tlbml6ZXIgJyR7cn0nIGRvZXMgbm90IGV4"
    b"aXN0YCk7aWYoWyJvcHRpb25zIiwicnVsZXMiLCJsZXhlciJdLmluY2x1ZGVzKHIpKWNvbnRpbnVl"
    b"O2xldCBvPXIsYT1uLnRva2VuaXplcltvXSxjPWlbb107aVtvXT0oLi4ucCk9PntsZXQgdT1hLmFw"
    b"cGx5KGkscCk7cmV0dXJuIHU9PT0hMSYmKHU9Yy5hcHBseShpLHApKSx1fX1zLnRva2VuaXplcj1p"
    b"fWlmKG4uaG9va3Mpe2xldCBpPXRoaXMuZGVmYXVsdHMuaG9va3N8fG5ldyBMO2ZvcihsZXQgciBp"
    b"biBuLmhvb2tzKXtpZighKHIgaW4gaSkpdGhyb3cgbmV3IEVycm9yKGBob29rICcke3J9JyBkb2Vz"
    b"IG5vdCBleGlzdGApO2lmKFsib3B0aW9ucyIsImJsb2NrIl0uaW5jbHVkZXMocikpY29udGludWU7"
    b"bGV0IG89cixhPW4uaG9va3Nbb10sYz1pW29dO0wucGFzc1Rocm91Z2hIb29rcy5oYXMocik/aVtv"
    b"XT1wPT57aWYodGhpcy5kZWZhdWx0cy5hc3luYylyZXR1cm4gUHJvbWlzZS5yZXNvbHZlKGEuY2Fs"
    b"bChpLHApKS50aGVuKGQ9PmMuY2FsbChpLGQpKTtsZXQgdT1hLmNhbGwoaSxwKTtyZXR1cm4gYy5j"
    b"YWxsKGksdSl9Omlbb109KC4uLnApPT57bGV0IHU9YS5hcHBseShpLHApO3JldHVybiB1PT09ITEm"
    b"Jih1PWMuYXBwbHkoaSxwKSksdX19cy5ob29rcz1pfWlmKG4ud2Fsa1Rva2Vucyl7bGV0IGk9dGhp"
    b"cy5kZWZhdWx0cy53YWxrVG9rZW5zLHI9bi53YWxrVG9rZW5zO3Mud2Fsa1Rva2Vucz1mdW5jdGlv"
    b"bihvKXtsZXQgYT1bXTtyZXR1cm4gYS5wdXNoKHIuY2FsbCh0aGlzLG8pKSxpJiYoYT1hLmNvbmNh"
    b"dChpLmNhbGwodGhpcyxvKSkpLGF9fXRoaXMuZGVmYXVsdHM9ey4uLnRoaXMuZGVmYXVsdHMsLi4u"
    b"c319KSx0aGlzfXNldE9wdGlvbnMoZSl7cmV0dXJuIHRoaXMuZGVmYXVsdHM9ey4uLnRoaXMuZGVm"
    b"YXVsdHMsLi4uZX0sdGhpc31sZXhlcihlLHQpe3JldHVybiB4LmxleChlLHQ/P3RoaXMuZGVmYXVs"
    b"dHMpfXBhcnNlcihlLHQpe3JldHVybiBiLnBhcnNlKGUsdD8/dGhpcy5kZWZhdWx0cyl9cGFyc2VN"
    b"YXJrZG93bihlKXtyZXR1cm4obixzKT0+e2xldCBpPXsuLi5zfSxyPXsuLi50aGlzLmRlZmF1bHRz"
    b"LC4uLml9LG89dGhpcy5vbkVycm9yKCEhci5zaWxlbnQsISFyLmFzeW5jKTtpZih0aGlzLmRlZmF1"
    b"bHRzLmFzeW5jPT09ITAmJmkuYXN5bmM9PT0hMSlyZXR1cm4gbyhuZXcgRXJyb3IoIm1hcmtlZCgp"
    b"OiBUaGUgYXN5bmMgb3B0aW9uIHdhcyBzZXQgdG8gdHJ1ZSBieSBhbiBleHRlbnNpb24uIFJlbW92"
    b"ZSBhc3luYzogZmFsc2UgZnJvbSB0aGUgcGFyc2Ugb3B0aW9ucyBvYmplY3QgdG8gcmV0dXJuIGEg"
    b"UHJvbWlzZS4iKSk7aWYodHlwZW9mIG4+InUifHxuPT09bnVsbClyZXR1cm4gbyhuZXcgRXJyb3Io"
    b"Im1hcmtlZCgpOiBpbnB1dCBwYXJhbWV0ZXIgaXMgdW5kZWZpbmVkIG9yIG51bGwiKSk7aWYodHlw"
    b"ZW9mIG4hPSJzdHJpbmciKXJldHVybiBvKG5ldyBFcnJvcigibWFya2VkKCk6IGlucHV0IHBhcmFt"
    b"ZXRlciBpcyBvZiB0eXBlICIrT2JqZWN0LnByb3RvdHlwZS50b1N0cmluZy5jYWxsKG4pKyIsIHN0"
    b"cmluZyBleHBlY3RlZCIpKTtyLmhvb2tzJiYoci5ob29rcy5vcHRpb25zPXIsci5ob29rcy5ibG9j"
    b"az1lKTtsZXQgYT1yLmhvb2tzP3IuaG9va3MucHJvdmlkZUxleGVyKCk6ZT94LmxleDp4LmxleElu"
    b"bGluZSxjPXIuaG9va3M/ci5ob29rcy5wcm92aWRlUGFyc2VyKCk6ZT9iLnBhcnNlOmIucGFyc2VJ"
    b"bmxpbmU7aWYoci5hc3luYylyZXR1cm4gUHJvbWlzZS5yZXNvbHZlKHIuaG9va3M/ci5ob29rcy5w"
    b"cmVwcm9jZXNzKG4pOm4pLnRoZW4ocD0+YShwLHIpKS50aGVuKHA9PnIuaG9va3M/ci5ob29rcy5w"
    b"cm9jZXNzQWxsVG9rZW5zKHApOnApLnRoZW4ocD0+ci53YWxrVG9rZW5zP1Byb21pc2UuYWxsKHRo"
    b"aXMud2Fsa1Rva2VucyhwLHIud2Fsa1Rva2VucykpLnRoZW4oKCk9PnApOnApLnRoZW4ocD0+Yyhw"
    b"LHIpKS50aGVuKHA9PnIuaG9va3M/ci5ob29rcy5wb3N0cHJvY2VzcyhwKTpwKS5jYXRjaChvKTt0"
    b"cnl7ci5ob29rcyYmKG49ci5ob29rcy5wcmVwcm9jZXNzKG4pKTtsZXQgcD1hKG4scik7ci5ob29r"
    b"cyYmKHA9ci5ob29rcy5wcm9jZXNzQWxsVG9rZW5zKHApKSxyLndhbGtUb2tlbnMmJnRoaXMud2Fs"
    b"a1Rva2VucyhwLHIud2Fsa1Rva2Vucyk7bGV0IHU9YyhwLHIpO3JldHVybiByLmhvb2tzJiYodT1y"
    b"Lmhvb2tzLnBvc3Rwcm9jZXNzKHUpKSx1fWNhdGNoKHApe3JldHVybiBvKHApfX19b25FcnJvcihl"
    b"LHQpe3JldHVybiBuPT57aWYobi5tZXNzYWdlKz1gClBsZWFzZSByZXBvcnQgdGhpcyB0byBodHRw"
    b"czovL2dpdGh1Yi5jb20vbWFya2VkanMvbWFya2VkLmAsZSl7bGV0IHM9IjxwPkFuIGVycm9yIG9j"
    b"Y3VycmVkOjwvcD48cHJlPiIrUihuLm1lc3NhZ2UrIiIsITApKyI8L3ByZT4iO3JldHVybiB0P1By"
    b"b21pc2UucmVzb2x2ZShzKTpzfWlmKHQpcmV0dXJuIFByb21pc2UucmVqZWN0KG4pO3Rocm93IG59"
    b"fX07dmFyIE09bmV3IEU7ZnVuY3Rpb24gayhsLGUpe3JldHVybiBNLnBhcnNlKGwsZSl9ay5vcHRp"
    b"b25zPWsuc2V0T3B0aW9ucz1mdW5jdGlvbihsKXtyZXR1cm4gTS5zZXRPcHRpb25zKGwpLGsuZGVm"
    b"YXVsdHM9TS5kZWZhdWx0cyxOKGsuZGVmYXVsdHMpLGt9O2suZ2V0RGVmYXVsdHM9ejtrLmRlZmF1"
    b"bHRzPXc7ay51c2U9ZnVuY3Rpb24oLi4ubCl7cmV0dXJuIE0udXNlKC4uLmwpLGsuZGVmYXVsdHM9"
    b"TS5kZWZhdWx0cyxOKGsuZGVmYXVsdHMpLGt9O2sud2Fsa1Rva2Vucz1mdW5jdGlvbihsLGUpe3Jl"
    b"dHVybiBNLndhbGtUb2tlbnMobCxlKX07ay5wYXJzZUlubGluZT1NLnBhcnNlSW5saW5lO2suUGFy"
    b"c2VyPWI7ay5wYXJzZXI9Yi5wYXJzZTtrLlJlbmRlcmVyPSQ7ay5UZXh0UmVuZGVyZXI9XztrLkxl"
    b"eGVyPXg7ay5sZXhlcj14LmxleDtrLlRva2VuaXplcj1TO2suSG9va3M9TDtrLnBhcnNlPWs7dmFy"
    b"IGl0PWsub3B0aW9ucyxvdD1rLnNldE9wdGlvbnMsbHQ9ay51c2UsYXQ9ay53YWxrVG9rZW5zLGN0"
    b"PWsucGFyc2VJbmxpbmUscHQ9ayx1dD1iLnBhcnNlLGh0PXgubGV4OwoKaWYoX19leHBvcnRzICE9"
    b"IGV4cG9ydHMpbW9kdWxlLmV4cG9ydHMgPSBleHBvcnRzO3JldHVybiBtb2R1bGUuZXhwb3J0c30p"
    b"KTsK"
).decode("utf-8")
del _b64

PORT                = 8080

def _session_path() -> Path:
    local = os.environ.get("LOCALAPPDATA", "")
    base = Path(local) if local else Path.home() / "AppData" / "Local"
    return base / "SLCode" / "ide-session.json"


def _slcode_state_dir() -> Path:
    local = os.environ.get("LOCALAPPDATA", "")
    base = Path(local) if local else Path.home() / "AppData" / "Local"
    return base / "SLCode"


_INSTANCE_MUTEX_NAME = "SLCodeServerInstance"
_SERVER_PORT_FILE    = _slcode_state_dir() / "server-port.txt"
_SERVER_PID_FILE     = _slcode_state_dir() / "server-pid.txt"

def _acquire_instance_lock(port: int):
    """Try to acquire a single-instance mutex.

    Returns the mutex handle (truthy) if we are the first/only instance.
    Returns None if another server instance is already running, after opening
    the existing instance's UI in the system browser.

    No-op and returns a sentinel on non-Windows platforms.
    """
    if sys.platform != "win32":
        return True  # not enforced on non-Windows

    try:
        import ctypes
        handle = ctypes.windll.kernel32.CreateMutexW(None, True, _INSTANCE_MUTEX_NAME)
        if ctypes.windll.kernel32.GetLastError() == 183:  # ERROR_ALREADY_EXISTS
            # Mutex exists — another instance may be running.  Verify the
            # server is actually reachable before yielding to it; a stale
            # mutex from a killed process would otherwise block every launch.
            existing_port = port
            try:
                existing_port = int(_SERVER_PORT_FILE.read_text().strip())
            except Exception:
                pass
            existing_url = f"http://127.0.0.1:{existing_port}"
            server_alive = False
            try:
                import urllib.request
                urllib.request.urlopen(
                    f"{existing_url}/api/status", timeout=2).read()
                server_alive = True
            except Exception:
                pass
            if server_alive and os.environ.get("SLCODE_FORCE_RESTART"):
                # Force-restart: the C stub already terminated the old process
                # before launching us.  The mutex may still be in "abandoned"
                # state while Windows cleans up.  Wait briefly for it to clear,
                # then claim it as the new owner.
                ctypes.windll.kernel32.CloseHandle(handle)
                _SERVER_PORT_FILE.unlink(missing_ok=True)
                for _ in range(20):
                    handle = ctypes.windll.kernel32.CreateMutexW(None, True, _INSTANCE_MUTEX_NAME)
                    if ctypes.windll.kernel32.GetLastError() != 183:
                        break
                    ctypes.windll.kernel32.CloseHandle(handle)
                    time.sleep(0.25)
                # Fall through to write port file and return handle.
            elif server_alive:
                ctypes.windll.kernel32.CloseHandle(handle)
                print(f"[slcode] Server already running — opening {existing_url}", flush=True)
                import webbrowser
                webbrowser.open(existing_url)
                return None
            # Stale mutex — previous process died without cleanup.
            # Release this handle; CreateMutex already gave us ownership
            # on an abandoned mutex, so just continue as the new owner.
            _SERVER_PORT_FILE.unlink(missing_ok=True)
        # Write our port so a future second instance can find us
        try:
            _SERVER_PORT_FILE.parent.mkdir(parents=True, exist_ok=True)
            _SERVER_PORT_FILE.write_text(str(port))
        except Exception:
            pass
        return handle
    except Exception:
        return True  # if ctypes fails, don't block startup


def _release_instance_lock(handle) -> None:
    """Release the single-instance mutex and remove the port and PID files."""
    try:
        _SERVER_PORT_FILE.unlink(missing_ok=True)
    except Exception:
        pass
    try:
        _SERVER_PID_FILE.unlink(missing_ok=True)
    except Exception:
        pass
    if handle and handle is not True and sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.kernel32.ReleaseMutex(handle)
            ctypes.windll.kernel32.CloseHandle(handle)
        except Exception:
            pass

CATEGORIES = {
    "functions":    CACHE_ROOT / "functions",
    "events":       CACHE_ROOT / "events",
    "constants":    CACHE_ROOT / "constants",
    "tutorials":    CACHE_ROOT / "tutorials",
    "ossl":         CACHE_ROOT / "ossl",
    "slua":         CACHE_ROOT / "slua",
    "patterns":     CACHE_ROOT / "patterns",
    "examples":     CACHE_ROOT / "examples",
    "reference":    CACHE_ROOT,  # root-level: types, operators, flow-control, etc.
}

# Root-level files to exclude from the reference category
REFERENCE_SKIP = {"README.md", "CHANGELOG.md"}

# ── Checker integration ──────────────────────────────────────────────────────

_syntax_mod  = None  # lsl-syntax-checker module
_sanity_mod  = None  # lsl-sanity-checker module
_lslint_bin  = None  # path to bundled lslint.exe
_lslint_btxt = None  # path to lslint-builtins.txt (for -b flag)
_mem_mod     = None  # lsl-memory-estimator module
_chan_mod     = None  # lsl-channel-map module
_sleep_mod   = None  # lsl-sleep-profiler module
_flatten_mod = None  # lsl-include-flattener module
_fmt_mod     = None  # lsl-formatter module
_sx_funcs    = None  # known functions (syntax)
_sx_events   = None  # known events   (syntax)
_sx_consts   = None  # known constants (syntax)
_sn_funcs    = None  # known functions (sanity)

_QUIET_MODE  = False  # suppress logs for machine-readable CLI output
_LOG_ENABLED = os.environ.get("SLCODE_LOG_ENABLED", "1") == "1"


# ── Logging ──────────────────────────────────────────────────────────────────

def _log(msg: str) -> None:
  """Print a timestamped log line to stderr, keeping stdout clean for JSON output."""
  if _QUIET_MODE or (not _LOG_ENABLED):
    return
  line = f"[{time.strftime('%H:%M:%S')}] {msg}"
  try:
    print(line, file=sys.stderr, flush=True)
    return
  except Exception:
    pass

  encoded = (line + "\n").encode("utf-8", errors="replace")
  for fd in (2, 1):
    try:
      os.write(fd, encoded)
      return
    except Exception:
      pass

  for stream in (getattr(sys, "stderr", None), getattr(sys, "stdout", None), getattr(sys, "__stderr__", None), getattr(sys, "__stdout__", None)):
    if not stream:
      continue
    try:
      stream.write(line + "\n")
      stream.flush()
      return
    except Exception:
      continue

  if sys.platform == "win32":
    try:
      import ctypes
      kernel32 = ctypes.windll.kernel32
      for handle_id in (-12, -11):  # STDERR, STDOUT
        handle = kernel32.GetStdHandle(handle_id)
        if not handle or handle in (ctypes.c_void_p(-1).value, -1):
          continue
        written = ctypes.c_ulong(0)
        if kernel32.WriteFile(handle, encoded, len(encoded), ctypes.byref(written), None):
          return
    except Exception:
      pass


def _emit_json(payload: dict | list) -> None:
    """Emit UTF-8 JSON safely on Windows consoles and when piped to agents."""
    text = json.dumps(payload, indent=2, ensure_ascii=True)
    try:
        sys.stdout.buffer.write(text.encode("utf-8"))
        sys.stdout.buffer.write(b"\n")
        sys.stdout.buffer.flush()
    except Exception:
        try:
            sys.stdout.write(text + "\n")
            sys.stdout.flush()
        except Exception:
            try:
                sys.__stdout__.write(text + "\n")
                sys.__stdout__.flush()
            except Exception:
                pass


def _emit_text(text: str) -> None:
    """Emit UTF-8 text safely on Windows consoles and when stdout is redirected."""
    out = (text if text is not None else "") + "\n"
    try:
        sys.stdout.buffer.write(out.encode("utf-8", errors="replace"))
        sys.stdout.buffer.flush()
    except Exception:
        try:
            sys.stdout.write(out)
            sys.stdout.flush()
        except Exception:
            try:
                sys.__stdout__.write(out)
                sys.__stdout__.flush()
            except Exception:
                pass


def _console_process_count() -> int:
  if sys.platform != "win32":
    return 0
  try:
    import ctypes
    kernel32 = ctypes.windll.kernel32
    process_ids = (ctypes.c_ulong * 16)()
    count = kernel32.GetConsoleProcessList(process_ids, len(process_ids))
    return int(count or 0)
  except Exception:
    return 0


def _is_terminal_launch() -> bool:
  if sys.platform != "win32":
    try:
      return bool(sys.stdout and sys.stdout.isatty())
    except Exception:
      return False

  try:
    if (sys.stdout and sys.stdout.isatty()) or (sys.stdin and sys.stdin.isatty()):
      return True
  except Exception:
    pass

  return _console_process_count() >= 3


def _detach_terminal_silent_launch_if_needed(args) -> bool:
  if sys.platform != "win32":
    return False
  if os.environ.get("SLCODE_DETACHED", "") == "1":
    return False
  if getattr(args, "command", None) not in (None, "serve"):
    return False

  wants_logs = bool(getattr(args, "as_browser", False) or getattr(args, "no_open", False))
  if wants_logs or (not _is_terminal_launch()):
    return False

  env = os.environ.copy()
  env["SLCODE_DETACHED"] = "1"
  creationflags = getattr(subprocess, "DETACHED_PROCESS", 0) | getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)

  if getattr(sys, "frozen", False):
    cmd = [sys.executable, *sys.argv[1:]]
  else:
    cmd = [sys.executable, str(Path(__file__).resolve()), *sys.argv[1:]]

  subprocess.Popen(
    cmd,
    stdin=subprocess.DEVNULL,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    creationflags=creationflags,
    close_fds=True,
    env=env,
    cwd=str(APP_ROOT),
  )
  return True


def _hide_own_console_if_needed(args) -> None:
  if sys.platform != "win32":
    return
  if getattr(args, "command", None) not in (None, "serve"):
    return

  wants_logs = bool(getattr(args, "as_browser", False) or getattr(args, "no_open", False))
  if wants_logs:
    return
  if _is_terminal_launch():
    return

  try:
    import ctypes
    kernel32 = ctypes.windll.kernel32
    user32 = ctypes.windll.user32
    hwnd = kernel32.GetConsoleWindow()
    if not hwnd:
      return
    user32.ShowWindow(hwnd, 0)  # SW_HIDE
    try:
      kernel32.FreeConsole()
    except Exception:
      pass
  except Exception:
    pass


def _configure_serve_log_routing(args) -> None:
  """Apply requested 4-state log behavior for Windows console launches.

  States:
    1) Double-click no flags      -> no logs
    2) Double-click -browser/-none -> popup console with logs
    3) Terminal no flags          -> no logs
    4) Terminal -browser/-none    -> logs in parent terminal
  """
  global _LOG_ENABLED
  _LOG_ENABLED = False

  if getattr(args, "command", None) not in (None, "serve"):
    return

  wants_logs = bool(getattr(args, "as_browser", False) or getattr(args, "no_open", False))
  if not wants_logs:
    return

  if sys.platform != "win32":
    _LOG_ENABLED = True
    return

  _LOG_ENABLED = True


def _clean_builtins_txt(src: Path) -> str:
  """Strip comment/blank lines from a builtins.txt; write BOM-free UTF-8 temp file; return path."""
  lines = [
    ln for ln in src.read_text(encoding="utf-8-sig").splitlines()
    if ln.strip() and not ln.strip().startswith("//")
  ]
  fd, tmp = tempfile.mkstemp(suffix=".txt", prefix="lslint_builtins_")
  with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(lines))
  return tmp


def _find_lslint() -> None:
  """Locate bundled lslint.exe and a compatible builtins.txt for the -b flag."""
  global _lslint_bin, _lslint_btxt
  for p in (BUNDLE_ROOT / "lslint.exe", APP_ROOT / "lslint.exe"):
    if p.is_file():
      _lslint_bin = str(p)
      _log(f"  lslint binary: {p.name}")
      break
  else:
    _log("  lslint binary not found — built-in style checks will be used as fallback")
    return
  # Pre-cleaned file bundled next to the binary
  for p in (BUNDLE_ROOT / "lslint-builtins.txt", APP_ROOT / "lslint-builtins.txt"):
    if p.is_file():
      _lslint_btxt = str(p)
      _log(f"  lslint builtins: {p.name}")
      return
  # Fall back to pyoptimizer builtins.txt — strip comment/BOM at runtime
  raw = CACHE_BASE / "lsl-docs" / "vscode-extension-data" / "pyoptimizer" / "builtins.txt"
  if raw.is_file():
    _lslint_btxt = _clean_builtins_txt(raw)
    _log(f"  lslint builtins: cleaned from pyoptimizer/builtins.txt")


def load_checkers():
  """Dynamically load checker and analysis skill modules from active cache skills/."""
  global _syntax_mod, _sanity_mod, _mem_mod, _chan_mod, _sleep_mod, _flatten_mod, _fmt_mod
  mods = [
    ("_syntax_mod",  "lsl-syntax-checker.py"),
    ("_sanity_mod",  "lsl-sanity-checker.py"),
    ("_mem_mod",     "lsl-memory-estimator.py"),
    ("_chan_mod",    "lsl-channel-map.py"),
    ("_sleep_mod",   "lsl-sleep-profiler.py"),
    ("_flatten_mod", "lsl-include-flattener.py"),
    ("_fmt_mod",     "lsl-formatter.py"),
  ]
  for var, fname in mods:
    p = SKILLS_PATH / fname
    if not p.exists():
      _log(f"  skill not found: {fname}")
      continue
    try:
      t0 = time.time()
      mod_name = fname.replace("-", "_").replace(".py", "")
      spec = importlib.util.spec_from_file_location(mod_name, p)
      mod = importlib.util.module_from_spec(spec)
      spec.loader.exec_module(mod)
      globals()[var] = mod
      _log(f"  loaded {fname} ({time.time()-t0:.2f}s)")
    except Exception as e:
      _log(f"  WARNING: could not load {fname}: {e}")
  _find_lslint()


def preload_checker_data():
  """Pre-load LSL cache data into both checkers (once at startup)."""
  global _sx_funcs, _sx_events, _sx_consts, _sn_funcs
  if _syntax_mod:
    try:
      _sx_funcs = _syntax_mod.load_known_functions()
      _sx_events = _syntax_mod.load_known_events()
      _sx_consts = _syntax_mod.load_known_constants()
      _log(f"  Syntax checker: {len(_sx_funcs)} funcs, "
         f"{len(_sx_events)} events, {len(_sx_consts)} consts.")
    except Exception as e:
      _log(f"  Syntax checker data load error: {e}")
  if _sanity_mod:
    try:
      _sn_funcs = _sanity_mod.load_known_functions()
      _log(f"  Sanity checker: {len(_sn_funcs)} funcs.")
    except Exception as e:
      _log(f"  Sanity checker data load error: {e}")
  if _lslint_bin:
    _log(f"  lslint: active (builtins: {'custom' if _lslint_btxt else 'compiled-in'}).")
  else:
    _log("  lslint: binary not found — built-in style checks active.")


def _run_builtin_lint_compat(source: str) -> list[tuple[str, str, int, str]]:
    """Fallback lint checks embedded in app (used when lslint binary is unavailable)."""
    issues: list[tuple[str, str, int, str]] = []
    lines = source.splitlines()

    has_default = any(re.match(r"^\s*default\s*\{\s*$", ln) for ln in lines)
    if not has_default:
        issues.append(("ERROR", "LINT004", 1, "Script is missing a default state block"))

    state_event_map: dict[str, dict[str, int]] = {}
    state_seen: dict[str, int] = {}
    state_stack: list[str] = []
    event_re = re.compile(r"^\s*([A-Za-z_]\w*)\s*\([^;{}]*\)\s*\{\s*$")
    state_re = re.compile(r"^\s*state\s+([A-Za-z_]\w*)\s*\{\s*$")

    for line_no, raw in enumerate(lines, 1):
        line = raw.rstrip("\r\n")
        stripped = line.strip()
        if not stripped:
            continue

        if "\t" in line:
            issues.append(("WARN", "LINT001", line_no,
                           "Tab character found; prefer spaces for stable formatting"))
        if line.endswith(" "):
            issues.append(("WARN", "LINT002", line_no, "Trailing whitespace"))
        if len(line) > 120:
            issues.append(("WARN", "LINT003", line_no, "Line length exceeds 120 characters"))

        if re.match(r"^\s*default\s*\{\s*$", line):
            sname = "default"
            if sname in state_seen:
                issues.append(("ERROR", "LINT005", line_no, "Duplicate state 'default'"))
            else:
                state_seen[sname] = line_no
            state_stack.append(sname)
            state_event_map.setdefault(sname, {})
        else:
            sm = state_re.match(line)
            if sm:
                sname = sm.group(1)
                if sname in state_seen:
                    issues.append(("ERROR", "LINT005", line_no, f"Duplicate state '{sname}'"))
                else:
                    state_seen[sname] = line_no
                state_stack.append(sname)
                state_event_map.setdefault(sname, {})
            elif state_stack:
                em = event_re.match(line)
                if em:
                    ev = em.group(1)
                    current = state_stack[-1]
                    first = state_event_map[current].get(ev)
                    if first:
                        issues.append((
                            "ERROR", "LINT006", line_no,
                            f"Duplicate event handler '{ev}' in state '{current}' (first at line {first})"
                        ))
                    else:
                        state_event_map[current][ev] = line_no
        m_say = re.search(r"\b(llSay|llShout|llRegionSay)\s*\(\s*(-?\d+)", line)
        if m_say:
            channel = int(m_say.group(2))
            if channel > 0:
                issues.append((
                    "WARN", "LINT007", line_no,
                    f"{m_say.group(1)} uses positive chat channel {channel}; prefer negative/private channels"
                ))

        if re.search(r"\bllSleep\s*\(", line):
            issues.append((
                "WARN", "LINT008", line_no,
                "llSleep can stall script responsiveness; prefer timer/state design when possible"
            ))
        opens = line.count("{")
        if closes > opens and state_stack:
            pop_count = min(len(state_stack), closes - opens)
            for _ in range(pop_count):
                state_stack.pop()

    dedup = []
    seen = set()
    for item in issues:
        key = (item[1], item[2], item[3])
        if key in seen:
            continue
        seen.add(key)
        dedup.append(item)
    return dedup


def _e010_comment_lines(source: str) -> set[int]:
  """Return the set of 1-based line numbers where every non-ASCII character
  sits inside a // or /* */ comment (not in code or a string literal).

  Uses a character-by-character scan so inline comments are handled correctly,
  e.g.  ``integer x; // café``  → line is in the result set.
  """
  # Build a boolean array: in_comment[i] is True if source[i] is inside a comment.
  n = len(source)
  in_comment = bytearray(n)  # 0 = code/string, 1 = comment
  i = 0
  in_block = False
  in_string = False
  while i < n:
    c = source[i]
    if in_string:
      if c == '\\' and i + 1 < n:
        i += 2        # skip escape sequence — never comment
        continue
      if c == '"':
        in_string = False
    elif in_block:
      in_comment[i] = 1
      if c == '*' and i + 1 < n and source[i + 1] == '/':
        in_comment[i + 1] = 1
        i += 2
        in_block = False
        continue
    elif c == '/' and i + 1 < n and source[i + 1] == '/':
      # Line comment: mark to end of line
      while i < n and source[i] != '\n':
        in_comment[i] = 1
        i += 1
      continue
    elif c == '/' and i + 1 < n and source[i + 1] == '*':
      in_comment[i] = 1
      in_comment[i + 1] = 1
      i += 2
      in_block = True
      continue
    elif c == '"':
      in_string = True
    i += 1

  # For each line, check whether ALL non-ASCII chars are inside comments.
  # Use keepends=True so pos advances by the actual byte count including \r\n.
  result: set[int] = set()
  pos = 0
  for lineno, line in enumerate(source.splitlines(keepends=True), 1):
    bare = line.rstrip('\r\n')
    has_nonascii = False
    all_in_comment = True
    for j, ch in enumerate(bare):
      if ord(ch) >= 128:
        has_nonascii = True
        if not in_comment[pos + j]:
          all_in_comment = False
          break
    if has_nonascii and all_in_comment:
      result.add(lineno)
    pos += len(line)
  return result


def _parse_lslint_output(output: str) -> list[tuple[str, str, int, str]]:
  """Parse lslint stderr text into (severity, code, line, msg) tuples."""
  issues: list[tuple[str, str, int, str]] = []
  pat = re.compile(
    r'^\s*(ERROR|WARN)\s*::\s*\(\s*(\d+)\s*,\s*\d+\s*\)\s*:\s*(?:\[E(\d+)\]\s*)?(.+)$'
  )
  for line in output.splitlines():
    m = pat.match(line)
    if m:
      sev = m.group(1)
      lineno = int(m.group(2))
      ecode = m.group(3)
      msg = m.group(4).strip()
      code = f"E{ecode}" if ecode else ("LSLE" if sev == "ERROR" else "LSLW")
      issues.append((sev, code, lineno, msg))
  return issues


def _run_lslint(source: str, path: str) -> list[tuple[str, str, int, str]]:
  """Run bundled lslint binary on an LSL file; fall back to built-in style checks."""
  if not _lslint_bin:
    return _run_builtin_lint_compat(source)
  cmd = [_lslint_bin, "-m", "-i"]
  if _lslint_btxt:
    cmd += ["-b", _lslint_btxt]
  cmd += ["-#", path]
  try:
    r = subprocess.run(
      cmd,
      capture_output=True,
      text=True,
      timeout=15,
      creationflags=0,
    )
    issues = _parse_lslint_output(r.stderr)
    issues = _parse_lslint_output(r.stderr)
    has_e010 = any(c in ('E10', 'E010') for _, c, _, _ in issues)
    comment_lines = _e010_comment_lines(source) if has_e010 else set()
    return [
      (sev, code, line, msg) for sev, code, line, msg in issues
      if not (code in ('E10', 'E010') and line in comment_lines)
    ]
  except subprocess.TimeoutExpired:
    return [("WARN", "LSLW_TIMEOUT", 0, "lslint check timed out; skipping")]
  except Exception as e:
    _log(f"  lslint exec error: {e}")
    return _run_builtin_lint_compat(source)


def run_checks(source: str, mode: str = "both", ossl: bool = False, firestorm: bool = False) -> dict:
  """Write LSL source to a temp file, run checkers, return structured results.

  ossl=True     — augment known-functions with os* OSSL names so they aren't flagged unknown.
  firestorm=True — pre-flatten Firestorm #include / #define directives before checking.
  """
  result: dict = {
    "issues": [],
    "stats": {"errors": 0, "warnings": 0, "infos": 0},
    "checkers_available": [],
  }
  if _syntax_mod and _sx_funcs is not None:
    result["checkers_available"].append("syntax")
  if _sanity_mod and _sn_funcs is not None:
    result["checkers_available"].append("sanity")
  result["checkers_available"].append("lint")
  if not result["checkers_available"]:
    result["error"] = "No checkers available — skill files not found in active cache skills/."
    return result

  # Firestorm: pre-process #include / #define before handing to checkers
  if firestorm:
    try:
      flat = flatten_lsl(source)
      if flat.get("result"):
        source = flat["result"]
    except Exception:
      pass

  # OSSL: build augmented known_funcs dict so os* calls aren't flagged unknown
  sx_funcs_eff = _sx_funcs
  sn_funcs_eff = _sn_funcs
  if ossl and (INDEX or True):
    build_index()
    ossl_names = {doc["name"] for doc in INDEX if doc.get("category") == "ossl"}
    if ossl_names:
      if _sx_funcs is not None:
        sx_funcs_eff = dict(_sx_funcs)
        for name in ossl_names:
          if name not in sx_funcs_eff:
            sx_funcs_eff[name] = {"param_count": -1, "return_type": "void",
                                   "sleep": 0.0, "experimental": False, "broken": False}
      if _sn_funcs is not None:
        sn_funcs_eff = dict(_sn_funcs)
        for name in ossl_names:
          if name not in sn_funcs_eff:
            sn_funcs_eff[name] = {"param_count": -1, "return_type": "void",
                                   "sleep": 0.0, "experimental": False, "broken": False}

  try:
    fd, tmp = tempfile.mkstemp(suffix=".lsl")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
      f.write(source)
  except Exception as e:
    result["error"] = f"Could not write temp file: {e}"
    return result

  seen: set = set()
  try:
    if mode in ("syntax", "both") and _syntax_mod and _sx_funcs is not None:
      try:
        for sev, code, line, msg in _syntax_mod.check_file(
            tmp, sx_funcs_eff, _sx_events, _sx_consts):
          key = (code, line, msg)
          if key not in seen:
            seen.add(key)
            result["issues"].append({"checker": "syntax", "severity": sev,
                         "code": code, "line": line, "message": msg})
      except Exception as e:
        result["issues"].append({"checker": "syntax", "severity": "ERROR",
                     "code": "INT01", "line": 0,
                     "message": f"Syntax checker error: {e}"})

    if mode in ("sanity", "both") and _sanity_mod and _sn_funcs is not None:
      try:
        for sev, code, line, msg in _sanity_mod.check_file(
            tmp, sn_funcs_eff, run_hv_protocol=False):
          key = (code, line, msg)
          if key not in seen:
            seen.add(key)
            result["issues"].append({"checker": "sanity", "severity": sev,
                         "code": code, "line": line, "message": msg})
      except Exception as e:
        result["issues"].append({"checker": "sanity", "severity": "ERROR",
                     "code": "INT02", "line": 0,
                     "message": f"Sanity checker error: {e}"})

    if mode in ("lint", "both", "all"):
      try:
        lint_issues = _run_lslint(source, tmp)
        for sev, code, line, msg in lint_issues:
          key = (code, line, msg)
          if key not in seen:
            seen.add(key)
            result["issues"].append({"checker": "lint", "severity": sev,
                         "code": code, "line": line, "message": msg})
      except Exception as e:
        result["issues"].append({"checker": "lint", "severity": "ERROR",
                     "code": "INT03", "line": 0,
                     "message": f"Lint checker error: {e}"})
  finally:
    try:
      os.unlink(tmp)
    except OSError:
      pass

  result["issues"].sort(key=lambda x: (x["line"], x["severity"]))
  s = result["stats"]
  s["errors"] = sum(1 for i in result["issues"] if i["severity"] == "ERROR")
  s["warnings"] = sum(1 for i in result["issues"] if i["severity"] == "WARN")
  s["infos"] = sum(1 for i in result["issues"] if i["severity"] == "INFO")
  return result




def run_all_analyses(source: str) -> dict:
    """Run memory, channel, and sleep analyses on LSL source. Returns combined result."""
    result: dict = {"memory": None, "channels": None, "delays": None}
    try:
        fd, tmp = tempfile.mkstemp(suffix=".lsl")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(source)
    except Exception as e:
        return {"error": f"Could not write temp file: {e}"}
    try:
        if _mem_mod:
            try:
                result["memory"] = _mem_mod.estimate_file(tmp)
            except Exception as e:
                result["memory"] = {"error": str(e)}
        if _chan_mod:
            try:
                result["channels"] = _chan_mod.channel_map_file(tmp)
            except Exception as e:
                result["channels"] = {"error": str(e)}
        if _sleep_mod:
            try:
                result["delays"] = _sleep_mod.profile_file(tmp)
            except Exception as e:
                result["delays"] = {"error": str(e)}
    finally:
        try:
            os.unlink(tmp)
        except OSError:
            pass
    return result


def format_lsl(source: str) -> dict:
    """Format LSL source using the formatter skill."""
    if not _fmt_mod:
        return {"error": "Formatter not available (lsl-formatter.py not found in skills/)."}
    try:
        return _fmt_mod.format_source(source)
    except Exception as e:
        return {"error": str(e)}


def flatten_lsl(source: str) -> dict:
    """Flatten Firestorm #include directives in LSL source."""
    if not _flatten_mod:
        return {"error": "Flattener not available (lsl-include-flattener.py not found in skills/)."}
    try:
        return _flatten_mod.flatten_source(source)
    except Exception as e:
        return {"error": str(e)}


# ── Project filesystem API ────────────────────────────────────────────────────

PROJECT_ROOT = Path.cwd().resolve() if getattr(sys, "frozen", False) else APP_ROOT


def _safe_project_path(rel: str) -> "Path | None":
    """Resolve a relative path inside the project root. Returns None if escape attempted."""
    if not rel:
        return None
    try:
        p = (PROJECT_ROOT / rel).resolve()
        if not str(p).startswith(str(PROJECT_ROOT.resolve())):
            return None
        return p
    except Exception:
        return None


def _dir_entries(folder: Path, depth: int = 8, rel_prefix: str = "") -> list:
    """Recursively list directory entries up to `depth` levels."""
    entries = []
    try:
        items = sorted(folder.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
    except PermissionError:
        return entries
    SKIP = {'.git', '__pycache__', '.vscode', 'node_modules', '.mypy_cache'}
    for item in items:
        if item.name.startswith('.') and item.name not in ('.vscode',):
            if item.name in SKIP:
                continue
        if item.name in SKIP:
            continue
        rel_path = f"{rel_prefix}/{item.name}" if rel_prefix else item.name
        if item.is_dir() and depth > 0:
            entries.append({
                "name":     item.name,
                "type":     "dir",
            "path":     rel_path,
            "children": _dir_entries(item, depth - 1, rel_path),
            })
        elif item.is_file():
          entries.append({
            "name": item.name,
            "type": "file",
            "path": rel_path,
            "size": item.stat().st_size,
          })
    return entries


def fs_list() -> dict:
      return {"entries": _dir_entries(PROJECT_ROOT), "cwd": str(PROJECT_ROOT)}


def fs_read(rel: str) -> dict:
    p = _safe_project_path(rel)
    if p is None:
        return {"error": "forbidden"}
    if not p.exists():
        return {"error": "not found"}
    try:
        content = p.read_text(encoding="utf-8", errors="replace")
        return {"path": rel, "content": content}
    except Exception as e:
        return {"error": str(e)}


def fs_write(rel: str, content: str) -> dict:
    p = _safe_project_path(rel)
    if p is None:
        return {"error": "forbidden"}
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return {"ok": True}
    except Exception as e:
        return {"error": str(e)}


def fs_mkdir(rel: str) -> dict:
    p = _safe_project_path(rel)
    if p is None:
        return {"error": "forbidden"}
    try:
        p.mkdir(parents=True, exist_ok=True)
        return {"ok": True}
    except Exception as e:
        return {"error": str(e)}


def fs_delete(rel: str) -> dict:
    p = _safe_project_path(rel)
    if p is None:
        return {"error": "forbidden"}
    if not p.exists():
        return {"error": "not found"}
    try:
        if p.is_dir():
            import shutil
            shutil.rmtree(p)
        else:
            p.unlink()
        return {"ok": True}
    except Exception as e:
        return {"error": str(e)}


def fs_rename(from_rel: str, to_rel: str) -> dict:
    src = _safe_project_path(from_rel)
    dst = _safe_project_path(to_rel)
    if src is None or dst is None:
        return {"error": "forbidden"}
    if not src.exists():
        return {"error": "source not found"}
    try:
      dst.parent.mkdir(parents=True, exist_ok=True); src.rename(dst); return {"ok": True}
    except Exception as e:
        return {"error": str(e)}


def fs_cwd() -> dict:
    return {"cwd": str(PROJECT_ROOT)}


def fs_chdir(path: str) -> dict:
    global PROJECT_ROOT
    try:
        p = Path(path).expanduser().resolve()
    except Exception as e:
        return {"error": str(e)}
    if not p.exists():
        return {"error": f"Path not found: {path}"}
    if not p.is_dir():
        return {"error": f"Not a directory: {path}"}
    PROJECT_ROOT = p
    return {"ok": True, "cwd": str(PROJECT_ROOT)}


# ── Git API ───────────────────────────────────────────────────────────────────

def _parse_git_porcelain(output: str) -> dict:
  """Parse `git status --porcelain=v1 --branch` output into structured fields."""
  branch = ""
  ahead = 0
  behind = 0
  changed = []
  for raw in output.splitlines():
    line = raw.rstrip("\n")
    if not line:
      continue
    if line.startswith("## "):
      branch = line[3:]
      m_ahead = re.search(r"ahead (\d+)", branch)
      m_behind = re.search(r"behind (\d+)", branch)
      ahead = int(m_ahead.group(1)) if m_ahead else 0
      behind = int(m_behind.group(1)) if m_behind else 0
      continue
    if len(line) < 4:
      continue
    x = line[0]
    y = line[1]
    path = line[3:]
    if " -> " in path:
      path = path.split(" -> ", 1)[1]
    staged = x != " " and x != "?"
    unstaged = y != " "
    untracked = x == "?" and y == "?"
    changed.append({
      "path": path,
      "xy": f"{x}{y}",
      "staged": staged,
      "unstaged": unstaged,
      "untracked": untracked,
    })
  return {
    "branch": branch,
    "ahead": ahead,
    "behind": behind,
    "changed": changed,
  }


def git_status() -> dict:
  try:
    t0 = time.time()
    proc_short = subprocess.run(
      ["git", "status", "--porcelain=v1", "--branch"],
      cwd=str(PROJECT_ROOT),
      capture_output=True,
      text=True,
      timeout=5,
      stdin=subprocess.DEVNULL,
      creationflags=0,
    )
    proc_human = subprocess.run(
      ["git", "status"],
      cwd=str(PROJECT_ROOT),
      capture_output=True,
      text=True,
      timeout=5,
      stdin=subprocess.DEVNULL,
      creationflags=0,
    )
    elapsed = time.time() - t0
    if elapsed > 1.0:
      _log(f"git status took {elapsed:.2f}s")

    short_output = proc_short.stdout + proc_short.stderr
    output = proc_human.stdout + proc_human.stderr
    parsed = _parse_git_porcelain(short_output) if proc_short.returncode == 0 else {
      "branch": "",
      "ahead": 0,
      "behind": 0,
      "changed": [],
    }
    return {
      "output": output,
      "short_output": short_output,
      "parsed": parsed,
      "exit_code": proc_human.returncode,
    }
  except FileNotFoundError:
    return {"error": "git not found \u2014 is Git installed?"}
  except Exception as e:
    return {"error": str(e)}


def git_run(args: list) -> dict:
    """Run a git command in the project root. args = list of strings after 'git'."""
    ALLOWED = {"add", "commit", "push", "pull", "fetch", "status", "log",
                "diff", "stash", "checkout", "branch", "reset", "init"}
    if not args or args[0] not in ALLOWED:
        return {"error": f"git command '{args[0] if args else ''}' not allowed"}
    try:
        proc = subprocess.run(
            ["git"] + args,
            cwd=str(PROJECT_ROOT),
            capture_output=True, text=True, timeout=60,
            stdin=subprocess.DEVNULL,
            creationflags=0,
        )
        output = proc.stdout + proc.stderr
        return {"output": output, "exit_code": proc.returncode}
    except FileNotFoundError:
        return {"error": "git not found"}
    except subprocess.TimeoutExpired:
        return {"error": "git command timed out"}
    except Exception as e:
        return {"error": str(e)}


# ── IDE completions ────────────────────────────────────────────────────────────

def get_ide_completions() -> list:
    """Build completion list from all extension sources and pattern library."""
    import re as _re
    items: list = []
    ext_root = CACHE_ROOT / "vscode-extension-data"
    jyaoma   = ext_root / "jyaoma"

    def _load_json(path: Path) -> object:
        text = path.read_text(encoding="utf-8", errors="replace")
        # Strip single-line comments (JSONC support)
        text = _re.sub(r"//[^\n]*", "", text)
        return json.loads(text)

    def _snippet_body(body) -> str:
        if isinstance(body, list):
            return "\n".join(body)
        return str(body or "")

    # ── jyaoma: Functions ────────────────────────────────────────────────────
    fn_path = jyaoma / "functions.json"
    if fn_path.exists():
        try:
            raw = _load_json(fn_path)
            if isinstance(raw, dict):
                for name, info in raw.items():
                    if not isinstance(info, dict):
                        continue
                    sig  = info.get("signature") or info.get("insertText") or name
                    desc = info.get("description") or info.get("documentation") or ""
                    items.append({"label": name, "kind": "function", "signature": sig,
                                  "description": desc[:200], "snippet": sig})
        except Exception:
            pass

    # ── jyaoma: Events ───────────────────────────────────────────────────────
    ev_path = jyaoma / "events.json"
    if ev_path.exists():
        try:
            raw = _load_json(ev_path)
            if isinstance(raw, dict):
                for name, info in raw.items():
                    if not isinstance(info, dict):
                        continue
                    items.append({"label": name, "kind": "event",
                                  "signature": info.get("insertText") or name,
                                  "description": "", "snippet": info.get("insertText") or name})
        except Exception:
            pass

    # ── jyaoma: Constants ────────────────────────────────────────────────────
    const_path = jyaoma / "constants.json"
    if const_path.exists():
        try:
            raw = _load_json(const_path)
            if isinstance(raw, dict):
                for name, info in raw.items():
                    if not isinstance(info, dict):
                        info = {}
                    items.append({"label": name, "kind": "constant",
                                  "signature": "", "description": str(info.get("value", "")),
                                  "snippet": name})
        except Exception:
            pass

    # ── jyaoma: Snippets ─────────────────────────────────────────────────────
    snip_path = jyaoma / "snippets.json"
    if snip_path.exists():
        try:
            raw = _load_json(snip_path)
            if isinstance(raw, dict):
                for name, info in raw.items():
                    if not isinstance(info, dict):
                        continue
                    prefix = info.get("prefix") or name
                    body   = _snippet_body(info.get("body", ""))
                    desc   = info.get("description") or ""
                    if body:
                        items.append({"label": prefix, "kind": "snippet",
                                      "signature": name, "description": desc,
                                      "snippet": body})
        except Exception:
            pass

    # ── buildersbrewery: Snippets (skip single-token constants) ──────────────
    bb_path = ext_root / "buildersbrewery" / "lsl.json"
    if bb_path.exists():
        try:
            raw = _load_json(bb_path)
            lsl = raw.get("lsl", {}) if isinstance(raw, dict) else {}
            for name, info in lsl.items():
                if not isinstance(info, dict):
                    continue
                body = _snippet_body(info.get("body", ""))
                # Only include entries whose body is richer than a bare identifier
                if not body or body.strip() == name.strip():
                    continue
                prefix = info.get("prefix") or name
                desc   = info.get("description") or ""
                items.append({"label": prefix, "kind": "snippet",
                              "signature": name, "description": desc,
                              "snippet": body})
        except Exception:
            pass

    # ── Pattern library: idioms, patterns, anti-patterns ─────────────────────
    patterns_root = CACHE_ROOT / "patterns"
    if patterns_root.exists():
        for category in ("idioms", "patterns", "anti-patterns"):
            cat_dir = patterns_root / category
            if not cat_dir.exists():
                continue
            for md in sorted(cat_dir.glob("*.md")):
                try:
                    text = md.read_text(encoding="utf-8", errors="replace")
                    # Extract front-matter name
                    label = md.stem.replace("-", " ").title()
                    if text.startswith("---"):
                        end = text.find("---", 3)
                        if end > 0:
                            for line in text[3:end].splitlines():
                                if line.startswith("name:"):
                                    label = line.split(":", 1)[1].strip().strip('"\'')
                                    break
                    # Extract code block from ## Code section
                    m = _re.search(r"## Code\n+```(?:lsl|lua)?\n(.*?)```", text, _re.DOTALL)
                    if not m:
                        continue
                    code = m.group(1).rstrip()
                    if code:
                        items.append({"label": label, "kind": "snippet",
                                      "signature": f"{category}/{md.stem}",
                                      "description": f"LSL {category[:-1]}", "snippet": code})
                except Exception:
                    pass

    return items


# ── Cache management ─────────────────────────────────────────────────────────

MANIFEST_PATH = CACHE_BASE / "cache-manifest.json"


def _find_bash() -> list[str]:
  """Return a bash command prefix suitable for the current platform.

  On Windows: tries Git Bash locations, then falls back to WSL bash.
  On other platforms: returns ["bash"].
  """
  if sys.platform != "win32":
    return ["bash"]
  candidates = [
    r"C:\Program Files\Git\bin\bash.exe",
    r"C:\Program Files (x86)\Git\bin\bash.exe",
  ]
  import shutil
  git = shutil.which("git")
  if git:
    git_bash = str(Path(git).parent / "bash.exe")
    candidates.insert(0, git_bash)
  for c in candidates:
    if Path(c).exists():
      return [c, "--login"]
  return ["bash"]


def _bash_script_cmd(script_path: Path) -> list[str]:
    """Build a cross-platform bash command for a script path."""
    prefix = _find_bash()
    script = str(script_path).replace("\\", "/")
    return prefix + [script]


def _skill_cmd(name: str) -> list[str]:
    """Command to invoke a bundled skill via the exe's run-skill subcommand."""
    return [sys.executable, "run-skill", name]


CACHE_TOOLS = [
    {
        "id":          "analyse-snippets",
        "name":        "Analyse Snippets",
        "description": "Rebuild the pattern library (idioms, patterns, anti-patterns, "
                       "function-usage notes) from all extension snippet files.",
        "cmd":         _skill_cmd("analyse-snippets"),
        "options":     [],
        "note":        None,
        "web":         False,
    },
    {
        "id":          "generate-docs",
        "name":        "Generate Docs from Cache",
        "description": "Synthesise missing function and event doc files from local "
                       "jyaoma, pyoptimizer, and makopo data. No web requests.",
        "cmd":         _skill_cmd("generate-docs-from-cache"),
        "options": [
            {"flag": "--type",  "label": "Type",            "type": "select",
             "choices": ["all", "functions", "events"],     "default": "all"},
            {"flag": "--force", "label": "Force overwrite", "type": "bool", "default": False},
        ],
        "note": None,
        "web":  False,
    },
    {
        "id":          "scrape-wiki",
        "name":        "Scrape Wiki Pages",
        "description": "Fetch Caveats, Examples, Notes, and See Also sections from the "
                       "SL wiki and merge into existing cache docs.",
        "cmd":         _skill_cmd("scrape-wiki-pages"),
        "options": [
            {"flag": "--type",  "label": "Type",       "type": "select",
             "choices": ["all", "functions", "events"], "default": "all"},
            {"flag": "--limit", "label": "Page limit",  "type": "number", "default": ""},
        ],
        "note": "Requires internet access.",
        "web":  True,
    },
    {
        "id":          "scrape-library",
        "name":        "Scrape LSL Library",
        "description": "Fetch script examples from the SL wiki LSL Library category "
                       "and save to the examples cache.",
        "cmd":         _skill_cmd("scrape-lsl-library"),
        "options": [
            {"flag": "--limit",  "label": "Page limit",         "type": "number", "default": ""},
            {"flag": "--resume", "label": "Resume from last run","type": "bool",   "default": False},
        ],
        "note": "Requires internet access.",
        "web":  True,
    },
    {
        "id":          "update-extension-data",
        "name":        "Update Extension Data",
        "description": "Fetch the latest language data from all five GitHub sources "
                       "(jyaoma, kwdb, pyoptimizer, makopo, buildersbrewery) then re-run snippet analysis.",
        "cmd":         _bash_script_cmd(BUNDLED_SKILLS_PATH / "update-extension-data.sh"),
        "options":     [],
        "note":        "Requires bash and curl. On Windows, Git Bash is used automatically if installed.",
        "web":         True,
    },
    {
        "id":          "cache-repair",
        "name":        "Cache Repair",
        "description": "Auto-repair common front matter issues: fill empty descriptions, "
                       "infer missing type/language, construct missing wiki_url fields.",
        "cmd":         _skill_cmd("lsl-cache-repair"),
        "options": [
            {"flag": "--dry-run",  "label": "Dry run (preview only)", "type": "bool",   "default": False},
            {"flag": "--category", "label": "Category",               "type": "select",
             "choices": ["all", "functions", "events", "constants", "examples", "tutorials", "ossl", "slua"],
             "default": "all"},
        ],
        "note": None,
        "web":  False,
    },
    {
        "id":          "full-update",
        "name":        "Full Cache Update",
        "description": "Run all local update steps in order: generate missing docs, "
                       "repair front matter, rebuild pattern library. No web requests.",
        "cmd":         _skill_cmd("cache-full-update"),
        "options": [
            {"flag": "--skip-docs",     "label": "Skip doc generation", "type": "bool", "default": False},
            {"flag": "--skip-repair",   "label": "Skip repair step",    "type": "bool", "default": False},
            {"flag": "--skip-patterns", "label": "Skip pattern rebuild","type": "bool", "default": False},
        ],
        "note": None,
        "web":  False,
    },
    {
        "id":          "fetch-ossl",
        "name":        "Fetch OSSL Docs",
        "description": "Generate OSSL function docs from the opensim/opensim GitHub repository "
                       "(IOSSL_Api.cs + OSSL_Api.cs). Includes function signatures, "
                       "//ApiDesc descriptions, and threat levels. Cross-references local "
                       "kwdb and makopo for parameter names and timing data.",
        "cmd":         _skill_cmd("fetch-ossl-from-github"),
        "options": [
            {"flag": "--force", "label": "Force overwrite", "type": "bool", "default": False},
        ],
        "note": "Source: opensim/opensim on GitHub. No opensimulator.org wiki requests.",
        "web":  True,
    },
    {
        "id":          "fetch-slua",
        "name":        "Fetch SLua Docs",
        "description": "Download SLua scripting documentation from wiki.secondlife.com "
                       "to the active cache lsl-docs/slua/.",
        "cmd":         _skill_cmd("fetch-slua-docs"),
        "options": [
            {"flag": "--force", "label": "Force overwrite", "type": "bool", "default": False},
        ],
        "note": "Requires internet access. SLua wiki coverage may be sparse.",
        "web":  True,
    },
    {
        "id":          "generate-ossl-from-kwdb",
        "name":        "Generate OSSL Docs (Local)",
        "description": "Generate OSSL function docs from locally cached kwdb.xml and makopo "
                       "data — no internet required. Creates 241 function docs in lsl-docs/ossl/.",
        "cmd":         _skill_cmd("generate-ossl-from-kwdb"),
        "options": [
            {"flag": "--force", "label": "Force overwrite", "type": "bool", "default": False},
        ],
        "note": "Uses locally cached kwdb.xml (241 functions) + makopo tooltip data.",
        "web":  False,
    },
    {
        "id":          "fetch-extra-libraries",
        "name":        "Fetch Extra Script Libraries",
        "description": "Download LSL script examples from GitHub repos, web libraries, and "
                       "the OpenSimulator script library wiki. Sources: Outworldz (web + GitHub), "
                       "AbsolutelyCraiCrai, AvaCon OpenSim, opensimulator.org/wiki/OSSL_Script_Library. "
                       "Deduplicates against existing examples by filename and content hash.",
        "cmd":         _skill_cmd("fetch-extra-libraries"),
        "options": [
            {"flag": "--force",  "label": "Force overwrite",  "type": "bool",   "default": False},
            {"flag": "--limit",  "label": "Files per source", "type": "number", "default": ""},
            {"flag": "--source", "label": "Source ID filter", "type": "text",
             "default": "",
             "hint":  "Leave blank for all. IDs: outworldz-web, absolutelycraicrai, outworldz-github, avacon-opensim, opensim-script-library"},
        ],
        "note": "Requires internet access. GitHub API rate limit: 60 req/hr unauthenticated.",
        "web":  True,
    },
    {
        "id":          "clear-runtime-cache",
        "name":        "Clear Runtime Cache",
        "description": "Remove the persistent extraction cache so SLCode fully "
                       "re-extracts on next launch. Use this after an update if "
                       "the app fails to start, or to reclaim disk space.",
        "cmd":         _skill_cmd("clear-runtime-cache"),
        "options":     [],
        "note":        "SLCode will re-extract (~5-10 s) on the next launch.",
        "web":         False,
    },
    {
        "id":          "sync-seed-cache",
        "name":        "Sync Bundled Cache",
        "description": "Copy any files from the bundled seed cache that are missing "
                       "from the runtime cache. Use this if examples or docs are "
                       "missing after installing a new version.",
        "cmd":         _skill_cmd("sync-seed-cache"),
        "options":     [],
        "note":        "Safe to run any time — only adds missing files, never overwrites.",
        "web":         False,
    },
]

_jobs:       dict = {}
_jobs_lock           = threading.Lock()
_active_job: str | None = None


def start_job(cmd: list) -> str:
  """Launch a subprocess, buffer stdout+stderr, return job ID."""
  job_id = uuid.uuid4().hex[:8]
  lines: deque = deque(maxlen=4000)
  with _jobs_lock:
    _jobs[job_id] = {"lines": lines, "done": False, "exit_code": None, "proc": None}

  def _run():
    try:
      env = os.environ.copy()
      env["LSL_CACHE_BASE"] = str(CACHE_BASE)
      # Inject saved GitHub token so skill scripts can use it without extra flags
      if "GITHUB_TOKEN" not in env and _GH_TOKEN_FILE.exists():
          try:
              tok = _GH_TOKEN_FILE.read_text(encoding="utf-8").strip()
              if tok:
                  env["GITHUB_TOKEN"] = tok
          except Exception:
              pass
      proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        stdin=subprocess.DEVNULL,
        text=True,
        encoding="utf-8",
        errors="replace",
        creationflags=0,
        env=env,
      )
      with _jobs_lock:
        _jobs[job_id]["proc"] = proc
      for line in proc.stdout:
        with _jobs_lock:
          lines.append(line.rstrip("\n"))
      proc.wait()
      with _jobs_lock:
        _jobs[job_id]["done"] = True
        _jobs[job_id]["exit_code"] = proc.returncode
    except Exception as exc:
      with _jobs_lock:
        lines.append(f"[ERROR] {exc}")
        _jobs[job_id]["done"] = True
        _jobs[job_id]["exit_code"] = -1

  threading.Thread(target=_run, daemon=True).start()
  return job_id


# GitHub token file — stored in the cache root, never inside lsl-docs
_GH_TOKEN_FILE = CACHE_BASE / ".gh-token"


def _gh_token_status() -> dict:
    """Return current token info without exposing the full value."""
    tok = os.environ.get("GITHUB_TOKEN", "").strip()
    source = "env"
    if not tok and _GH_TOKEN_FILE.exists():
        try:
            tok    = _GH_TOKEN_FILE.read_text(encoding="utf-8").strip()
            source = "file"
        except Exception:
            tok = ""
    if not tok:
        return {"set": False, "masked": None, "source": None}
    masked = (tok[:4] + "…" + tok[-4:]) if len(tok) > 8 else "***"
    return {"set": True, "masked": masked, "source": source}


def _clear_runtime_cache_skill() -> int:
    """Delete the extracted SLCode-app dir and mtime file so the next launch
    triggers a fresh extraction from SLCode-app.zip."""
    import shutil as _shutil
    local = os.environ.get("LOCALAPPDATA", "")
    if not local:
        print("clear-runtime-cache: LOCALAPPDATA not set", flush=True)
        return 1
    slcode_dir  = Path(local) / "SLCode"
    app_dir     = slcode_dir / "SLCode-app"
    did_something = False
    if app_dir.exists():
        try:
            _shutil.rmtree(str(app_dir))
            print(f"Removed {app_dir}", flush=True)
            did_something = True
        except Exception as e:
            print(f"clear-runtime-cache: could not remove {app_dir}: {e}", flush=True)
            return 1
    if did_something:
        print("SLCode will re-extract on next launch.", flush=True)
    else:
        print("No runtime cache found (already cleared).", flush=True)
    return 0


def _sync_seed_cache_skill() -> int:
    """Copy files present in the bundled seed cache but missing from the runtime cache."""
    import shutil as _shutil
    src = BUNDLED_CACHE_BASE
    dst = CACHE_BASE
    if src.resolve() == dst.resolve():
        print("Dev mode: runtime cache and seed cache are the same — nothing to sync.", flush=True)
        return 0
    if not src.exists():
        print(f"sync-seed-cache: bundled cache not found at {src}", flush=True)
        return 1
    all_files = [f for f in src.rglob("*") if f.is_file()]
    total   = len(all_files)
    copied  = 0
    skipped = 0
    errors  = 0
    print(f"Seed cache : {src}", flush=True)
    print(f"Runtime    : {dst}", flush=True)
    print(f"Scanning {total} bundled files...", flush=True)
    for src_file in all_files:
        rel      = src_file.relative_to(src)
        dst_file = dst / rel
        dst_file.parent.mkdir(parents=True, exist_ok=True)
        try:
            if not dst_file.exists():
                _shutil.copy2(src_file, dst_file)
                copied += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"  ERROR: {rel}: {e}", flush=True)
            errors += 1
        done = copied + skipped + errors
        if done % 200 == 0 or done == total:
            print(f"  {done}/{total} checked, {copied} copied...", end="\r", flush=True)
    print(f"  {total}/{total} checked, {copied} copied.            ", flush=True)
    print(f"Done: {copied} new files synced, {skipped} already present, {errors} errors.", flush=True)
    return 0 if errors == 0 else 1


def run_skill_cmd(skill_name: str, extra_args: list[str]) -> int:
    """Run a bundled skill script via runpy using the embedded Python runtime.

    Used when the exe is invoked as: SLCode run-skill <name> [args...]
    Prefers the _MEIPASS copy (always present) over the persistent cache copy.
    """
    # Built-in skills that don't need a separate .py file
    if skill_name == "clear-runtime-cache":
        return _clear_runtime_cache_skill()
    if skill_name == "sync-seed-cache":
        return _sync_seed_cache_skill()

    import runpy as _runpy
    candidates = [
        BUNDLED_SKILLS_PATH / f"{skill_name}.py",
        SKILLS_PATH / f"{skill_name}.py",
    ]
    script = next((c for c in candidates if c.exists()), None)
    if script is None:
        print(f"run-skill: skill '{skill_name}' not found (searched {[str(c) for c in candidates]})", flush=True)
        return 1
    old_argv = sys.argv[:]
    old_env_cache = os.environ.get("LSL_CACHE_BASE")
    os.environ["LSL_CACHE_BASE"] = str(CACHE_BASE)
    try:
        sys.argv = [str(script)] + extra_args
        _runpy.run_path(str(script), run_name="__main__")
        return 0
    except SystemExit as e:
        return e.code if isinstance(e.code, int) else 0
    except Exception as e:
        print(f"run-skill: {skill_name} raised {e}", flush=True)
        return 1
    finally:
        sys.argv = old_argv
        if old_env_cache is None:
            os.environ.pop("LSL_CACHE_BASE", None)
        else:
            os.environ["LSL_CACHE_BASE"] = old_env_cache


def get_cache_status() -> dict:
    """Return manifest data plus per-category doc file counts."""
    manifest = {}
    if MANIFEST_PATH.exists():
        try:
            manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass

    counts = {}
    for cat, folder in CATEGORIES.items():
        if not folder.exists():
            counts[cat] = 0
            continue
        if cat == "reference":
            counts[cat] = len([p for p in folder.glob("*.md")
                               if p.name not in REFERENCE_SKIP])
        else:
            counts[cat] = len(list(folder.rglob("*.md")))

    # Derive core/ossl/slua presence from actual files if manifest doesn't say so
    secs = manifest.setdefault("sections", {})
    core_count = counts.get("functions", 0) + counts.get("events", 0) + counts.get("constants", 0)
    if not secs.get("core") and core_count > 0:
        secs["core"] = True
    if not secs.get("ossl") and counts.get("ossl", 0) > 0:
        secs["ossl"] = True
    if not secs.get("slua") and counts.get("slua", 0) > 0:
        secs["slua"] = True

    return {"manifest": manifest, "doc_counts": counts, "total": sum(counts.values())}


def get_doc_gaps() -> dict:
    """Compare jyaoma functions.json against cached .md files to find missing/stub docs."""
    result: dict = {"missing": [], "stub": [], "total_known": 0, "total_cached": 0}
    jyaoma_path = CACHE_ROOT / "vscode-extension-data" / "jyaoma" / "functions.json"
    if not jyaoma_path.exists():
        result["error"] = "jyaoma/functions.json not found"
        return result
    try:
        raw = json.loads(jyaoma_path.read_text(encoding="utf-8", errors="replace"))
    except Exception as e:
        result["error"] = str(e)
        return result
    if isinstance(raw, dict):
        all_funcs = list(raw.keys())
    elif isinstance(raw, list):
        all_funcs = [f.get("name", "") for f in raw if isinstance(f, dict)]
    else:
        result["error"] = "Unexpected functions.json format"
        return result
    result["total_known"] = len(all_funcs)
    funcs_dir    = CACHE_ROOT / "functions"
    cached_names = {p.stem.lower() for p in funcs_dir.glob("*.md")} if funcs_dir.exists() else set()
    result["total_cached"] = len(cached_names)
    for fn in all_funcs:
        if not fn:
            continue
        if fn.lower() not in cached_names:
            result["missing"].append(fn)
        else:
            md_path = funcs_dir / f"{fn}.md"
            if md_path.exists():
                try:
                    text = md_path.read_text(encoding="utf-8", errors="replace")
                    _, body = parse_front_matter(text)
                    if len(body.strip()) < 150:
                        result["stub"].append(fn)
                except Exception:
                    pass
    return result


def validate_cache_frontmatter() -> dict:
    """Check all .md files for required YAML front matter fields.

    Pattern files (idioms, patterns, anti-patterns, function-usage) require only
    name and category — they don't have wiki_url, type, or language fields.
    All other doc files require the full set.
    """
    REQUIRED_DOC     = ["name", "category", "type", "language", "description", "wiki_url"]
    REQUIRED_PATTERN = ["name", "category"]
    PATTERN_CATS     = {"idioms", "patterns", "anti-patterns", "function-usage"}

    issues:  list = []
    checked: int  = 0
    for cat, folder in CATEGORIES.items():
        if not folder.exists():
            continue
        pat = folder.glob("*.md") if cat == "reference" else folder.rglob("*.md")
        for md_path in pat:
            if md_path.name in REFERENCE_SKIP:
                continue
            checked += 1
            try:
                text  = md_path.read_text(encoding="utf-8", errors="replace")
                fm, _ = parse_front_matter(text)
                # Determine which field set applies
                rel     = md_path.relative_to(CACHE_ROOT).as_posix()
                parts   = rel.split("/")
                subcat  = parts[1] if len(parts) >= 2 else ""
                is_pat  = cat == "patterns" and subcat in PATTERN_CATS
                req     = REQUIRED_PATTERN if is_pat else REQUIRED_DOC
                # source_url (GitHub/web fetch) is accepted as equivalent to wiki_url
                missing = [
                    f for f in req
                    if f not in fm or not fm[f]
                    if not (f == "wiki_url" and fm.get("source_url"))
                ]
                if missing:
                    issues.append({"path": rel, "missing": missing, "has_fm": bool(fm)})
            except Exception as e:
                rel = md_path.relative_to(CACHE_ROOT).as_posix()
                issues.append({"path": rel, "missing": ["(read error)"], "has_fm": False})
    return {"issues": issues, "checked": checked, "ok": checked - len(issues)}


def get_disk_usage() -> dict:
    """Return size in bytes for each top-level entry in the cache directory."""
    cache_root = CACHE_BASE
    if not cache_root.exists():
        return {"error": "Cache root not found"}
    dirs:  dict = {}
    total: int  = 0
    for entry in sorted(cache_root.iterdir()):
        if entry.is_dir():
            size = sum(f.stat().st_size for f in entry.rglob("*") if f.is_file())
        else:
            try:
                size = entry.stat().st_size
            except OSError:
                size = 0
        dirs[entry.name] = size
        total += size
    return {"dirs": dirs, "total": total, "total_kb": round(total / 1024, 1)}


def get_reconciliation() -> dict:
    """Read and parse RECONCILIATION.md discrepancy table."""
    path = CACHE_ROOT / "vscode-extension-data" / "RECONCILIATION.md"
    if not path.exists():
        return {"error": "RECONCILIATION.md not found", "rows": []}
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return {"error": str(e), "rows": []}
    rows        = []
    header_done = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith('|') and '---' not in stripped:
            cells = [c.strip() for c in stripped.strip('|').split('|')]
            if not header_done:
                header_done = True
                continue
            if len(cells) >= 2:
                rows.append(cells)
    return {"rows": rows, "count": len(rows), "preview": text[:3000]}


def get_pattern_tags() -> dict:
    """Build a tag → pattern list index from all pattern files."""
    patterns_dir = CACHE_ROOT / "patterns"
    if not patterns_dir.exists():
        return {"error": "patterns/ directory not found", "tags": {}}
    tag_map: dict = {}
    count:   int  = 0
    for md_path in patterns_dir.rglob("*.md"):
        if md_path.name == "README.md":
            continue
        try:
            text = md_path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        fm, _ = parse_front_matter(text)
        name  = fm.get("name", md_path.stem)
        raw_tags = fm.get("tags", "")
        if raw_tags.startswith('['):
            tags = [t.strip().strip('"\'') for t in raw_tags.strip('[]').split(',') if t.strip()]
        else:
            tags = [t.strip() for t in raw_tags.split(',') if t.strip()]
        for tag in tags:
            tag_map.setdefault(tag, []).append({
                "name":     name,
                "path":     md_path.relative_to(CACHE_ROOT).as_posix(),
                "category": fm.get("category", ""),
            })
        count += 1
    for tag in tag_map:
        tag_map[tag].sort(key=lambda x: x["name"])
    return {
        "tags":      dict(sorted(tag_map.items())),
        "count":     count,
        "tag_count": len(tag_map),
    }


# ── Front matter parser ──────────────────────────────────────────────────────

def parse_front_matter(text: str) -> tuple[dict, str]:
    """Extract YAML-like front matter and return (fields, body)."""
    fields = {}
    body   = text
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", text, re.DOTALL)
    if not m:
        return fields, body
    raw_fm, body = m.group(1), m.group(2)
    for line in raw_fm.splitlines():
        kv = re.match(r'^(\w+):\s*(.*)', line)
        if kv:
            key, val = kv.group(1), kv.group(2).strip().strip('"')
            fields[key] = val
    return fields, body


# ── Indexer ──────────────────────────────────────────────────────────────────

INDEX: list[dict] = []

def build_index(force: bool = False):
    """Walk all .md files in the cache and build an in-memory search index.
    If force=False and the index is already populated, this is a no-op."""
    global INDEX
    if not force and INDEX:
        return
    INDEX = []
    t0 = time.time()
    _log(f"build_index: scanning {CACHE_ROOT} …")
    for cat, folder in CATEGORIES.items():
        if not folder.exists():
            _log(f"  category '{cat}' folder missing: {folder}")
            continue

        if cat == "reference":
            # Only index root-level .md files (non-recursive), skipping meta files
            md_files = [p for p in folder.glob("*.md") if p.name not in REFERENCE_SKIP]
        else:
            md_files = list(folder.rglob("*.md"))

        for md_path in md_files:
            # Skip hidden directories (e.g. .versions/ sidecars)
            if any(part.startswith('.') for part in md_path.relative_to(folder).parts):
                continue
            # Skip pattern library index
            if md_path.name == "README.md" and cat == "patterns":
                continue
            try:
                text = md_path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            fm, body = parse_front_matter(text)
            rel = md_path.relative_to(CACHE_ROOT).as_posix()
            # Determine subcategory for pattern files
            display_cat = cat
            if cat == "patterns":
                parts = rel.split("/")
                if len(parts) >= 2:
                    display_cat = parts[1]  # idioms / patterns / anti-patterns / function-usage
            INDEX.append({
                "path":        rel,
                "category":    display_cat,
                "name":        fm.get("name", md_path.stem),
                "description": fm.get("description", ""),
                "signature":   fm.get("signature", ""),
                "return_type": fm.get("return_type", ""),
                "sleep_time":  fm.get("sleep_time", ""),
                "energy_cost": fm.get("energy_cost", ""),
                "wiki_url":         fm.get("wiki_url", ""),
                "source_url":        fm.get("source_url", ""),
                "source_doc_kind":   fm.get("source_doc_kind", ""),
                "source_project":    fm.get("source_project", ""),
                "source_part_index": fm.get("source_part_index", ""),
                "source_part_total": fm.get("source_part_total", ""),
                "tags":        fm.get("tags", ""),
                "deprecated":  fm.get("deprecated", ""),
                "language":    fm.get("language", ""),
                "has_versions":  fm.get("has_versions", ""),
                "active_version": fm.get("active_version", ""),
                "custom":        fm.get("custom", ""),
                "body":        body[:2000],  # keep a snippet for content search
            })
    by_cat = {}
    for d in INDEX:
        by_cat.setdefault(d["category"], 0)
        by_cat[d["category"]] += 1
    summary = ", ".join(f"{v} {k}" for k, v in sorted(by_cat.items()))
    _log(f"build_index: {len(INDEX)} docs in {time.time()-t0:.2f}s ({summary})")


def index_one_file(doc_path: Path):
    """Rebuild the INDEX entry for a single file (used after version switches)."""
    global INDEX
    rel = doc_path.relative_to(CACHE_ROOT).as_posix()
    try:
        text = doc_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return
    fm, body = parse_front_matter(text)
    cat = fm.get("category", "examples")
    INDEX = [d for d in INDEX if d["path"] != rel]
    INDEX.append({
        "path":          rel,
        "category":      cat,
        "name":          fm.get("name", doc_path.stem),
        "description":   fm.get("description", ""),
        "signature":     fm.get("signature", ""),
        "return_type":   fm.get("return_type", ""),
        "sleep_time":    fm.get("sleep_time", ""),
        "energy_cost":   fm.get("energy_cost", ""),
        "wiki_url":           fm.get("wiki_url", ""),
        "source_url":         fm.get("source_url", ""),
        "source_doc_kind":    fm.get("source_doc_kind", ""),
        "source_project":     fm.get("source_project", ""),
        "source_part_index":  fm.get("source_part_index", ""),
        "source_part_total":  fm.get("source_part_total", ""),
        "has_versions":       fm.get("has_versions", ""),
        "active_version":     fm.get("active_version", ""),
        "custom":             fm.get("custom", ""),
        "tags":          fm.get("tags", ""),
        "deprecated":    fm.get("deprecated", ""),
        "language":      fm.get("language", ""),
        "body":          body[:2000],
    })


# ── Search ───────────────────────────────────────────────────────────────────

CATEGORY_ALIASES = {
    "function-usage": ["function-usage"],
    "anti-patterns":  ["anti-patterns"],
    "idioms":         ["idioms"],
    "patterns":       ["patterns"],
    "functions":      ["functions"],
    "events":         ["events"],
    "constants":      ["constants"],
    "tutorials":      ["tutorials"],
}

def search(query: str, category: str = "all") -> list[dict]:
    q = query.lower().strip()
    results = []
    for doc in INDEX:
        # Category filter
        if category != "all":
            if doc["category"] != category:
                continue
        # Score
        score = 0
        name_lower = doc["name"].lower()
        if q:
            if name_lower == q:
                score += 100
            elif name_lower.startswith(q):
                score += 50
            elif q in name_lower:
                score += 20
            if q in doc["description"].lower():
                score += 10
            if q in doc["signature"].lower():
                score += 8
            if q in doc["tags"].lower():
                score += 5
            if q in doc["body"].lower():
                score += 2
            if score == 0:
                continue  # no match
        else:
            score = 1  # browse mode — return all

        results.append({**doc, "_score": score})

    results.sort(key=lambda x: (-x["_score"], x["name"].lower()))
    for r in results:
        del r["body"]
    return results


def lookup_cache_doc(name: str) -> dict:
    """Exact-ish cache doc lookup by symbol name, returning front matter and body."""
    build_index()
    name = (name or "").strip()
    if not name:
        return {"error": "name required"}
    hit = None
    name_lower = name.lower()
    for doc in INDEX:
        if doc["name"] == name:
            hit = doc
            break
    if not hit:
        for doc in INDEX:
            if doc["name"].lower() == name_lower:
                hit = doc
                break
    if not hit:
        for doc in INDEX:
            if doc["name"].lower().startswith(name_lower):
                hit = doc
                break
    if not hit:
        return {"found": False}
    try:
        doc_path = (CACHE_ROOT / hit["path"]).resolve()
        if not str(doc_path).startswith(str(CACHE_ROOT.resolve())):
            return {"error": "forbidden"}
        text = doc_path.read_text(encoding="utf-8", errors="replace")
        fm, body = parse_front_matter(text)
        return {"found": True, "name": hit["name"], "path": hit["path"],
                "front_matter": fm, "body": body}
    except Exception:
        return {"found": True, "name": hit["name"], "path": hit["path"],
                "front_matter": hit, "body": ""}


# ── HTTP handler ─────────────────────────────────────────────────────────────

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>SLCode</title>
<script src="/marked.min.js"></script>
<style>
  :root {
    --bg:       #0f1117;
    --surface:  #1a1d27;
    --border:   #2a2d3e;
    --accent:   #4f8ef7;
    --accent2:  #7c6af7;
    --text:     #d4d8f0;
    --muted:    #7880a0;
    --warn:     #e8a44a;
    --danger:   #e85a5a;
    --green:    #4fc28a;
    --radius:   8px;
    --mono:     'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { height: 100%; }
  body { background: var(--bg); color: var(--text); font-family: system-ui, sans-serif;
         font-size: 14px; display: flex; flex-direction: column; }
  body.window-live-resize *, body.window-live-resize *::before, body.window-live-resize *::after {
    transition: none !important;
    animation: none !important;
    caret-color: transparent !important;
  }
  body.window-live-resize #search-dropdown,
  body.window-live-resize #ide-loading-overlay,
  body.window-live-resize #ide-loading-card,
  body.window-live-resize .tool-card,
  body.window-live-resize .analysis-card,
  body.window-live-resize #doc-body pre,
  body.window-live-resize #ext-nav {
    box-shadow: none !important;
    backdrop-filter: none !important;
  }
  body.window-live-resize .monaco-editor .minimap,
  body.window-live-resize .monaco-editor .decorationsOverviewRuler,
  body.window-live-resize .monaco-editor .scroll-decoration {
    opacity: 0 !important;
  }
  body.frameless { position: relative; overflow: hidden; }
  body.frameless:not(.window-maximized):not(.native-window-frame)::after {
    content: '';
    position: fixed;
    inset: 0;
    border: 1px solid var(--border);
    border-radius: 12px;
    box-shadow: inset 0 0 0 1px rgba(17, 17, 27, .35);
    pointer-events: none;
    z-index: 9999;
  }

  /* ── Frameless window controls ── */
  #window-bar { display: none !important; }
  #window-title { font-size: 12px; color: var(--text); font-weight: 500; white-space: nowrap;
                  flex: 1; text-align: center; }
  #window-controls { display: flex; gap: 2px; -webkit-app-region: no-drag; }
  .win-btn { width: 32px; height: 32px; background: none; border: none; color: var(--muted);
             cursor: pointer; display: flex; align-items: center; justify-content: center;
             font-size: 16px; transition: background .15s, color .15s; }
  .win-btn:hover { background: var(--surface2); color: var(--text); }
  .win-btn#win-close:hover { background: var(--danger); color: #fff; }
  #header-window-controls { display: none; align-items: center; gap: 2px; flex-shrink: 0; }
  body.custom-window-controls #header-window-controls { display: inline-flex !important; }
  #header-window-controls .win-btn { width: 28px; height: 28px; border: 1px solid var(--border);
                                     border-radius: var(--radius); font-size: 13px; }

  /* ── Header ── */
  header { background: var(--surface); border-bottom: 1px solid var(--border);
           padding: 12px 20px; display: flex; align-items: center; gap: 16px; flex-shrink: 0; }
  body.frameless header { min-height: 50px; user-select: none; }
  #header-drag-region { display: flex; align-items: center; gap: 12px; flex-shrink: 0; min-width: 120px; }
  body.frameless #header-drag-region.pywebview-drag-region { cursor: move; }
  header h1 { font-size: 15px; font-weight: 600; color: var(--accent);
              letter-spacing: .04em; white-space: nowrap; }
  body.frameless #header-drag-region,
  body.frameless #header-drag-region * { -webkit-app-region: drag; user-select: none; }
  #search-wrap { flex: 1; position: relative; }
  body.frameless #search-wrap,
  body.frameless #search,
  body.frameless #search-dropdown,
  body.frameless #reload-btn,
  body.frameless #mode-switcher,
  body.frameless .mode-btn,
  body.frameless #header-window-controls,
  body.frameless #header-window-controls * { -webkit-app-region: no-drag; user-select: auto; }
  body.frameless #search-wrap,
  body.frameless #search,
  body.frameless #search-dropdown,
  body.frameless #reload-btn,
  body.frameless #mode-switcher,
  body.frameless .mode-btn,
  body.frameless #header-window-controls,
  body.frameless #header-window-controls * { cursor: auto; }
  #search { width: 100%; background: var(--bg); border: 1px solid var(--border);
            border-radius: var(--radius); padding: 8px 14px 8px 36px;
            color: var(--text); font-size: 14px; outline: none; transition: border .15s; }
  #search:focus { border-color: var(--accent); }
  #search-wrap::before { content: '⌕'; position: absolute; left: 11px; top: 50%;
                          transform: translateY(-50%); color: var(--muted); font-size: 18px;
                          pointer-events: none; }
  #search-dropdown { position: absolute; top: calc(100% + 6px); left: 0; right: 0;
                     background: var(--surface); border: 1px solid var(--border);
                     border-radius: var(--radius); box-shadow: 0 8px 24px rgba(0,0,0,.45);
                     z-index: 1000; overflow: hidden; display: none; }
  #search-dropdown.visible { display: block; }
  .sdrop-item { padding: 9px 14px; cursor: pointer; border-bottom: 1px solid var(--border);
                transition: background .1s; }
  .sdrop-item:hover, .sdrop-item:focus { background: rgba(79,142,247,.1); outline: none; }
  .sdrop-name { font-family: var(--mono); font-size: 13px; font-weight: 600; color: var(--accent); }
  .sdrop-cat  { display: inline-block; font-size: 10px; padding: 1px 5px; border-radius: 3px;
                margin-left: 7px; vertical-align: middle; font-weight: 500;
                text-transform: uppercase; letter-spacing: .05em; }
  .sdrop-desc { font-size: 12px; color: var(--muted); margin-top: 3px;
                white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .sdrop-more { padding: 9px 14px; text-align: center; font-size: 12px; color: var(--accent);
                cursor: pointer; background: rgba(79,142,247,.04); }
  .sdrop-more:hover { background: rgba(79,142,247,.12); }
  #count { color: var(--muted); font-size: 12px; white-space: nowrap; }
  #reload-btn { background: none; border: 1px solid var(--border); border-radius: var(--radius);
                color: var(--muted); font-size: 16px; padding: 4px 10px; cursor: pointer;
                transition: color .15s, border-color .15s; flex-shrink: 0; }
  #reload-btn:hover { color: var(--accent); border-color: var(--accent); }

  /* ── Mode switcher ── */
  #mode-switcher { display: flex; gap: 4px; flex-shrink: 0; }
  .mode-btn { background: none; border: 1px solid var(--border); border-radius: var(--radius);
              color: var(--muted); font-size: 12px; font-weight: 500; padding: 5px 13px;
              cursor: pointer; transition: color .15s, border-color .15s, background .15s;
              white-space: nowrap; }
  .mode-btn:hover { color: var(--text); border-color: var(--muted); }
  .mode-btn.active { background: var(--accent); border-color: var(--accent); color: #fff; }
  .mode-btn[data-mode="debug"].active   { background: var(--warn);   border-color: var(--warn); }
  .mode-btn[data-mode="tools"].active   { background: var(--green);  border-color: var(--green); }
  .mode-btn[data-mode="ide"].active     { background: var(--accent2); border-color: var(--accent2); }
  .mode-btn[data-mode="files"].active { background: #3a8a5a; border-color: #3a8a5a; }

  /* ── Library sub-tabs ── */
  #lib-tabs { background: var(--surface); border-bottom: 1px solid var(--border);
              padding: 0 20px; display: none; gap: 2px; flex-shrink: 0; overflow-x: auto; }
  body[data-mode="library"] #lib-tabs { display: flex; }
  .tab { padding: 8px 13px; cursor: pointer; border-bottom: 2px solid transparent;
         color: var(--muted); font-size: 12px; white-space: nowrap; transition: color .15s, border-color .15s; }
  .tab:hover { color: var(--text); }
  .tab.active { color: var(--accent); border-bottom-color: var(--accent); }
  .tab[data-cat="ossl"].active  { color: var(--warn);  border-bottom-color: var(--warn); }
  .tab[data-cat="slua"].active  { color: #b07eff;       border-bottom-color: #b07eff; }

  /* ── Library sub-tabs (OSSL subcategory / Examples subcategory) ── */
  #lib-subtabs { background: var(--bg); border-bottom: 1px solid var(--border);
                 padding: 0 16px; display: none; gap: 0; flex-shrink: 0; overflow-x: auto; }
  #lib-subtabs.visible { display: flex; }
  .subtab { padding: 5px 11px; cursor: pointer; border-bottom: 2px solid transparent;
            color: var(--muted); font-size: 11px; white-space: nowrap;
            transition: color .15s, border-color .15s; }
  .subtab:hover { color: var(--text); }
  .subtab.active { color: var(--accent); border-bottom-color: var(--accent); font-weight: 600; }
  #lib-subtabs.ossl-mode .subtab.active { color: var(--warn); border-bottom-color: var(--warn); }
  #lib-subtabs.examples-mode .subtab.active { color: #78e8c8; border-bottom-color: #78e8c8; }

  /* ── IDE mode toggles (OSSL / Firestorm FS+) ── */
  .ide-mode-toggle { background: none; border: 1px solid var(--border); border-radius: var(--radius);
                     padding: 3px 9px; font-size: 11px; color: var(--muted); cursor: pointer;
                     transition: border-color .15s, color .15s, background .15s; font-family: var(--mono); }
  .ide-mode-toggle:hover { border-color: var(--text); color: var(--text); }
  .ide-mode-toggle.active-ossl { border-color: var(--warn); color: var(--warn);
                                  background: rgba(232,164,74,.12); }
  .ide-mode-toggle.active-fs   { border-color: var(--accent2); color: var(--accent2);
                                  background: rgba(130,100,255,.12); }

  /* ── Layout ── */
  #main { display: flex; flex: 1; overflow: hidden; }

  /* ── Resize splitter ── */
  #splitter { width: 5px; flex-shrink: 0; cursor: col-resize; background: transparent;
              border-right: 1px solid var(--border); transition: border-color .15s; position: relative; }
  #splitter:hover, #splitter.dragging { border-right-color: var(--accent); }
  #splitter::after { content: ''; position: absolute; top: 50%; left: 50%;
                     transform: translate(-50%,-50%); width: 3px; height: 32px;
                     border-radius: 2px; background: var(--border); transition: background .15s; }
  #splitter:hover::after, #splitter.dragging::after { background: var(--accent); }

  /* ── Results pane ── */
  #results-pane { width: 360px; min-width: 180px; max-width: 70%; flex-shrink: 0;
                  overflow-y: auto; display: flex; flex-direction: column; border-right: none;
                  will-change: width; contain: layout; }
  .result-card { padding: 12px 16px; border-bottom: 1px solid var(--border);
                 cursor: pointer; transition: background .1s; }
  .result-card:hover { background: var(--surface); }
  .result-card.selected { background: rgba(79,142,247,.12); border-left: 3px solid var(--accent); }
  .card-name { font-family: var(--mono); font-size: 13px; font-weight: 600; color: var(--accent); }
  .card-cat  { display: inline-block; font-size: 10px; padding: 1px 6px;
               border-radius: 3px; margin-left: 8px; vertical-align: middle;
               font-weight: 500; text-transform: uppercase; letter-spacing: .05em; }
  .cat-functions    { background: rgba(79,142,247,.18); color: #7fb4ff; }
  .cat-events       { background: rgba(124,106,247,.18); color: #a99bff; }
  .cat-constants    { background: rgba(79,194,138,.18); color: #7de8b5; }
  .cat-tutorials    { background: rgba(232,164,74,.18); color: #f0c070; }
  .cat-idioms       { background: rgba(100,180,200,.18); color: #88d4e8; }
  .cat-patterns     { background: rgba(180,120,240,.18); color: #d0a0ff; }
  .cat-anti-patterns{ background: rgba(232,90,90,.18); color: #ff9090; }
  .cat-function-usage{ background: rgba(150,200,100,.18); color: #b0e880; }
  .cat-reference     { background: rgba(200,160,80,.18);  color: #e8c878; }
  .cat-examples      { background: rgba(80,200,160,.18);  color: #78e8c8; }
  .cat-ossl          { background: rgba(232,164,74,.18);  color: var(--warn); }
  .cat-slua          { background: rgba(176,126,255,.18); color: #b07eff; }
  .card-sig  { font-family: var(--mono); font-size: 11px; color: var(--muted);
               margin-top: 3px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .card-desc { font-size: 12px; color: var(--muted); margin-top: 4px;
               display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
  .card-meta { display: flex; gap: 10px; margin-top: 5px; }
  .card-pill { font-size: 10px; padding: 1px 6px; border-radius: 3px; }
  .pill-sleep  { background: rgba(232,164,74,.15); color: var(--warn); }
  .pill-energy { background: rgba(79,194,138,.15); color: var(--green); }
  .pill-dep    { background: rgba(232,90,90,.15);  color: var(--danger); }
  #no-results  { padding: 40px 20px; color: var(--muted); text-align: center; }

  /* ── Doc viewer ── */
  #doc-pane { flex: 1; overflow-y: auto; padding: 0; display: flex; flex-direction: column; }
  #doc-header { background: var(--surface); border-bottom: 1px solid var(--border);
                padding: 14px 24px; display: flex; align-items: flex-start; gap: 16px; flex-shrink: 0; }
  #doc-title { font-family: var(--mono); font-size: 20px; font-weight: 700; color: var(--accent); }
  #doc-subtitle { font-family: var(--mono); font-size: 13px; color: var(--muted); margin-top: 4px; }
  #doc-meta { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 8px; }
  .meta-chip { font-size: 11px; padding: 3px 10px; border-radius: 4px;
               background: var(--border); color: var(--text); }
  .meta-chip b { color: var(--muted); margin-right: 4px; }
  #doc-wiki { margin-left: auto; flex-shrink: 0; }
  #doc-wiki a { color: var(--accent); font-size: 12px; text-decoration: none; }
  #doc-wiki a:hover { text-decoration: underline; }
  #doc-body { padding: 24px; flex: 1; user-select: text; -webkit-user-select: text; }
  #doc-body h1,#doc-body h2,#doc-body h3 { color: var(--text); margin: 1.2em 0 .5em; }
  #doc-body h1 { font-size: 18px; }
  #doc-body h2 { font-size: 15px; border-bottom: 1px solid var(--border); padding-bottom: 4px; }
  #doc-body h3 { font-size: 13px; color: var(--muted); }
  #doc-body p  { line-height: 1.7; margin: .6em 0; color: var(--text); }
  #doc-body a  { color: var(--accent); }
  #doc-body code { font-family: var(--mono); font-size: 12px; background: var(--surface);
                   padding: 1px 5px; border-radius: 3px; color: #c8e0ff; }
  #doc-body pre { background: var(--surface); border: 1px solid var(--border);
                  border-radius: var(--radius); padding: 16px; overflow-x: auto; margin: 0; }
  #doc-body pre code { background: none; padding: 0; color: #b8d8ff; font-size: 12.5px; }
  #doc-body table { border-collapse: collapse; width: 100%; margin: 1em 0; font-size: 13px; }
  #doc-body th,#doc-body td { border: 1px solid var(--border); padding: 6px 10px; }
  #doc-body th { background: var(--surface); color: var(--muted); text-align: left; }
  #doc-body blockquote { border-left: 3px solid var(--warn); padding: 8px 16px;
                          background: rgba(232,164,74,.06); margin: 1em 0; color: var(--warn); }
  #doc-body ul,#doc-body ol { padding-left: 1.6em; margin: .5em 0; line-height: 1.7; }
  /* ── Code block copy button ── */
  .code-wrap { position: relative; margin: 1em 0; }
  .copy-btn { position: absolute; top: 6px; right: 8px;
              background: var(--bg); border: 1px solid var(--border);
              border-radius: var(--radius); color: var(--muted); font-size: 11px;
              padding: 2px 8px; cursor: pointer; opacity: 0;
              transition: opacity .15s, color .15s, border-color .15s;
              font-family: var(--mono); line-height: 1.6; }
  .code-wrap:hover .copy-btn { opacity: 1; }
  .copy-btn:hover { color: var(--text); border-color: var(--muted); }
  .copy-btn.copied { color: var(--green); border-color: var(--green); opacity: 1; }
  /* ── Version switcher bar ── */
  .version-bar { display:flex; align-items:center; gap:6px; padding:0 0 8px; flex-wrap:wrap; }
  .ver-label   { font-size:0.78em; opacity:0.55; white-space:nowrap; }
  .ver-btn     { font-size:0.76em; padding:2px 8px; border-radius:var(--radius); cursor:pointer;
                 border:1px solid var(--border); background:var(--bg2); color:var(--text); }
  .ver-btn.active { background:var(--accent); color:#fff; border-color:var(--accent); }
  .ver-btn:hover  { border-color:var(--muted); }
  .ver-lock-btn   { font-size:0.76em; padding:2px 8px; border-radius:var(--radius); cursor:pointer;
                    border:1px dashed var(--border); background:transparent; color:var(--muted);
                    margin-left:auto; }
  .ver-lock-btn:hover { color:var(--text); border-color:var(--muted); }
  .open-ide-btn   { font-size:0.82em; padding:3px 10px; border-radius:var(--radius); cursor:pointer;
                    border:1px solid var(--accent); color:var(--accent); background:transparent;
                    flex-shrink:0; align-self:flex-start; margin-top:2px; }
  .open-ide-btn:hover { background:var(--accent); color:#fff; }
  #doc-placeholder { display: flex; flex: 1; align-items: center; justify-content: center;
                     color: var(--muted); flex-direction: column; gap: 10px; }
  #doc-placeholder .big { font-size: 48px; opacity: .2; }

  /* ── Scrollbars ── */
  ::-webkit-scrollbar { width: 6px; height: 6px; }
  ::-webkit-scrollbar-track { background: transparent; }
  ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

  /* ── Debug pane ── */
  #debug-pane { flex: 1; overflow: hidden; display: flex; }
  #debug-editor { width: 360px; min-width: 180px; max-width: 70%; flex-shrink: 0;
                  display: flex; flex-direction: column; overflow: hidden;
                  will-change: width; contain: layout; }
  #debug-toolbar { background: var(--surface); border-bottom: 1px solid var(--border);
                   padding: 10px 14px; display: flex; align-items: center; gap: 10px;
                   flex-shrink: 0; }
  #load-file-btn { background: var(--surface); border: 1px solid var(--border);
                   border-radius: var(--radius); color: var(--text); font-size: 12px;
                   padding: 5px 10px; cursor: pointer; white-space: nowrap;
                   flex-shrink: 0; transition: border-color .15s, color .15s; }
  #load-file-btn:hover { border-color: var(--accent); color: var(--accent); }
  #file-label { font-size: 11px; color: var(--muted); overflow: hidden;
                text-overflow: ellipsis; white-space: nowrap; max-width: 130px;
                flex-shrink: 1; }
  #check-mode { background: var(--bg); border: 1px solid var(--border);
                border-radius: var(--radius); color: var(--text);
                padding: 5px 8px; font-size: 12px; cursor: pointer; }
  #run-check { background: var(--accent); border: none; border-radius: var(--radius);
               color: #fff; font-size: 12px; font-weight: 600;
               padding: 6px 14px; cursor: pointer; transition: opacity .15s; }
  #run-check:hover { opacity: .85; }
  #run-check:disabled { opacity: .45; cursor: default; }
  #check-stats { font-size: 11px; color: var(--muted); flex: 1; text-align: right; }
  #lsl-source { flex: 1; background: var(--bg); border: none; resize: none;
                color: var(--text); font-family: var(--mono); font-size: 12.5px;
                padding: 14px 16px; outline: none; line-height: 1.6; }
  #issues-pane { flex: 1; overflow-y: auto; display: flex; flex-direction: column; }
  .issue-row { padding: 10px 16px; border-bottom: 1px solid var(--border);
               display: flex; gap: 10px; align-items: flex-start;
               transition: background .1s; cursor: pointer; }
  .issue-row:hover { background: var(--surface); }
  .issue-sev { font-size: 10px; font-weight: 700; padding: 2px 7px;
               border-radius: 3px; white-space: nowrap; flex-shrink: 0; margin-top: 2px; }
  .sev-ERROR { background: rgba(232,90,90,.18); color: var(--danger); }
  .sev-WARN  { background: rgba(232,164,74,.18); color: var(--warn); }
  .sev-INFO  { background: rgba(79,142,247,.18); color: var(--accent); }
  .issue-line { font-family: var(--mono); font-size: 11px; color: var(--muted);
                flex-shrink: 0; min-width: 38px; text-align: right; margin-top: 3px; }
  .issue-body { flex: 1; }
  .issue-code { font-family: var(--mono); font-size: 10px; color: var(--muted); }
  .issue-msg  { font-size: 12px; color: var(--text); margin-top: 2px; line-height: 1.45; }
  .issue-src  { font-size: 10px; color: var(--muted); margin-top: 2px; }
  .issue-row.expanded { background: var(--surface); }
  .issue-detail { display: none; padding: 10px 16px 14px 16px;
                  border-bottom: 1px solid var(--border); background: var(--surface); }
  .issue-detail.open { display: block; }
  .issue-detail-name { font-family: var(--mono); font-size: 13px; color: var(--accent);
                       font-weight: 600; margin-bottom: 4px; }
  .issue-detail-sig  { font-family: var(--mono); font-size: 11px; color: var(--text);
                       background: var(--bg); padding: 4px 8px; border-radius: 4px;
                       margin-bottom: 6px; white-space: pre-wrap; word-break: break-all; }
  .issue-detail-desc { font-size: 12px; color: var(--text); line-height: 1.5; }
  .issue-detail-meta { font-size: 10px; color: var(--muted); margin-top: 4px;
                       display: flex; gap: 14px; flex-wrap: wrap; }
  .issue-detail-actions { display: flex; gap: 8px; margin-top: 8px; }
  .issue-jump-btn { font-size: 10px; padding: 3px 9px; cursor: pointer;
                    background: none; border: 1px solid var(--accent); color: var(--accent);
                    border-radius: 4px; }
  .issue-jump-btn:hover { background: rgba(79,142,247,.12); }
  .issue-wiki-btn { font-size: 10px; padding: 3px 9px; cursor: pointer;
                    background: none; border: 1px solid var(--muted); color: var(--muted);
                    border-radius: 4px; }
  .issue-wiki-btn:hover { background: rgba(255,255,255,.05); }
  #issues-empty { display: flex; flex: 1; flex-direction: column;
                  align-items: center; justify-content: center;
                  color: var(--muted); gap: 10px; padding: 40px; text-align: center; }

  /* ── Tools pane ── */
  #tools-pane { flex: 1; overflow: hidden; display: flex; }
  #cache-sidebar { width: 260px; flex-shrink: 0; border-right: 1px solid var(--border);
                   overflow-y: auto; padding: 16px 14px; display: flex; flex-direction: column; gap: 14px; }
  #cache-tools-area { flex: 1; overflow-y: auto; padding: 16px 20px;
                      display: flex; flex-direction: column; gap: 12px; }
  .stat-block { background: var(--surface); border: 1px solid var(--border);
                border-radius: var(--radius); padding: 12px 14px; }
  .stat-block h3 { font-size: 11px; font-weight: 600; color: var(--muted);
                   text-transform: uppercase; letter-spacing: .06em; margin-bottom: 8px; }
  .stat-row { display: flex; justify-content: space-between; align-items: baseline;
              font-size: 12px; padding: 2px 0; }
  .stat-row .stat-key { color: var(--muted); }
  .stat-row .stat-val { font-family: var(--mono); color: var(--text); font-size: 11px; }
  .stat-val.ok  { color: var(--green); }
  .stat-val.off { color: var(--muted); }
  .tool-card { background: var(--surface); border: 1px solid var(--border);
               border-radius: var(--radius); overflow: hidden; }
  .tool-card.running { border-color: var(--accent); }
  .tool-card-header { padding: 12px 16px; display: flex; align-items: flex-start; gap: 12px; }
  .tool-card-info { flex: 1; }
  .tool-card-name { font-size: 13px; font-weight: 600; color: var(--text); }
  .tool-card-desc { font-size: 12px; color: var(--muted); margin-top: 3px; line-height: 1.5; }
  .tool-card-note { font-size: 11px; color: var(--warn); margin-top: 5px; }
  .tool-card-opts { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 8px; align-items: center; }
  .tool-opt-label { font-size: 11px; color: var(--muted); }
  .tool-opt-select { background: var(--bg); border: 1px solid var(--border);
                     border-radius: 4px; color: var(--text); padding: 3px 6px; font-size: 11px; }
  .tool-opt-number { background: var(--bg); border: 1px solid var(--border);
                     border-radius: 4px; color: var(--text); padding: 3px 6px;
                     font-size: 11px; width: 72px; font-family: var(--mono); }
  .tool-opt-check { accent-color: var(--accent); width: 13px; height: 13px; cursor: pointer; }
  .tool-run-btn { background: var(--accent); border: none; border-radius: var(--radius);
                  color: #fff; font-size: 12px; font-weight: 600; padding: 6px 14px;
                  cursor: pointer; white-space: nowrap; flex-shrink: 0;
                  transition: opacity .15s; align-self: flex-start; }
  .tool-run-btn:hover { opacity: .85; }
  .tool-run-btn:disabled { opacity: .45; cursor: default; }
  .tool-run-btn.cancel { background: var(--danger); }
  .tool-output { border-top: 1px solid var(--border); background: var(--bg);
                 font-family: var(--mono); font-size: 11.5px; line-height: 1.55;
                 max-height: 260px; overflow-y: auto; padding: 10px 14px;
                 color: var(--muted); display: none; user-select: text; }
  .tool-output.visible { display: block; }
  .out-line { white-space: pre-wrap; word-break: break-word; }
  .out-line.err { color: var(--danger); }
  .out-status { margin-top: 6px; font-size: 11px; font-weight: 600; padding: 3px 0; }
  .out-status.ok  { color: var(--green); }
  .out-status.err { color: var(--danger); }

  /* ── Debug sub-tabs ── */
  #debug-splitter { width: 5px; flex-shrink: 0; cursor: col-resize; background: transparent;
                    border-right: 1px solid var(--border); transition: border-color .15s; position: relative; }
  #debug-splitter:hover, #debug-splitter.dragging { border-right-color: var(--accent); }
  #debug-splitter::after { content: ''; position: absolute; top: 50%; left: 50%;
                           transform: translate(-50%,-50%); width: 3px; height: 32px;
                           border-radius: 2px; background: var(--border); transition: background .15s; }
  #debug-splitter:hover::after, #debug-splitter.dragging::after { background: var(--accent); }
  #lib-splitter { width: 5px; flex-shrink: 0; cursor: col-resize; background: transparent;
                  border-right: 1px solid var(--border); transition: border-color .15s; position: relative; }
  #lib-splitter:hover, #lib-splitter.dragging { border-right-color: var(--accent); }
  #lib-splitter::after { content: ''; position: absolute; top: 50%; left: 50%;
                         transform: translate(-50%,-50%); width: 3px; height: 32px;
                         border-radius: 2px; background: var(--border); transition: background .15s; }
  #lib-splitter:hover::after, #lib-splitter.dragging::after { background: var(--accent); }
  #debug-right { flex: 1; overflow: hidden; display: flex; flex-direction: column; }
  #debug-subtabs { background: var(--surface); border-bottom: 1px solid var(--border);
                   padding: 0 14px; display: flex; gap: 2px; flex-shrink: 0; }
  .debug-subtab { padding: 7px 12px; cursor: pointer; border-bottom: 2px solid transparent;
                  color: var(--muted); font-size: 12px; white-space: nowrap;
                  transition: color .15s, border-color .15s; }
  .debug-subtab:hover { color: var(--text); }
  .debug-subtab.active { color: var(--accent); border-bottom-color: var(--accent); }
  .debug-subpane { flex: 1; overflow-y: auto; display: none; flex-direction: column; }
  .debug-subpane.active { display: flex; }

  /* ── Memory sub-pane ── */
  .mem-summary { padding: 12px 16px; border-bottom: 1px solid var(--border);
                 display: flex; flex-wrap: wrap; gap: 14px; align-items: flex-end; }
  .mem-stat { display: flex; flex-direction: column; }
  .mem-stat-val { font-family: var(--mono); font-size: 18px; font-weight: 700; color: var(--accent); }
  .mem-stat-val.warn   { color: var(--warn); }
  .mem-stat-val.danger { color: var(--danger); }
  .mem-stat-key { font-size: 10px; color: var(--muted); margin-top: 2px; }
  .mem-bar-wrap { padding: 0 16px 10px; }
  .mem-bar-track { width: 100%; height: 6px; background: var(--border); border-radius: 3px; }
  .mem-bar { height: 6px; border-radius: 3px; background: var(--accent); transition: width .3s; }
  .mem-var-row { padding: 5px 16px; border-bottom: 1px solid var(--border);
                 display: flex; gap: 8px; font-size: 12px; align-items: baseline; }
  .mem-var-scope { font-size: 10px; padding: 1px 5px; border-radius: 3px; font-weight: 600;
                   flex-shrink: 0; }
  .scope-global { background: rgba(79,142,247,.15); color: var(--accent); }
  .scope-local  { background: rgba(79,194,138,.15); color: var(--green); }
  .mem-var-type { font-family: var(--mono); color: var(--muted); width: 68px; flex-shrink: 0; }
  .mem-var-name { font-family: var(--mono); color: var(--text); flex: 1; }
  .mem-var-size { font-family: var(--mono); font-size: 11px; color: var(--muted); flex-shrink: 0; }
  .mem-note { padding: 10px 16px; font-size: 11px; color: var(--muted); font-style: italic; }

  /* ── Channel sub-pane ── */
  .chan-row { padding: 7px 16px; border-bottom: 1px solid var(--border);
              display: flex; gap: 10px; font-size: 12px; align-items: baseline; }
  .chan-num  { font-family: var(--mono); color: var(--accent); width: 88px; flex-shrink: 0; }
  .chan-func { font-family: var(--mono); color: var(--text); width: 130px; flex-shrink: 0; }
  .chan-label{ color: var(--muted); flex: 1; }
  .chan-line { font-family: var(--mono); font-size: 11px; color: var(--muted); flex-shrink: 0; }
  .chan-warning { padding: 8px 16px; color: var(--warn); font-size: 12px;
                  border-bottom: 1px solid var(--border); display: flex; gap: 6px; }

  /* ── Delays sub-pane ── */
  .delay-event { background: var(--surface); border-bottom: 2px solid var(--border);
                 padding: 7px 16px; font-size: 12px; font-weight: 600; color: var(--text);
                 display: flex; justify-content: space-between; align-items: baseline; }
  .delay-event-total { font-family: var(--mono); color: var(--warn); font-size: 13px; }
  .delay-row { padding: 5px 16px 5px 28px; border-bottom: 1px solid var(--border);
               display: flex; gap: 10px; font-size: 12px; align-items: baseline; }
  .delay-func { font-family: var(--mono); color: var(--text); flex: 1; }
  .delay-line { font-family: var(--mono); font-size: 11px; color: var(--muted); }
  .delay-secs { font-family: var(--mono); font-size: 11px; color: var(--warn); flex-shrink: 0; }

  /* ── Debug toolbar additions ── */
  .toolbar-sep { width: 1px; background: var(--border); height: 20px; flex-shrink: 0; }
  #fmt-btn, #flatten-btn, #debug-ide-tab-select {
    background: none; border: 1px solid var(--border); border-radius: var(--radius);
    color: var(--muted); font-size: 11px; padding: 5px 9px; cursor: pointer;
    white-space: nowrap; transition: border-color .15s, color .15s; flex-shrink: 0;
  }
  #fmt-btn:hover           { border-color: var(--accent);  color: var(--accent); }
  #flatten-btn:hover       { border-color: var(--accent2); color: var(--accent2); }
  #debug-ide-tab-select:hover,
  #debug-ide-tab-select:focus { border-color: var(--accent); color: var(--accent); outline: none; }
  #fmt-btn:disabled, #flatten-btn:disabled, #debug-ide-tab-select:disabled { opacity: .45; cursor: default; }

  /* ── IDE tabs / loading ── */
  #ide-tabs-bar { background: var(--bg); border-bottom: 1px solid var(--border);
                  display: flex; align-items: center; gap: 6px; padding: 6px 10px;
                  overflow-x: auto; overflow-y: hidden; flex-shrink: 0; }
  #ide-tabs-empty { color: var(--muted); font-size: 11px; padding: 3px 6px; }
  .ide-tab { display: inline-flex; align-items: center; gap: 6px; min-width: 0;
             max-width: 260px; background: var(--surface); border: 1px solid var(--border);
             border-radius: var(--radius); color: var(--muted); padding: 5px 9px;
             cursor: pointer; transition: border-color .15s, color .15s, background .15s;
             flex-shrink: 0; }
  .ide-tab:hover { border-color: var(--text); color: var(--text); }
  .ide-tab.active { border-color: var(--accent); color: var(--accent); background: rgba(79,142,247,.08); }
  .ide-tab-label { min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
                   font-family: var(--mono); font-size: 11px; }
  .ide-tab-close { background: none; border: none; color: inherit; cursor: pointer;
                   font-size: 13px; line-height: 1; padding: 0; opacity: .75; flex-shrink: 0; }
  .ide-tab-close:hover { opacity: 1; }
  #ide-loading-overlay { position: absolute; inset: 0; display: none; align-items: center; justify-content: center;
                         background: rgba(12,16,22,.55); backdrop-filter: blur(2px); z-index: 5; }
  #ide-loading-overlay.active { display: flex; }
  #ide-loading-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius);
                      padding: 16px 20px; color: var(--text); font-size: 12px; display: flex; align-items: center;
                      gap: 10px; box-shadow: 0 8px 24px rgba(0,0,0,.35); }
  .ide-loading-spinner { width: 14px; height: 14px; border-radius: 50%; border: 2px solid rgba(255,255,255,.14);
                         border-top-color: var(--accent); animation: ide-spin .8s linear infinite; }
  @keyframes ide-spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

  /* ── Cache analysis cards (GET-based) ── */
  .analysis-section-hdr { font-size: 11px; font-weight: 600; color: var(--muted);
                           text-transform: uppercase; letter-spacing: .06em;
                           padding: 14px 4px 6px; border-top: 1px solid var(--border);
                           margin-top: 4px; }
  .analysis-card { background: var(--surface); border: 1px solid var(--border);
                   border-radius: var(--radius); overflow: hidden; }
  .analysis-card-hdr  { padding: 10px 16px; display: flex; align-items: flex-start; gap: 12px; }
  .analysis-card-info { flex: 1; }
  .analysis-card-name { font-size: 13px; font-weight: 600; color: var(--text); }
  .analysis-card-desc { font-size: 12px; color: var(--muted); margin-top: 3px; }
  .analysis-run-btn { background: none; border: 1px solid var(--accent);
                      border-radius: var(--radius); color: var(--accent);
                      font-size: 11px; padding: 5px 12px; cursor: pointer;
                      white-space: nowrap; flex-shrink: 0;
                      transition: background .15s, color .15s; }
  .analysis-run-btn:hover    { background: var(--accent); color: #fff; }
  .analysis-run-btn:disabled { opacity: .45; cursor: default; }
  .analysis-result { border-top: 1px solid var(--border); padding: 12px 16px;
                     display: none; font-size: 12px; line-height: 1.6; }
  .analysis-result.visible { display: block; }
  .analysis-table { width: 100%; border-collapse: collapse; font-size: 11.5px; margin-top: 8px; }
  .analysis-table th { text-align: left; color: var(--muted); font-weight: 600;
                       padding: 3px 8px; border-bottom: 1px solid var(--border); }
  .analysis-table td { padding: 3px 8px; border-bottom: 1px solid rgba(255,255,255,.04);
                       color: var(--text); vertical-align: top; }
  .td-mono { font-family: var(--mono); font-size: 11px; }
  .tag-cloud { display: flex; flex-wrap: wrap; gap: 6px; padding: 8px 0; }
  .tag-pill { background: rgba(79,142,247,.12); color: var(--accent); font-size: 11px;
              padding: 3px 10px; border-radius: 12px; cursor: pointer;
              transition: background .15s; user-select: none; }
  .tag-pill:hover, .tag-pill.active { background: var(--accent); color: #fff; }
  .tag-pattern-row { padding: 3px 0; display: flex; gap: 8px; font-size: 12px; }
  .tag-pattern-cat { font-family: var(--mono); font-size: 10px; color: var(--muted);
                     min-width: 90px; flex-shrink: 0; }
  .run-tools-hdr { font-size: 11px; font-weight: 600; color: var(--muted);
                   text-transform: uppercase; letter-spacing: .06em; padding: 4px 4px 8px; }

  /* ── IDE / Library shared button style ── */
  .ide-tool-btn { background: none; border: 1px solid var(--border); border-radius: var(--radius);
                  color: var(--muted); font-size: 12px; padding: 5px 10px; cursor: pointer;
                  white-space: nowrap; flex-shrink: 0;
                  transition: border-color .15s, color .15s, background .15s; }
  .ide-tool-btn:hover { border-color: var(--text); color: var(--text); }
  .ide-tool-btn:disabled { opacity: .4; cursor: default; }
  /* Elements only shown when running inside pywebview */
  .pv-only { display: none !important; }
  body.pv-ready .pv-only { display: inline-flex !important; }

  /* ── File tree ── */
  .ftree-item { padding: 4px 10px 4px 16px; cursor: pointer; display: flex;
                align-items: center; gap: 6px; border-left: 2px solid transparent;
                transition: background .1s; }
  .ftree-item:hover { background: var(--surface); }
  .ftree-item.selected { background: rgba(79,142,247,.1); border-left-color: var(--accent); }
  .ftree-item.dir { color: var(--text); font-weight: 500; }
  .ftree-item.file { color: var(--muted); }
  .ftree-item .ftree-icon { font-size: 13px; flex-shrink: 0; }
  .ftree-dir-children { padding-left: 10px; }

  /* ── External editor banner ── */
  #ide-ext-banner { display: none; }
  #ide-ext-banner.active { display: flex !important; }

  /* ── External page viewer ── */
  #ext-viewer { display: none; position: fixed; inset: 0; z-index: 2000;
                flex-direction: column; background: var(--bg); }
  #ext-viewer.visible { display: flex; }
  #ext-nav { display: flex; align-items: center; gap: 6px; padding: 6px 10px;
             background: var(--surface); border-bottom: 1px solid var(--border);
             flex-shrink: 0; }
  #ext-nav button { background: var(--surface2); border: 1px solid var(--border);
                    color: var(--text); border-radius: var(--radius); padding: 3px 10px;
                    cursor: pointer; font-size: 13px; }
  #ext-nav button:hover:not(:disabled) { background: var(--surface3); }
  #ext-nav button:disabled { opacity: 0.35; cursor: default; }
  #ext-url-bar { flex: 1; font-size: 11px; color: var(--text-dim); overflow: hidden;
                 text-overflow: ellipsis; white-space: nowrap; padding: 0 4px; }
  #ext-frame { flex: 1; border: none; width: 100%; background: #fff; }
</style>
</head>
<body data-mode="ide">

<!-- Frameless window control bar (shown only when frameless=true) -->
<div id="window-bar">
  <div id="window-title">SLCode</div>
  <div id="window-controls">
    <button class="win-btn" id="legacy-win-minimize" title="Minimize" aria-label="Minimize window">&#8211;</button>
    <button class="win-btn" id="legacy-win-maximize" title="Maximize" aria-label="Maximize window">&#9645;</button>
    <button class="win-btn" id="legacy-win-close" title="Close" aria-label="Close window">&#10005;</button>
  </div>
</div>

<div id="ext-viewer">
  <div id="ext-nav">
    <button id="ext-back-btn" title="Back" disabled>&#8592;</button>
    <button id="ext-fwd-btn"  title="Forward" disabled>&#8594;</button>
    <span id="ext-url-bar"></span>
    <button id="ext-browser-btn" title="Open in system browser">&#127760; Open in Browser</button>
    <button id="ext-close-btn" title="Close">&#10005; Close</button>
  </div>
  <iframe id="ext-frame" sandbox="allow-scripts allow-same-origin allow-forms allow-popups"></iframe>
  <div id="ext-blocked" style="display:none;flex:1;align-items:center;justify-content:center;
       flex-direction:column;gap:12px;color:var(--text-dim);font-size:14px;">
    <div>&#128683; This page cannot be displayed here.</div>
    <button id="ext-blocked-open" style="background:var(--accent);color:#fff;border:none;
            border-radius:var(--radius);padding:7px 18px;cursor:pointer;font-size:13px;">
      Open in System Browser
    </button>
  </div>
</div>

<header>
  <div id="header-drag-region" class="pywebview-drag-region">
    <h1>SLCode</h1>
    <span id="count"></span>
  </div>
  <div id="search-wrap">
    <input id="search" type="search" placeholder="Search functions, events, constants, patterns…" autofocus autocomplete="off">
    <div id="search-dropdown"></div>
  </div>
  <button id="reload-btn" title="Reload index from disk">↺</button>
  <div id="mode-switcher">
    <button class="mode-btn active" data-mode="files">&#128193; Files</button>
    <button class="mode-btn" data-mode="ide">&#128187; IDE</button>
    <button class="mode-btn" data-mode="debug">&#9881; Debug</button>
    <button class="mode-btn" data-mode="library">&#128196; Library</button>
    <button class="mode-btn" data-mode="tools">&#9881; Tools</button>
  </div>
  <div id="header-window-controls" aria-label="Window controls">
    <button class="win-btn" id="win-minimize" title="Minimize" aria-label="Minimize window">&#8211;</button>
    <button class="win-btn" id="win-maximize" title="Maximize" aria-label="Maximize window">&#9633;</button>
    <button class="win-btn" id="win-close" title="Close" aria-label="Close window">&#10005;</button>
  </div>
</header>

<div id="lib-tabs">
  <div class="tab active" data-cat="all">All</div>
  <div class="tab" data-cat="functions">Functions</div>
  <div class="tab" data-cat="events">Events</div>
  <div class="tab" data-cat="constants">Constants</div>
  <div class="tab" data-cat="tutorials">Tutorials</div>
  <div class="tab" data-cat="ossl">OSSL</div>
  <div class="tab" data-cat="slua">SLua</div>
  <div class="tab" data-cat="idioms">Idioms</div>
  <div class="tab" data-cat="patterns">Patterns</div>
  <div class="tab" data-cat="anti-patterns">Anti-patterns</div>
  <div class="tab" data-cat="function-usage">Fn Usage</div>
  <div class="tab" data-cat="examples">Examples</div>
  <div class="tab" data-cat="reference">Reference</div>
</div>
<div id="lib-subtabs"></div>

<div id="main">
  <div id="results-pane"></div>
  <div id="splitter"></div>
  <div id="doc-pane">
    <div id="doc-placeholder">
      <div class="big">⌕</div>
      <div>Select a result to view its documentation</div>
    </div>
  </div>
</div>

<div id="tools-pane" style="display:none; flex:1; overflow:hidden; flex-direction:row;">
  <div id="cache-sidebar">
    <div class="stat-block" id="manifest-block">
      <h3>Cache Status</h3>
      <div class="stat-row"><span class="stat-key">Loading&#8230;</span></div>
    </div>
    <div class="stat-block" id="sources-block">
      <h3>Extension Sources</h3>
      <div class="stat-row"><span class="stat-key">Loading&#8230;</span></div>
    </div>
    <div class="stat-block" id="docs-block">
      <h3>Doc Counts</h3>
      <div class="stat-row"><span class="stat-key">Loading&#8230;</span></div>
    </div>
  </div>
  <div id="cache-tools-area">
    <div style="color:var(--muted);font-size:12px;padding:4px 0">Loading tools&#8230;</div>
  </div>
</div>

<div id="debug-pane" style="display:none; flex:1; overflow:hidden; flex-direction:row;">
  <div id="debug-editor">
    <div id="debug-toolbar">
      <label id="load-file-btn" for="file-input" title="Open .lsl or .lua file">&#128194; Open</label>
      <input type="file" id="file-input" accept=".lsl,.lua" style="display:none">
      <span id="file-label"></span>
      <select id="check-mode">
        <option value="both">Syntax + Sanity + Lint</option>
        <option value="syntax">Syntax only</option>
        <option value="sanity">Sanity only</option>
        <option value="lint">Lint only</option>
      </select>
      <button id="run-check" title="Run (Ctrl+Enter)">&#9654; Run</button>
      <button id="dbg-ossl-toggle" class="ide-mode-toggle" title="Enable OSSL (OpenSimulator) function support">OSSL</button>
      <button id="dbg-fs-toggle"   class="ide-mode-toggle" title="Enable Firestorm preprocessor (#include / #define)">FS+</button>
      <div class="toolbar-sep"></div>
      <button id="fmt-btn" title="Format source code">&#8706; Format</button>
      <button id="flatten-btn" title="Flatten #include directives">&#8801; Flatten</button>
      <div class="toolbar-sep"></div>
      <select id="debug-ide-tab-select" title="Load an open IDE tab into the debugger">
        <option value="">Open IDE tab…</option>
      </select>
      <span id="check-stats"></span>
    </div>
    <textarea id="lsl-source" spellcheck="false" placeholder="Paste LSL source here&#8230; (Ctrl+Enter to run)"></textarea>
  </div>
  <div id="debug-splitter"></div>
  <div id="debug-right">
    <div id="debug-subtabs">
      <div class="debug-subtab active" data-subtab="issues">Issues</div>
      <div class="debug-subtab" data-subtab="memory">Memory</div>
      <div class="debug-subtab" data-subtab="channels">Channels</div>
      <div class="debug-subtab" data-subtab="delays">Delays</div>
    </div>
    <div class="debug-subpane active" id="subpane-issues">
      <div id="issues-empty">
        <div class="big" style="opacity:.2">&#9881;</div>
        <div>Paste LSL code and click Run</div>
      </div>
    </div>
    <div class="debug-subpane" id="subpane-memory">
      <div style="display:flex;flex:1;flex-direction:column;align-items:center;justify-content:center;color:var(--muted);gap:10px;padding:40px;text-align:center">
        <div class="big" style="opacity:.2">&#9632;</div>
        <div>Run a check to see memory estimates</div>
      </div>
    </div>
    <div class="debug-subpane" id="subpane-channels">
      <div style="display:flex;flex:1;flex-direction:column;align-items:center;justify-content:center;color:var(--muted);gap:10px;padding:40px;text-align:center">
        <div class="big" style="opacity:.2">&#128225;</div>
        <div>Run a check to see channel map</div>
      </div>
    </div>
    <div class="debug-subpane" id="subpane-delays">
      <div style="display:flex;flex:1;flex-direction:column;align-items:center;justify-content:center;color:var(--muted);gap:10px;padding:40px;text-align:center">
        <div class="big" style="opacity:.2">&#9201;</div>
        <div>Run a check to see sleep / delay profile</div>
      </div>
    </div>
  </div>
</div>

<!-- ── IDE Pane ──────────────────────────────────────────────────────── -->
<div id="ide-pane" style="display:none; flex:1; overflow:hidden; flex-direction:column;">
  <div id="ide-toolbar" style="background:var(--surface);border-bottom:1px solid var(--border);padding:8px 14px;display:flex;align-items:center;gap:10px;flex-shrink:0;">
    <span id="ide-file-label" style="font-family:var(--mono);font-size:12px;color:var(--muted);flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">untitled.lsl</span>
    <button id="ide-new-btn" class="ide-tool-btn">&#43; New</button>
    <button id="ide-open-btn" class="ide-tool-btn">&#128194; Open</button>
    <input type="file" id="ide-file-input" accept=".lsl,.lua" style="display:none">
    <button id="ide-save-btn" class="ide-tool-btn">&#128190; Save</button>
    <button id="ide-save-as-btn" class="ide-tool-btn" title="Save as a new project path">Save As</button>
    <button id="ide-reload-btn" class="ide-tool-btn" title="Reload from last saved version on disk">&#8635; Reload</button>
    <div class="toolbar-sep"></div>
    <button id="ide-undo-btn" class="ide-tool-btn" title="Undo (Ctrl+Z)">&#8630; Undo</button>
    <button id="ide-redo-btn" class="ide-tool-btn" title="Redo (Ctrl+Y / Ctrl+Shift+Z)">&#8631; Redo</button>
    <button id="ide-selection-btn" class="ide-tool-btn" title="Selection actions">Selection ▾</button>
    <button id="ide-wrap-btn" class="ide-tool-btn" title="Toggle word wrap (Alt+Z)">Wrap: On</button>
    <button id="ide-autocomplete-btn" class="ide-tool-btn" title="Toggle autocomplete suggestions">AC: On</button>
    <button id="ide-check-btn" class="ide-tool-btn" style="border-color:var(--accent);color:var(--accent)">&#9654; Check</button>
    <button id="ide-ossl-toggle" class="ide-mode-toggle" title="Enable OSSL (OpenSimulator extension functions) — os* functions treated as valid">OSSL</button>
    <button id="ide-fs-toggle"   class="ide-mode-toggle" title="Enable Firestorm preprocessor — #include / #define treated as valid">FS+</button>
    <div class="toolbar-sep"></div>
    <button id="ide-watch-btn" class="ide-tool-btn" title="Watch a file for Firestorm external editor sync">&#128279; Watch</button>
    <button id="ide-unwatch-btn" class="ide-tool-btn" style="display:none;border-color:var(--warn);color:var(--warn)" title="Stop watching — disconnect from Firestorm">&#128279; Unwatch</button>
    <button id="ide-fs-setup-btn" class="ide-tool-btn" title="Show Firestorm external editor setup">&#9881; FS Setup</button>
    <span id="ide-status" style="font-size:11px;color:var(--muted);flex-shrink:0;"></span>
  </div>
  <div id="ide-ext-banner" style="display:none;background:rgba(232,164,74,.12);border-bottom:1px solid rgba(232,164,74,.3);padding:5px 14px;flex-shrink:0;display:none;align-items:center;gap:10px;font-size:11px;color:var(--warn);">
    <span style="font-weight:600;flex-shrink:0;">&#128279; FIRESTORM SYNC</span>
    <span id="ide-ext-path" style="font-family:var(--mono);flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;opacity:.8;"></span>
    <span id="ide-ext-status" style="flex-shrink:0;"></span>
    <button id="ide-ext-reload-btn" class="ide-tool-btn" style="display:none;font-size:10px;padding:2px 8px;border-color:var(--warn);color:var(--warn)">&#8635; Reload</button>
  </div>
  <div id="ide-tabs-bar">
    <div id="ide-tabs-empty">No open tabs</div>
  </div>
  <div id="ide-body" style="flex:1;overflow:hidden;display:flex;flex-direction:row;">
    <div id="ide-editor-wrap" style="flex:1;overflow:hidden;position:relative;">
      <div id="ide-loading-overlay">
        <div id="ide-loading-card">
          <div class="ide-loading-spinner"></div>
          <div id="ide-loading-text">Loading…</div>
        </div>
      </div>
    </div>
    <div id="ide-issues-sidebar" style="width:280px;min-width:180px;flex-shrink:0;border-left:1px solid var(--border);overflow-y:auto;display:flex;flex-direction:column;">
      <div id="ide-issues-hdr" style="padding:8px 12px;background:var(--surface);border-bottom:1px solid var(--border);font-size:11px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;">Issues</div>
      <div id="ide-issues-list" style="flex:1;overflow-y:auto;">
        <div style="padding:20px;color:var(--muted);font-size:12px;text-align:center;">Check your code to see issues here.</div>
      </div>
    </div>
  </div>
</div>

<!-- ── Files / Project Pane ─────────────────────────────────────────── -->
<div id="files-pane" style="display:none; flex:1; overflow:hidden; flex-direction:row;">
  <!-- File browser sidebar -->
  <div id="lib-file-sidebar" style="width:280px;min-width:180px;flex-shrink:0;display:flex;flex-direction:column;overflow:hidden;">
    <div style="padding:10px 14px;background:var(--surface);border-bottom:1px solid var(--border);display:flex;align-items:center;gap:8px;flex-shrink:0;">
      <span style="font-size:11px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;flex:1;">Project Files</span>
      <button id="files-new-file-btn" class="ide-tool-btn" style="font-size:11px;padding:3px 8px;">&#43; File</button>
      <button id="files-new-dir-btn" class="ide-tool-btn" style="font-size:11px;padding:3px 8px;">&#43; Folder</button>
      <button id="lib-refresh-btn" class="ide-tool-btn" style="font-size:11px;padding:3px 8px;">&#8635;</button>
    </div>
    <div style="padding:8px 10px;background:var(--bg);border-bottom:1px solid var(--border);display:flex;align-items:center;gap:6px;flex-shrink:0;">
      <button id="lib-browse-btn" class="ide-tool-btn" style="width:100%;justify-content:center;font-size:12px;padding:8px 10px;border-color:var(--accent);color:var(--accent);font-weight:600;" title="Select folder from the system dialog">&#128193; Browse for Folder…</button>
    </div>
    <div style="padding:5px 10px;background:var(--bg);border-bottom:1px solid var(--border);display:flex;align-items:center;gap:5px;flex-shrink:0;" title="Working directory — edit and press Enter or click Go">
      <span style="font-size:10px;color:var(--muted);font-weight:600;flex-shrink:0;">DIR</span>
      <input id="lib-cwd-input" type="text" spellcheck="false"
        style="flex:1;min-width:0;background:transparent;border:none;color:var(--muted);font-family:var(--mono);font-size:10px;outline:none;overflow:hidden;text-overflow:ellipsis;">
      <button id="lib-cwd-btn" class="ide-tool-btn" style="font-size:10px;padding:2px 6px;flex-shrink:0;">Go</button>
    </div>
    <div id="lib-file-tree" tabindex="0" style="flex:1;overflow-y:auto;padding:8px 0;font-size:12px;font-family:var(--mono);outline:none;"></div>
  </div>
  <div id="lib-splitter"></div>
  <!-- Main area -->
  <div style="flex:1;overflow:hidden;display:flex;flex-direction:column;">
    <!-- File detail / actions panel -->
    <div id="lib-file-detail" style="background:var(--surface);border-bottom:1px solid var(--border);padding:12px 18px;display:flex;align-items:center;gap:12px;flex-shrink:0;min-height:54px;">
      <div id="lib-selected-name" style="font-family:var(--mono);font-size:13px;color:var(--accent);flex:1;">Select a file</div>
      <button id="files-open-ide-btn" class="ide-tool-btn" style="display:none;">&#128187; Open in IDE</button>
      <button id="files-rename-btn"   class="ide-tool-btn" style="display:none;">&#9998; Rename</button>
      <button id="files-delete-btn"   class="ide-tool-btn" style="display:none;border-color:var(--danger);color:var(--danger);">&#10005; Delete</button>
    </div>
    <!-- Git panel -->
    <div id="lib-git-panel" style="flex:1;overflow:hidden;display:flex;flex-direction:column;">
      <div style="padding:8px 18px;background:var(--surface);border-bottom:1px solid var(--border);display:flex;align-items:center;gap:10px;flex-shrink:0;">
        <span style="font-size:11px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;flex:1;">Git</span>
        <button id="git-stage-selected-btn" class="ide-tool-btn" style="font-size:11px;padding:3px 8px;" title="git add -- &lt;selected file&gt;">Stage Selected</button>
        <button id="git-unstage-selected-btn" class="ide-tool-btn" style="font-size:11px;padding:3px 8px;" title="git reset HEAD -- &lt;selected file&gt;">Unstage Selected</button>
        <button id="git-diff-selected-btn" class="ide-tool-btn" style="font-size:11px;padding:3px 8px;" title="git diff -- &lt;selected file&gt;">Diff Selected</button>
        <button id="git-refresh-btn" class="ide-tool-btn" style="font-size:11px;padding:3px 8px;">&#8635; Status</button>
        <button id="git-pull-btn" class="ide-tool-btn" style="font-size:11px;padding:3px 8px;">&#8595; Pull</button>
        <button id="git-push-btn" class="ide-tool-btn" style="font-size:11px;padding:3px 8px;">&#8593; Push</button>
      </div>
      <div id="git-status-area" style="padding:10px 18px;font-size:12px;color:var(--muted);font-family:var(--mono);flex-shrink:0;border-bottom:1px solid var(--border);max-height:160px;overflow-y:auto;">
        <em>Click "Status" to check git state.</em>
      </div>
      <div style="padding:10px 18px;display:flex;flex-direction:column;gap:8px;flex-shrink:0;">
        <div style="font-size:11px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;">Commit</div>
        <input id="git-commit-msg" type="text" placeholder="Commit message&#8230;"
          style="background:var(--bg);border:1px solid var(--border);border-radius:var(--radius);color:var(--text);padding:7px 10px;font-size:12px;width:100%;outline:none;">
        <div style="display:flex;gap:8px;align-items:center;">
          <label style="display:flex;align-items:center;gap:5px;font-size:11px;color:var(--muted);cursor:pointer;">
            <input type="checkbox" id="git-add-all" checked style="accent-color:var(--accent);cursor:pointer;"> Stage all
          </label>
          <button id="git-commit-btn" class="ide-tool-btn" style="border-color:var(--accent);color:var(--accent);">&#10003; Commit</button>
        </div>
      </div>
      <div id="git-output-area" style="flex:1;overflow-y:auto;font-family:var(--mono);font-size:11.5px;padding:10px 18px;color:var(--muted);white-space:pre-wrap;word-break:break-word;"></div>
    </div>
  </div>
</div>

<!-- Firestorm external editor setup modal — must be in DOM before <script> runs -->
<div id="fs-setup-modal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:1000;align-items:center;justify-content:center;">
  <div style="background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:28px 32px;max-width:560px;width:90%;position:relative;">
    <div style="font-size:15px;font-weight:700;color:var(--accent);margin-bottom:16px;">&#9881; Firestorm External Editor Setup</div>
    <p style="font-size:13px;color:var(--text);line-height:1.7;margin-bottom:12px;">
      In Firestorm: <b>Preferences → Firestorm → Use external editor</b><br>
      Enable the checkbox, then paste the command below into the field:
    </p>
    <div style="background:var(--bg);border:1px solid var(--border);border-radius:var(--radius);padding:10px 14px;font-family:var(--mono);font-size:12px;color:var(--text);word-break:break-all;margin-bottom:12px;" id="fs-cmd-display"></div>
    <button id="fs-cmd-copy-btn" class="ide-tool-btn" style="border-color:var(--accent);color:var(--accent);margin-bottom:16px;">&#128203; Copy command</button>
    <p style="font-size:12px;color:var(--muted);line-height:1.6;margin-bottom:4px;">
      When you open a script in Firestorm, it will launch this app with the temp file path. The IDE will open the file and keep it in sync automatically.
    </p>
    <button id="fs-setup-close-btn" style="position:absolute;top:14px;right:16px;background:none;border:none;font-size:20px;color:var(--muted);cursor:pointer;line-height:1;">&#10005;</button>
  </div>
</div>

<!-- ── Name dialog — filename input without typing full paths ─────────────── -->
<div id="name-dialog" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:1001;align-items:center;justify-content:center;">
  <div style="background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:22px 24px;min-width:340px;max-width:90%;box-shadow:0 8px 32px rgba(0,0,0,.4);">
    <div id="name-dialog-title" style="font-size:13px;font-weight:700;color:var(--accent);margin-bottom:6px;"></div>
    <div id="name-dialog-context" style="font-size:11px;color:var(--muted);font-family:var(--mono);margin-bottom:12px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;"></div>
    <input id="name-dialog-input" type="text" spellcheck="false"
      style="width:100%;box-sizing:border-box;background:var(--bg);border:1px solid var(--border);border-radius:var(--radius);color:var(--text);padding:7px 10px;font-size:13px;font-family:var(--mono);outline:none;margin-bottom:14px;">
    <div style="display:flex;justify-content:flex-end;gap:8px;">
      <button id="name-dialog-cancel" class="ide-tool-btn">Cancel</button>
      <button id="name-dialog-ok" class="ide-tool-btn" style="border-color:var(--accent);color:var(--accent);">OK</button>
    </div>
  </div>
</div>
<!-- ── Right-click context menu ──────────────────────────────────────────── -->
<div id="ctx-menu" style="display:none;position:fixed;z-index:1002;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);box-shadow:0 4px 16px rgba(0,0,0,.4);padding:4px 0;font-size:12px;min-width:160px;"></div>

<script>
// ── JS error display (debug) ──────────────────────────────────────────────────
// Catches any uncaught error and shows it in a red banner so it's visible
// without needing to open DevTools.
window.addEventListener('error', function(ev) {
  var d = document.getElementById('_js_err');
  if (!d) {
    d = document.createElement('div');
    d.id = '_js_err';
    d.style.cssText = 'position:fixed;top:0;left:0;right:0;background:#c00;color:#fff;'
      + 'padding:8px 14px;font:12px/1.4 monospace;z-index:99999;white-space:pre-wrap;cursor:pointer;';
    d.title = 'Click to dismiss';
    d.onclick = function(){ d.remove(); };
    document.body.appendChild(d);
  }
  d.textContent += '[' + (ev.filename||'?').replace(/.*\//, '') + ':' + ev.lineno + '] '
    + ev.message + '\n';
});
window.addEventListener('unhandledrejection', function(ev) {
  var d = document.getElementById('_js_err');
  if (!d) {
    d = document.createElement('div');
    d.id = '_js_err';
    d.style.cssText = 'position:fixed;top:0;left:0;right:0;background:#c00;color:#fff;'
      + 'padding:8px 14px;font:12px/1.4 monospace;z-index:99999;white-space:pre-wrap;cursor:pointer;';
    d.title = 'Click to dismiss';
    d.onclick = function(){ d.remove(); };
    document.body.appendChild(d);
  }
  d.textContent += '[unhandled promise] ' + (ev.reason && (ev.reason.stack || ev.reason)) + '\n';
});
// ─────────────────────────────────────────────────────────────────────────────
// Clipboard helper — avoids navigator.clipboard permission prompt in WebView2.
// Uses the execCommand path (no prompt, works in all Chromium-based WebViews).
function _clipCopy(text) {
  const ta = document.createElement('textarea');
  ta.value = text;
  ta.style.cssText = 'position:fixed;top:-9999px;left:-9999px;opacity:0';
  document.body.appendChild(ta);
  ta.focus();
  ta.select();
  try { document.execCommand('copy'); } catch (_) {}
  document.body.removeChild(ta);
}
// ─────────────────────────────────────────────────────────────────────────────

const searchEl  = document.getElementById('search');
const countEl   = document.getElementById('count');
const resultsEl = document.getElementById('results-pane');
const docEl     = document.getElementById('doc-pane');

let currentCat    = 'all';
let currentSubcat = 'all';   // active sub-tab within ossl / examples
let _lastResults  = [];       // full result set from last doSearch (for sub-tab filtering)
let ideOsslMode   = localStorage.getItem('ide-ossl-mode') === '1';
let ideFsMode     = localStorage.getItem('ide-fs-mode')   === '1';
let currentPath = null;
let debounce    = null;
let _multipartGroups = new Map();

function _stripPartSuffix(name) {
  const s = String(name || '').trim();
  return s.replace(/[ _\-](\d+)$/, '').trim() || s;
}

function _parsePartNumber(v) {
  const n = parseInt(String(v || ''), 10);
  return Number.isFinite(n) ? n : null;
}

function _groupMultipartExamples(docs) {
  _multipartGroups = new Map();
  if (!Array.isArray(docs) || !docs.length) return docs || [];

  const order = [];
  const clusters = new Map();
  const groupedPathSet = new Set();

  for (const d of docs) {
    if (!d || d.category !== 'examples') continue;
    const total = _parsePartNumber(d.source_part_total);
    const idx = _parsePartNumber(d.source_part_index);
    if (!total || total < 2 || idx === null || idx < 0) continue;
    const baseName = _stripPartSuffix(d.name);
    const project = String(d.source_project || '');
    const key = `${project.toLowerCase()}|${baseName.toLowerCase()}|${total}`;
    if (!clusters.has(key)) {
      clusters.set(key, {
        key,
        total,
        baseName,
        project,
        docs: [],
        firstPos: Number.MAX_SAFE_INTEGER,
      });
      order.push(key);
    }
    const c = clusters.get(key);
    c.docs.push(d);
    c.firstPos = Math.min(c.firstPos, docs.indexOf(d));
    groupedPathSet.add(d.path);
  }

  for (const key of order) {
    const c = clusters.get(key);
    if (!c || c.docs.length < 2) continue;
    c.docs.sort((a, b) => (_parsePartNumber(a.source_part_index) || 0) - (_parsePartNumber(b.source_part_index) || 0));
    const first = c.docs[0];
    const groupId = `group:${key}`;
    const groupDoc = {
      ...first,
      name: c.baseName || first.name,
      description: first.description || '',
      signature: '',
      source_part_index: '',
      source_part_total: String(c.total),
      __is_multipart_group: true,
      __group_id: groupId,
      __group_key: key,
      __part_total: c.docs.length,
      __parts: c.docs.map(x => ({
        path: x.path,
        name: x.name,
        source_part_index: x.source_part_index,
        source_part_total: x.source_part_total,
        source_doc_kind: x.source_doc_kind,
        source_url: x.source_url,
        source_name: x.source_name,
        language: x.language,
      })),
    };
    _multipartGroups.set(groupId, groupDoc);
  }

  const out = [];
  const emittedGroups = new Set();
  for (const d of docs) {
    if (!d || d.category !== 'examples') {
      out.push(d);
      continue;
    }
    if (!groupedPathSet.has(d.path)) {
      out.push(d);
      continue;
    }
    const total = _parsePartNumber(d.source_part_total);
    const baseName = _stripPartSuffix(d.name);
    const project = String(d.source_project || '');
    const key = `${project.toLowerCase()}|${baseName.toLowerCase()}|${total}`;
    const groupId = `group:${key}`;
    if (_multipartGroups.has(groupId) && !emittedGroups.has(groupId)) {
      out.push(_multipartGroups.get(groupId));
      emittedGroups.add(groupId);
    }
  }
  return out;
}

function _extractPrimaryCode(body) {
  const text = String(body || '').replace(/\r/g, '');
  const m = text.match(/```(?:lsl|lua)?\n([\s\S]*?)```/i);
  return (m ? m[1] : text).trim();
}

function _extractPrimaryText(body) {
  const text = String(body || '').replace(/\r/g, '').trim();
  const m = text.match(/```[^\n]*\n([\s\S]*?)```/i);
  return (m ? m[1] : text).trim();
}

function _inferDocKind(pathOrName, explicitKind = '', body = '') {
  const kind = String(explicitKind || '').toLowerCase();
  if (kind) return kind;
  const n = String(pathOrName || '').toLowerCase();
  const b = String(body || '').toLowerCase().slice(0, 4000);
  const merged = `${n}\n${b}`;
  if (/\b(licen[cs]e|eula|copyright|gpl|mit|apache|bsd)\b/.test(merged)) return 'license';
  if (/\b(notecard|note\s*card|route|waypoint)\b/.test(merged)) return 'notecard';
  if (/\b(config|settings?|ini|menuitems?|positions?|channel|param)\b/.test(merged)) return 'config';
  if (/\b(readme|manual|install|usage|history|changelog|attribution|docs?|documentation|help|guide)\b/.test(merged)) return 'user-doc';
  return 'script';
}

function _docKindRank(kind) {
  const k = String(kind || '').toLowerCase();
  if (k === 'user-doc') return 0;
  if (k === 'license') return 2;
  return 1;
}

function _orderResultsForDisplay(docs) {
  if (!Array.isArray(docs)) return [];
  if (currentCat !== 'examples' && !(currentCat === 'ossl' && currentSubcat === 'examples')) {
    return docs;
  }
  return [...docs].sort((a, b) => {
    const ka = _inferDocKind(a.path || a.name, a.source_doc_kind || '');
    const kb = _inferDocKind(b.path || b.name, b.source_doc_kind || '');
    const ra = _docKindRank(ka);
    const rb = _docKindRank(kb);
    if (ra !== rb) return ra - rb;
    return String(a.name || '').localeCompare(String(b.name || ''));
  });
}

async function loadDocById(docId) {
  if (!docId) return;
  if (!String(docId).startsWith('group:')) {
    return loadDoc(docId);
  }
  currentPath = docId;
  const group = _multipartGroups.get(docId);
  if (!group) return;
  const parts = group.__parts || [];
  const partPayloads = await Promise.all(
    parts.map(async part => {
      const res = await fetch(`/api/doc?path=${encodeURIComponent(part.path)}`);
      const data = await res.json();
      return { part, data };
    })
  );

  const enriched = partPayloads.map(({ part, data }, order) => {
    const fm = data.front_matter || {};
    const body = data.body || '';
    const kind = _inferDocKind(part.path || part.name, fm.source_doc_kind || part.source_doc_kind || '', body);
    const idxRaw = _parsePartNumber(part.source_part_index);
    const idx = idxRaw !== null ? idxRaw : order;
    const total = _parsePartNumber(part.source_part_total) || partPayloads.length;
    const src = fm.source_url || part.source_url || '';
    const partName = String(part.name || '').replace(/`/g, '').trim() || `Part ${idx + 1}`;
    return {
      kind,
      order,
      idx,
      total,
      partName,
      src,
      lang: String((fm.language || part.language || 'LSL')).toLowerCase(),
      code: _extractPrimaryCode(body),
      text: _extractPrimaryText(body),
    };
  });

  const docsTop = enriched
    .filter(x => x.kind === 'user-doc')
    .sort((a, b) => a.order - b.order);

  const codeKinds = new Set(['script', 'notecard', 'config']);
  const codeParts = enriched
    .filter(x => codeKinds.has(x.kind) || !['user-doc', 'license'].includes(x.kind))
    .sort((a, b) => a.idx - b.idx || a.order - b.order);

  const licensesBottom = enriched
    .filter(x => x.kind === 'license')
    .sort((a, b) => a.order - b.order);

  const navLines = codeParts.map((part, i) => {
    const label = `Part ${i + 1}`;
    const anchor = `part-${i + 1}`;
    return `- [${label}](#${anchor}) — \`${part.partName}\``;
  }).join('\n');

  const docsSection = docsTop.length
    ? `## User Docs\n\n${docsTop.map(d => {
      const src = d.src ? `Source: [${d.src}](${d.src})\n\n` : '';
      return `### ${d.partName}\n\n${src}${d.text}`;
    }).join('\n\n')}\n\n---\n\n`
    : '';

  const partsSection = codeParts.length
    ? `## Parts\n\n${navLines}\n\n---\n\n${codeParts.map((part, i) => {
      const label = `Part ${i + 1} of ${codeParts.length}`;
      const heading = `${label} — ${part.partName}`;
      const src = part.src ? `Source: [${part.src}](${part.src})\n\n` : '';
      return `<a id="part-${i + 1}"></a>\n\n### ${heading}\n\n${src}\`\`\`${part.lang}\n${part.code}\n\`\`\``;
    }).join('\n\n')}`
    : '## Parts\n\n_No script/config/notecard parts found in this grouped example._';

  const licenseSection = licensesBottom.length
    ? `\n\n---\n\n## Licenses\n\n${licensesBottom.map(d => {
      const src = d.src ? `Source: [${d.src}](${d.src})\n\n` : '';
      return `### ${d.partName}\n\n${src}\`\`\`text\n${d.text}\n\`\`\``;
    }).join('\n\n')}`
    : '';

  const combinedBody = `${docsSection}${partsSection}${licenseSection}`;

  renderDoc({
    path: group.path,
    front_matter: {
      ...(partPayloads[0]?.data?.front_matter || {}),
      name: group.name,
      signature: '',
      description: group.description || '',
      source_part_index: '',
      source_part_total: String(codeParts.length || group.__part_total || parts.length),
    },
    body: combinedBody,
  });
}

// ── Mode switching ────────────────────────────────────────────────────────────
const toolsPaneEl = document.getElementById('tools-pane');
let toolsLoaded   = false;
let currentMode   = 'ide';

const idePaneEl     = document.getElementById('ide-pane');
const filesPaneEl = document.getElementById('files-pane');
let ideReady   = false;
let ideEditor  = null;
let ideInitPromise = null;
let ideLayoutRaf = 0;
let windowResizeTimer = 0;
let ideFilePath = null;   // currently open file path (relative to project root)
let ideDirty = false;
let ideInternalSet = false;
let ideTabs = [];
let ideActiveTabId = null;
let ideTabSeq = 1;
let ideRestoreDone = false;
let ideBusyDepth = 0;
let ideClosedTabs = [];
let ideKeybindsBound = false;
let ideWordWrapMode = 'on';
let filesLoaded  = false;
let filesSelectedPath = null;
let filesSelectedEntry = null;
let filesExpandedDirs = new Set();

function scheduleIdeLayout() {
  if (!ideEditor || currentMode !== 'ide') return;
  if (ideLayoutRaf) cancelAnimationFrame(ideLayoutRaf);
  ideLayoutRaf = requestAnimationFrame(() => {
    ideLayoutRaf = 0;
    try {
      ideEditor.layout();
    } catch (_) {}
  });
}

function beginLiveResize() {
  document.body.classList.add('window-live-resize');
}

function endLiveResize() {
  document.body.classList.remove('window-live-resize');
  scheduleIdeLayout();
}

window.addEventListener('resize', () => {
  beginLiveResize();
  if (windowResizeTimer) clearTimeout(windowResizeTimer);
  windowResizeTimer = setTimeout(() => {
    windowResizeTimer = 0;
    endLiveResize();
  }, 90);
});

// ── External editor state ─────────────────────────────────────────────────────
let ideIsExternalFile  = false;   // true when IDE is synced to a Firestorm temp file
let _extPendingContent = null;    // content received from Firestorm while user was editing
const IDE_TABS_KEY = 'lslcache-ide-tabs-v1';

// ── IndexedDB helpers for FileSystemFileHandle persistence ────────────────────
// FileSystemFileHandle objects cannot be serialised to JSON/localStorage but
// CAN be stored in IndexedDB.  On restore we re-request permission at first use.
const _IDB_NAME  = 'slcode-ide';
const _IDB_VER   = 1;
const _IDB_STORE = 'fileHandles';
function _idbOpen() {
  return new Promise((res, rej) => {
    const r = indexedDB.open(_IDB_NAME, _IDB_VER);
    r.onupgradeneeded = e => e.target.result.createObjectStore(_IDB_STORE);
    r.onsuccess = e => res(e.target.result);
    r.onerror   = e => rej(e.target.error);
  });
}
async function _idbPut(key, value) {
  try {
    const db = await _idbOpen();
    await new Promise((res, rej) => {
      const tx = db.transaction(_IDB_STORE, 'readwrite');
      tx.objectStore(_IDB_STORE).put(value, key);
      tx.oncomplete = res; tx.onerror = e => rej(e.target.error);
    });
    db.close();
  } catch (_) {}
}
async function _idbGet(key) {
  try {
    const db = await _idbOpen();
    const val = await new Promise((res, rej) => {
      const req = db.transaction(_IDB_STORE, 'readonly').objectStore(_IDB_STORE).get(key);
      req.onsuccess = e => res(e.target.result);
      req.onerror   = e => rej(e.target.error);
    });
    db.close(); return val;
  } catch (_) { return undefined; }
}
async function _idbDelete(key) {
  try {
    const db = await _idbOpen();
    await new Promise((res, rej) => {
      const tx = db.transaction(_IDB_STORE, 'readwrite');
      tx.objectStore(_IDB_STORE).delete(key);
      tx.oncomplete = res; tx.onerror = e => rej(e.target.error);
    });
    db.close();
  } catch (_) {}
}
// Debounced flush of all current tab fileHandles to IndexedDB
let _idbFlushTimer = null;
function _idbScheduleFlush() {
  clearTimeout(_idbFlushTimer);
  _idbFlushTimer = setTimeout(async () => {
    const ids = new Set(ideTabs.map(t => t.id));
    // Write handles for tabs that have them
    for (const tab of ideTabs) {
      if (tab.fileHandle) _idbPut(tab.id, tab.fileHandle);
      else _idbDelete(tab.id);
    }
    // Prune stale entries (closed tabs)
    try {
      const db = await _idbOpen();
      const keys = await new Promise((res, rej) => {
        const req = db.transaction(_IDB_STORE, 'readonly').objectStore(_IDB_STORE).getAllKeys();
        req.onsuccess = e => res(e.target.result); req.onerror = e => rej(e.target.error);
      });
      db.close();
      for (const k of keys) { if (!ids.has(k)) _idbDelete(k); }
    } catch (_) {}
  }, 500);
}

function normalizeRelPath(path) {
  return String(path || '').replace(/\\\\/g, '/').replace(/^\/+/, '').trim();
}

function joinRelPath(base, name) {
  const b = normalizeRelPath(base);
  const n = normalizeRelPath(name);
  if (!b) return n;
  if (!n) return b;
  return `${b}/${n}`;
}

function getSelectedDirectoryPath() {
  if (!filesSelectedPath || !filesSelectedEntry) return '';
  if (filesSelectedEntry.type === 'dir') return filesSelectedPath;
  const idx = filesSelectedPath.lastIndexOf('/');
  return idx >= 0 ? filesSelectedPath.slice(0, idx) : '';
}

// ── Name dialog — replaces all prompt() for new/rename/save-as ───────────────
let _nameDialogResolve = null;
const _nameDlg    = document.getElementById('name-dialog');
const _nameDlgInp = document.getElementById('name-dialog-input');

function showNameDialog(title, context, defaultValue) {
  return new Promise(resolve => {
    _nameDialogResolve = resolve;
    document.getElementById('name-dialog-title').textContent   = title;
    document.getElementById('name-dialog-context').textContent = context || '';
    _nameDlgInp.value = defaultValue || '';
    _nameDlg.style.display = 'flex';
    setTimeout(() => { _nameDlgInp.focus(); _nameDlgInp.select(); }, 30);
  });
}

function _closeNameDlg(value) {
  _nameDlg.style.display = 'none';
  if (_nameDialogResolve) {
    const v = typeof value === 'string' ? value.trim() : '';
    _nameDialogResolve(v || null);
    _nameDialogResolve = null;
  }
}

document.getElementById('name-dialog-ok').addEventListener('click', () => {
  _closeNameDlg(_nameDlgInp.value);
});
document.getElementById('name-dialog-cancel').addEventListener('click', () => _closeNameDlg(null));
_nameDlgInp.addEventListener('keydown', e => {
  if (e.key === 'Enter')  { e.preventDefault(); _closeNameDlg(_nameDlgInp.value); }
  if (e.key === 'Escape') { e.preventDefault(); _closeNameDlg(null); }
});
_nameDlg.addEventListener('click', e => {
  if (e.target === _nameDlg) _closeNameDlg(null);
});

// ── Right-click context menu ──────────────────────────────────────────────────
const _ctxMenu = document.getElementById('ctx-menu');

function showCtxMenu(x, y, items) {
  _ctxMenu.innerHTML = '';
  items.forEach(item => {
    if (item === '---') {
      const sep = document.createElement('div');
      sep.style.cssText = 'border-top:1px solid var(--border);margin:3px 0;';
      _ctxMenu.appendChild(sep);
      return;
    }
    const btn = document.createElement('button');
    const isDisabled = !!item.disabled;
    btn.style.cssText = 'display:block;width:100%;text-align:left;background:none;border:none;'
      + 'color:' + (isDisabled ? 'var(--muted)' : (item.danger ? 'var(--danger)' : 'var(--text)')) + ';'
      + 'padding:6px 14px;cursor:' + (isDisabled ? 'default' : 'pointer') + ';font-size:12px;white-space:nowrap;'
      + 'opacity:' + (isDisabled ? '.55' : '1') + ';';
    btn.textContent = item.label;
    if (!isDisabled) {
      btn.addEventListener('mouseenter', () => { btn.style.background = 'var(--bg)'; });
      btn.addEventListener('mouseleave', () => { btn.style.background = 'none'; });
      btn.addEventListener('click', () => { hideCtxMenu(); item.action(); });
    }
    _ctxMenu.appendChild(btn);
  });
  _ctxMenu.style.display = 'block';
  const rect = _ctxMenu.getBoundingClientRect();
  _ctxMenu.style.left = Math.min(x, window.innerWidth  - rect.width  - 4) + 'px';
  _ctxMenu.style.top  = Math.min(y, window.innerHeight - rect.height - 4) + 'px';
}

function hideCtxMenu() { _ctxMenu.style.display = 'none'; }
document.addEventListener('click', hideCtxMenu);

// ── New file / folder helpers (shared between toolbar buttons + context menu) ─
async function newFileInDir(dir) {
  const name = await showNameDialog(
    'New File',
    dir ? 'in ' + dir + '/' : 'project root',
    'untitled.lsl'
  );
  if (!name) return;
  const path = normalizeRelPath(dir ? dir + '/' + name : name);
  try {
    const res  = await fetch('/api/fs/write', {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ path, content: '' }),
    });
    const data = await res.json();
    if (data.error) { alert('Error: ' + data.error); return; }
    filesSelectedPath = path;
    loadFileTree(path);
  } catch (e) { alert('Failed: ' + e.message); }
}

async function newFolderInDir(dir) {
  const name = await showNameDialog(
    'New Folder',
    dir ? 'in ' + dir + '/' : 'project root',
    'new-folder'
  );
  if (!name) return;
  const path = normalizeRelPath(dir ? dir + '/' + name : name);
  try {
    const res  = await fetch('/api/fs/mkdir', {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ path }),
    });
    const data = await res.json();
    if (data.error) { alert('Error: ' + data.error); return; }
    filesSelectedPath = path;
    filesExpandedDirs.add(path);
    loadFileTree(path);
  } catch (e) { alert('Failed: ' + e.message); }
}

function updateIdeFileLabel() {
  const labelEl = document.getElementById('ide-file-label');
  const displayPath = ideFilePath || 'untitled.lsl';
  labelEl.textContent = ideDirty ? `${displayPath} *` : displayPath;
  labelEl.title = displayPath;
}

function ideInferLang(path) {
  return String(path || '').toLowerCase().endsWith('.lua') ? 'lua' : 'lsl';
}

function ideTabDisplayPath(tab) {
  return tab?.path || tab?.name || 'untitled.lsl';
}

function ideTabShortName(tab) {
  const full = ideTabDisplayPath(tab);
  const slash = Math.max(full.lastIndexOf('/'), full.lastIndexOf('\\'));
  return slash >= 0 ? full.slice(slash + 1) : full;
}

function ideTabLabel(tab) {
  const base = ideTabDisplayPath(tab);
  return tab?.dirty ? `${base} *` : base;
}

function ideTabShortLabel(tab) {
  const base = ideTabShortName(tab);
  return tab?.dirty ? `${base} *` : base;
}

function ideGetTab(tabId = ideActiveTabId) {
  return ideTabs.find(tab => tab.id === tabId) || null;
}

function ideGetActiveTab() {
  return ideGetTab(ideActiveTabId);
}

function ideNextUntitledName() {
  const names = new Set(ideTabs.map(tab => tab.path || tab.name || ''));
  if (!names.has('untitled.lsl')) return 'untitled.lsl';
  let idx = 2;
  while (names.has(`untitled-${idx}.lsl`)) idx += 1;
  return `untitled-${idx}.lsl`;
}

function ideSetBusy(message) {
  ideBusyDepth += 1;
  const overlay = document.getElementById('ide-loading-overlay');
  const text = document.getElementById('ide-loading-text');
  if (text) text.textContent = message || 'Loading…';
  if (overlay) overlay.classList.add('active');
}

function ideClearBusy() {
  ideBusyDepth = Math.max(0, ideBusyDepth - 1);
  if (ideBusyDepth > 0) return;
  const overlay = document.getElementById('ide-loading-overlay');
  if (overlay) overlay.classList.remove('active');
}

function idePersistSession() {
  try {
    const payload = {
      seq: ideTabSeq,
      active: ideActiveTabId,
      tabs: ideTabs.map(tab => ({
        id: tab.id,
        path: tab.path || null,
        name: tab.name || null,
        dirty: !!tab.dirty,
        isExternal: !!tab.isExternal,
        externalPath: tab.externalPath || '',
        content: tab.model ? tab.model.getValue() : (tab.content || ''),
      })),
    };
    localStorage.setItem(IDE_TABS_KEY, JSON.stringify(payload));
  } catch (_) {}
  _idbScheduleFlush();
  // Sync to server so other instances (browser ↔ app) share the same session
  clearTimeout(_sessionSyncTimer);
  _sessionSyncTimer = setTimeout(() => {
    try {
      const payload = JSON.parse(localStorage.getItem(IDE_TABS_KEY) || 'null');
      if (payload) fetch('/api/session', {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload),
      }).catch(() => {});
    } catch (_) {}
  }, 800);
}
let _sessionSyncTimer = null;

function ideRefreshExternalBanner() {
  const tab = ideGetActiveTab();
  const banner = document.getElementById('ide-ext-banner');
  if (tab && tab.isExternal) {
    banner.classList.add('active');
    document.getElementById('ide-ext-path').textContent = tab.externalPath || ideTabDisplayPath(tab);
    document.getElementById('ide-unwatch-btn').style.display = '';
    document.getElementById('ide-watch-btn').style.display = 'none';
  } else {
    banner.classList.remove('active');
    document.getElementById('ide-ext-path').textContent = '';
    document.getElementById('ide-ext-status').textContent = '';
    document.getElementById('ide-ext-reload-btn').style.display = 'none';
    document.getElementById('ide-unwatch-btn').style.display = 'none';
    document.getElementById('ide-watch-btn').style.display = '';
  }
}

function ideSyncActiveState() {
  const tab = ideGetActiveTab();
  ideFilePath = tab ? ideTabDisplayPath(tab) : null;
  ideDirty = tab ? !!tab.dirty : false;
  ideIsExternalFile = tab ? !!tab.isExternal : false;
  updateIdeFileLabel();
  ideRefreshExternalBanner();
  refreshDebugIdeTabOptions();
}

function renderIdeTabs() {
  const bar = document.getElementById('ide-tabs-bar');
  if (!bar) return;
  if (!ideTabs.length) {
    bar.innerHTML = '<div id="ide-tabs-empty">No open tabs</div>';
    return;
  }
  bar.innerHTML = ideTabs.map(tab => `
    <div class="ide-tab${tab.id === ideActiveTabId ? ' active' : ''}" data-tab-id="${esc(tab.id)}" title="${esc(ideTabLabel(tab))}">
      <span class="ide-tab-label">${esc(ideTabShortLabel(tab))}</span>
      <button class="ide-tab-close" data-tab-close="${esc(tab.id)}" title="Close tab">&#10005;</button>
    </div>`).join('');
  bar.querySelectorAll('[data-tab-id]').forEach(el => {
    el.addEventListener('click', e => {
      if (e.target.closest('[data-tab-close]')) return;
      ideActivateTab(el.dataset.tabId);
    });
    el.addEventListener('auxclick', e => {
      if (e.button !== 1) return;
      e.preventDefault();
      ideCloseTab(el.dataset.tabId);
    });
    el.addEventListener('mousedown', e => {
      if (e.button !== 1) return;
      e.preventDefault();
    });
    el.addEventListener('contextmenu', e => {
      e.preventDefault();
      const tabId = el.dataset.tabId;
      ideActivateTab(tabId);
      const menuItems = [
        { label: 'Close', action: () => ideCloseTab(tabId) },
        { label: 'Close Others', action: () => ideCloseOtherTabs(tabId) },
      ];
      if (ideClosedTabs.length) {
        menuItems.push({ label: 'Reopen Closed Tab', action: () => ideReopenLastClosedTab() });
      }
      menuItems.push('---');
      menuItems.push({ label: 'Close All', danger: true, action: () => ideCloseAllTabs() });
      showCtxMenu(e.clientX, e.clientY, menuItems);
    });
  });
  bar.querySelectorAll('[data-tab-close]').forEach(el => {
    el.addEventListener('click', e => {
      e.stopPropagation();
      ideCloseTab(el.dataset.tabClose);
    });
  });
  const activeTabEl = bar.querySelector('.ide-tab.active');
  if (activeTabEl) {
    activeTabEl.scrollIntoView({ behavior: 'auto', block: 'nearest', inline: 'nearest' });
  }
}

function ideAttachModel(tab, content) {
  const model = monaco.editor.createModel(content || '', ideInferLang(tab.path || tab.name));
  tab.model = model;
  tab._changeDisposable = model.onDidChangeContent(() => {
    if (!tab.dirty) tab.dirty = true;
    if (tab.id === ideActiveTabId) ideDirty = true;
    renderIdeTabs();
    updateIdeFileLabel();
    idePersistSession();
    refreshDebugIdeTabOptions();
  });
}

function _ideRenderCheckResults(issues, stats) {
  const listEl = document.getElementById('ide-issues-list');
  if (!listEl) return;
  if (!issues) {
    listEl.innerHTML = '<div style="padding:20px;text-align:center;color:var(--muted);font-size:12px">\u25b6 Run Check to see issues</div>';
    return;
  }
  if (!issues.length) {
    listEl.innerHTML = '<div style="padding:20px;text-align:center;color:var(--green);font-size:13px">\u2713 No issues</div>';
    return;
  }
  listEl.innerHTML = issues.map(iss => `<div class="issue-row" data-line="${iss.line}" style="cursor:pointer;">
    <span class="issue-sev sev-${esc(iss.severity)}">${esc(iss.severity)}</span>
    ${iss.line ? `<span class="issue-line">:${iss.line}</span>` : '<span class="issue-line"></span>'}
    <div class="issue-body">
      <div class="issue-code">${esc(iss.code)}</div>
      <div class="issue-msg">${esc(iss.message)}</div>
    </div>
  </div>`).join('');
  listEl.querySelectorAll('.issue-row[data-line]').forEach(row => {
    row.addEventListener('click', () => {
      const ln = parseInt(row.dataset.line, 10);
      if (ideEditor && ln) {
        ideEditor.revealLineInCenter(ln);
        ideEditor.setSelection({ startLineNumber: ln, startColumn: 1, endLineNumber: ln, endColumn: 999 });
        ideEditor.focus();
      }
    });
  });
}

function ideActivateTab(tabId) {
  const tab = ideGetTab(tabId);
  if (!tab) return;
  ideActiveTabId = tab.id;
  if (ideEditor && tab.model) {
    ideInternalSet = true;
    ideEditor.setModel(tab.model);
    ideInternalSet = false;
    ideEditor.focus();
  }
  renderIdeTabs();
  ideSyncActiveState();
  idePersistSession();
  // Restore per-tab check results in the issues sidebar
  _ideRenderCheckResults(tab.checkIssues ?? null, tab.checkStats ?? null);
}

function ideOpenTab(path, content, opts = {}) {
  const normalizedPath = opts.isExternal ? String(path || '') : normalizeRelPath(path);
  const existing = !opts.forceNew && normalizedPath
    ? ideTabs.find(tab => (tab.path || '') === normalizedPath && !!tab.isExternal === !!opts.isExternal)
    : null;
  if (existing) {
    ideActivateTab(existing.id);
    return existing;
  }
  const tab = {
    id: `ide-tab-${ideTabSeq++}`,
    path: normalizedPath || null,
    name: opts.name || (!normalizedPath ? ideNextUntitledName() : null),
    dirty: !!opts.dirty,
    isExternal: !!opts.isExternal,
    externalPath: opts.externalPath || (opts.isExternal ? String(path || '') : ''),
    model: null,
    _changeDisposable: null,
  };
  ideAttachModel(tab, content || '');
  ideTabs.push(tab);
  renderIdeTabs();
  if (opts.activate === false) idePersistSession();
  else ideActivateTab(tab.id);
  return tab;
}

function ideCreateUntitledTab() {
  return ideOpenTab('', '', { forceNew: true, name: ideNextUntitledName() });
}

function ideActivateTabByOffset(offset) {
  if (!ideTabs.length) return;
  const idx = ideTabs.findIndex(tab => tab.id === ideActiveTabId);
  const start = idx >= 0 ? idx : 0;
  const next = (start + offset + ideTabs.length) % ideTabs.length;
  ideActivateTab(ideTabs[next].id);
}

function ideReopenLastClosedTab() {
  const snap = ideClosedTabs.pop();
  if (!snap) {
    const statusEl = document.getElementById('ide-status');
    statusEl.textContent = 'No recently closed tab';
    setTimeout(() => { if (statusEl.textContent === 'No recently closed tab') statusEl.textContent = ''; }, 1500);
    return null;
  }
  const reopened = ideOpenTab(snap.path || '', snap.content || '', {
    forceNew: true,
    name: snap.name || null,
    dirty: !!snap.dirty,
    isExternal: !!snap.isExternal,
    externalPath: snap.externalPath || '',
  });
  if (reopened) {
    reopened.dirty = !!snap.dirty;
    ideSyncActiveState();
    renderIdeTabs();
    idePersistSession();
  }
  return reopened;
}

async function ideSaveAllTabs() {
  const statusEl = document.getElementById('ide-status');
  let saved = 0, skipped = 0, failed = 0;
  for (const tab of ideTabs) {
    if (!tab.dirty) continue;
    if (tab.isExternal) {
      if (tab.id === ideActiveTabId) {
        await ideFileSave(false);
        if (!tab.dirty) saved += 1; else failed += 1;
      } else {
        skipped += 1;
      }
      continue;
    }
    const path = normalizeRelPath(tab.path || '');
    if (!path) { skipped += 1; continue; }
    try {
      const res = await fetch('/api/fs/write', {
        method: 'POST', headers: {'Content-Type':'application/json'},
        body: JSON.stringify({ path, content: tab.model ? tab.model.getValue() : '' }),
      });
      const data = await res.json();
      if (data.error) {
        failed += 1;
      } else {
        tab.dirty = false;
        saved += 1;
      }
    } catch (_) {
      failed += 1;
    }
  }
  ideSyncActiveState();
  renderIdeTabs();
  idePersistSession();
  statusEl.textContent = failed
    ? `Saved ${saved}, failed ${failed}${skipped ? `, skipped ${skipped}` : ''}`
    : `Saved ${saved} tab(s)${skipped ? `, skipped ${skipped}` : ''}`;
  setTimeout(() => { statusEl.textContent = ''; }, 2200);
}

function updateIdeWrapButton() {
  const btn = document.getElementById('ide-wrap-btn');
  if (!btn) return;
  const on = ideWordWrapMode === 'on';
  btn.textContent = on ? 'Wrap: On' : 'Wrap: Off';
  btn.style.borderColor = on ? 'var(--accent)' : '';
  btn.style.color = on ? 'var(--accent)' : '';
}

function ideUndo() {
  if (!ideEditor) return;
  ideEditor.trigger('keyboard', 'undo', null);
}

function ideRedo() {
  if (!ideEditor) return;
  ideEditor.trigger('keyboard', 'redo', null);
}

function ideSelectAll() {
  if (!ideEditor) return;
  const model = ideEditor.getModel();
  if (!model) return;
  ideEditor.setSelection(model.getFullModelRange());
  ideEditor.focus();
}

function ideSelectNone() {
  if (!ideEditor) return;
  const pos = ideEditor.getPosition();
  if (!pos) return;
  ideEditor.setSelection(new monaco.Selection(pos.lineNumber, pos.column, pos.lineNumber, pos.column));
  ideEditor.focus();
}

function ideCut() {
  if (!ideEditor) return;
  ideEditor.focus();
  ideEditor.trigger('keyboard', 'editor.action.clipboardCutAction', null);
}

function ideCopy() {
  if (!ideEditor) return;
  ideEditor.focus();
  ideEditor.trigger('keyboard', 'editor.action.clipboardCopyAction', null);
}

function idePaste() {
  if (!ideEditor) return;
  ideEditor.focus();
  ideEditor.trigger('keyboard', 'editor.action.clipboardPasteAction', null);
}

function ideInvertSelection() {
  if (!ideEditor) return;
  const model = ideEditor.getModel();
  const sel = ideEditor.getSelection();
  if (!model || !sel) return;
  const full = model.getFullModelRange();
  if (sel.isEmpty()) {
    ideEditor.setSelection(full);
    ideEditor.focus();
    return;
  }

  const beforeExists = sel.startLineNumber > full.startLineNumber
    || (sel.startLineNumber === full.startLineNumber && sel.startColumn > full.startColumn);
  const afterExists = sel.endLineNumber < full.endLineNumber
    || (sel.endLineNumber === full.endLineNumber && sel.endColumn < full.endColumn);

  const selections = [];
  if (beforeExists) {
    selections.push(new monaco.Selection(
      full.startLineNumber, full.startColumn,
      sel.startLineNumber, sel.startColumn
    ));
  }
  if (afterExists) {
    selections.push(new monaco.Selection(
      sel.endLineNumber, sel.endColumn,
      full.endLineNumber, full.endColumn
    ));
  }

  if (!selections.length) {
    ideSelectNone();
    return;
  }
  ideEditor.setSelections(selections);
  ideEditor.focus();
}

function ideHasSelection() {
  if (!ideEditor) return false;
  const sel = ideEditor.getSelection();
  return !!sel && !sel.isEmpty();
}

function ideToggleWordWrap() {
  ideWordWrapMode = ideWordWrapMode === 'on' ? 'off' : 'on';
  if (ideEditor) ideEditor.updateOptions({ wordWrap: ideWordWrapMode });
  updateIdeWrapButton();
}

function showIdeEditorContextMenu(x, y) {
  const hasEditor = !!ideEditor;
  const hasSelection = ideHasSelection();
  showCtxMenu(x, y, [
    { label: 'Undo (Ctrl+Z)', action: () => ideUndo(), disabled: !hasEditor },
    { label: 'Redo (Ctrl+Y)', action: () => ideRedo(), disabled: !hasEditor },
    '---',
    { label: 'Cut (Ctrl+X)', action: () => ideCut(), disabled: !hasEditor || !hasSelection },
    { label: 'Copy (Ctrl+C)', action: () => ideCopy(), disabled: !hasEditor || !hasSelection },
    { label: 'Paste (Ctrl+V)', action: () => idePaste(), disabled: !hasEditor },
    '---',
    { label: 'Select All (Ctrl+A)', action: () => ideSelectAll(), disabled: !hasEditor },
    { label: 'Select None (Ctrl+Shift+A)', action: () => ideSelectNone(), disabled: !hasEditor || !hasSelection },
    { label: 'Invert Selection (Ctrl+Alt+I)', action: () => ideInvertSelection(), disabled: !hasEditor || !hasSelection },
    '---',
    { label: ideWordWrapMode === 'on' ? 'Word Wrap: On (Alt+Z)' : 'Word Wrap: Off (Alt+Z)', action: () => ideToggleWordWrap(), disabled: !hasEditor },
  ]);
}

function bindIdeGlobalKeybinds() {
  if (ideKeybindsBound) return;
  ideKeybindsBound = true;
  document.addEventListener('keydown', async e => {
    if (currentMode !== 'ide') return;
    if (e.altKey && (e.key || '').toLowerCase() === 'z' && !e.ctrlKey && !e.metaKey) {
      e.preventDefault();
      ideToggleWordWrap();
      return;
    }
    const ctrlOrCmd = e.ctrlKey || e.metaKey;
    if (!ctrlOrCmd) return;
    if (e.key === 'Tab') {
      e.preventDefault();
      ideActivateTabByOffset(e.shiftKey ? -1 : 1);
      return;
    }
    const key = (e.key || '').toLowerCase();
    if (key === 'w' && !e.shiftKey) {
      e.preventDefault();
      const tab = ideGetActiveTab();
      if (tab) ideCloseTab(tab.id);
      return;
    }
    if (key === 'z' && !e.shiftKey && !e.altKey) {
      e.preventDefault();
      ideUndo();
      return;
    }
    if ((key === 'y' && !e.shiftKey && !e.altKey) || (key === 'z' && e.shiftKey && !e.altKey)) {
      e.preventDefault();
      ideRedo();
      return;
    }
    if (key === 'a' && !e.shiftKey && !e.altKey) {
      e.preventDefault();
      ideSelectAll();
      return;
    }
    if (key === 'x' && !e.shiftKey && !e.altKey) {
      e.preventDefault();
      ideCut();
      return;
    }
    if (key === 'c' && !e.shiftKey && !e.altKey) {
      e.preventDefault();
      ideCopy();
      return;
    }
    if (key === 'v' && !e.shiftKey && !e.altKey) {
      e.preventDefault();
      idePaste();
      return;
    }
    if (key === 'a' && e.shiftKey && !e.altKey) {
      e.preventDefault();
      ideSelectNone();
      return;
    }
    if (key === 'i' && e.altKey) {
      e.preventDefault();
      ideInvertSelection();
      return;
    }
    if (key === 't' && e.shiftKey) {
      e.preventDefault();
      ideReopenLastClosedTab();
      return;
    }
    if (key === 's' && e.shiftKey) {
      e.preventDefault();
      await ideSaveAllTabs();
      return;
    }
    if (key === 'o' && !e.shiftKey) {
      e.preventDefault();
      document.getElementById('ide-open-btn').click();
      return;
    }
    if (key === 'n' && !e.shiftKey) {
      e.preventDefault();
      document.getElementById('ide-new-btn').click();
    }
  });
}

function ideCloseTab(tabId, opts = {}) {
  const tab = ideGetTab(tabId);
  if (!tab) return false;
  if (!opts.skipGuard && tab.dirty) {
    if (!confirm(`Close ${ideTabDisplayPath(tab)} with unsaved changes?`)) return false;
  }
  const idx = ideTabs.findIndex(item => item.id === tabId);
  if (idx < 0) return false;
  if (!opts.skipHistory) {
    ideClosedTabs.push({
      path: tab.path || null,
      name: tab.name || null,
      dirty: !!tab.dirty,
      isExternal: !!tab.isExternal,
      externalPath: tab.externalPath || '',
      content: tab.model ? tab.model.getValue() : '',
    });
    if (ideClosedTabs.length > 30) ideClosedTabs = ideClosedTabs.slice(-30);
  }
  if (tab._changeDisposable) tab._changeDisposable.dispose();
  if (tab.model) tab.model.dispose();
  _idbDelete(tab.id);
  ideTabs.splice(idx, 1);
  if (!ideTabs.length) {
    ideCreateUntitledTab();
  } else if (ideActiveTabId === tabId) {
    const next = ideTabs[Math.max(0, idx - 1)] || ideTabs[0];
    ideActivateTab(next.id);
  } else {
    renderIdeTabs();
    ideSyncActiveState();
    idePersistSession();
  }
  return true;
}

function ideCloseOtherTabs(keepTabId) {
  const toClose = ideTabs.filter(tab => tab.id !== keepTabId).map(tab => tab.id);
  for (const tabId of toClose) {
    if (!ideCloseTab(tabId)) return false;
  }
  return true;
}

function ideCloseAllTabs() {
  const toClose = ideTabs.map(tab => tab.id);
  for (const tabId of toClose) {
    if (!ideCloseTab(tabId)) return false;
  }
  return true;
}

async function ideRestoreSession() {
  if (ideRestoreDone) return;
  ideRestoreDone = true;
  let data = null;
  // Try server first (shared across browser ↔ app instances)
  try {
    const res = await fetch('/api/session');
    if (res.ok) {
      const srv = await res.json();
      if (srv && Array.isArray(srv.tabs) && srv.tabs.length) {
        data = srv;
        // Keep localStorage in sync
        try { localStorage.setItem(IDE_TABS_KEY, JSON.stringify(srv)); } catch (_) {}
      }
    }
  } catch (_) {}
  // Fall back to localStorage (GitHub Pages / offline)
  if (!data) {
    try {
      const raw = localStorage.getItem(IDE_TABS_KEY);
      if (raw) data = JSON.parse(raw);
    } catch (_) {}
  }
  let restored = false;
  if (data && Array.isArray(data.tabs) && data.tabs.length) {
    ideTabSeq = Math.max(ideTabSeq, Number(data.seq) || 1);
    data.tabs.forEach(tab => {
      ideOpenTab(tab.path || '', tab.content || '', {
        activate: false,
        forceNew: true,
        name: tab.name || null,
        dirty: !!tab.dirty,
        isExternal: !!tab.isExternal,
        externalPath: tab.externalPath || '',
      });
    });
    restored = true;
    ideActivateTab(ideGetTab(data.active)?.id || ideTabs[0].id);
  }
  if (!restored) ideCreateUntitledTab();
  refreshDebugIdeTabOptions();
  // Restore FileSystemFileHandles from IndexedDB (async, best-effort)
  for (const tab of ideTabs) {
    const handle = await _idbGet(tab.id);
    if (handle) tab.fileHandle = handle;
  }
}

function refreshDebugIdeTabOptions() {
  const selectEl = document.getElementById('debug-ide-tab-select');
  if (!selectEl) return;
  const prev = selectEl.value || '';
  selectEl.innerHTML = '';
  const first = document.createElement('option');
  first.value = '';
  first.textContent = 'Open IDE tab…';
  selectEl.appendChild(first);
  ideTabs.forEach(tab => {
    const opt = document.createElement('option');
    opt.value = tab.id;
    opt.textContent = ideTabLabel(tab);
    selectEl.appendChild(opt);
  });
  if (prev && ideGetTab(prev)) selectEl.value = prev;
  else selectEl.value = '';
  selectEl.disabled = !ideTabs.length;
}

function loadDebugFromIdeTab(tabId) {
  const tab = ideGetTab(tabId);
  if (!tab || !tab.model) return;
  const content = tab.model.getValue();
  if (!content.trim()) {
    statsEl.textContent = 'Selected IDE tab is empty.';
    return;
  }
  sourceEl.value = content;
  debugSourceTabId = tab.id;
  const label = ideTabDisplayPath(tab);
  document.getElementById('file-label').textContent = label;
  document.getElementById('file-label').title       = label;
  issuesEl.innerHTML = `<div id="issues-empty"><div class="big" style="opacity:.2">&#9881;</div><div>Loaded from IDE tab (${esc(label)}) — press Ctrl+Enter to check</div></div>`;
  statsEl.textContent = '';
  sourceEl.focus();
}

function confirmDiscardIdeChanges() {
  if (!ideDirty || ideIsExternalFile) return true;
  return confirm('You have unsaved IDE changes. Continue and discard them?');
}

function setMode(mode) {
  hideSearchDrop();
  currentMode = mode;
  document.body.dataset.mode = mode;
  document.querySelectorAll('.mode-btn').forEach(b =>
    b.classList.toggle('active', b.dataset.mode === mode));

  mainEl.style.display         = mode === 'library' ? 'flex' : 'none';
  debugPane.style.display      = mode === 'debug'   ? 'flex' : 'none';
  toolsPaneEl.style.display    = mode === 'tools'   ? 'flex' : 'none';
  idePaneEl.style.display      = mode === 'ide'     ? 'flex' : 'none';
  filesPaneEl.style.display  = mode === 'files'  ? 'flex' : 'none';

  if (mode === 'library') {
    searchEl.focus();
  } else {
    subtabsEl.innerHTML = '';
    subtabsEl.className = '';
  }
  if (mode === 'debug') {
    sourceEl.focus();
  } else if (mode === 'tools') {
    if (!toolsLoaded) { toolsLoaded = true; loadCacheStatus(); loadCacheTools(); }
  } else if (mode === 'ide') {
    if (!ideReady) initIde().then(() => {
      scheduleIdeLayout();
      if (ideEditor) ideEditor.focus();
    });
    else if (ideEditor) {
      scheduleIdeLayout();
      ideEditor.focus();
    }
  } else if (mode === 'files') {
    if (!filesLoaded) { filesLoaded = true; loadCwd(); loadFileTree(); loadGitStatus(); }
  }
}

// ── IDE (Monaco) ──────────────────────────────────────────────────────────────
function initIde() {
  if (ideInitPromise) return ideInitPromise;
  ideReady = true;
  const wrap = document.getElementById('ide-editor-wrap');
  ideInitPromise = new Promise((resolve, reject) => {
    const finishInit = () => {
      require.config({ paths: { 'vs': 'https://cdn.jsdelivr.net/npm/monaco-editor@0.47.0/min/vs' } });
      require(['vs/editor/editor.main'], () => {
        registerLslLanguage();
        const wrapEl = document.getElementById('ide-editor-wrap');
        ideEditor = monaco.editor.create(wrap, {
          value: '',
          language: 'lsl',
          theme: 'lsl-dark',
          fontSize: 13,
          fontFamily: "'JetBrains Mono','Fira Code','Cascadia Code',monospace",
          minimap: { enabled: true },
          wordWrap: 'on',
          scrollBeyondLastLine: false,
          renderLineHighlight: 'all',
          suggestOnTriggerCharacters: true,
          quickSuggestions: true,
          tabSize: 4,
          insertSpaces: true,
          automaticLayout: false,
        });

        scheduleIdeLayout();

        if (wrapEl) {
          wrapEl.addEventListener('contextmenu', e => {
            if (currentMode !== 'ide' || !ideEditor) return;
            e.preventDefault();
            e.stopPropagation();
            showIdeEditorContextMenu(e.clientX, e.clientY);
          }, true);
        }

        monaco.languages.registerCompletionItemProvider('lsl', {
          provideCompletionItems: async (model, position) => {
            if (!_ideCompletionsEnabled) return { suggestions: [] };
            const word  = model.getWordUntilPosition(position);
            const range = {
              startLineNumber: position.lineNumber, endLineNumber: position.lineNumber,
              startColumn: word.startColumn,        endColumn:   word.endColumn,
            };
            const items = await fetchLslCompletions();
            return { suggestions: items.map(s => ({ ...s, range })) };
          }
        });

        ideEditor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyS, ideFileSave);
        ideEditor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, ideRunCheck);
        ideEditor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyMod.Shift | monaco.KeyCode.KeyN, () => document.getElementById('ide-new-btn').click());
        ideEditor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyN, () => document.getElementById('ide-new-btn').click());
        ideEditor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyO, () => document.getElementById('ide-open-btn').click());
        ideEditor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyZ, ideUndo);
        ideEditor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyY, ideRedo);
        ideEditor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyMod.Shift | monaco.KeyCode.KeyZ, ideRedo);
        ideEditor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyX, ideCut);
        ideEditor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyC, ideCopy);
        ideEditor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyV, idePaste);
        ideEditor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyA, ideSelectAll);
        ideEditor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyMod.Shift | monaco.KeyCode.KeyA, ideSelectNone);
        ideEditor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyMod.Alt | monaco.KeyCode.KeyI, ideInvertSelection);
        ideEditor.addCommand(monaco.KeyMod.Alt | monaco.KeyCode.KeyZ, ideToggleWordWrap);
        ideEditor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyW, () => {
          const tab = ideGetActiveTab();
          if (tab) ideCloseTab(tab.id);
        });
        ideEditor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyMod.Shift | monaco.KeyCode.KeyT, () => ideReopenLastClosedTab());
        ideEditor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyMod.Shift | monaco.KeyCode.KeyS, () => ideSaveAllTabs());
        ideEditor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Tab, () => ideActivateTabByOffset(1));
        ideEditor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyMod.Shift | monaco.KeyCode.Tab, () => ideActivateTabByOffset(-1));

        bindIdeGlobalKeybinds();
        updateIdeWrapButton();

        ideRestoreSession().then(() => {
          ideEditor.focus();
          ideSyncActiveState();
          resolve();
        });
      });
    };

    if (window.require && window.monaco) {
      finishInit();
      return;
    }

    const loaderScript = document.createElement('script');
    loaderScript.src = 'https://cdn.jsdelivr.net/npm/monaco-editor@0.47.0/min/vs/loader.js';
    loaderScript.onload = finishInit;
    loaderScript.onerror = () => reject(new Error('Failed to load Monaco editor'));
    document.head.appendChild(loaderScript);
  });
  return ideInitPromise;
}

function registerLslLanguage() {
  monaco.languages.register({ id: 'lsl' });

  monaco.languages.setMonarchTokensProvider('lsl', {
    keywords: [
      'default','state','event','if','elseif','else','while','for','do','jump','return',
      'integer','float','string','list','vector','rotation','key',
      'TRUE','FALSE','NULL_KEY','ZERO_VECTOR','ZERO_ROTATION',
    ],
    operators: ['=','+','-','*','/','%','<','>','<=','>=','==','!=','&&','||','!','&','|','^','~','<<','>>','+=','-=','*=','/=','%='],
    tokenizer: {
      root: [
        [/\/\/.*$/, 'comment'],
        [/\/\*/, 'comment', '@comment'],
        [/"([^"\\]|\\.)*"/, 'string'],
        [/\b(ll[A-Z]\w*)\b/, 'type.identifier'],         // ll* functions
        [/\b(os[A-Z]\w*)\b/, 'type.identifier'],         // os* (OSSL)
        [/\b[A-Z][A-Z0-9_]+\b/, 'constant'],             // CONSTANTS
        [/\b(integer|float|string|list|vector|rotation|key)\b/, 'keyword.type'],
        [/\b(default|state|elseif|if|else|while|for|do|jump|return|event)\b/, 'keyword'],
        [/\b(TRUE|FALSE|NULL_KEY|ZERO_VECTOR|ZERO_ROTATION)\b/, 'constant'],
        [/\d+\.\d*([eE][+-]?\d+)?/, 'number.float'],
        [/\d+/, 'number'],
        [/[{}()\[\]]/, 'delimiter'],
        [/[<>;,@]/, 'delimiter'],
      ],
      comment: [
        [/[^/*]+/, 'comment'],
        [/\*\//, 'comment', '@pop'],
        [/[/*]/, 'comment'],
      ],
    }
  });

  monaco.editor.defineTheme('lsl-dark', {
    base: 'vs-dark',
    inherit: true,
    rules: [
      { token: 'comment',         foreground: '6a737d', fontStyle: 'italic' },
      { token: 'string',          foreground: '9ecbff' },
      { token: 'keyword',         foreground: 'f97583' },
      { token: 'keyword.type',    foreground: '79b8ff' },
      { token: 'type.identifier', foreground: 'b392f0' },
      { token: 'constant',        foreground: 'ffab70' },
      { token: 'number',          foreground: '79b8ff' },
      { token: 'number.float',    foreground: '79b8ff' },
      { token: 'delimiter',       foreground: 'e1e4e8' },
    ],
    colors: {
      'editor.background': '#0f1117',
      'editor.foreground': '#d4d8f0',
      'editorLineNumber.foreground': '#444c5e',
      'editor.lineHighlightBackground': '#1a1d27',
      'editorCursor.foreground': '#4f8ef7',
      'editor.selectionBackground': '#264f78',
    }
  });
}

let _lslCompletions = null;
async function fetchLslCompletions() {
  if (_lslCompletions) return _lslCompletions;
  try {
    const res  = await fetch('/api/ide/completions');
    const data = await res.json();
    _lslCompletions = data.map(item => ({
      label:            item.label,
      kind:             item.kind === 'function'  ? monaco.languages.CompletionItemKind.Function
                      : item.kind === 'constant'  ? monaco.languages.CompletionItemKind.Constant
                      : item.kind === 'event'     ? monaco.languages.CompletionItemKind.Event
                      : item.kind === 'snippet'   ? monaco.languages.CompletionItemKind.Snippet
                      : monaco.languages.CompletionItemKind.Text,
      insertText:       item.snippet || item.label,
      insertTextRules:  monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
      documentation:    item.description || '',
      detail:           item.signature   || '',
    }));
    return _lslCompletions;
  } catch (e) {
    return [];
  }
}

async function ideRunCheck() {
  if (!ideEditor) return;
  const tab = ideGetActiveTab();
  if (!tab) return;
  const source = tab.model ? tab.model.getValue() : ideEditor.getValue();
  if (!source.trim()) return;
  const statusEl = document.getElementById('ide-status');
  const listEl   = document.getElementById('ide-issues-list');
  statusEl.textContent = 'Checking\u2026';
  listEl.innerHTML = '<div style="padding:12px;color:var(--muted);font-size:12px">Running checks\u2026</div>';
  try {
    const res  = await fetch('/api/check', {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ source, mode: 'both', ossl: ideOsslMode, firestorm: ideFsMode }),
    });
    const data = await res.json();
    if (data.error) { statusEl.textContent = 'Error: ' + data.error; return; }
    const { issues, stats } = data;
    // Store results on the tab so they survive tab switches
    tab.checkIssues = issues;
    tab.checkStats  = stats;
    const parts = [];
    if (stats.errors)   parts.push(`${stats.errors}E`);
    if (stats.warnings) parts.push(`${stats.warnings}W`);
    if (stats.infos)    parts.push(`${stats.infos}I`);
    statusEl.textContent = parts.length ? parts.join(' ') : '\u2713 Clean';
    // Update Monaco markers on this tab's model
    const markers = issues.map(iss => ({
      severity: iss.severity === 'ERROR' ? monaco.MarkerSeverity.Error
              : iss.severity === 'WARN'  ? monaco.MarkerSeverity.Warning
              : monaco.MarkerSeverity.Info,
      message:     iss.message,
      startLineNumber: iss.line || 1, startColumn: 1,
      endLineNumber:   iss.line || 1, endColumn:   999,
    }));
    monaco.editor.setModelMarkers(tab.model, 'lsl-checker', markers);
    // Render into the sidebar (only if this tab is still active)
    if (ideActiveTabId === tab.id) _ideRenderCheckResults(issues, stats);
  } catch (e) {
    statusEl.textContent = 'Failed: ' + e.message;
  }
}

// Write content via the File System Access API fileHandle stored on the tab.
// Returns true on success, false on permission error (caller should re-pick).
async function _ideWriteViaHandle(tab, source) {
  try {
    if ((await tab.fileHandle.queryPermission({ mode: 'readwrite' })) !== 'granted') {
      await tab.fileHandle.requestPermission({ mode: 'readwrite' });
    }
    const writable = await tab.fileHandle.createWritable();
    await writable.write(source);
    await writable.close();
    return true;
  } catch (_) {
    return false;
  }
}

async function ideFileSave(forceSaveAs = false) {
  if (!ideEditor) return;
  const tab = ideGetActiveTab();
  if (!tab) return;
  const source   = tab.model ? tab.model.getValue() : ideEditor.getValue();
  const statusEl = document.getElementById('ide-status');
  statusEl.textContent = 'Saving\u2026';
  try {
    if (tab.isExternal) {
      // Write back to the Firestorm temp file (absolute path, bypasses sandbox)
      const res = await fetch('/api/external/write', {
        method: 'POST', headers: {'Content-Type':'application/json'},
        body: JSON.stringify({ content: source }),
      });
      const data = await res.json();
      if (data.error) { statusEl.textContent = 'Save error: ' + data.error; return; }
      document.getElementById('ide-ext-status').textContent = 'Saved \u2713';
      tab.dirty = false;
      ideSyncActiveState();
      renderIdeTabs();
      statusEl.textContent = '\u2713 Saved';
      setTimeout(() => { statusEl.textContent = ''; }, 2000);
      return;
    }

    let pathToSave = normalizeRelPath(tab.path || tab.name || '');
    const needPicker = !pathToSave || forceSaveAs;

    // ── Path already known + fileHandle stored: write directly ───────────────
    if (!needPicker && tab.fileHandle) {
      const ok = await _ideWriteViaHandle(tab, source);
      if (ok) {
        tab.dirty = false;
        ideSyncActiveState();
        renderIdeTabs();
        idePersistSession();
        loadFileTree(tab.path);
        statusEl.textContent = '\u2713 Saved';
        setTimeout(() => { statusEl.textContent = ''; }, 2000);
        return;
      }
      // Permission revoked — clear path so picker shows below
      tab.fileHandle = null;
      pathToSave = '';
    }

    // ── Need a path: pick via dialog ─────────────────────────────────────────
    if (needPicker || (!pathToSave && !tab.fileHandle)) {
      const suggestedName = (pathToSave ? pathToSave.split('/').pop() : '') || 'untitled.lsl';

      if (window.pywebview?.api?.save_file_dialog) {
        // webview mode — native dialog via pywebview
        const dlg = await window.pywebview.api.save_file_dialog(
          pathToSave || joinRelPath(getSelectedDirectoryPath(), suggestedName) || suggestedName
        );
        if (!dlg || dlg.cancelled) { statusEl.textContent = ''; return; }
        if (dlg.error) { statusEl.textContent = 'Save error: ' + dlg.error; return; }
        pathToSave = normalizeRelPath(dlg.path || '');

      } else if (typeof window.showSaveFilePicker === 'function') {
        // File System Access API — works in Edge/Chrome and on GitHub Pages
        let fileHandle;
        try {
          fileHandle = await window.showSaveFilePicker({
            suggestedName,
            types: [{ description: 'LSL/SLua Files', accept: { 'text/plain': ['.lsl', '.lua'] } }],
            startIn: 'documents',
          });
        } catch (e) {
          if (e.name === 'AbortError') { statusEl.textContent = ''; return; }
          throw e;
        }
        const ok = await _ideWriteViaHandle({ fileHandle }, source);
        if (!ok) { statusEl.textContent = 'Save error: permission denied'; return; }
        tab.fileHandle = fileHandle;
        tab.path = fileHandle.name;
        tab.name = null;
        tab.dirty = false;
        ideSyncActiveState();
        renderIdeTabs();
        idePersistSession();
        loadFileTree(tab.path);
        statusEl.textContent = '\u2713 Saved';
        setTimeout(() => { statusEl.textContent = ''; }, 2000);
        return;

      } else {
        // Last resort: text input dialog
        const dirCtx = pathToSave && pathToSave.includes('/')
          ? pathToSave.slice(0, pathToSave.lastIndexOf('/'))
          : getSelectedDirectoryPath();
        const entered = await showNameDialog(
          'Save As',
          dirCtx ? 'in ' + dirCtx + '/' : 'project root',
          pathToSave || joinRelPath(getSelectedDirectoryPath(), suggestedName) || suggestedName
        );
        pathToSave = normalizeRelPath(entered || '');
      }

      if (!pathToSave) { statusEl.textContent = ''; return; }
    }

    // ── Write via backend ─────────────────────────────────────────────────────
    const res = await fetch('/api/fs/write', {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ path: pathToSave, content: source }),
    });
    const data = await res.json();
    if (data.error) { statusEl.textContent = 'Save error: ' + data.error; return; }
    tab.path = pathToSave;
    tab.name = null;
    tab.dirty = false;
    ideSyncActiveState();
    renderIdeTabs();
    idePersistSession();
    loadFileTree(tab.path);
    statusEl.textContent = '\u2713 Saved';
    setTimeout(() => { statusEl.textContent = ''; }, 2000);
  } catch (e) {
    statusEl.textContent = 'Save failed: ' + e.message;
  }
}

function ideLoadContent(path, content, opts = {}) {
  const tab = ideOpenTab(path, content, opts);
  document.getElementById('ide-status').textContent = '';
  if (ideEditor?.getModel()) monaco.editor.setModelMarkers(ideEditor.getModel(), 'lsl-checker', []);
  return tab;
}

function ideLoadExternalFile(path, content) {
  const tab = ideLoadContent(path, content, { isExternal: true, externalPath: String(path || '') });
  if (tab) {
    tab.dirty = false;
    ideSyncActiveState();
    renderIdeTabs();
    idePersistSession();
  }
  document.getElementById('ide-ext-status').textContent = '';
}

function ideStopExternalMode() {
  _extPendingContent = null;
  const tab = ideGetActiveTab();
  if (tab) {
    tab.isExternal = false;
    tab.externalPath = '';
  }
  ideSyncActiveState();
  renderIdeTabs();
  idePersistSession();
}

// Called from Python via evaluate_js when Firestorm rewrites the temp file
function onExternalFileChanged(path, content) {
  const tab = ideTabs.find(t => t.isExternal && (t.externalPath === path || t.path === path));
  if (!tab) return;
  _extPendingContent = { tabId: tab.id, content };
  if (ideActiveTabId === tab.id) {
    document.getElementById('ide-ext-status').textContent     = '⚠ Updated by viewer';
    document.getElementById('ide-ext-reload-btn').style.display = '';
  }
}

// ── IDE open dialog ───────────────────────────────────────────────────────────
document.getElementById('ide-open-btn').addEventListener('click', async () => {
  if (window.pywebview?.api) {
    setMode('ide');
    ideSetBusy('Loading file\u2026');
    try {
      await initIde();
      const result = await window.pywebview.api.open_file_dialog();
      if (!result || result.cancelled) return;
      if (result.error) { document.getElementById('ide-status').textContent = 'Error: ' + result.error; return; }
      ideLoadContent(result.path, result.content || '');
    } finally {
      ideClearBusy();
    }
    return;
  }
  if (typeof window.showOpenFilePicker === 'function') {
    let fileHandle;
    try {
      [fileHandle] = await window.showOpenFilePicker({
        multiple: false,
        types: [{ description: 'LSL/SLua Files', accept: { 'text/plain': ['.lsl', '.lua', '.txt'] } }],
      });
    } catch (e) {
      if (e.name !== 'AbortError') {
        document.getElementById('ide-status').textContent = 'Open error: ' + e.message;
      }
      return;
    }
    setMode('ide');
    ideSetBusy('Loading file\u2026');
    try {
      await initIde();
      const file = await fileHandle.getFile();
      const content = await file.text();
      const tab = ideLoadContent(fileHandle.name, content, { forceNew: true });
      if (tab) { tab.fileHandle = fileHandle; tab.path = fileHandle.name; }
    } catch (e) {
      document.getElementById('ide-status').textContent = 'Open error: ' + e.message;
    } finally {
      ideClearBusy();
    }
    return;
  }
  // Fallback: hidden file input (no fileHandle, basename only)
  document.getElementById('ide-file-input').click();
});

document.getElementById('ide-file-input').addEventListener('change', e => {
  const file = e.target.files[0];
  if (!file) return;
  setMode('ide');
  ideSetBusy('Loading file…');
  const reader = new FileReader();
  reader.onload = async ev => {
    try {
      await initIde();
      ideLoadContent(file.name, ev.target.result || '', { forceNew: true });
    } finally {
      ideClearBusy();
    }
  };
  reader.onerror = () => { ideClearBusy(); };
  reader.readAsText(file, 'utf-8');
  e.target.value = '';
});

document.getElementById('ide-new-btn').addEventListener('click', async () => {
  setMode('ide');
  await initIde();
  const dirCtx = getSelectedDirectoryPath();
  const name = await showNameDialog(
    'New File',
    dirCtx ? 'in ' + dirCtx + '/' : 'project root',
    joinRelPath(dirCtx, ideNextUntitledName()) || ideNextUntitledName()
  );
  if (!name) return;
  const tab = ideOpenTab(name, '', { forceNew: true });
  tab.dirty = true;
  ideSyncActiveState();
  renderIdeTabs();
  idePersistSession();
});

document.getElementById('ide-save-btn').addEventListener('click', () => ideFileSave(false));
document.getElementById('ide-save-as-btn').addEventListener('click', () => ideFileSave(true));
document.getElementById('ide-reload-btn').addEventListener('click', async () => {
  const tab = ideGetActiveTab();
  if (!tab) return;
  const statusEl = document.getElementById('ide-status');
  // Reload via stored fileHandle (File System Access API)
  if (tab.fileHandle) {
    try {
      const file = await tab.fileHandle.getFile();
      const content = await file.text();
      ideInternalSet = true;
      tab.model.setValue(content);
      ideInternalSet = false;
      tab.dirty = false;
      ideSyncActiveState();
      renderIdeTabs();
      idePersistSession();
      statusEl.textContent = '\u2713 Reloaded';
      setTimeout(() => { statusEl.textContent = ''; }, 2000);
    } catch (e) {
      statusEl.textContent = 'Reload error: ' + e.message;
    }
    return;
  }
  // Reload via backend path
  const path = tab.path;
  if (!path) { statusEl.textContent = 'No saved path to reload from'; return; }
  try {
    const res = await fetch('/api/fs/read?path=' + encodeURIComponent(path));
    const data = await res.json();
    if (data.error) { statusEl.textContent = 'Reload error: ' + data.error; return; }
    ideInternalSet = true;
    tab.model.setValue(data.content || '');
    ideInternalSet = false;
    tab.dirty = false;
    ideSyncActiveState();
    renderIdeTabs();
    idePersistSession();
    statusEl.textContent = '\u2713 Reloaded';
    setTimeout(() => { statusEl.textContent = ''; }, 2000);
  } catch (e) {
    statusEl.textContent = 'Reload error: ' + e.message;
  }
});
document.getElementById('ide-undo-btn').addEventListener('click', ideUndo);
document.getElementById('ide-redo-btn').addEventListener('click', ideRedo);
document.getElementById('ide-selection-btn').addEventListener('click', e => {
  e.stopPropagation();
  const hasSelection = ideHasSelection();
  const btn = e.currentTarget;
  const rect = btn.getBoundingClientRect();
  showCtxMenu(rect.left, rect.bottom + 2, [
    { label: 'Select All (Ctrl+A)', action: () => ideSelectAll() },
    { label: 'Select None (Ctrl+Shift+A)', action: () => ideSelectNone(), disabled: !hasSelection },
    { label: 'Invert Selection (Ctrl+Alt+I)', action: () => ideInvertSelection(), disabled: !hasSelection },
    '---',
    { label: 'Cut (Ctrl+X)', action: () => ideCut(), disabled: !hasSelection },
    { label: 'Copy (Ctrl+C)', action: () => ideCopy(), disabled: !hasSelection },
    { label: 'Paste (Ctrl+V)', action: () => idePaste() },
  ]);
});
document.getElementById('ide-wrap-btn').addEventListener('click', ideToggleWordWrap);
document.getElementById('ide-check-btn').addEventListener('click', ideRunCheck);

// ── IDE OSSL / Firestorm toggle buttons ───────────────────────────────────────
(function() {
  const osslBtn = document.getElementById('ide-ossl-toggle');
  const fsBtn   = document.getElementById('ide-fs-toggle');

  function _updateOssl() {
    osslBtn.classList.toggle('active-ossl', ideOsslMode);
    osslBtn.title = ideOsslMode
      ? 'OSSL mode ON — os* functions accepted, click to disable'
      : 'Enable OSSL (OpenSimulator extension functions) — os* functions treated as valid';
  }
  function _updateFs() {
    fsBtn.classList.toggle('active-fs', ideFsMode);
    fsBtn.title = ideFsMode
      ? 'Firestorm FS+ mode ON — #include / #define accepted, click to disable'
      : 'Enable Firestorm preprocessor — #include / #define treated as valid';
  }
  _updateOssl();
  _updateFs();

  osslBtn.addEventListener('click', () => {
    ideOsslMode = !ideOsslMode;
    localStorage.setItem('ide-ossl-mode', ideOsslMode ? '1' : '0');
    _updateOssl();
    // Sync debug pane toggle
    const dbgBtn = document.getElementById('dbg-ossl-toggle');
    if (dbgBtn) dbgBtn.classList.toggle('active-ossl', ideOsslMode);
  });
  fsBtn.addEventListener('click', () => {
    ideFsMode = !ideFsMode;
    localStorage.setItem('ide-fs-mode', ideFsMode ? '1' : '0');
    _updateFs();
    const dbgBtn = document.getElementById('dbg-fs-toggle');
    if (dbgBtn) dbgBtn.classList.toggle('active-fs', ideFsMode);
  });
})();

let _ideCompletionsEnabled = localStorage.getItem('slcode-ac') !== '0';
(function() {
  const btn = document.getElementById('ide-autocomplete-btn');
  function _updateAcBtn() {
    btn.textContent = 'AC: ' + (_ideCompletionsEnabled ? 'On' : 'Off');
    btn.style.borderColor = _ideCompletionsEnabled ? 'var(--accent)' : '';
    btn.style.color = _ideCompletionsEnabled ? 'var(--accent)' : '';
  }
  _updateAcBtn();
  btn.addEventListener('click', () => {
    _ideCompletionsEnabled = !_ideCompletionsEnabled;
    localStorage.setItem('slcode-ac', _ideCompletionsEnabled ? '1' : '0');
    if (ideEditor) ideEditor.updateOptions({ suggest: { showSnippets: _ideCompletionsEnabled }, quickSuggestions: _ideCompletionsEnabled });
    _updateAcBtn();
  });
})();

// ── External editor buttons ────────────────────────────────────────────────────
document.getElementById('ide-watch-btn').addEventListener('click', async () => {
  let path;
  let fileContent = '';
  if (window.pywebview?.api) {
    // Use native file dialog to get path and content
    const dlg = await window.pywebview.api.open_file_dialog();
    if (!dlg || dlg.cancelled || dlg.error) return;
    path = dlg.path;
    fileContent = dlg.content || '';
  } else {
    path = prompt('Enter absolute path to LSL file to watch:');
    if (!path) return;
  }
  const watchRes = await fetch('/api/external/watch', {
    method: 'POST', headers: {'Content-Type':'application/json'},
    body: JSON.stringify({ path }),
  }).then(r => r.json());
  if (watchRes.error) { alert('Watch error: ' + watchRes.error); return; }
  if (watchRes.content !== undefined) fileContent = watchRes.content;
  ideLoadExternalFile(path, fileContent);
  setMode('ide');
});

document.getElementById('ide-unwatch-btn').addEventListener('click', async () => {
  await fetch('/api/external/unwatch', { method: 'POST', headers: {'Content-Type':'application/json'}, body: '{}' });
  ideStopExternalMode();
});

document.getElementById('ide-ext-reload-btn').addEventListener('click', () => {
  if (_extPendingContent && ideEditor) {
    const tab = ideGetTab(_extPendingContent.tabId);
    if (tab?.model) {
      tab.model.setValue(_extPendingContent.content || '');
      tab.dirty = false;
      if (tab.id === ideActiveTabId) ideSyncActiveState();
      renderIdeTabs();
      idePersistSession();
    }
    _extPendingContent = null;
    document.getElementById('ide-ext-status').textContent = 'Reloaded \u2713';
    document.getElementById('ide-ext-reload-btn').style.display = 'none';
  }
});

document.getElementById('ide-fs-setup-btn').addEventListener('click', async () => {
  const modal = document.getElementById('fs-setup-modal');
  modal.style.display = 'flex';
  let cmd = '';
  try {
    const res = await fetch('/api/external/editor-command').then(r => r.json());
    cmd = res.command || '';
  } catch (_) {
    cmd = '(run search-cache.py from terminal — path shown on startup)';
  }
  document.getElementById('fs-cmd-display').textContent = cmd;
});

document.getElementById('fs-setup-close-btn').addEventListener('click', () => {
  document.getElementById('fs-setup-modal').style.display = 'none';
});

document.getElementById('fs-cmd-copy-btn').addEventListener('click', () => {
  const txt = document.getElementById('fs-cmd-display').textContent;
  _clipCopy(txt);
  const btn = document.getElementById('fs-cmd-copy-btn');
  btn.textContent = '\u2713 Copied';
  setTimeout(() => { btn.innerHTML = '&#128203; Copy command'; }, 1500);
});

document.getElementById('fs-setup-modal').addEventListener('click', e => {
  if (e.target === document.getElementById('fs-setup-modal'))
    document.getElementById('fs-setup-modal').style.display = 'none';
});

// ── Library / Project pane ────────────────────────────────────────────────────
async function loadCwd() {
  try {
    const res  = await fetch('/api/fs/cwd');
    const data = await res.json();
    if (data.cwd) document.getElementById('lib-cwd-input').value = data.cwd;
  } catch (_) {}
}

async function changeCwd() {
  const input = document.getElementById('lib-cwd-input');
  const path  = input.value.trim();
  if (!path) return;
  try {
    const res  = await fetch('/api/fs/chdir', {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ path }),
    });
    const data = await res.json();
    if (data.error) {
      input.style.color = 'var(--danger)';
      setTimeout(() => { input.style.color = ''; }, 1500);
    } else {
      input.value = data.cwd;
      input.style.color = 'var(--green)';
      setTimeout(() => { input.style.color = ''; }, 800);
      filesSelectedPath = null;
      filesSelectedEntry = null;
      document.getElementById('lib-selected-name').textContent = 'Select a file';
      ['lib-open-ide-btn','lib-rename-btn','lib-delete-btn'].forEach(id =>
        document.getElementById(id).style.display = 'none');
      loadFileTree();
      loadGitStatus();
    }
  } catch (e) {
    input.style.color = 'var(--danger)';
    setTimeout(() => { input.style.color = ''; }, 1500);
  }
}

document.getElementById('lib-cwd-btn').addEventListener('click', changeCwd);
document.getElementById('lib-cwd-input').addEventListener('keydown', e => {
  if (e.key === 'Enter') changeCwd();
});

document.getElementById('lib-browse-btn').addEventListener('click', async () => {
  if (!window.pywebview?.api) {
    alert('Native folder picker is only available in the desktop app.');
    return;
  }
  const result = await window.pywebview.api.open_folder_dialog();
  if (!result || result.cancelled || result.error) return;
  document.getElementById('lib-cwd-input').value = result.path;
  changeCwd();
});

async function loadFileTree(selectPath) {
  const targetPath = normalizeRelPath(selectPath || filesSelectedPath || '');
  if (targetPath) expandParents(targetPath);
  const treeEl = document.getElementById('lib-file-tree');
  treeEl.innerHTML = '<div style="padding:10px;color:var(--muted);font-size:12px">Loading\u2026</div>';
  try {
    const res  = await fetch('/api/fs/list');
    const data = await res.json();
    if (data.error) { treeEl.innerHTML = `<div style="padding:10px;color:var(--danger);font-size:12px">${esc(data.error)}</div>`; return; }
    treeEl.innerHTML = '';
    renderFileTree(treeEl, data.entries, '');
    if (targetPath) {
      const sel = treeEl.querySelector(`.ftree-item[data-path="${CSS.escape(targetPath)}"]`);
      if (sel) sel.click();
    }
  } catch (e) {
    treeEl.innerHTML = `<div style="padding:10px;color:var(--danger);font-size:12px">${esc(e.message)}</div>`;
  }
}

function expandParents(path) {
  const parts = normalizeRelPath(path).split('/').filter(Boolean);
  let acc = '';
  for (let i = 0; i < parts.length - 1; i++) {
    acc = acc ? `${acc}/${parts[i]}` : parts[i];
    filesExpandedDirs.add(acc);
  }
}

function renderFileTree(container, entries, prefix) {
  entries.forEach(entry => {
    const fullPath = normalizeRelPath(entry.path || (prefix ? `${prefix}/${entry.name}` : entry.name));
    const item = document.createElement('div');
    item.className = `ftree-item ${entry.type === 'dir' ? 'dir' : 'file'}`;
    item.tabIndex = 0;
    item.dataset.path = fullPath;
    item.dataset.type = entry.type;
    if (fullPath === filesSelectedPath) item.classList.add('selected');
    const isDir = entry.type === 'dir';
    const topLevel = !fullPath.includes('/');
    const expanded = isDir && (filesExpandedDirs.has(fullPath) || topLevel);
    if (expanded) filesExpandedDirs.add(fullPath);
    const icon = isDir
      ? (expanded ? '▾' : '▸')
      : (entry.name.endsWith('.lsl') ? '\u{1F4C4}' : (entry.name.endsWith('.lua') ? '\u{1F319}' : '\u{1F4C3}'));
    item.innerHTML = `<span class="ftree-icon" data-toggle="${isDir ? '1' : '0'}">${icon}</span><span>${esc(entry.name)}</span>`;
    item.addEventListener('click', (e) => {
      e.stopPropagation();
      document.querySelectorAll('.ftree-item').forEach(i => i.classList.remove('selected'));
      item.classList.add('selected');
      item.focus();
      filesSelectedPath = fullPath;
       filesSelectedEntry = entry;
      selectLibFile(entry, fullPath);
    });
    item.addEventListener('dblclick', (e) => {
      e.stopPropagation();
      if (entry.type === 'file') {
        document.getElementById('files-open-ide-btn').click();
      } else {
        item.querySelector('.ftree-icon[data-toggle="1"]')?.click();
      }
    });
    item.addEventListener('contextmenu', (e) => {
      e.preventDefault();
      e.stopPropagation();
      document.querySelectorAll('.ftree-item').forEach(i => i.classList.remove('selected'));
      item.classList.add('selected');
      item.focus();
      filesSelectedPath = fullPath;
      filesSelectedEntry = entry;
      selectLibFile(entry, fullPath);
      const dir = entry.type === 'dir' ? fullPath
        : (fullPath.includes('/') ? fullPath.slice(0, fullPath.lastIndexOf('/')) : '');
      const ctxItems = [];
      if (entry.type === 'file') {
        ctxItems.push({ label: 'Open in IDE', action: () => document.getElementById('files-open-ide-btn').click() });
        ctxItems.push('---');
      }
      ctxItems.push({ label: '+ New File Here',   action: () => newFileInDir(dir) });
      ctxItems.push({ label: '+ New Folder Here', action: () => newFolderInDir(dir) });
      ctxItems.push('---');
      ctxItems.push({ label: 'Rename', action: () => document.getElementById('files-rename-btn').click() });
      ctxItems.push({ label: 'Delete', danger: true, action: () => document.getElementById('files-delete-btn').click() });
      showCtxMenu(e.clientX, e.clientY, ctxItems);
    });
    container.appendChild(item);
    if (entry.type === 'dir' && entry.children && entry.children.length) {
      const children = document.createElement('div');
      children.className = 'ftree-dir-children';
      children.style.display = expanded ? '' : 'none';
      renderFileTree(children, entry.children, fullPath);
      container.appendChild(children);
      item.querySelector('.ftree-icon')?.addEventListener('click', (e) => {
        e.stopPropagation();
        const isOpen = children.style.display !== 'none';
        if (isOpen) {
          children.style.display = 'none';
          item.querySelector('.ftree-icon').textContent = '▸';
          filesExpandedDirs.delete(fullPath);
        } else {
          children.style.display = '';
          item.querySelector('.ftree-icon').textContent = '▾';
          filesExpandedDirs.add(fullPath);
        }
      });
    }
  });
}

function selectLibFile(entry, fullPath) {
  const nameEl   = document.getElementById('lib-selected-name');
  const openBtn  = document.getElementById('files-open-ide-btn');
  const renameBtn= document.getElementById('files-rename-btn');
  const deleteBtn= document.getElementById('files-delete-btn');
  nameEl.textContent = fullPath;
  openBtn.style.display  = entry.type === 'file' ? '' : 'none';
  renameBtn.style.display= '';
  deleteBtn.style.display= '';
}

document.getElementById('files-open-ide-btn').addEventListener('click', async () => {
  if (!filesSelectedPath) return;
  try {
    setMode('ide');
    ideSetBusy('Loading from project…');
    const res  = await fetch(`/api/fs/read?path=${encodeURIComponent(filesSelectedPath)}`);
    const data = await res.json();
    if (data.error) { alert('Error: ' + data.error); return; }
    await initIde();
    ideLoadContent(filesSelectedPath, data.content || '');
  } catch (e) { alert('Failed to load: ' + e.message); }
  finally { ideClearBusy(); }
});

document.getElementById('files-rename-btn').addEventListener('click', async () => {
  if (!filesSelectedPath) return;
  const newName = await showNameDialog(
    'Rename',
    filesSelectedPath,
    filesSelectedPath.split('/').pop()
  );
  if (!newName) return;
  const newPath = filesSelectedPath.includes('/')
    ? filesSelectedPath.substring(0, filesSelectedPath.lastIndexOf('/') + 1) + newName
    : newName;
  try {
    const res  = await fetch('/api/fs/rename', {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ from: filesSelectedPath, to: newPath }),
    });
    const data = await res.json();
    if (data.error) { alert('Error: ' + data.error); return; }
    filesSelectedPath = null;
    filesSelectedEntry = null;
    loadFileTree();
    document.getElementById('lib-selected-name').textContent = 'Select a file';
    ['lib-open-ide-btn','lib-rename-btn','lib-delete-btn'].forEach(id =>
      document.getElementById(id).style.display = 'none');
  } catch (e) { alert('Failed: ' + e.message); }
});

document.getElementById('files-delete-btn').addEventListener('click', async () => {
  if (!filesSelectedPath) return;
  if (!confirm(`Delete "${filesSelectedPath}"?`)) return;
  try {
    const res  = await fetch('/api/fs/delete', {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ path: filesSelectedPath }),
    });
    const data = await res.json();
    if (data.error) { alert('Error: ' + data.error); return; }
    filesSelectedPath = null;
    filesSelectedEntry = null;
    loadFileTree();
    document.getElementById('lib-selected-name').textContent = 'Select a file';
    ['lib-open-ide-btn','lib-rename-btn','lib-delete-btn'].forEach(id =>
      document.getElementById(id).style.display = 'none');
  } catch (e) { alert('Failed: ' + e.message); }
});

document.getElementById('files-new-file-btn').addEventListener('click', () => {
  newFileInDir(getSelectedDirectoryPath());
});

document.getElementById('files-new-dir-btn').addEventListener('click', () => {
  newFolderInDir(getSelectedDirectoryPath());
});

document.getElementById('lib-refresh-btn').addEventListener('click', () => loadFileTree());

function getVisibleTreeItems() {
  return [...document.querySelectorAll('#lib-file-tree .ftree-item')].filter(el => {
    let parent = el.parentElement;
    while (parent && parent.id !== 'lib-file-tree') {
      if (parent.classList.contains('ftree-dir-children') && parent.style.display === 'none') return false;
      parent = parent.parentElement;
    }
    return true;
  });
}

function selectTreeItem(item) {
  if (!item) return;
  item.click();
}

document.getElementById('lib-file-tree').addEventListener('keydown', e => {
  const visible = getVisibleTreeItems();
  if (!visible.length) return;
  const active = document.activeElement && document.activeElement.classList.contains('ftree-item')
    ? document.activeElement
    : visible.find(i => i.classList.contains('selected')) || visible[0];
  const idx = Math.max(0, visible.indexOf(active));

  if (e.key === 'ArrowDown') {
    e.preventDefault();
    const next = visible[Math.min(visible.length - 1, idx + 1)];
    if (next) selectTreeItem(next);
  } else if (e.key === 'ArrowUp') {
    e.preventDefault();
    const prev = visible[Math.max(0, idx - 1)];
    if (prev) selectTreeItem(prev);
  } else if (e.key === 'ArrowRight') {
    if (active.dataset.type === 'dir') {
      e.preventDefault();
      const icon = active.querySelector('.ftree-icon[data-toggle="1"]');
      if (icon && icon.textContent.trim() === '▸') icon.click();
    }
  } else if (e.key === 'ArrowLeft') {
    if (active.dataset.type === 'dir') {
      e.preventDefault();
      const icon = active.querySelector('.ftree-icon[data-toggle="1"]');
      if (icon && icon.textContent.trim() === '▾') icon.click();
    }
  } else if (e.key === 'Enter') {
    e.preventDefault();
    if (filesSelectedEntry && filesSelectedEntry.type === 'file') {
      document.getElementById('files-open-ide-btn').click();
    }
  } else if (e.key === 'F2') {
    e.preventDefault();
    if (filesSelectedPath) document.getElementById('files-rename-btn').click();
  } else if (e.key === 'Delete') {
    e.preventDefault();
    if (filesSelectedPath) document.getElementById('files-delete-btn').click();
  }
});

// ── Git ────────────────────────────────────────────────────────────────────────
async function loadGitStatus() {
  const el = document.getElementById('git-status-area');
  el.innerHTML = '<em>Checking\u2026</em>';
  try {
    const res  = await fetch('/api/git/status');
    const data = await res.json();
    if (data.error) {
      el.innerHTML = `<span style="color:var(--danger)">${esc(data.error)}</span>`;
      return;
    }
    renderGitStatus(el, data);
  } catch (e) { el.innerHTML = `<span style="color:var(--danger)">${esc(e.message)}</span>`; }
}

function renderGitStatus(el, data) {
  const parsed = data.parsed || {};
  const changed = parsed.changed || [];
  const staged = changed.filter(c => c.staged).length;
  const unstaged = changed.filter(c => c.unstaged).length;
  const untracked = changed.filter(c => c.untracked).length;
  const branch = parsed.branch || '(unknown branch)';

  let html = `<div style="margin-bottom:8px;line-height:1.55">
    <div><b>${esc(branch)}</b></div>
    <div style="color:var(--muted)">changed: ${changed.length} &#183; staged: ${staged} &#183; unstaged: ${unstaged} &#183; untracked: ${untracked}</div>
  </div>`;

  if (!changed.length) {
    html += `<div style="color:var(--green)">&#10003; Working tree clean</div>`;
  } else {
    html += changed.map(c => {
      const color = c.staged ? 'var(--green)' : (c.untracked ? 'var(--accent)' : 'var(--warn)');
      return `<div class="git-changed-row" data-path="${esc(c.path)}" style="display:flex;gap:8px;align-items:center;padding:3px 0;cursor:pointer;border-bottom:1px solid rgba(255,255,255,.04)">
        <span style="font-family:var(--mono);color:${color};min-width:22px">${esc(c.xy)}</span>
        <span style="font-family:var(--mono);flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${esc(c.path)}</span>
      </div>`;
    }).join('');
  }

  html += `<details style="margin-top:8px"><summary style="cursor:pointer;color:var(--muted)">Raw output</summary><pre style="margin:6px 0 0 0;white-space:pre-wrap;word-break:break-word;font-size:11px">${esc(data.output || '')}</pre></details>`;
  el.innerHTML = html;

  el.querySelectorAll('.git-changed-row').forEach(row => {
    row.addEventListener('click', () => {
      const path = normalizeRelPath(row.dataset.path || '');
      if (!path) return;
      filesSelectedPath = path;
      expandParents(path);
      loadFileTree(path);
    });
  });
}

async function runGitCmd(args) {
  const outEl = document.getElementById('git-output-area');
  outEl.textContent = 'Running\u2026';
  try {
    const res  = await fetch('/api/git/run', {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ args }),
    });
    const data = await res.json();
    outEl.textContent = data.output || data.error || '(no output)';
    if (data.exit_code && data.exit_code !== 0) {
      outEl.style.color = 'var(--danger)';
    } else {
      outEl.style.color = 'var(--muted)';
    }
    loadGitStatus();
    return data;
  } catch (e) {
    outEl.style.color = 'var(--danger)';
    outEl.textContent = e.message;
    return { error: e.message };
  }
}

function getGitTargetPath() {
  return normalizeRelPath(filesSelectedPath || ideFilePath || '');
}

document.getElementById('git-refresh-btn').addEventListener('click', loadGitStatus);
document.getElementById('git-pull-btn').addEventListener('click', () => runGitCmd(['pull']));
document.getElementById('git-push-btn').addEventListener('click', () => runGitCmd(['push']));
document.getElementById('git-stage-selected-btn').addEventListener('click', async () => {
  const target = getGitTargetPath();
  if (!target) { alert('Select a file in Project Files (or open one in IDE) first.'); return; }
  await runGitCmd(['add', '--', target]);
});
document.getElementById('git-unstage-selected-btn').addEventListener('click', async () => {
  const target = getGitTargetPath();
  if (!target) { alert('Select a file in Project Files (or open one in IDE) first.'); return; }
  await runGitCmd(['reset', 'HEAD', '--', target]);
});
document.getElementById('git-diff-selected-btn').addEventListener('click', async () => {
  const target = getGitTargetPath();
  if (!target) { alert('Select a file in Project Files (or open one in IDE) first.'); return; }
  await runGitCmd(['diff', '--', target]);
});
document.getElementById('git-commit-btn').addEventListener('click', async () => {
  const msg     = document.getElementById('git-commit-msg').value.trim();
  const addAll  = document.getElementById('git-add-all').checked;
  if (!msg) { alert('Enter a commit message.'); return; }
  if (addAll) await runGitCmd(['add', '-A']);
  const result = await runGitCmd(['commit', '-m', msg]);
  if (!result.error && (!result.exit_code || result.exit_code === 0)) {
    document.getElementById('git-commit-msg').value = '';
  }
});

document.querySelectorAll('.mode-btn').forEach(btn => {
  btn.addEventListener('click', () => setMode(btn.dataset.mode));
});

async function loadCacheStatus() {
  try {
    const res  = await fetch('/api/cache/status');
    const data = await res.json();
    renderCacheStatus(data);
  } catch (e) {
    document.getElementById('manifest-block').innerHTML =
      `<h3>Cache Status</h3><div style="color:var(--danger);font-size:12px">Failed: ${esc(e.message)}</div>`;
  }
}

function renderCacheStatus(data) {
  const m  = data.manifest || {};
  const dc = data.doc_counts || {};

  // Manifest block
  const sections = m.sections || {};
  document.getElementById('manifest-block').innerHTML = `<h3>Cache Status</h3>
    ${statRow('Last updated', m.last_updated || 'unknown')}
    ${statRow('Core',  sections.core  ? '&#10003; present' : '&#10007; missing', sections.core ? 'ok' : 'off')}
    ${statRow('OSSL',  sections.ossl  ? '&#10003; present' : '&#8212; not fetched', sections.ossl ? 'ok' : 'off')}
    ${statRow('SLua',  sections.slua  ? '&#10003; present' : '&#8212; not fetched', sections.slua ? 'ok' : 'off')}
    ${statRow('Patterns last run', m.patterns_last_run || 'never')}`;

  // Sources block
  const src = m.extension_sources || {};
  const srcNames = ['jyaoma','kwdb','pyoptimizer','makopo','buildersbrewery'];
  document.getElementById('sources-block').innerHTML = `<h3>Extension Sources</h3>
    ${srcNames.map(s => statRow(s, src[s] || 'not fetched', src[s] ? 'ok' : 'off')).join('')}`;

  // Doc counts block
  document.getElementById('docs-block').innerHTML = `<h3>Doc Counts</h3>
    ${Object.entries(dc).map(([k, v]) => statRow(k, v)).join('')}
    ${statRow('Total', data.total, '')}`;
}

function statRow(key, val, cls = '') {
  return `<div class="stat-row">
    <span class="stat-key">${esc(String(key))}</span>
    <span class="stat-val ${esc(cls)}">${esc(String(val))}</span>
  </div>`;
}

// ── Cache tools ───────────────────────────────────────────────────────────────
let _tools       = [];
let _activeJobId      = null;
let _activeToolId     = null;
let _pollTimer        = null;
let _updateAllRunning = false;

async function loadCacheTools() {
  try {
    const [toolsRes, authRes] = await Promise.all([
      fetch('/api/cache/tools'),
      fetch('/api/github/token'),
    ]);
    _tools = await toolsRes.json();
    const authStatus = await authRes.json();
    renderCacheTools(authStatus);
  } catch (e) {
    document.getElementById('cache-tools-area').innerHTML =
      `<div style="color:var(--danger);font-size:12px">Failed to load tools: ${esc(e.message)}</div>`;
  }
}

/* ── GitHub auth card ─────────────────────────────────────────────────────── */

function ghAuthCardHtml(status) {
  const badge = status.set
    ? `<span style="font-size:10px;padding:1px 6px;border-radius:3px;background:rgba(80,200,120,.13);color:var(--green);margin-left:6px;font-weight:600">authenticated</span>`
    : `<span style="font-size:10px;padding:1px 6px;border-radius:3px;background:rgba(232,164,74,.12);color:var(--warn);margin-left:6px">unauthenticated</span>`;
  const statusLine = status.set
    ? `Token: <code style="font-family:var(--mono);font-size:11px">${esc(status.masked)}</code> &nbsp;<span style="color:var(--muted)">(${esc(status.source === 'env' ? 'from GITHUB_TOKEN env var' : 'saved in cache')})</span>`
    : `No token set &mdash; API limited to 60 requests/hr.`;
  const clearBtn = status.set && status.source !== 'env'
    ? `<button id="gh-auth-clear" class="tool-run-btn" style="background:var(--danger);font-size:11px;padding:4px 10px;">Clear</button>`
    : '';
  return `<div class="tool-card" id="card-gh-auth" style="margin-bottom:8px">
    <div class="tool-card-header">
      <div class="tool-card-info">
        <div class="tool-card-name">GitHub Authentication${badge}</div>
        <div class="tool-card-desc">Personal Access Token for the GitHub API (raises rate limit from 60 to 5&thinsp;000 req/hr). Required only for fetching from private repos or heavy use. <a href="https://github.com/settings/tokens" target="_blank" style="color:var(--accent)">Generate a token &#8599;</a> &mdash; no scopes needed for public repos.</div>
        <div style="font-size:11px;color:var(--muted);margin-top:6px">${statusLine}</div>
        <div class="tool-card-opts" id="gh-auth-opts" style="margin-top:8px;gap:6px;align-items:center">
          <input id="gh-token-input" type="password" placeholder="ghp_&hellip;"
            style="background:var(--bg);border:1px solid var(--border);border-radius:4px;color:var(--text);padding:4px 8px;font-size:12px;font-family:var(--mono);width:280px"
            autocomplete="off" spellcheck="false">
          <button id="gh-auth-save" class="tool-run-btn" style="font-size:11px;padding:4px 10px;">Save Token</button>
          ${clearBtn}
          <span id="gh-auth-msg" style="font-size:11px;color:var(--muted)"></span>
        </div>
      </div>
    </div>
  </div>`;
}

async function _ghAuthAction(action, token) {
  const msg = document.getElementById('gh-auth-msg');
  msg.textContent = action === 'save' ? 'Saving…' : 'Clearing…';
  try {
    const res  = await fetch('/api/github/token', {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({action, token: token || ''}),
    });
    const data = await res.json();
    if (data.error) { msg.style.color = 'var(--danger)'; msg.textContent = data.error; return; }
    msg.style.color = 'var(--green)';
    msg.textContent = action === 'save' ? '✓ Saved' : '✓ Cleared';
    // Refresh the auth card with updated status
    const card = document.getElementById('card-gh-auth');
    if (card) card.outerHTML = ghAuthCardHtml(data.status);
    _bindGhAuthEvents();
    if (action === 'save') document.getElementById('gh-token-input').value = '';
  } catch (e) {
    msg.style.color = 'var(--danger)'; msg.textContent = e.message;
  }
}

function _bindGhAuthEvents() {
  const saveBtn  = document.getElementById('gh-auth-save');
  const clearBtn = document.getElementById('gh-auth-clear');
  const inp      = document.getElementById('gh-token-input');
  if (saveBtn) saveBtn.addEventListener('click', () => _ghAuthAction('save', inp?.value.trim()));
  if (clearBtn) clearBtn.addEventListener('click', () => _ghAuthAction('clear', ''));
  if (inp) inp.addEventListener('keydown', e => {
    if (e.key === 'Enter') { e.preventDefault(); _ghAuthAction('save', inp.value.trim()); }
  });
}

/* ── Tool area render ─────────────────────────────────────────────────────── */

function renderCacheTools(authStatus) {
  const area = document.getElementById('cache-tools-area');
  const runSec = document.createElement('div');
  runSec.innerHTML =
    ghAuthCardHtml(authStatus || {set: false}) +
    `<div id="update-all-bar" style="display:flex;align-items:center;gap:10px;padding:4px 4px 12px;border-bottom:1px solid var(--border);margin-bottom:4px;margin-top:8px">
      <button id="update-all-btn" class="tool-run-btn" style="font-size:12px;padding:6px 16px;">&#8593; Update All (Online)</button>
      <span id="update-all-status" style="font-size:11px;color:var(--muted);"></span>
    </div>
    <div class="tool-output" id="update-all-output" style="max-height:340px;"></div>
    <div class="run-tools-hdr" style="margin-top:12px;">Individual Tools</div>`
    + _tools.map(t => toolCardHtml(t)).join('');
  area.innerHTML = '';
  area.appendChild(runSec);
  _bindGhAuthEvents();
  document.getElementById('update-all-btn').addEventListener('click', runUpdateAllOnline);
  _tools.forEach(t => {
    document.getElementById(`run-${t.id}`).addEventListener('click', () => onRunClick(t));
  });
  renderAnalysisSection();
}

function toolCardHtml(t) {
  const opts = t.options.map(opt => {
    if (opt.type === 'select') {
      return `<span class="tool-opt-label">${esc(opt.label)}:</span>
        <select class="tool-opt-select" id="opt-${t.id}-${opt.flag.replace(/^--/,'')}">
          ${opt.choices.map(c => `<option value="${esc(c)}"${c===opt.default?' selected':''}>${esc(c)}</option>`).join('')}
        </select>`;
    }
    if (opt.type === 'number') {
      return `<span class="tool-opt-label">${esc(opt.label)}:</span>
        <input class="tool-opt-number" type="number" min="1"
          id="opt-${t.id}-${opt.flag.replace(/^--/,'')}" placeholder="all">`;
    }
    if (opt.type === 'bool') {
      return `<label style="display:flex;align-items:center;gap:5px;font-size:11px;color:var(--muted);cursor:pointer">
        <input class="tool-opt-check" type="checkbox"
          id="opt-${t.id}-${opt.flag.replace(/^--/,'')}"> ${esc(opt.label)}</label>`;
    }
    return '';
  }).join('');

  const webBadge = t.web
    ? `<span style="font-size:10px;padding:1px 5px;border-radius:3px;background:rgba(232,164,74,.12);color:var(--warn);margin-left:6px">web</span>`
    : '';
  const note = t.note
    ? `<div class="tool-card-note">&#9888; ${esc(t.note)}</div>` : '';
  const optsHtml = opts
    ? `<div class="tool-card-opts">${opts}</div>` : '';

  return `<div class="tool-card" id="card-${t.id}">
    <div class="tool-card-header">
      <div class="tool-card-info">
        <div class="tool-card-name">${esc(t.name)}${webBadge}</div>
        <div class="tool-card-desc">${esc(t.description)}</div>
        ${note}${optsHtml}
      </div>
      <button class="tool-run-btn" id="run-${t.id}">&#9654; Run</button>
    </div>
    <div class="tool-output" id="out-${t.id}"></div>
  </div>`;
}

function getToolOptions(tool) {
  const opts = {};
  tool.options.forEach(opt => {
    const key   = opt.flag.replace(/^--/, '');
    const el    = document.getElementById(`opt-${tool.id}-${key}`);
    if (!el) return;
    if (opt.type === 'bool')   opts[opt.flag] = el.checked;
    else if (opt.type === 'number') { if (el.value) opts[opt.flag] = el.value; }
    else opts[opt.flag] = el.value;
  });
  return opts;
}

async function onRunClick(tool) {
  const btn = document.getElementById(`run-${tool.id}`);

  // Cancel if this tool's job is currently running
  if (_activeToolId === tool.id && _activeJobId) {
    await fetch('/api/cache/cancel', {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({job_id: _activeJobId}),
    });
    return;
  }

  const out = document.getElementById(`out-${tool.id}`);
  out.innerHTML = '';
  out.classList.add('visible');
  document.getElementById(`card-${tool.id}`).classList.add('running');
  btn.textContent = '&#9632; Cancel';
  btn.classList.add('cancel');

  // Disable all other run buttons
  _tools.forEach(t => {
    if (t.id !== tool.id) document.getElementById(`run-${t.id}`).disabled = true;
  });

  try {
    const res  = await fetch('/api/cache/run', {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({tool_id: tool.id, options: getToolOptions(tool)}),
    });
    const data = await res.json();
    if (data.error) {
      appendOutput(out, `[ERROR] ${data.error}`, true);
      resetToolCard(tool);
      return;
    }
    _activeJobId  = data.job_id;
    _activeToolId = tool.id;
    pollOutput(tool, data.job_id, 0, out);
  } catch (e) {
    appendOutput(out, `[ERROR] ${e.message}`, true);
    resetToolCard(tool);
  }
}

function pollOutput(tool, jobId, offset, out) {
  _pollTimer = setTimeout(async () => {
    try {
      const res  = await fetch(`/api/cache/poll?job=${jobId}&offset=${offset}`);
      const data = await res.json();
      data.lines.forEach(l => appendOutput(out, l, l.startsWith('[ERROR]')));
      if (!data.done) {
        pollOutput(tool, jobId, data.offset, out);
      } else {
        const ok = data.exit_code === 0;
        const status = document.createElement('div');
        status.className = `out-status ${ok ? 'ok' : 'err'}`;
        status.textContent = ok
          ? '\u2713 Completed successfully'
          : `\u2717 Exited with code ${data.exit_code}`;
        out.appendChild(status);
        out.scrollTop = out.scrollHeight;
        resetToolCard(tool);
        // Refresh index + status after a successful run
        if (ok) { build_index_client(); loadCacheStatus(); }
      }
    } catch (e) {
      appendOutput(out, `[poll error] ${e.message}`, true);
      resetToolCard(tool);
    }
  }, 800);
}

function appendOutput(out, line, isErr = false) {
  const el = document.createElement('div');
  el.className = `out-line${isErr ? ' err' : ''}`;
  el.textContent = line;
  out.appendChild(el);
  out.scrollTop = out.scrollHeight;
}

function resetToolCard(tool) {
  const btn  = document.getElementById(`run-${tool.id}`);
  const card = document.getElementById(`card-${tool.id}`);
  btn.innerHTML   = '&#9654; Run';
  btn.disabled    = false;
  btn.classList.remove('cancel');
  card.classList.remove('running');
  _activeJobId  = null;
  _activeToolId = null;
  if (!_updateAllRunning)
    _tools.forEach(t => { document.getElementById(`run-${t.id}`).disabled = false; });
}

// ── Update All (Online) — sequential runner ───────────────────────────────────
const _UPDATE_ALL_SEQ = ['update-extension-data', 'scrape-wiki', 'scrape-library', 'full-update'];

async function runUpdateAllOnline() {
  if (_updateAllRunning || _activeJobId) return;
  _updateAllRunning = true;
  const btn    = document.getElementById('update-all-btn');
  const out    = document.getElementById('update-all-output');
  const status = document.getElementById('update-all-status');
  btn.disabled  = true;
  btn.innerHTML = '&#8987; Running&#8230;';
  out.innerHTML = '';
  out.classList.add('visible');
  _tools.forEach(t => { document.getElementById(`run-${t.id}`).disabled = true; });

  let allOk = true;
  for (const toolId of _UPDATE_ALL_SEQ) {
    const tool = _tools.find(t => t.id === toolId);
    if (!tool) continue;
    const sep = document.createElement('div');
    sep.className = 'out-line';
    sep.style.cssText = 'color:var(--accent);font-weight:600;padding-top:6px;';
    sep.textContent = `\u2500\u2500 ${tool.name} \u2500\u2500`;
    out.appendChild(sep);
    status.textContent = `${tool.name}\u2026`;
    out.scrollTop = out.scrollHeight;
    const result = await _runToolSequential(tool, out);
    if (!result.ok) {
      allOk = false;
      const errDiv = document.createElement('div');
      errDiv.className = 'out-status err';
      errDiv.textContent = `\u2717 ${tool.name} failed (exit ${result.exit_code}) \u2014 sequence aborted`;
      out.appendChild(errDiv);
      out.scrollTop = out.scrollHeight;
      break;
    }
  }

  if (allOk) {
    const okDiv = document.createElement('div');
    okDiv.className = 'out-status ok';
    okDiv.textContent = '\u2713 Full online update completed';
    out.appendChild(okDiv);
    out.scrollTop = out.scrollHeight;
    build_index_client();
    loadCacheStatus();
  }
  status.textContent = allOk ? 'Done' : 'Failed';
  btn.disabled  = false;
  btn.innerHTML = '&#8593; Update All (Online)';
  _tools.forEach(t => { document.getElementById(`run-${t.id}`).disabled = false; });
  _updateAllRunning = false;
}

function _runToolSequential(tool, out) {
  return new Promise(async resolve => {
    try {
      const res  = await fetch('/api/cache/run', {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({tool_id: tool.id, options: {}}),
      });
      const data = await res.json();
      if (data.error) {
        appendOutput(out, `[ERROR] ${data.error}`, true);
        return resolve({ok: false, exit_code: -1});
      }
      _pollToolSequential(data.job_id, 0, out, resolve);
    } catch (e) {
      appendOutput(out, `[ERROR] ${e.message}`, true);
      resolve({ok: false, exit_code: -1});
    }
  });
}

function _pollToolSequential(jobId, offset, out, resolve) {
  setTimeout(async () => {
    try {
      const res  = await fetch(`/api/cache/poll?job=${jobId}&offset=${offset}`);
      const data = await res.json();
      data.lines.forEach(l => appendOutput(out, l, l.startsWith('[ERROR]')));
      if (!data.done) {
        _pollToolSequential(jobId, data.offset, out, resolve);
      } else {
        resolve({ok: data.exit_code === 0, exit_code: data.exit_code});
      }
    } catch (e) {
      appendOutput(out, `[poll error] ${e.message}`, true);
      resolve({ok: false, exit_code: -1});
    }
  }, 800);
}

async function build_index_client() {
  await fetch('/api/reload');
  doSearch();
}

// ── Debug pane handles ────────────────────────────────────────────────────────
const mainEl    = document.getElementById('main');
const debugPane = document.getElementById('debug-pane');
const sourceEl  = document.getElementById('lsl-source');
const runBtn    = document.getElementById('run-check');
const modeEl    = document.getElementById('check-mode');
const statsEl   = document.getElementById('check-stats');
const issuesEl  = document.getElementById('subpane-issues');
let debugSourceTabId = null;

// Debug pane OSSL/FS+ toggles — shared state with IDE toggles
(function() {
  const dbgOssl = document.getElementById('dbg-ossl-toggle');
  const dbgFs   = document.getElementById('dbg-fs-toggle');
  function _syncDbg() {
    dbgOssl.classList.toggle('active-ossl', ideOsslMode);
    dbgFs.classList.toggle('active-fs',     ideFsMode);
  }
  _syncDbg();
  dbgOssl.addEventListener('click', () => {
    ideOsslMode = !ideOsslMode;
    localStorage.setItem('ide-ossl-mode', ideOsslMode ? '1' : '0');
    _syncDbg();
    // Also sync IDE toolbar toggle if it exists
    const ideBtn = document.getElementById('ide-ossl-toggle');
    if (ideBtn) ideBtn.classList.toggle('active-ossl', ideOsslMode);
  });
  dbgFs.addEventListener('click', () => {
    ideFsMode = !ideFsMode;
    localStorage.setItem('ide-fs-mode', ideFsMode ? '1' : '0');
    _syncDbg();
    const ideBtn = document.getElementById('ide-fs-toggle');
    if (ideBtn) ideBtn.classList.toggle('active-fs', ideFsMode);
  });
})();

async function jumpToIssueLine(lineNo) {
  if (!lineNo || Number.isNaN(lineNo)) return;
  if (debugSourceTabId && ideGetTab(debugSourceTabId)) {
    if (!ideReady) await initIde();
    ideActivateTab(debugSourceTabId);
  }
  if (!ideReady) await initIde();
  if (ideEditor) {
    setMode('ide');
    ideEditor.revealLineInCenter(lineNo);
    ideEditor.setPosition({ lineNumber: lineNo, column: 1 });
    ideEditor.focus();
    return;
  }
  const lines = sourceEl.value.split('\n');
  let pos = 0;
  for (let i = 0; i < lineNo - 1 && i < lines.length; i++) pos += lines[i].length + 1;
  sourceEl.focus();
  sourceEl.setSelectionRange(pos, pos + (lines[lineNo - 1] || '').length);
}

async function runCheck() {
  const source = sourceEl.value.trim();
  if (!source) {
    issuesEl.innerHTML = '<div id="issues-empty"><div class="big" style="opacity:.2">&#9881;</div><div>Nothing to check &#8212; paste some LSL source first</div></div>';
    statsEl.textContent = '';
    return;
  }
  runBtn.disabled     = true;
  runBtn.textContent  = '\u2026';
  statsEl.textContent = 'Checking\u2026';
  issuesEl.innerHTML  = '';
  try {
    const [checkRes, analyzeRes] = await Promise.all([
      fetch('/api/check', {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ source, mode: modeEl.value, ossl: ideOsslMode, firestorm: ideFsMode }),
      }),
      fetch('/api/analyze', {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ source }),
      }),
    ]);
    const checkData   = await checkRes.json();
    const analyzeData = await analyzeRes.json();
    if (checkData.error) { statsEl.textContent = 'Error: ' + checkData.error; return; }
    renderIssues(checkData);
    renderMemory(analyzeData.memory);
    renderChannels(analyzeData.channels);
    renderDelays(analyzeData.delays);
  } catch (e) {
    statsEl.textContent = 'Request failed: ' + e.message;
  } finally {
    runBtn.disabled    = false;
    runBtn.textContent = '\u25b6 Run';
  }
}

function renderIssues(data) {
  const { issues, stats } = data;
  const parts = [];
  if (stats.errors)   parts.push(`${stats.errors} error${stats.errors !== 1 ? 's' : ''}`);
  if (stats.warnings) parts.push(`${stats.warnings} warning${stats.warnings !== 1 ? 's' : ''}`);
  if (stats.infos)    parts.push(`${stats.infos} note${stats.infos !== 1 ? 's' : ''}`);
  statsEl.textContent = parts.length ? parts.join(', ') : 'No issues found \u2713';

  if (!issues.length) {
    issuesEl.innerHTML = '<div id="issues-empty"><div style="font-size:36px;opacity:.3">\u2713</div><div>No issues found</div></div>';
    return;
  }

  // Build rows + detail placeholders
  issuesEl.innerHTML = issues.map((iss, idx) => {
    const lineLabel = iss.line
      ? `<span class="issue-line">:${iss.line}</span>`
      : '<span class="issue-line"></span>';
    return `<div class="issue-row" data-line="${iss.line}" data-idx="${idx}" data-msg="${esc(iss.message)}">
      <span class="issue-sev sev-${esc(iss.severity)}">${esc(iss.severity)}</span>
      ${lineLabel}
      <div class="issue-body">
        <div class="issue-code">${esc(iss.code)} <span style="font-size:10px;opacity:.5;font-family:var(--mono)">${esc(iss.checker)}</span></div>
        <div class="issue-msg">${esc(iss.message)}</div>
      </div>
      <span style="font-size:10px;color:var(--muted);flex-shrink:0;margin-top:3px;" title="Click to expand detail">&#9660;</span>
    </div>
    <div class="issue-detail" id="issue-detail-${idx}"></div>`;
  }).join('');

  issuesEl.querySelectorAll('.issue-row').forEach(row => {
    row.addEventListener('click', async () => {
      const idx     = row.dataset.idx;
      const lineNo  = parseInt(row.dataset.line, 10);
      const detailEl = document.getElementById(`issue-detail-${idx}`);
      const isOpen  = detailEl.classList.contains('open');

      if (lineNo) await jumpToIssueLine(lineNo);

      // Close all other details
      issuesEl.querySelectorAll('.issue-detail.open').forEach(d => {
        d.classList.remove('open');
        d.closest('.issue-row')?.classList?.remove('expanded');
      });
      issuesEl.querySelectorAll('.issue-row.expanded').forEach(r => r.classList.remove('expanded'));

      if (isOpen) return; // toggle off

      row.classList.add('expanded');
      detailEl.classList.add('open');

      // Extract identifier from message (e.g. `llFoo' or 'llFoo' or "llFoo")
      const msgText = row.dataset.msg || '';
      const identMatch = msgText.match(/[`'"]([A-Za-z_]\w+)[`'"]/)
                      || msgText.match(/(\bll[A-Z]\w+|LINKSETDATA_\w+|[A-Z_]{4,})/i);
      const ident = identMatch ? identMatch[1] : null;

      // Build action buttons
      let actionsHtml = '';
      if (lineNo) {
        actionsHtml += `<button class="issue-jump-btn" data-line="${lineNo}">&#8679; Go to line ${lineNo}</button>`;
      }

      if (ident) {
        detailEl.innerHTML = `<div class="issue-detail-desc" style="color:var(--muted)">Looking up <code>${esc(ident)}</code>…</div>${actionsHtml ? '<div class="issue-detail-actions">' + actionsHtml + '</div>' : ''}`;
        try {
          const res  = await fetch(`/api/lookup?name=${encodeURIComponent(ident)}`);
          const data = await res.json();
          if (data.found) {
            const fm   = data.front_matter || {};
            const sig  = fm.signature || fm.name || data.name;
            const desc = fm.description || '';
            const cat  = fm.category || fm.type || '';
            const rtype = fm.return_type || '';
            const params = Array.isArray(fm.parameters) ? fm.parameters : [];
            const sleep = fm.sleep_time != null ? `sleep: ${fm.sleep_time}s` : '';
            const energy = fm.energy_cost != null ? `energy: ${fm.energy_cost}` : '';
            const wiki  = fm.wiki_url || '';
            const bodyText = String(data.body || '').replace(/\r/g, '').trim();
            const para = bodyText ? bodyText.split(/\n\s*\n/)[0].replace(/\n+/g, ' ').trim() : '';
            const preview = para.length > 360 ? para.slice(0, 360) + '…' : para;
            if (wiki) actionsHtml += `<a class="issue-wiki-btn" href="${esc(wiki)}" target="_blank">&#127760; Wiki</a>`;
            detailEl.innerHTML =
              `<div class="issue-detail-name">${esc(data.name)}</div>` +
              (sig  ? `<div class="issue-detail-sig">${esc(sig)}</div>` : '') +
              (desc ? `<div class="issue-detail-desc">${esc(desc)}</div>` : '') +
              (preview && preview !== desc ? `<div class="issue-detail-desc">${esc(preview)}</div>` : '') +
              `<div class="issue-detail-meta">${[cat, rtype ? `returns: ${rtype}` : '', params.length ? `params: ${params.length}` : '', sleep, energy].filter(Boolean).map(s => `<span>${esc(s)}</span>`).join('')}</div>` +
              (actionsHtml ? `<div class="issue-detail-actions">${actionsHtml}</div>` : '');
          } else {
            detailEl.innerHTML =
              `<div class="issue-detail-desc" style="color:var(--muted)">No cache entry found for <code>${esc(ident)}</code></div>` +
              (actionsHtml ? `<div class="issue-detail-actions">${actionsHtml}</div>` : '');
          }
        } catch (_) {
          detailEl.innerHTML =
            (actionsHtml ? `<div class="issue-detail-actions">${actionsHtml}</div>` : '');
        }
      } else {
        detailEl.innerHTML = actionsHtml ? `<div class="issue-detail-actions">${actionsHtml}</div>` : '<div class="issue-detail-desc" style="color:var(--muted)">No identifier found in message.</div>';
      }

      // Wire jump button
      detailEl.querySelectorAll('.issue-jump-btn[data-line]').forEach(btn => {
        btn.addEventListener('click', async e => {
          e.stopPropagation();
          const ln = parseInt(btn.dataset.line, 10);
          await jumpToIssueLine(ln);
        });
      });
    });
  });
}

runBtn.addEventListener('click', runCheck);
sourceEl.addEventListener('keydown', e => {
  if (e.key === 'Enter' && e.ctrlKey) { e.preventDefault(); runCheck(); }
});

document.getElementById('debug-ide-tab-select').addEventListener('change', e => {
  const tabId = e.target.value || '';
  if (!tabId) return;
  loadDebugFromIdeTab(tabId);
});

document.getElementById('file-input').addEventListener('change', e => {
  const file = e.target.files[0];
  if (!file) return;
  debugSourceTabId = null;
  const reader = new FileReader();
  reader.onload = ev => {
    sourceEl.value = ev.target.result;
    document.getElementById('file-label').textContent = file.name;
    document.getElementById('file-label').title = file.name;
    issuesEl.innerHTML = '<div id="issues-empty"><div class="big" style="opacity:.2">&#9881;</div><div>' + esc(file.name) + ' loaded &#8212; press Ctrl+Enter to check</div></div>';
    statsEl.textContent = '';
  };
  reader.readAsText(file, 'utf-8');
  e.target.value = '';  // allow re-selecting the same file
});

// ── Debug sub-tab switching ────────────────────────────────────────────────────
document.querySelectorAll('.debug-subtab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.debug-subtab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.debug-subpane').forEach(p => p.classList.remove('active'));
    tab.classList.add('active');
    document.getElementById(`subpane-${tab.dataset.subtab}`).classList.add('active');
  });
});

// ── Format / Flatten buttons ───────────────────────────────────────────────────
document.getElementById('fmt-btn').addEventListener('click', async () => {
  const source = sourceEl.value.trim();
  if (!source) return;
  const btn = document.getElementById('fmt-btn');
  btn.disabled = true; btn.textContent = '\u2026';
  try {
    const res  = await fetch('/api/format', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ source }),
    });
    const data = await res.json();
    if (data.error) {
      statsEl.textContent = 'Format error: ' + data.error;
    } else {
      sourceEl.value      = data.source;
      statsEl.textContent = `Formatted \u2014 ${data.changes} change(s)`;
    }
  } catch (e) {
    statsEl.textContent = 'Format failed: ' + e.message;
  } finally {
    btn.disabled = false; btn.textContent = '\u2202 Format';
  }
});

document.getElementById('flatten-btn').addEventListener('click', async () => {
  const source = sourceEl.value.trim();
  if (!source) return;
  const btn = document.getElementById('flatten-btn');
  btn.disabled = true; btn.textContent = '\u2026';
  try {
    const res  = await fetch('/api/flatten', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ source }),
    });
    const data = await res.json();
    if (data.error) {
      statsEl.textContent = 'Flatten error: ' + data.error;
    } else {
      sourceEl.value = data.source;
      const n = data.include_count || 0;
      const w = (data.warnings || []).length;
      statsEl.textContent = `Flattened \u2014 ${n} include(s) resolved` + (w ? ` (${w} warning(s))` : '');
    }
  } catch (e) {
    statsEl.textContent = 'Flatten failed: ' + e.message;
  } finally {
    btn.disabled = false; btn.textContent = '\u2261 Flatten';
  }
});

// ── renderMemory ───────────────────────────────────────────────────────────────
function renderMemory(data) {
  const el = document.getElementById('subpane-memory');
  if (!data) {
    el.innerHTML = '<div style="padding:20px;color:var(--muted);font-size:12px">Memory estimator not available — lsl-memory-estimator.py not found in skills/.</div>';
    return;
  }
  if (data.error) {
    el.innerHTML = `<div style="padding:20px;color:var(--danger);font-size:12px">Error: ${esc(data.error)}</div>`;
    return;
  }
  const pct      = data.pct_heap || 0;
  const barW     = Math.min(100, pct);
  const barColor = pct > 80 ? 'var(--danger)' : pct > 60 ? 'var(--warn)' : 'var(--accent)';
  const valCls   = pct > 80 ? 'danger' : pct > 60 ? 'warn' : '';

  let html = `<div class="mem-summary">
    <div class="mem-stat"><div class="mem-stat-val ${valCls}">${data.total_kb}&nbsp;KB</div><div class="mem-stat-key">Estimated total</div></div>
    <div class="mem-stat"><div class="mem-stat-val">${data.limit_kb}&nbsp;KB</div><div class="mem-stat-key">Heap limit</div></div>
    <div class="mem-stat"><div class="mem-stat-val ${valCls}">${pct}%</div><div class="mem-stat-key">Usage</div></div>
    <div class="mem-stat"><div class="mem-stat-val">${data.globals_count}</div><div class="mem-stat-key">Globals</div></div>
    <div class="mem-stat"><div class="mem-stat-val">${data.locals_count}</div><div class="mem-stat-key">Locals</div></div>
  </div>
  <div class="mem-bar-wrap"><div class="mem-bar-track"><div class="mem-bar" style="width:${barW}%;background:${barColor}"></div></div></div>`;

  if (data.warning) {
    html += `<div style="padding:8px 16px;color:var(--warn);font-size:12px;border-bottom:1px solid var(--border)">&#9888; Approaching memory limit &#8212; add llGetUsedMemory() to profile in-world.</div>`;
  }
  if (data.items && data.items.length) {
    html += data.items.map(it =>
      `<div class="mem-var-row">
        <span class="mem-var-scope scope-${esc(it.scope)}">${esc(it.scope)}</span>
        <span class="mem-var-type">${esc(it.type)}</span>
        <span class="mem-var-name">${esc(it.name)}</span>
        <span class="mem-var-size">~${it.size_bytes}B</span>
        ${it.note ? `<span style="color:var(--muted);font-size:10px">${esc(it.note)}</span>` : ''}
      </div>`
    ).join('');
  }
  if (data.note) html += `<div class="mem-note">${esc(data.note)}</div>`;
  el.innerHTML = html;
}

// ── renderChannels ─────────────────────────────────────────────────────────────
function renderChannels(data) {
  const el = document.getElementById('subpane-channels');
  if (!data) {
    el.innerHTML = '<div style="padding:20px;color:var(--muted);font-size:12px">Channel map not available &#8212; lsl-channel-map.py not found in skills/.</div>';
    return;
  }
  if (data.error) {
    el.innerHTML = `<div style="padding:20px;color:var(--danger);font-size:12px">Error: ${esc(data.error)}</div>`;
    return;
  }
  let html = '';
  if (data.warnings && data.warnings.length) {
    html += data.warnings.map(w => `<div class="chan-warning">&#9888; ${esc(w)}</div>`).join('');
  }
  if (!data.calls || !data.calls.length) {
    html += '<div style="padding:20px;color:var(--muted);font-size:12px">No communication calls found.</div>';
  } else {
    html += `<div style="padding:7px 16px;font-size:11px;color:var(--muted);border-bottom:1px solid var(--border)">${data.total_calls} call(s) &#183; ${(data.unique_channels || []).length} unique resolved channel(s)</div>`;
    html += data.calls.map(c =>
      `<div class="chan-row">
        <span class="chan-num">${c.channel !== null && c.channel !== undefined ? c.channel : '<em style="color:var(--muted)">dynamic</em>'}</span>
        <span class="chan-func">${esc(c.func)}</span>
        <span class="chan-label">${esc(c.note || '')}</span>
        <span class="chan-line">:${c.line}</span>
      </div>`
    ).join('');
  }
  el.innerHTML = html;
}

// ── renderDelays ───────────────────────────────────────────────────────────────
function renderDelays(data) {
  const el = document.getElementById('subpane-delays');
  if (!data) {
    el.innerHTML = '<div style="padding:20px;color:var(--muted);font-size:12px">Sleep profiler not available &#8212; lsl-sleep-profiler.py not found in skills/.</div>';
    return;
  }
  if (data.error) {
    el.innerHTML = `<div style="padding:20px;color:var(--danger);font-size:12px">Error: ${esc(data.error)}</div>`;
    return;
  }
  let html = `<div style="padding:7px 16px;font-size:11px;color:var(--muted);border-bottom:1px solid var(--border)">${(data.calls || []).length} delayed call(s) &#183; ${data.total_delay}s total forced delay</div>`;
  if (data.warnings && data.warnings.length) {
    html += data.warnings.map(w => `<div class="chan-warning">&#9888; ${esc(w)}</div>`).join('');
  }
  if (!data.calls || !data.calls.length) {
    html += '<div style="padding:16px;color:var(--green);font-size:12px">&#10003; No forced-delay calls found.</div>';
  } else {
    const byEvent = data.by_event || {};
    html += Object.entries(byEvent).map(([ev, info]) => {
      const rows = info.calls.map(c =>
        `<div class="delay-row">
          <span class="delay-func">${esc(c.func)}</span>
          <span class="delay-line">:${c.line}</span>
          <span class="delay-secs">${c.delay}s</span>
        </div>`
      ).join('');
      return `<div class="delay-event"><span>${esc(ev)}</span><span class="delay-event-total">${info.total_delay}s</span></div>${rows}`;
    }).join('');
  }
  el.innerHTML = html;
}

// ── Cache analysis cards ───────────────────────────────────────────────────────
const ANALYSIS_TOOLS = [
  { id: 'gaps',           name: 'Doc Gap Reporter',       desc: 'Identify LSL functions with missing or stub documentation.',                 endpoint: '/api/cache/gaps',           render: renderGaps },
  { id: 'validate',       name: 'Front Matter Validator', desc: 'Check all doc files for required YAML front matter fields.',                endpoint: '/api/cache/validate',       render: renderValidation },
  { id: 'disk',           name: 'Disk Usage',             desc: 'Show the size of each directory in the LSL cache.',                         endpoint: '/api/cache/disk-usage',     render: renderDiskUsage },
  { id: 'reconciliation', name: 'Reconciliation Viewer',  desc: 'View cross-source discrepancies from RECONCILIATION.md.',                   endpoint: '/api/cache/reconciliation', render: renderReconciliation },
  { id: 'tags',           name: 'Pattern Tag Browser',    desc: 'Browse the pattern library by tag.',                                        endpoint: '/api/cache/patterns/tags',  render: renderPatternTags },
];

function renderAnalysisSection() {
  const area = document.getElementById('cache-tools-area');
  const sec  = document.createElement('div');
  sec.innerHTML = `<div class="analysis-section-hdr">Cache Analysis</div>` +
    ANALYSIS_TOOLS.map(t =>
      `<div class="analysis-card" id="acard-${t.id}">
        <div class="analysis-card-hdr">
          <div class="analysis-card-info">
            <div class="analysis-card-name">${esc(t.name)}</div>
            <div class="analysis-card-desc">${esc(t.desc)}</div>
          </div>
          <button class="analysis-run-btn" id="abtn-${t.id}">Analyse</button>
        </div>
        <div class="analysis-result" id="ares-${t.id}"></div>
      </div>`
    ).join('');
  area.appendChild(sec);
  ANALYSIS_TOOLS.forEach(t => {
    document.getElementById(`abtn-${t.id}`).addEventListener('click', () => runAnalysis(t));
  });
}

async function runAnalysis(tool) {
  const btn   = document.getElementById(`abtn-${tool.id}`);
  const resEl = document.getElementById(`ares-${tool.id}`);
  btn.disabled     = true;
  btn.textContent  = '\u2026';
  resEl.classList.add('visible');
  resEl.innerHTML  = '<div style="color:var(--muted);font-size:12px">Loading\u2026</div>';
  try {
    const res  = await fetch(tool.endpoint);
    const data = await res.json();
    tool.render(resEl, data);
  } catch (e) {
    resEl.innerHTML = `<div style="color:var(--danger);font-size:12px">Error: ${esc(e.message)}</div>`;
  } finally {
    btn.disabled    = false;
    btn.textContent = 'Analyse';
  }
}

function renderGaps(el, data) {
  if (data.error) { el.innerHTML = `<div style="color:var(--danger)">${esc(data.error)}</div>`; return; }
  let html = `<div style="color:var(--muted);font-size:11px;margin-bottom:8px">${data.total_cached} of ${data.total_known} functions have doc files &#183; ${data.missing.length} missing &#183; ${data.stub.length} stub</div>`;
  if (data.missing.length) {
    html += `<div style="font-size:11px;font-weight:600;color:var(--warn);margin-bottom:4px">Missing (${data.missing.length})</div>`;
    html += `<div style="font-family:var(--mono);font-size:11px;color:var(--text);line-height:1.8">` +
      data.missing.slice(0, 60).map(fn => esc(fn)).join('<br>') +
      (data.missing.length > 60 ? `<br><em style="color:var(--muted)">&#8230;and ${data.missing.length - 60} more</em>` : '') + '</div>';
  }
  if (data.stub.length) {
    html += `<div style="font-size:11px;font-weight:600;color:var(--muted);margin:10px 0 4px">Stubs (${data.stub.length})</div>`;
    html += `<div style="font-family:var(--mono);font-size:11px;color:var(--muted);line-height:1.8">` +
      data.stub.slice(0, 40).map(fn => esc(fn)).join('<br>') + '</div>';
  }
  if (!data.missing.length && !data.stub.length)
    html += '<div style="color:var(--green)">&#10003; All known functions have doc files.</div>';
  el.innerHTML = html;
}

function renderValidation(el, data) {
  if (data.error) { el.innerHTML = `<div style="color:var(--danger)">${esc(data.error)}</div>`; return; }
  let html = `<div style="color:var(--muted);font-size:11px;margin-bottom:8px">${data.ok} of ${data.checked} files valid &#183; ${data.issues.length} with issues</div>`;
  if (!data.issues.length) {
    html += '<div style="color:var(--green)">&#10003; All doc files have required front matter.</div>';
  } else {
    html += `<table class="analysis-table"><tr><th>File</th><th>Missing fields</th></tr>` +
      data.issues.slice(0, 60).map(iss =>
        `<tr><td class="td-mono">${esc(iss.path)}</td><td style="color:var(--warn)">${esc(iss.missing.join(', '))}</td></tr>`
      ).join('') +
      (data.issues.length > 60 ? `<tr><td colspan="2" style="color:var(--muted)">&#8230;and ${data.issues.length - 60} more</td></tr>` : '') +
      '</table>';
  }
  el.innerHTML = html;
}

function renderDiskUsage(el, data) {
  if (data.error) { el.innerHTML = `<div style="color:var(--danger)">${esc(data.error)}</div>`; return; }
  const total = data.total || 1;
  let html = `<div style="color:var(--muted);font-size:11px;margin-bottom:8px">Total: ${data.total_kb} KB (${(data.total_kb/1024).toFixed(1)} MB)</div>`;
  html += `<table class="analysis-table"><tr><th>Name</th><th style="text-align:right">Size</th><th style="text-align:right">%</th></tr>` +
    Object.entries(data.dirs || {}).sort(([,a],[,b]) => b - a).map(([name, bytes]) => {
      const kb  = (bytes / 1024).toFixed(1);
      const pct = Math.round(bytes / total * 100);
      return `<tr><td class="td-mono">${esc(name)}</td><td class="td-mono" style="text-align:right">${kb} KB</td><td class="td-mono" style="text-align:right;color:var(--muted)">${pct}%</td></tr>`;
    }).join('') + '</table>';
  el.innerHTML = html;
}

function renderReconciliation(el, data) {
  if (data.error && !(data.rows && data.rows.length)) { el.innerHTML = `<div style="color:var(--danger)">${esc(data.error)}</div>`; return; }
  if (!data.rows || !data.rows.length) { el.innerHTML = '<div style="color:var(--muted)">No discrepancies recorded.</div>'; return; }
  let html = `<div style="color:var(--muted);font-size:11px;margin-bottom:8px">${data.count} discrepancies recorded</div>`;
  html += `<table class="analysis-table"><tr><th>Item</th><th>Issue</th><th>Sources</th><th>Resolution</th></tr>` +
    data.rows.map(row =>
      `<tr><td class="td-mono">${esc(row[0]||'')}</td><td>${esc(row[1]||'')}</td><td style="color:var(--muted)">${esc(row[2]||'')}</td><td style="color:var(--muted)">${esc(row[3]||'')}</td></tr>`
    ).join('') + '</table>';
  el.innerHTML = html;
}

let _tagData   = null;
let _activeTag = null;
function renderPatternTags(el, data) {
  if (data.error) { el.innerHTML = `<div style="color:var(--danger)">${esc(data.error)}</div>`; return; }
  _tagData   = data;
  _activeTag = null;
  const tags = Object.keys(data.tags || {});
  if (!tags.length) { el.innerHTML = '<div style="color:var(--muted)">No tags found in pattern library.</div>'; return; }
  el.innerHTML = `<div style="color:var(--muted);font-size:11px;margin-bottom:6px">${data.count} patterns &#183; ${data.tag_count} tags</div>
    <div class="tag-cloud" id="tag-cloud-inner">` +
      tags.map(tag => `<span class="tag-pill" data-tag="${esc(tag)}">${esc(tag)}&nbsp;<small>${data.tags[tag].length}</small></span>`).join('') +
    `</div><div id="tag-pattern-list"></div>`;
  el.querySelectorAll('.tag-pill').forEach(pill => {
    pill.addEventListener('click', () => {
      const tag = pill.dataset.tag;
      el.querySelectorAll('.tag-pill').forEach(p => p.classList.remove('active'));
      if (_activeTag === tag) { _activeTag = null; document.getElementById('tag-pattern-list').innerHTML = ''; return; }
      _activeTag = tag;
      pill.classList.add('active');
      const patterns = _tagData.tags[tag] || [];
      document.getElementById('tag-pattern-list').innerHTML =
        `<div style="font-size:11px;font-weight:600;color:var(--muted);margin:10px 0 4px">${esc(tag)} (${patterns.length})</div>` +
        patterns.map(p => `<div class="tag-pattern-row"><span class="tag-pattern-cat">${esc(p.category)}</span><span>${esc(p.name)}</span></div>`).join('');
    });
  });
}

// ── Sub-tab definitions ───────────────────────────────────────────────────────
const OSSL_SUBTABS = [
  {id:'all',      label:'All'},
  {id:'npc',      label:'NPC'},
  {id:'avatar',   label:'Avatar'},
  {id:'drawing',  label:'Drawing'},
  {id:'region',   label:'Region'},
  {id:'grid',     label:'Grid'},
  {id:'sound',    label:'Sound'},
  {id:'utils',    label:'Utils'},
  {id:'misc',     label:'Misc'},
  {id:'examples', label:'Examples'},
];
const EXAMPLE_SUBTABS = [
  {id:'all',       label:'All'},
  {id:'avatar',    label:'Avatar/AO'},
  {id:'hud',       label:'HUD/Menu'},
  {id:'comms',     label:'Communication'},
  {id:'security',  label:'Security'},
  {id:'sensors',   label:'Sensors'},
  {id:'vehicles',  label:'Vehicles'},
  {id:'weapons',   label:'Weapons'},
  {id:'particles', label:'Particles'},
  {id:'vendor',    label:'Vendor'},
  {id:'games',     label:'Games'},
  {id:'media',     label:'Sound/Media'},
  {id:'land',      label:'Land/TP'},
  {id:'building',  label:'Building'},
  {id:'utils',     label:'Math/Utils'},
  {id:'ossl',      label:'OSSL'},
  {id:'misc',      label:'Other'},
];

function osslSubcat(name) {
  if (/^osNpc|^osGetNPC|^osIsNpc/.test(name)) return 'npc';
  if (/^os(Avatar|ForceAttach|ForceDetach|GetAvatarHome|GetAvatarList|AgentSave)/.test(name)) return 'avatar';
  if (/^os(Draw|SetPen|MovePen|SetFont|GetDrawString|SetDynamic|SetContent)/.test(name)) return 'drawing';
  if (/^os(GetRegion|SetRegion|RegionNotice|RegionRestart|SetEstate|Parcel|GetParcel|SetParcel|GetSimulator|GetHostName|Die\b)/.test(name)) return 'region';
  if (/^os(GetGrid|IsHyperGrid|GetSimulatorVersion|GetHostName)/.test(name)) return 'grid';
  if (/^os(AdjustSound|CollisionSound|SetSound)/.test(name)) return 'sound';
  if (/^os(Format|Key2Name|AvatarName2Key|ApproxEquals|AngleBetween|MakeNotecard|Clamp|Vec|String|List|GetInventory|GetLink|GetObject|Set(Inertia|Health|HealRate|OwnerSpeed|SitTarget))/.test(name)) return 'utils';
  return 'misc';
}

function exampleSubcat(name, desc) {
  // Strategy: check the example NAME first (high confidence — specific terms only),
  // then fall back to DESCRIPTION with tight multi-word phrases.
  // Broad words like "score", "level", "play", "board", "message", "display"
  // are intentionally excluded — they appear in too many unrelated contexts.
  // Unmatched examples fall to 'misc' rather than getting a wrong category.
  const n = name.toLowerCase().replace(/[_\-]/g, ' ').trim();
  const d = (desc || '').toLowerCase();

  // OSSL — check both name and description
  if (/\bossl\b|opensim|\bnpc\b/.test(n + ' ' + d) || /\bos[a-z]{3,}/i.test(name)) return 'ossl';

  // ── Name-based checks (substring OK for embedded ll-prefixed function names) ──

  // Comms: HTTP, email, notecard, listen/chat channels — checked FIRST so
  // "HTTP Score Tracker" doesn't fall into games via "score"
  if (/http|email|\bnotecard\b|\blisten\b|\bchat\b|\bchannel\b|\brelay\b|\bwhisper\b/.test(n)) return 'comms';

  // Media: sound and streaming functions
  if (/sound|music|\bstream\b|\baudio\b|\bmedia\b|\bparcel.*music\b/.test(n)) return 'media';

  // Particles: particle systems and visual FX
  if (/particle|\bemitter\b|\bfirework\b|\bsmoke\b|\bspark\b/.test(n)) return 'particles';

  // Vehicles: physical movement
  if (/vehicle|\bhover\b|\bboat\b|\bflight\b|\baircraf|\bkart\b|\bdriv/.test(n)) return 'vehicles';

  // Weapons: combat and projectiles
  if (/weapon|\bgun\b|\bshoot\b|\bbullet\b|\bprojectile\b|\bturret\b|\bcombat\b|\bsword\b|\bgrenade\b/.test(n)) return 'weapons';

  // Vendor: commerce and sales
  if (/vendor|\bvend\b|\btip.?jar\b|\batm\b/.test(n)) return 'vendor';

  // Security: access control
  if (/security|\ban.orb\b|\beject\b|\bcage\b|\bblacklist\b|\bwhitelist\b/.test(n)) return 'security';
  if (/\bban\b/.test(n)) return 'security';

  // Avatar: animation, AO, appearance
  if (/avatar|animation|\bposeball\b|\bpose\b|\bao\b|\battach\b/.test(n)) return 'avatar';
  if (/\bsit\b|\bstand\b/.test(n)) return 'avatar';

  // HUD / menus / UI
  if (/\bhud\b|dialog|\bmenu\b|\btextbox\b/.test(n)) return 'hud';

  // Sensors / detection
  if (/sensor|\bradar\b|\bscanner\b|\bdetect\b|\btracker\b|\bproximity\b/.test(n)) return 'sensors';

  // Land / teleport / region
  if (/teleport|\bparcel\b|\bregion\b|\blandmark\b|\bslurl\b/.test(n)) return 'land';
  if (/\btp\b/.test(n)) return 'land';

  // Building / prim tools
  if (/\brez\b|\bprim\b|\bbuild\b|\btexture\b|\bsculpt\b|\bmesh\b/.test(n)) return 'building';

  // Games — only if the name explicitly says game/puzzle/dice; "score", "level",
  // "race", "play", "board" are deliberately omitted as they appear everywhere
  if (/\bgame\b|\bpuzzle\b|\bdice\b|\brespawn\b|\bquest\b/.test(n)) return 'games';

  // Math / utils — specific algorithmic terms only
  if (/\bmath\b|encrypt|\bbase64\b|\bhash\b|\bcipher\b|\bsort\b|\bcalc\b|\balgorithm\b|bignum/.test(n)) return 'utils';

  // ── Description fallbacks — specific multi-word phrases only ──

  if (/http request|http response|\bnotecard\b|listen.*channel|chat.*channel|instant message/.test(d)) return 'comms';
  if (/vehicle type|vehicle.*physic|physic.*vehicle/.test(d)) return 'vehicles';
  if (/\bweapon\b|\bprojectile\b|\bdamage system/.test(d)) return 'weapons';
  if (/particle system|particle emitter/.test(d)) return 'particles';
  if (/vending machine|tip jar|buy.*item|sell.*item/.test(d)) return 'vendor';
  if (/security orb|access control|ban list/.test(d)) return 'security';
  if (/animation override|pose ball/.test(d)) return 'avatar';
  if (/\bhud\b|dialog menu/.test(d)) return 'hud';
  if (/proximity sensor|sensor event/.test(d)) return 'sensors';
  if (/sound effect|music stream|parcel media|media url/.test(d)) return 'media';
  if (/teleport agent|parcel land|parcel.*boundary/.test(d)) return 'land';
  if (/rez.*object|prim.*color|prim.*colour/.test(d)) return 'building';
  if (/\bgame\b|\bpuzzle\b/.test(d)) return 'games';

  return 'misc';
}

const subtabsEl = document.getElementById('lib-subtabs');

function _buildSubtabs(defs, modeClass) {
  subtabsEl.innerHTML = defs.map(d =>
    `<div class="subtab${d.id === currentSubcat ? ' active' : ''}" data-subcat="${d.id}">${d.label}</div>`
  ).join('');
  subtabsEl.className = `visible ${modeClass}`;
  subtabsEl.querySelectorAll('.subtab').forEach(st => {
    st.addEventListener('click', () => {
      subtabsEl.querySelectorAll('.subtab').forEach(s => s.classList.remove('active'));
      st.classList.add('active');
      currentSubcat = st.dataset.subcat;
      renderResults(_applySubcatFilter(_lastResults), searchEl.value.trim());
    });
  });
}

function _showSubtabs(cat) {
  if (cat === 'ossl')     { _buildSubtabs(OSSL_SUBTABS,    'ossl-mode'); }
  else if (cat === 'examples') { _buildSubtabs(EXAMPLE_SUBTABS, 'examples-mode'); }
  else { subtabsEl.innerHTML = ''; subtabsEl.className = ''; }
}

function _applySubcatFilter(docs) {
  if (currentSubcat === 'all') return docs;
  if (currentCat === 'ossl') {
    if (currentSubcat === 'examples') {
      // Cross-category: filter examples with OSSL language or OSSL keywords
      return docs.filter(d => {
        const lang = (d.language || '').toUpperCase();
        const s    = (d.name + ' ' + (d.description || '')).toLowerCase();
        return lang === 'OSSL' || /\bossl\b|opensim|npc\b/.test(s);
      });
    }
    return docs.filter(d => osslSubcat(d.name) === currentSubcat);
  }
  if (currentCat === 'examples') {
    return docs.filter(d => exampleSubcat(d.name, d.description) === currentSubcat);
  }
  return docs;
}

// ── Category tabs ────────────────────────────────────────────────────────────
document.querySelectorAll('.tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    currentCat    = tab.dataset.cat;
    currentSubcat = 'all';
    _showSubtabs(currentCat);
    doSearch();
  });
});

// ── Search input ─────────────────────────────────────────────────────────────
searchEl.addEventListener('input', () => {
  clearTimeout(debounce);
  if (currentMode === 'library') {
    debounce = setTimeout(doSearch, 180);
  } else {
    debounce = setTimeout(doGlobalSearch, 180);
  }
});
searchEl.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    if (currentMode === 'library') { searchEl.value = ''; doSearch(); }
    else { hideSearchDrop(); searchEl.value = ''; }
  }
  if (e.key === 'ArrowDown' && currentMode === 'library') { focusResult(0); e.preventDefault(); }
});
document.addEventListener('mousedown', e => {
  if (!document.getElementById('search-wrap').contains(e.target)) hideSearchDrop();
});

// ── Keyboard nav in results ───────────────────────────────────────────────────
resultsEl.addEventListener('keydown', e => {
  const cards = [...resultsEl.querySelectorAll('.result-card')];
  const idx   = cards.indexOf(document.activeElement);
  if (e.key === 'ArrowDown' && idx < cards.length - 1) { cards[idx+1].focus(); e.preventDefault(); }
  if (e.key === 'ArrowUp')   { if (idx > 0) { cards[idx-1].focus(); } else { searchEl.focus(); } e.preventDefault(); }
  if (e.key === 'Enter')     { document.activeElement.click(); }
});

function focusResult(i) {
  const cards = resultsEl.querySelectorAll('.result-card');
  if (cards[i]) cards[i].focus();
}

// ── Splitter drag (transform-based for zero-latency feedback) ─────────────────
function makeSplitter(splitterId, paneId, storeKey) {
  const splitter = document.getElementById(splitterId);
  const pane     = document.getElementById(paneId);
  let dragging = false, startX = 0, startW = 0, currentDelta = 0;

  const saved = parseInt(localStorage.getItem(storeKey), 10);
  if (saved && saved >= 180 && saved <= window.innerWidth * 0.7)
    pane.style.width = saved + 'px';

  splitter.addEventListener('mousedown', e => {
    dragging = true;
    startX   = e.clientX;
    startW   = pane.getBoundingClientRect().width;
    currentDelta = 0;
    splitter.classList.add('dragging');
    pane.style.transition = 'none';
    pane.style.willChange = 'transform';
    document.body.style.cursor     = 'col-resize';
    document.body.style.userSelect = 'none';
    document.documentElement.style.pointerEvents = 'none';
    e.preventDefault();
  });

  document.addEventListener('mousemove', e => {
    if (!dragging) return;
    const delta = e.clientX - startX;
    const newW = Math.min(Math.max(startW + delta, 180), window.innerWidth * 0.7);
    currentDelta = newW - startW;
    // Use transform for instant visual feedback (no layout recalc)
    pane.style.transform = `scaleX(${(startW + currentDelta) / startW})`;
    pane.style.transformOrigin = 'left';
  });

  document.addEventListener('mouseup', () => {
    if (!dragging) return;
    dragging = false;
    // Commit the actual width change
    const finalW = Math.min(Math.max(startW + currentDelta, 180), window.innerWidth * 0.7);
    pane.style.transform = 'scaleX(1)';
    pane.style.willChange = '';
    pane.style.width = finalW + 'px';
    pane.style.transition = '';
    splitter.classList.remove('dragging');
    document.body.style.cursor     = '';
    document.body.style.userSelect = '';
    document.documentElement.style.pointerEvents = '';
    localStorage.setItem(storeKey, Math.round(finalW));
  });
}

makeSplitter('splitter',       'results-pane',  'lslcache-sidebar-w');
makeSplitter('debug-splitter', 'debug-editor',  'lslcache-debug-w');
makeSplitter('lib-splitter',   'lib-file-sidebar', 'lslcache-lib-w');

// ── API calls ─────────────────────────────────────────────────────────────────
async function doSearch() {
  const q = searchEl.value.trim();
  // OSSL "Examples" subtab: cross-fetch from examples category
  const fetchCat = (currentCat === 'ossl' && currentSubcat === 'examples') ? 'examples' : currentCat;
  const url = `/api/search?q=${encodeURIComponent(q)}&cat=${fetchCat}`;
  const res = await fetch(url);
  const data = await res.json();
  const grouped = _groupMultipartExamples(data);
  _lastResults = grouped;
  renderResults(_applySubcatFilter(grouped), q);
  return data;
}

// ── Global search dropdown (non-cache modes) ──────────────────────────────────
const searchDropEl = document.getElementById('search-dropdown');

function hideSearchDrop() {
  searchDropEl.classList.remove('visible');
  searchDropEl.innerHTML = '';
}

function showSearchDrop(docs, q) {
  if (!q || !docs.length) { hideSearchDrop(); return; }
  const groupedDocs = _groupMultipartExamples(docs);
  const top5 = groupedDocs.slice(0, 5);
  searchDropEl.innerHTML = top5.map(d => {
    const raw  = d.description || '';
    const desc = raw.length > 90 ? raw.slice(0, 90) + '…' : raw;
    const catCls = CAT_CLASS[d.category] || '';
    const docId = d.__is_multipart_group ? d.__group_id : d.path;
    return `<div class="sdrop-item" tabindex="0" data-docid="${esc(docId)}">
      <div><span class="sdrop-name">${esc(d.name)}</span><span class="sdrop-cat ${catCls}">${esc(d.category)}</span></div>
      ${desc ? `<div class="sdrop-desc">${esc(desc)}</div>` : ''}
    </div>`;
  }).join('') + `<div class="sdrop-more" id="sdrop-see-more">See all results in Cache →</div>`;

  searchDropEl.querySelectorAll('.sdrop-item').forEach(item => {
    const openResult = (e) => {
      if (e) e.preventDefault();
      const docId = item.dataset.docid;
      hideSearchDrop();
      setMode('library');
      loadDocById(docId);  // show doc immediately; renderResults will restore selection via currentPath
      doSearch();     // populate results list in parallel
    };
    item.addEventListener('mousedown', openResult);
    item.addEventListener('keydown', e => { if (e.key === 'Enter') openResult(e); });
  });

  const seeMoreEl = document.getElementById('sdrop-see-more');
  seeMoreEl.addEventListener('mousedown', e => {
    e.preventDefault();
    hideSearchDrop();
    setMode('library');
    doSearch();
  });

  searchDropEl.classList.add('visible');
}

async function doGlobalSearch() {
  const q = searchEl.value.trim();
  if (!q) { hideSearchDrop(); return; }
  const res  = await fetch(`/api/search?q=${encodeURIComponent(q)}&cat=all`);
  const data = await res.json();
  showSearchDrop(data, q);
}

async function loadDoc(path) {
  currentPath = path;
  const res  = await fetch(`/api/doc?path=${encodeURIComponent(path)}`);
  const data = await res.json();
  renderDoc(data);
}

// ── Render results ─────────────────────────────────────────────────────────────
const CAT_CLASS = {
  'functions':     'cat-functions',
  'events':        'cat-events',
  'constants':     'cat-constants',
  'tutorials':     'cat-tutorials',
  'idioms':        'cat-idioms',
  'patterns':      'cat-patterns',
  'anti-patterns': 'cat-anti-patterns',
  'function-usage':'cat-function-usage',
  'examples':      'cat-examples',
  'reference':     'cat-reference',
};

function renderResults(docs, query) {
  const orderedDocs = _orderResultsForDisplay(docs);
  countEl.textContent = orderedDocs.length ? `${orderedDocs.length} result${orderedDocs.length !== 1 ? 's' : ''}` : '';
  if (!orderedDocs.length) {
    resultsEl.innerHTML = `<div id="no-results">No results${query ? ` for "<b>${esc(query)}</b>"` : ''}</div>`;
    return;
  }
  resultsEl.innerHTML = orderedDocs.map((d, i) => {
    const catCls  = CAT_CLASS[d.category] || '';
    const sigHtml = d.signature ? `<div class="card-sig">${esc(d.signature)}</div>` : '';
    const descHtml= d.description ? `<div class="card-desc">${esc(d.description)}</div>` : '';
    const docId = d.__is_multipart_group ? d.__group_id : d.path;
    const pills   = [
      d.sleep_time  && d.sleep_time !== '0' ? `<span class="card-pill pill-sleep">⏱ ${d.sleep_time}s</span>` : '',
      d.energy_cost && d.energy_cost !== '0' ? `<span class="card-pill pill-energy">⚡ ${d.energy_cost}</span>` : '',
      d.deprecated  && d.deprecated !== 'false' ? `<span class="card-pill pill-dep">deprecated</span>` : '',
      d.__is_multipart_group ? `<span class="card-pill">📦 ${d.__part_total} parts</span>` : '',
    ].filter(Boolean).join('');
    return `<div class="result-card" tabindex="0" data-docid="${esc(docId)}" data-i="${i}">
      <div><span class="card-name">${esc(d.name)}</span><span class="card-cat ${catCls}">${esc(d.category)}</span></div>
      ${sigHtml}${descHtml}
      ${pills ? `<div class="card-meta">${pills}</div>` : ''}
    </div>`;
  }).join('');

  resultsEl.querySelectorAll('.result-card').forEach(card => {
    card.addEventListener('click', () => {
      resultsEl.querySelectorAll('.result-card').forEach(c => c.classList.remove('selected'));
      card.classList.add('selected');
      loadDocById(card.dataset.docid);
    });
  });

  // Restore selection
  if (currentPath) {
    const sel = resultsEl.querySelector(`[data-docid="${CSS.escape(currentPath)}"]`);
    if (sel) sel.classList.add('selected');
  }
}

// ── Render doc ─────────────────────────────────────────────────────────────────
function renderDoc(data) {
  const fm   = data.front_matter || {};
  const body = data.body || '';

  const chips = [
    fm.return_type  ? `<span class="meta-chip"><b>returns</b>${esc(fm.return_type)}</span>` : '',
    fm.sleep_time && fm.sleep_time !== '0' ? `<span class="meta-chip"><b>delay</b>${esc(fm.sleep_time)}s</span>` : '',
    fm.energy_cost && fm.energy_cost !== '0' ? `<span class="meta-chip"><b>energy</b>${esc(fm.energy_cost)}</span>` : '',
    fm.language     ? `<span class="meta-chip"><b>lang</b>${esc(fm.language)}</span>` : '',
    fm.deprecated && fm.deprecated !== 'false' ? `<span class="meta-chip pill-dep"><b>⚠</b>deprecated</span>` : '',
    fm.source_part_index && fm.source_part_total ? `<span class="meta-chip"><b>part</b>${esc(fm.source_part_index)} / ${esc(fm.source_part_total)}</span>` : '',
  ].filter(Boolean).join('');

  const wikiLink = fm.wiki_url
    ? `<div id="doc-wiki"><a href="${esc(fm.wiki_url)}" target="_blank">↗ SL Wiki</a></div>`
    : fm.source_url
      ? `<div id="doc-wiki"><a href="${esc(fm.source_url)}" target="_blank">↗ Source</a></div>`
      : fm.local_only
        ? `<div id="doc-wiki" style="opacity:0.55">Local Cache Only</div>`
        : '';

  docEl.innerHTML = `
    <div id="doc-header">
      <div style="flex:1">
        <div id="doc-title">${esc(fm.name || data.path)}</div>
        ${fm.signature ? `<div id="doc-subtitle">${esc(fm.signature)}</div>` : ''}
        ${chips ? `<div id="doc-meta">${chips}</div>` : ''}
        ${fm.description ? `<p style="margin-top:8px;font-size:12px;color:var(--muted)">${esc(fm.description)}</p>` : ''}
      </div>
      ${wikiLink}
    </div>
    <div id="doc-body">${marked.parse(body)}</div>
  `;

  /* Version switcher bar (examples/patterns with multiple scraped versions) */
  if (fm.has_versions === "true") {
    loadDocVersionBar(data.path, docEl.querySelector('#doc-header'));
  }
  /* Open in Editor button (always shown for examples and patterns) */
  const _cat = fm.category || fm.type || '';
  if (_cat === 'examples' || _cat === 'example' || _cat === 'patterns' || _cat === 'pattern' ||
      _cat === 'idioms' || _cat === 'anti-patterns') {
    const _header = docEl.querySelector('#doc-header');
    if (_header) _header.appendChild(makeOpenInEditorBtn(data.path, body));
  }

  /* Wrap every <pre> block in a .code-wrap and inject a copy button */
  docEl.querySelectorAll('#doc-body pre').forEach(pre => {
    const wrap = document.createElement('div');
    wrap.className = 'code-wrap';
    pre.parentNode.insertBefore(wrap, pre);
    wrap.appendChild(pre);

    const btn = document.createElement('button');
    btn.className = 'copy-btn';
    btn.textContent = 'copy';
    btn.title = 'Copy code to clipboard';
    btn.addEventListener('click', async e => {
      e.stopPropagation();
      const code = (pre.querySelector('code') || pre).innerText;
      _clipCopy(code);
      btn.textContent = '✓ copied';
      btn.classList.add('copied');
      setTimeout(() => { btn.textContent = 'copy'; btn.classList.remove('copied'); }, 2000);
    });
    wrap.insertBefore(btn, pre);
  });
}

// ── Version switcher ──────────────────────────────────────────────────────────────
async function loadDocVersionBar(path, headerEl) {
  if (!headerEl) return;
  try {
    const res  = await fetch(`/api/doc-versions?path=${encodeURIComponent(path)}`);
    const data = await res.json();
    if (!data.versions || data.versions.length === 0) return;
    const bar = document.createElement('div');
    bar.className = 'version-bar';
    const label = document.createElement('span');
    label.className = 'ver-label';
    label.textContent = 'Versions:';
    bar.appendChild(label);
    data.versions.forEach(v => {
      const btn = document.createElement('button');
      btn.className = 'ver-btn' + (v.version_id === data.active_version ? ' active' : '');
      btn.textContent = v.custom === 'true' ? '\uD83D\uDD12 Custom' : (v.source_name || v.version_id) + (v.last_updated ? '\u00A0' + v.last_updated : '');
      btn.title = v.version_id;
      btn.onclick = () => switchDocVersion(path, v.version_id);
      bar.appendChild(btn);
    });
    const lockBtn = document.createElement('button');
    lockBtn.className = 'ver-lock-btn';
    lockBtn.textContent = data.custom === 'true' ? '\uD83D\uDD12 Locked' : '\uD83D\uDD13 Lock as Custom';
    lockBtn.title = data.custom === 'true' ? 'Click to unlock this version' : 'Lock current version as custom (fetcher will not overwrite)';
    lockBtn.onclick = () => markDocCustom(path);
    bar.appendChild(lockBtn);
    // Insert before the first child (title) of the header
    headerEl.insertBefore(bar, headerEl.firstChild);
  } catch (_) {}
}

async function switchDocVersion(path, versionId) {
  try {
    await fetch('/api/doc-set-version', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path, version_id: versionId }),
    });
    await loadDoc(path);
    // Update Monaco tab content if this path is open
    const tab = ideTabs.find(t => (t.path || '') === path);
    if (tab) {
      const res  = await fetch(`/api/doc?path=${encodeURIComponent(path)}`);
      const data = await res.json();
      const code = extractCodeFromBody(data.body || '');
      if (tab.model) tab.model.setValue(code);
    }
  } catch (_) {}
}

async function markDocCustom(path) {
  try {
    await fetch('/api/doc-mark-custom', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path }),
    });
    await loadDoc(path);
  } catch (_) {}
}

function extractCodeFromBody(body) {
  const m = body.match(/```(?:lsl|LSL)?\n([\s\S]*?)```/);
  return m ? m[1] : body;
}

function makeOpenInEditorBtn(path, body) {
  const code = extractCodeFromBody(body);
  const btn  = document.createElement('button');
  btn.className = 'open-ide-btn';
  btn.textContent = '\u29C1 Open in Editor';
  btn.title = 'Load this script into the IDE editor';
  btn.onclick = () => {
    setMode('ide');
    initIde().then(() => ideLoadContent(path, code, { isExternal: false }));
  };
  return btn;
}

function esc(s) {
  return String(s ?? '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

// ── Reload ────────────────────────────────────────────────────────────────────
document.getElementById('reload-btn').addEventListener('click', async () => {
  const btn = document.getElementById('reload-btn');
  btn.textContent = '…';
  btn.disabled = true;
  const res  = await fetch('/api/reload');
  const data = await res.json();
  btn.textContent = '↺';
  btn.disabled = false;
  countEl.textContent = `Index: ${data.count} docs`;
  doSearch();
});

// All API calls use HTTP fetch in both browser and pywebview (URL-based) modes.
// pywebview js_api is only used for native dialogs and frameless window controls.

// ── Frameless window controls ──────────────────────────────────────────────────
let _windowControlsBound = false;
let _windowIsMaximized = false;
const USE_CUSTOM_WINDOW_CONTROLS = false;

function _windowActionEndpoint(action) {
  return `/api/window/${action}`;
}

async function invokeWindowAction(action) {
  const apiMethod = `window_${action}`;
  try {
    if (window.pywebview?.api && typeof window.pywebview.api[apiMethod] === 'function') {
      return await window.pywebview.api[apiMethod]();
    }
  } catch (_) {}

  try {
    const res = await fetch(_windowActionEndpoint(action), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: '{}',
    });
    return await res.json();
  } catch (_) {
    return { error: `window_${action} unavailable` };
  }
}

async function requestAppShutdown() {
  try {
    await fetch('/api/shutdown', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: '{}',
    });
  } catch (_) {}
}

function _bindNoDragHeaderInteractions() {
  const noDragSelectors = [
    '#search-wrap',
    '#search',
    '#search-dropdown',
    '#reload-btn',
    '#mode-switcher',
    '.mode-btn',
    '#header-window-controls',
    '#header-window-controls *',
  ];
  document.querySelectorAll(noDragSelectors.join(',')).forEach(el => {
    if (el.dataset.dragGuardBound === '1') return;
    el.addEventListener('mousedown', (e) => e.stopPropagation());
    el.dataset.dragGuardBound = '1';
  });
}

function setupWindowControls() {
  if (_windowControlsBound) return;
  if (!USE_CUSTOM_WINDOW_CONTROLS) return;

  document.body.classList.add('frameless');
  document.body.classList.add('custom-window-controls');
  _bindNoDragHeaderInteractions();

  const minimizeButtons = [
    document.getElementById('win-minimize'),
    document.getElementById('legacy-win-minimize'),
  ].filter(Boolean);
  const maximizeButtons = [
    document.getElementById('win-maximize'),
    document.getElementById('legacy-win-maximize'),
  ].filter(Boolean);
  const closeButtons = [
    document.getElementById('win-close'),
    document.getElementById('legacy-win-close'),
  ].filter(Boolean);

  minimizeButtons.forEach(btn => {
    btn.addEventListener('click', async () => {
      await invokeWindowAction('minimize');
    });
  });

  maximizeButtons.forEach(btn => {
    btn.addEventListener('click', async () => {
      try {
        if (_windowIsMaximized) {
          const result = await invokeWindowAction('restore');
          _windowIsMaximized = !!result?.maximized;
        } else {
          const result = await invokeWindowAction('maximize');
          _windowIsMaximized = !!result?.maximized;
        }
        maximizeButtons.forEach(b => { b.textContent = _windowIsMaximized ? '❐' : '□'; });
        document.body.classList.toggle('window-maximized', _windowIsMaximized);
      } catch (_) {}
    });
  });

  closeButtons.forEach(btn => {
    btn.addEventListener('click', async () => {
      try {
        const closeResult = await invokeWindowAction('close');
        if (!closeResult?.ok && typeof window.pywebview === 'undefined') {
          await requestAppShutdown();
        }
      } catch (_) {
        if (typeof window.pywebview === 'undefined') {
          await requestAppShutdown();
        } else {
          window.close();
        }
      }
    });
  });

  _windowControlsBound = true;
}

// ── Init ──────────────────────────────────────────────────────────────────────
async function init() {
  const onPywebviewReady = async () => {
    document.body.classList.add('pv-ready');
    document.body.classList.add('native-window-frame');
    if (USE_CUSTOM_WINDOW_CONTROLS) {
      document.body.classList.add('frameless');
      document.body.classList.remove('window-maximized');
      setupWindowControls();
    }
  };

  window.addEventListener('pywebviewready', () => {
    onPywebviewReady().catch(() => {});
  }, { once: true });

  // Detect pywebview (URL-based mode: js_api available for native dialogs only)
  if (typeof window.pywebview !== 'undefined') {
    document.body.classList.add('native-window-frame');
    if (USE_CUSTOM_WINDOW_CONTROLS) {
      document.body.classList.add('frameless');
      setupWindowControls();
    }
    if (!window.pywebview.api) {
      await new Promise(resolve =>
        window.addEventListener('pywebviewready', resolve, { once: true }));
    }
    await onPywebviewReady();
  }

  // Check for startup file (Firestorm external editor) via HTTP
  try {
    const sf = await fetch('/api/external/status').then(r => r.json());
    if (sf.startup) {
      setMode('ide');
      await initIde();
      ideLoadExternalFile(sf.startup, sf.startup_content || '');
    }
  } catch (_) {}

  // Apply correct pane visibility and trigger content load for the active mode.
  setMode(currentMode);
  doSearch();  // pre-populate cache results in the background

  // Tell the launcher stub the UI is ready — closes the splash window.
  // Falls back to the server-side events.loaded handler if this fetch never fires.
  fetch('/api/splash-ready').catch(() => {});
}

window.addEventListener('beforeunload', () => {
  idePersistSession();
});

// ── External page viewer ─────────────────────────────────────────────────────
(function () {
  const viewer      = document.getElementById('ext-viewer');
  const frame       = document.getElementById('ext-frame');
  const urlBar      = document.getElementById('ext-url-bar');
  const backBtn     = document.getElementById('ext-back-btn');
  const fwdBtn      = document.getElementById('ext-fwd-btn');
  const closeBtn    = document.getElementById('ext-close-btn');
  const browserBtn  = document.getElementById('ext-browser-btn');
  const blockedDiv  = document.getElementById('ext-blocked');
  const blockedOpen = document.getElementById('ext-blocked-open');

  let history = [];
  let idx = -1;
  let savedMode = null;
  let savedPath = null;
  let currentUrl = '';

  function _openInBrowser(url) {
    if (!url || !url.startsWith('http')) return;
    fetch('/api/open-browser?url=' + encodeURIComponent(url)).catch(() => {});
  }

  function _showBlocked(blocked) {
    frame.style.display    = blocked ? 'none' : '';
    blockedDiv.style.display = blocked ? 'flex' : 'none';
  }

  function _setFrame(url) {
    currentUrl = url;
    _showBlocked(false);
    frame.src = url;
    urlBar.textContent = url;
    backBtn.disabled = idx <= 0;
    fwdBtn.disabled  = idx >= history.length - 1;
  }

  window.openExtViewer = function (url) {
    // Snapshot app state so close can restore it
    if (!viewer.classList.contains('visible')) {
      savedMode = currentMode;
      savedPath = currentPath;
    }
    // Truncate forward history
    history = history.slice(0, idx + 1);
    history.push(url);
    idx = history.length - 1;
    _setFrame(url);
    viewer.classList.add('visible');
  };

  backBtn.addEventListener('click', () => {
    if (idx > 0) { idx--; _setFrame(history[idx]); }
  });

  fwdBtn.addEventListener('click', () => {
    if (idx < history.length - 1) { idx++; _setFrame(history[idx]); }
  });

  browserBtn.addEventListener('click', () => _openInBrowser(currentUrl));
  blockedOpen.addEventListener('click', () => _openInBrowser(currentUrl));

  closeBtn.addEventListener('click', () => {
    viewer.classList.remove('visible');
    frame.src = 'about:blank';
    _showBlocked(false);
    history = []; idx = -1; currentUrl = '';
    // Restore where the user was
    if (savedMode) { setMode(savedMode); savedMode = null; }
    if (savedPath) { loadDocById(savedPath); savedPath = null; }
  });

  // Track in-frame navigations (same-origin only; cross-origin silently fails)
  // Also detect blocked pages: a load event with about:blank after setting a real URL
  // means the browser swallowed the navigation (X-Frame-Options, CSP, etc.)
  frame.addEventListener('load', () => {
    try {
      const url = frame.contentWindow.location.href;
      if (url === 'about:blank' && currentUrl && currentUrl !== 'about:blank') {
        // Page refused to load in the iframe
        _showBlocked(true);
        return;
      }
      _showBlocked(false);
      if (url && url !== 'about:blank' && url !== history[idx]) {
        history = history.slice(0, idx + 1);
        history.push(url);
        idx = history.length - 1;
        urlBar.textContent = url;
        backBtn.disabled = idx <= 0;
        fwdBtn.disabled  = true;
      }
    } catch (_) {
      // Cross-origin means page loaded — leave url bar as-is
      _showBlocked(false);
    }
  });

  // Intercept all external link clicks app-wide
  document.addEventListener('click', e => {
    const a = e.target.closest('a[href]');
    if (!a) return;
    const href = a.getAttribute('href') || '';
    if (!href.startsWith('http')) return;
    // Let localhost links through normally
    if (/^https?:\/\/(localhost|127\.0\.0\.1)(:\d+)?/.test(href)) return;
    e.preventDefault();
    openExtViewer(href);
  }, true);  // capture phase so we beat any other click handlers
})();

init();
</script>
</body>
</html>
"""


# ── External editor (Firestorm integration) ───────────────────────────────────
_startup_file: Path | None  = None   # file path passed on command line
_watch_file:   Path | None  = None   # file currently being watched
_watch_mtime:  float | None = None   # last-known mtime of the watched file
_watch_active: bool         = False  # True while watcher loop is running
_watch_lock    = threading.Lock()


def _file_watch_loop():
    """Poll the watched file every 500 ms; notify JS when Firestorm modifies it."""
    global _watch_mtime, _watch_active
    while True:
        time.sleep(0.5)
        with _watch_lock:
            if not _watch_active or _watch_file is None:
                break
            f = _watch_file
        try:
            mt = f.stat().st_mtime
            with _watch_lock:
                old = _watch_mtime
            if old is not None and mt != old:
                with _watch_lock:
                    _watch_mtime = mt
                content = f.read_text(encoding="utf-8", errors="replace")
                if _pv_window:
                    safe_path    = json.dumps(str(f))
                    safe_content = json.dumps(content)
                    _pv_window.evaluate_js(
                        f"typeof onExternalFileChanged==='function'&&"
                        f"onExternalFileChanged({safe_path},{safe_content})"
                    )
        except Exception:
            pass
    with _watch_lock:
        _watch_active = False


# ── pywebview window reference (set in main()) ───────────────────────────────
_pv_window = None   # pywebview Window object; needed for native file/folder dialogs

# ── Remote-shutdown hook (set by serve_ui(), used by /api/shutdown) ──────────
_shutdown_fn = None  # callable: _request_shutdown closure from the active serve_ui()

def _exit_process_soon(delay: float = 0.8) -> None:
  def _kill():
    try:
      time.sleep(max(0.0, float(delay)))
      os._exit(0)
    except Exception:
      pass
  try:
    threading.Thread(target=_kill, daemon=True).start()
  except Exception:
    pass

# ── pywebview JS API ──────────────────────────────────────────────────────────
# Mirrors every HTTP endpoint so the page can run without an HTTP server when
# loaded directly inside a pywebview window.

class JsApi:

    # ── Search / doc ───────────────────────────────────────────────────────────
    def search(self, q='', cat='all'):
        return search(q, cat)

    def doc(self, path=''):
        doc_path = (CACHE_ROOT / path).resolve()
        if not str(doc_path).startswith(str(CACHE_ROOT.resolve())):
            return {"error": "forbidden"}
        if not doc_path.exists():
            return {"error": "not found"}
        try:
            text = doc_path.read_text(encoding="utf-8", errors="replace")
            fm, body = parse_front_matter(text)
            return {"path": path, "front_matter": fm, "body": body}
        except Exception as e:
            return {"error": str(e)}

    def reload(self):
        build_index(force=True)
        return {"ok": True, "count": len(INDEX)}

    def status(self):
        from collections import Counter
        cats = Counter(d["category"] for d in INDEX)
        return {"count": len(INDEX), "by_category": dict(cats)}

    # ── Checker / analysis ────────────────────────────────────────────────────
    def check(self, source='', mode='both'):
        return run_checks(source, mode)

    def analyze(self, source=''):
        return run_all_analyses(source)

    def format_source(self, source=''):
        return format_lsl(source)

    def flatten_source(self, source=''):
        return flatten_lsl(source)

    # ── Cache management ──────────────────────────────────────────────────────
    def cache_status(self):
        return get_cache_status()

    def cache_tools(self):
        return [{k: v for k, v in t.items() if k != "cmd"} for t in CACHE_TOOLS]

    def cache_run(self, tool_id='', options=None):
        global _active_job
        if options is None:
            options = {}
        tool = next((t for t in CACHE_TOOLS if t["id"] == tool_id), None)
        if not tool:
            return {"error": f"Unknown tool: {tool_id}"}
        with _jobs_lock:
            busy = _active_job and not _jobs.get(_active_job, {}).get("done", True)
        if busy:
            return {"error": "A tool is already running", "job_id": _active_job}
        cmd = list(tool["cmd"])
        for opt in tool["options"]:
            flag = opt["flag"]
            val  = options.get(flag, "")
            if opt["type"] == "bool":
                if val: cmd.append(flag)
            elif val:
                cmd.extend([flag, str(val)])
        job_id = start_job(cmd)
        with _jobs_lock:
            _active_job = job_id
        return {"job_id": job_id}

    def cache_cancel(self, job_id=''):
        with _jobs_lock:
            job = _jobs.get(job_id)
        if job and job.get("proc"):
            try:
                job["proc"].terminate()
                with _jobs_lock:
                    job["done"]      = True
                    job["exit_code"] = -2
                    job["lines"].append("[Cancelled by user]")
            except Exception:
                pass
        return {"ok": True}

    def cache_poll(self, job_id='', offset=0):
        with _jobs_lock:
            job = _jobs.get(job_id)
        if not job:
            return {"error": "unknown job"}
        with _jobs_lock:
            all_lines = list(job["lines"])
            done      = job["done"]
            exit_code = job["exit_code"]
        new_lines = all_lines[offset:]
        return {"lines": new_lines, "offset": offset + len(new_lines),
                "done": done, "exit_code": exit_code}

    def cache_gaps(self):           return get_doc_gaps()
    def cache_validate(self):       return validate_cache_frontmatter()
    def cache_disk_usage(self):     return get_disk_usage()
    def cache_reconciliation(self): return get_reconciliation()
    def cache_pattern_tags(self):   return get_pattern_tags()

    # ── Filesystem ────────────────────────────────────────────────────────────
    def get_cwd(self):                          return fs_cwd()
    def list_dir(self):                         return fs_list()
    def read_file(self, path=''):               return fs_read(path)
    def write_file(self, path='', content=''): return fs_write(path, content)
    def make_dir(self, path=''):                return fs_mkdir(path)
    def delete_path(self, path=''):             return fs_delete(path)
    def rename_path(self, from_path='', to_path=''): return fs_rename(from_path, to_path)
    def chdir(self, path=''):                   return fs_chdir(path)

    # ── Git ───────────────────────────────────────────────────────────────────
    def git_status_api(self):          return git_status()
    def git_run_api(self, args=None):
        return git_run([str(a) for a in (args or [])])

    # ── Native dialogs ────────────────────────────────────────────────────────
    def open_file_dialog(self):
        if _pv_window is None:
            return {"error": "no pywebview window"}
        try:
            import webview as _wv
            try:
                result = _pv_window.create_file_dialog(
                    _wv.OPEN_DIALOG,
                    allow_multiple=False,
                    file_types=('LSL Files (*.lsl)', 'SLua Files (*.lua)', 'All Files (*.*)'),
                )
            except Exception as e:
                if "file filter" in str(e).lower():
                    result = _pv_window.create_file_dialog(
                        _wv.OPEN_DIALOG,
                        allow_multiple=False,
                    )
                else:
                    raise
            if not result:
                return {"cancelled": True}
            path = result[0]
            content = Path(path).read_text(encoding="utf-8", errors="replace")
            return {"path": path, "content": content}
        except Exception as e:
            return {"error": str(e)}

    def save_file_dialog(self, default_path=''):
      try:
        proj_root = PROJECT_ROOT.resolve()
        rel_default = str(default_path or '').replace('\\', '/').lstrip('/')
        save_name = Path(rel_default).name if rel_default else 'untitled.lsl'
        if not save_name.lower().endswith(('.lsl', '.lua')):
          save_name += '.lsl'
        if _pv_window is not None:
          import webview as _wv
          try:
            result = _pv_window.create_file_dialog(
              _wv.SAVE_DIALOG,
              directory=str(proj_root),
              save_filename=save_name,
              file_types=('LSL Files (*.lsl)', 'SLua Files (*.lua)', 'All Files (*.*)'),
            )
          except Exception as e:
            if "file filter" in str(e).lower():
              result = _pv_window.create_file_dialog(
                _wv.SAVE_DIALOG,
                directory=str(proj_root),
                save_filename=save_name,
              )
            else:
              raise
        else:
          # Save dialog is now handled entirely in JS via showSaveFilePicker().
          # This backend path is only reached from pywebview JS API mode.
          return {"error": "no native dialog available — use browser save dialog"}
        if not result:
          return {"cancelled": True}
        abs_path = Path(result[0]).resolve()
        try:
          rel_path = abs_path.relative_to(proj_root).as_posix()
        except Exception:
          return {"error": "Please choose a location inside the project root."}
        return {"path": rel_path, "absolute_path": str(abs_path)}
      except Exception as e:
        return {"error": str(e)}

    def open_folder_dialog(self):
        if _pv_window is None:
            return {"error": "no pywebview window"}
        try:
            import webview as _wv
            result = _pv_window.create_file_dialog(_wv.FOLDER_DIALOG)
            if not result:
                return {"cancelled": True}
            return {"path": result[0]}
        except Exception as e:
            return {"error": str(e)}

    def window_minimize(self):
      if _pv_window is None:
        return {"error": "no pywebview window"}
      try:
        _pv_window.minimize()
        return {"ok": True}
      except Exception as e:
        return {"error": str(e)}

    def window_maximize(self):
      global _WINDOW_RESTORE_BOUNDS, _WINDOW_MANUAL_MAXIMIZED
      if _pv_window is None:
        return {"error": "no pywebview window"}
      if sys.platform != "win32":
        try:
          _pv_window.maximize()
          _WINDOW_MANUAL_MAXIMIZED = True
          return {"ok": True, "maximized": True}
        except Exception as e:
          return {"error": str(e)}
      try:
        import ctypes

        class RECT(ctypes.Structure):
          _fields_ = [("left", ctypes.c_long), ("top", ctypes.c_long),
                      ("right", ctypes.c_long), ("bottom", ctypes.c_long)]

        class MONITORINFO(ctypes.Structure):
          _fields_ = [("cbSize", ctypes.c_ulong), ("rcMonitor", RECT),
                      ("rcWork", RECT), ("dwFlags", ctypes.c_ulong)]

        hwnd = _get_pywebview_hwnd()
        if not hwnd:
          return {"error": "window handle not found"}

        user32 = ctypes.windll.user32
        current = RECT()
        if not user32.GetWindowRect(hwnd, ctypes.byref(current)):
          return {"error": "GetWindowRect failed"}

        _WINDOW_RESTORE_BOUNDS = (
          current.left,
          current.top,
          current.right - current.left,
          current.bottom - current.top,
        )

        monitor = user32.MonitorFromWindow(hwnd, 2)
        mi = MONITORINFO()
        mi.cbSize = ctypes.sizeof(MONITORINFO)
        if not user32.GetMonitorInfoW(monitor, ctypes.byref(mi)):
          return {"error": "GetMonitorInfoW failed"}

        work_w = mi.rcWork.right - mi.rcWork.left
        work_h = mi.rcWork.bottom - mi.rcWork.top
        user32.SetWindowPos(hwnd, 0, mi.rcWork.left, mi.rcWork.top, work_w, work_h,
                            0x0004 | 0x0010 | 0x0020)
        _WINDOW_MANUAL_MAXIMIZED = True
        return {"ok": True, "maximized": True}
      except Exception as e:
        return {"error": str(e)}

    def window_restore(self):
      global _WINDOW_RESTORE_BOUNDS, _WINDOW_MANUAL_MAXIMIZED
      if _pv_window is None:
        return {"error": "no pywebview window"}
      if sys.platform != "win32":
        try:
          _pv_window.restore()
          _WINDOW_MANUAL_MAXIMIZED = False
          return {"ok": True, "maximized": False}
        except Exception as e:
          return {"error": str(e)}
      try:
        import ctypes
        hwnd = _get_pywebview_hwnd()
        if not hwnd:
          return {"error": "window handle not found"}
        if _WINDOW_RESTORE_BOUNDS:
          left, top, width, height = _WINDOW_RESTORE_BOUNDS
          ctypes.windll.user32.SetWindowPos(hwnd, 0, left, top, width, height,
                                            0x0004 | 0x0010 | 0x0020)
        else:
          _pv_window.restore()
        _WINDOW_MANUAL_MAXIMIZED = False
        return {"ok": True, "maximized": False}
      except Exception as e:
        return {"error": str(e)}

    def window_close(self):
      try:
        if _pv_window is not None:
          try:
            _pv_window.destroy()
          except Exception:
            pass
        if _shutdown_fn:
          threading.Thread(
            target=lambda: _shutdown_fn("Window close requested — shutting down…"),
            daemon=True,
          ).start()
        _exit_process_soon(0.8)
        return {"ok": True}
      except Exception as e:
        _exit_process_soon(0.8)
        return {"error": str(e)}

    # ── External editor (Firestorm) ───────────────────────────────────────────
    def get_startup_file(self):
        """Return the file passed on the command line, if any."""
        if _startup_file and _startup_file.exists():
            try:
                content = _startup_file.read_text(encoding="utf-8", errors="replace")
                return {"path": str(_startup_file), "content": content}
            except Exception as e:
                return {"error": str(e)}
        return {"path": None}

    def watch_file(self, path=""):
        """Start watching an absolute file path for external changes."""
        global _watch_file, _watch_mtime, _watch_active
        p = Path(path).resolve()
        if not p.exists():
            return {"error": f"File not found: {path}"}
        with _watch_lock:
            _watch_file   = p
            _watch_mtime  = p.stat().st_mtime
            already_running = _watch_active
            _watch_active = True
        if not already_running:
            threading.Thread(target=_file_watch_loop, daemon=True).start()
        return {"ok": True, "path": str(p)}

    def stop_watching(self):
        """Stop the file watcher."""
        global _watch_file, _watch_active
        with _watch_lock:
            _watch_file   = None
            _watch_active = False
        return {"ok": True}

    def get_watched_path(self):
        with _watch_lock:
            return {"path": str(_watch_file) if _watch_file else None}

    def write_watched_file(self, content=""):
        """Write content back to the watched external file (bypasses PROJECT_ROOT sandbox)."""
        with _watch_lock:
            f = _watch_file
        if f is None:
            return {"error": "no file is being watched"}
        try:
            f.write_text(content, encoding="utf-8")
            with _watch_lock:
                _watch_mtime = f.stat().st_mtime   # update so we don't trigger self-reload
            return {"ok": True}
        except Exception as e:
            return {"error": str(e)}

    def get_editor_command(self):
        """Return the command string the user should paste into Firestorm."""
        exe = Path(sys.executable)
        script = Path(__file__).resolve()
        # If frozen by PyInstaller the script IS the exe
        if getattr(sys, "frozen", False):
            return {"command": f'"{sys.executable}" --use-external="$file"'}
        return {"command": f'"{exe}" "{script}" --use-external="$file"'}

    # ── IDE ───────────────────────────────────────────────────────────────────
    def ide_completions(self): return get_ide_completions()


class Handler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        pass  # handled by do_GET/do_POST wrappers

    def _log_request(self, status: int, elapsed: float) -> None:
        flag = " !!SLOW" if elapsed > 1.0 else ""
        _log(f"  {self.command:4s} {self.path}  →  {status}  ({elapsed*1000:.0f}ms){flag}")

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", len(body))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        _t0 = time.time()
        _orig_send = self.send_response
        _status_box = [200]
        def _tracked_send(code, message=None):
            _status_box[0] = code
            _orig_send(code, message)
        self.send_response = _tracked_send
        try:
            self._do_GET_inner()
        except Exception as e:
            _log(f"  GET {self.path} ERROR: {e}")
            raise
        finally:
            self._log_request(_status_box[0], time.time() - _t0)

    def _do_GET_inner(self):
        parsed = urlparse(self.path)
        path   = parsed.path
        qs     = parse_qs(parsed.query)

        if path == "/" or path == "/index.html":
            body = HTML.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", len(body))
            self.end_headers()
            self.wfile.write(body)

        elif path == "/marked.min.js":
            body = MARKED_JS.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/javascript; charset=utf-8")
            self.send_header("Content-Length", len(body))
            self.send_header("Cache-Control", "public, max-age=86400")
            self.end_headers()
            self.wfile.write(body)

        elif path == "/api/search":
            q   = qs.get("q", [""])[0]
            cat = qs.get("cat", ["all"])[0]
            self.send_json(search(q, cat))

        elif path == "/api/lookup":
          name = qs.get("name", [""])[0].strip()
          payload = lookup_cache_doc(name)
          status = 400 if payload.get("error") == "name required" else 200
          self.send_json(payload, status)

        elif path == "/api/doc":
            rel = qs.get("path", [""])[0]
            # Security: only allow paths inside CACHE_ROOT/lsl-docs
            doc_path = (CACHE_ROOT / rel).resolve()
            if not str(doc_path).startswith(str(CACHE_ROOT.resolve())):
                self.send_json({"error": "forbidden"}, 403)
                return
            if not doc_path.exists():
                self.send_json({"error": "not found"}, 404)
                return
            try:
                text = doc_path.read_text(encoding="utf-8", errors="replace")
                fm, body = parse_front_matter(text)
                self.send_json({"path": rel, "front_matter": fm, "body": body})
            except Exception as e:
                self.send_json({"error": str(e)}, 500)

        elif path == "/api/doc-versions":
            rel      = qs.get("path", [""])[0]
            doc_path = (CACHE_ROOT / rel).resolve()
            if not str(doc_path).startswith(str(CACHE_ROOT.resolve())):
                self.send_json({"error": "forbidden"}, 403)
                return
            if not doc_path.exists():
                self.send_json({"error": "not found"}, 404)
                return
            vdir     = doc_path.parent / ".versions" / doc_path.stem
            versions = []
            if vdir.exists():
                for vf in sorted(vdir.glob("*.md")):
                    try:
                        vfm, _ = parse_front_matter(vf.read_text(encoding="utf-8", errors="replace"))
                    except Exception:
                        vfm = {}
                    versions.append({
                        "version_id":   vf.stem,
                        "source_name":  vfm.get("source_name", vf.stem),
                        "last_updated": vfm.get("last_updated", ""),
                        "custom":       vfm.get("custom", ""),
                    })
            try:
                afm, _ = parse_front_matter(doc_path.read_text(encoding="utf-8", errors="replace"))
            except Exception:
                afm = {}
            self.send_json({
                "active_version": afm.get("active_version", "current"),
                "custom":         afm.get("custom", ""),
                "versions":       versions,
            })

        elif path == "/api/browse":
            cat = qs.get("cat", ["all"])[0]
            results = [d for d in INDEX if cat == "all" or d["category"] == cat]
            results.sort(key=lambda x: x["name"].lower())
            self.send_json(results)

        elif path == "/api/splash-ready":
            _signal_splash_ready()
            self.send_json({"ok": True})

        elif path == "/api/reload":
            build_index(force=True)
            self.send_json({"ok": True, "count": len(INDEX)})

        elif path == "/api/status":
            from collections import Counter
            cats = Counter(d["category"] for d in INDEX)
            self.send_json({"count": len(INDEX), "by_category": dict(cats)})

        elif path == "/api/cache/status":
            self.send_json(get_cache_status())

        elif path == "/api/cache/tools":
            tools = [{k: v for k, v in t.items() if k != "cmd"} for t in CACHE_TOOLS]
            self.send_json(tools)

        elif path == "/api/github/token":
            self.send_json(_gh_token_status())

        elif path == "/api/cache/poll":
            job_id = qs.get("job", [""])[0]
            offset = int(qs.get("offset", ["0"])[0])
            with _jobs_lock:
                job = _jobs.get(job_id)
            if not job:
                self.send_json({"error": "unknown job"}, 404)
                return
            with _jobs_lock:
                all_lines = list(job["lines"])
                done      = job["done"]
                exit_code = job["exit_code"]
            new_lines = all_lines[offset:]
            self.send_json({
                "lines":     new_lines,
                "offset":    offset + len(new_lines),
                "done":      done,
                "exit_code": exit_code,
            })

        elif path == "/api/cache/gaps":
            self.send_json(get_doc_gaps())

        elif path == "/api/cache/validate":
            self.send_json(validate_cache_frontmatter())

        elif path == "/api/cache/disk-usage":
            self.send_json(get_disk_usage())

        elif path == "/api/cache/reconciliation":
            self.send_json(get_reconciliation())

        elif path == "/api/open-browser":
            url_to_open = qs.get("url", [""])[0]
            if url_to_open.startswith(("http://", "https://")):
                try:
                    webbrowser.open(url_to_open)
                    self.send_json({"ok": True})
                except Exception as e:
                    self.send_json({"ok": False, "error": str(e)})
            else:
                self.send_json({"ok": False, "error": "Invalid URL"})

        elif path == "/api/cache/patterns/tags":
            self.send_json(get_pattern_tags())

        elif path == "/api/fs/cwd":
            self.send_json(fs_cwd())

        elif path == "/api/fs/list":
            self.send_json(fs_list())

        elif path == "/api/fs/read":
            rel = qs.get("path", [""])[0]
            self.send_json(fs_read(unquote(rel)))

        elif path == "/api/session":
            sp = _session_path()
            try:
                self.send_json(json.loads(sp.read_text(encoding="utf-8")) if sp.exists() else {})
            except Exception:
                self.send_json({})

        elif path == "/api/git/status":
            self.send_json(git_status())

        elif path == "/api/ide/completions":
            self.send_json(get_ide_completions())

        elif path == "/api/external/status":
            with _watch_lock:
                wp = str(_watch_file) if _watch_file else None
            startup_path = str(_startup_file) if _startup_file else None
            startup_content = None
            if _startup_file:
                try:
                    startup_content = _startup_file.read_text(encoding="utf-8", errors="replace")
                except Exception:
                    startup_content = ""
            self.send_json({"watched": wp, "startup": startup_path, "startup_content": startup_content})

        elif path == "/api/external/editor-command":
            exe = Path(sys.executable)
            script = Path(__file__).resolve()
            if getattr(sys, "frozen", False):
                cmd = f'"{sys.executable}" --use-external="$file"'
            else:
                cmd = f'"{exe}" "{script}" --use-external="$file"'
            self.send_json({"command": cmd})

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        _t0 = time.time()
        _orig_send = self.send_response
        _status_box = [200]
        def _tracked_send(code, message=None):
            _status_box[0] = code
            _orig_send(code, message)
        self.send_response = _tracked_send
        try:
            self._do_POST_inner()
        except Exception as e:
            _log(f"  POST {self.path} ERROR: {e}")
            raise
        finally:
            self._log_request(_status_box[0], time.time() - _t0)

    def _do_POST_inner(self):
        length = int(self.headers.get("Content-Length", 0))
        raw    = self.rfile.read(length)
        try:
            data = json.loads(raw) if raw else {}
        except Exception:
            self.send_json({"error": "invalid JSON"}, 400)
            return

        if self.path == "/api/check":
            source    = data.get("source", "")
            mode      = data.get("mode", "both")
            ossl      = bool(data.get("ossl", False))
            firestorm = bool(data.get("firestorm", False))
            self.send_json(run_checks(source, mode, ossl=ossl, firestorm=firestorm))

        elif self.path == "/api/analyze":
            source = data.get("source", "")
            self.send_json(run_all_analyses(source))

        elif self.path == "/api/format":
            source = data.get("source", "")
            self.send_json(format_lsl(source))

        elif self.path == "/api/flatten":
            source = data.get("source", "")
            self.send_json(flatten_lsl(source))

        elif self.path == "/api/github/token":
            action = data.get("action", "")
            if action == "save":
                token = data.get("token", "").strip()
                if not token:
                    self.send_json({"error": "token is required"}, 400)
                    return
                try:
                    import stat as _stat
                    _GH_TOKEN_FILE.write_text(token + "\n", encoding="utf-8")
                    try:
                        _GH_TOKEN_FILE.chmod(_stat.S_IRUSR | _stat.S_IWUSR)
                    except Exception:
                        pass
                    self.send_json({"ok": True, "status": _gh_token_status()})
                except Exception as e:
                    self.send_json({"error": str(e)}, 500)
            elif action == "clear":
                try:
                    if _GH_TOKEN_FILE.exists():
                        _GH_TOKEN_FILE.unlink()
                    self.send_json({"ok": True, "status": _gh_token_status()})
                except Exception as e:
                    self.send_json({"error": str(e)}, 500)
            else:
                self.send_json({"error": "action must be 'save' or 'clear'"}, 400)

        elif self.path == "/api/cache/run":
            global _active_job
            tool_id = data.get("tool_id", "")
            options = data.get("options", {})  # {"--type": "functions", "--force": true}
            tool = next((t for t in CACHE_TOOLS if t["id"] == tool_id), None)
            if not tool:
                self.send_json({"error": f"Unknown tool: {tool_id}"}, 400)
                return
            # Reject if another job is still running
            with _jobs_lock:
                busy = _active_job and not _jobs.get(_active_job, {}).get("done", True)
            if busy:
                self.send_json({"error": "A tool is already running", "job_id": _active_job})
                return
            # Build command from template + options
            cmd = list(tool["cmd"])
            for opt in tool["options"]:
                flag = opt["flag"]
                val  = options.get(flag, "")
                if opt["type"] == "bool":
                    if val:
                        cmd.append(flag)
                elif val:
                    cmd.append(f"{flag}={val}")
            job_id = start_job(cmd)
            with _jobs_lock:
                _active_job = job_id
            self.send_json({"job_id": job_id})

        elif self.path == "/api/native/save-dialog":
            default_path = data.get("default_path", "")
            self.send_json(JsApi().save_file_dialog(default_path))

        elif self.path == "/api/window/minimize":
          self.send_json(JsApi().window_minimize())

        elif self.path == "/api/window/maximize":
          self.send_json(JsApi().window_maximize())

        elif self.path == "/api/window/restore":
          self.send_json(JsApi().window_restore())

        elif self.path == "/api/window/close":
          self.send_json(JsApi().window_close())

        elif self.path == "/api/cache/cancel":
            job_id = data.get("job_id", "")
            with _jobs_lock:
                job = _jobs.get(job_id)
            if job and job.get("proc"):
                try:
                    job["proc"].terminate()
                    with _jobs_lock:
                        job["done"]      = True
                        job["exit_code"] = -2
                        job["lines"].append("[Cancelled by user]")
                except Exception:
                    pass
            self.send_json({"ok": True})

        elif self.path == "/api/fs/chdir":
            self.send_json(fs_chdir(data.get("path", "")))

        elif self.path == "/api/doc-set-version":
            rel        = data.get("path", "")
            version_id = data.get("version_id", "")
            if not rel or not version_id:
                self.send_json({"error": "path and version_id required"}, 400)
                return
            doc_path = (CACHE_ROOT / rel).resolve()
            if not str(doc_path).startswith(str(CACHE_ROOT.resolve())):
                self.send_json({"error": "forbidden"}, 403)
                return
            if not doc_path.exists():
                self.send_json({"error": "not found"}, 404)
                return
            vdir    = doc_path.parent / ".versions" / doc_path.stem
            sidecar = vdir / f"{version_id}.md"
            if not sidecar.exists():
                self.send_json({"error": "version not found"}, 404)
                return
            try:
                current_text = doc_path.read_text(encoding="utf-8", errors="replace")
                cur_fm, _    = parse_front_matter(current_text)
                cur_ver_id   = cur_fm.get("active_version", "scraped-prev")
                first_fetch  = cur_fm.get("first_fetched", "")
                # Save current active as sidecar (if not already there)
                vdir.mkdir(parents=True, exist_ok=True)
                cur_sidecar = vdir / f"{cur_ver_id}.md"
                if not cur_sidecar.exists():
                    cur_sidecar.write_text(current_text, encoding="utf-8")
                # Read the requested version sidecar and update metadata fields
                new_text = sidecar.read_text(encoding="utf-8", errors="replace")
                def _set_fm_field(text, key, value):
                    replacement = f'{key}: "{value}"'
                    if re.search(rf'^{key}:', text, re.MULTILINE):
                        return re.sub(rf'^{key}:.+$', replacement, text,
                                      count=1, flags=re.MULTILINE)
                    return re.sub(r'(\n---\n)', f'\n{replacement}\\1', text, count=1)
                new_text = _set_fm_field(new_text, "active_version", version_id)
                new_text = _set_fm_field(new_text, "has_versions", "true")
                if first_fetch:
                    new_text = _set_fm_field(new_text, "first_fetched", first_fetch)
                doc_path.write_text(new_text, encoding="utf-8")
                index_one_file(doc_path)
                self.send_json({"ok": True, "path": rel})
            except Exception as e:
                self.send_json({"error": str(e)}, 500)

        elif self.path == "/api/doc-mark-custom":
            rel = data.get("path", "")
            if not rel:
                self.send_json({"error": "path required"}, 400)
                return
            doc_path = (CACHE_ROOT / rel).resolve()
            if not str(doc_path).startswith(str(CACHE_ROOT.resolve())):
                self.send_json({"error": "forbidden"}, 403)
                return
            if not doc_path.exists():
                self.send_json({"error": "not found"}, 404)
                return
            try:
                text      = doc_path.read_text(encoding="utf-8", errors="replace")
                cur_fm, _ = parse_front_matter(text)
                is_custom = cur_fm.get("custom") == "true"
                vdir      = doc_path.parent / ".versions" / doc_path.stem
                vdir.mkdir(parents=True, exist_ok=True)
                if not is_custom:
                    (vdir / "custom.md").write_text(text, encoding="utf-8")
                    def _set_fm_field(text, key, value):
                        replacement = f'{key}: "{value}"'
                        if re.search(rf'^{key}:', text, re.MULTILINE):
                            return re.sub(rf'^{key}:.+$', replacement, text,
                                          count=1, flags=re.MULTILINE)
                        return re.sub(r'(\n---\n)', f'\n{replacement}\\1', text, count=1)
                    text = _set_fm_field(text, "custom", "true")
                    text = _set_fm_field(text, "active_version", "custom")
                    text = _set_fm_field(text, "has_versions", "true")
                else:
                    # Toggle off: remove custom and active_version flags
                    text = re.sub(r'^custom:.*\n', '', text, flags=re.MULTILINE)
                    text = re.sub(r'^active_version:.*\n', '', text, flags=re.MULTILINE)
                doc_path.write_text(text, encoding="utf-8")
                index_one_file(doc_path)
                self.send_json({"ok": True, "custom": not is_custom})
            except Exception as e:
                self.send_json({"error": str(e)}, 500)

        elif self.path == "/api/fs/write":
            rel     = data.get("path", "")
            content = data.get("content", "")
            self.send_json(fs_write(rel, content))

        elif self.path == "/api/fs/mkdir":
            rel = data.get("path", "")
            self.send_json(fs_mkdir(rel))

        elif self.path == "/api/fs/delete":
            rel = data.get("path", "")
            self.send_json(fs_delete(rel))

        elif self.path == "/api/fs/rename":
            self.send_json(fs_rename(data.get("from", ""), data.get("to", "")))

        elif self.path == "/api/session":
            sp = _session_path()
            try:
                sp.parent.mkdir(parents=True, exist_ok=True)
                sp.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
                self.send_json({"ok": True})
            except Exception as e:
                self.send_json({"error": str(e)})

        elif self.path == "/api/git/run":
            args = data.get("args", [])
            if not isinstance(args, list):
                args = []
            self.send_json(git_run([str(a) for a in args]))

        elif self.path == "/api/external/watch":
            api = JsApi()
            result = api.watch_file(data.get("path", ""))
            # Include initial file content in the response for browser-mode callers
            if not result.get("error") and _watch_file:
                try:
                    result["content"] = _watch_file.read_text(encoding="utf-8", errors="replace")
                except Exception:
                    result["content"] = ""
            self.send_json(result)

        elif self.path == "/api/external/write":
            api = JsApi()
            self.send_json(api.write_watched_file(data.get("content", "")))

        elif self.path == "/api/external/unwatch":
            api = JsApi()
            self.send_json(api.stop_watching())

        elif self.path == "/api/shutdown":
            self.send_json({"ok": True})
            if _shutdown_fn:
                threading.Thread(
                    target=lambda: _shutdown_fn("Remote shutdown requested — shutting down…"),
                    daemon=True,
                ).start()

        else:
            self.send_response(404)
            self.end_headers()


# ── Main ──────────────────────────────────────────────────────────────────────

def parse_cli_args(argv: list[str]):
  parser = argparse.ArgumentParser(
    prog="search-cache.py",
    description="SLCode — LSL documentation browser and IDE",
  )
  sub = parser.add_subparsers(dest="command")

  serve = sub.add_parser("serve", help="Run local HTTP UI server")
  serve.add_argument("--port", type=int, default=PORT, help="Server port (default: 8080)")
  serve.add_argument("--host", default="127.0.0.1", help="Bind host (default: 127.0.0.1)")
  serve.add_argument("--window-mode", choices=["auto", "webview", "browser"], default="auto",
                     help="Window strategy (default: auto)")
  serve.add_argument("--as-browser", action="store_true", help="Force browser mode")
  serve.add_argument("--as-webview", action="store_true", help="Force pywebview mode")
  serve.add_argument("--no-open", action="store_true", help="Do not auto-open browser/window")
  serve.add_argument("--use-external", default="", help="External editor file path (Firestorm mode)")

  status_cmd = sub.add_parser("status", help="Print cache and index status")
  status_cmd.add_argument("--json", action="store_true", help="Output machine-readable JSON")

  search_cmd = sub.add_parser("search", help="Search cache from CLI")
  search_cmd.add_argument("query", nargs="+", help="Search text")
  search_cmd.add_argument("--cat", default="all", help="Category filter")
  search_cmd.add_argument("--limit", type=int, default=20, help="Max results to print")
  search_cmd.add_argument("--json", action="store_true", help="Output JSON")

  doc_cmd = sub.add_parser("doc", help="Show a cache doc by relative path")
  doc_cmd.add_argument("path", help="Path under lsl-docs (e.g. functions/llSay.md)")
  doc_cmd.add_argument("--body-lines", type=int, default=40, help="Body preview line count")
  doc_cmd.add_argument("--json", action="store_true", help="Output JSON")

  lookup_cmd = sub.add_parser("lookup", help="Look up a cache symbol by name")
  lookup_cmd.add_argument("name", help="Function/event/constant name")
  lookup_cmd.add_argument("--json", action="store_true", help="Output JSON")

  completions_cmd = sub.add_parser("completions", help="Print IDE completion items from cache data")
  completions_cmd.add_argument("--prefix", default="", help="Optional label prefix filter")
  completions_cmd.add_argument("--limit", type=int, default=0, help="Optional result limit (0 = all)")
  completions_cmd.add_argument("--json", action="store_true", help="Output JSON")

  check_cmd = sub.add_parser("check", help="Run built-in checkers on a source file or stdin")
  check_cmd.add_argument("path", nargs="?", default="", help="Source file path")
  check_cmd.add_argument("--stdin", action="store_true", help="Read source from stdin")
  check_cmd.add_argument("--mode", choices=["syntax", "sanity", "lint", "both", "all"], default="both",
                         help="Checker mode (default: both)")
  check_cmd.add_argument("--ossl", action="store_true",
                         help="Treat OSSL (os*) functions as valid — suppress unknown-function errors for OpenSimulator extensions")
  check_cmd.add_argument("--fs", action="store_true",
                         help="Firestorm preprocessor mode — pre-flatten #include / #define before checking")
  check_cmd.add_argument("--json", action="store_true", help="Output JSON")

  analyze_cmd = sub.add_parser("analyze", help="Run analysis tools on a source file or stdin")
  analyze_cmd.add_argument("path", nargs="?", default="", help="Source file path")
  analyze_cmd.add_argument("--stdin", action="store_true", help="Read source from stdin")
  analyze_cmd.add_argument("--json", action="store_true", help="Output JSON")

  debug_cmd = sub.add_parser("debug", help="Run the full debug pipeline (checks + analyses)")
  debug_cmd.add_argument("path", nargs="?", default="", help="Source file path")
  debug_cmd.add_argument("--stdin", action="store_true", help="Read source from stdin")
  debug_cmd.add_argument("--mode", choices=["syntax", "sanity", "lint", "both", "all"], default="both",
                         help="Checker mode for debug checks (default: both)")
  debug_cmd.add_argument("--ossl", action="store_true",
                         help="Treat OSSL (os*) functions as valid")
  debug_cmd.add_argument("--fs", action="store_true",
                         help="Firestorm preprocessor mode — pre-flatten #include / #define")
  debug_cmd.add_argument("--json", action="store_true", help="Output JSON")

  format_cmd = sub.add_parser("format", help="Format a source file or stdin")
  format_cmd.add_argument("path", nargs="?", default="", help="Source file path")
  format_cmd.add_argument("--stdin", action="store_true", help="Read source from stdin")
  format_cmd.add_argument("--json", action="store_true", help="Output JSON")

  flatten_cmd = sub.add_parser("flatten", help="Flatten #include directives from a source file or stdin")
  flatten_cmd.add_argument("path", nargs="?", default="", help="Source file path")
  flatten_cmd.add_argument("--stdin", action="store_true", help="Read source from stdin")
  flatten_cmd.add_argument("--json", action="store_true", help="Output JSON")

  fs_cmd = sub.add_parser("fs", help="Project filesystem operations for agents")
  fs_sub = fs_cmd.add_subparsers(dest="fs_command")

  skill_cmd = sub.add_parser("run-skill", help="Run a bundled skill script (internal use)")
  skill_cmd.add_argument("skill", help="Skill name (without .py)")
  skill_cmd.add_argument("args", nargs=argparse.REMAINDER, help="Arguments forwarded to the skill")

  cache_cmd = sub.add_parser("cache", help="Cache inspection and maintenance commands")
  cache_sub = cache_cmd.add_subparsers(dest="cache_command")

  cache_status_cmd = cache_sub.add_parser("status", help="Show cache status")
  cache_status_cmd.add_argument("--json", action="store_true", help="Output JSON")

  cache_reload_cmd = cache_sub.add_parser("reload", help="Rebuild in-memory cache index")
  cache_reload_cmd.add_argument("--json", action="store_true", help="Output JSON")

  cache_tools_cmd = cache_sub.add_parser("tools", help="List available cache tools")
  cache_tools_cmd.add_argument("--json", action="store_true", help="Output JSON")

  cache_gaps_cmd = cache_sub.add_parser("gaps", help="Show doc gaps vs known function data")
  cache_gaps_cmd.add_argument("--json", action="store_true", help="Output JSON")

  cache_validate_cmd = cache_sub.add_parser("validate", help="Validate cache front matter")
  cache_validate_cmd.add_argument("--json", action="store_true", help="Output JSON")

  cache_disk_cmd = cache_sub.add_parser("disk-usage", help="Show cache disk usage")
  cache_disk_cmd.add_argument("--json", action="store_true", help="Output JSON")

  cache_recon_cmd = cache_sub.add_parser("reconciliation", help="Show reconciliation notes")
  cache_recon_cmd.add_argument("--json", action="store_true", help="Output JSON")

  cache_tags_cmd = cache_sub.add_parser("pattern-tags", help="Show pattern tag index")
  cache_tags_cmd.add_argument("--json", action="store_true", help="Output JSON")

  cache_run_cmd = cache_sub.add_parser("run", help="Run a cache maintenance tool synchronously")
  cache_run_cmd.add_argument("tool_id", help="Tool id from 'cache tools'")
  cache_run_cmd.add_argument("--set", action="append", default=[], help="Option in FLAG=VALUE form (repeatable)")
  cache_run_cmd.add_argument("--flag", action="append", default=[], help="Boolean option flag to enable (repeatable)")
  cache_run_cmd.add_argument("--json", action="store_true", help="Output JSON")

  fs_cwd_cmd = fs_sub.add_parser("cwd", help="Print current project root")
  fs_cwd_cmd.add_argument("--json", action="store_true", help="Output JSON")

  fs_chdir_cmd = fs_sub.add_parser("chdir", help="Change project root directory")
  fs_chdir_cmd.add_argument("path", help="New project root path")
  fs_chdir_cmd.add_argument("--json", action="store_true", help="Output JSON")

  fs_list_cmd = fs_sub.add_parser("list", help="List project tree")
  fs_list_cmd.add_argument("--json", action="store_true", help="Output JSON")

  fs_read_cmd = fs_sub.add_parser("read", help="Read a project-relative file")
  fs_read_cmd.add_argument("path", help="Project-relative path")
  fs_read_cmd.add_argument("--json", action="store_true", help="Output JSON")

  fs_write_cmd = fs_sub.add_parser("write", help="Write a project-relative file")
  fs_write_cmd.add_argument("path", help="Project-relative path to write")
  fs_write_cmd.add_argument("content_file", nargs="?", default="", help="Path to content file")
  fs_write_cmd.add_argument("--stdin", action="store_true", help="Read content from stdin")
  fs_write_cmd.add_argument("--json", action="store_true", help="Output JSON")

  fs_mkdir_cmd = fs_sub.add_parser("mkdir", help="Create a project-relative directory")
  fs_mkdir_cmd.add_argument("path", help="Project-relative directory path")
  fs_mkdir_cmd.add_argument("--json", action="store_true", help="Output JSON")

  fs_delete_cmd = fs_sub.add_parser("delete", help="Delete a project-relative file or folder")
  fs_delete_cmd.add_argument("path", help="Project-relative path")
  fs_delete_cmd.add_argument("--json", action="store_true", help="Output JSON")

  fs_rename_cmd = fs_sub.add_parser("rename", help="Rename or move a project-relative path")
  fs_rename_cmd.add_argument("from_path", help="Source project-relative path")
  fs_rename_cmd.add_argument("to_path", help="Destination project-relative path")
  fs_rename_cmd.add_argument("--json", action="store_true", help="Output JSON")

  known = {"serve", "status", "search", "doc", "lookup", "completions", "check", "analyze", "debug", "format", "flatten", "fs", "cache", "run-skill"}
  normalized = list(argv)

  legacy_map = {
    "-browser": "--as-browser",
    "-webview": "--as-webview",
    "-none": "--no-open",
    "-no-open": "--no-open",
    "-port": "--port",
    "-host": "--host",
    "-window-mode": "--window-mode",
    "-use-external": "--use-external",
  }
  normalized = [legacy_map.get(token, token) for token in normalized]
  if normalized and normalized[0] in ("-h", "--help"):
    return parser.parse_args(normalized)
  if not normalized or normalized[0] not in known:
    normalized = ["serve"] + normalized
  return parser.parse_args(normalized)


def initialize_runtime() -> None:
  _log(f"SLCode starting")
  _log(f"  cache root : {CACHE_ROOT}")
  _log(f"  project    : {PROJECT_ROOT}")
  _log(f"  skills     : {SKILLS_PATH}")

  if not CACHE_ROOT.exists():
    raise RuntimeError(f"Cache not found at {CACHE_ROOT}")

  t_start = time.time()
  _log("Loading checker skills…")
  load_checkers()
  _log("Pre-loading checker data…")
  preload_checker_data()
  build_index()
  _log(f"Startup complete ({time.time()-t_start:.2f}s total)")


def cli_status(as_json: bool = False) -> int:
  build_index()
  status = get_cache_status()
  payload = {
    "cache_root": str(CACHE_ROOT),
    "project_root": str(PROJECT_ROOT),
    "index_count": len(INDEX),
    "status": status,
  }
  if as_json:
    _emit_json(payload)
  else:
    print(f"Cache root : {payload['cache_root']}")
    print(f"Project    : {payload['project_root']}")
    print(f"Index docs : {payload['index_count']}")
    print(f"Total docs : {status.get('total', 0)}")
  return 0


def cli_search(query: str, category: str, limit: int, as_json: bool = False) -> int:
  build_index()
  results = search(query, category)
  shown = results[: max(1, limit)]
  if as_json:
    _emit_json(shown)
    return 0
  print(f"{len(results)} result(s)")
  for idx, item in enumerate(shown, 1):
    sig = item.get("signature") or ""
    sig_sfx = f" — {sig}" if sig else ""
    print(f"{idx:2d}. [{item.get('category')}] {item.get('name')} ({item.get('path')}){sig_sfx}")
  return 0


def cli_doc(rel_path: str, body_lines: int, as_json: bool = False) -> int:
  doc_path = (CACHE_ROOT / rel_path).resolve()
  if not str(doc_path).startswith(str(CACHE_ROOT.resolve())):
    print("ERROR: forbidden path")
    return 2
  if not doc_path.exists():
    print(f"ERROR: not found: {rel_path}")
    return 2
  text = doc_path.read_text(encoding="utf-8", errors="replace")
  fm, body = parse_front_matter(text)
  payload = {"path": rel_path, "front_matter": fm, "body": body}
  if as_json:
    _emit_json(payload)
    return 0
  print(f"Path: {rel_path}")
  print(f"Name: {fm.get('name', '')}")
  print(f"Category: {fm.get('category', '')}")
  if fm.get("signature"):
    print(f"Signature: {fm.get('signature')}")
  print("-" * 72)
  preview = "\n".join(body.splitlines()[: max(1, body_lines)])
  print(preview)
  return 0


def cli_lookup(name: str, as_json: bool = False) -> int:
  payload = lookup_cache_doc(name)
  if as_json:
    _emit_json(payload)
    return 0 if not payload.get("error") else 1
  if payload.get("error"):
    print(f"ERROR: {payload['error']}")
    return 1
  if not payload.get("found"):
    print(f"No cache entry found for: {name}")
    return 0
  fm = payload.get("front_matter", {})
  print(f"Name: {payload.get('name', '')}")
  print(f"Path: {payload.get('path', '')}")
  if fm.get("signature"):
    print(f"Signature: {fm['signature']}")
  if fm.get("description"):
    print(f"Description: {fm['description']}")
  meta = [
    f"category={fm.get('category')}" if fm.get("category") else "",
    f"type={fm.get('type')}" if fm.get("type") else "",
    f"return={fm.get('return_type')}" if fm.get("return_type") else "",
  ]
  meta = [m for m in meta if m]
  if meta:
    print("Meta: " + ", ".join(meta))
  body = str(payload.get("body", "")).strip()
  if body:
    print("-" * 72)
    print("\n".join(body.splitlines()[:20]))
  return 0


def cli_completions(prefix: str = "", limit: int = 0, as_json: bool = False) -> int:
  items = get_ide_completions()
  prefix = (prefix or "").strip().lower()
  if prefix:
    items = [item for item in items if str(item.get("label", "")).lower().startswith(prefix)]
  if limit and limit > 0:
    items = items[:limit]
  if as_json:
    _emit_json(items)
    return 0
  print(f"{len(items)} completion(s)")
  for item in items:
    print(f"[{item.get('kind', '')}] {item.get('label', '')}")
  return 0


def _read_cli_source(path: str, read_stdin: bool) -> tuple[str | None, str | None]:
  """Read source either from file path or stdin. Returns (source, error)."""
  if read_stdin:
    try:
      return sys.stdin.read(), None
    except Exception as e:
      return None, f"Could not read stdin: {e}"
  if not path:
    return None, "No input source provided"
  try:
    return Path(path).read_text(encoding="utf-8", errors="replace"), None
  except Exception as e:
    return None, f"Could not read file '{path}': {e}"


def cli_check(path: str, mode: str, as_json: bool = False, read_stdin: bool = False,
              ossl: bool = False, firestorm: bool = False) -> int:
  source, error = _read_cli_source(path, read_stdin)
  if error:
    if as_json:
      _emit_json({"error": error})
    else:
      print(f"ERROR: {error}")
    return 2
  payload = run_checks(source, mode, ossl=ossl, firestorm=firestorm)
  has_errors = payload.get("stats", {}).get("errors", 0) > 0
  if as_json:
    _emit_json(payload)
    return 0 if not payload.get("error") and not has_errors else 1
  if payload.get("error"):
    print(f"ERROR: {payload['error']}")
    return 1
  stats = payload.get("stats", {})
  print(f"Errors: {stats.get('errors', 0)}  Warnings: {stats.get('warnings', 0)}  Notes: {stats.get('infos', 0)}")
  for issue in payload.get("issues", []):
    print(f"[{issue.get('severity')}] {issue.get('code')} L{issue.get('line', 0)}: {issue.get('message')}")
  return 1 if has_errors else 0


def cli_analyze(path: str, as_json: bool = False, read_stdin: bool = False) -> int:
  source, error = _read_cli_source(path, read_stdin)
  if error:
    if as_json:
      _emit_json({"error": error})
    else:
      print(f"ERROR: {error}")
    return 2
  payload = run_all_analyses(source)
  if as_json:
    _emit_json(payload)
    return 0 if not payload.get("error") else 1
  if payload.get("error"):
    print(f"ERROR: {payload['error']}")
    return 1
  print(json.dumps(payload, indent=2, ensure_ascii=False))
  return 0


def cli_debug(path: str, mode: str, as_json: bool = False, read_stdin: bool = False,
              ossl: bool = False, firestorm: bool = False) -> int:
  source, error = _read_cli_source(path, read_stdin)
  if error:
    if as_json:
      _emit_json({"error": error})
    else:
      print(f"ERROR: {error}")
    return 2
  payload = {
    "check": run_checks(source, mode, ossl=ossl, firestorm=firestorm),
    "analyze": run_all_analyses(source),
  }
  has_errors = payload["check"].get("stats", {}).get("errors", 0) > 0
  if as_json:
    _emit_json(payload)
    return 0 if not payload["check"].get("error") and not payload["analyze"].get("error") and not has_errors else 1
  print(json.dumps(payload, indent=2, ensure_ascii=False))
  return 1 if has_errors else 0


def cli_format(path: str, as_json: bool = False, read_stdin: bool = False) -> int:
  source, error = _read_cli_source(path, read_stdin)
  if error:
    if as_json:
      _emit_json({"error": error})
    else:
      print(f"ERROR: {error}")
    return 2
  payload = format_lsl(source)
  if as_json:
    _emit_json(payload)
    return 0 if not payload.get("error") else 1
  if payload.get("error"):
    print(f"ERROR: {payload['error']}")
    return 1
  _emit_text(payload.get("formatted", source))
  return 0


def cli_flatten(path: str, as_json: bool = False, read_stdin: bool = False) -> int:
  source, error = _read_cli_source(path, read_stdin)
  if error:
    if as_json:
      _emit_json({"error": error})
    else:
      print(f"ERROR: {error}")
    return 2
  payload = flatten_lsl(source)
  if as_json:
    _emit_json(payload)
    return 0 if not payload.get("error") else 1
  if payload.get("error"):
    print(f"ERROR: {payload['error']}")
    return 1
  _emit_text(payload.get("flattened", source))
  return 0


def cli_fs(args) -> int:
  payload = None
  if args.fs_command == "cwd":
    payload = fs_cwd()
  elif args.fs_command == "chdir":
    payload = fs_chdir(args.path)
  elif args.fs_command == "list":
    payload = fs_list()
  elif args.fs_command == "read":
    payload = fs_read(args.path)
  elif args.fs_command == "write":
    content, error = _read_cli_source(args.content_file, args.stdin)
    payload = {"error": error} if error else fs_write(args.path, content)
  elif args.fs_command == "mkdir":
    payload = fs_mkdir(args.path)
  elif args.fs_command == "delete":
    payload = fs_delete(args.path)
  elif args.fs_command == "rename":
    payload = fs_rename(args.from_path, args.to_path)
  else:
    payload = {"error": f"Unknown fs command: {args.fs_command}"}

  if getattr(args, "json", False):
    _emit_json(payload)
    return 0 if not payload.get("error") else 1
  if payload.get("error"):
    print(f"ERROR: {payload['error']}")
    return 1
  print(json.dumps(payload, indent=2, ensure_ascii=False))
  return 0


def cli_cache(args) -> int:
  payload = None
  if args.cache_command == "status":
    payload = get_cache_status()
  elif args.cache_command == "reload":
    build_index(force=True)
    payload = {"ok": True, "count": len(INDEX)}
  elif args.cache_command == "tools":
    payload = [{k: v for k, v in t.items() if k != "cmd"} for t in CACHE_TOOLS]
  elif args.cache_command == "gaps":
    payload = get_doc_gaps()
  elif args.cache_command == "validate":
    payload = validate_cache_frontmatter()
  elif args.cache_command == "disk-usage":
    payload = get_disk_usage()
  elif args.cache_command == "reconciliation":
    payload = get_reconciliation()
  elif args.cache_command == "pattern-tags":
    payload = get_pattern_tags()
  elif args.cache_command == "run":
    tool = next((t for t in CACHE_TOOLS if t["id"] == args.tool_id), None)
    if not tool:
      payload = {"error": f"Unknown tool: {args.tool_id}"}
    else:
      cmd = list(tool["cmd"])
      bool_flags = set(args.flag or [])
      set_map = {}
      for item in args.set or []:
        if "=" not in item:
          payload = {"error": f"Invalid --set value: {item}"}
          break
        key, value = item.split("=", 1)
        set_map[key] = value
      if payload is None:
        for opt in tool.get("options", []):
          flag = opt["flag"]
          if opt["type"] == "bool":
            if flag in bool_flags:
              cmd.append(flag)
          elif flag in set_map and set_map[flag] != "":
            cmd.append(f"{flag}={set_map[flag]}")
        try:
          env = os.environ.copy()
          env["LSL_CACHE_BASE"] = str(CACHE_BASE)
          proc = subprocess.run(
            cmd,
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=600,
            creationflags=0,
            env=env,
          )
          payload = {"tool_id": args.tool_id, "output": proc.stdout + proc.stderr, "exit_code": proc.returncode}
        except subprocess.TimeoutExpired:
          payload = {"tool_id": args.tool_id, "error": "tool timed out"}
        except Exception as e:
          payload = {"tool_id": args.tool_id, "error": str(e)}
  else:
    payload = {"error": f"Unknown cache command: {args.cache_command}"}

  if getattr(args, "json", False):
    _emit_json(payload)
    if isinstance(payload, dict) and payload.get("error"):
      return 1
    if isinstance(payload, dict) and payload.get("exit_code") not in (None, 0):
      return 1
    return 0
  if isinstance(payload, dict) and payload.get("error"):
    print(f"ERROR: {payload['error']}")
    return 1
  print(json.dumps(payload, indent=2, ensure_ascii=False))
  if isinstance(payload, dict) and payload.get("exit_code") not in (None, 0):
    return 1
  return 0


def _is_gui_launch() -> bool:
  """Best-effort detection for Explorer/shortcut launch (no interactive terminal)."""
  try:
    return sys.platform == "win32" and (not sys.stdin.isatty()) and (not sys.stdout.isatty())
  except Exception:
    return sys.platform == "win32"



def serve_ui(port: int, host: str, force_browser: bool, force_webview: bool,
             no_open: bool, window_mode: str = "auto") -> int:
  if force_browser and force_webview:
    print("ERROR: --as-browser and --as-webview are mutually exclusive.")
    return 2

  # Single-instance guard — only one server at a time.
  # CLI commands never call serve_ui so they are unaffected.
  _instance_lock = _acquire_instance_lock(port)
  if _instance_lock is None:
    return 0  # another instance is running; browser was opened to it

  # Record our PID so the C stub can terminate us on a force-extract restart.
  try:
    _SERVER_PID_FILE.parent.mkdir(parents=True, exist_ok=True)
    _SERVER_PID_FILE.write_text(str(os.getpid()))
  except Exception:
    pass

  if _startup_file:
    _log(f"External editor mode: {_startup_file}")
    JsApi().watch_file(str(_startup_file))

  browse_host = "127.0.0.1" if host in ("0.0.0.0", "::") else host
  url = f"http://{browse_host}:{port}"
  _log(f"Starting server on http://{host}:{port}")

  server = ThreadingHTTPServer((host, port), Handler)
  shutdown_lock = threading.Lock()
  shutdown_requested = {"value": False}
  signal_exit_requested = {"value": False}
  force_exit_on_signal = {"value": False}
  window_exit_requested = {"value": False}
  tray_state = {"icon": None, "thread": None}

  def _create_tray_icon_image():
    from PIL import Image, ImageDraw
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((6, 6, 58, 58), radius=12, fill=(24, 24, 24, 255))
    draw.rounded_rectangle((12, 12, 52, 52), radius=10, fill=(45, 125, 255, 255))
    draw.rectangle((18, 30, 46, 36), fill=(255, 255, 255, 255))
    return img

  def _stop_tray_icon() -> None:
    icon = tray_state["icon"]
    if not icon:
      return
    try:
      icon.stop()
    except Exception:
      pass

  def _tray_diag(msg: str) -> None:
    try:
      _tl = Path(tempfile.gettempdir()) / "slcode-launcher.log"
      with _tl.open("a", encoding="utf-8", errors="replace") as _tf:
        _tf.write(f"tray: {msg}\n")
    except Exception:
      pass

  def _start_tray_icon() -> None:
    if sys.platform != "win32":
      return
    if tray_state["icon"] is not None:
      return
    try:
      import pystray
      _tray_diag("pystray imported ok")
    except Exception as e:
      _tray_diag(f"pystray import failed: {e}")
      _log(f"Tray unavailable (pystray missing): {e}")
      return
    try:
      icon_image = _create_tray_icon_image()
      _tray_diag("icon image created ok")
    except Exception as e:
      _tray_diag(f"icon image failed: {e}")
      _log(f"Tray unavailable (icon creation failed): {e}")
      return

    def _open_ui(_icon, _item):
      try:
        webbrowser.open(url)
      except Exception:
        pass

    def _quit_from_tray(_icon, _item):
      window_exit_requested["value"] = True
      _request_shutdown("Tray close requested — shutting down…")
      try:
        if _pv_window:
          _pv_window.destroy()
      except Exception:
        pass
      try:
        if app_proc and app_proc.poll() is None:
          app_proc.terminate()
      except Exception:
        pass
      _exit_process_soon(0.8)

    menu = pystray.Menu(
      pystray.MenuItem("Open SLCode", _open_ui),
      pystray.MenuItem("Close SLCode", _quit_from_tray),
    )
    icon = pystray.Icon("SLCode", icon_image, "SLCode server active", menu)
    tray_state["icon"] = icon
    def _run_icon():
      try:
        icon.run()
        _tray_diag("icon.run() returned normally")
      except Exception as _ie:
        _tray_diag(f"icon.run() raised: {_ie}")
    t = threading.Thread(target=_run_icon, daemon=True)
    tray_state["thread"] = t
    t.start()
    _tray_diag("tray thread started")

  def _request_shutdown(reason: str = "") -> None:
    with shutdown_lock:
      if shutdown_requested["value"]:
        return
      shutdown_requested["value"] = True
    if reason:
      _log(reason)
    _stop_tray_icon()
    try:
      if app_proc and app_proc.poll() is None:
        app_proc.terminate()
    except Exception:
      pass
    try:
      if _pv_window:
        _pv_window.destroy()
    except Exception:
      pass
    try:
      server.shutdown()
    except Exception:
      pass

  global _shutdown_fn
  _shutdown_fn = _request_shutdown

  old_sigint = None
  old_sigterm = None

  def _install_signal_handlers() -> None:
    nonlocal old_sigint, old_sigterm
    if threading.current_thread() is not threading.main_thread():
      return
    try:
      old_sigint = signal.getsignal(signal.SIGINT)
      signal.signal(signal.SIGINT, _signal_handler)
    except Exception:
      old_sigint = None
    try:
      old_sigterm = signal.getsignal(signal.SIGTERM)
      signal.signal(signal.SIGTERM, _signal_handler)
    except Exception:
      old_sigterm = None

  def _restore_signal_handlers() -> None:
    if threading.current_thread() is not threading.main_thread():
      return
    try:
      if old_sigint is not None:
        signal.signal(signal.SIGINT, old_sigint)
    except Exception:
      pass
    try:
      if old_sigterm is not None:
        signal.signal(signal.SIGTERM, old_sigterm)
    except Exception:
      pass

  def _signal_handler(signum, _frame):
    try:
      signame = signal.Signals(signum).name
    except Exception:
      signame = str(signum)
    signal_exit_requested["value"] = True
    _request_shutdown(f"Signal received ({signame}) — shutting down…")

  _install_signal_handlers()

  if force_browser:
    open_mode = "browser"
  elif force_webview:
    open_mode = "webview"
  else:
    open_mode = window_mode

  if no_open:
    open_mode = "none"

  if open_mode == "auto":
    _env_mode = os.environ.get("SLCODE_WINDOW_MODE", "")
    _tray_diag(f"serve_ui: SLCODE_WINDOW_MODE={_env_mode!r} _is_gui_launch={_is_gui_launch()}")
    if _env_mode in ("webview", "browser", "none"):
      open_mode = _env_mode
    else:
      try:
        import webview  # noqa: F401
        open_mode = "webview"
        _log("pywebview detected — using native window")
      except Exception as _wv_ex:
        _tray_diag(f"serve_ui: webview import failed: {_wv_ex}")
        open_mode = "browser"

  _tray_diag(f"serve_ui: open_mode={open_mode}")

  force_exit_on_signal["value"] = open_mode in ("browser", "none")

  if open_mode == "webview":
    try:
      import webview
    except Exception as e:
      _log(f"ERROR: webview mode requested but pywebview failed to load: {e}")
      _log("  Install with: pip install pywebview")
      server.server_close()
      return 2
    import webview
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    _signal_splash_server()   # splash: "Starting server…"
    _start_tray_icon()
    _log("Opening pywebview window…")
    global _pv_window
    _pv_window = webview.create_window(
      "SLCode",
      url=url,
      js_api=JsApi(),
      width=1400,
      height=900,
      resizable=True,
      min_size=(800, 600),
      background_color="#0F1117",
      frameless=False,
      easy_drag=False,
    )

    def _on_webview_closed(*_args):
      window_exit_requested["value"] = True
      _request_shutdown("Window closed — shutting down server…")

    try:
      _pv_window.events.closed += _on_webview_closed
    except Exception:
      pass

    # events.loaded fires when the WebView2 DOM is ready — show "Ready" on the
    # splash.  JS then calls /api/splash-ready once init() finishes, which
    # closes the splash.  The 3-second sleep is a fallback in case JS never fires.
    def _on_page_loaded():
      _apply_native_window_frame()
      _signal_splash_pageload()   # splash: "Ready"
      time.sleep(3)               # give JS time to call /api/splash-ready
      _signal_splash_ready()      # fallback close (idempotent if JS already did it)
    try:
      _pv_window.events.loaded += lambda: threading.Thread(
        target=_on_page_loaded, daemon=True).start()
    except Exception:
      pass

    _tray_diag("serve_ui: calling webview.start()")
    _signal_splash_webview()  # splash: "Opening window…"
    try:
      webview.start(debug=False)
      _tray_diag("serve_ui: webview.start() returned normally")
    except KeyboardInterrupt:
      signal_exit_requested["value"] = True
      _request_shutdown("Keyboard interrupt received — shutting down…")
    except Exception as _webview_exc:
      import traceback as _tb
      _tray_diag(f"serve_ui: webview.start() raised: {_webview_exc}")
      _wv_log = Path(tempfile.gettempdir()) / "slcode-launcher.log"
      try:
        with _wv_log.open("a", encoding="utf-8", errors="replace") as _f:
          _f.write(f"webview-start-error: {_webview_exc}\n")
          _f.write(_tb.format_exc())
      except Exception:
        pass
    finally:
      _tray_diag("serve_ui: webview finally block — calling os._exit(0)")
      _request_shutdown()
      _pv_window = None
      server.server_close()
      _restore_signal_handlers()
      _release_instance_lock(_instance_lock)
      _log("Server stopped.")
      os._exit(0)
    return 0

  _start_tray_icon()

  # Run server in a daemon thread so the main thread remains interruptible.
  # Calling server.shutdown() from a signal handler while serve_forever() is
  # on the same thread causes a deadlock; this pattern avoids that entirely.
  server_thread = threading.Thread(target=server.serve_forever, daemon=True)
  server_thread.start()

  if no_open:
    _log(f"No-open mode: serving at {url}")
    _signal_splash_ready()  # no window to wait for — dismiss splash now
  else:
    if force_browser:
      _log("Browser mode (--as-browser) — opening system browser.")
    else:
      _log("pywebview not available — opening system browser.")
      _log("  Install with: pip install pywebview")
    webbrowser.open(url)
    _signal_splash_ready()  # browser is opening — dismiss splash

  _log(f"Serving on {url}  (Ctrl+C to stop)")
  try:
    while not shutdown_requested["value"]:
      time.sleep(0.25)
  except KeyboardInterrupt:
    signal_exit_requested["value"] = True
    _request_shutdown("Keyboard interrupt received — shutting down…")
  finally:
    _request_shutdown()
    server.server_close()
    _restore_signal_handlers()
    _release_instance_lock(_instance_lock)
    _log("Server stopped.")
    if signal_exit_requested["value"] and force_exit_on_signal["value"]:
      os._exit(0)
  return 0


def main():
  global _startup_file, _QUIET_MODE
  args = parse_cli_args(sys.argv[1:])

  _QUIET_MODE = bool(getattr(args, "json", False))

  if getattr(args, "use_external", ""):
    p = Path(args.use_external).resolve()
    if p.exists() and p.is_file():
      _startup_file = p
      _log(f"External editor mode: {p}")
    else:
      _log(f"WARNING: --use-external path not found: {p}")

  if args.command == "run-skill":
    return run_skill_cmd(args.skill, args.args or [])

  # Suppress startup logs for non-serve CLI commands (check, search, etc.)
  # so they don't clutter the command output.  Restored after init.
  _is_serve = (args.command == "serve")
  if not _is_serve:
    _QUIET_MODE = True

  try:
    initialize_runtime()
  except Exception as e:
    print(f"[slcode-cli] ERROR: {e}", file=sys.stderr, flush=True)
    return 1

  # Restore quiet mode to the --json flag value after silent startup
  if not _is_serve:
    _QUIET_MODE = bool(getattr(args, "json", False))

  if args.command == "status":
    return cli_status(args.json)
  if args.command == "search":
    return cli_search(" ".join(args.query), args.cat, args.limit, args.json)
  if args.command == "doc":
    return cli_doc(args.path, args.body_lines, args.json)
  if args.command == "lookup":
    return cli_lookup(args.name, args.json)
  if args.command == "completions":
    return cli_completions(args.prefix, args.limit, args.json)
  if args.command == "check":
    return cli_check(args.path, args.mode, args.json, args.stdin,
                     ossl=getattr(args, 'ossl', False), firestorm=getattr(args, 'fs', False))
  if args.command == "analyze":
    return cli_analyze(args.path, args.json, args.stdin)
  if args.command == "debug":
    return cli_debug(args.path, args.mode, args.json, args.stdin,
                     ossl=getattr(args, 'ossl', False), firestorm=getattr(args, 'fs', False))
  if args.command == "format":
    return cli_format(args.path, args.json, args.stdin)
  if args.command == "flatten":
    return cli_flatten(args.path, args.json, args.stdin)
  if args.command == "fs":
    return cli_fs(args)
  if args.command == "cache":
    return cli_cache(args)

  return serve_ui(
    port=args.port,
    host=args.host,
    force_browser=args.as_browser,
    force_webview=args.as_webview,
    no_open=args.no_open,
    window_mode=args.window_mode,
  )


if __name__ == "__main__":
  raise SystemExit(main())
