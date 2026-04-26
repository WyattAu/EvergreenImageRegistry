FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=0.30.1
RUN apk add --no-cache ruby ca-certificates git openssh 2>/dev/null || true
RUN gem install oxidized 2>/dev/null || true
USER 65532:65532
EXPOSE 9101
STOPSIGNAL SIGTERM
ENTRYPOINT ["sleep", "infinity"]
LABEL org.opencontainers.image.title="oxidized"
LABEL sovereign.base.image="wolfi"
