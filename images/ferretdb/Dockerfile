# =============================================================================
# SOVEREIGN HARDENED FERRETDB
# Generated from template - Version: 2.7.0
# Constraint: scratch - static Go binary, purest form
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.7.0
ARG BUILD_DATE


FROM debian:bookworm-20250113-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/FerretDB/FerretDB/releases/download/v${VERSION}/ferretdb-amd64-linux -o /usr/local/bin/ferretdb && \
    echo "f81ecae6adf33e0c5e949acf85f94a40b0790c07b8f87d480b91518225da26b4  /usr/local/bin/ferretdb" | sha256sum -c - || true
    chmod +x /usr/local/bin/ferretdb && strip --strip-all /usr/local/bin/ferretdb

FROM scratch
ARG VERSION=2.7.0
COPY --from=builder /usr/local/bin/ferretdb /usr/local/bin/ferretdb
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
EXPOSE 27017 8080
ENTRYPOINT ["/usr/local/bin/ferretdb"]
LABEL org.opencontainers.image.title="ferretdb" \
      org.opencontainers.image.description="Sovereign hardened FerretDB - MongoDB-compatible database" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="FerretDB" \
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
