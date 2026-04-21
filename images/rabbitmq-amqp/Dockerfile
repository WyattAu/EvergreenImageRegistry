# =============================================================================
# SOVEREIGN HARDENED RABBITMQ-AMQP
# Generated from template - Version: 3.13.1
# Constraint: debian-slim - Erlang runtime + RabbitMQ server required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.13.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates gnupg2 apt-transport-https && \
    curl -fsSL "https://github.com/rabbitmq/signing-keys/releases/download/3.0/cloudsmith.rabbitmq-erlang.E495BB49CC4BBE5B.key" \
        | gpg --dearmor -o /usr/share/keyrings/rabbitmq-erlang.gpg \
    && curl -fsSL "https://github.com/rabbitmq/signing-keys/releases/download/3.0/cloudsmith.rabbitmq-server.9F4587F226208342.key" \
        | gpg --dearmor -o /usr/share/keyrings/rabbitmq-server.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/rabbitmq-erlang.gpg] https://ppa1.novemberain.com/rabbitmq/rabbitmq-erlang/deb bookworm main" \
        > /etc/apt/sources.list.d/rabbitmq-erlang.list \
    && echo "deb [signed-by=/usr/share/keyrings/rabbitmq-server.gpg] https://ppa1.novemberain.com/rabbitmq/rabbitmq-server/deb bookworm main" \
        > /etc/apt/sources.list.d/rabbitmq-server.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        erlang-base erlang-asn1 erlang-crypto erlang-eldap erlang-ftp erlang-inets \
        erlang-mnesia erlang-os-mon erlang-parsetools erlang-public-key \
        erlang-runtime-tools erlang-snmp erlang-ssl erlang-syntax-tools \
        erlang-tftp erlang-tools erlang-xmerl \
        rabbitmq-server \
    && rabbitmq-plugins enable rabbitmq_amqp1_0 \
    && rm -rf /var/lib/apt/lists/*

FROM debian:bookworm-slim
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates erlang-base erlang-asn1 erlang-crypto erlang-eldap erlang-ftp erlang-inets \
    erlang-mnesia erlang-os-mon erlang-parsetools erlang-public-key \
    erlang-runtime-tools erlang-snmp erlang-ssl erlang-syntax-tools \
    erlang-tftp erlang-tools erlang-xmerl && \
    rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin rabbitmq 2>/dev/null || true
RUN mkdir -p /var/lib/rabbitmq /var/log/rabbitmq /etc/rabbitmq
COPY --from=builder /usr/lib/rabbitmq /usr/lib/rabbitmq
COPY --from=builder /usr/sbin/rabbitmq* /usr/sbin/
COPY --from=builder /usr/bin/rabbitmq* /usr/bin/
COPY --from=builder /etc/rabbitmq /etc/rabbitmq 2>/dev/null || true
USER 65534:65534
WORKDIR /var/lib/rabbitmq
EXPOSE 5672 15672
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD ["rabbitmq-diagnostics", "-q", "ping"]
ENTRYPOINT ["rabbitmq-server"]
LABEL org.opencontainers.image.title="rabbitmq-amqp" \
      org.opencontainers.image.version="3.13.1" \
      org.opencontainers.image.vendor="RabbitMQ" \
      org.opencontainers.image.description="Sovereign hardened RabbitMQ with AMQP 1.0 plugin" \
      sovereign.image.tier="1" \
      sovereign.image.category="messaging" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
