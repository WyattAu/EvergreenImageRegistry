# VictoriaLogs - Evergreen Hardened Image

## Image Information

| Attribute | Value |
|-----------|-------|
| Image | `victoria-logs` |
| Base | `scratch` |
| Binary Source | Official release (VictoriaMetrics) |
| Version | v1.50.0 |
| Architecture | amd64 |
| Size | ~20MB |
| Classification | Tier 1 - Observability/Logging |

## What is VictoriaLogs?

VictoriaLogs is a cost-effective logs storage solution by VictoriaMetrics, designed for high-volume log ingestion and query.

---

## Constraint Compliance Checklist

| ID | Constraint | Status | Notes |
|----|-----------|--------|-------|
| C001 | Non-root (USER 65532) | PASS | |
| C002 | Read-only filesystem | PASS | Runtime flag |
| C003 | No shell in image | PASS | |
| C004 | No package manager | PASS | |
| C005 | Static binary | PASS | |
| C010 | Health check | PASS | /health endpoint |
| C011 | Signal handling | PASS | |
| C012 | No embedded secrets | PASS | |
| C013 | OCI compliant | PASS | |

---

## Usage

```bash
docker run -d \
  --name victoria-logs \
  -p 9428:9428 \
  -v /var/lib/victoria-logs:/var/lib/victoria-logs \
  ghcr.io/evergreen/victoria-logs:latest
```

---

## Sources

- Binary: https://github.com/VictoriaMetrics/VictoriaLogs/releases
- Documentation: https://docs.victoriametrics.com/victorialogs/

---

**END OF README**
