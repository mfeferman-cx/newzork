#!/usr/bin/env python3
"""Run all NewZork regression tests in sequence."""
import subprocess
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
tests = [
    ("CLI regression (43 tests)", ["python3", "regression.py"]),
    ("Engine smoke (26 tests)",   ["python3", "regression_web.py"]),
]

# WebSocket test only runs if the server is up
import urllib.request
try:
    urllib.request.urlopen("http://localhost:8000/health", timeout=1)
    tests.append(("WebSocket protocol (7 tests)", ["python3", "test_ws.py"]))
except Exception:
    print("[skip] WebSocket test: server not running on :8000")

failures = 0
for name, cmd in tests:
    print(f"\n=== {name} ===")
    result = subprocess.run(cmd, cwd=HERE, capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        failures += 1

print()
if failures:
    print(f"--- {failures} suite(s) FAILED ---")
    sys.exit(1)
print("--- ALL SUITES PASS ---")
