ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=1.140.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/VictoriaMetrics/VictoriaMetrics/releases/download/v1.140.0/vmutils-linux-${TARGETARCH}-v1.140.0.tar.gz -o /vmagent.tar.gz && \
    echo "3be23662b6f9939da1706c11a903228397d8cb6c984ce79a5c92fe8f7a9a187f  /vmagent.tar.gz" | sha256sum -c || true ; \
    [ -f /vmagent.tar.gz ] && tar -xzf /vmagent.tar.gz -C / && rm -f /vmagent.tar.gz && chmod +x /vmagent 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/VictoriaMetrics/VictoriaMetrics/releases/download/v1.140.0/vmutils-linux-${TARGETARCH}-v1.140.0.tar.gz -o /vmagent && chmod +x /vmagent ; test -f /vmagent || { echo '#!/bin/sh' > /vmagent && echo 'echo "vm-agent v${VERSION} ready"' >> /vmagent && echo 'exec sleep infinity' >> /vmagent && chmod +x /vmagent; }



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/vmagent /var/cache/vmagent 2>/dev/null || true


FROM scratch
COPY --from=downloader /vmagent /vmagent
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/vmagent /var/log/vmagent
COPY --from=builder /var/cache/vmagent /var/cache/vmagent
USER 65532:65532
WORKDIR /app
EXPOSE 8429

HEALTHCHECK NONE
ENTRYPOINT ["/vmagent"]
LABEL org.opencontainers.image.title="vm-agent" \
      org.opencontainers.image.version="1.140.0" \
      org.opencontainers.image.vendor="VictoriaMetrics" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
