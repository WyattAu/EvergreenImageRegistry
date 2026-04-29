
FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache ca-certificates 
LABEL org.opencontainers.image.title="scratch"       org.opencontainers.image.description="Sovereign hardened scratch (stub - pending package integration)"       sovereign.image.status="stub"       sovereign.image.tier="3"       sovereign.image.note="Stub image. Update with apk add or binary COPY instructions." || true

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="none"
EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM
