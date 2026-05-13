# Registry Health Metrics Dashboard

## Grafana Dashboard Specification

**UID:** `evergreen-registry-health`
**Title:** Evergreen Image Registry Health
**Refresh:** 5m
**Tags:** `evergreen`, `registry`, `policy`, `compliance`

---

## Data Sources

| Name | Type | Purpose |
|------|------|---------|
| Prometheus | prometheus | CI metrics, image sizes, layer counts |
| JSON API | json-datasource | evergreenctl policy scan results |
| GitHub Actions | github-datasource | Workflow run outcomes |

---

## Panels

### Row 1: Coverage Gauges

#### Panel 1.1: Non-Root Compliance
- **Type:** Gauge
- **Title:** Non-Root User Coverage
- **Query:** `count(evergreen_policy_check{check="user",status="pass"}) / count(evergreen_policy_check{check="user"}) * 100`
- **Thresholds:** Green >= 95, Yellow >= 80, Red < 80
- **Unit:** percent (0-100)

#### Panel 1.2: SBOM Coverage
- **Type:** Gauge
- **Title:** SBOM Generation Coverage
- **Query:** `count(evergreen_policy_check{check="sbom_file",status="pass"}) / count(evergreen_policy_check{check="sbom_file"}) * 100`
- **Thresholds:** Green >= 90, Yellow >= 70, Red < 70
- **Unit:** percent (0-100)

#### Panel 1.3: Digest-Pinned FROM
- **Type:** Gauge
- **Title:** Digest-Pinned Base Images
- **Query:** `count(evergreen_policy_check{check="from_digest",status="pass"}) / count(evergreen_policy_check{check="from_digest"}) * 100`
- **Thresholds:** Green >= 95, Yellow >= 80, Red < 80
- **Unit:** percent (0-100)

#### Panel 1.4: Multi-Arch Build Coverage
- **Type:** Gauge
- **Title:** Multi-Arch Builds
- **Query:** `count(evergreen_image_arch{arch=~"amd64|arm64"}) by (image) > 1` / total images
- **Thresholds:** Green >= 80, Yellow >= 50, Red < 50
- **Unit:** percent (0-100)

---

### Row 2: Trend Charts

#### Panel 2.1: CI Pass Rate Over Time
- **Type:** Time series
- **Title:** CI Pipeline Pass Rate (30d)
- **Query:** `sum(rate(github_workflow_run_total{conclusion="success"}[1d])) / sum(rate(github_workflow_run_total[1d])) * 100`
- **Legend:** Pass rate %
- **Y-axis:** 0-100%
- **Tooltip:** Show per-workflow breakdown

#### Panel 2.2: Vulnerability Count Over Time
- **Type:** Time series
- **Title:** Known Vulnerabilities (30d)
- **Query A (Critical):** `sum(evergreen_vulnerability_total{severity="critical"})`
- **Query B (High):** `sum(evergreen_vulnerability_total{severity="high"})`
- **Query C (Medium):** `sum(evergreen_vulnerability_total{severity="medium"})`
- **Legend:** Per-severity stacked
- **Alert:** Critical > 0 triggers alert

#### Panel 2.3: Policy Violations Over Time
- **Type:** Time series
- **Title:** Policy Violations Trend (30d)
- **Query A (Block):** `sum(evergreen_policy_violations{severity="block"})`
- **Query B (Warn):** `sum(evergreen_policy_violations{severity="warn"})`
- **Fill opacity:** 10%

---

### Row 3: Tables

#### Panel 3.1: Upstream Version Drift
- **Type:** Table
- **Title:** Upstream Version Drift by Category
- **Transformations:** Organize fields by category, sort by drift_days desc
- **Columns:**
  - Image name
  - Category (proxy, database, monitoring, etc.)
  - Current version
  - Latest upstream version
  - Drift (days behind)
  - Status (current / minor-behind / major-behind / critical)
- **Color rows:** Red if drift > 90d, Yellow if > 30d, Green otherwise

#### Panel 3.2: Recently Bumped Images
- **Type:** Table
- **Title:** Images Bumped in Last 7 Days
- **Transformations:** Sort by bump_date desc
- **Columns:**
  - Image name
  - Previous version
  - New version
  - Bump date
  - PR number
  - CI status (icon)
- **Footer:** Count of images bumped this week

---

### Row 4: Alerts & Annotations

#### Panel 4.1: Active Alerts
- **Type:** Alert list
- **Title:** Active Registry Alerts
- **Alert Rules:**
  - `EvergreenCriticalVuln`: Any critical vulnerability detected
  - `EvergreenPolicyBlock`: Any block-severity policy violation
  - `EvergreenStaleImage`: Image drift > 90 days
  - `EvergreenCIFailure`: Build pipeline failure rate > 10%

---

## Variables

| Name | Type | Values | Default |
|------|------|--------|---------|
| `category` | Custom | proxy, database, monitoring, security, devops, messaging, dns, vpn, search, app, runtime, official | All |
| `tier` | Custom | 1, 2, 3 | All |
| `severity` | Custom | critical, high, medium, low | All |

---

## Grafana JSON Template

