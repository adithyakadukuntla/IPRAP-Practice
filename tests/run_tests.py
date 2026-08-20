#!/usr/bin/env python3
"""
Test Execution Runner
Executes all test suites and generates comprehensive reports
"""
import subprocess
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Test suite definitions
TEST_SUITES = {
    "API": {
        "path": "tests/automation/api",
        "tests": [
            "test_api_health.py",
            "test_api_contract.py",
            "test_api_holdings.py",
            "test_api_risk.py",
            "test_api_performance.py",
            "test_api_allocation.py",
            "test_api_dashboard.py",
            "test_negative_scenarios.py",
            "test_security.py",
            "test_performance.py"
        ]
    },
    "DATA": {
        "path": "tests/automation/data",
        "tests": [
            "test_data_reconciliation.py",
            "test_data_quality.py"
        ]
    }
}

def run_test_suite(suite_name, suite_config):
    """Run a single test suite"""
    print(f"\n{'='*60}")
    print(f"Running {suite_name} Test Suite")
    print(f"{'='*60}\n")
    
    test_dir = suite_config["path"]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = f"tests/reports/{suite_name}_{timestamp}"
    
    os.makedirs(report_dir, exist_ok=True)
    
    cmd = [
        "pytest",
        test_dir,
        "--verbose",
        f"--html={report_dir}/report.html",
        "--self-contained-html",
        f"--cov=tests",
        f"--cov-report=html:{report_dir}/coverage",
        f"--junit-xml={report_dir}/junit.xml",
        "-v"
    ]
    
    result = subprocess.run(cmd, cwd=".")
    return result.returncode == 0

def run_all_tests():
    """Run all test suites"""
    print("\n" + "="*60)
    print("IPRAP Test Execution Suite")
    print("="*60)
    print(f"Start Time: {datetime.now()}\n")
    
    results = {}
    total_passed = 0
    total_failed = 0
    
    for suite_name, suite_config in TEST_SUITES.items():
        success = run_test_suite(suite_name, suite_config)
        results[suite_name] = "PASSED" if success else "FAILED"
        
        if success:
            total_passed += 1
        else:
            total_failed += 1
    
    # Summary
    print("\n" + "="*60)
    print("TEST EXECUTION SUMMARY")
    print("="*60)
    for suite_name, status in results.items():
        status_symbol = "✓" if status == "PASSED" else "✗"
        print(f"{status_symbol} {suite_name}: {status}")
    
    print(f"\nTotal: {total_passed} passed, {total_failed} failed")
    print(f"End Time: {datetime.now()}\n")
    
    return total_failed == 0

def run_specific_test(test_file):
    """Run a specific test file"""
    print(f"Running specific test: {test_file}\n")
    
    cmd = ["pytest", test_file, "-v", "--tb=short"]
    result = subprocess.run(cmd, cwd=".")
    return result.returncode == 0

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run specific test
        test_file = sys.argv[1]
        success = run_specific_test(test_file)
    else:
        # Run all tests
        success = run_all_tests()
    
    sys.exit(0 if success else 1)
