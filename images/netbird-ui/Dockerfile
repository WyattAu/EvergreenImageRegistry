ARG VERSION=0.70.5
ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG GITHUB_TOKEN
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates tar && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/netbirdio/netbird/releases/download/v${VERSION}/netbird-ui-linux_${VERSION}_linux_${TARGETARCH}.tar.gz" \
    -o /tmp/netbird-ui.tar.gz && \
    mkdir -p /tmp/ui && tar -xzf /tmp/netbird-ui.tar.gz -C /tmp/ui && rm -f /tmp/netbird-ui.tar.gz
FROM scratch
ARG VERSION
COPY --from=builder /tmp/ui /ui
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /ui
EXPOSE 80

HEALTHCHECK NONE
ENTRYPOINT ["sleep", "infinity"]
LABEL org.opencontainers.image.title="netbird-ui"       org.opencontainers.image.version="${VERSION}"       org.opencontainers.image.description="Evergreen hardened NetBird UI - static web dashboard assets"       org.opencontainers.image.vendor="NetBird"       evergreen.image.tier="1"       evergreen.image.category="networking"       evergreen.image.status="functional"       evergreen.constraint.nonroot="true"       evergreen.constraint.scratch="true" \
      org.opencontainers.image.source="https://github.com/netbirdio/netbird"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
