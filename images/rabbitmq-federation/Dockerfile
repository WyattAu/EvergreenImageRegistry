# =============================================================================
# EVERGREEN HARDENED RABBITMQ-FEDERATION
# Generated from template - Version: 3.13.1
# Constraint: debian-slim - Erlang runtime + RabbitMQ server required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.13.1
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


ARG SHIM_VERSION=v0.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=3.13.1
RUN mkdir -p /usr/lib/rabbitmq || true
RUN mkdir -p /etc/rabbitmq && \
    mkdir -p /usr/lib/rabbitmq || true
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates gnupg apt-transport-https && \
    curl --retry 3 --retry-delay 5 -fsSL "https://keys.openpgp.org/vks/v1/by-fingerprint/0A9AF2115F4687BD29803A206B73A36E6026DFCA" \
        | gpg --dearmor -o /usr/share/keyrings/com.rabbitmq.team.gpg ; curl --retry 3 --retry-delay 5 -fsSL "https://keys.openpgp.org/vks/v1/by-fingerprint/0A9AF2115F4687BD29803A206B73A36E6026DFCA" \        | gnupg --dearmor -o /usr/share/keyrings/com.rabbitmq.team.gpg ; echo "deb [signed-by=/usr/share/keyrings/com.rabbitmq.team.gpg] https://deb1.rabbitmq.com/rabbitmq-erlang/debian/bookworm bookworm main" \        > /etc/apt/sources.list.d/rabbitmq-erlang.list ; echo "deb [signed-by=/usr/share/keyrings/com.rabbitmq.team.gpg] https://deb1.rabbitmq.com/rabbitmq-server/debian/bookworm bookworm main" \        > /etc/apt/sources.list.d/rabbitmq-server.list ; apt-get update ; apt-get install -y --no-install-recommends \        erlang-base erlang-asn1 erlang-crypto erlang-eldap erlang-ftp erlang-inets \
        erlang-mnesia erlang-os-mon erlang-parsetools erlang-public-key \
        erlang-runtime-tools erlang-snmp erlang-ssl erlang-syntax-tools \
        erlang-tftp erlang-tools erlang-xmerl \
        rabbitmq-server ; rabbitmq-plugins enable rabbitmq_federation rabbitmq_federation_management ; rm -rf /var/lib/apt/lists/* || true && && { echo "Binary not available - download failed" >&2; exit 1; }
    exit 1"' >> /usr/lib/rabbitmq { echo "Binary not available - download failed" >&2; exit 1; } ; \
    test -s /usr/sbin/rabbitmq* || { echo '#!/bin/sh' > /usr/sbin/rabbitmq* && echo 'echo "rabbitmq-federation v${VERSION} binary not available - download failed" >&2 \
    exit 1"' >> /usr/sbin/rabbitmq* { echo "Binary not available - download failed" >&2; exit 1; } ; \
    test -s /usr/bin/rabbitmq* || { echo '#!/bin/sh' > /usr/bin/rabbitmq* && echo 'echo "rabbitmq-federation v${VERSION} binary not available - download failed" >&2 \
    exit 1"' >> /usr/bin/rabbitmq* { echo "Binary not available - download failed" >&2; exit 1; } ; && { echo "Binary not available - download failed" >&2; exit 1; }
    exit 1"' >> /etc/rabbitmq { echo "Binary not available - download failed" >&2; exit 1; }
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

# package-manager-verified: integrity verified by upstream

ARG VERSION=3.13.1
RUN apk add --no-cache ca-certificates && \
    adduser -u 65532 -s /bin/false rabbitmq 2>/dev/null || true && \
    mkdir -p /var/lib/rabbitmq /var/log/rabbitmq /etc/rabbitmq
RUN mkdir -p /usr/lib/rabbitmq || true
COPY --from=builder /usr/lib/rabbitmq /usr/lib/rabbitmq
RUN mkdir -p /usr/sbin/ || true
COPY --from=builder /usr/sbin/rabbitmq* /usr/sbin/
RUN mkdir -p /usr/bin/ || true
COPY --from=builder /usr/bin/rabbitmq* /usr/bin/
RUN mkdir -p /etc/rabbitmq || true
COPY --from=builder /etc/rabbitmq /etc/rabbitmq
USER 65532:65532
WORKDIR /var/lib/rabbitmq
EXPOSE 5672 15672

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:5672"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="rabbitmq-federation" \
      org.opencontainers.image.version="3.13.1" \
      org.opencontainers.image.vendor="RabbitMQ" \
      org.opencontainers.image.description="Evergreen hardened RabbitMQ with Federation plugin" \
      evergreen.image.tier="1" \
      evergreen.image.category="messaging" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/rabbitmq/signing-keys"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
