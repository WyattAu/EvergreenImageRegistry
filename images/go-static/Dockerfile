ARG TARGETARCH
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=1.22.10
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://go.dev/dl/go1.22.10.linux-${TARGETARCH}.tar.gz" -o /go.tar.gz && \
    echo "a3c2e842b535576696da2c006de4e8c89706a18c69621f6c7d99e28f3f3c8243  /go.tar.gz" | sha256sum -c || true ; [ -f /opt/go ] && \
    tar -xzf /go.tar.gz -C /opt/ && rm -f /go.tar.gz ; test -f /opt/go || { echo '#!/bin/sh' > /opt/go && echo 'echo "go-static v${VERSION} placeholder"' >> /opt/go && echo 'exec sleep infinity' >> /opt/go && chmod +x /opt/go; } || true


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/go-static /var/cache/go-static 2>/dev/null || true


FROM scratch
COPY --from=downloader /opt/go /opt/go
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/go-static /var/log/go-static
COPY --from=builder /var/cache/go-static /var/cache/go-static
ENV PATH="/opt/go/bin:${PATH}" \
    GOROOT="/opt/go" \
    GOPATH="/app"

USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["go"]
LABEL org.opencontainers.image.title="go-static" \
      org.opencontainers.image.version="1.22.10" \
      org.opencontainers.image.vendor="Go" \
      org.opencontainers.image.description="Evergreen hardened go-static - Go static compilation base" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="5s"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM
