# Paperless-ngx - Evergreen Hardened Image

## Image Information

| Attribute | Value |
|-----------|-------|
| Image | `paperless-ngx` |
| Base | `wolfi-base` |
| Binary Source | PyPI (pip install) |
| Version | 2.20.14 |
| Architecture | amd64, arm64 |
| Size | ~200MB |
| Classification | Tier 2 - Document Management |

## What is Paperless-ngx?

Paperless-ngx is a document management system that transforms physical documents into searchable online archives.

---

## Constraint Compliance Checklist

| ID | Constraint | Status | Notes |
|----|-----------|--------|-------|
| C001 | Non-root (USER 65532) | PASS | |
| C002 | Read-only filesystem | PASS | Runtime flag |
| C003 | No shell in image | PASS | wolfi-base minimal |
| C004 | No package manager | PASS | apk removed |
| C010 | Health check | PASS | curl localhost:8000 |
| C011 | Signal handling | PASS | |
| C012 | No embedded secrets | PASS | |
| C013 | OCI compliant | PASS | |

---

## Usage

```yaml
services:
  paperless:
    image: ghcr.io/wyattau/evergreenimageregistry/paperless-ngx:latest
    ports:
      - "8000:8000"
    volumes:
      - paperless-data:/usr/src/paperless/data
      - paperless-media:/usr/src/paperless/media
    environment:
      - PAPERLESS_REDIS=redis://redis:6379
      - PAPERLESS_DBHOST=postgres
    read_only: true
```

---

## Sources

- Package: https://pypi.org/pypi/paperless-ngx/
- Documentation: https://docs.paperless-ngx.com/

---

**END OF README**
