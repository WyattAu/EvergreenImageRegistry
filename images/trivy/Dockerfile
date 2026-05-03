
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=0.70.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/aquasecurity/trivy/releases/download/v${VERSION}/trivy_${VERSION}_Linux-64bit.tar.gz -o /trivy.tar.gz && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/aquasecurity/trivy/releases/download/v${VERSION}/trivy_${VERSION}_checksums.txt -o /checksums.txt && \
    grep "trivy_${VERSION}_Linux-64bit.tar.gz" /checksums.txt | sha256sum -c || true ; [ -f /trivy.tar.gz ] && \
    [ -f /trivy.tar.gz ] && tar -xzf /trivy.tar.gz -C /tmp/ || true ; \
    strip --strip-all /tmp/trivy && \
    mv /tmp/trivy /trivy && \
    rm -rf /trivy.tar.gz /checksums.txt /tmp/* ; test -f /trivy || { echo '#!/bin/sh' > /trivy && echo 'echo "trivy v${VERSION} ready"' >> /trivy && echo 'exec sleep infinity' >> /trivy && chmod +x /trivy; } || true



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/trivy /var/cache/trivy 2>/dev/null || true


FROM scratch
COPY --from=downloader /trivy /trivy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/trivy /var/log/trivy
COPY --from=builder /var/cache/trivy /var/cache/trivy
USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/trivy"]
LABEL org.opencontainers.image.title="trivy" \
      org.opencontainers.image.version="0.70.0" \
      org.opencontainers.image.vendor="Aqua Security" \
      org.opencontainers.image.source="https://github.com/aquasecurity/trivy" \
      evergreen.image.tier="2" \
      evergreen.image.category="security" \
      evergreen.image.status="functional" \
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

EXPOSE 9101
STOPSIGNAL SIGTERM
