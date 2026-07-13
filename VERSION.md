# Evergreen Image Registry

**Version:** v35.0.0 **Phase:** 130 **Date:** 2026-07-12

## Registry Status

| Metric          | Value             | Notes                                               |
| --------------- | ----------------- | --------------------------------------------------- |
| Active images   | 802               | All have valid manifests, entrypoint validation     |
| Archived images | 211               | Stubs, broken upstreams, duplicates                 |
| Hardened images | 20 verified       | scratch/wolfi, non-root, smoke-tested               |
| Build pass rate | ~82%              | 41/50 in latest CI build (without Docker Hub creds) |
| Supply chain    | ✅ All 4 verified | Cosign + SPDX + CycloneDX + SLSA                    |
| CI lint         | ✅ Green          | Prettier, Ruff, Entrypoint, Manifest validation     |
| Multi-arch      | amd64, arm64      | s390x, ppc64le configured but untested              |
| SIS stacks      | 19/20 on EIR      | Only webhook remains external                       |

## Supply Chain (Verified End-to-End)

All 4 supply chain artifacts verified on `nginx:latest`:

```
✅ Cosign signature: cosign verify → passes
✅ SPDX SBOM: cosign verify-attestation --type spdxjson → passes
✅ CycloneDX SBOM: cosign verify-attestation --type cyclonedx → passes
✅ SLSA provenance: cosign verify-attestation --type slsaprovenance → passes
```

See `docs/verifying-images.md` for verification commands.

## Hardened Images (20 verified)

Runtime smoke-tested, confirmed working:

| Image             | Base             | Smoke Test                   |
| ----------------- | ---------------- | ---------------------------- |
| redis             | scratch          | ✅ Running                   |
| traefik           | scratch          | ✅ Running                   |
| grafana           | scratch          | ✅ Running                   |
| nats              | scratch          | ✅ Running                   |
| node-exporter     | scratch          | ✅ Running                   |
| valkey            | Chainguard wolfi | ✅ Running                   |
| forgejo           | scratch          | ✅ Running                   |
| vaultwarden       | Repack           | ✅ Running                   |
| keycloak          | Repack           | ✅ HTTP 200                  |
| postgresql-16     | Chainguard wolfi | ✅ SELECT 1                  |
| mariadb           | Chainguard wolfi | ✅ mysqladmin alive          |
| oauth2-proxy      | scratch          | ✅ HTTP 403                  |
| nginx             | wolfi-base       | ✅ (needs /run tmpfs)        |
| prometheus        | scratch          | ✅ (needs /prometheus tmpfs) |
| alertmanager      | scratch          | ✅ (needs config)            |
| etcd              | scratch          | ✅ (needs --data-dir)        |
| cloudflared       | scratch          | ✅ (needs tunnel config)     |
| dex               | Repack           | ✅ (needs config)            |
| step-ca           | Repack           | ✅ (needs CA config)         |
| blackbox-exporter | scratch          | ✅ (needs config)            |

## Known Issues

1. **Docker Hub credentials expired** — refresh `DOCKERHUB_TOKEN` in GitHub secrets
2. **9/50 images fail to build** — old restored images with broken upstreams
3. **Docker Hub mirror references reverted** — GHCR nested packages can't be set public
4. **~50 images have no runtime smoke test** — built but not verified at runtime
