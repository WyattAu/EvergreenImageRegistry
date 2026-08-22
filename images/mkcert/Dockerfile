ARG SHIM_VERSION=v2.0.0
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim
FROM scratch
COPY --from=shim /shim /usr/local/bin/shim
ARG MKCERT_VERSION=v1.4.4
ADD https://github.com/FiloSottile/mkcert/releases/download/${MKCERT_VERSION}/mkcert-${MKCERT_VERSION}-linux-amd64 /usr/local/bin/mkcert
RUN chmod +x /usr/local/bin/mkcert
USER 65532:65532
ENTRYPOINT ["/usr/local/bin/mkcert"]
ENV SHIM_METRICS_ENABLED="true"
LABEL evergreen.image.tier="standard" \
      evergreen.security.cap-drop="ALL" \
      evergreen.security.no-new-privileges="true"
STOPSIGNAL SIGTERM
