#!/usr/bin/env python3
"""
Build script — packages search-cache.py into a standalone executable.

Requirements:
    pip install pyinstaller pywebview

Usage:
    python build.py                     # onedir + zip (default — fast subsequent launches)
    python build.py --onefile           # legacy single-file mode
    python build.py --windowed          # WINDOWS subsystem app bundle (debug only)
    python build.py --prune-artifacts   # remove PyInstaller build cache/spec after success

Default (onedir + zip) output:
    dist/SLCode.exe          <- users run this (tiny WINDOWS-subsystem stub)
    dist/SLCode-app.zip      <- app bundle; stub extracts to %%LOCALAPPDATA%%\\SLCode\\ on first run

Notes:
- WebView2 runtime must be present on the target machine.
  On Windows 10/11 with Edge installed it is already there.
- The local `LSL Cache/` directory is bundled into the application.
- On first launch the stub extracts SLCode-app.zip to
    %%LOCALAPPDATA%%\\SLCode\\SLCode-app\\ via PowerShell.
  Subsequent launches start directly from the extracted directory with no
  extraction overhead.
"""

import os
import subprocess
import sys
import shutil
import zipfile
from pathlib import Path

ROOT            = Path(__file__).parent
SCRIPT          = ROOT / "slcode-launcher.py"
STUB_SRC        = ROOT / "slcode-stub.c"
STUB_RC         = ROOT / "slcode-res.rc"
STUB_RES_OBJ    = ROOT / "build" / "slcode-res.o"
APP_BUNDLE_NAME = "SLCode-app"
CACHE_DIR       = ROOT / "LSL Cache"
LSLINT_EXE      = ROOT / "lslint.exe"
LSLINT_BUILTINS = ROOT / "lslint-builtins.txt"
SEARCH_CACHE_SCRIPT = ROOT / "search-cache.py"
RUNTIME_STAGING  = ROOT / ".build-staging"
RUNTIME_PAYLOAD = RUNTIME_STAGING / "_slcode_runtime.py"
RUNTIME_MODULE  = RUNTIME_STAGING / "slcode_runtime.py"

# Hidden imports required by runtime backends (pywebview + tray support)
HIDDEN = [
    "webview",
    "webview.platforms.winforms",
    "webview.platforms.edgechromium",
    "clr",          # pythonnet — used by pywebview on Windows
    "System",
    "pystray",
    "pystray._win32",
    "PIL",
    "PIL.Image",
    "PIL.ImageDraw",
    "html.parser",  # used by generate-docs-from-cache skill
    "html.entities",
    "xml.etree.ElementTree",  # used by generate-ossl-from-kwdb skill
    "bottle",        # pywebview 6.x internal HTTP server (webview/http.py)
    "proxy_tools",   # pywebview 6.x module property helper (webview/__init__.py)
]


def main():
    onefile        = "--onefile" in sys.argv
    windowed       = "--windowed" in sys.argv
    prune_artifacts = "--prune-artifacts" in sys.argv

    payload, runtime_module = _prepare_runtime_payloads()
    try:
        cmd = _build_command(
            name=APP_BUNDLE_NAME,
            console_mode=not windowed,
            onefile=onefile,
            runtime_payload=payload,
            runtime_module=runtime_module,
        )
        print(f"Running: {' '.join(cmd)}\n")
        result = subprocess.run(cmd, cwd=str(ROOT))
        if result.returncode != 0:
            print("\nPyInstaller build failed — check output above.")
            sys.exit(1)

        if onefile:
            app_out      = ROOT / "dist" / (APP_BUNDLE_NAME + ".exe")
            app_version  = _build_version_string()
            stub_out = _build_stub_exe(ROOT / "dist" / "SLCode.exe",     console=False, app_version=app_version)
            cli_out  = _build_stub_exe(ROOT / "dist" / "slcode-cli.exe", console=True,  app_version=app_version)
            _sign_exe(stub_out)
            _sign_exe(cli_out)
            print(f"\nBuild complete (onefile mode).")
            print(f"  {stub_out}  <- double-click / GUI launch")
            print(f"  {cli_out}   <- terminal / CLI launch")
            print(f"  {app_out}   <- spawned by stub")
        else:
            # onedir: write version.txt, zip the bundle, stub extracts on first launch
            bundle_dir   = ROOT / "dist" / APP_BUNDLE_NAME
            zip_out      = ROOT / "dist" / (APP_BUNDLE_NAME + ".zip")
            app_version  = _build_version_string()
            _write_version_file(bundle_dir, app_version)
            print(f"\nZipping {bundle_dir} ...")
            _build_zip(bundle_dir, zip_out)
            stub_out = _build_stub_exe(ROOT / "dist" / "SLCode.exe",     console=False, app_version=app_version)
            cli_out  = _build_stub_exe(ROOT / "dist" / "slcode-cli.exe", console=True,  app_version=app_version)
            _sign_exe(stub_out)
            _sign_exe(cli_out)
            print(f"\nBuild complete.")
            print(f"  {stub_out}   <- double-click / GUI launch")
            print(f"  {cli_out}    <- terminal / CLI launch")
            print(f"  {zip_out}  <- extracted to %LOCALAPPDATA%\\SLCode\\ on first launch")

        if prune_artifacts:
            _prune_artifacts()
    finally:
        for p in (payload, runtime_module):
            try:
                p.unlink(missing_ok=True)
            except Exception:
                pass


