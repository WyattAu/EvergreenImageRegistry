# Nginx Static - Evergreen Hardened Image

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
| C001 | PASS | Non-root (USER 65532) |
| C002 | PASS | Read-only (runtime) |
| C003 | PASS | No shell |
| C004 | PASS | No package manager |
| C005 | PASS | Static binary |
| C006 | WARN | Partially stripped |
| C007 | WARN | CI/CD scanning |
| C008 | WARN | CI/CD signing |
| C009 | WARN | CI/CD SBOM |
| C010 | PASS | stub_status |
| C011 | PASS | Graceful shutdown |
| C012 | PASS | No secrets |
| C013 | PASS | OCI |

**Score: 10/13 (77%)**

---

## Usage

```bash
# Basic run
docker run -d -p 80:80 -p 443:443 \
  --read-only --tmpfs /var/cache \
  ghcr.io/evergreen/nginx:latest

# With config
docker run -d -p 80:80 \
  -v nginx.conf:/etc/nginx/nginx.conf:ro \
  --read-only \
  ghcr.io/evergreen/nginx:latest
```

## Health Check

```bash
curl http://localhost/health_status.html
```

## Verified

| Test | Result |
|------|--------|
| Non-root | PASS UID 65532 |
| No shell | PASS |
| No package manager | PASS |
| Static binary | WARN Most |
| Health check | PASS |

**END README**