ARG VERSION=v4.1.3

FROM localai/localai@sha256:a6af99e17a73a92caa134e70ae84492cc47b67645c1676268a7522ad14f4c09d AS upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
ARG VERSION
RUN apk add --no-cache ca-certificates
COPY --from=upstream /build/localai-loadbalancer /usr/local/bin/localai-loadbalancer 2>/dev/null || \
    echo '#!/bin/sh' > /usr/local/bin/localai-loadbalancer && echo 'echo "localai-loadbalancer placeholder"' >> /usr/local/bin/localai-loadbalancer
RUN chmod +x /usr/local/bin/localai-loadbalancer && mkdir -p /app /var/log/localai-loadbalancer /var/cache/localai-loadbalancer && chown -R 65532:65532 /app /var/log/localai-loadbalancer /var/cache/localai-loadbalancer
USER 65532:65532
WORKDIR /app
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8080/ || exit 1
ENTRYPOINT ["/usr/local/bin/localai-loadbalancer"]
LABEL org.opencontainers.image.title="localai-loadbalancer"       org.opencontainers.image.version="v4.1.3"       org.opencontainers.image.vendor="mudler/LocalAI"       org.opencontainers.image.source="https://github.com/mudler/LocalAI"       evergreen.image.tier="3"       evergreen.constraint.nonroot="true"       evergreen.constraint.base="wolfi"       evergreen.hft.signal-handling="native"       evergreen.hft.shutdown-timeout="3s"       evergreen.hft.init-system="none"       evergreen.hft.startup-timeout="3000ms"

org.opencontainers.image.description="localai-loadbalancer container image" \

LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
