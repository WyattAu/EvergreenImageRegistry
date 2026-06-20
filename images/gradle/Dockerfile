ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=8.10.2
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://services.gradle.org/distributions/gradle-8.10.2-bin.zip" -o /gradle.zip && \
    echo "31c55713e40233a8303827ceb42ca48a47267a0ad4bab9177123121e71524c26  /gradle.zip" | sha256sum -c ; \
    unzip -q /gradle.zip -d /opt/ && rm -f /gradle.zip && ln -sf /opt/gradle-8.10.2/bin/gradle /usr/local/bin/gradle && { echo "Binary not available - download failed" >&2; exit 1; }
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/gradle /var/cache/gradle /home/gradle 2>/dev/null || true


ARG SHIM_VERSION=v1.2.0
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim

RUN apk add --no-cache ca-certificates
COPY --from=downloader /opt/gradle-8.10.2 /opt/gradle-8.10.2
COPY --from=downloader /usr/local/bin/gradle /usr/local/bin/gradle
COPY --from=builder /app /app
COPY --from=builder /var/log/gradle /var/log/gradle
COPY --from=builder /var/cache/gradle /var/cache/gradle
COPY --from=builder /home/gradle /home/gradle
RUN adduser -u 65532 -D gradle 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENV HOME=/app
ENV GRADLE_HOME=/opt/gradle-8.10.2

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9101/metrics || exit 1
ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "gradle"]
LABEL org.opencontainers.image.title="gradle" \
      org.opencontainers.image.version="8.10.2" \
      org.opencontainers.image.vendor="Gradle" \
      org.opencontainers.image.description="Evergreen hardened gradle - Java build tool" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="30s" \
            org.opencontainers.image.source="https://github.com/gradle/gradle"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
