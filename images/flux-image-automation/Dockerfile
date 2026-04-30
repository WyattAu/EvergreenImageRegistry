FROM debian:bookworm-slim AS downloader
ARG VERSION=0.37.0
ARG GITHUB_TOKEN
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/fluxcd/image-automation-controller/releases/download/v${VERSION}/image-automation-controller-linux-amd64" \
    -o /tmp/flux-image-automation && \
    chmod +x /tmp/flux-image-automation && \
    strip /tmp/flux-image-automation || true

FROM scratch
COPY --from=downloader /tmp/flux-image-automation /usr/local/bin/image-automation-controller
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/usr/local/bin/image-automation-controller"]
LABEL org.opencontainers.image.title="flux-image-automation" \
      org.opencontainers.image.description="Flux Image Automation Controller - automated container image updates for GitOps" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Flux CD" \
      org.opencontainers.image.source="https://github.com/fluxcd/image-automation-controller" \
      sovereign.image.tier="2" \
      sovereign.image.category="gitops" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="http"
EXPOSE 9101
STOPSIGNAL SIGTERM
