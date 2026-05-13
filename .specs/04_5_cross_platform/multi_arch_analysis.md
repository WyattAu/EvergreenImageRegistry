# Multi-Arch Analysis for Evergreen Image Registry

## Date: 2026-05-13

## Version: v26.14.0

## Executive Summary

Analysis of all 998 Dockerfiles for multi-architecture (amd64 + arm64) support. Current state: 250 images (25.1%) have
`ARG TARGETARCH`, 584 (58.5%) are single-arch non-scratch, 164 (16.4%) are scratch-based single-arch. ~65% of
single-arch images likely have upstream arm64 support available.

## Current State

| Category                   | Count | %     |
| -------------------------- | ----- | ----- |
| Has `ARG TARGETARCH`       | 250   | 25.1% |
| Scratch-based (all)        | 398   | 39.9% |
| Scratch + TARGETARCH       | 234   | 23.4% |
| Scratch, single-arch       | 164   | 16.4% |
| Non-scratch, no TARGETARCH | 584   | 58.5% |
| Non-scratch + TARGETARCH   | 16    | 1.6%  |

### Cross-Reference Matrix

|              | Has TARGETARCH | No TARGETARCH | Total |
| ------------ | -------------- | ------------- | ----- |
| FROM scratch | 234            | 164           | 398   |
| Not scratch  | 16             | 584           | 600   |
| Total        | 250            | 748           | 998   |

## Feasibility Tiers

### Tier 1: Easy Wins -- Download-Binary with Known arm64 Upstream (~123 images)

These images download pre-built upstream binaries via curl/wget. The upstream project publishes arm64 binaries.
Conversion requires adding `ARG TARGETARCH` and conditional URL selection.

**Pattern:**

```dockerfile
ARG TARGETARCH
RUN case ${TARGETARCH} in \
    amd64) ARCH="amd64" ;; \
    arm64) ARCH="arm64" ;; \
    *) echo "Unsupported architecture: ${TARGETARCH}" && exit 1 ;; \
    esac && \
    curl -fsSL "https://example.com/${ARCH}/app.tar.gz" -o app.tar.gz
```

**Examples:** redis, postgresql, mysql, mongodb, elasticsearch, nginx, haproxy, consul, vault, grafana, keycloak,
jenkins, gitlab, gitea, minio, kafka, rabbitmq, cassandra, neo4j, milvus, opensearch, fluent-bit, vector, loki, thanos,
trivy, restic, prometheus, etcd, cadvisor, envoy, coreDNS, unbound, bind, adguard-home, tailscale, wireguard, headscale,
influxdb, dragonfly, memcached, valkey, powerdns, sonarr, radarr, prowlarr, readarr, lidarr, jellyfin, transmission,
qBittorrent, vaultwarden, kaniko, sentry, authentik, graylog, arangodb, couchdb, timescaledb, pgbouncer, emqx,
nextcloud, pi-hole, home-assistant, nat, etc.

**Effort:** 2-4h (automated pattern detection + bulk conversion script) **Risk:** Low -- upstream already provides arm64
binaries

### Tier 2: Wolfi-Base Package-Install (~273 images)

These images use `apk add`/`dnf install` from Chainguard's wolfi repository, which already publishes arm64 packages.
Conversion requires adding `ARG TARGETARCH` and ensuring CI builds multi-platform.

**Pattern:** No code changes needed -- wolfi packages are already multi-arch. Only CI pipeline changes required (build
with `--platform linux/amd64,linux/arm64`).

**Includes:** Infrastructure tools, security scanners, utility images, CLI tools, and many others that install packages
from wolfi repos.

**Effort:** 1-2h (CI pipeline changes only) **Risk:** Very low -- wolfi repo already cross-compiled

### Tier 3: Wolfi-Base with Python pip (~145 images)

Python packages may have native C extensions that need arm64 wheels. Many popular Python packages already ship arm64
wheels on PyPI.

**Sub-categories:**

- Pure Python (no C extensions): Zero risk, just CI changes
- Python with popular C extensions (numpy, pandas, cryptography): Likely have arm64 wheels
- Python with niche C extensions: May need compilation or musl-based builds

**Effort:** 4-8h (audit + verify arm64 wheels + CI changes) **Risk:** Medium -- depends on upstream Python package arm64
availability

