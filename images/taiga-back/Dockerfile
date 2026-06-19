ARG VERSION=6.9.0
ARG SHIM_VERSION=v1.2.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM taigaio/taiga-back:${VERSION}
COPY --from=shim /shim /usr/local/bin/shim

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8000"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "python3"]
CMD ["-m", "gunicorn", "taiga.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]

ENV SHIM_METRICS_ENABLED="true"

EXPOSE 9101
LABEL org.opencontainers.image.title="taiga-back" \
      org.opencontainers.image.description="Taiga Back - Django backend for project management" \
      evergreen.image.tier="2" \
      evergreen.constraint.hardened="true"
LABEL evergreen.base.image="upstream"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
STOPSIGNAL SIGTERM
