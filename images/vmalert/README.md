# vmalert - Evergreen Hardened Image

## Image Information

| Attribute | Value |
|-----------|-------|
| Image | `vmalert` |
| Base | `scratch` |
| Binary Source | Official release (VictoriaMetrics) |
| Version | v1.142.0 |
| Architecture | amd64, arm64 |
| Size | ~20MB |
| Classification | Tier 1 - Observability/Alerting |

## What is vmalert?

vmalert is the alerting engine for VictoriaMetrics, evaluating alerting and recording rules against VictoriaMetrics data.

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
  --name vmalert \
  -p 8880:8880 \
  ghcr.io/evergreen/vmalert:latest \
  -prometheus.url=http://victoriametrics:8428 \
  -rule.file=/etc/alerts/*.yaml
```

---

## Sources

- Binary: https://github.com/VictoriaMetrics/VictoriaMetrics/releases
- Documentation: https://docs.victoriametrics.com/vmalert/

---

**END OF README**
