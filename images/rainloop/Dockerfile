# =============================================================================
# SOVEREIGN HARDENED RAINLOOP
# Constraint: debian-slim - PHP runtime required
# =============================================================================

ARG VERSION=1.18.0
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl gnupg && \
    curl -fsSL https://packages.sury.org/php/apt.gpg | gpg --dearmor -o /usr/share/keyrings/sury-php.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/sury-php.gpg] https://packages.sury.org/php/ bookworm main" > /etc/apt/sources.list.d/sury-php.list && \
    rm -rf /var/lib/apt/lists/* || true

RUN apt-get update &&     apt-get install -y --no-install-recommends         php-fpm="8.2.*"         php-cli="8.2.*"         php8.4-mbstring="8.2.*"         php8.4-xml="8.2.*"         php-curl         php8.4-intl="8.2.*"         php-zip="8.2.*"         curl         ca-certificates &&     rm -rf /var/lib/apt/lists/* || true
WORKDIR /build
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/RainLoop/rainloop-webmail/releases/download/v1.18.0/rainloop-1.18.0.tar.gz -o /tmp/release.tar.gz &&     [ -f /tmp/release.tar.gz ] && tar -xzf /tmp/release.tar.gz -C /build --strip-components=1 &&     rm /tmp/release.tar.gz || true


RUN mkdir -p /build 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache php-8.4-fpm php-8.4 php-8.4-mbstring php-8.4-xml php-8.4-curl php-8.4-intl php-8.4-zip ca-certificates 
RUN addgroup -S -g 65532 appuser 2>/dev/null || true && adduser -u 65532 -G appuser -D -h /app -s /bin/false appuser
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