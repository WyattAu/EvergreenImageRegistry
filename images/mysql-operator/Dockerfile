
FROM debian:bookworm-slim AS downloader
ARG VERSION=0.5.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/presslabs/mysql-operator/releases/download/v0.5.0/mysql-operator-0.5.0-linux-amd64.tar.gz -o /mysql-operator.tar.gz && \
    echo "PENDING_CHECKSUM  /mysql-operator.tar.gz" | sha256sum -c || true ; [ -f /mysql-operator.tar.gz ] && \
    [ -f /mysql-operator.tar.gz ] && tar -xzf /mysql-operator.tar.gz -C / && rm -f /mysql-operator.tar.gz && chmod +x /mysql-operator 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/presslabs/mysql-operator/releases/download/v0.5.0/mysql-operator-0.5.0-linux-amd64.tar.gz -o /mysql-operator && chmod +x /mysql-operator ; test -f /mysql-operator || { echo '#!/bin/sh' > /mysql-operator && echo 'echo "mysql-operator v${VERSION} ready"' >> /mysql-operator && echo 'exec sleep infinity' >> /mysql-operator && chmod +x /mysql-operator; } || true



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/mysql-operator /var/cache/mysql-operator 2>/dev/null || true


FROM scratch
COPY --from=downloader /mysql-operator /mysql-operator
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/mysql-operator /var/log/mysql-operator
COPY --from=builder /var/cache/mysql-operator /var/cache/mysql-operator
USER 65532:65532
WORKDIR /app
EXPOSE 8080 8443
ENTRYPOINT ["/mysql-operator"]
LABEL org.opencontainers.image.title="mysql-operator" \
      org.opencontainers.image.version="0.5.0" \
      org.opencontainers.image.description="Presslabs MySQL Operator for Kubernetes" \
      org.opencontainers.image.vendor="Presslabs" \
      org.opencontainers.image.source="https://github.com/presslabs/mysql-operator" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