def _prepare_runtime_payloads() -> tuple[Path, Path]:
    RUNTIME_STAGING.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SEARCH_CACHE_SCRIPT, RUNTIME_PAYLOAD)
    shutil.copyfile(SEARCH_CACHE_SCRIPT, RUNTIME_MODULE)
    return RUNTIME_PAYLOAD, RUNTIME_MODULE


def _build_zip(bundle_dir: Path, zip_out: Path) -> None:
    """Zip the onedir bundle so the stub can extract it on first launch.

    The archive root is `SLCode-app/` so extracting to %LOCALAPPDATA%\\SLCode\\
    produces %LOCALAPPDATA%\\SLCode\\SLCode-app\\SLCode-app.exe.
    """
    total = sum(1 for _ in bundle_dir.rglob("*") if _.is_file())
    done  = 0
    with zipfile.ZipFile(zip_out, "w", compression=zipfile.ZIP_DEFLATED,
                         compresslevel=6) as zf:
        for path in sorted(bundle_dir.rglob("*")):
            if path.is_file():
                arcname = path.relative_to(bundle_dir.parent)  # SLCode-app/...
                zf.write(path, arcname)
                done += 1
                if done % 100 == 0 or done == total:
                    print(f"  zipped {done}/{total} files...", end="\r")
    size_mb = zip_out.stat().st_size / 1024 / 1024
    print(f"  {zip_out.name}  ({size_mb:.1f} MB, {total} files)          ")


def _compile_resource(gcc: str) -> Path | None:
    """Compile slcode-res.rc into slcode-res.o using windres.

    windres is in the same bin directory as gcc. Returns the object path on
    success, or None if windres is not found or the source .rc file is missing.
    """
    if not STUB_RC.exists():
        print("WARNING: slcode-res.rc not found — icon will not be embedded.")
        return None

    gcc_exe  = Path(gcc)
    gcc_bin  = gcc_exe.parent
    windres  = gcc_bin / "windres.exe"
    if not windres.exists():
        windres_on_path = shutil.which("windres")
        if windres_on_path:
            windres = Path(windres_on_path)
        else:
            print("WARNING: windres not found — icon will not be embedded.")
            return None

    STUB_RES_OBJ.parent.mkdir(parents=True, exist_ok=True)

    # windres calls gcc -E as a preprocessor; gcc needs its own bin dir in
    # PATH to locate cc1.exe, and -xc so it treats the .rc file as C source.
    import tempfile as _tf
    win_tmp  = os.path.normpath(_tf.gettempdir())
    msys2_usr = gcc_bin.parent.parent / "usr" / "bin"
    env = dict(os.environ)
    env["PATH"]  = (str(gcc_bin) + os.pathsep
                    + str(msys2_usr) + os.pathsep
                    + env.get("PATH", ""))
    env["TEMP"]  = win_tmp
    env["TMP"]   = win_tmp

    cmd = [
        str(windres),
        "--use-temp-file",
        f"--preprocessor={gcc_exe}",
        "--preprocessor-arg=-E",
        "--preprocessor-arg=-DRC_INVOKED",
        "--preprocessor-arg=-xc",
        str(STUB_RC),
        "-O", "coff",
        "-o", str(STUB_RES_OBJ),
    ]
    print(f"Compiling resources: windres {STUB_RC.name} -> {STUB_RES_OBJ.name}")

    result = subprocess.run(cmd, cwd=str(ROOT), env=env, stderr=subprocess.PIPE)
    if result.stderr:
        print(result.stderr.decode(errors="replace"), end="")
    if result.returncode != 0:
        print("WARNING: windres failed — icon will not be embedded.")
        return None

    return STUB_RES_OBJ


