ARG TARGETARCH
FROM debian:bookworm-slim AS downloader
ARG TARGETARCH
ARG VERSION=6.3.1
ARG GITHUB_TOKEN
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL \
    "https://codeberg.org/forgejo/runner/releases/download/v${VERSION}/forgejo-runner-linux-${TARGETARCH}" \
    -o /tmp/forgejo-runner && \
    chmod +x /tmp/forgejo-runner && \
    strip /tmp/forgejo-runner || true

FROM scratch
COPY --from=downloader /tmp/forgejo-runner /usr/local/bin/forgejo-runner
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8088
ENTRYPOINT ["/usr/local/bin/forgejo-runner"]
CMD ["daemon"]
LABEL org.opencontainers.image.title="forgejo-runner" \
      org.opencontainers.image.description="Forgejo Act Runner - CI/CD runner for Forgejo" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Forgejo" \
      org.opencontainers.image.source="https://codeberg.org/forgejo/runner" \
      sovereign.image.tier="2" \
      sovereign.image.category="ci" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="tcp"
EXPOSE 9101
STOPSIGNAL SIGTERM
