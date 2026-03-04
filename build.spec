# -*- mode: python ; coding: utf-8 -*-
import os

# 读取版本号
version_file = os.path.join(os.path.dirname(os.path.abspath(SPEC)), 'VERSION')
if os.path.exists(version_file):
    with open(version_file, 'r', encoding='utf-8') as f:
        version = f.read().strip()
else:
    version = '1.5'

block_cipher = None

a = Analysis(
    ['pcwatcher.py'],
    pathex=[],
    binaries=[],
    datas=[('VERSION', '.'), ('CHANGELOG.md', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=f'PCWatcher_V{version}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)