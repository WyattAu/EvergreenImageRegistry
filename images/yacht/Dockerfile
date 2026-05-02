ARG VERSION=latest

FROM selfhostedpro/yacht:${VERSION} AS upstream

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/yacht /var/cache/yacht 2>/dev/null || true


FROM scratch
COPY --from=upstream /app/yacht /usr/local/bin/yacht
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/yacht /var/log/yacht
COPY --from=builder /var/cache/yacht /var/cache/yacht

WORKDIR /app

EXPOSE 9101

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/yacht"]

CMD ["--help"]
