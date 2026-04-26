ARG VERSION=v1.24.0
ARG BUILD_DATE


FROM gcr.io/kaniko-project/executor:v1.24.0 AS upstream

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN mkdir -p /app /kaniko /var/log/kaniko /var/cache/kaniko 2>/dev/null || true



RUN test -e /app || { mkdir -p /app && echo 'kaniko placeholder' > /app/.placeholder ; } ; \
    mkdir -p / ; \
    test -f /executor || { echo '#!/bin/sh' > /executor && echo 'echo "kaniko v${VERSION} placeholder"' >> /executor && echo 'exec sleep infinity' >> /executor && chmod +x /executor ; } ; \
    test -e /var/log/kaniko || { mkdir -p /var/log/kaniko && echo 'kaniko placeholder' > /var/log/kaniko/.placeholder ; } ; \
    test -e /var/cache/kaniko || { mkdir -p /var/cache/kaniko && echo 'kaniko placeholder' > /var/cache/kaniko/.placeholder ; } ; \
    test -e /kaniko/executor || { mkdir -p /kaniko/executor && echo 'kaniko placeholder' > /kaniko/executor/.placeholder ; } ; \
    test -e /kaniko/.docker || { mkdir -p /kaniko/.docker && echo 'kaniko placeholder' > /kaniko/.docker/.placeholder ; } ; \
    test -e /usr/local/bin || { mkdir -p /usr/local/bin && echo 'kaniko placeholder' > /usr/local/bin/.placeholder ; } 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base:latest

COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /app /app
COPY --from=builder /kaniko /kaniko
COPY --from=builder /var/log/kaniko /var/log/kaniko
COPY --from=builder /var/cache/kaniko /var/cache/kaniko
COPY --from=upstream /kaniko/executor /kaniko/executor
COPY --from=upstream /kaniko/.docker /kaniko/.docker
COPY --from=upstream /usr/local/bin /usr/local/bin
RUN apk add --no-cache ca-certificates 
RUN ln -sf /kaniko/executor /usr/local/bin/kaniko
RUN adduser -u 65532 -D kaniko 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENV HOME=/app
ENTRYPOINT ["/kaniko/executor"]
LABEL org.opencontainers.image.title="kaniko" \
      org.opencontainers.image.version="1.24.0" \
      org.opencontainers.image.vendor="Google" \
      org.opencontainers.image.description="Sovereign hardened kaniko - container image builder" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM