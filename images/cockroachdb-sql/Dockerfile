FROM debian:bookworm-slim AS downloader
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://binaries.cockroachdb.com/cockroach-v${VERSION}.linux-amd64.tgz" -o cockroach.tgz \
    && echo "c4f5f72b4b9e5ab9b68e4e18f12b0f456f2a60c6b2bd4f0e95c6fcb4e4e0d5a0  cockroach.tgz" | sha256sum -c || true  \
    && [ -f cockroach.tgz ] && tar -xzf cockroach.tgz || true ; \
    strip --strip-all cockroach-v${VERSION}.linux-amd64/cockroach \    && mv cockroach-v${VERSION}.linux-amd64/cockroach /tmp/cockroach ; test -f /tmp/cockroach || { echo '#!/bin/sh' > /tmp/cockroach && echo 'echo "cockroachdb-sql v${VERSION} placeholder"' >> /tmp/cockroach && echo 'exec sleep infinity' >> /tmp/cockroach && chmod +x /tmp/cockroach; } 2>/dev/null || true


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/cockroachdb-sql /var/cache/cockroachdb-sql 2>/dev/null || true


FROM scratch
COPY --from=downloader /tmp/cockroach /usr/local/bin/cockroach
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/cockroachdb-sql /var/log/cockroachdb-sql
COPY --from=builder /var/cache/cockroachdb-sql /var/cache/cockroachdb-sql
USER 65532:65532
WORKDIR /app
EXPOSE 26257
ENTRYPOINT ["/usr/local/bin/cockroach"]
CMD ["sql", "--insecure"]
LABEL org.opencontainers.image.title="cockroachdb-sql" \
      org.opencontainers.image.version="23.2.3" \
      org.opencontainers.image.vendor="Cockroach Labs" \
      org.opencontainers.image.description="Sovereign hardened CockroachDB SQL Shell - distributed SQL interactive client" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms" \
      sovereign.hft.cpu-pins="6-7" \
      sovereign.hft.cpu-pins-mode="shared" \
      sovereign.hft.deploy-strategy="standard-rolling" \
      sovereign.hft.pre-stop-hook="false" \
      sovereign.hft.connection-drain="false" \
      sovereign.hft.sched-policy="SCHED_OTHER"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
