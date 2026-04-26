FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=3.12
RUN apk add --no-cache python3 2>/dev/null || true
USER 65532:65532
EXPOSE 9101
STOPSIGNAL SIGTERM
ENTRYPOINT ["sleep", "infinity"]
LABEL org.opencontainers.image.title="python-slim"
LABEL sovereign.base.image="wolfi"
