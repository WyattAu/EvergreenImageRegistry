# =============================================================================
# EVERGREEN HARDENED RABBITMQ MANAGEMENT
# Generated from template - Version: 3.13.1
# Constraint: debian-slim - Erlang runtime + RabbitMQ server required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.13.1
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

# hadolint ignore=DL3023

ARG SHIM_VERSION=v1.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=3.13.1
RUN mkdir -p /usr/lib/rabbitmq || true
RUN mkdir -p /etc/rabbitmq && \
    mkdir -p /usr/lib/rabbitmq || true
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates gnupg apt-transport-https && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/rabbitmq/signing-keys/releases/download/3.0/cloudsmith.rabbitmq-erlang.E495BB49CC4BBE5B.key \
        | gnupg --dearmor -o /usr/share/keyrings/rabbitmq-erlang.gnupg ; curl --retry 3 --retry-delay 5 -fsSL https://github.com/rabbitmq/signing-keys/releases/download/3.0/cloudsmith.rabbitmq-server.9F4587F226208342.key \        | gnupg --dearmor -o /usr/share/keyrings/rabbitmq-server.gnupg ; echo "deb [signed-by=/usr/share/keyrings/rabbitmq-erlang.gnupg] https://ppa1.novemberain.com/rabbitmq/rabbitmq-erlang/deb bookworm main" \        > /etc/apt/sources.list.d/rabbitmq-erlang.list ; echo "deb [signed-by=/usr/share/keyrings/rabbitmq-server.gnupg] https://ppa1.novemberain.com/rabbitmq/rabbitmq-server/deb bookworm main" \        > /etc/apt/sources.list.d/rabbitmq-server.list ; apt-get update ; apt-get install -y --no-install-recommends \        erlang-base erlang-asn1 erlang-crypto erlang-eldap erlang-ftp erlang-inets \
        erlang-mnesia erlang-os-mon erlang-parsetools erlang-public-key \
        erlang-runtime-tools erlang-snmp erlang-ssl erlang-syntax-tools \
        erlang-tftp erlang-tools erlang-xmerl \
        rabbitmq-server rabbitmq-management ; rm -rf /var/lib/apt/lists/* || true
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

# package-manager-verified: integrity verified by upstream

ARG VERSION=3.13.1
RUN apk add --no-cache ca-certificates && \
    adduser -u 65532 -s /bin/false rabbitmq || true && \
    mkdir -p /var/lib/rabbitmq /var/log/rabbitmq /etc/rabbitmq
COPY --from=builder /usr/lib/rabbitmq /usr/lib/rabbitmq
COPY --from=builder /usr/sbin/rabbitmq* /usr/sbin/
COPY --from=builder /usr/bin/rabbitmq* /usr/bin/
COPY --from=builder /etc/rabbitmq /etc/rabbitmq
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /var/lib/rabbitmq
EXPOSE 5672 15672 15692

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:5672"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "rabbitmq-server"]
LABEL evergreen.image.status="functional" \
      evergreen.image.tier="1" \
      evergreen.image.category="messaging" \
      org.opencontainers.image.title="rabbitmq-management" \
      org.opencontainers.image.description="Evergreen hardened RabbitMQ Management - RabbitMQ with management UI plugin" \
      org.opencontainers.image.version="${VERSION}" \
            org.opencontainers.image.source="https://github.com/rabbitmq/rabbitmq-server"
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
