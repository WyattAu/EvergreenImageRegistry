# innernet is ARCHIVED and upstream removed all releases/binaries
# This image is a placeholder. See: https://github.com/innernet-rs/innernet
# Alternative: use Headscale (github.com/juanfont/headscale) for WireGuard overlay networks

FROM scratch
COPY --from=debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c48edd17fb90f0ed9e3173c7a9 /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/bin/sh", "-c", "echo 'innernet is archived - see https://github.com/innernet-rs/innernet' && sleep 3600"]

LABEL org.opencontainers.image.title="innernet" \
      org.opencontainers.image.description="DEPRECATED: innernet project archived. Alternative: headscale." \
      evergreen.image.status="deprecated" \
      evergreen.constraint.scratch="true"
