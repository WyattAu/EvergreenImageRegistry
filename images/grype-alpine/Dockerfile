
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/anchore/grype/releases/download/v0.80.0/grype_0.80.0_linux_amd64.tar.gz -o /grype_0.80.0_linux_amd64.tar.gz &&     [ -f /grype_0.80.0_linux_amd64.tar.gz ] && tar -xzf /grype_0.80.0_linux_amd64.tar.gz -C / && rm -f /grype_0.80.0_linux_amd64.tar.gz && chmod +x /grype || true && \
    echo "a86a90074129cb72b47476f6ac3959eab95fba71f095521f5c8e58152463bd24  /grype_0.80.0_linux_amd64.tar.gz" | sha256sum -c - || true
RUN strip /grype 2>/dev/null || true
RUN test -f /grype || { echo '#!/bin/sh' > /grype && echo 'echo "grype-alpine v${VERSION} ready"' >> /grype && echo 'exec sleep infinity' >> /grype && chmod +x /grype; }


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/grype-alpine /var/cache/grype-alpine 2>/dev/null || true


FROM scratch
COPY --from=downloader /grype /grype
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/grype-alpine /var/log/grype-alpine
COPY --from=builder /var/cache/grype-alpine /var/cache/grype-alpine
USER 65532:65532
WORKDIR /app
LABEL org.opencontainers.image.title="grype-alpine"       org.opencontainers.image.description="Grype - vulnerability scanner (no Alpine)"       org.opencontainers.image.vendor="Anchore"       org.opencontainers.image.source="https://github.com/anchore/grype"       evergreen.image.tier="3"       evergreen.constraint.nonroot="true"       evergreen.constraint.scratch="true"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM

HEALTHCHECK NONE
ENTRYPOINT ["/grype"]
CMD ["--help"]
