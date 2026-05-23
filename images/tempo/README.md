# Tempo - Evergreen Hardened Image

## Image Information

| Attribute | Value |
|-----------|-------|
| Image | `tempo` |
| Base | `scratch` |
| Binary Source | Official release (Grafana) |
| Version | 2.8.0 |
| Architecture | amd64, arm64 |
| Size | ~50MB |
| Classification | Tier 1 - Observability/Tracing |

## What is Tempo?

Tempo is a distributed tracing backend by Grafana, compatible with Jaeger, Zipkin, and OpenTelemetry protocols.

---

## Constraint Compliance Checklist

| ID | Constraint | Status | Notes |
|----|-----------|--------|-------|
| C001 | Non-root (USER 65532) | PASS | |
| C002 | Read-only filesystem | PASS | Runtime flag |
| C003 | No shell in image | PASS | |
| C004 | No package manager | PASS | |
| C005 | Static binary | PASS | |
| C010 | Health check | PASS | /ready endpoint |
| C011 | Signal handling | PASS | |
| C012 | No embedded secrets | PASS | |
| C013 | OCI compliant | PASS | |

---

## Usage

```bash
docker run -d \
  --name tempo \
  -p 3200:3200 \
  -v /etc/tempo.yaml:/etc/tempo.yaml:ro \
  ghcr.io/wyattau/evergreenimageregistry/tempo:latest
```

---

## Sources

- Binary: https://github.com/grafana/tempo/releases
- Documentation: https://grafana.com/docs/tempo/

---

**END OF README**
