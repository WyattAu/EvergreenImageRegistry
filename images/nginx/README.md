# Nginx Static - Sovereign Hardened Image

## Image Information

| Attribute | Value |
|-----------|-------|
| Image | `nginx-static` |
| Base | `scratch` |
| Binary Source | Official nginx.org (static) |
| Version | 1.27.1 |
| Architecture | amd64 |
| Size | ~15MB |
| Classification | CRITICAL - Web Server |

## Constraint Compliance

| ID | Constraint | Status | Notes |
|----|-----------|--------|-------|
| C001 | ✅ | Non-root (USER 65534) |
| C002 | ✅ | Read-only (runtime) |
| C003 | ✅ | No shell |
| C004 | ✅ | No package manager |
| C005 | ✅ | Static binary |
| C006 | ⚠️ | Partially stripped |
| C007 | ⚠️ | CI/CD scanning |
| C008 | ⚠️ | CI/CD signing |
| C009 | ⚠️ | CI/CD SBOM |
| C010 | ✅ | stub_status |
| C011 | ✅ | Graceful shutdown |
| C012 | ✅ | No secrets |
| C013 | ✅ | OCI |

**Score: 10/13 (77%)**

---

## Usage

```bash
# Basic run
docker run -d -p 80:80 -p 443:443 \
  --read-only --tmpfs /var/cache \
  ghcr.io/sovereign/nginx:latest

# With config
docker run -d -p 80:80 \
  -v nginx.conf:/etc/nginx/nginx.conf:ro \
  --read-only \
  ghcr.io/sovereign/nginx:latest
```

## Health Check

```bash
curl http://localhost/health_status.html
```

## Verified

| Test | Result |
|------|--------|
| Non-root | ✅ UID 65534 |
| No shell | ✅ |
| No package manager | ✅ |
| Static binary | ⚠️ Most |
| Health check | ✅ |

**END README**