### Tier 4: Wolfi-Base with Node.js npm (~63 images)

Most Node.js packages are JavaScript-only. Some have native add-ons (node-gyp).

**Effort:** 2-4h (audit native add-ons + CI changes) **Risk:** Low -- most Node packages are pure JS

### Tier 5: Wolfi-Base with Java JVM (~29 images)

Java is inherently cross-platform (JVM handles arch differences).

**Effort:** 1h (CI changes only) **Risk:** Very low -- JVM is arch-independent

### Tier 6: Wolfi-Base with PHP (~39 images)

Most PHP extensions are pure PHP. Some have native extensions.

**Effort:** 2-4h (audit + CI changes) **Risk:** Low

### Tier 7: Wolfi-Base with Ruby gem (~9 images)

Some Ruby gems have native extensions (nokogiri, etc.).

**Effort:** 2-4h (audit + CI changes) **Risk:** Low-Medium

### Tier 8: Scratch-Based Single-Arch (~164 images)

These require source rebuilds with `GOARCH`/`TARGETARCH` awareness, or obtaining arm64 binaries from upstream.

**Sub-categories:**

- 74 upstream-repackage: May be straightforward if upstream provides arm64 images
- 72 debian-builder: Need cross-compilation setup
- 17 scratch-only: Need upstream arm64 binaries (highest effort)
- 1 Go builder reference template

**Effort:** 8-16h **Risk:** Medium-High -- requires upstream arm64 binary availability

### Tier 9: Blocked -- No arm64 Upstream (~7-24 images)

Images where upstream has no arm64 support:

- plex, plex-media-server, plex-push (no arm64 builds)
- oracledb-xe (x86_64 only)
- scylladb (no arm64)
- tigergraph, tigergraph-ecosystem (no arm64)
- cubrid, orientdb, nxlog, xteve (no arm64)

**Effort:** N/A (blocked) **Risk:** N/A (cannot support without upstream change)

## Language/Framework Summary

| Language             | Total Runtime | Multi-Arch Ready | Needs Work        |
| -------------------- | ------------- | ---------------- | ----------------- |
| Java/JVM             | 29            | 29 (100%)        | CI only           |
| Pure binary download | 123           | ~123             | CI + URL pattern  |
| wolfi apk/dnf        | 273           | ~273             | CI only           |
| Node.js              | 63            | ~60              | CI + audit native |
| PHP                  | 39            | ~37              | CI + audit native |
| Python               | 145           | ~120             | CI + audit wheels |
| Ruby                 | 9             | ~7               | CI + audit gems   |
| Go (builder)         | 18            | 17               | Already done      |
| Rust (runtime)       | 2             | 2                | CI only           |

## Recommended Approach

### Phase 64a: CI Multi-Platform Support (1h)

- Add `--platform linux/amd64,linux/arm64` to CI build matrix
- Add `ARG TARGETARCH` to the standard Dockerfile template
- Verify wolfi-base Tier-2 images build on arm64

### Phase 64b: Tier-1 Download-Binary Conversion (2-4h)

- Write automated script to detect download-binary patterns
- Generate TARGETARCH-aware Dockerfile patches
- Validate arm64 binary URLs for top 50 images
- Apply patches in batches

### Phase 64c: Tier-2/5/6 CI-Only (1-2h)

- Enable multi-platform CI builds for package-install images
- No Dockerfile changes needed

### Phase 64d: Tier-3 Python Audit (4-8h)

- Audit 145 Python images for native extensions
- Verify arm64 wheel availability on PyPI
- Flag images that need source compilation

### Phase 64e: Tier-8 Scratch-Based (8-16h)

- Categorize 164 scratch images by upstream arm64 availability
- Convert upstream-repackage images (74)
- Convert debian-builder images with cross-compilation (72)

## Success Metrics

| Metric              | Current     | Target (Post-Phase 64) | Target (Post-Phase 65) |
| ------------------- | ----------- | ---------------------- | ---------------------- |
| TARGETARCH images   | 250 (25.1%) | 500 (50.1%)            | 800 (80.2%)            |
| arm64 CI builds     | 0           | 400+                   | 800+                   |
| Blocked by upstream | Unknown     | 24 (2.4%)              | 24 (2.4%)              |
