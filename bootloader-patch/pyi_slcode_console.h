/*
 * SLCode console management for PyInstaller CONSOLE-subsystem bootloader.
 *
 * Called from wmain() in main.c before pyi_main(), so the correct console
 * state is established before Python initialises its I/O handles.
 *
 * Rules:
 *   - Log flags in argv (-browser, --as-browser, -none, --no-open)
 *       → do nothing; the console stays attached for output.
 *   - Launched from a terminal (PROMPT, PSModulePath, or WT_SESSION set)
 *       → do nothing; the process exits quickly and the prompt returns.
 *   - Double-click, no log flags
 *       → FreeConsole(); detaches and destroys the auto-created window so
 *          Python starts with no console (silent webview launch).
 */

#ifndef PYI_SLCODE_CONSOLE_H
#define PYI_SLCODE_CONSOLE_H

#ifdef _WIN32

void pyi_slcode_setup_console(void);

#endif /* _WIN32 */

#endif /* PYI_SLCODE_CONSOLE_H */
