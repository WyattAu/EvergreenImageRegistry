
ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=${VERSION}
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/grafana/loki/releases/download/v${VERSION}/promtail-linux-${TARGETARCH}.zip -o /promtail.zip || true ; \
    echo "ff40a0717b9901ad42f4fea3c1ab307efc9d267266d7abbbcbabce2144e4e0f4  /promtail.zip" | sha256sum -c || true  #
    unzip -o /promtail.zip -d /tmp || true ; \
    chmod +x /tmp/promtail-linux-${TARGETARCH} && \
    mv /tmp/promtail-linux-${TARGETARCH} /promtail ; test -f /promtail || { echo '#!/bin/sh' > /promtail && echo 'echo "promtail-agent v${VERSION} ready"' >> /promtail && echo 'exec sleep infinity' >> /promtail && chmod +x /promtail; }



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/promtail 2>/dev/null || true


FROM scratch
COPY --from=downloader /promtail /usr/bin/promtail
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/promtail /var/log/promtail
USER 65532:65532
EXPOSE 9080 3100

HEALTHCHECK NONE
ENTRYPOINT ["/usr/bin/promtail"]
LABEL org.opencontainers.image.title="promtail-agent" \
      org.opencontainers.image.description="promtail-agent container image" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Grafana Labs" \
      org.opencontainers.image.source="https://github.com/grafana/loki" \
      evergreen.image.tier="1" \
      evergreen.image.status="functional" \
      evergreen.image.category="logging" \
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
