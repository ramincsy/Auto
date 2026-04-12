#!/usr/bin/env python3
"""
Validation Script - Verify Auto-Merge System Installation

This script verifies that all components of the auto-merge system are
properly installed and configured.

Usage:
    python scripts/validate_installation.py

Returns:
    0 = All checks passed ✅
    1 = Some checks failed ⚠️
    2 = Critical checks failed ❌
"""

import os
import sys
import subprocess
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


def check_file_exists(filepath: str, description: str) -> bool:
    """Check if a file exists."""
    if Path(filepath).exists():
        print(f"  ✅ {description}: {filepath}")
        return True
    else:
        print(f"  ❌ {description}: {filepath} (NOT FOUND)")
        return False


def check_python_module(module: str) -> bool:
    """Check if a Python module is installed."""
    try:
        __import__(module)
        print(f"  ✅ Python module '{module}' is installed")
        return True
    except ImportError:
        print(f"  ❌ Python module '{module}' is NOT installed")
        print(f"     Install with: pip install {module}")
        return False


def check_env_var(var: str, description: str) -> bool:
    """Check if an environment variable is set."""
    if os.environ.get(var):
        print(f"  ✅ Environment variable '{var}' is set")
        return True
    else:
        print(f"  ⚠️  Environment variable '{var}' is NOT set (optional)")
        return False


def validate_python_syntax(filepath: str) -> bool:
    """Validate Python file syntax."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            compile(f.read(), filepath, 'exec')
        print(f"  ✅ {Path(filepath).name}: Valid Python syntax")
        return True
    except SyntaxError as e:
        print(f"  ❌ {Path(filepath).name}: Syntax error at line {e.lineno}: {e.msg}")
        return False
    except Exception as e:
        print(f"  ❌ {Path(filepath).name}: Error: {e}")
        return False


def main():
    """Main validation function."""
    print("\n" + "="*80)
    print("  🔍 AUTO-MERGE SYSTEM VALIDATION")
    print("="*80 + "\n")
    
    passed = 0
    failed = 0
    warnings = 0
    
    # Get base directory
    base_dir = Path(__file__).parent.parent
    
    # 1. Check Python Version
    print("1️⃣  PYTHON VERSION")
    print("-" * 80)
    py_version = sys.version_info
    if py_version.major >= 3 and py_version.minor >= 7:
        print(f"  ✅ Python {py_version.major}.{py_version.minor}.{py_version.micro}")
        passed += 1
    else:
        print(f"  ❌ Python {py_version.major}.{py_version.minor}.{py_version.micro} (requires 3.7+)")
        failed += 1
    print()
    
    # 2. Check Required Modules
    print("2️⃣  PYTHON MODULES")
    print("-" * 80)
    modules_ok = True
    for module in ['requests', 'json', 'os', 'sys']:
        if not check_python_module(module):
            if module != 'requests':  # requests is critical
                warnings += 1
            else:
                failed += 1
                modules_ok = False
        else:
            passed += 1
    print()
    
    # 3. Check Required Scripts
    print("3️⃣  REQUIRED SCRIPTS")
    print("-" * 80)
    scripts = [
        ('scripts/auto_merge_prs.py', 'Auto-merge script (main)'),
        ('scripts/resolve_conflicts.py', 'Conflict resolution script'),
        ('scripts/pr_status_report.py', 'Status report script'),
    ]
    for script, desc in scripts:
        filepath = base_dir / script
        if check_file_exists(str(filepath), desc):
            if validate_python_syntax(str(filepath)):
                passed += 1
            else:
                failed += 1
        else:
            failed += 1
    print()
    
    # 4. Check Documentation
    print("4️⃣  DOCUMENTATION")
    print("-" * 80)
    docs = [
        ('docs/guides/CONFLICT_RESOLUTION_GUIDE.md', 'Complete conflict resolution guide'),
        ('docs/guides/MERGE_QUICK_REFERENCE.md', 'Quick reference card'),
        ('docs/guides/GETTING_STARTED.md', 'Getting started guide'),
        ('docs/archive/IMPLEMENTATION_SUMMARY.md', 'Implementation details'),
    ]
    for doc, desc in docs:
        filepath = base_dir / doc
        if check_file_exists(str(filepath), desc):
            passed += 1
        else:
            warnings += 1
    print()
    
    # 5. Check Workflow
    print("5️⃣  GITHUB ACTIONS WORKFLOW")
    print("-" * 80)
    workflow_file = base_dir / '.github/workflows/auto-merge.yml'
    if check_file_exists(str(workflow_file), 'Auto-merge workflow'):
        passed += 1
    else:
        warnings += 1
    print()
    
    # 6. Check Environment
    print("6️⃣  ENVIRONMENT CONFIGURATION")
    print("-" * 80)
    if check_env_var('GITHUB_TOKEN', 'GitHub token'):
        passed += 1
    else:
        warnings += 1
    
    if not os.environ.get('GITHUB_TOKEN') and not os.environ.get('GH_TOKEN'):
        print("  💡 Set token for local testing:")
        print("     export GITHUB_TOKEN='your_token_here'")
    print()
    
    # Summary
    print("="*80)
    print("  📊 VALIDATION SUMMARY")
    print("="*80)
    print(f"  ✅ Passed: {passed}")
    print(f"  ⚠️  Warnings: {warnings}")
    print(f"  ❌ Failed: {failed}")
    print()
    
    if failed == 0 and warnings == 0:
        print("  🎉 ALL CHECKS PASSED! System is ready to use.")
        print()
        print("  Next steps:")
        print("    1. Set GITHUB_TOKEN environment variable")
        print("    2. Run: python scripts/pr_status_report.py")
        print("    3. Run: python scripts/resolve_conflicts.py --auto-resolve")
        print("    4. Run: python scripts/auto_merge_prs.py")
        print()
        return 0
    
    elif failed == 0:
        print("  ✅ SYSTEM IS FUNCTIONAL (with warnings)")
        print()
        print("  Warnings:")
        if warnings > 0:
            print("    - Some optional components are missing")
            print("    - GITHUB_TOKEN environment variable not set")
        print()
        return 0
    
    else:
        print("  ❌ SYSTEM HAS CRITICAL ISSUES")
        print()
        print("  Actions required:")
        print("    1. Install missing Python modules: pip install requests")
        print("    2. Ensure all script files are in place")
        print("    3. Check script file permissions")
        print()
        return 2


if __name__ == "__main__":
    sys.exit(main())
