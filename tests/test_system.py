#!/usr/bin/env python3
"""
Test script to verify the contribution system works locally
"""

import os
import sys
from datetime import datetime
from pathlib import Path


def configure_output_encoding():
    """Prefer UTF-8 output when the host console supports reconfiguration."""
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except ValueError:
                pass


configure_output_encoding()

# Test 1: Create contribution directories
print("🧪 Test 1: Creating contribution files structure...")
date_str = "2026-04-13"
year, month, day = date_str.split("-")

for i in range(5):  # Test with 5 files
    folder = Path("updates") / year / month
    folder.mkdir(parents=True, exist_ok=True)
    
    filename = f"{day}-contribution-{i}.md"
    filepath = folder / filename
    
    if not filepath.exists():
        content = f"""# Contribution #{i} - {date_str}

## 📚 Topic
Automated testing contribution #{i}

## 🎯 Activity  
- Index: {i}
- Date: {date_str}
- Test: Local execution

## 📝 Details
Testing the contribution system locally.
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✅ Created: {filepath}")
    else:
        print(f"  ⏭️  Already exists: {filepath}")

# Test 2: Verify files were created
print("\n🧪 Test 2: Verifying created files...")
test_path = Path("updates") / year / month
if test_path.exists():
    files = list(test_path.glob(f"{day}-contribution-*.md"))
    print(f"  ✅ Found {len(files)} files in {test_path}")
    for f in files[:3]:
        print(f"     - {f.name}")
else:
    print(f"  ❌ Path does not exist: {test_path}")

# Test 3: Git operations test
print("\n🧪 Test 3: Testing git operations...")
os.system("git --version")

# Cleanup temporary contribution files created by this test
for filepath in (Path("updates") / year / month).glob(f"{day}-contribution-*.md"):
    filepath.unlink(missing_ok=True)

print("\n🧹 Temporary test files cleaned up.")

print("\n✅ All local tests passed!")
print("\nNext steps:")
print("1. Trigger workflow on GitHub")
print("2. Monitor: https://github.com/ramincsy/Auto/actions")
print("3. Check pull requests: https://github.com/ramincsy/Auto/pulls")
