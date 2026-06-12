# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path


project_dir = Path(SPECPATH)
datas = []


def add_file(relative_path: str, destination: str | None = None) -> None:
    source_path = project_dir / relative_path
    if source_path.exists():
        target_dir = destination if destination is not None else str(Path(relative_path).parent)
        datas.append((str(source_path), target_dir))


def add_tree(relative_dir: str) -> None:
    source_dir = project_dir / relative_dir
    if not source_dir.exists():
        return

    ignored_files = {
        "aprendizes.db",
        "aprendizes.db-journal",
        "aprendizes.db-wal",
        "aprendizes.db-shm",
    }
    for source_path in source_dir.rglob("*"):
        if source_path.is_dir():
            continue
        if " - Copia" in source_path.name:
            continue
        if "__pycache__" in source_path.parts:
            continue
        if source_path.suffix in {".pyc", ".pyo"}:
            continue
        if source_path.name in ignored_files:
            continue

        target_dir = source_path.parent.relative_to(project_dir)
        datas.append((str(source_path), str(target_dir)))


for package_dir in (
    "assets",
    "data",
    "database",
    "views",
    "controllers",
    "services",
    "models",
    "backups",
    "reports",
):
    add_tree(package_dir)

add_file("config.py", ".")

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
    name="SistemaAprendizes",
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
    name="SistemaAprendizes",
)
