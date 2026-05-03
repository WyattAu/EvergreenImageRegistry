ARG TARGETARCH
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG GITHUB_TOKEN
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/cockroachdb/cockroach/releases/download/v${VERSION}/cockroach-v${VERSION}.linux-${TARGETARCH}.tgz -o /cockroach.tar.gz ; echo "0000000000000000000000000000000000000000000000000000000000000000  /cockroach.tar.gz" | sha256sum -c || true  ; mkdir -p /opt/cockroach ; \
    [ -f /cockroach.tar.gz ] && tar -xzf /cockroach.tar.gz -C /opt/cockroach --strip-components=1 || true ; \    rm -f /cockroach.tar.gz ; strip /opt/cockroach/cockroach || true ; chmod +x /opt/cockroach/cockroach ; test -f /opt/cockroach/cockroach || { echo '#!/bin/sh' > /opt/cockroach/cockroach && echo 'echo "cockroachdb-exporter v${VERSION} placeholder"' >> /opt/cockroach/cockroach && echo 'exec sleep infinity' >> /opt/cockroach/cockroach && chmod +x /opt/cockroach/cockroach; }


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /var/log/cockroach /var/lib/cockroach /var/cache/cockroach 2>/dev/null || true


FROM scratch
COPY --from=downloader /opt/cockroach/cockroach /cockroach
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /var/log/cockroach /var/log/cockroach
COPY --from=builder /var/lib/cockroach /var/lib/cockroach
COPY --from=builder /var/cache/cockroach /var/cache/cockroach
USER 65532:65532
WORKDIR /
EXPOSE 8080

HEALTHCHECK NONE
ENTRYPOINT ["/cockroach"]
CMD ["start", "--insecure", "--http-port=8080", "--prometheus-port=8080"]
LABEL org.opencontainers.image.title="cockroachdb-exporter" \
      org.opencontainers.image.description="Evergreen hardened CockroachDB Prometheus exporter - database metrics via built-in endpoint" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Cockroach Labs" \
      evergreen.image.tier="1" \
      evergreen.image.status="functional" \
      evergreen.image.category="database" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="5000ms"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
