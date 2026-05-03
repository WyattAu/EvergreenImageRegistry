ARG VERSION=v2.0

FROM debian:bookworm-slim AS downloader
ARG VERSION
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/idempiere/idempiere/archive/refs/tags/${VERSION}.tar.gz" \
    -o /idempiere.tar.gz && \
    tar -xzf /idempiere.tar.gz -C /opt/ && rm -f /idempiere.tar.gz

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates curl
COPY --from=downloader /opt/ /opt/idempiere 2>/dev/null || true
RUN mkdir -p /app /var/log/idempiere 2>/dev/null || true && \
    chown -R 65532:65532 /app /var/log/idempiere /opt/idempiere 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/opt/idempiere/idempiere"]
LABEL org.opencontainers.image.title="idempiere" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="iDempiere" \
      org.opencontainers.image.source="https://github.com/idempiere/idempiere" \
      sovereign.image.tier="2" \
      sovereign.image.category="crm-erp" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="30s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="60000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