def _build_version_string() -> str:
    """Generate a build version string.

    Format: YYYYMMDD-HHMMSS-<git-short-hash> (or ...-local)

    Include wall-clock time so repeated local builds (without new commits)
    still produce a new version string. This guarantees the launcher stub's
    version.txt check triggers re-extraction after every rebuild.
    """
    from datetime import datetime
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    try:
        import subprocess as _sp
        result = _sp.run(
            ["git", "rev-parse", "--short=8", "HEAD"],
            capture_output=True, text=True, cwd=str(ROOT), timeout=5
        )
        if result.returncode == 0:
            short = result.stdout.strip()
            return f"{stamp}-{short}"
    except Exception:
        pass
    return f"{stamp}-local"


def _write_version_file(bundle_dir: Path, version: str) -> None:
    """Write version.txt into the bundle directory before zipping."""
    version_file = bundle_dir / "version.txt"
    version_file.write_text(version + "\n", encoding="utf-8")
    print(f"  version.txt: {version}")


def _build_stub_exe(out_path: Path, console: bool = False, app_version: str = "") -> Path:
    """Compile slcode-stub.c into an exe using MinGW gcc.

    console=False  ->  WINDOWS subsystem (SLCode.exe)  — no console ever.
    console=True   ->  CONSOLE subsystem (slcode-cli.exe) — inherits terminal.
    """
    gcc = shutil.which("gcc")
    if not gcc:
        candidate = Path(r"C:\msys64\mingw64\bin\gcc.exe")
        if candidate.exists():
            gcc = str(candidate)
        else:
            print("WARNING: gcc not found — stub not built. Add MinGW to PATH.")
            return out_path

    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Compile resource file (.rc -> .o) so the icon is embedded in both stubs.
    res_obj = _compile_resource(gcc)

    cmd = [
        gcc,
        str(STUB_SRC),
        "-o", str(out_path),
        "-O2",
        "-Wall",
        "-municode",         # wWinMain / wmain unicode entry point
        "-lkernel32",
        "-luser32",
        "-lole32",
        "-lgdi32",           # GDI functions used by the GUI splash window
        "-static",
        "-static-libgcc",
        "-static-libstdc++",
    ]
    if res_obj:
        cmd.append(str(res_obj))   # link embedded icon resource
    if app_version:
        cmd.append(f"-DAPP_VERSION=\"{app_version}\"")
    if console:
        cmd.append("-DCONSOLE_MODE")   # selects wmain + inherit-console path
    else:
        cmd.append("-mwindows")        # WINDOWS subsystem — no console ever
    print(f"Building stub: {' '.join(cmd)}\n")

    # MSYS2/MinGW's cc1.exe needs the MinGW bin dirs in PATH to find DLLs.
    import tempfile as _tf
    win_tmp   = os.path.normpath(_tf.gettempdir())
    gcc_exe   = Path(gcc)
    msys2_bin = gcc_exe.parent
    msys2_usr = gcc_exe.parent.parent.parent / "usr" / "bin"
    gcc_env   = dict(os.environ)
    gcc_env["PATH"] = (str(msys2_bin) + os.pathsep
                       + str(msys2_usr) + os.pathsep
                       + gcc_env.get("PATH", ""))
    gcc_env["TEMP"] = win_tmp
    gcc_env["TMP"]  = win_tmp

    result = subprocess.run(cmd, cwd=str(ROOT), env=gcc_env,
                            stderr=subprocess.PIPE)
    if result.stderr:
        print(result.stderr.decode(errors="replace"), end="")
    if result.returncode != 0:
        print("\nStub build failed.")
        sys.exit(1)
    return out_path


def _find_signtool() -> str | None:
    """Locate signtool.exe from the Windows SDK or PATH."""
    on_path = shutil.which("signtool")
    if on_path:
        return on_path
    # Search common Windows SDK locations (newest first)
    sdk_root = Path(r"C:\Program Files (x86)\Windows Kits\10\bin")
    if sdk_root.exists():
        candidates = sorted(sdk_root.glob("10.*/x64/signtool.exe"), reverse=True)
        if candidates:
            return str(candidates[0])
    return None


