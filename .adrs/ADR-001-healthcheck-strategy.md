# Architecture Decision Record: HEALTHCHECK Strategy for Scratch/Distroless Images

## ADR-001: HEALTHCHECK Strategy for Scratch/Distroless Images

### Status
ACCEPTED

### Date
2026-04-19

### Author
Nexus (Principal Systems Architect)

### Context

All 104 scratch-based images and 7 distroless-based images in the registry use **shell-form** HEALTHCHECK instructions:

```dockerfile
HEALTHCHECK CMD nginx -v
```

Docker interprets shell-form HEALTHCHECK as:
```
/bin/sh -c "nginx -v"
```

Since `FROM scratch` and `gcr.io/distroless/*` contain no `/bin/sh`, **every HEALTHCHECK fails** with:
```
OCI runtime exec failed: exec: "/bin/sh": stat /bin/sh: no such file or directory
```

Additionally, the ENTRYPOINT/HEALTHCHECK interaction causes a secondary bug:
- ENTRYPOINT: `["/nginx"]`
- HEALTHCHECK CMD: `nginx -v` (shell form, appended to ENTRYPOINT)
- Actual execution: `/nginx nginx -v` — wrong

This means constraint C010 (health check endpoint) is **not satisfied** for 111 of 223 images.

### Decision

**Use exec-form HEALTHCHECK with absolute binary paths for all scratch and distroless images.**

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/nginx", "-v"]
```

#### Rules

1. **Exec form ONLY** for scratch/distroless images: `CMD ["/binary", "arg"]`
2. **Absolute path REQUIRED**: No reliance on PATH (scratch has no PATH)
3. **Do NOT depend on ENTRYPOINT**: HEALTHCHECK CMD in exec form runs independently
4. **Version flag as health proxy**: For Phase 0, use `--version`/`-v` to verify binary integrity
5. **HTTP health checks deferred to Phase 2**: Requires embedding a static `wget` binary

#### Per-Category Strategy

| Category | Strategy | HEALTHCHECK Format |
|----------|----------|-------------------|
| A: Scratch (static binary) | Binary version check | `CMD ["/binary", "--version"]` |
| B: Distroless (glibc binary) | Binary version check | `CMD ["/binary", "--version"]` |
| C: Wolfi (has shell) | curl-based HTTP check | `CMD ["/usr/bin/curl", "-sf", "http://localhost:PORT/path"]` |
| D: Debian-slim (has shell+curl) | curl-based HTTP check | `CMD curl -sf http://localhost:PORT/path \|\| exit 1` |
| E: Official (varies) | curl-based or none | Per-image decision |

### Consequences

**Positive:**
- HEALTHCHECK actually works at runtime
- Constraint C010 satisfied for all images
- No shell dependency introduced
- Consistent pattern across all images

**Negative:**
- Version flag check only verifies binary integrity, not service health
- HTTP health checks deferred to Phase 2 (requires static wget embedding)
- Some binaries may not support `--version` flag (need per-image handling)

**Risks:**
- Some binaries may not have a `--version` flag — need alternative (e.g., `--help`, `-V`)
- Some binaries may return non-zero exit code on `--version` — need testing

### Alternatives Considered

| Alternative | Pros | Cons | Reason Rejected |
|-------------|------|------|-----------------|
| Embed busybox in scratch | Enables shell-form HEALTHCHECK and curl | Adds ~1MB, adds shell (violates C003) | Violates zero-shell constraint |
| Embed static wget in scratch | Enables HTTP health checks | Adds ~500KB, requires per-image URL | Deferred to Phase 2 |
| Remove HEALTHCHECK entirely | Simplest | Violates C010, no health monitoring | Constraint violation |
| Use wget/curl from wolfi | Shell available | Only for wolfi-based images | Not applicable to scratch |
| Docker-native health check via API | Most accurate | Requires docker socket (violates C017) | Constraint violation |

### Related Standards

| Standard | Clause | Requirement |
|----------|--------|-------------|
| CIS Docker Benchmark | 4.1 | Health checks for containers |
| NIST SP 800-190 | 3.2 | Container monitoring |
| OCI Image Spec | Health | HEALTHCHECK instruction |

### Related Yellow Papers

- YP-OBSERVABILITY-001: Container Observability Theory (ALG-003: Health Check Implementation)

### Related Blue Papers

- BP-IMAGE-REGISTRY-001: Sovereign Hardened Image Registry Architecture

### Related ADRs

- ADR-004: CI Matrix Scaling (batching strategy)

### Related Constraints

- C010: Health check endpoint
- C003: No shell binaries
- C017: No Docker socket

### Implementation Checklist

- [ ] Generate list of all scratch/distroless images with binary names
- [ ] Map each binary to its version flag (`--version`, `-v`, `-V`, `version`)
- [ ] Update all 104 scratch Dockerfiles with exec-form HEALTHCHECK
- [ ] Update all 7 distroless Dockerfiles with exec-form HEALTHCHECK
- [ ] Test each HEALTHCHECK locally
- [ ] Update pre-commit validator to enforce exec-form for scratch/distroless
- [ ] Update CI constraint verification to check HEALTHCHECK format

### Binary-to-Flag Mapping (Partial)

| Binary | Version Flag | Notes |
|--------|-------------|-------|
| nginx | `-v` | Outputs version to stderr, exit 0 |
| traefik | `version` | Subcommand, not flag |
| vault | `version` | Subcommand |
| prometheus | `--version` | Standard flag |
| alertmanager | `--version` | Standard flag |
| consul | `version` | Subcommand |
| etcd | `--version` | Standard flag |
| haproxy | `-v` | Short flag |
| coredns | `-version` | Single dash |
| minio | `--version` | Standard flag |
| trivy | `--version` | Standard flag |
| cosign | `version` | Subcommand |
| syft | `version` | Subcommand |
| grype | `version` | Subcommand |

---

**END OF ADR-001**
