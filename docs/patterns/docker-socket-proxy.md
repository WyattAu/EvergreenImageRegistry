Many containers need Docker API access; watchdogs (watchtower), CI runners (forgejo-runners, woodpecker), monitoring
- **Single-user development environments**; direct socket mount is simpler
- **Containers that need `EXEC` access**; the proxy cannot fully replicate `docker exec` semantics
- **Performance-critical workloads**; the HTTP proxy adds ~1ms latency per API call
1. **HAProxy version changes can break config templates**; when wolfi shipped HAProxy 3.3.x, the environment variable
2. **Consumer containers must use `DOCKER_HOST`**; not all images respect `DOCKER_HOST`. Test before deploying.
3. **Health checks require the health-shim**; distroless images cannot run `curl` for health checks. Use the Evergreen
4. **Port binding matters**; binding to `0.0.0.0:2375` exposes the Docker API to the network. Always bind to
- [Tecnativa/docker-socket-proxy](https://github.com/tecnativa/docker-socket-proxy); upstream project
- [Docker API Security](https://docs.docker.com/engine/security/); Docker daemon security model
- [Evergreen docker-socket-proxy image](../../images/docker-socket-proxy/); hardened implementation