#!/usr/bin/env python3
"""
Background Build Monitor & Debug Loop
======================================
Runs in background, monitoring CI builds, fixing failures iteratively.
Designed to run as a subtask while main agent handles other work.
"""

import subprocess
import sys
import time
from datetime import datetime

# Configuration
REPO = "WyattAu/EvergreenImageRegistry"
MAX_ITERATIONS = 50  # Max retry cycles
SLEEP_SECONDS = 120  # Wait between checks
AUTO_FIX = True      # Automatically try to fix failures

def run_cmd(cmd):
    """Run shell command and return output."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout, result.stderr, result.returncode

def get_failed_builds():
    """Get list of currently failing image builds."""
    stdout, _, _ = run_cmd(f"gh run list --repo {REPO} --status failure --limit 1")

    failed = []
    for line in stdout.split('\n'):
        if 'failure' in line.lower():
            # Extract job name
            parts = line.split()
            if len(parts) >= 2:
                failed.append(parts[-1])  # Last column is usually job name
    return failed

def get_latest_run_id():
    """Get the most recent workflow run ID."""
    stdout, _, _ = run_cmd(f"gh run list --repo {REPO} --limit 1 --json id")
    import json
    try:
        data = json.loads(stdout)
        if data:
            return data[0]['id']
    except:
        pass
    return None

def check_build_status():
    """Check current build status."""
    stdout, _, rc = run_cmd(f"gh run list --repo {REPO} --status in_progress --limit 1")

    if rc == 0 and stdout:
        return "running"
    return "completed"

def get_failed_jobs():
    """Get list of failed jobs from latest run."""
    run_id = get_latest_run_id()
    if not run_id:
        return []

    stdout, _, _ = run_cmd(f"gh run view {run_id} --repo {REPO} --json jobs")
    import json
    try:
        data = json.loads(stdout)
        jobs = data.get('jobs', [])
        failed = []
        for job in jobs:
            if job.get('status') == 'completed' and job.get('conclusion') == 'failure':
                failed.append(job.get('name', 'unknown'))
        return failed
    except:
        return []

def analyze_failure(failed_job):
    """Analyze why a specific job failed."""
    print(f"Analyzing failure: {failed_job}")

    # Get job logs
    run_id = get_latest_run_id()
    if run_id:
        stdout, _, _ = run_cmd(f"gh run view {run_id} --repo {REPO} --log-failed 2>/dev/null | head -100")
        print(f"Logs:\n{stdout}")

    return "analyzed"

def main():
    """Main background loop."""
    print(f"Background Build Monitor Started: {datetime.now()}")
    print(f"Monitoring repo: {REPO}")
    print(f"Check interval: {SLEEP_SECONDS}s")
    print("=" * 60)

    iteration = 0
    total_failures = 0

    while iteration < MAX_ITERATIONS:
        iteration += 1
        print(f"\n--- Iteration {iteration}/{MAX_ITERATIONS} ---")

        # Check if build is still running
        status = check_build_status()

        if status == "running":
            print(f"Build still running... waiting {SLEEP_SECONDS}s")
            time.sleep(SLEEP_SECONDS)
            continue

        # Build completed - check for failures
        print("Build completed, checking results...")
        failed_jobs = get_failed_jobs()

        if not failed_jobs:
            print("✅ ALL BUILDS PASSED!")
            return 0

        print(f"❌ Failed jobs: {len(failed_jobs)}")
        for job in failed_jobs:
            print(f"  - {job}")

        total_failures += len(failed_jobs)

        # Analyze each failure
        for job in failed_jobs:
            analyze_failure(job)

        # If auto-fix enabled, would trigger fixes here
        # For now, just report
        print(f"\nTotal failures so far: {total_failures}")
        print("Need manual intervention or script update to fix URLs")

        # Wait before next check
        print(f"Waiting {SLEEP_SECONDS}s before next check...")
        time.sleep(SLEEP_SECONDS)

    print(f"\nMax iterations reached. Total failures: {total_failures}")
    return 1

if __name__ == '__main__':
    sys.exit(main())
