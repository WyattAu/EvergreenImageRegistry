# =============================================================================

# PHASE 6: CONTINUOUS MONITORING & IMPROVEMENT - Detailed Execution Plan

# =============================================================================

# Version: 1.0.0

# Status: PENDING

# Date: 2026-04-20

#

# ABSTRACT: This phase establishes continuous monitoring, automated alerting,

# and improvement loops for the Evergreen Image Registry. Daily CVE rescans,

# SBOM drift detection, compliance score tracking, base image freshness

# monitoring, supply chain monitoring, and metrics dashboards ensure the

# registry remains hardened over time. Phase 5 must pass all quality gates

# before this phase begins.

# =============================================================================

## Table of Contents

1. [Task Inventory](#1-task-inventory)
2. [6.1 Daily CVE Rescan Pipeline](#2-61-daily-cve-rescan-pipeline)
3. [6.2 SBOM Drift Detection](#3-62-sbom-drift-detection)
4. [6.3 Compliance Score Tracking](#4-63-compliance-score-tracking)
5. [6.4 Base Image Freshness Monitoring](#5-64-base-image-freshness-monitoring)
6. [6.5 Supply Chain Monitoring](#6-65-supply-chain-monitoring)
7. [6.6 Metrics Dashboard](#7-66-metrics-dashboard)
8. [Quality Gates](#8-quality-gates)
9. [Dependencies](#9-dependencies)
10. [Risk Assessment](#10-risk-assessment)
11. [Timeline](#11-timeline)

---

## 1. Task Inventory

### Dependency Graph

```
Phase 5 (all gates passed)
    |
    +--> T6.1.1 (daily CVE rescan workflow) ──> Independent
    +--> T6.1.2 (CVE baseline + comparison logic) ──> Depends on T6.1.1
    +--> T6.1.3 (auto-issue creation for new CVEs) ──> Depends on T6.1.2
    +--> T6.1.4 (conditional rebuild trigger) ──> Depends on T6.1.2
    +--> T6.1.5 (CVE history tracking) ──> Depends on T6.1.2
    |
    +--> T6.2.1 (weekly SBOM generation) ──> Independent
    +--> T6.2.2 (SBOM diff / drift detection) ──> Depends on T6.2.1
    +--> T6.2.3 (drift alerting) ──> Depends on T6.2.2
    |
    +--> T6.3.1 (CIS benchmark weekly run) ──> Independent
    +--> T6.3.2 (STIG weekly run) ──> Independent
    +--> T6.3.3 (score tracking CSV) ──> Depends on T6.3.1, T6.3.2
    +--> T6.3.4 (regression alerting) ──> Depends on T6.3.3
    |
    +--> T6.4.1 (base image freshness check) ──> Independent
    +--> T6.4.2 (>30 day stale alerting) ──> Depends on T6.4.1
    +--> T6.4.3 (auto-PR for base image updates) ──> Depends on T6.4.1
    |
    +--> T6.5.1 (dependency URL health check) ──> Independent
    +--> T6.5.2 (checksum change detection) ──> Depends on T6.5.1
    +--> T6.5.3 (URL breakage alerting) ──> Depends on T6.5.1, T6.5.2
    |
    +--> T6.6.1 (weekly metrics aggregation) ──> Depends on T6.1.5, T6.3.3
    +--> T6.6.2 (markdown report generation) ──> Depends on T6.6.1
    +--> T6.6.3 (trend tracking) ──> Depends on T6.6.1
```

### Parallel Execution Streams

```
Stream A: CVE Scanning (T6.1.1 -> T6.1.2 -> T6.1.3, T6.1.4, T6.1.5) ── 24 hours
Stream B: SBOM Drift  (T6.2.1 -> T6.2.2 -> T6.2.3) ── 12 hours
Stream C: Compliance  (T6.3.1, T6.3.2 -> T6.3.3 -> T6.3.4) ── 16 hours
Stream D: Base Images (T6.4.1 -> T6.4.2, T6.4.3) ── 12 hours
Stream E: Supply Chain (T6.5.1 -> T6.5.2 -> T6.5.3) ── 8 hours
Stream F: Dashboard   (T6.6.1 -> T6.6.2, T6.6.3) ── 12 hours (starts after A, C)
```

| Stream    | Wall-Clock    | Dependencies                           |
| --------- | ------------- | -------------------------------------- |
| A         | 24 hours      | None                                   |
| B         | 12 hours      | None                                   |
| C         | 16 hours      | None                                   |
| D         | 12 hours      | None                                   |
| E         | 8 hours       | None                                   |
| F         | 12 hours      | A (CVE history), C (compliance scores) |
| **Total** | **~36 hours** |                                        |

---

## 2. 6.1 Daily CVE Rescan Pipeline

### T6.1.1: Daily CVE Rescan Workflow

**Problem:** CVEs are discovered continuously. Images built weeks ago may have newly disclosed vulnerabilities that are
not yet addressed.

**Solution:** Scheduled GitHub Actions workflow running at 06:00 UTC daily to rescan all 223 images with Trivy and
Grype.

**Files to create:**

| File                                        | Purpose                                     |
| ------------------------------------------- | ------------------------------------------- |
| `.github/workflows/daily-security-scan.yml` | Scheduled CI workflow (cron 06:00 UTC)      |
| `scripts/scan_all_images.sh`                | Orchestrator script for scanning all images |
| `scripts/compare_cve_baseline.py`           | Compare current scan against known baseline |

**Implementation:**

1. GitHub Actions workflow triggered by `schedule` (cron `0 6 * * *`) and `workflow_dispatch`
2. Checkout with `fetch-depth: 0` for full history
3. Set up Docker Buildx
4. Discover all images using the same batched pattern as `build.yml` (50 images/batch)
5. Pull images from GHCR (or build locally if not in registry)
6. Run Trivy scan (JSON output, all severities)
7. Run Grype scan (JSON output, all severities)
8. Upload scan results as GitHub Actions artifacts (30-day retention)

### T6.1.2: CVE Baseline and Comparison

**Problem:** Need to distinguish new CVEs from previously known ones to avoid alert fatigue.

**Solution:** Maintain a baseline of known CVEs and compare each scan against it.

**Files to create:**

| File                                  | Purpose                                   |
| ------------------------------------- | ----------------------------------------- |
| `.reports/cve_baseline/`              | Directory for baseline CVE data per image |
| `.reports/cve_baseline/baseline.json` | Aggregated known CVE baseline             |
| `scripts/update_cve_baseline.py`      | Update baseline after acknowledged CVEs   |

**Baseline format:**

```json
{
  "generated": "2026-04-20T06:00:00Z",
  "images": {
    "nginx": {
      "critical": ["CVE-2024-XXXX"],
      "high": ["CVE-2024-YYYY"],
      "medium": [],
      "low": []
    }
  }
}
```

**Comparison logic:**

- If a CVE exists in current scan but NOT in baseline: flag as **NEW**
- If a CVE exists in baseline but NOT in current scan: flag as **RESOLVED**
- CRITICAL/HIGH new CVEs trigger immediate alerting
- MEDIUM/LOW new CVEs are logged and included in weekly report

### T6.1.3: Auto-Issue Creation for New CVEs

**Problem:** Security teams need immediate notification of new vulnerabilities.

**Solution:** Automatically create GitHub Issues when new CVEs are detected.

**Files to create:**

| File                                  | Purpose                                  |
| ------------------------------------- | ---------------------------------------- |
| `scripts/create_cve_issue.py`         | Create GitHub Issue via API for new CVEs |
| `.github/ISSUE_TEMPLATE/cve-alert.md` | Template for auto-generated CVE issues   |

**Issue format:**

```
Title: [CVE-ALERT] CRITICAL: CVE-2024-XXXX in <image>

Body:
- Image: <image-name>
- CVE ID: CVE-2024-XXXX
- Severity: CRITICAL
- Package: <pkg-name> <pkg-version>
- Description: <cve description>
- Scan date: <date>
- Action required: Rebuild with patched base image
```

### T6.1.4: Conditional Rebuild Trigger

**Problem:** CRITICAL and HIGH CVEs require immediate remediation.

**Solution:** Automatically trigger the build workflow when CRITICAL or HIGH CVEs are detected.

**Implementation:**

1. After scan completion, check for CRITICAL/HIGH new CVEs
2. If found, trigger `build.yml` via `workflow_dispatch` with `repository_dispatch` event
3. Pass affected image list as payload
4. Track triggered rebuilds in `.reports/cve_history/rebuilds.log`

### T6.1.5: CVE History Tracking

**Problem:** Need historical trend data for compliance reporting and audit trails.

**Solution:** Store daily scan results with timestamps for historical analysis.

**Files to create:**

| File                                   | Purpose                              |
| -------------------------------------- | ------------------------------------ |
| `.reports/cve_history/`                | Directory for daily CVE scan history |
| `.reports/cve_history/YYYY-MM-DD.json` | Daily scan results per image         |
| `scripts/archive_cve_scan.py`          | Archive scan results with date stamp |

---

## 3. 6.2 SBOM Drift Detection

### T6.2.1: Weekly SBOM Generation

**Problem:** Dependencies can change between builds without explicit notification.

**Solution:** Generate SBOMs for all built images weekly and compare against previous week.

**Files to create:**

| File                                      | Purpose                                       |
| ----------------------------------------- | --------------------------------------------- |
| `.github/workflows/weekly-sbom-check.yml` | Weekly SBOM generation workflow               |
| `.reports/sbom_history/`                  | Directory for weekly SBOM archives            |
| `.reports/sbom_history/YYYY-WXX/`         | Per-week SBOM directory                       |
| `scripts/generate_all_sboms.sh`           | Generate SPDX SBOMs for all images using Syft |

**Implementation:**

1. Pull all images from registry
2. Generate SPDX JSON SBOMs using `syft`
3. Store in date-stamped directory
4. Retain 52 weeks of history (1 year rolling)

### T6.2.2: SBOM Diff / Drift Detection

**Problem:** New packages or version changes in base images can introduce unexpected dependencies.

**Solution:** Compare current week's SBOMs against previous week and report differences.

**Files to create:**

| File                           | Purpose                                       |
| ------------------------------ | --------------------------------------------- |
| `scripts/diff_sboms.py`        | Compare two SBOM directories and report drift |
| `scripts/sbom_drift_report.sh` | Generate human-readable drift report          |

**Drift detection categories:**

| Category          | Description                             | Severity |
| ----------------- | --------------------------------------- | -------- |
| New package added | Package in current SBOM not in previous | MEDIUM   |
| Package removed   | Package in previous SBOM not in current | LOW      |
| Version bump      | Same package, different version         | LOW      |
| New vulnerability | Package version has known CVE           | HIGH     |
| License change    | Package license changed                 | HIGH     |

### T6.2.3: Drift Alerting

**Solution:** Create GitHub Issue on HIGH severity drift (new vulnerabilities, license changes).

---

## 4. 6.3 Compliance Score Tracking

### T6.3.1: CIS Docker Benchmark Weekly Run

**Problem:** Compliance scores can regress as images are updated or rebuilt.

**Solution:** Run CIS Docker Benchmark against all images weekly and track scores.

**Files to create:**

| File                                      | Purpose                         |
| ----------------------------------------- | ------------------------------- |
| `.github/workflows/weekly-compliance.yml` | Weekly compliance workflow      |
| `scripts/run_weekly_cis.sh`               | Run CIS benchmark on all images |
| `.reports/compliance_tracking/cis/`       | CIS benchmark result history    |

### T6.3.2: STIG Weekly Run

**Solution:** Run DISA STIG checks weekly and track pass/fail rates.

**Files to create:**

| File                                 | Purpose                       |
| ------------------------------------ | ----------------------------- |
| `scripts/run_weekly_stig.sh`         | Run STIG checks on all images |
| `.reports/compliance_tracking/stig/` | STIG check result history     |

### T6.3.3: Score Tracking CSV

**Problem:** Need longitudinal data for compliance audits and trend analysis.

**Solution:** Maintain a CSV file tracking all compliance scores over time.

**Files to create:**

| File                                      | Purpose                           |
| ----------------------------------------- | --------------------------------- |
| `.reports/compliance_tracking/scores.csv` | Time-series compliance scores     |
| `scripts/update_scores_csv.py`            | Append new scores to tracking CSV |

**CSV format:**

```csv
date,image,cis_score,cis_total,cis_pass,stig_score,stig_total,stig_pass
2026-04-20,nginx,92,50,46,88,13,11
2026-04-20,redis,95,50,47,100,13,13
```

### T6.3.4: Regression Alerting

**Solution:** Alert when compliance score drops below previous week's score.

**Thresholds:**

| Metric      | Alert Condition | Action                |
| ----------- | --------------- | --------------------- |
| CIS score   | Drop >= 5%      | Create GitHub Issue   |
| CIS score   | Drop >= 10%     | Block image promotion |
| STIG checks | New failure     | Create GitHub Issue   |
| STIG checks | >3 new failures | Block image promotion |

---

## 5. 6.4 Base Image Freshness Monitoring

### T6.4.1: Base Image Freshness Check

**Problem:** Base images receive security updates regularly. Stale base images accumulate unpatched CVEs.

**Solution:** Check for new versions of all base images daily.

**Files to create:**

| File                                                 | Purpose                                    |
| ---------------------------------------------------- | ------------------------------------------ |
| `scripts/check_base_image_freshness.sh`              | Check upstream for new base image versions |
| `.reports/base_image_tracking/`                      | Base image version tracking data           |
| `.reports/base_image_tracking/registry_sources.yaml` | Map of base image -> upstream registry     |

**Base images to monitor:**

| Base Image                      | Registry                     | Check Method         |
| ------------------------------- | ---------------------------- | -------------------- |
| `debian:bookworm-slim`          | `docker.io/library/debian`   | Docker Hub API       |
| `gcr.io/distroless/static`      | `gcr.io`                     | GCR tags API         |
| `cgr.dev/chainguard/wolfi-base` | `cgr.dev`                    | Chainguard API       |
| `redhat/ubi9-minimal`           | `registry.access.redhat.com` | Red Hat API          |
| `scratch`                       | N/A                          | Skip (no base image) |

**Note:** `FROM scratch` images are excluded from freshness checks.

### T6.4.2: Stale Image Alerting

**Solution:** Alert when base images are >30 days old.

**Files to create:**

| File                                 | Purpose                                         |
| ------------------------------------ | ----------------------------------------------- |
| `scripts/check_base_image_age.sh`    | Check published date of current base image tags |
| `scripts/alert_stale_base_images.py` | Create GitHub Issue for stale base images       |

### T6.4.3: Auto-PR for Base Image Updates

**Problem:** Manual base image updates are time-consuming and error-prone for 223 images.

**Solution:** Automatically create pull requests updating base image references.

**Files to create:**

| File                                          | Purpose                                  |
| --------------------------------------------- | ---------------------------------------- |
| `scripts/update_base_images.sh`               | Update FROM lines in Dockerfiles         |
| `scripts/create_base_image_pr.py`             | Create GitHub PR with base image updates |
| `.github/ISSUE_TEMPLATE/base-image-update.md` | Template for base image update PRs       |

**Implementation:**

1. Detect new base image version via registry API
2. Update `FROM` lines in all Dockerfiles referencing that base image
3. Run lint (hadolint) on updated Dockerfiles
4. Trigger test build for affected images
5. If tests pass, create PR with updated Dockerfiles
6. Include SBOM diff and CVE scan results in PR description

---

## 6. 6.5 Supply Chain Monitoring

### T6.5.1: Dependency URL Health Check

**Problem:** Download URLs for binaries can break (HTTP 404, domain changes, etc.) without warning.

**Solution:** Monitor all dependency URLs daily to detect breakage.

**Files to create:**

| File                                    | Purpose                                             |
| --------------------------------------- | --------------------------------------------------- |
| `scripts/check_dependency_urls.sh`      | HTTP check all download URLs from Dockerfiles       |
| `scripts/extract_download_urls.py`      | Extract URLs from Dockerfiles (curl, wget commands) |
| `.reports/supply_chain/url_health.json` | URL health status tracking                          |

**Check methods:**

| Check           | Method                                | Alert Condition         |
| --------------- | ------------------------------------- | ----------------------- |
| HTTP status     | `curl -o /dev/null -w "%{http_code}"` | Non-200 response        |
| DNS resolution  | `dig +short`                          | No DNS record           |
| TLS certificate | `openssl s_client`                    | Expired or invalid cert |
| Content-Type    | `curl -I`                             | Unexpected content type |

### T6.5.2: Checksum Change Detection

**Problem:** A changed checksum without a corresponding version bump may indicate a supply chain attack.

**Solution:** Compare current checksums against CHECKSUMS files and alert on unexpected changes.

**Files to create:**

| File                                          | Purpose                              |
| --------------------------------------------- | ------------------------------------ |
| `scripts/verify_checksums.sh`                 | Re-download and verify all checksums |
| `.reports/supply_chain/checksum_changes.json` | Checksum change log                  |

### T6.5.3: URL Breakage Alerting

**Solution:** Create GitHub Issue immediately when a URL returns 404 or checksum changes unexpectedly.

**Issue severity:**

| Condition            | Severity | SLA       |
| -------------------- | -------- | --------- |
| URL returns 404      | CRITICAL | 24 hours  |
| URL returns 5xx      | HIGH     | 48 hours  |
| TLS cert expired     | HIGH     | 24 hours  |
| Checksum mismatch    | CRITICAL | Immediate |
| Content-Type changed | MEDIUM   | 1 week    |

---

## 7. 6.6 Metrics Dashboard

### T6.6.1: Weekly Metrics Aggregation

**Problem:** No single view of registry health across all dimensions.

**Solution:** Aggregate all monitoring data into a weekly summary.

**Files to create:**

| File                                  | Purpose                                  |
| ------------------------------------- | ---------------------------------------- |
| `scripts/aggregate_weekly_metrics.py` | Collect data from all monitoring sources |
| `.reports/weekly_metrics/`            | Directory for weekly metric reports      |

**Data sources:**

| Source         | Location                                  | Metrics                         |
| -------------- | ----------------------------------------- | ------------------------------- |
| CVE scans      | `.reports/cve_history/`                   | CVE count by severity per image |
| Compliance     | `.reports/compliance_tracking/scores.csv` | CIS/STIG scores per image       |
| SBOM drift     | `.reports/sbom_history/`                  | Package count, drift events     |
| Build pipeline | GitHub Actions API                        | Build success rate, duration    |
| Image sizes    | Build artifacts                           | Size per image, trend           |

### T6.6.2: Markdown Report Generation

**Solution:** Generate a markdown report suitable for GitHub Actions job summary.

**Files to create:**

| File                                  | Purpose                  |
| ------------------------------------- | ------------------------ |
| `scripts/generate_weekly_report.py`   | Generate markdown report |
| `.reports/weekly_metrics/YYYY-WXX.md` | Weekly report per week   |

**Report sections:**

```markdown
# Weekly Security Report - YYYY-WXX

## CVE Summary

| Metric   | This Week | Last Week | Delta |
| -------- | --------- | --------- | ----- |
| CRITICAL | 0         | 1         | -1    |
| HIGH     | 3         | 5         | -2    |
| MEDIUM   | 12        | 10        | +2    |

## Compliance Scores

| Image | CIS Score | STIG Score | Trend |
| ----- | --------- | ---------- | ----- |

## Base Image Freshness

| Base Image | Current Version | Latest Version | Status |
| ---------- | --------------- | -------------- | ------ |

## Build Success Rate

| Metric       | Value |
| ------------ | ----- |
| Total builds | 223   |
| Successful   | 220   |
| Failed       | 3     |
| Success rate | 98.7% |

## Image Size Trend (Top 10 largest)

| Image | Size | Delta |
| ----- | ---- | ----- |
```

### T6.6.3: Trend Tracking

**Solution:** Track metrics over time to identify trends and regressions.

**Files to create:**

| File                                 | Purpose                                  |
| ------------------------------------ | ---------------------------------------- |
| `.reports/weekly_metrics/trends.csv` | Longitudinal metric data                 |
| `scripts/plot_trends.py`             | Generate ASCII trend charts for markdown |

---

## 8. Quality Gates

### QG-6.1: CVE Rescan Pipeline

| Criterion         | Threshold                     | Measurement                                |
| ----------------- | ----------------------------- | ------------------------------------------ |
| Daily scan runs   | 7/7 days per week             | GitHub Actions run history                 |
| Scan coverage     | 100% of images                | Scan result artifact completeness          |
| New CVE detection | Working                       | Baseline comparison produces diff          |
| Alert latency     | < 1 hour from scan completion | Issue creation timestamp vs scan timestamp |
| Rebuild trigger   | Working for CRITICAL/HIGH     | Workflow dispatch log                      |

### QG-6.2: SBOM Drift Detection

| Criterion                | Threshold                               | Measurement                                |
| ------------------------ | --------------------------------------- | ------------------------------------------ |
| Weekly SBOM generation   | 52 weeks retained                       | `.reports/sbom_history/` directory listing |
| Drift detection accuracy | Zero false positives on known-good diff | Manual validation                          |
| HIGH drift alerting      | GitHub Issue created within 24 hours    | Issue timestamp                            |

### QG-6.3: Compliance Tracking

| Criterion                | Threshold                      | Measurement            |
| ------------------------ | ------------------------------ | ---------------------- |
| CIS benchmark weekly run | Operational                    | Workflow run history   |
| STIG weekly run          | Operational                    | Workflow run history   |
| Score CSV                | Updated weekly with all images | `scores.csv` row count |
| Regression detection     | Working (>= 5% drop detected)  | Issue creation log     |

### QG-6.4: Base Image Freshness

| Criterion        | Threshold                       | Measurement          |
| ---------------- | ------------------------------- | -------------------- |
| Freshness check  | Runs daily                      | Workflow run history |
| Stale alerting   | Alerts for images > 30 days old | Issue creation log   |
| Auto-PR creation | Working for eligible updates    | PR listing           |

### QG-6.5: Supply Chain Monitoring

| Criterion                 | Threshold           | Measurement              |
| ------------------------- | ------------------- | ------------------------ |
| URL health check          | Runs daily          | Workflow run history     |
| 404 detection             | Alert within 1 hour | Issue creation timestamp |
| Checksum change detection | Working             | Alert log                |

### QG-6.6: Metrics Dashboard

| Criterion               | Threshold                | Measurement                          |
| ----------------------- | ------------------------ | ------------------------------------ |
| Weekly report generated | Every Monday             | `.reports/weekly_metrics/` directory |
| Report completeness     | All 5 sections populated | Manual review                        |
| Trend data              | 12+ weeks of history     | `trends.csv` row count               |

---

## 9. Dependencies

| Dependency                       | Source           | Status   |
| -------------------------------- | ---------------- | -------- |
| Phase 5 all quality gates passed | Phase 5 plan     | REQUIRED |
| Trivy installed and configured   | Phase 1 (T1.4.1) | Complete |
| Grype installed and configured   | Phase 1          | Complete |
| Syft installed and configured    | Phase 1 (T1.3.2) | Complete |
| docker-bench-security integrated | Phase 5 (T5.1.1) | Complete |
| STIG checks integrated           | Phase 5 (T5.2.1) | Complete |
| Images pushed to GHCR            | Phase 0 (T0.6.1) | Complete |
| Cosign signing operational       | Phase 1 (T1.2.1) | Complete |
| CHECKSUMS files for all images   | Phase 1 (T1.1.1) | Complete |
| Build workflow operational       | Phase 0 (T0.1.2) | Complete |

### External Dependencies

| Dependency               | Purpose                    | Risk if Unavailable           |
| ------------------------ | -------------------------- | ----------------------------- |
| GitHub Actions scheduler | Daily/weekly cron triggers | Manual triggering required    |
| GitHub Issues API        | Auto-issue creation        | Email notification fallback   |
| Docker Hub API           | Base image version checks  | Registry API polling fallback |
| GCR API                  | Distroless version checks  | Manual version tracking       |
| NVD API                  | CVE data enrichment        | Trivy/Grype local DB fallback |
| Trivy DB                 | Vulnerability database     | Scan results incomplete       |

---

## 10. Risk Assessment

| Risk ID  | Risk                                         | Probability | Impact | Mitigation                                                          | Status |
| -------- | -------------------------------------------- | ----------- | ------ | ------------------------------------------------------------------- | ------ |
| RISK-601 | GHA cron job silently fails                  | MEDIUM      | HIGH   | Monitor workflow run history; secondary alerting via external cron  | OPEN   |
| RISK-602 | Alert fatigue from too many issues           | HIGH        | MEDIUM | Deduplication, severity-based routing, weekly digest for LOW/MEDIUM | OPEN   |
| RISK-603 | Registry API rate limiting                   | MEDIUM      | LOW    | Cache results, use conditional requests, respect rate limits        | OPEN   |
| RISK-604 | False positive CVE detection                 | MEDIUM      | MEDIUM | Cross-reference Trivy + Grype; manual review for CRITICAL alerts    | OPEN   |
| RISK-605 | Base image auto-PR breaks builds             | LOW         | HIGH   | Run test build before creating PR; require CI pass for merge        | OPEN   |
| RISK-606 | Checksum mismatch false positive             | LOW         | HIGH   | Verify URL hasn't legitimately changed; manual confirmation step    | OPEN   |
| RISK-607 | SBOM generation fails for complex images     | LOW         | MEDIUM | Fallback to filesystem analysis; document unsupported images        | OPEN   |
| RISK-608 | Metrics data loss                            | LOW         | MEDIUM | Commit reports to git; GitHub Actions artifact backup               | OPEN   |
| RISK-609 | Supply chain URL monitoring misses redirects | MEDIUM      | LOW    | Follow redirects (-L flag); check final URL                         | OPEN   |

---

## 11. Timeline

### Phase 6 Execution Schedule

Phase 6 is **ongoing** with no fixed end date. Implementation of the monitoring infrastructure follows this schedule:

| Week | Tasks                          | Deliverables                              |
| ---- | ------------------------------ | ----------------------------------------- |
| 1    | T6.1.1, T6.1.2                 | Daily scan workflow + baseline system     |
| 2    | T6.1.3, T6.1.4, T6.1.5         | Auto-issues, rebuild trigger, CVE history |
| 3    | T6.2.1, T6.2.2, T6.2.3         | SBOM drift detection                      |
| 4    | T6.3.1, T6.3.2, T6.3.3, T6.3.4 | Compliance score tracking                 |
| 5    | T6.4.1, T6.4.2, T6.4.3         | Base image freshness + auto-PR            |
| 6    | T6.5.1, T6.5.2, T6.5.3         | Supply chain monitoring                   |
| 7    | T6.6.1, T6.6.2, T6.6.3         | Metrics dashboard                         |

### Ongoing Schedule (Post-Implementation)

| Frequency       | Activity                             | Trigger       |
| --------------- | ------------------------------------ | ------------- |
| Daily 06:00 UTC | CVE rescan (Trivy + Grype)           | Cron schedule |
| Daily 06:00 UTC | Base image freshness check           | Cron schedule |
| Daily 06:00 UTC | Supply chain URL health check        | Cron schedule |
| Weekly Monday   | SBOM generation + drift detection    | Cron schedule |
| Weekly Monday   | CIS Docker Benchmark                 | Cron schedule |
| Weekly Monday   | DISA STIG checks                     | Cron schedule |
| Weekly Monday   | Compliance score update              | Cron schedule |
| Weekly Monday   | Metrics report generation            | Cron schedule |
| On-demand       | Manual trigger via workflow_dispatch | Manual        |

### Estimated Total Effort

| Component                        | Estimated Hours |
| -------------------------------- | --------------- |
| CVE Scanning Pipeline (T6.1.x)   | 24              |
| SBOM Drift Detection (T6.2.x)    | 12              |
| Compliance Tracking (T6.3.x)     | 16              |
| Base Image Freshness (T6.4.x)    | 12              |
| Supply Chain Monitoring (T6.5.x) | 8               |
| Metrics Dashboard (T6.6.x)       | 12              |
| **Total**                        | **84 hours**    |

---

**END OF PHASE 6 PLAN**
