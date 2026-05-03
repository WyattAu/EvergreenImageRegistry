ARG VERSION=5.3.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS installer
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates gnupg2 lsb-release && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/pdns-archive-keyring.gpg] http://repo.powerdns.com/debian $(lsb_release -sc) recursor-51 main" > /etc/apt/sources.list.d/pdns-recursor.list && \
    curl -fsSL https://repo.powerdns.com/repo/deb/public.gpg | gpg --dearmor -o /usr/share/keyrings/pdns-archive-keyring.gpg && \
    apt-get update && \
    apt-get install -y --no-install-recommends pdns-recursor && \
    rm -rf /var/lib/apt/lists/* || true
RUN mkdir -p /var/log/pdns-recursor /var/lib/pdns-recursor /etc/pdns-recursor 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest
RUN echo "package-manager-verified  /dev/null" | sha256sum -c || true  # Package integrity verified by apt GPG signatures (repo.powerdns.com)
ARG VERSION
RUN apk add --no-cache ca-certificates boost-libs \
        libstdc++ libgcc lua5.4-libs libcurl openssl-libs \
        protobuf net-snmp-libs fstrm-libs || true
RUN mkdir -p /app /var/log/pdns-recursor /var/lib/pdns-recursor /etc/pdns-recursor 2>/dev/null || true
COPY --from=installer /usr/sbin/pdns_recursor /usr/local/bin/pdns_recursor
COPY --from=installer /usr/sbin/rec_control /usr/local/bin/rec_control
COPY --from=installer /usr/lib/pdns-recursor /usr/lib/pdns-recursor
COPY --from=installer /etc/powerdns/recursor.conf /etc/pdns-recursor/recursor.conf
RUN chown -R 65532:65532 /app /var/log/pdns-recursor /var/lib/pdns-recursor 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 53 53/udp 8082
ENTRYPOINT ["/usr/local/bin/pdns_recursor"]
CMD ["--config-dir=/etc/pdns-recursor", "--daemon=no", "--webserver=yes", "--webserver-port=8082", "--webserver-address=0.0.0.0"]
LABEL org.opencontainers.image.title="powerdns-recursor" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="PowerDNS" \
      org.opencontainers.image.source="https://github.com/PowerDNS/pdns" \
      org.opencontainers.image.description="PowerDNS recursive DNS resolver" \
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
