# PyInstaller spec file voor Schaduwagent
# Bouw met: pyinstaller schaduwagent.spec

a = Analysis(
    ['schaduwagent/main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['pystray._win32' if __import__('platform').system() == 'Windows' else 'pystray._xorg'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='schaduwagent',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Geen terminal-venster (Windows)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # TODO: voeg icoon toe
)
