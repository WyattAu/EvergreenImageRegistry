# Etcd

etcd - distributed reliable key-value store

| Attribute | Value |
|-----------|-------|
| Version | 3.6.10 |
| Tier | 1 |
| Base Image | scratch |
| Architecture | multi-arch |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/etcd:3.6.10
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

### Etcd Data Directory

Etcd requires a writable data directory. Mount a volume:

```bash
docker run -d -p 2379:2379 \
  -v /path/to/data:/data \
  ghcr.io/wyattau/evergreenimageregistry/etcd:latest \
  --data-dir /data
```
