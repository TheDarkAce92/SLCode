/*
 * SLCode launcher stub.
 *
 * Compiled twice:
 *   SLCode.exe     — WINDOWS subsystem (-mwindows), no console ever.
 *                    For double-click / GUI launch.  Always shows a splash
 *                    window with an animated progress bar; stays visible until
 *                    Python signals a named event (SLCodeReady_<pid>) or
 *                    until 30 s timeout.
 *   slcode-cli.exe — CONSOLE subsystem (-DCONSOLE_MODE), inherits terminal.
 *                    For command-line use.  Shows a spinner on stderr while
 *                    extracting.  Detaches cleanly when used as a GUI launcher.
 *
 * SLCode-app.zip (next to this exe) contains the full PyInstaller onedir
 * application bundle.  On first launch — or when the zip is newer than what
 * was previously extracted — the bundle is extracted to
 *
 *     %LOCALAPPDATA%\SLCode\SLCode-app\
 *
 * using .NET's ZipFile class (via PowerShell).  Every subsequent launch
 * starts directly from the extracted directory: no bundle scan, no extraction.
 *
 * Flags:
 *   -extract                Force re-extraction even if already up-to-date.
 *                           Same effect as deleting SLCode-app\version.txt.
 *   -browser / --as-browser
 *   -none    / --no-open    Log flags (WINDOWS stub only): open a new console.
 *
 * Files written to %LOCALAPPDATA%\SLCode\:
 *   SLCode-app\             Extracted application bundle.
 *   SLCode-app\version.txt  Build version string embedded at compile time.
 *                           Delete this file to force re-extraction on next launch.
 */

#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <wchar.h>
#include <stdlib.h>
#include <stdio.h>

#define SBUF 32768

/* ── Icon resource ID (defined in slcode-res.rc) ────────────────────────── */
#define IDI_APP 1

/* ── Launch modes (passed to _run) ──────────────────────────────────────── */
#define MODE_GUI      0  /* SLCode.exe   — splash + named-event wait          */
#define MODE_CLI_CMD  1  /* slcode-cli   — running a command, wait for exit   */
#define MODE_CLI_GUI  2  /* slcode-cli   — launching GUI (serve), detach      */

/* ── Flag detection ──────────────────────────────────────────────────────── */

static int
_has_flag(const wchar_t *flag)
{
    const wchar_t *cmdline = GetCommandLineW();
    const wchar_t *p;
    size_t flen;
    wchar_t before, after;

    if (!cmdline || !flag) return 0;
    flen = wcslen(flag);
    p = wcsstr(cmdline, flag);
    if (!p) return 0;
    before = (p == cmdline) ? L' ' : *(p - 1);
    after  = *(p + flen);
    return (before == L' ' || before == L'"' || before == L'\t') &&
           (after  == L'\0' || after  == L' ' || after  == L'\t');
}

static void
_strip_flag(const wchar_t *src, const wchar_t *flag, wchar_t *dst)
{
    size_t flen = wcslen(flag);
    const wchar_t *s = src;
    wchar_t *d = dst;
    int stripped = 0;

    while (*s && (d - dst) < SBUF - 1) {
        if (!stripped && (*s == L' ' || *s == L'\t')) {
            if (wcsncmp(s + 1, flag, flen) == 0) {
                wchar_t after = *(s + 1 + flen);
                if (after == L'\0' || after == L' ' || after == L'\t') {
                    s += 1 + flen;
                    stripped = 1;
                    continue;
                }
            }
        }
        *d++ = *s++;
    }
    *d = L'\0';
}

static int
_wants_logs(void)
{
    static const wchar_t *flags[] = {
        L"-browser", L"--as-browser", L"-none", L"--no-open", NULL
    };
    const wchar_t *cmdline = GetCommandLineW();
    int i;

    if (!cmdline) return 0;
    for (i = 0; flags[i]; i++) {
        const wchar_t *p = wcsstr(cmdline, flags[i]);
        if (p) {
            wchar_t before = (p == cmdline) ? L' ' : *(p - 1);
            if (before == L' ' || before == L'"' || before == L'\t')
                return 1;
        }
    }
    return 0;
}

/* ── Version file ────────────────────────────────────────────────────────── */

#ifndef APP_VERSION
#define APP_VERSION "dev"
#endif

/*
 * Read the first line of a UTF-8 text file into buf (max buflen-1 chars).
 * Returns 1 on success, 0 if the file doesn't exist or can't be read.
 * Strips trailing whitespace / newlines.
 */
