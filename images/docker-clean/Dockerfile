ARG VERSION=0.3.0
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.2.0
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
ARG VERSION=0.3.0
RUN apk add --no-cache ca-certificates docker-cli bash && \
    mkdir -p /app /tmp/cleanup 2>/dev/null || true && \
    printf '#!/bin/bash\nset -euo pipefail\n# docker-clean v%s - Docker cleanup script\n# Based on common Docker cleanup patterns\n\nGRACE_PERIOD_SECONDS="${GRACE_PERIOD_SECONDS:-3600}"\n\ncontainer_ids=$(docker ps -a -q --filter "status=exited" 2>/dev/null || true)\nfor cid in ${container_ids}; do\n    created=$(docker inspect --format "{{.Created}}" "${cid}" 2>/dev/null || echo "")\n    if [ -n "${created}" ]; then\n        echo "Removing exited container: ${cid}"\n        docker rm "${cid}" 2>/dev/null || true\n    fi\ndone\n\ndangling_images=$(docker images -q -f "dangling=true" 2>/dev/null || true)\nif [ -n "${dangling_images}" ]; then\n    echo "Removing dangling images..."\n    docker rmi ${dangling_images} 2>/dev/null || true\nfi\n\necho "Docker cleanup complete."\n' "${VERSION}" > /usr/local/bin/docker-clean && \
    chmod +x /usr/local/bin/docker-clean && \
    addgroup -S -g 2 nogroup >/dev/null || true && \
    adduser -u 65532 -G nogroup -D -h /app -s /bin/false dockerclean 2>/dev/null || true && \
    chown -R 65532:65532 /app /tmp/cleanup 2>/dev/null || true
USER 65532:65532
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9101/metrics || exit 1
ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "docker-clean"]
LABEL org.opencontainers.image.title="docker-clean" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Docker cleanup and pruning tool" \
      org.opencontainers.image.source="https://github.com/zzehring/docker-cleanup" \
      evergreen.image.tier="3" \
      evergreen.image.category="devops" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
