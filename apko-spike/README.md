# apko Reproducible Build Spike

## Goal

Evaluate whether migrating hardened images from Dockerfile to apko.yaml achieves reproducible builds (same input → same
digest).

## Methodology

1. Build 5 hardened images with apko
2. Build same 5 images twice
3. Compare digests — if identical, builds are reproducible

## Findings

(to be filled after spike execution)

## Prerequisites

- `apko` CLI tool
- `melange` CLI tool (for building packages from source)
- Wolfi package repository access

## Status

**Not started** — apko requires Wolfi packages for all components. Our hardened images use binary downloads from GitHub
releases, which apko doesn't handle natively. Would need melange pipelines to package each binary as an APK first.

## Alternative Approach

Use `docker build --build-arg SOURCE_DATE_EPOCH=0` for semi-reproducible Docker builds. This doesn't guarantee identical
digests (due to timestamp metadata in layers) but gets close.

## Recommendation

For EIR's use case (self-hosted, not enterprise-certified), reproducible builds via apko provide marginal value over
signed images with provenance. Defer apko migration until there's a concrete need (e.g., supply chain audit
requirement).
