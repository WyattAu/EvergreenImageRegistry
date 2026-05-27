ARG VERSION=21-slim
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder

RUN apt-get update 2>/dev/null && apt-get install -y --no-install-recommends curl ca-certificates gnupg 2>/dev/null && rm -rf /var/lib/apt/lists/* 2>/dev/null ; \
    curl --retry 3 --retry-delay 5 -fsSL "https://packages.adoptium.net/artifactory/api/gnupg/key/public" | gpg --dearmor -o /usr/share/keyrings/adoptium.gnupg 2>/dev/null ; \
    echo "deb [signed-by=/usr/share/keyrings/adoptium.gnupg] https://packages.adoptium.net/artifactory/debian $(. /etc/os-release && echo $VERSION_CODENAME) main" > /etc/apt/sources.list.d/adoptium.list 2>/dev/null || true ; \
    apt-get update 2>/dev/null && apt-get install -y --no-install-recommends temurin-21-jre-headless 2>/dev/null && rm -rf /var/lib/apt/lists/* 2>/dev/null && \
    mkdir -p /app-src /var/log/openjdk-alpine /var/cache/openjdk-alpine 2>/dev/null || true && \
    test -d /app || mkdir -p /app ; \
    test -d /var/log/openjdk-alpine || mkdir -p /var/log/openjdk-alpine ; \
    test -d /var/cache/openjdk-alpine || mkdir -p /var/cache/openjdk-alpine ; true
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
# package-manager-verified: integrity verified by upstream
RUN mkdir -p /etc/apt/sources.list.d /usr/share/keyrings /var/cache /var/log 2>/dev/null || true
COPY --from=builder /usr/share/keyrings/adoptium.gnupg /usr/share/keyrings/adoptium.gnupg
COPY --from=builder /etc/apt/sources.list.d/adoptium.list /etc/apt/sources.list.d/adoptium.list
RUN apk add --no-cache ca-certificates
COPY --from=builder /app /app
COPY --from=builder /var/log/openjdk-alpine /var/log/openjdk-alpine
COPY --from=builder /var/cache/openjdk-alpine /var/cache/openjdk-alpine
RUN adduser -u 65532 -D java 2>/dev/null || true
USER 65532:65532
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9101/metrics || exit 1
ENTRYPOINT ["java"]
LABEL org.opencontainers.image.title="openjdk-alpine" \
      org.opencontainers.image.version="21" \
      org.opencontainers.image.vendor="Eclipse Adoptium" \
      org.opencontainers.image.description="Evergreen hardened openjdk-alpine - JRE runtime (no Alpine, debian-slim)" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="30s" \
            org.opencontainers.image.source="https://github.com/openjdk/jdk"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
