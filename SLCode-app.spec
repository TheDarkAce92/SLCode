# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [('C:\\Users\\ben_c\\Claude Projects\\LSL Queries\\LSL Cache', 'LSL Cache'), ('C:\\Users\\ben_c\\Claude Projects\\LSL Queries\\lslint-builtins.txt', '.'), ('C:\\Users\\ben_c\\Claude Projects\\LSL Queries\\.build-staging\\_slcode_runtime.py', '.')]
binaries = [('C:\\Users\\ben_c\\Claude Projects\\LSL Queries\\lslint.exe', '.')]
hiddenimports = ['slcode_runtime', 'webview', 'webview.platforms.winforms', 'webview.platforms.edgechromium', 'clr', 'System', 'pystray', 'pystray._win32', 'PIL', 'PIL.Image', 'PIL.ImageDraw', 'html.parser', 'html.entities', 'xml.etree.ElementTree', 'bottle', 'proxy_tools']
tmp_ret = collect_all('webview')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('pythonnet')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('pystray')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('PIL')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['C:\\Users\\ben_c\\Claude Projects\\LSL Queries\\slcode-launcher.py'],
    pathex=['C:\\Users\\ben_c\\Claude Projects\\LSL Queries\\.build-staging'],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SLCode-app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\ben_c\\Claude Projects\\LSL Queries\\slcode-cli.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SLCode-app',
)
