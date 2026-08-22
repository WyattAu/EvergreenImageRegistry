# Grafana

Grafana - observability dashboard and visualization

| Attribute | Value |
|-----------|-------|
| Version | 12.2.8-security-04 |
| Tier | critical |
| Base Image | cgr.dev/chainguard/wolfi-base:latest |
| Architecture | multi-arch |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/grafana:12.2.8-security-04
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images

## ⚠️ Configuration Required

This image requires a configuration file to start. Without it, the container will exit immediately.

### Quick Start

```bash
# grafana: mount grafana.ini
docker run -d -p 3000:3000 \
  -v /path/to/grafana.ini:/etc/grafana/grafana.ini:ro \
  ghcr.io/wyattau/evergreenimageregistry/grafana:latest

# Example grafana.ini
cat > grafana.ini << 'CFG'
[server]
http_port = 3000
CFG
```

### grafana.ini Reference

| Key | Default | Description |
|-----|---------|-------------|
| `http_port` | `3000` | HTTP listen port |
| `server.root_url` | `%(protocol)s://%(domain)s:%(http_port)s/` | Public URL |
| `security.admin_user` | `admin` | Admin username |
| `security.admin_password` | `admin` | Admin password (change in production!) |
