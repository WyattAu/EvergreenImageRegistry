# Evergreen Operator

Kubernetes operator for the Evergreen Image Registry. Provides:

1. **Auto-Updates** — Watches image manifests and auto-updates Deployments on version bumps
2. **Compliance Enforcement** — Runs policy checks against running workloads
3. **Drift Detection** — Alerts when running images drift from registry versions
4. **SBOM Sync** — Ensures SBOMs are current for all deployed images

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    Evergreen Operator                     │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Image Watcher │  │  Compliance   │  │    Drift     │  │
│  │              │  │   Enforcer    │  │   Detector   │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                  │                  │          │
│  ┌──────▼──────────────────▼──────────────────▼───────┐  │
│  │              evergreenctl CLI                      │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │           Custom Resource Definitions              │  │
│  │  - EvergreenImage (image tracking)                │  │
│  │  - EvergreenPolicy (compliance rules)             │  │
│  │  - EvergreenDrift (drift alerts)                  │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

## Custom Resource Definitions (CRDs)

### EvergreenImage

Tracks a specific EIR image and manages auto-updates.

```yaml
apiVersion: evergreenimageregistry.io/v1
kind: EvergreenImage
metadata:
  name: redis
  namespace: default
spec:
  image: ghcr.io/wyattau/evergreenimageregistry/redis
  tag: latest
  autoUpdate: true
  updateStrategy: rolling  # rolling | recreate
  compliance:
    requireSBOM: true
    requireVEX: true
    fipsRequired: false
  notifications:
    slack: "#security-alerts"
    pagerduty: true
status:
  currentTag: latest
  lastUpdated: "2026-08-22T00:00:00Z"
  SBOMStatus: valid
  complianceStatus: passing
```

### EvergreenPolicy

Defines compliance policies for a namespace or cluster.

```yaml
apiVersion: evergreenimageregistry.io/v1
kind: EvergreenPolicy
metadata:
  name: tier1-policy
  namespace: production
spec:
  scope: namespace  # namespace | cluster
  rules:
    - id: FIPS-001
      severity: critical
      enforce: true
    - id: SIZE-001
      severity: medium
      enforce: true
      config:
        maxSizeMB: 500
  exemptions:
    - image: custom-app
      reason: "Legacy app, migrating to EIR"
```

### EvergreenDrift

Monitors for image drift and generates alerts.

```yaml
apiVersion: evergreenimageregistry.io/v1
kind: EvergreenDrift
metadata:
  name: production-drift
  namespace: production
spec:
  interval: 1h
  scope: namespace
  alerting:
    slack: "#security-alerts"
    pagerduty: true
  thresholds:
    critical: 0    # No drift allowed for Tier 1
    standard: 3    # 3h grace period for Tier 2
status:
  lastCheck: "2026-08-22T00:00:00Z"
  driftDetected: 0
  alerts: []
```

## Installation

```bash
# Install via Helm
helm install evergreen-operator ./operator \
  --namespace evergreen-system \
  --create-namespace

# Or install from GitHub
helm install evergreen-operator \
  oci://ghcr.io/wyattau/evergreenimageregistry/operator \
  --version 0.1.0
```

## Features

### Auto-Update Workflow

1. Operator watches `EvergreenImage` resources
2. On new version detected (via registry webhook or polling):
   - Validates new image passes constraint engine
   - Generates SBOM if missing
   - Updates Deployment image tag
   - Rolls out update with configurable strategy
   - Notifies on success/failure

### Compliance Enforcement

1. Operator runs `evergreenctl validate-parallel` on schedule
2. Violations trigger `EvergreenPolicy` events
3. BLOCK violations auto-reject image updates
4. WARN violations generate Slack/PagerDuty alerts

### Drift Detection

1. Operator compares running image digests against registry
2. Detects unauthorized image modifications
3. Alerts on drift exceeding threshold
4. Optional: auto-rollback to last known good version

## RBAC

The operator requires:
- `get`, `list`, `watch` on Deployments, DaemonSets, StatefulSets
- `update` on Deployments (for image updates)
- `create`, `update`, `delete` on EvergreenImage/EvergreenPolicy/EvergreenDrift CRDs
- `get`, `list` on ConfigMaps, Secrets (for configuration)
