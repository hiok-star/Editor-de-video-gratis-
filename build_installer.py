#!/usr/bin/env python3
"""
Build script for Video Editor Windows Installer
Creates standalone executable with PyInstaller and packages with NSIS
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
DIST_DIR = PROJECT_DIR / "dist"
BUILD_DIR = PROJECT_DIR / "build"
INSTALLER_DIR = PROJECT_DIR / "installer"

def run_cmd(cmd, cwd=None, check=True):
    """Run command and print output"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}")
    return result

def clean_dirs():
    """Clean previous build directories"""
    for d in [DIST_DIR, BUILD_DIR]:
        if d.exists():
            print(f"Cleaning {d}")
            shutil.rmtree(d)
    if INSTALLER_DIR.exists():
        # Keep NSIS script but clean output
        for f in INSTALLER_DIR.glob("*.exe"):
            f.unlink()

def build_executable():
    """Build standalone executable with PyInstaller"""
    print("Building executable with PyInstaller...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--name=video_editor",
        "--onefile",
        "--windowed",
        "--icon=resources/icon.ico" if (PROJECT_DIR / "resources" / "icon.ico").exists() else "",
        "--add-data=core;core",
        "--add-data=render;render",
        "--add-data=ui;ui",
        "--add-data=plugins;plugins",
        "--add-data=resources;resources",
        "--hidden-import=PySide6",
        "--hidden-import=PySide6.QtCore",
        "--hidden-import=PySide6.QtGui",
        "--hidden-import=PySide6.QtWidgets",
        "--hidden-import=av",
        "--hidden-import=numpy",
        "--hidden-import=cv2",
        "--collect-all=PySide6",
        "--collect-all=av",
        "main.py"
    ]
    
    # Filter empty strings
    cmd = [c for c in cmd if c]
    
    run_cmd(" ".join(cmd), cwd=PROJECT_DIR)

def create_license():
    """Create license file for installer"""
    license_text = """Video Editor - MIT License

Copyright (c) 2024 Video Editor Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    (INSTALLER_DIR / "LICENSE.txt").write_text(license_text)

def build_installer():
    """Build NSIS installer"""
    print("Building NSIS installer...")
    
    # Check if NSIS is available
    nsis_path = r"C:\Program Files (x86)\NSIS\makensis.exe"
    if not Path(nsis_path).exists():
        nsis_path = r"C:\Program Files\NSIS\makensis.exe"
    
    if not Path(nsis_path).exists():
        print("NSIS not found. Installing via winget...")
        run_cmd("winget install NSIS.NSIS", check=False)
    
    # Copy executable to installer input directory
    exe_src = DIST_DIR / "video_editor.exe"
    if not exe_src.exists():
        raise FileNotFoundError(f"Executable not found: {exe_src}")
    
    installer_input = INSTALLER_DIR / "dist" / "video_editor"
    installer_input.mkdir(parents=True, exist_ok=True)
    shutil.copy2(exe_src, installer_input / "video_editor.exe")
    
    # Create license
    create_license()
    
    # Run NSIS
    nsi_script = INSTALLER_DIR / "video_editor_installer.nsi"
    if Path(nsis_path).exists():
        run_cmd(f'"{nsis_path}" "{nsi_script}"', cwd=INSTALLER_DIR)
        print(f"Installer created: {INSTALLER_DIR / 'VideoEditor-Setup-1.0.0.exe'}")
    else:
        print("NSIS not available. Creating portable zip instead...")
        create_portable_zip()

def create_portable_zip():
    """Create portable zip as alternative"""
    import zipfile
    
    zip_path = INSTALLER_DIR / "VideoEditor-Portable.zip"
    exe_src = DIST_DIR / "video_editor.exe"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(exe_src, "video_editor.exe")
        # Add README
        zf.write(PROJECT_DIR / "README.md", "README.md")
    
    print(f"Portable zip created: {zip_path}")

def main():
    print("=" * 60)
    print("Video Editor - Windows Installer Builder")
    print("=" * 60)
    
    try:
        clean_dirs()
        build_executable()
        build_installer()
        print("\n" + "=" * 60)
        print("BUILD COMPLETE!")
        print("=" * 60)
        print(f"Executable: {DIST_DIR / 'video_editor.exe'}")
        print(f"Installer: {INSTALLER_DIR / 'VideoEditor-Setup-1.0.0.exe'}")
        print(f"Portable: {INSTALLER_DIR / 'VideoEditor-Portable.zip'}")
    except Exception as e:
        print(f"\nBUILD FAILED: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()