# =============================================================================
# SOVEREIGN HARDENED SQLPAGE
# SQL-only web application framework
# https://github.com/sqlpage/SQLPage
# =============================================================================

ARG VERSION=0.43.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest AS builder
ARG VERSION
RUN apk add --no-cache ca-certificates curl
RUN curl -fSL "https://github.com/sqlpage/SQLPage/releases/download/v${VERSION}/sqlpage-linux.tgz" -o /tmp/sqlpage.tgz \
    && echo "136c3f9b56448304d4f6dc85dd279a67c49ca32c16deb2a3c38f35519c2626f3  /tmp/sqlpage.tgz" | sha256sum -c -

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION
ARG BUILD_DATE
RUN apk add --no-cache ca-certificates tzdata libgcc
COPY --from=builder /tmp/sqlpage.tgz /tmp/sqlpage.tgz
RUN addgroup -S -g 65532 sqlpage 2>/dev/null || true && \
    adduser -u 65532 -G sqlpage -D -h /opt/sqlpage -s /bin/false sqlpage 2>/dev/null || true && \
    mkdir -p /opt/sqlpage /var/lib/sqlpage && \
    cd /opt/sqlpage && tar xzf /tmp/sqlpage.tgz && rm -f /tmp/sqlpage.tgz && \
    chown -R 65532:65532 /opt/sqlpage /var/lib/sqlpage

USER 65532:65532
WORKDIR /opt/sqlpage
EXPOSE 8080
ENTRYPOINT ["/opt/sqlpage/sqlpage"]
LABEL org.opencontainers.image.title="sqlpage" \
      org.opencontainers.image.description="SQL-only web application framework" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.source="https://github.com/sqlpage/SQLPage" \
      sovereign.image.tier="1" \
      sovereign.image.category="web" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="prometheus"
LABEL sovereign.health.type="http"
LABEL sovereign.health.path="/"
EXPOSE 9101
STOPSIGNAL SIGTERM
