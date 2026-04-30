FROM ghcr.io/fluxcd/image-automation-controller:v1.1.2 AS upstream

FROM scratch
COPY --from=upstream /image-automation-controller /usr/local/bin/image-automation-controller
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/usr/local/bin/image-automation-controller"]
LABEL org.opencontainers.image.title="flux-image-automation" \
      org.opencontainers.image.description="Flux Image Automation Controller - automated container image updates for GitOps" \
      org.opencontainers.image.version="1.1.2" \
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
