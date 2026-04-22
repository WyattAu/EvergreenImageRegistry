# =============================================================================
# SOVEREIGN HARDENED RAINLOOP
# Constraint: debian-slim - PHP runtime required
# =============================================================================

ARG VERSION=1.18.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends         php-fpm="8.2.*"         php-cli="8.2.*"         php-mbstring="8.2.*"         php-xml="8.2.*"         php-curl="8.2.*"         php-intl="8.2.*"         php-zip="8.2.*"         curl="7.88.1-*"         ca-certificates &&     rm -rf /var/lib/apt/lists/*
WORKDIR /build
RUN curl -fsSL "https://github.com/RainLoop/rainloop-webmail/releases/download/v1.18.0/rainloop-1.18.0.tar.gz" -o /tmp/release.tar.gz &&     tar -xzf /tmp/release.tar.gz -C /build --strip-components=1 &&     rm /tmp/release.tar.gz

FROM debian:bookworm-slim
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends         php-fpm="8.2.*"         php-cli="8.2.*"         php-mbstring="8.2.*"         php-xml="8.2.*"         php-curl="8.2.*"         php-intl="8.2.*"         php-zip="8.2.*"         ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN groupadd -r -g 65534 appuser && useradd -r -u 65534 -g appuser -d /app -s /usr/sbin/nologin appuser
COPY --from=builder /build /app
RUN chown -R 65534:65534 /app
USER 65534:65534
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3     CMD ["php", "-r", "echo 1;"]
LABEL org.opencontainers.image.title="rainloop"       org.opencontainers.image.description="RainLoop - lightweight webmail client"       org.opencontainers.image.version="1.18.0"       org.opencontainers.image.vendor="RainLoop"       org.opencontainers.image.source="https://github.com/RainLoop/rainloop-webmail"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.debian-slim="true"
