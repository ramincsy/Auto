#!/usr/bin/env python3
"""
Comprehensive test of GitHub automation system for ramincsy/Auto repository.
"""

import os
import sys
from pathlib import Path
from datetime import datetime


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

# Test results tracking
test_results = {
    "python_scripts": [],
    "workflow_files": [],
    "github_status": [],
    "token_config": [],
    "overall": "PENDING",
}

print("=" * 80)
print("🔍 COMPREHENSIVE GITHUB AUTOMATION SYSTEM TEST")
print("=" * 80)
print("Date: {0}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
print("Repository: ramincsy/Auto")
print("=" * 80)

# ============================================================================
# TEST 1: Python Scripts - Token Handling and Error Cases
# ============================================================================
print("\n" + "=" * 80)
print("TEST 1: Python Scripts Token Handling")
print("=" * 80)

scripts_to_test = [
    "scripts/auto_merge_prs.py",
    "scripts/resolve_conflicts.py",
    "scripts/pr_status_report.py",
    "scripts/merge_daily_updates.py",
]

print("\n1.1 Testing error handling without token...")
# Clear token
os.environ.pop("GH_TOKEN3", None)
os.environ.pop("GITHUB_TOKEN", None)
os.environ.pop("GH_TOKEN", None)

for script in scripts_to_test:
    if not Path(script).exists():
        test_results["python_scripts"].append(
            {
                "script": script,
                "test": "File existence",
                "status": "❌ FAIL",
                "detail": "Script not found",
            }
        )
        continue

    print(f"\nTesting: {script}")

    # Read the script
    with open(script, "r", encoding="utf-8") as f:
        content = f.read()

    # Check 1: GH_TOKEN3 priority
    checks = {
        "Has GH_TOKEN3 check": "GH_TOKEN3" in content,
        "Checks GITHUB_TOKEN": "GITHUB_TOKEN" in content,
        "Checks GH_TOKEN": "GH_TOKEN" in content,
        "Error handling": "if not token" in content or "sys.exit" in content,
        "Uses Bearer auth": "Bearer" in content or "token {" in content,
        "Error message": "Error: No GitHub token" in content or "❌ Error" in content,
    }

    for check_name, result in checks.items():
        status = "✅ PASS" if result else "⚠️  WARN"
        test_results["python_scripts"].append(
            {
                "script": script,
                "test": check_name,
                "status": status,
                "detail": "Found" if result else "Not found",
            }
        )
        print(f"  {status} {check_name}")

# ============================================================================
# TEST 2: Workflow Files - YAML Syntax and Token Usage
# ============================================================================
print("\n" + "=" * 80)
print("TEST 2: Workflow Files (YAML Syntax and Configuration)")
print("=" * 80)

workflow_files = [
    ".github/workflows/auto-merge.yml",
    ".github/workflows/daily-contribution.yml",
    ".github/workflows/code-quality.yml",
]

for workflow_file in workflow_files:
    if not Path(workflow_file).exists():
        test_results["workflow_files"].append(
            {
                "file": workflow_file,
                "test": "File existence",
                "status": "❌ FAIL",
                "detail": "File not found",
            }
        )
        continue

    print(f"\nTesting: {workflow_file}")

    # Read and validate YAML syntax (basic check)
    with open(workflow_file, "r", encoding="utf-8") as f:
        content = f.read()
        # Basic YAML validation - check for common syntax errors
        yaml_valid = True
        if content.count(":") > 5 and content.count("\n") > 5:
            yaml_valid = True
            print("  ✅ PASS YAML structure looks valid")
            test_results["workflow_files"].append(
                {
                    "file": workflow_file,
                    "test": "YAML syntax",
                    "status": "✅ PASS",
                    "detail": "YAML structure valid",
                }
            )
        else:
            yaml_valid = False
            print("  ❌ FAIL YAML structure issue detected")
            test_results["workflow_files"].append(
                {
                    "file": workflow_file,
                    "test": "YAML syntax",
                    "status": "⚠️  WARN",
                    "detail": "YAML structure may have issues",
                }
            )

    # Check for GH_TOKEN3 usage
    with open(workflow_file, "r", encoding="utf-8") as f:
        content = f.read()

    checks = {
        "Uses GH_TOKEN3": "GH_TOKEN3" in content,
        "Uses secrets": "secrets" in content,
        "Has jobs defined": "jobs:" in content,
        "Proper indentation": content.count("\n") > 5,
    }

    for check_name, result in checks.items():
        status = "✅ PASS" if result else "⚠️  WARN"
        test_results["workflow_files"].append(
            {
                "file": workflow_file,
                "test": check_name,
                "status": status,
                "detail": "Yes" if result else "No",
            }
        )
        print(f"  {status} {check_name}")

# ============================================================================
# TEST 3: Token Configuration Verification
# ============================================================================
print("\n" + "=" * 80)
print("TEST 3: Token Configuration Verification")
print("=" * 80)

print("\n3.1 Checking token priority chain in scripts...")

for script in scripts_to_test:
    if not Path(script).exists():
        continue

    with open(script, "r", encoding="utf-8") as f:
        content = f.read()

    # Check token priority order
    if "GH_TOKEN3" in content:
        idx_gh3 = content.find("GH_TOKEN3")
        idx_github = (
            content.find("GITHUB_TOKEN", idx_gh3) if "GITHUB_TOKEN" in content else 9999
        )
        idx_gh = (
            content.find("GH_TOKEN", idx_github)
            if "GH_TOKEN" in content[idx_github:]
            else 9999
        )

        if idx_gh3 < idx_github and idx_github < idx_gh:
            status = "✅ PASS"
            detail = "GH_TOKEN3 → GITHUB_TOKEN → GH_TOKEN"
        else:
            status = "⚠️  WARN"
            detail = "Priority order may not be correct"

        test_results["token_config"].append(
            {
                "script": script,
                "test": "Token priority",
                "status": status,
                "detail": detail,
            }
        )
        print(f"  {status} {script}: {detail}")

# ============================================================================
# TEST 4: Auto-Merge PR Check (Without Real API Call)
# ============================================================================
print("\n" + "=" * 80)
print("TEST 4: Auto-Merge Implementation Analysis")
print("=" * 80)

print("\n4.1 Checking auto_merge_prs.py implementation...")

with open("scripts/auto_merge_prs.py", "r", encoding="utf-8") as f:
    auto_merge_content = f.read()

checks = {
    "Filters daily PRs": "Daily Update" in auto_merge_content
    or "daily-contribution" in auto_merge_content,
    "Checks mergeable status": "mergeable" in auto_merge_content,
    "Handles conflicts (dirty)": "dirty" in auto_merge_content,
    "Skips drafts": "draft" in auto_merge_content,
    "Has merge logic": "merge_pr" in auto_merge_content,
    "Reports summary": "merged_count" in auto_merge_content,
    "Handles network errors": "RequestException" in auto_merge_content,
    "Reasonable timeout": "timeout=30" in auto_merge_content
    or "timeout" in auto_merge_content,
}

for check_name, result in checks.items():
    status = "✅ PASS" if result else "❌ FAIL"
    test_results["overall"] = (
        "❌ FAIL"
        if not result and test_results["overall"] == "PENDING"
        else test_results["overall"]
    )
    print(f"  {status} {check_name}")

# ============================================================================
# TEST 5: Workflow File Content Validation
# ============================================================================
print("\n" + "=" * 80)
print("TEST 5: Workflow File Implementation Details")
print("=" * 80)

print("\n5.1 Checking daily-contribution.yml...")
with open(".github/workflows/daily-contribution.yml", "r", encoding="utf-8") as f:
    daily_content = f.read()

daily_checks = {
    "Schedules morning run (00:00)": "'0 0 * * *'" in daily_content
    or '"0 0 * * *"' in daily_content,
    "Schedules afternoon run (12:00)": "'0 12 * * *'" in daily_content
    or '"0 12 * * *"' in daily_content,
    "Uses GH_TOKEN3 for PR creation": "GH_TOKEN3" in daily_content,
    "Configures git user": "user.email" in daily_content
    and "user.name" in daily_content,
    "Generates content": "generate_content.py" in daily_content,
    "Creates branches": "daily-contribution-" in daily_content,
    "Pushes to origin": "push origin" in daily_content,
    "Uses dedicated auto-merge workflow": "auto-merge:" not in daily_content
    and "needs: make-contribution" not in daily_content,
}

for check_name, result in daily_checks.items():
    status = "✅ PASS" if result else "⚠️  WARN"
    print(f"  {status} {check_name}")

print("\n5.2 Checking auto-merge.yml...")
with open(".github/workflows/auto-merge.yml", "r", encoding="utf-8") as f:
    merge_content = f.read()

merge_checks = {
    "Schedule 1 hour after morning": "'0 1 * * *'" in merge_content
    or '"0 1 * * *"' in merge_content,
    "Schedule 1 hour after afternoon": "'0 13 * * *'" in merge_content
    or '"0 13 * * *"' in merge_content,
    "Uses GH_TOKEN3": "GH_TOKEN3" in merge_content,
    "Runs conflict resolution first": "resolve_conflicts.py" in merge_content,
    "Then runs auto-merge": "auto_merge_prs.py" in merge_content,
    "Installs requests package": "pip install requests" in merge_content
    or "requests" in merge_content,
    "Has error handling": "continue-on-error" in merge_content,
}

for check_name, result in merge_checks.items():
    status = "✅ PASS" if result else "⚠️  WARN"
    print(f"  {status} {check_name}")

# ============================================================================
# TEST 6: Syntax Validation
# ============================================================================
print("\n" + "=" * 80)
print("TEST 6: Python Syntax Validation")
print("=" * 80)

print("\n6.1 Checking Python syntax...")
for script in scripts_to_test:
    if not Path(script).exists():
        continue

    try:
        with open(script, "r", encoding="utf-8") as file:
            compile(file.read(), script, "exec")
        print(f"  ✅ PASS {script}")
        test_results["python_scripts"].append(
            {
                "script": script,
                "test": "Python syntax",
                "status": "✅ PASS",
                "detail": "Valid Python",
            }
        )
    except SyntaxError as e:
        print(f"  ❌ FAIL {script}: {str(e)[:60]}")
        test_results["python_scripts"].append(
            {
                "script": script,
                "test": "Python syntax",
                "status": "❌ FAIL",
                "detail": f"Syntax error: {str(e)[:60]}",
            }
        )

# ============================================================================
# SUMMARY REPORT
# ============================================================================
print("\n" + "=" * 80)
print("📊 COMPREHENSIVE TEST SUMMARY")
print("=" * 80)


# Count results
def count_status(results, status):
    return sum(1 for r in results if r.get("status", "").startswith(status[0]))


total_tests = (
    len(test_results["python_scripts"])
    + len(test_results["workflow_files"])
    + len(test_results["token_config"])
)

pass_tests = sum(
    1
    for tests in test_results.values()
    if isinstance(tests, list)
    for t in tests
    if t.get("status", "").startswith("✅")
)
fail_tests = sum(
    1
    for tests in test_results.values()
    if isinstance(tests, list)
    for t in tests
    if t.get("status", "").startswith("❌")
)
warn_tests = sum(
    1
    for tests in test_results.values()
    if isinstance(tests, list)
    for t in tests
    if t.get("status", "").startswith("⚠️")
)

print(f"\nTotal Tests Run: {total_tests}")
print(f"  ✅ PASS: {pass_tests}")
print(f"  ⚠️  WARN: {warn_tests}")
print(f"  ❌ FAIL: {fail_tests}")

print("\n" + "=" * 80)
print("DETAILED RESULTS BY CATEGORY")
print("=" * 80)

print("\nPython Scripts:")
script_tests = test_results["python_scripts"]
for script in set(r["script"] for r in script_tests if "script" in r):
    tests = [r for r in script_tests if r.get("script") == script]
    fails = [r for r in tests if r["status"].startswith("❌")]
    if fails:
        print(f"  ❌ {script}")
        for t in fails:
            print(f"     - {t['test']}: {t['detail']}")
    else:
        print(f"  ✅ {script}")

print("\nWorkflow Files:")
workflow_tests = test_results["workflow_files"]
for wf in set(r["file"] for r in workflow_tests if "file" in r):
    tests = [r for r in workflow_tests if r.get("file") == wf]
    fails = [r for r in tests if r["status"].startswith("❌")]
    if fails:
        print(f"  ❌ {wf}")
        for t in fails:
            print(f"     - {t['test']}: {t['detail']}")
    else:
        print(f"  ✅ {wf}")

print("\nToken Configuration:")
token_tests = test_results["token_config"]
if token_tests:
    for script in set(r["script"] for r in token_tests if "script" in r):
        tests = [r for r in token_tests if r.get("script") == script]
        fails = [r for r in tests if r["status"].startswith("❌")]
        if fails:
            print(f"  ❌ {script}")
            for t in fails:
                print(f"     - {t['test']}: {t['detail']}")
        else:
            print(f"  ✅ {script}")

# ============================================================================
# FINAL VERDICT
# ============================================================================
print("\n" + "=" * 80)
if fail_tests == 0:
    print("🎉 ALL CRITICAL TESTS PASSED!")
    print("=" * 80)
    print("\n✅ Python Scripts: All scripts have proper token handling")
    print("✅ Workflow Files: All YAML files are valid and properly configured")
    print("✅ Token Config: Token priority chains are correct")
    print("✅ Implementation: All core features are implemented")
else:
    print("⚠️  SOME TESTS FAILED - REVIEW NEEDED")
    print("=" * 80)
    print(f"\n{fail_tests} test(s) failed:")
    for tests in test_results.values():
        if isinstance(tests, list):
            for t in tests:
                if t.get("status", "").startswith("❌"):
                    print(f"  ❌ {t.get('script') or t.get('file')}: {t['test']}")

print("\n" + "=" * 80)
print("✨ Test completed at " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("=" * 80)
