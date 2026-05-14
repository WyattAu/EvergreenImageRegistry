# Blackbox Exporter - Evergreen Hardened Image

## Image Information

| Attribute | Value |
|-----------|-------|
| Image | `blackbox-exporter` |
| Base | `scratch` |
| Binary Source | Official release (Prometheus) |
| Version | v0.26.0 |
| Architecture | amd64, arm64 |
| Size | ~15MB |
| Classification | Tier 1 - Observability/Probing |

## What is Blackbox Exporter?

Blackbox Exporter probes endpoints (HTTP, HTTPS, DNS, TCP, ICMP) and exports metrics for Prometheus.

---

## Constraint Compliance Checklist

| ID | Constraint | Status | Notes |
|----|-----------|--------|-------|
| C001 | Non-root (USER 65532) | PASS | |
| C002 | Read-only filesystem | PASS | Runtime flag |
| C003 | No shell in image | PASS | |
| C004 | No package manager | PASS | |
| C005 | Static binary | PASS | |
| C010 | Health check | PASS | / endpoint |
| C011 | Signal handling | PASS | |
| C012 | No embedded secrets | PASS | |
| C013 | OCI compliant | PASS | |

---

## Usage

```bash
docker run -d \
  --name blackbox-exporter \
  -p 9115:9115 \
  -v /etc/blackbox.yml:/etc/blackbox_exporter/config.yml:ro \
  ghcr.io/evergreen/blackbox-exporter:latest
```

---

## Sources

- Binary: https://github.com/prometheus/blackbox_exporter/releases
- Documentation: https://github.com/prometheus/blackbox_exporter

---

**END OF README**
