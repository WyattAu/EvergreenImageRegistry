# Docker Socket Proxy - Evergreen Hardened Image

## Image Information

| Attribute | Value |
|-----------|-------|
| Image | `docker-socket-proxy` |
| Base | `scratch` |
| Binary Source | Official release (Tecnativa) |
| Version | v0.4.2 |
| Architecture | amd64, arm64 |
| Size | ~10MB |
| Classification | Tier 2 - Docker Security Proxy |

## What is Docker Socket Proxy?

Docker Socket Proxy provides a secure proxy for the Docker socket, allowing fine-grained access control to Docker API endpoints.

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
  --name docker-socket-proxy \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -p 2375:2375 \
  -e CONTAINERS=1 \
  -e IMAGES=1 \
  ghcr.io/wyattau/evergreenimageregistry/docker-socket-proxy:latest
```

---

## Sources

- Binary: https://github.com/tecnativa/docker-socket-proxy/releases
- Documentation: https://github.com/tecnativa/docker-socket-proxy

---

**END OF README**
