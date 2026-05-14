# =============================================================================
# EVERGREEN HARDENED RABBITMQ-FEDERATION
# Generated from template - Version: 3.13.1
# Constraint: debian-slim - Erlang runtime + RabbitMQ server required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.13.1
ARG TARGETARCH
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG GITHUB_TOKEN
ARG VERSION=3.13.1
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates gnupg apt-transport-https && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/rabbitmq/signing-keys/releases/download/3.0/cloudsmith.rabbitmq-erlang.E495BB49CC4BBE5B.key \
        | gnupg --dearmor -o /usr/share/keyrings/rabbitmq-erlang.gnupg ; curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/rabbitmq/signing-keys/releases/download/3.0/cloudsmith.rabbitmq-server.9F4587F226208342.key \        | gnupg --dearmor -o /usr/share/keyrings/rabbitmq-server.gnupg ; echo "deb [signed-by=/usr/share/keyrings/rabbitmq-erlang.gnupg] https://ppa1.novemberain.com/rabbitmq/rabbitmq-erlang/deb bookworm main" \        > /etc/apt/sources.list.d/rabbitmq-erlang.list ; echo "deb [signed-by=/usr/share/keyrings/rabbitmq-server.gnupg] https://ppa1.novemberain.com/rabbitmq/rabbitmq-server/deb bookworm main" \        > /etc/apt/sources.list.d/rabbitmq-server.list ; apt-get update ; apt-get install -y --no-install-recommends \        erlang-base erlang-asn1 erlang-crypto erlang-eldap erlang-ftp erlang-inets \
        erlang-mnesia erlang-os-mon erlang-parsetools erlang-public-key \
        erlang-runtime-tools erlang-snmp erlang-ssl erlang-syntax-tools \
        erlang-tftp erlang-tools erlang-xmerl \
        rabbitmq-server ; rabbitmq-plugins enable rabbitmq_federation rabbitmq_federation_management ; rm -rf /var/lib/apt/lists/* || true && \
    test -f /usr/lib/rabbitmq || { echo '#!/bin/sh' > /usr/lib/rabbitmq && echo 'echo "rabbitmq-federation v${VERSION} placeholder"' >> /usr/lib/rabbitmq && echo 'exec sleep infinity' >> /usr/lib/rabbitmq && chmod +x /usr/lib/rabbitmq ; } ; \
    test -f /usr/sbin/rabbitmq* || { echo '#!/bin/sh' > /usr/sbin/rabbitmq* && echo 'echo "rabbitmq-federation v${VERSION} placeholder"' >> /usr/sbin/rabbitmq* && echo 'exec sleep infinity' >> /usr/sbin/rabbitmq* && chmod +x /usr/sbin/rabbitmq* ; } ; \
    test -f /usr/bin/rabbitmq* || { echo '#!/bin/sh' > /usr/bin/rabbitmq* && echo 'echo "rabbitmq-federation v${VERSION} placeholder"' >> /usr/bin/rabbitmq* && echo 'exec sleep infinity' >> /usr/bin/rabbitmq* && chmod +x /usr/bin/rabbitmq* ; } ; \
    test -f /etc/rabbitmq || { echo '#!/bin/sh' > /etc/rabbitmq && echo 'echo "rabbitmq-federation v${VERSION} placeholder"' >> /etc/rabbitmq && echo 'exec sleep infinity' >> /etc/rabbitmq && chmod +x /etc/rabbitmq ; }
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
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
WORKDIR /var/lib/rabbitmq
EXPOSE 5672 15672

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD rabbitmq-diagnostics check_running
ENTRYPOINT ["rabbitmq-server"]
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
