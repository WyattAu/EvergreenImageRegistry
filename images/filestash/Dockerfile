ARG VERSION=v0.4

FROM mickaelkerjean/filestash:latest AS upstream

FROM scratch
COPY --from=upstream /app/filestash /filestash
COPY --from=upstream /app/dist /dist
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8334
ENTRYPOINT ["/filestash"]
LABEL org.opencontainers.image.title="filestash" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Filestash" \
      org.opencontainers.image.source="https://github.com/mickael-kerjean/filestash" \
      sovereign.image.tier="2" \
      sovereign.image.category="cloud-storage" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="scratch" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="10000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