static int
_read_version_file(const wchar_t *path, char *buf, int buflen)
{
    HANDLE h;
    DWORD  nr;
    int    i;

    h = CreateFileW(path, GENERIC_READ, FILE_SHARE_READ, NULL,
                    OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (h == INVALID_HANDLE_VALUE) return 0;
    ReadFile(h, buf, (DWORD)(buflen - 1), &nr, NULL);
    CloseHandle(h);
    buf[nr] = '\0';
    /* strip trailing newline / whitespace */
    for (i = (int)nr - 1; i >= 0 && (buf[i] == '\r' || buf[i] == '\n' ||
                                      buf[i] == ' '  || buf[i] == '\t'); i--)
        buf[i] = '\0';
    return nr > 0;
}

/* ── Debug helper (console mode only) ───────────────────────────────────── */

#ifdef CONSOLE_MODE
#define DBG(fmt, ...) (fwprintf(stderr, L"[slcode-cli] " fmt L"\n", ##__VA_ARGS__), fflush(stderr))
#else
#define DBG(fmt, ...) ((void)0)
#endif

/* ═══════════════════════════════════════════════════════════════════════════
 * CONSOLE MODE — terminal spinner
 * ═══════════════════════════════════════════════════════════════════════════ */

#ifdef CONSOLE_MODE

static volatile int      _spin_run    = 0;
static volatile LPCWSTR  _spin_msg    = L"";
static HANDLE            _spin_handle = NULL;

static DWORD WINAPI
_spin_thread(LPVOID unused)
{
    static const wchar_t * const frames[] = { L"|", L"/", L"-", L"\\" };
    int i = 0;
    (void)unused;
    while (_spin_run) {
        fwprintf(stderr, L"\r  %ls  %ls   ", frames[i & 3], _spin_msg);
        fflush(stderr);
        i++;
        Sleep(120);
    }
    /* Erase the spinner line */
    fwprintf(stderr, L"\r                                                  \r");
    fflush(stderr);
    return 0;
}

static void
_spin_start(LPCWSTR msg)
{
    _spin_msg = msg;
    _spin_run = 1;
    _spin_handle = CreateThread(NULL, 0, _spin_thread, NULL, 0, NULL);
}

static void
_spin_stop(void)
{
    if (!_spin_handle) return;
    _spin_run = 0;
    WaitForSingleObject(_spin_handle, 600);
    CloseHandle(_spin_handle);
    _spin_handle = NULL;
}

#endif /* CONSOLE_MODE */

/* ═══════════════════════════════════════════════════════════════════════════
 * GUI MODE — splash window
 * ═══════════════════════════════════════════════════════════════════════════ */

#ifndef CONSOLE_MODE

/* Theme colours matching the app's dark palette */
#define COL_BG     RGB(0x1e, 0x1e, 0x2e)   /* dark background  */
#define COL_TITLE  RGB(0xcd, 0xd6, 0xf4)   /* near-white title */
#define COL_STATUS RGB(0x6c, 0x70, 0x86)   /* muted-grey status */
#define COL_TRACK  RGB(0x31, 0x32, 0x44)   /* progress track   */
#define COL_BAR    RGB(0x89, 0xb4, 0xfa)   /* accent blue bar  */

#define SPLASH_W   420
#define SPLASH_H   120
#define BAR_H      5
#define SPLASH_CLS L"SLCodeSplash"

static HWND    g_splash    = NULL;
static HFONT   g_font_big  = NULL;
static HFONT   g_font_sm   = NULL;
static wchar_t g_status[256] = L"Initialising\u2026";
static int     g_anim_pos  = 0;

static LRESULT CALLBACK
_splash_proc(HWND hwnd, UINT msg, WPARAM wp, LPARAM lp)
{
    switch (msg) {

    case WM_ERASEBKGND:
        return 1;  /* suppress flicker; WM_PAINT fills everything */

    case WM_PAINT: {
        PAINTSTRUCT ps;
        HDC hdc = BeginPaint(hwnd, &ps);
        RECT rc;
        GetClientRect(hwnd, &rc);

        /* ── Background ── */
        HBRUSH bg = CreateSolidBrush(COL_BG);
        FillRect(hdc, &rc, bg);
        DeleteObject(bg);

        SetBkMode(hdc, TRANSPARENT);

        /* ── Title ── */
        RECT r_title = { 20, 18, rc.right - 20, 52 };
        SelectObject(hdc, g_font_big);
        SetTextColor(hdc, COL_TITLE);
        DrawTextW(hdc, L"SLCode", -1, &r_title,
                  DT_LEFT | DT_VCENTER | DT_SINGLELINE);

        /* ── Status ── */
        RECT r_status = { 20, 52, rc.right - 20, 82 };
        SelectObject(hdc, g_font_sm);
        SetTextColor(hdc, COL_STATUS);
        DrawTextW(hdc, g_status, -1, &r_status,
                  DT_LEFT | DT_VCENTER | DT_SINGLELINE);

        /* ── Progress bar (marquee) ── */
        RECT r_track = { 0, rc.bottom - BAR_H, rc.right, rc.bottom };
        HBRUSH trk = CreateSolidBrush(COL_TRACK);
        FillRect(hdc, &r_track, trk);
        DeleteObject(trk);

        int bar_w  = rc.right;
        int seg_w  = bar_w / 3;
        int travel = bar_w + seg_w;
        int pos    = (g_anim_pos * 4) % travel - seg_w;
        RECT r_seg = { pos, r_track.top, pos + seg_w, r_track.bottom };
        if (r_seg.left  < 0)       r_seg.left  = 0;
        if (r_seg.right > bar_w)   r_seg.right = bar_w;
        if (r_seg.left < r_seg.right) {
            HBRUSH bar = CreateSolidBrush(COL_BAR);
            FillRect(hdc, &r_seg, bar);
            DeleteObject(bar);
        }

        EndPaint(hwnd, &ps);
        return 0;
    }

    case WM_TIMER:
        g_anim_pos++;
        InvalidateRect(hwnd, NULL, FALSE);
        return 0;

    case WM_DESTROY:
        return 0;
    }
    return DefWindowProcW(hwnd, msg, wp, lp);
}

static void
_splash_create(void)
{
    WNDCLASSEXW wc = {0};
    wc.cbSize        = sizeof(wc);
    wc.style         = CS_HREDRAW | CS_VREDRAW;
    wc.lpfnWndProc   = _splash_proc;
    wc.hInstance     = GetModuleHandleW(NULL);
    wc.hIcon         = LoadIconW(GetModuleHandleW(NULL), MAKEINTRESOURCEW(IDI_APP));
    wc.hCursor       = LoadCursorW(NULL, IDC_ARROW);
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);
    wc.lpszClassName = SPLASH_CLS;
    RegisterClassExW(&wc);

    /* Fonts */
    g_font_big = CreateFontW(22, 0, 0, 0, FW_SEMIBOLD, FALSE, FALSE, FALSE,
                              DEFAULT_CHARSET, OUT_DEFAULT_PRECIS,
                              CLIP_DEFAULT_PRECIS, CLEARTYPE_QUALITY,
                              DEFAULT_PITCH | FF_SWISS, L"Segoe UI");
    g_font_sm  = CreateFontW(14, 0, 0, 0, FW_NORMAL, FALSE, FALSE, FALSE,
                              DEFAULT_CHARSET, OUT_DEFAULT_PRECIS,
                              CLIP_DEFAULT_PRECIS, CLEARTYPE_QUALITY,
                              DEFAULT_PITCH | FF_SWISS, L"Segoe UI");

    /* Centre on screen */
    int sw = GetSystemMetrics(SM_CXSCREEN);
    int sh = GetSystemMetrics(SM_CYSCREEN);
    int x  = (sw - SPLASH_W) / 2;
    int y  = (sh - SPLASH_H) / 2;

    g_splash = CreateWindowExW(
        WS_EX_TOOLWINDOW | WS_EX_TOPMOST,
        SPLASH_CLS, L"SLCode",
        WS_POPUP | WS_VISIBLE,
        x, y, SPLASH_W, SPLASH_H,
        NULL, NULL, GetModuleHandleW(NULL), NULL);

    SetTimer(g_splash, 1, 40, NULL);   /* ~25 fps animation */
    UpdateWindow(g_splash);
}