```json
{
  "dashboard": {
    "uid": "evergreen-registry-health",
    "title": "Evergreen Image Registry Health",
    "tags": ["evergreen", "registry", "policy", "compliance"],
    "timezone": "browser",
    "refresh": "5m",
    "time": { "from": "now-30d", "to": "now" },
    "templating": {
      "list": [
        {
          "name": "category",
          "type": "custom",
          "multi": true,
          "includeAll": true,
          "allValue": ".*",
          "current": { "selected": true, "text": "All", "value": "$__all" },
          "values": [
            "proxy", "database", "monitoring", "security", "devops",
            "messaging", "dns", "vpn", "search", "app", "runtime", "official"
          ]
        },
        {
          "name": "tier",
          "type": "custom",
          "multi": true,
          "includeAll": true,
          "allValue": ".*",
          "current": { "selected": true, "text": "All", "value": "$__all" },
          "values": ["1", "2", "3"]
        }
      ]
    },
    "panels": [
      {
        "type": "row",
        "title": "Coverage Gauges",
        "gridPos": { "h": 1, "w": 24, "x": 0, "y": 0 }
      },
      {
        "id": 1,
        "type": "gauge",
        "title": "Non-Root User Coverage",
        "gridPos": { "h": 6, "w": 6, "x": 0, "y": 1 },
        "targets": [
          {
            "expr": "count(evergreen_policy_check{check=\"user\",status=\"pass\"}) / count(evergreen_policy_check{check=\"user\"}) * 100",
            "legendFormat": "non-root"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "percent",
            "thresholds": {
              "steps": [
                { "color": "red", "value": null },
                { "color": "yellow", "value": 80 },
                { "color": "green", "value": 95 }
              ]
            },
            "min": 0,
            "max": 100
          }
        }
      },
      {
        "id": 2,
        "type": "gauge",
        "title": "SBOM Generation Coverage",
        "gridPos": { "h": 6, "w": 6, "x": 6, "y": 1 },
        "targets": [
          {
            "expr": "count(evergreen_policy_check{check=\"sbom_file\",status=\"pass\"}) / count(evergreen_policy_check{check=\"sbom_file\"}) * 100",
            "legendFormat": "sbom"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "percent",
            "thresholds": {
              "steps": [
                { "color": "red", "value": null },
                { "color": "yellow", "value": 70 },
                { "color": "green", "value": 90 }
              ]
            },
            "min": 0,
            "max": 100
          }
        }
      },
      {
        "id": 3,
        "type": "gauge",
        "title": "Digest-Pinned Base Images",
        "gridPos": { "h": 6, "w": 6, "x": 12, "y": 1 },
        "targets": [
          {
            "expr": "count(evergreen_policy_check{check=\"from_digest\",status=\"pass\"}) / count(evergreen_policy_check{check=\"from_digest\"}) * 100",
            "legendFormat": "digest-pinned"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "percent",
            "thresholds": {
              "steps": [
                { "color": "red", "value": null },
                { "color": "yellow", "value": 80 },
                { "color": "green", "value": 95 }
              ]
            },
            "min": 0,
            "max": 100
          }
        }
      },
      {
        "id": 4,
        "type": "gauge",
        "title": "Multi-Arch Builds",
        "gridPos": { "h": 6, "w": 6, "x": 18, "y": 1 },
        "targets": [
          {
            "expr": "count(count by (image) (evergreen_image_arch)) / count(count by (image) (evergreen_image_arch) > 1) * 100",
            "legendFormat": "multi-arch"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "percent",
            "thresholds": {
              "steps": [
                { "color": "red", "value": null },
                { "color": "yellow", "value": 50 },
                { "color": "green", "value": 80 }
              ]
            },
            "min": 0,
            "max": 100
          }
        }
      },
      {
        "type": "row",
        "title": "Trend Charts",
        "gridPos": { "h": 1, "w": 24, "x": 0, "y": 7 }
      },
      {
        "id": 5,
        "type": "timeseries",
        "title": "CI Pipeline Pass Rate (30d)",
        "gridPos": { "h": 8, "w": 8, "x": 0, "y": 8 },
        "targets": [
          {
            "expr": "sum(rate(github_workflow_run_total{conclusion=\"success\"}[1d])) / sum(rate(github_workflow_run_total[1d])) * 100",
            "legendFormat": "pass rate"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "percent",
            "min": 0,
            "max": 100,
            "custom": { "fillOpacity": 20 }
          }
        }
      },
      {
        "id": 6,
        "type": "timeseries",
        "title": "Known Vulnerabilities (30d)",
        "gridPos": { "h": 8, "w": 8, "x": 8, "y": 8 },
        "targets": [
          {
            "expr": "sum(evergreen_vulnerability_total{severity=\"critical\"})",
            "legendFormat": "critical"
          },
          {
            "expr": "sum(evergreen_vulnerability_total{severity=\"high\"})",
            "legendFormat": "high"
          },
          {
            "expr": "sum(evergreen_vulnerability_total{severity=\"medium\"})",
            "legendFormat": "medium"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "short",
            "custom": {
              "fillOpacity": 10,
              "stacking": { "mode": "normal" }
            }
          }
        }
      },
      {
        "id": 7,
        "type": "timeseries",
        "title": "Policy Violations Trend (30d)",
        "gridPos": { "h": 8, "w": 8, "x": 16, "y": 8 },
        "targets": [
          {
            "expr": "sum(evergreen_policy_violations{severity=\"block\"})",
            "legendFormat": "block"
          },
          {
            "expr": "sum(evergreen_policy_violations{severity=\"warn\"})",
            "legendFormat": "warn"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "short",
            "custom": { "fillOpacity": 10 }
          }
        }
      },
      {
        "type": "row",
        "title": "Tables",
        "gridPos": { "h": 1, "w": 24, "x": 0, "y": 16 }
      },
      {
        "id": 8,
        "type": "table",
        "title": "Upstream Version Drift by Category",
        "gridPos": { "h": 10, "w": 12, "x": 0, "y": 17 },
        "targets": [
          {
            "expr": "evergreen_image_version_drift_days",
            "legendFormat": "{{image}}",
            "format": "table",
            "instant": true
          }
        ],
        "transformations": [
          { "id": "organize", "options": { "excludeByName": { "Time": true } } },
          { "id": "sortBy", "options": { "fields": {}, "sort": [{ "field": "drift_days", "desc": true }] } }
        ],
        "fieldConfig": {
          "defaults": {
            "thresholds": {
              "mode": "absolute",
              "steps": [
                { "color": "green", "value": null },
                { "color": "yellow", "value": 30 },
                { "color": "red", "value": 90 }
              ]
            },
            "custom": {
              "align": "auto",
              "cellOptions": { "type": "auto" }
            }
          },
          "overrides": [
            {
              "matcher": { "id": "byName", "options": "drift_days" },
              "properties": [
                { "id": "unit", "value": "d" },
                { "id": "thresholds", "value": { "mode": "absolute", "steps": [
                  { "color": "green", "value": null },
                  { "color": "yellow", "value": 30 },
                  { "color": "red", "value": 90 }
                ] } },
                { "id": "cellOptions", "value": { "type": "color-background" } }
              ]
            }
          ]
        }
      },
      {
        "id": 9,
        "type": "table",
        "title": "Images Bumped in Last 7 Days",
        "gridPos": { "h": 10, "w": 12, "x": 12, "y": 17 },
        "targets": [
          {
            "expr": "evergreen_image_bump{bump_date >= now() - 7d}",
            "legendFormat": "{{image}}",
            "format": "table",
            "instant": true
          }
        ],
        "transformations": [
          { "id": "organize", "options": { "excludeByName": { "Time": true } } },
          { "id": "sortBy", "options": { "fields": {}, "sort": [{ "field": "bump_date", "desc": true }] } }
        ],
        "fieldConfig": {
          "defaults": {
            "custom": { "align": "auto" }
          }
        }
      }
    ],
    "alerting": {
      "alert_rules": [
        {
          "uid": "evergreen-critical-vuln",
          "title": "Critical Vulnerability Detected",
          "condition": "A",
          "data": [
            {
              "refId": "A",
              "queryType": "",
              "datasourceUid": "prometheus",
              "model": {
                "expr": "sum(evergreen_vulnerability_total{severity=\"critical\"}) > 0"
              }
            }
          ],
          "for": "5m",
          "annotations": { "summary": "Critical vulnerability found in registry images" },
          "labels": { "severity": "critical" }
        },
        {
          "uid": "evergreen-policy-block",
          "title": "Block-Level Policy Violation",
          "condition": "A",
          "data": [
            {
              "refId": "A",
              "queryType": "",
              "datasourceUid": "prometheus",
              "model": {
                "expr": "sum(evergreen_policy_violations{severity=\"block\"}) > 0"
              }
            }
          ],
          "for": "15m",
          "annotations": { "summary": "Block-severity policy violation detected" },
          "labels": { "severity": "warning" }
        },
        {
          "uid": "evergreen-stale-image",
          "title": "Image Version Drift Exceeds 90 Days",
          "condition": "A",
          "data": [
            {
              "refId": "A",
              "queryType": "",
              "datasourceUid": "prometheus",
              "model": {
                "expr": "count(evergreen_image_version_drift_days > 90) > 0"
              }
            }
          ],
          "for": "1h",
          "annotations": { "summary": "One or more images are more than 90 days behind upstream" },
          "labels": { "severity": "warning" }
        },
        {
          "uid": "evergreen-ci-failure",
          "title": "Build Pipeline Failure Rate > 10%",
          "condition": "A",
          "data": [
            {
              "refId": "A",
              "queryType": "",
              "datasourceUid": "prometheus",
              "model": {
                "expr": "sum(rate(github_workflow_run_total{conclusion=\"failure\"}[1d])) / sum(rate(github_workflow_run_total[1d])) * 100 > 10"
              }
            }
          ],
          "for": "30m",
          "annotations": { "summary": "CI build failure rate exceeds 10%" },
          "labels": { "severity": "warning" }
        }
      ]
    }
  }
}
```
