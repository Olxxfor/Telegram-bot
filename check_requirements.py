#!/usr/bin/env python3
"""
Check if all required dependencies are installed
"""

import sys
import importlib

required_packages = [
    'telegram',
    'PIL',
    'PyPDF2', 
    'docx',
    'reportlab',
    'rarfile'
]

optional_packages = [
    'ffmpeg'
]

def check_package(package_name):
    try:
        importlib.import_module(package_name)
        return True
    except ImportError:
        return False

print("Checking required packages...")
all_good = True

for package in required_packages:
    if check_package(package):
        print(f"✅ {package}")
    else:
        print(f"❌ {package} - NOT FOUND")
        all_good = False

print("\nChecking optional packages...")
for package in optional_packages:
    if check_package(package):
        print(f"✅ {package}")
    else:
        print(f"⚠️  {package} - NOT FOUND (optional)")

if all_good:
    print("\n🎉 All required packages are installed!")
    sys.exit(0)
else:
    print("\n❌ Some required packages are missing!")
    sys.exit(1)