static void
_splash_set_status(const wchar_t *text)
{
    if (!g_splash) return;
    wcsncpy(g_status, text, 255);
    g_status[255] = L'\0';
    InvalidateRect(g_splash, NULL, FALSE);
    /* Pump a quick round so the repaint actually lands */
    MSG msg;
    while (PeekMessageW(&msg, NULL, 0, 0, PM_REMOVE)) {
        TranslateMessage(&msg);
        DispatchMessageW(&msg);
    }
}

static void
_splash_destroy(void)
{
    if (!g_splash) return;
    KillTimer(g_splash, 1);
    DestroyWindow(g_splash);
    g_splash = NULL;
    if (g_font_big) { DeleteObject(g_font_big); g_font_big = NULL; }
    if (g_font_sm)  { DeleteObject(g_font_sm);  g_font_sm  = NULL; }
}

/*
 * Pump the splash message loop while waiting for hproc to finish.
 * Used during the PowerShell extraction step only.
 */
static void
_splash_wait_proc(HANDLE hproc)
{
    MSG msg;
    while (1) {
        DWORD r = MsgWaitForMultipleObjects(1, &hproc, FALSE,
                                            INFINITE, QS_ALLINPUT);
        if (r == WAIT_OBJECT_0) break;   /* process finished */
        while (PeekMessageW(&msg, NULL, 0, 0, PM_REMOVE)) {
            TranslateMessage(&msg);
            DispatchMessageW(&msg);
        }
    }
}

