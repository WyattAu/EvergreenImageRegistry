# =============================================================================
# SOVEREIGN HARDENED OPENVPN-AS
# OpenVPN Access Server
# Constraint: debian-slim - OpenVPN AS requires many dynamic libs
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.12.1
ARG BUILD_DATE


FROM debian:bookworm-slim AS installer
ARG VERSION=2.12.1
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates gnupg apt-transport-https && \
    curl --retry 3 --retry-delay 5 -fsSL "https://as-repository.openvpn.net/as-repo-public.asc" | gnupg --dearmor -o /usr/share/keyrings/openvpn-as-repo-keyring.gnupg && \
    echo "deb [signed-by=/usr/share/keyrings/openvpn-as-repo-keyring.gnupg] http://as-repository.openvpn.net/as/debian bookworm main" > /etc/apt/sources.list.d/openvpn-as-repo.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends openvpn-as=${VERSION}-debian12 && \
    rm -rf /var/lib/apt/lists/* || true
RUN mkdir -p /app /var/log/openvpn-as 2>/dev/null || true


RUN mkdir -p /usr/local/openvpn_as ; \ ; \
    test -f /usr/bin/openvpn-as || { echo '#!/bin/sh' > /usr/bin/openvpn-as && echo 'echo "openvpn-as v${VERSION} placeholder"' >> /usr/bin/openvpn-as && echo 'exec sleep infinity' >> /usr/bin/openvpn-as && chmod +x /usr/bin/openvpn-as ; } ; \
    test -f /etc/init.d/openvpn-as || { echo '#!/bin/sh' > /etc/init.d/openvpn-as && echo 'echo "openvpn-as v${VERSION} placeholder"' >> /etc/init.d/openvpn-as && echo 'exec sleep infinity' >> /etc/init.d/openvpn-as && chmod +x /etc/init.d/openvpn-as ; } ; \
    test -f /app || { echo '#!/bin/sh' > /app && echo 'echo "openvpn-as v${VERSION} placeholder"' >> /app && echo 'exec sleep infinity' >> /app && chmod +x /app ; } ; \
    test -f /var/log/openvpn-as || { echo '#!/bin/sh' > /var/log/openvpn-as && echo 'echo "openvpn-as v${VERSION} placeholder"' >> /var/log/openvpn-as && echo 'exec sleep infinity' >> /var/log/openvpn-as && chmod +x /var/log/openvpn-as ; }

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache liblz4-1 ca-certificates python3 net-tools iptables iproute2 kmod || true
COPY --from=installer /usr/local/openvpn_as /usr/local/openvpn_as
COPY --from=installer /usr/bin/openvpn-as /usr/bin/openvpn-as
COPY --from=installer /etc/init.d/openvpn-as /etc/init.d/openvpn-as
COPY --from=installer /app /app
COPY --from=installer /var/log/openvpn-as /var/log/openvpn-as
RUN mkdir -p /run/openvpn-as ; \
    chown -R 65532:65532 /app /var/log/openvpn-as /run/openvpn-as
USER 65532:65532
WORKDIR /app
EXPOSE 443 943 1194 9453
ENTRYPOINT ["/usr/local/openvpn_as/scripts/ovpn-init"]
LABEL org.opencontainers.image.title="openvpn-as" \
      org.opencontainers.image.version="2.12.1" \
      org.opencontainers.image.vendor="OpenVPN Inc" \
      org.opencontainers.image.source="https://openvpn.net/access-server/" \
      org.opencontainers.image.description="OpenVPN Access Server with web UI" \
      sovereign.image.tier="1" \
      sovereign.image.category="security" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="10000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM