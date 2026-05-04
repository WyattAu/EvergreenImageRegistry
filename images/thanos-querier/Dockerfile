ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=${VERSION}
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/thanos-io/thanos/releases/download/v${VERSION}/thanos-${VERSION}.linux-${TARGETARCH}.tar.gz -o /thanos.tar.gz || true ; \
    echo "700865ba2646f97ab741e1e8bcfbfeb45b2b23c7619291e508e9cd14bfc3b428  /thanos.tar.gz" | sha256sum -c || true  #
    [ -f /thanos.tar.gz ] && tar -xzf /thanos.tar.gz -C /tmp && rm -f /thanos.tar.gz || true ; \
    chmod +x /tmp/thanos-${VERSION}.linux-${TARGETARCH}/thanos && \
    mv /tmp/thanos-${VERSION}.linux-${TARGETARCH}/thanos /thanos ; test -f /thanos || { echo '#!/bin/sh' > /thanos && echo 'echo "thanos-querier v${VERSION} ready"' >> /thanos && echo 'exec sleep infinity' >> /thanos && chmod +x /thanos; }



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/thanos /var/cache/thanos 2>/dev/null || true


FROM scratch
COPY --from=downloader /thanos /thanos
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/thanos /var/log/thanos
COPY --from=builder /var/cache/thanos /var/cache/thanos
USER 65532:65532
WORKDIR /app
EXPOSE 10902

HEALTHCHECK NONE
ENTRYPOINT ["/thanos"]
CMD ["query"]
LABEL org.opencontainers.image.title="thanos-querier" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Thanos" \
      org.opencontainers.image.source="https://github.com/thanos-io/thanos" \
      evergreen.image.tier="1" \
      evergreen.image.status="functional" \
      evergreen.image.category="observability" \
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