/*
 * Startup stage events fired by Python to update the splash text.
 * Each entry is an auto-reset named event + the status string to display.
 * The ready event (manual-reset, NULL text) is handled separately — it
 * closes the splash rather than updating the label.
 */
typedef struct { HANDLE h; const wchar_t *text; } SplashStage;

/*
 * Wait for either the child process to exit, a Python stage event, the
 * ready-close event, or the 30-second timeout.  Pumps the message loop
 * throughout so the splash animation stays alive.
 *
 * stages / nstages — auto-reset events that update the splash label.
 * hready           — manual-reset event that closes the splash.
 */
static void
_splash_wait_ready(HANDLE hproc,
                   SplashStage *stages, DWORD nstages,
                   HANDLE hready)
{
    HANDLE handles[8];   /* proc + up to 6 stage events + ready */
    DWORD  nhandles   = 0;
    DWORD  stage_base;
    DWORD  idx_ready  = (DWORD)-1;
    DWORD  i;
    MSG    msg;
    DWORD  r;

    handles[nhandles++] = hproc;
    stage_base = nhandles;
    for (i = 0; i < nstages; i++)
        if (stages[i].h) handles[nhandles++] = stages[i].h;
    if (hready) { idx_ready = nhandles; handles[nhandles++] = hready; }

    for (;;) {
        r = MsgWaitForMultipleObjects(nhandles, handles, FALSE,
                                      30000, QS_ALLINPUT);
        if (r == WAIT_OBJECT_0) break;  /* child exited */
        if (r == WAIT_TIMEOUT)  break;

        /* message queue — pump and continue */
        if (r == WAIT_OBJECT_0 + nhandles) {
            while (PeekMessageW(&msg, NULL, 0, 0, PM_REMOVE)) {
                TranslateMessage(&msg);
                DispatchMessageW(&msg);
            }
            continue;
        }

        /* ready event — close splash */
        if (idx_ready != (DWORD)-1 && r == WAIT_OBJECT_0 + idx_ready)
            break;

        /* stage event — update splash text and keep waiting */
        i = r - WAIT_OBJECT_0 - stage_base;
        if (i < nstages && stages[i].text)
            _splash_set_status(stages[i].text);
    }
}

#endif /* !CONSOLE_MODE */

/* ── Extraction via PowerShell / .NET ZipFile ────────────────────────────── */

/*
 * Extract zip_path into dest_dir using .NET's ZipFile class via PowerShell.
 * In GUI mode the splash message loop is pumped during the wait.
 * Returns 1 on success, 0 on failure.
 */
static int
_extract_zip(const wchar_t *zip_path, const wchar_t *dest_dir)
{
    static wchar_t tmp_ps1[SBUF];
    static wchar_t script[SBUF * 4];
    static wchar_t ps_cmdline[SBUF];
    STARTUPINFOW si;
    PROCESS_INFORMATION pi;
    HANDLE hf;
    DWORD nw, exit_code = 1;
    BOOL ok;
    static const BYTE bom[2] = {0xFF, 0xFE};

    if (!GetTempPathW(SBUF, tmp_ps1)) return 0;
    wcsncat(tmp_ps1, L"slcode-extract.ps1", SBUF - 1 - wcslen(tmp_ps1));

    _snwprintf(script, SBUF * 4 - 1,
        L"Add-Type -Assembly System.IO.Compression.FileSystem\r\n"
        L"$app = Join-Path '%ls' 'SLCode-app'\r\n"
        L"if (Test-Path $app) { Remove-Item $app -Recurse -Force }\r\n"
        L"[System.IO.Compression.ZipFile]::ExtractToDirectory('%ls', '%ls')\r\n",
        dest_dir, zip_path, dest_dir);

    hf = CreateFileW(tmp_ps1, GENERIC_WRITE, 0, NULL,
                     CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hf == INVALID_HANDLE_VALUE) return 0;
    WriteFile(hf, bom, 2, &nw, NULL);
    WriteFile(hf, script, (DWORD)(wcslen(script) * sizeof(wchar_t)), &nw, NULL);
    CloseHandle(hf);

    _snwprintf(ps_cmdline, SBUF - 1,
        L"powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass "
        L"-WindowStyle Hidden -File \"%ls\"",
        tmp_ps1);

    ZeroMemory(&si, sizeof(si)); si.cb = sizeof(si);
    ZeroMemory(&pi, sizeof(pi));

    ok = CreateProcessW(NULL, ps_cmdline,
                        NULL, NULL, FALSE, CREATE_NO_WINDOW,
                        NULL, NULL, &si, &pi);
    if (!ok) {
        DeleteFileW(tmp_ps1);
        return 0;
    }

#ifdef CONSOLE_MODE
    WaitForSingleObject(pi.hProcess, INFINITE);
#else
    _splash_wait_proc(pi.hProcess);
#endif

    GetExitCodeProcess(pi.hProcess, &exit_code);
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);
    DeleteFileW(tmp_ps1);
    return exit_code == 0 ? 1 : 0;
}

