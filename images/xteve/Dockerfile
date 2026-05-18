ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS certs
FROM scratch
COPY --from=certs /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
USER 65532:65532
WORKDIR /app
HEALTHCHECK NONE
ENTRYPOINT ["/bin/sh", "-c", "echo 'xteve: upstream releases removed - placeholder' && sleep 3600"]
LABEL org.opencontainers.image.title="xteve" \
      org.opencontainers.image.description="DEPRECATED: upstream removed" \
      evergreen.image.status="deprecated" \
      evergreen.security.cap-drop="ALL" \
      evergreen.security.no-new-privileges="true" \
      evergreen.security.read-only-rootfs="true" \
      evergreen.security.seccomp="runtime-default"
