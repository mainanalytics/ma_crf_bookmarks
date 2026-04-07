# -*- mode: python ; coding: utf-8 -*-

datas = [
    ('ma.ico', '.'),
    ('images/error_sign.png', 'images'),
    ('images/warning_sign.png', 'images'),
    ('images/ok_sign.png', 'images'),
    ('images/Python-logo-notext.svg.png', 'images'),
    ('images/mainanalytics_Logo.png', 'images'),
]


a = Analysis(
    ['src\ma_crf_bookmarks\main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[],
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
    name='ma_crf_bookmarks v0.1.0',
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
    icon=['ma.ico'],
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='GBS CRF Bookmarks v0.1.0',
)
