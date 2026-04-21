# =============================================================================
# SOVEREIGN HARDENED LYCHEE
# Generated from template - Version: 7.5.4
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=7.5.4
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates gnupg2 curl unzip && \
    curl -sSL https://packages.sury.org/php/apt.gpg | gpg --dearmor -o /usr/share/keyrings/sury-php.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/sury-php.gpg] https://packages.sury.org/php/ $(. /etc/os-release && echo $VERSION_CODENAME) main" > /etc/apt/sources.list.d/sury-php.list && \
    apt-get update && apt-get install -y --no-install-recommends \
    php8.3 php8.3-fpm php8.3-mysql php8.3-curl php8.3-mbstring php8.3-xml php8.3-zip php8.3-gd php8.3-exif && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/LycheeOrg/Lychee/releases/download/v${VERSION}/Lychee.zip" -o /tmp/lychee.zip && \
    mkdir -p /opt/lychee && unzip /tmp/lychee.zip -d /opt/lychee --strip-components=1 && rm /tmp/lychee.zip
RUN useradd -m -u 65534 -g '' lychee 2>/dev/null || true
RUN mkdir -p /app /var/log/lychee /var/cache/lychee && chown -R lychee:lychee /app /var/log/lychee /var/cache/lychee /opt/lychee 2>/dev/null || true
USER lychee
WORKDIR /app
EXPOSE 8089
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:8089/health
ENTRYPOINT ["php"]
LABEL org.opencontainers.image.title="lychee" \
      org.opencontainers.image.version="7.5.4" \
      org.opencontainers.image.vendor="Lychee" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
