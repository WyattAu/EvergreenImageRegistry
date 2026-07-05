# Watchtower - Evergreen Hardened Image

## Image Information

| Attribute | Value |
|-----------|-------|
| Image | `watchtower` |
| Base | `scratch` |
| Binary Source | Official static (containrrr) |
| Version | 1.7.1 |
| Architecture | amd64 |
| Size | ~10MB |
| Classification | Tier 2 - Container Lifecycle |

## What is Watchtower?

Watchtower automatically updates running Docker containers when new images are available.

---

## Constraint Compliance Checklist

| ID | Constraint | Status | Notes |
|----|-----------|--------|-------|
| C001 | Non-root (USER 65532) | PASS | |
| C002 | Read-only filesystem | PASS | Runtime flag |
| C003 | No shell in image | PASS | |
| C004 | No package manager | PASS | |
| C005 | Static binary | PASS | |
| C010 | Health check | PASS | NONE |
| C011 | Signal handling | PASS | |
| C012 | No embedded secrets | PASS | |
| C013 | OCI compliant | PASS | |

---

## Usage

```bash
docker run -d \
  --name watchtower \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  watchtower --interval 300
```

---

## Sources

- Binary: https://github.com/containrrr/watchtower/releases
- Documentation: https://containrrr.dev/watchtower/

---

**END OF README**
