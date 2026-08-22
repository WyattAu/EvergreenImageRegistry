# Feedbin

**WIP** - Ruby on Rails app with 12+ containers. Too complex for single Dockerfile.

| Attribute | Value |
|-----------|-------|
| Version | 0.1.0 |
| Tier | 3 |
| Status | WIP |
| Base Image | cgr.dev/chainguard/wolfi-base:latest |
| Architecture | amd64 |
| Health Check | exec |

## Why WIP

Feedbin is a Ruby on Rails application composed of 12+ containers including:
- PostgreSQL
- Redis
- Sidekiq workers
- Elasticsearch
- Multiple Rails app instances

A single Dockerfile cannot capture this architecture. A docker-compose.yml or Helm chart would be needed.

## Security

- Non-root by default
- Digest-pinned base images
