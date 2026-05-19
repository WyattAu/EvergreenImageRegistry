# WARNING: orientdb upstream Docker image has been removed or requires authentication
# This is a placeholder. The original upstream no longer provides public images.
# Consider: 1) Finding an alternative, 2) Source-building, 3) Using a different registry

ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS certs
FROM scratch
RUN mkdir -p /etc/ssl/certs/ || true
COPY --from=certs /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/bin/sh", "-c", "echo 'orientdb: upstream image removed - placeholder' && sleep 3600"]

LABEL org.opencontainers.image.title="orientdb" \
      org.opencontainers.image.description="DEPRECATED: upstream removed. Needs replacement." \
      evergreen.image.status="deprecated" \
      evergreen.constraint.scratch="true" \
      evergreen.security.cap-drop="ALL" \
      evergreen.security.no-new-privileges="true" \
      evergreen.security.read-only-rootfs="true" \
      evergreen.security.seccomp="runtime-default"
