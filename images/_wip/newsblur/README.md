# Newsblur

**WIP** - Django/Python app requiring PostgreSQL, Redis, MongoDB. Too complex for single Dockerfile.

| Attribute | Value |
|-----------|-------|
| Version | 0.1.0 |
| Tier | 3 |
| Status | WIP |
| Base Image | cgr.dev/chainguard/wolfi-base:latest |
| Architecture | amd64 |
| Health Check | exec |

## Why WIP

NewsBlur is a full-stack Django application requiring multiple external services:
- PostgreSQL (database)
- Redis (task queue/caching)
- MongoDB (data store)

A single Dockerfile cannot capture this architecture. A docker-compose.yml or Helm chart would be needed.

## Security

- Non-root by default
- Digest-pinned base images
