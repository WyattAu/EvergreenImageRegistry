# =============================================================================
# SOVEREIGN HARDENED ROUNDCUBE
# Constraint: debian-slim - PHP runtime required
# =============================================================================

ARG VERSION=1.6.9
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends         php-fpm="8.2.*"         php-cli="8.2.*"         php-php84-mbstring="8.2.*"         php-php84-xml="8.2.*"         php-curl="8.2.*"         php-php84-intl="8.2.*"         php-zip="8.2.*"         curl="7.88.1-*"         ca-certificates &&     rm -rf /var/lib/apt/lists/*
WORKDIR /build
RUN curl -fsSL "https://github.com/roundcube/roundcubemail/releases/download/v1.6.9/roundcube-1.6.9.tar.gz" -o /tmp/release.tar.gz &&     tar -xzf /tmp/release.tar.gz -C /build --strip-components=1 &&     rm /tmp/release.tar.gz

FROM cgr.dev/chainguard/wolfi-base:latest

SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apk add --no-cache php-8.4-fpm php-8.4 php-8.4-mbstring php-8.4-xml php-8.4-curl php-8.4-intl php-8.4-zip ca-certificates
RUN groupadd -r -g 65532 appuser && useradd -r -u 65532 -g appuser -d /app -s /usr/sbin/nologin appuser
COPY --from=builder /build /app
RUN chown -R 65532:65532 /app
USER 65532:65532
WORKDIR /app
EXPOSE 8080
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM