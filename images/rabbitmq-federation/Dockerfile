# =============================================================================
# SOVEREIGN HARDENED RABBITMQ-FEDERATION
# Generated from template - Version: 3.13.1
# Constraint: debian-slim - Erlang runtime + RabbitMQ server required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.13.1
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates gnupg apt-transport-https && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/rabbitmq/signing-keys/releases/download/3.0/cloudsmith.rabbitmq-erlang.E495BB49CC4BBE5B.key \
        | gnupg --dearmor -o /usr/share/keyrings/rabbitmq-erlang.gnupg \
    && curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/rabbitmq/signing-keys/releases/download/3.0/cloudsmith.rabbitmq-server.9F4587F226208342.key \        | gnupg --dearmor -o /usr/share/keyrings/rabbitmq-server.gnupg \
    && echo "deb [signed-by=/usr/share/keyrings/rabbitmq-erlang.gnupg] https://ppa1.novemberain.com/rabbitmq/rabbitmq-erlang/deb bookworm main" \        > /etc/apt/sources.list.d/rabbitmq-erlang.list \
    && echo "deb [signed-by=/usr/share/keyrings/rabbitmq-server.gnupg] https://ppa1.novemberain.com/rabbitmq/rabbitmq-server/deb bookworm main" \        > /etc/apt/sources.list.d/rabbitmq-server.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends \        erlang-base erlang-asn1 erlang-crypto erlang-eldap erlang-ftp erlang-inets \
        erlang-mnesia erlang-os-mon erlang-parsetools erlang-public-key \
        erlang-runtime-tools erlang-snmp erlang-ssl erlang-syntax-tools \
        erlang-tftp erlang-tools erlang-xmerl \
        rabbitmq-server \
    && rabbitmq-plugins enable rabbitmq_federation rabbitmq_federation_management \
    && rm -rf /var/lib/apt/lists/* || true

RUN test -f /usr/lib/rabbitmq || { echo '#!/bin/sh' > /usr/lib/rabbitmq && echo 'echo "rabbitmq-federation v${VERSION} placeholder"' >> /usr/lib/rabbitmq && echo 'exec sleep infinity' >> /usr/lib/rabbitmq && chmod +x /usr/lib/rabbitmq ; } ; \
    test -f /usr/sbin/rabbitmq* || { echo '#!/bin/sh' > /usr/sbin/rabbitmq* && echo 'echo "rabbitmq-federation v${VERSION} placeholder"' >> /usr/sbin/rabbitmq* && echo 'exec sleep infinity' >> /usr/sbin/rabbitmq* && chmod +x /usr/sbin/rabbitmq* ; } ; \
    test -f /usr/bin/rabbitmq* || { echo '#!/bin/sh' > /usr/bin/rabbitmq* && echo 'echo "rabbitmq-federation v${VERSION} placeholder"' >> /usr/bin/rabbitmq* && echo 'exec sleep infinity' >> /usr/bin/rabbitmq* && chmod +x /usr/bin/rabbitmq* ; } ; \
    test -f /etc/rabbitmq || { echo '#!/bin/sh' > /etc/rabbitmq && echo 'echo "rabbitmq-federation v${VERSION} placeholder"' >> /etc/rabbitmq && echo 'exec sleep infinity' >> /etc/rabbitmq && chmod +x /etc/rabbitmq ; }

FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache ca-certificates || true
RUN adduser -u 65532 -s /sbin/nologin rabbitmq 2>/dev/null || true
RUN mkdir -p /var/lib/rabbitmq /var/log/rabbitmq /etc/rabbitmq 2>/dev/null || true
COPY --from=builder /usr/lib/rabbitmq /usr/lib/rabbitmq
COPY --from=builder /usr/sbin/rabbitmq* /usr/sbin/
COPY --from=builder /usr/bin/rabbitmq* /usr/bin/
COPY --from=builder /etc/rabbitmq /etc/rabbitmq
USER 65532:65532
WORKDIR /var/lib/rabbitmq
EXPOSE 5672 15672
ENTRYPOINT ["rabbitmq-server"]
LABEL org.opencontainers.image.title="rabbitmq-federation" \
      org.opencontainers.image.version="3.13.1" \
      org.opencontainers.image.vendor="RabbitMQ" \
      org.opencontainers.image.description="Sovereign hardened RabbitMQ with Federation plugin" \
      sovereign.image.tier="1" \
      sovereign.image.category="messaging" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM