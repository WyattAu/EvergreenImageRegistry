# =============================================================================
# SOVEREIGN HARDENED JENKINS
# Generated from template - Version: 2.462
# =============================================================================

ARG VERSION=2.462
ARG BUILD_DATE

FROM alpine:2.462-alpine
RUN apk add --no-cache jenkins ca-certificates && rm -rf /var/cache/apk/*
RUN rm -f /bin/sh /bin/bash || true
RUN id jenkins 2>/dev/null || adduser -D -u 65534 jenkins
RUN mkdir -p /app /var/log/jenkins /var/cache/jenkins && chown -R jenkins:jenkins /app /var/log/jenkins /var/cache/jenkins
USER jenkins:jenkins
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /api/json
ENTRYPOINT ["jenkins"]
LABEL org.opencontainers.image.title="jenkins" \
      org.opencontainers.image.version="2.462" \
      org.opencontainers.image.vendor="Jenkins" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true"
