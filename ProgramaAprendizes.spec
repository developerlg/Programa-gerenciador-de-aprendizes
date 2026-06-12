# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path


project_dir = Path(SPECPATH)

datas = []
for source, destination in (
    ("assets", "assets"),
    ("data/aprendizes_inicial.db", "data"),
    ("backups", "backups"),
    ("reports", "reports"),
):
    source_path = project_dir / source
    if source_path.exists():
        datas.append((str(source_path), destination))

icon_path = project_dir / "assets" / "icons" / "app.ico"
icon = str(icon_path) if icon_path.exists() else None

a = Analysis(
    ["main.py"],
    pathex=[str(project_dir)],
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
    name="ProgramaAprendizes",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    icon=icon,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="ProgramaAprendizes",
)
