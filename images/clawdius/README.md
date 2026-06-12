# Clawdius

AI coding assistant with formal verification, multi-provider LLM, and 9 messaging adapters

| Attribute | Value |
|-----------|-------|
| Version | 1.0.0 |
| Tier | critical |
| Base Image | scratch |
| Architecture | amd64 |
| Health Check | exec (TCP :8080) |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Quick Start

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/clawdius:1.0.0

docker run -d \
  --name clawdius \
  -p 8080:8080 \
  -v clawdius-data:/app/data \
  -v clawdius-config:/app/config \
  ghcr.io/wyattau/evergreenimageregistry/clawdius:1.0.0
```

## Configuration

| Environment Variable | Default | Description |
|----------------------|---------|-------------|
| `CLAWDIUS_CONFIG` | `/app/config/config.toml` | Config file path |
| `CLAWDIUS_DATA_DIR` | `/app/data` | Data directory |
| `CLAWDIUS_LOG_DIR` | `/app/logs` | Log directory |
| `RUST_LOG` | `info` | Log level (trace, debug, info, warn, error) |

## Security Features

- Non-root container (UID 65532)
- Scratch base image (no shell, no package manager)
- CAP_DROP_ALL enforced
- No-new-privileges enabled
- Seccomp runtime-default profile
- Static musl-linked binary
- HEALTHCHECK enabled via TCP probe on port 8080
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images

## Health Check

TCP health check on port 8080 via the Evergreen health shim:

- Interval: 30s
- Timeout: 10s
- Start period: 10s
- Retries: 3

## Usage Examples

With a config file:

```bash
docker run -d \
  -p 8080:8080 \
  -v /path/to/config.toml:/app/config/config.toml:ro \
  -v clawdius-data:/app/data \
  ghcr.io/wyattau/evergreenimageregistry/clawdius:1.0.0
```

With environment overrides:

```bash
docker run -d \
  -p 8080:8080 \
  -e RUST_LOG=debug \
  -e CLAWDIUS_DATA_DIR=/app/data \
  -v clawdius-data:/app/data \
  ghcr.io/wyattau/evergreenimageregistry/clawdius:1.0.0
```
