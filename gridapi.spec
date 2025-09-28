# -*- mode: python ; coding: utf-8 -*-
# Generic PyInstaller spec file for all platforms

import os
import sys
from pathlib import Path

# Get the current directory (where the spec file is located)
project_root = Path.cwd()

# Determine platform-specific settings
platform = sys.platform
is_windows = platform.startswith('win')
is_macos = platform == 'darwin'
is_linux = platform.startswith('linux')

# Platform-specific executable name
if is_windows:
    exe_name = 'gridapi.exe'
    console = True
else:
    exe_name = 'gridapi'
    console = True

block_cipher = None

# Define the main analysis
a = Analysis(
    ['gridapi/cli.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=[
        ('README.md', '.'),
        ('LICENSE', '.'),
        ('examples', 'examples'),
    ],
    hiddenimports=[
        'gridapi',
        'gridapi.auth',
        'gridapi.client',
        'gridapi.exceptions',
        'gridapi.managers',
        'gridapi.managers.base',
        'gridapi.managers.grid_manager',
        'gridapi.managers.image_manager',
        'gridapi.managers.taskflow_manager',
        'gridapi.models',
        'gridapi.models.base',
        'gridapi.models.grid',
        'gridapi.models.image',
        'gridapi.query',
        'gridapi.query.builder',
        'gridapi.query.filters',
        'gridapi.utils',
        'gridapi.utils.helpers',
        'gridapi.utils.validators',
        'click',
        'rich',
        'rich.console',
        'rich.table',
        'rich.json',
        'requests',
        'pydantic',
        'dateutil',
        'typing_extensions',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'jupyter',
        'IPython',
        'notebook',
        'PyQt5',
        'PyQt6',
        'PySide2',
        'PySide6',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Remove duplicate binaries
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Create the executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=exe_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=console,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)