def _sign_exe(exe_path: Path) -> bool:
    """Sign exe_path with Authenticode using env-var-configured certificate.

    Supported env vars (checked in order):
      SLCODE_SIGN_THUMBPRINT  — SHA1 thumbprint of a cert already in the store
                                (required for EV certs / hardware tokens)
      SLCODE_SIGN_CERT        — path to a PFX file
      SLCODE_SIGN_PASS        — password for the PFX file (optional)

    Always uses SHA256 digest + RFC3161 timestamp so the signature remains
    valid after the certificate expires.

    Returns True on success, False on skip (not configured), exits on failure.
    """
    signtool = _find_signtool()
    if not signtool:
        print("WARNING: signtool.exe not found — skipping signing.")
        return False

    thumbprint = os.environ.get("SLCODE_SIGN_THUMBPRINT", "").strip()
    cert_path  = os.environ.get("SLCODE_SIGN_CERT", "").strip()

    if not thumbprint and not cert_path:
        print("INFO: No signing credentials configured — skipping signing.")
        print("      Set SLCODE_SIGN_THUMBPRINT (cert store) or")
        print("      SLCODE_SIGN_CERT + SLCODE_SIGN_PASS (PFX file).")
        return False

    timestamp_url = os.environ.get("SLCODE_SIGN_TIMESTAMP", "http://timestamp.digicert.com")

    cmd = [signtool, "sign", "/fd", "SHA256", "/tr", timestamp_url, "/td", "SHA256"]

    if thumbprint:
        cmd += ["/sha1", thumbprint]
    else:
        cmd += ["/f", cert_path]
        cert_pass = os.environ.get("SLCODE_SIGN_PASS", "").strip()
        if cert_pass:
            cmd += ["/p", cert_pass]

    cmd.append(str(exe_path))

    print(f"Signing: {exe_path.name} ...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="")
    if result.returncode != 0:
        print(f"\nERROR: signtool failed for {exe_path.name} (exit {result.returncode})")
        sys.exit(1)
    print(f"  Signed OK: {exe_path.name}")
    return True


def _build_command(name: str, console_mode: bool, onefile: bool,
                   runtime_payload: Path, runtime_module: Path) -> list[str]:
    app_icon = ROOT / "slcode-cli.ico"
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name", name,
        "--console" if console_mode else "--noconsole",
        "--clean",
        "-y",            # overwrite dist output dir without prompting
    ]
    if app_icon.exists():
        cmd += ["--icon", str(app_icon)]

    cmd += ["--paths", str(runtime_module.parent)]
    cmd += ["--hidden-import", "slcode_runtime"]

    for hi in HIDDEN:
        cmd += ["--hidden-import", hi]

    cmd += ["--collect-all", "webview"]
    cmd += ["--collect-all", "pythonnet"]
    cmd += ["--collect-all", "pystray"]
    cmd += ["--collect-all", "PIL"]

    data_sep = ";" if sys.platform.startswith("win") else ":"
    if CACHE_DIR.exists():
        cmd += ["--add-data", f"{CACHE_DIR}{data_sep}LSL Cache"]
        if LSLINT_BUILTINS.exists():
            cmd += ["--add-data", f"{LSLINT_BUILTINS}{data_sep}."]
    if runtime_payload.exists():
        cmd += ["--add-data", f"{runtime_payload}{data_sep}."]
    if LSLINT_EXE.exists():
        cmd += ["--add-binary", f"{LSLINT_EXE}{data_sep}."]

    cmd.append("--onefile" if onefile else "--onedir")
    cmd.append(str(SCRIPT))
    return cmd


def _prune_artifacts():
    removed = []
    for build_dir in [ROOT / "build" / APP_BUNDLE_NAME,
                      ROOT / "build" / "LSL Cache"]:
        if build_dir.exists():
            shutil.rmtree(build_dir, ignore_errors=True)
            removed.append(str(build_dir))
    for spec_file in [ROOT / f"{APP_BUNDLE_NAME}.spec"]:
        if spec_file.exists():
            spec_file.unlink(missing_ok=True)
            removed.append(str(spec_file))
    if removed:
        print("Pruned build artifacts:")
        for p in removed:
            print(f"  - {p}")
    else:
        print("No build artifacts to prune.")


if __name__ == "__main__":
    main()
