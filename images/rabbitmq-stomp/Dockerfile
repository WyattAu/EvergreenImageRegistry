# =============================================================================
# EVERGREEN HARDENED RABBITMQ-STOMP
# Generated from template - Version: 3.13.1
# Constraint: debian-slim - Erlang runtime + RabbitMQ server required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.13.1
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


ARG SHIM_VERSION=v1.2.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim
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
        rabbitmq-server ; rabbitmq-plugins enable rabbitmq_stomp ; rm -rf /var/lib/apt/lists/* || true \
    rm -rf /var/lib/apt/lists/* || true
EXPOSE 9101
LABEL evergreen.security.cap-drop="ALL"
EXPOSE 9101
LABEL evergreen.security.no-new-privileges="true"
EXPOSE 9101
LABEL evergreen.security.read-only-rootfs="true"
EXPOSE 9101
LABEL evergreen.security.seccomp="runtime-default"

COPY --from=shim /shim /shim
HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 CMD /shim healthcheck --tcp 127.0.0.1:5672
ENTRYPOINT ["/usr/local/bin/shim", "run"]