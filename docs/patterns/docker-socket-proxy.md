# Docker Socket Proxy Pattern

A security architecture for exposing Docker API access to containers without granting direct socket access.

---

## Problem

Many containers need Docker API access — watchdogs (watchtower), CI runners (forgejo-runners, woodpecker), monitoring
agents (cAdvisor). Mounting `/var/run/docker.sock` directly gives full root-level control over the Docker daemon, which
is a critical security risk:

- A compromised container can spawn privileged containers
- Can read environment variables (secrets) from all containers
- Can modify network and volume configurations
- Can execute arbitrary commands in any running container

## Solution

Interpose an HAProxy-based proxy between the Docker socket and consumer containers. The proxy exposes a filtered HTTP
API on port 2375 and enforces ACLs that restrict which Docker API endpoints are accessible.

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    Docker Host                           │
│                                                          │
│  ┌──────────────┐       ┌────────────────────────────┐  │
│  │  docker.sock  │◄──────│  docker-socket-proxy       │  │
│  │  (unix socket)│       │  (haproxy + ACLs)          │  │
│  └──────────────┘       │  Port 2375 (HTTP)           │  │
│                         └────────────┬───────────────┘  │
│                                      │                  │
│                    ┌─────────────────┼───────────────┐  │
│                    │                 │               │  │
│           ┌────────▼──────┐ ┌───────▼──────┐ ┌─────▼──┐│
│           │  watchtower   │ │ forgejo-     │ │ cAdvisor││
│           │               │ │ runners      │ │         ││
│           │  CONTAINERS=1 │ │ CONTAINERS=1 │ │ CONT=1  ││
│           │  IMAGES=1     │ │ IMAGES=1     │ │ IMAGES=1││
│           │  EXEC=0       │ │ NETWORKS=1   │ │ EXEC=0  ││
│           │  VOLUMES=0    │ │ VOLUMES=1    │ │ VOL=0   ││
│           └───────────────┘ └──────────────┘ └─────────┘│
└──────────────────────────────────────────────────────────┘
```

## ACL Environment Variables

| Variable     | Controls                                              | Default |
| ------------ | ----------------------------------------------------- | ------- |
| `CONTAINERS` | List, inspect, create, stop, start, remove containers | 0       |
| `IMAGES`     | List, inspect, pull, build, remove images             | 0       |
| `NETWORKS`   | List, inspect, create, connect, disconnect networks   | 0       |
| `VOLUMES`    | List, inspect, create, remove volumes                 | 0       |
| `EXEC`       | Create and start exec instances in containers         | 0       |
| `EVENTS`     | Stream Docker daemon events                           | 0       |
| `INFO`       | Access Docker system info                             | 0       |

Set to `1` to allow, `0` to deny.

## When to Use

| Use Case                     | Required ACLs                                         | Notes                                            |
| ---------------------------- | ----------------------------------------------------- | ------------------------------------------------ |
| Watchtower (auto-updater)    | `CONTAINERS=1`, `IMAGES=1`                            | Needs to pull new images and recreate containers |
| Forgejo/Woodpecker runners   | `CONTAINERS=1`, `IMAGES=1`, `NETWORKS=1`, `VOLUMES=1` | Full build access needed                         |
| Portainer                    | `CONTAINERS=1`, `IMAGES=1`, `NETWORKS=1`, `VOLUMES=1` | Management UI requires broad access              |
| cAdvisor (monitoring)        | `CONTAINERS=1`, `IMAGES=1`                            | Read-only container inspection                   |
| Diun (image update notifier) | `IMAGES=1`                                            | Only needs to check for new tags                 |

## When NOT to Use

- **Single-user development environments** — direct socket mount is simpler
- **Containers that need `EXEC` access** — the proxy cannot fully replicate `docker exec` semantics
- **Performance-critical workloads** — the HTTP proxy adds ~1ms latency per API call

## Implementation with Evergreen

```yaml
services:
  docker-socket-proxy:
    image: ghcr.io/wyattau/evergreenimageregistry/docker-socket-proxy:v0.4.2
    container_name: docker-socket-proxy
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    ports:
      - '127.0.0.1:2375:2375'
    environment:
      CONTAINERS: 1
      IMAGES: 1
      NETWORKS: 0
      VOLUMES: 0
      EXEC: 0
      EVENTS: 0
      INFO: 1
    cap_drop:
      - ALL
    cap_add:
      - CHOWN
      - DAC_OVERRIDE
      - SETGID
      - SETUID
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
      - /run
    restart: unless-stopped
    healthcheck:
      test: ['CMD', '/usr/local/bin/shim', 'healthcheck', '--tcp', '127.0.0.1:2375']
      interval: 10s
      timeout: 5s
      start_period: 5s
      retries: 3

  watchtower:
    image: ghcr.io/wyattau/evergreenimageregistry/watchtower:latest
    environment:
      DOCKER_HOST: tcp://docker-socket-proxy:2375
      WATCHTOWER_POLL_INTERVAL: '300'
    depends_on:
      docker-socket-proxy:
        condition: service_healthy
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
    restart: unless-stopped
```

## Security Hardening Checklist

- [ ] Socket mounted **read-only** (`:ro`)
- [ ] Proxy runs as **non-root** (UID 65532)
- [ ] `cap_drop: ALL` on proxy container
- [ ] `read_only: true` on proxy container
- [ ] `no-new-privileges: true` on proxy container
- [ ] Port 2375 bound to `127.0.0.1` only (not `0.0.0.0`)
- [ ] ACLs set to minimum required permissions
- [ ] Health check configured for automatic recovery
- [ ] Consumer containers use `depends_on` with health condition

## Security Benefits

| Benefit                    | Description                                                      |
| -------------------------- | ---------------------------------------------------------------- |
| **Least-privilege**        | Each consumer gets only the API endpoints it needs               |
| **Blast radius reduction** | Compromised container cannot EXEC into others or modify volumes  |
| **Audit trail**            | HAProxy logs all API requests                                    |
| **Defense-in-depth**       | Combines with non-root, read-only, cap-drop for layered security |
| **No shell required**      | Proxy image uses distroless/wolfi-base with no shell             |

## Lessons Learned (from SIS)

1. **HAProxy version changes can break config templates** — when wolfi shipped HAProxy 3.3.x, the environment variable
   resolution syntax changed. Pin the HAProxy version or test upgrades carefully.
2. **Consumer containers must use `DOCKER_HOST`** — not all images respect `DOCKER_HOST`. Test before deploying.
3. **Health checks require the health-shim** — distroless images cannot run `curl` for health checks. Use the Evergreen
   health-shim binary.
4. **Port binding matters** — binding to `0.0.0.0:2375` exposes the Docker API to the network. Always bind to
   `127.0.0.1`.

## References

- [Tecnativa/docker-socket-proxy](https://github.com/tecnativa/docker-socket-proxy) — upstream project
- [Docker API Security](https://docs.docker.com/engine/security/) — Docker daemon security model
- [Evergreen docker-socket-proxy image](../../images/docker-socket-proxy/) — hardened implementation
