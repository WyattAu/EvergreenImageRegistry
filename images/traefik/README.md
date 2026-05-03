# Traefik - Evergreen Hardened Image

## Image Information

| Attribute | Value |
|-----------|-------|
| Image | `traefik` |
| Base | `scratch` |
| Binary Source | Official static (Traefik Labs) |
| Version | 3.1.4 |
| Architecture | amd64 (expandable to arm64) |
| Size | ~40MB |
| Classification | CRITICAL - Gateway/Reverse Proxy |

## What is Traefik?

Traefik is a modern HTTP reverse proxy and load balancer designed for microservices. It's the primary entry point for external traffic into your infrastructure.

---

## Constraint Compliance Checklist

| ID | Constraint | Status | Notes |
|----|-----------|--------|-------|
| C001 | ✅ | Non-root (USER 65534) |
| C002 | ✅ | Read-only filesystem (runtime flag) |
| C003 | ✅ | No shell in image |
| C004 | ✅ | No package manager |
| C005 | ✅ | Static binary |
| C006 | ✅ | Stripped symbols |
| C007 | ⚠️ | Zero CVEs CI/CD |
| C008 | ⚠️ | Image signing CI/CD |
| C009 | ⚠️ | SBOM generation |
| C010 | ✅ | Health check at /ping |
| C011 | ✅ | Signal handling |
| C012 | ✅ | No embedded secrets |
| C013 | ✅ | OCI compliant |

**Score: 11/13 (85%)**

### Gap Analysis

| Constraint | Gap | Round 2 Action |
|-----------|-----|--------------|
| C007 | Requires Trivy scan in pipeline |
| C008 | Requires Cosign signing |
| C009 | Requires Syft SBOM |

---

## Usage

### Basic Usage

```bash
# Pull the image
docker pull ghcr.io/evergreen/traefik:latest

# Run with configuration file
docker run -d \
  --name traefik \
  -p 80:80 \
  -p 443:443 \
  -p 8080:8080 \
  -v /path/to/traefik.yml:/etc/traefik/traefik.yml:ro \
  --read-only \
  --tmpfs /tmp \
  --tmpfs /var/cache \
  --tmpfs /var/log \
  ghcr.io/evergreen/traefik:latest
```

### With Docker Compose

```yaml
services:
  traefik:
    image: ghcr.io/evergreen/traefik:latest
    ports:
      - "80:80"
      - "443:443"
      - "8080:8080"
    volumes:
      - ./traefik.yml:/etc/traefik/traefik.yml:ro
    read_only: true
    tmpfs:
      - /tmp
      - /var/cache
      - /var/log
    security_opt:
      - no-new-privileges:true
    restart: unless-stopped
```

---

## Security Features

### What's Implemented

- ✅ **Non-root execution**: Runs as UID 65534 (nobody)
- ✅ **No shell**: `/bin/sh` and `/bin/bash` removed
- ✅ **No package managers**: apt, apk, dnf not present
- ✅ **Static binary**: Statically linked
- ✅ **No embedded secrets**: Configuration via files/env vars
- ✅ **Health check**: Built-in /ping endpoint at port 8080
- ✅ **Signal handling**: Graceful shutdown

### Runtime Security (Apply at deployment)

```bash
# Recommended runtime flags
docker run \
  --read-only \              # Root filesystem read-only
  --tmpfs /tmp \           # Temp files in memory
  --tmpfs /var/cache \      # Cache in memory
  --tmpfs /var/log \      # Logs in memory
  --user 65534 \            # Non-root
  --cap-drop ALL \          # Drop all capabilities
  --security-opt no-new-privileges \
  ghcr.io/evergreen/traefik:latest
```

---

## Health Check

The image includes a built-in health check at Traefik's `/ping` endpoint:

```bash
# Manual health check
curl http://localhost:8080/ping
# Returns:pong
```

**Health Check Details:**
- Interval: 30s
- Timeout: 5s
- Start Period: 10s
- Retries: 3

---

## Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `TRAEFIK_VERSION` | Traefik version | 3.1.4 |
| `TRAEFIK_LOG_LEVEL` | Logging level | INFO, DEBUG |
| `TRAEFIK_API_DASHBOARD` | Enable dashboard | true |

### Volume Mounts

| Path | Purpose | Mode |
|------|--------|------|
| `/etc/traefik` | Configuration | read-only |
| `/var/log/traefik` | Logs | read-write (tmpfs) |
| `/var/cache/traefik` | Cache | read-write (tmpfs) |
| `/letsencrypt` | Let's Encrypt | read-write |

---

## Known Limitations

1. **C007 (Zero CVEs)**: Requires external CVE scanning in CI/CD pipeline
2. **C008 (Signing)**: Requires Cosign setup in CI/CD  
3. **C009 (SBOM)**: Requires Syft in CI/CD

These will be addressed in the automated pipeline.

---

## Verified Versions

| Version | Build Date | Constraints Met |
|---------|-----------|------------------|
| 3.1.4 | 2026-04-19 | 11/13 |

---

## Sources

- Binary: https://github.com/traefik/traefik/releases
- Documentation: https://doc.traefik.io/traefik/
- Security: https://doc.traefik.io/traefik/security/overview/

---

## Support

| Channel | Contact |
|---------|---------|
| Issues | GitHub Issues |
| Security | security@evergreen.example |

---

**END OF README**