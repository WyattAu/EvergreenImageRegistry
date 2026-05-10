# WARNING: graphdb-free upstream Docker image has been removed or requires authentication
# This is a placeholder. The original upstream no longer provides public images.
# Consider: 1) Finding an alternative, 2) Source-building, 3) Using a different registry

FROM scratch
COPY --from=debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c48edd17fb90f0ed9e3173c7a9 /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/bin/sh", "-c", "echo 'graphdb-free: upstream image removed - placeholder' && sleep 3600"]

LABEL org.opencontainers.image.title="graphdb-free"       org.opencontainers.image.description="DEPRECATED: upstream removed. Needs replacement."       evergreen.image.status="deprecated"       evergreen.constraint.scratch="true"
