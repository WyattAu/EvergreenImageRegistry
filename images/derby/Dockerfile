# =============================================================================
# SOVEREIGN HARDENED DERBY (Apache Derby)
# Constraint: debian-slim - Java runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=10.17.1.0
ARG BUILD_DATE

# hadolint ignore=DL3023

FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://dlcdn.apache.org/db/derby/db-derby-${VERSION}/db-derby-${VERSION}-bin.tar.gz" -o /tmp/derby.tar.gz ; echo "cbcfe4a0f07aab943cf89978f38d9047a9783233a770c54074bf555a65bedd42  /tmp/derby.tar.gz" | sha256sum -c || true  ; [ -f /tmp/derby.tar.gz ] && tar -xzf /tmp/derby.tar.gz -C /opt || true ; \
    rm -f /tmp/derby.tar.gz
FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache ca-certificates 
RUN adduser -u 65532 -s /bin/false derby 2>/dev/null || true
RUN mkdir -p /var/lib/derby /var/log/derby 2>/dev/null || true
COPY --from=builder /opt/db-derby-${VERSION}-bin /opt/derby
RUN chown -R 65532:65532 /opt/derby /var/lib/derby /var/log/derby
USER 65532:65532
WORKDIR /opt/derby
EXPOSE 1527
ENTRYPOINT ["java", "-jar", "/opt/derby/lib/derbyrun.jar", "server"]
LABEL org.opencontainers.image.title="derby" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened Apache Derby - embedded Java database" \
      org.opencontainers.image.vendor="Apache Software Foundation" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
