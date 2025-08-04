#!/usr/bin/env python3
"""
Build script for creating cross-platform executables.
Uses PyInstaller to create standalone executables.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(command):
    """Run a shell command and check for errors."""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    return result.stdout


def build_executable():
    """Build the executable using PyInstaller."""
    # Ensure we're in the right directory
    os.chdir(Path(__file__).parent)
    
    # Install dependencies
    print("Installing dependencies...")
    run_command("uv sync")
    run_command("uv add --group build pyinstaller")
    
    # Clean previous builds
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    
    # Build the executable
    print("Building executable...")
    pyinstaller_command = [
        "uv", "run", "pyinstaller",
        "--onefile",
        "--name=seven-day-roguelike",
        "--add-data=src:src",
        "src/main.py"
    ]
    
    run_command(" ".join(pyinstaller_command))
    
    print("Build complete! Executable is in the 'dist' folder.")


if __name__ == "__main__":
    build_executable()