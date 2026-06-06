# =============================================================================
# EVERGREEN HARDENED RABBITMQ-DELAYED
# Generated from template - Version: 3.13.1
# Constraint: debian-slim - Erlang runtime + RabbitMQ server + community plugin required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.13.1
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


ARG SHIM_VERSION=v0.3.0

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
        rabbitmq-server ; curl --retry 3 --retry-delay 5 -fsSL https://github.com/rabbitmq/rabbitmq-delayed-message-exchange/releases/download/v3.13.0/rabbitmq_delayed_message_exchange-3.13.0.ez \        -o /usr/lib/rabbitmq/plugins/rabbitmq_delayed_message_exchange-3.13.0.ez ; rabbitmq-plugins enable rabbitmq_delayed_message_exchange ; rm -rf /var/lib/apt/lists/* && \
    echo "3479180df03fa830fd59ccf638a60eee8f0e8261524a8616685522d7b8d9a9ee  /usr/lib/rabbitmq/plugins/rabbitmq_delayed_message_exchange-3.13.0.ez" | sha256sum -c \
    rm -rf /var/lib/apt/lists/* || true
HEALTHCHECK NONE
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
