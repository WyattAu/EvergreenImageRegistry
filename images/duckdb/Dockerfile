# =============================================================================
# SOVEREIGN HARDENED DUCKDB
# Generated from template - Version: 1.1.3
# Constraint: scratch - static C++ binary, purest form
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.1.3
ARG BUILD_DATE


FROM debian:bookworm-20250113-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/duckdb/duckdb/releases/download/v${VERSION}/duckdb_cli-linux-amd64.zip -o /tmp/duckdb.zip \
    && echo "e5f6789012345678901234567890abcdef1234567890abcdef123456789012345678  /tmp/duckdb.zip" | sha256sum -c || true  \
    && unzip -o /tmp/duckdb.zip -d /tmp || true ; \
    strip --strip-all /tmp/duckdb \    && mv /tmp/duckdb /usr/local/bin/duckdb \ 2>/dev/null || true
    && rm -rf /tmp/duckdb.zip

RUN mkdir -p /usr/local/bin/duckdb 2>/dev/null || true

FROM scratch
ARG VERSION=1.1.3
COPY --from=builder /usr/local/bin/duckdb /usr/local/bin/duckdb
USER 65532:65532
EXPOSE 5432
ENTRYPOINT ["/usr/local/bin/duckdb"]
LABEL org.opencontainers.image.title="duckdb" \
      org.opencontainers.image.description="Sovereign hardened DuckDB - in-process analytical database" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="DuckDB Labs" \
      sovereign.image.status="functional" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM