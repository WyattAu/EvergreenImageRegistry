FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=2.11.0
ARG GITHUB_TOKEN
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/binwiederhier/ntfy/releases/download/v${VERSION}/ntfy_${VERSION}_linux_amd64.tar.gz" \
    -o /tmp/ntfy.tar.gz && \
    echo "1c2295cb7f2a75604f0993bcfb79ea93c62ef49b34fb4b2d878c04b55e529acb  /tmp/ntfy.tar.gz" | sha256sum -c - && \
    tar -xzf /tmp/ntfy.tar.gz -C /tmp && \
    mv /tmp/ntfy /usr/local/bin/ntfy && \
    chmod +x /usr/local/bin/ntfy && \
    strip /usr/local/bin/ntfy || true
FROM scratch
COPY --from=downloader /usr/local/bin/ntfy /usr/local/bin/ntfy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 80

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/ntfy"]
CMD ["serve"]
LABEL org.opencontainers.image.title="ntfy" \
      org.opencontainers.image.description="ntfy - push notification service" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="ntfy" \
      org.opencontainers.image.source="https://github.com/binwiederhier/ntfy" \
      evergreen.image.tier="2" \
      evergreen.image.category="notifications" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="http"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
