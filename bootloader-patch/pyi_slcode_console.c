/*
 * SLCode console management for PyInstaller CONSOLE-subsystem bootloader.
 *
 * Compiled into run.exe (CONSOLE subsystem) bootloader variant.
 * Called from wmain() in main.c before pyi_main().
 *
 * Strategy: CONSOLE subsystem is used for all launches so that cmd.exe blocks
 * when the user runs with log flags (-browser/-none) from a terminal.  For
 * silent double-click launches (Cases 1 & 3 with no flags), the watcher
 * re-launches itself with CREATE_NO_WINDOW and exits immediately — before the
 * console window has been drawn — so there is no visible flash.
 *
 *   SLCODE_SILENT_CHILD / SLCODE_FORCE_INLINE set
 *       → silent child (re-launched or detached server); return immediately.
 *
 *   No log flags AND no terminal env (double-click, no args):
 *       → set SLCODE_SILENT_CHILD=1 in env, re-launch self with CREATE_NO_WINDOW,
 *         FreeConsole(), TerminateProcess — exits before window is rendered.
 *
 *   Has terminal env OR log flags:
 *       → return; CONSOLE subsystem has already set up the correct handles
 *         (inherited terminal console or auto-created console for log window).
 */

#ifdef _WIN32

#include <windows.h>
#include <wchar.h>

#include "pyi_slcode_console.h"

/* ---------------------------------------------------------------------------
 * Helpers
 * --------------------------------------------------------------------------*/

static int
_slcode_wants_logs(void)
{
    static const wchar_t *flags[] = {
        L"-browser", L"--as-browser", L"-none", L"--no-open", NULL
    };
    const wchar_t *cmdline = GetCommandLineW();
    const wchar_t *p;
    int i;

    if (!cmdline) return 0;

    for (i = 0; flags[i]; i++) {
        p = wcsstr(cmdline, flags[i]);
        if (p) {
            if (p == cmdline || *(p - 1) == L' ' ||
                *(p - 1) == L'"' || *(p - 1) == L'\t') {
                return 1;
            }
        }
    }
    return 0;
}

static int
_slcode_has_env(const wchar_t *name)
{
    wchar_t buf[4];
    DWORD ret = GetEnvironmentVariableW(name, buf, 4);
    return (ret > 0) || (GetLastError() == ERROR_INSUFFICIENT_BUFFER);
}

static int
_slcode_is_terminal(void)
{
    return _slcode_has_env(L"PROMPT") ||
           _slcode_has_env(L"PSModulePath") ||
           _slcode_has_env(L"WT_SESSION");
}

/* ---------------------------------------------------------------------------
 * Re-launch self with CREATE_NO_WINDOW so the silent child runs with no
 * console at all, then return so the caller can FreeConsole + TerminateProcess.
 * --------------------------------------------------------------------------*/
static void
_slcode_relaunch_silent(void)
{
    wchar_t exe[32768];
    STARTUPINFOW si;
    PROCESS_INFORMATION pi;

    if (!GetModuleFileNameW(NULL, exe, 32768)) {
        return;
    }

    /* Set marker before CreateProcessW so child inherits it. */
    SetEnvironmentVariableW(L"SLCODE_SILENT_CHILD", L"1");

    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(si);
    ZeroMemory(&pi, sizeof(pi));

    /* CREATE_NO_WINDOW: CONSOLE-subsystem child with no console window.
     * bInheritHandles=FALSE: do not pass our (about-to-be-freed) console. */
    if (CreateProcessW(
            exe,               /* lpApplicationName */
            GetCommandLineW(), /* lpCommandLine — same args */
            NULL,              /* lpProcessAttributes */
            NULL,              /* lpThreadAttributes */
            FALSE,             /* bInheritHandles */
            CREATE_NO_WINDOW,  /* dwCreationFlags */
            NULL,              /* lpEnvironment — inherit ours (has SLCODE_SILENT_CHILD) */
            NULL,              /* lpCurrentDirectory */
            &si,
            &pi))
    {
        CloseHandle(pi.hProcess);
        CloseHandle(pi.hThread);
    }
}

/* ---------------------------------------------------------------------------
 * Early constructor — runs before wmain() and before PyInstaller archive init.
 * Priority 101 fires before default-priority (0) constructors that PyInstaller
 * may register for onefile extraction / archive setup.
 * --------------------------------------------------------------------------*/
#ifdef __GNUC__
__attribute__((constructor(101)))
static void
_pyi_slcode_early_init(void)
{
    pyi_slcode_setup_console();
}
#endif /* __GNUC__ */

/* ---------------------------------------------------------------------------
 * Public entry point — called from wmain() before pyi_main().
 * --------------------------------------------------------------------------*/
void
pyi_slcode_setup_console(void)
{
    /* Silent re-launched child (Case 1) or detached server child (Case 3).
     * CREATE_NO_WINDOW already gave us no console; just proceed. */
    if (_slcode_has_env(L"SLCODE_SILENT_CHILD") ||
        _slcode_has_env(L"SLCODE_FORCE_INLINE")) {
        return;
    }

    /* Has terminal env OR log flags: keep the console.
     *   - Terminal (Cases 3/4/CLI): inherited from parent shell — no new window. ✓
     *   - Double-click with log flags (Case 2): auto-created console window. ✓
     * CONSOLE subsystem already wired stdin/stdout/stderr correctly. */
    if (_slcode_is_terminal() || _slcode_wants_logs()) {
        return;
    }

    /* Case 1: double-click, no log flags.
     * Re-launch self silently (CREATE_NO_WINDOW) so the child does the real
     * work without a console, then exit this watcher ASAP.
     * The window created by the OS for this CONSOLE-subsystem process will be
     * destroyed by FreeConsole + TerminateProcess before it is rendered. */
    _slcode_relaunch_silent();
    FreeConsole();
    TerminateProcess(GetCurrentProcess(), 0);
    /* unreachable */
}

#endif /* _WIN32 */