/* ── Shared launch logic ─────────────────────────────────────────────────── */

/*
 * mode = MODE_GUI      — SLCode.exe: always show splash, wait for ready event
 * mode = MODE_CLI_CMD  — slcode-cli command: wait for child exit
 * mode = MODE_CLI_GUI  — slcode-cli serve/no-args: print detach msg, exit
 */
static int
_run(int mode)
{
    static wchar_t self_dir[SBUF];
    static wchar_t zip_path[SBUF];
    static wchar_t slcode_dir[SBUF];
    static wchar_t app_dir[SBUF];
    static wchar_t app_exe[SBUF];
    static wchar_t version_file[SBUF];
    static wchar_t local_appdata[SBUF];
    static wchar_t cmdline_buf[SBUF];
    static wchar_t fallback_exe[SBUF];

    wchar_t *sep;
    wchar_t *cmdline;
    STARTUPINFOW si;
    PROCESS_INFORMATION pi;
    DWORD flags;
    DWORD exit_code = 0;
    int logs, force_extract, need_extract, is_update;
    char stored_version[64];
    DWORD attr;
    const wchar_t *launch_exe;
#ifndef CONSOLE_MODE
    HANDLE hReadyEvent    = NULL;
    HANDLE hSeedingEvent  = NULL;
    HANDLE hServerEvent   = NULL;
    HANDLE hWebviewEvent  = NULL;
    HANDLE hPageLoadEvent = NULL;
#endif

    /* ── Locate zip next to this stub ─────────────────────────────────── */
    if (!GetModuleFileNameW(NULL, self_dir, SBUF)) {
        DBG(L"ERROR: GetModuleFileNameW failed");
        return 1;
    }
    sep = wcsrchr(self_dir, L'\\');
    if (!sep) { DBG(L"ERROR: no backslash in module path"); return 1; }
    *(sep + 1) = L'\0';

    wcsncpy(zip_path, self_dir, SBUF - 1); zip_path[SBUF - 1] = L'\0';
    wcsncat(zip_path, L"SLCode-app.zip", SBUF - 1 - wcslen(zip_path));

    DBG(L"self_dir  : %ls", self_dir);
    DBG(L"zip_path  : %ls", zip_path);

    /* ── Resolve %LOCALAPPDATA% ───────────────────────────────────────── */
    if (!GetEnvironmentVariableW(L"LOCALAPPDATA", local_appdata, SBUF))
        local_appdata[0] = L'\0';

    DBG(L"LOCALAPPDATA: %ls", local_appdata[0] ? local_appdata : L"(not set)");

    if (local_appdata[0]) {
        wcsncpy(slcode_dir, local_appdata, SBUF - 1); slcode_dir[SBUF - 1] = L'\0';
        wcsncat(slcode_dir, L"\\SLCode", SBUF - 1 - wcslen(slcode_dir));

        wcsncpy(app_dir, slcode_dir, SBUF - 1); app_dir[SBUF - 1] = L'\0';
        wcsncat(app_dir, L"\\SLCode-app", SBUF - 1 - wcslen(app_dir));

        wcsncpy(app_exe, app_dir, SBUF - 1); app_exe[SBUF - 1] = L'\0';
        wcsncat(app_exe, L"\\SLCode-app.exe", SBUF - 1 - wcslen(app_exe));

        wcsncpy(version_file, app_dir, SBUF - 1); version_file[SBUF - 1] = L'\0';
        wcsncat(version_file, L"\\version.txt", SBUF - 1 - wcslen(version_file));

        DBG(L"app_exe      : %ls", app_exe);
        DBG(L"version_file : %ls", version_file);
    }

    logs          = (mode == MODE_GUI) ? _wants_logs() : 0;
    force_extract = _has_flag(L"-extract");

    if (force_extract) {
        _strip_flag(GetCommandLineW(), L"-extract", cmdline_buf);
        cmdline = cmdline_buf;
    } else {
        cmdline = GetCommandLineW();
    }

    DBG(L"cmdline   : %ls", cmdline);
    DBG(L"mode      : %d", mode);

    /* ── Decide whether extraction is needed ──────────────────────────── */
    need_extract = 0;
    is_update    = 0;

    if (!local_appdata[0]) {
        DBG(L"no LOCALAPPDATA — skipping extraction check");
    } else if (force_extract) {
        DBG(L"force_extract set");
        need_extract = 1;
        attr = GetFileAttributesW(app_exe);
        is_update = (attr != INVALID_FILE_ATTRIBUTES);
    } else if (GetFileAttributesW(zip_path) == INVALID_FILE_ATTRIBUTES) {
        DBG(L"no zip found — skipping extraction");
    } else {
        attr = GetFileAttributesW(app_exe);
        if (attr == INVALID_FILE_ATTRIBUTES) {
            DBG(L"app_exe missing — fresh install");
            need_extract = 1;
            is_update    = 0;
        } else {
            stored_version[0] = '\0';
            _read_version_file(version_file, stored_version, sizeof(stored_version));
            DBG(L"APP_VERSION=%hs  stored=%hs", APP_VERSION, stored_version);
            if (strcmp(stored_version, APP_VERSION) != 0) {
                DBG(L"version mismatch — update needed");
                need_extract = 1;
                is_update    = 1;
            } else {
                DBG(L"version up-to-date — skipping extraction");
            }
        }
    }

    /* ── GUI: always show splash to cover the full load sequence ─────── */
#ifndef CONSOLE_MODE
    _splash_create();
    if (!need_extract)
        _splash_set_status(L"Loading SLCode\u2026");
    else if (is_update)
        _splash_set_status(L"Updating SLCode\u2026");
    else
        _splash_set_status(L"Installing SLCode\u2026");
#endif

    /* ── Force-restart: terminate any running server before extracting ── */
    /* Python writes server-pid.txt when it starts serving.  Reading and
     * terminating it here (before extraction) avoids a race where the new
     * Python finds the old server alive and either defers to it or tries
     * to start a second server on the same port. */
    if (force_extract && local_appdata[0]) {
        static wchar_t pid_file[SBUF];
        char     pid_buf[32];
        HANDLE   hf;
        DWORD    nread;
        DWORD    old_pid;
        HANDLE   hp;

        wcsncpy(pid_file, slcode_dir, SBUF - 1);
        pid_file[SBUF - 1] = L'\0';
        wcsncat(pid_file, L"\\server-pid.txt", SBUF - 1 - wcslen(pid_file));

        hf = CreateFileW(pid_file, GENERIC_READ, FILE_SHARE_READ,
                         NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
        if (hf != INVALID_HANDLE_VALUE) {
            ZeroMemory(pid_buf, sizeof(pid_buf));
            nread = 0;
            ReadFile(hf, pid_buf, sizeof(pid_buf) - 1, &nread, NULL);
            CloseHandle(hf);
            old_pid = (DWORD)atol(pid_buf);
            if (old_pid > 0) {
                hp = OpenProcess(PROCESS_TERMINATE | SYNCHRONIZE, FALSE, old_pid);
                if (hp) {
                    DBG(L"force-restart: terminating server PID %lu",
                        (unsigned long)old_pid);
                    TerminateProcess(hp, 0);
                    WaitForSingleObject(hp, 5000);
                    CloseHandle(hp);
                }
            }
            DeleteFileW(pid_file);
        }
    }

    /* ── Extract if needed ────────────────────────────────────────────── */
    if (need_extract && local_appdata[0]) {
        DBG(L"extracting zip...");
        CreateDirectoryW(slcode_dir, NULL);  /* ignore error if exists */

#ifdef CONSOLE_MODE
        /* CLI: spinner during extraction */
        fwprintf(stderr, L"SLCode: %ls (this may take a moment)...\n",
                 is_update ? L"updating app bundle" : L"extracting app bundle");
        fflush(stderr);
        _spin_start(is_update ? L"Updating..." : L"Extracting...");
        int ok = _extract_zip(zip_path, slcode_dir);
        _spin_stop();
        if (ok) {
            DBG(L"extraction OK");
        } else {
            DBG(L"ERROR: extraction FAILED");
        }
#else
        /* GUI: update splash status during extraction */
        _splash_set_status(is_update
            ? L"Updating app bundle\u2026"
            : L"Installing app bundle\u2026  (this only happens once)");
        if (_extract_zip(zip_path, slcode_dir)) {
            DBG(L"extraction OK");
        } else {
            DBG(L"ERROR: extraction FAILED");
        }
        _splash_set_status(L"Loading SLCode\u2026");
#endif
    }

    /* ── CLI GUI launch: hand off to SLCode.exe so it shows the splash ─ */
    /*
     * slcode-cli without args (or with 'serve') just wants the GUI to open.
     * Rather than spawning the Python app ourselves (no splash possible in a
     * console binary), we launch SLCode.exe — it lives next to us, handles
     * the splash, and takes the same args.
     */
#ifdef CONSOLE_MODE
    if (mode == MODE_CLI_GUI) {
        static wchar_t gui_exe[SBUF];
        static wchar_t gui_cmdline[SBUF];
        STARTUPINFOW     gsi = {0};
        PROCESS_INFORMATION gpi = {0};

        /* Locate SLCode.exe next to this binary */
        wcsncpy(gui_exe, self_dir, SBUF - 1);
        gui_exe[SBUF - 1] = L'\0';
        wcsncat(gui_exe, L"SLCode.exe", SBUF - 1 - wcslen(gui_exe));

        /* Skip our exe-name token from the command line; pass the rest on */
        const wchar_t *rest = cmdline;
        if (*rest == L'"') {
            rest++;
            while (*rest && *rest != L'"') rest++;
            if (*rest) rest++;
        } else {
            while (*rest && *rest != L' ' && *rest != L'\t') rest++;
        }
        while (*rest == L' ' || *rest == L'\t') rest++;

        _snwprintf(gui_cmdline, SBUF - 1, L"\"%ls\" %ls", gui_exe, rest);

        gsi.cb = sizeof(gsi);
        if (GetFileAttributesW(gui_exe) != INVALID_FILE_ATTRIBUTES &&
            CreateProcessW(gui_exe, gui_cmdline,
                           NULL, NULL, FALSE, 0,
                           NULL, NULL, &gsi, &gpi)) {
            CloseHandle(gpi.hProcess);
            CloseHandle(gpi.hThread);
        }

        fwprintf(stderr, L"[slcode-cli] GUI Launched, detaching from terminal\n");
        fflush(stderr);
        return 0;
    }
#endif

    /* ── GUI: create named event + pass PID to child via env var ─────── */
    /*
     * Python signals SLCodeReady_<pid> when the server is up and the
     * window is about to open.  The splash stays alive until that signal
     * (or 30 s timeout), preventing the blank-screen gap.
     */

    /* Tell Python to shut down any existing instance before taking over.
     * Set for force-extract; explicitly cleared otherwise so the env var
     * is never inherited from a parent process by accident. */
    SetEnvironmentVariableW(L"SLCODE_FORCE_RESTART", force_extract ? L"1" : NULL);

#ifndef CONSOLE_MODE
    {
        DWORD  my_pid = GetCurrentProcessId();
        wchar_t pid_str[32], event_name[64];
        _snwprintf(pid_str, 32, L"%lu", (unsigned long)my_pid);
        SetEnvironmentVariableW(L"SLCODE_STUB_PID", pid_str);
        /* Status events (auto-reset) — Python sets these to update the splash label */
        _snwprintf(event_name, 64, L"SLCodeSeeding_%lu",  (unsigned long)my_pid);
        hSeedingEvent  = CreateEventW(NULL, FALSE, FALSE, event_name);
        _snwprintf(event_name, 64, L"SLCodeServer_%lu",   (unsigned long)my_pid);
        hServerEvent   = CreateEventW(NULL, FALSE, FALSE, event_name);
        _snwprintf(event_name, 64, L"SLCodeWebview_%lu",  (unsigned long)my_pid);
        hWebviewEvent  = CreateEventW(NULL, FALSE, FALSE, event_name);
        _snwprintf(event_name, 64, L"SLCodePageLoad_%lu", (unsigned long)my_pid);
        hPageLoadEvent = CreateEventW(NULL, FALSE, FALSE, event_name);
        /* Ready event (manual-reset) — Python sets this to close the splash */
        _snwprintf(event_name, 64, L"SLCodeReady_%lu",    (unsigned long)my_pid);
        hReadyEvent    = CreateEventW(NULL, TRUE,  FALSE, event_name);
        DBG(L"splash events created for pid %lu", (unsigned long)my_pid);
    }
#endif

    /* ── Launch SLCode-app.exe ────────────────────────────────────────── */
    ZeroMemory(&si, sizeof(si)); si.cb = sizeof(si);
    ZeroMemory(&pi, sizeof(pi));

    if (mode == MODE_GUI) {
        flags = logs
            ? CREATE_NEW_CONSOLE
            : (CREATE_NO_WINDOW | 0x01000000u);  /* CREATE_BREAKAWAY_FROM_JOB */
    } else {
        /* MODE_CLI_CMD: inherit console so the child's output flows through */
        flags = 0;
    }

    launch_exe = (local_appdata[0] &&
                  GetFileAttributesW(app_exe) != INVALID_FILE_ATTRIBUTES)
                 ? app_exe : NULL;

    if (!launch_exe) {
        wcsncpy(fallback_exe, self_dir, SBUF - 1); fallback_exe[SBUF - 1] = L'\0';
        wcsncat(fallback_exe, L"SLCode-app.exe",
                SBUF - 1 - wcslen(fallback_exe));
        launch_exe = fallback_exe;
        DBG(L"using fallback exe: %ls", launch_exe);
    } else {
        DBG(L"using extracted exe: %ls", launch_exe);
    }

    DBG(L"CreateProcessW flags=0x%lx inherit=%d",
        (unsigned long)flags, mode == MODE_CLI_CMD);

    if (!CreateProcessW(launch_exe, cmdline,
                        NULL, NULL,
                        (mode == MODE_CLI_CMD) ? TRUE : FALSE,
                        flags,
                        NULL, NULL, &si, &pi)) {
        DBG(L"ERROR: CreateProcessW failed (GLE=%lu)", GetLastError());
#ifndef CONSOLE_MODE
        _splash_destroy();
        if (hReadyEvent) CloseHandle(hReadyEvent);
#endif
        return 1;
    }

    DBG(L"child pid=%lu", (unsigned long)pi.dwProcessId);

#ifdef CONSOLE_MODE
    /* MODE_CLI_CMD: wait for child to complete and propagate exit code */
    WaitForSingleObject(pi.hProcess, INFINITE);
    GetExitCodeProcess(pi.hProcess, &exit_code);
    DBG(L"child exited with code %lu", (unsigned long)exit_code);
#else
    /* GUI stub: keep splash alive until Python signals ready (max 30 s) */
    {
        SplashStage stages[] = {
            { hSeedingEvent,  L"Seeding cache\u2026"   },
            { hServerEvent,   L"Starting server\u2026" },
            { hWebviewEvent,  L"Opening window\u2026"  },
            { hPageLoadEvent, L"Ready"                 },
        };
        _splash_wait_ready(pi.hProcess,
                           stages, sizeof(stages) / sizeof(stages[0]),
                           hReadyEvent);
    }
    _splash_destroy();
    if (hSeedingEvent)  CloseHandle(hSeedingEvent);
    if (hServerEvent)   CloseHandle(hServerEvent);
    if (hWebviewEvent)  CloseHandle(hWebviewEvent);
    if (hPageLoadEvent) CloseHandle(hPageLoadEvent);
    if (hReadyEvent)    CloseHandle(hReadyEvent);
#endif

    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);
    return (mode == MODE_CLI_CMD) ? (int)exit_code : 0;
}

