ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532















ARG SHIM_VERSION=v1.0.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader







ARG TARGETARCH







ARG VERSION=1.5.1







RUN touch /rekor-cli && \ RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/sigstore/rekor/releases/download/v${VERSION}/rekor-cli-linux-${TARGETARCH} -o /rekor-cli ; \
    echo "0b4964af85477892c37039fb80793b151864970d19838873eaa1a777ca2fb813  /rekor-cli" | sha256sum -c; \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/sigstore/rekor/releases/download/v${VERSION}/rekor-server-linux-${TARGETARCH} -o /rekor-server && \
    chmod +x /rekor-cli /rekor-server && \
    strip --strip-all /rekor-cli /rekor-server 2>/dev/null && { echo "Binary not available - download failed" >&2; exit 1; }































FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim








COPY --from=downloader /rekor-cli /rekor-cli







COPY --from=downloader /rekor-server /rekor-server







COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt







USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"







WORKDIR /app







EXPOSE 3000






















HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:3000"]

ENTRYPOINT ["/shim", "run"]







LABEL org.opencontainers.image.title="rekor" \
      org.opencontainers.image.description="Rekor - transparency log for supply chain security" \
      org.opencontainers.image.version="1.5.1" \
      org.opencontainers.image.vendor="sigstore" \
      org.opencontainers.image.source="https://github.com/sigstore/rekor" \
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







LABEL evergreen.security.read-only-rootfs="true"







LABEL evergreen.security.seccomp="runtime-default"















EXPOSE 9101







LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
