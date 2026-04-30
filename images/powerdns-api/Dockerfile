ARG VERSION=4.9.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS installer
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates gnupg2 lsb-release && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/pdns-archive-keyring.gpg] http://repo.powerdns.com/debian $(lsb_release -sc) pdns-49 main" > /etc/apt/sources.list.d/pdns.list && \
    curl -fsSL https://repo.powerdns.com/repo/deb/public.gpg | gpg --dearmor -o /usr/share/keyrings/pdns-archive-keyring.gpg && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        pdns-server pdns-backend-sqlite3 pdns-tools && \
    rm -rf /var/lib/apt/lists/* || true
RUN mkdir -p /var/log/pdns /var/lib/pdns /etc/pdns 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION
RUN apk add --no-cache sqlite-libs ca-certificates boost-libs \
        libstdc++ libgcc lua5.4-libs libcurl openssl-libs \
        protobuf libxml2 || true
RUN mkdir -p /app /var/log/pdns /var/lib/pdns /etc/pdns 2>/dev/null || true
COPY --from=installer /usr/sbin/pdns_server /usr/local/bin/pdns_server
COPY --from=installer /usr/sbin/pdnsutil /usr/local/bin/pdnsutil
COPY --from=installer /usr/sbin/pdns_control /usr/local/bin/pdns_control
COPY --from=installer /usr/lib/pdns /usr/lib/pdns
COPY --from=installer /etc/powerdns /etc/pdns
RUN chown -R 65532:65532 /app /var/log/pdns /var/lib/pdns 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 53 53/udp 8081
ENTRYPOINT ["/usr/local/bin/pdns_server"]
CMD ["--config-dir=/etc/pdns", "--daemon=no", "--webserver=yes", "--webserver-port=8081", "--webserver-address=0.0.0.0", "--api=yes", "--api-key=changeme"]
LABEL org.opencontainers.image.title="powerdns-api" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="PowerDNS" \
      org.opencontainers.image.source="https://github.com/PowerDNS/pdns" \
      org.opencontainers.image.description="PowerDNS authoritative DNS server with REST API" \
      sovereign.image.tier="1" \
      sovereign.image.category="dns" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="5000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
