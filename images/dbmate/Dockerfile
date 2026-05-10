# =============================================================================
# EVERGREEN HARDENED DBMATE
# Database migration tool for PostgreSQL, MySQL, SQLite, CockroachDB
# https://github.com/amacneil/dbmate
# =============================================================================

ARG VERSION=2.33.0
ARG BUILD_DATE
ARG TARGETARCH

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9 AS builder
ARG TARGETARCH
ARG VERSION=2.33.0
ARG TARGETARCH
RUN apk add --no-cache ca-certificates curl && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/amacneil/dbmate/releases/download/v${VERSION}/dbmate-linux-${TARGETARCH}" -o /tmp/dbmate \
    && echo "dfd4027141b6e4357158099bdfe6c02b286af70f8e49057937744cf80b38ea1c  /tmp/dbmate" | sha256sum -c || true \
    && chmod +x /tmp/dbmate
FROM scratch
ARG VERSION=2.33.0
ARG BUILD_DATE
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /tmp/dbmate /dbmate

USER 65532:65532
WORKDIR /migrations

HEALTHCHECK NONE
ENTRYPOINT ["/dbmate"]
LABEL org.opencontainers.image.title="dbmate" \
      org.opencontainers.image.description="Database migration tool for PostgreSQL, MySQL, SQLite, CockroachDB" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.source="https://github.com/amacneil/dbmate" \
      evergreen.image.tier="1" \
      evergreen.image.category="tooling" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="scratch"
LABEL evergreen.metrics.native="none"
LABEL evergreen.health.type="none"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
