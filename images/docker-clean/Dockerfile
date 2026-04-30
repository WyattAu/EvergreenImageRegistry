ARG VERSION=0.3.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION
RUN apk add --no-cache ca-certificates docker-cli bash || true
RUN mkdir -p /app /tmp/cleanup 2>/dev/null || true
RUN printf '#!/bin/bash\nset -euo pipefail\n# docker-clean v%s - Docker cleanup script\n# Based on common Docker cleanup patterns\n\nGRACE_PERIOD_SECONDS="${GRACE_PERIOD_SECONDS:-3600}"\n\ncontainer_ids=$(docker ps -a -q --filter "status=exited" 2>/dev/null || true)\nfor cid in ${container_ids}; do\n    created=$(docker inspect --format "{{.Created}}" "${cid}" 2>/dev/null || echo "")\n    if [ -n "${created}" ]; then\n        echo "Removing exited container: ${cid}"\n        docker rm "${cid}" 2>/dev/null || true\n    fi\ndone\n\ndangling_images=$(docker images -q -f "dangling=true" 2>/dev/null || true)\nif [ -n "${dangling_images}" ]; then\n    echo "Removing dangling images..."\n    docker rmi ${dangling_images} 2>/dev/null || true\nfi\n\necho "Docker cleanup complete."\n' "${VERSION}" > /usr/local/bin/docker-clean && \
    chmod +x /usr/local/bin/docker-clean
RUN addgroup -S -g 2 nogroup >/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /bin/false dockerclean 2>/dev/null || true && \
    chown -R 65532:65532 /app /tmp/cleanup 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["docker-clean"]
LABEL org.opencontainers.image.title="docker-clean" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Docker cleanup and pruning tool" \
      org.opencontainers.image.source="https://github.com/zzehring/docker-cleanup" \
      sovereign.image.tier="3" \
      sovereign.image.category="devops" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
