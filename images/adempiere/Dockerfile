ARG VERSION=3.9.4
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=3.9.4
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/adempiere/adempiere/releases/download/${VERSION}/Adempiere_394LTS.tar.gz" \
    -o /Adempiere.tar.gz
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache ca-certificates curl
COPY --from=downloader /Adempiere.tar.gz /opt/adempiere.tar.gz
RUN mkdir -p /app /var/log/adempiere && \
    chown -R 65532:65532 /app /var/log/adempiere /opt/adempiere.tar.gz
USER 65532:65532
WORKDIR /app
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:8080/ || exit 1
ENTRYPOINT ["java", "-jar", "/opt/adempiere/Adempiere"]
LABEL org.opencontainers.image.title="adempiere" \
      org.opencontainers.image.description="adempiere container image" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Adempiere" \
      org.opencontainers.image.source="https://github.com/adempiere/adempiere" \
      evergreen.image.tier="2" \
      evergreen.image.category="crm-erp" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="30s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="60000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
