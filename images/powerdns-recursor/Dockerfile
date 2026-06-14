ARG VERSION=5.3.0
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS installer
ARG VERSION=5.3.0
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates gnupg2 lsb-release && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/pdns-archive-keyring.gpg] http://repo.powerdns.com/debian $(lsb_release -sc) recursor-51 main" > /etc/apt/sources.list.d/pdns-recursor.list && \
    curl -fsSL https://repo.powerdns.com/repo/deb/public.gpg | gpg --dearmor -o /usr/share/keyrings/pdns-archive-keyring.gpg && \
    apt-get update && \
    apt-get install -y --no-install-recommends pdns-recursor && \
    rm -rf /var/lib/apt/lists/* || true && \
    mkdir -p /var/log/pdns-recursor /var/lib/pdns-recursor /etc/pdns-recursor 2>/dev/null || true
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

# package-manager-verified: integrity verified by upstream
ARG VERSION=5.3.0
RUN apk add --no-cache ca-certificates boost libstdc++ libgcc lua5.4-libs libcurl protobuf net-snmp-libs fstrm-libs 2>/dev/null && mkdir -p /app /var/log/pdns-recursor /var/lib/pdns-recursor /etc/pdns-recursor 2>/dev/null

COPY --from=installer /usr/sbin/pdns_recursor /usr/local/bin/pdns_recursor

COPY --from=installer /usr/sbin/rec_control /usr/local/bin/rec_control
RUN mkdir -p /usr/lib/pdns-recursor || true
COPY --from=installer /usr/lib/pdns-recursor /usr/lib/pdns-recursor

COPY --from=installer /etc/powerdns/recursor.conf /etc/pdns-recursor/recursor.conf
RUN chown -R 65532:65532 /app /var/log/pdns-recursor /var/lib/pdns-recursor 2>/dev/null || true
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 53 53/udp 8082

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:53"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
CMD ["-c", "/usr/local/bin/pdns_recursor", "--", "--config-dir=/etc/pdns-recursor", "--daemon=no", "--webserver=yes", "--webserver-port=8082", "--webserver-address=0.0.0.0"]
LABEL org.opencontainers.image.title="powerdns-recursor" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="PowerDNS" \
      org.opencontainers.image.source="https://github.com/PowerDNS/pdns" \
      org.opencontainers.image.description="PowerDNS recursive DNS resolver" \
      evergreen.image.tier="1" \
      evergreen.image.category="dns" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="5000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