/* ── Entry points ────────────────────────────────────────────────────────── */

#ifdef CONSOLE_MODE

int
wmain(int argc, wchar_t **argv)
{
    /*
     * Detect whether the user is launching the GUI (serve / no args) or
     * running a short-lived CLI command.  The distinction controls whether
     * the stub waits for the child to exit.
     *
     * Known short-lived CLI commands that justify waiting:
     */
    static const wchar_t * const cli_cmds[] = {
        L"check", L"search", L"lookup", L"doc", L"completions",
        L"analyze", L"debug", L"format", L"flatten", L"fs", L"cache",
        L"status", L"run-skill", NULL
    };
    int is_cli_cmd = 0, i;

    if (argc >= 2) {
        for (i = 0; cli_cmds[i]; i++) {
            if (wcscmp(argv[1], cli_cmds[i]) == 0) {
                is_cli_cmd = 1;
                break;
            }
        }
    }

    /* --no-open means a headless server the user wants to watch */
    if (!is_cli_cmd && _has_flag(L"--no-open"))
        is_cli_cmd = 1;

    return _run(is_cli_cmd ? MODE_CLI_CMD : MODE_CLI_GUI);
}

#else

int WINAPI
wWinMain(HINSTANCE hInst, HINSTANCE hPrev, LPWSTR lpCmdLine, int nCmdShow)
{
    (void)hInst; (void)hPrev; (void)lpCmdLine; (void)nCmdShow;
    return _run(MODE_GUI);
}

#endif
