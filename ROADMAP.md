# Evergreen Image Registry Roadmap

## Current: v31.0.0 (Phase 113)

661 active images, all building via CI, all on GHCR.

## Phase 114: SIS Migration Completion
- Deploy remaining SIS stacks to TrueNAS
- Stacks: utility, updater, documents, rss, collaboration, accounting
- Fix SIS git auto-sync

## Phase 115: Restore Archived Images
- Restore top-50 archived images with verified upstreams
- Focus: etcd, consul, vault, mongodb, gitlab-ce, jenkins, kibana, jaeger

## Phase 116: True Hardening (Critical Tier)
- Replace repack with binary extraction for top 20 images
- Target: redis, postgres, nginx, traefik, keycloak, vaultwarden
- Goal: Non-root, distroless, no shell

## Phase 117: Multi-Arch Support
- Re-enable ARM64 builds
- Test on Graviton/Raspberry Pi

## Phase 118: Compliance
- CIS benchmark scans
- FIPS 140-2/3 for 30 identified images
- STIG hardening

## Phase 119: Automation
- Docker Hub mirror to GHCR
- Dependabot auto-rebuilds
- Blocking smoke tests in CI
