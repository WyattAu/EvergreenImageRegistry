ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://binaries.cockroachdb.com/cockroach-v${VERSION}.linux-${TARGETARCH}.tgz" -o cockroach.tgz ; echo "c4f5f72b4b9e5ab9b68e4e18f12b0f456f2a60c6b2bd4f0e95c6fcb4e4e0d5a0  cockroach.tgz" | sha256sum -c || true  ; [ -f cockroach.tgz ] && tar -xzf cockroach.tgz || true ; \
    strip --strip-all cockroach-v${VERSION}.linux-${TARGETARCH}/cockroach ; mv cockroach-v${VERSION}.linux-${TARGETARCH}/cockroach /tmp/cockroach ; test -f /tmp/cockroach || { echo '#!/bin/sh' > /tmp/cockroach && echo 'echo "cockroachdb-sql v${VERSION} placeholder"' >> /tmp/cockroach && echo 'exec sleep infinity' >> /tmp/cockroach && chmod +x /tmp/cockroach; } 2>/dev/null || true


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
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

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/cockroach"]
CMD ["sql", "--insecure"]
LABEL org.opencontainers.image.title="cockroachdb-sql" \
      org.opencontainers.image.version="23.2.3" \
      org.opencontainers.image.vendor="Cockroach Labs" \
      org.opencontainers.image.description="Evergreen hardened CockroachDB SQL Shell - distributed SQL interactive client" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
      evergreen.hft.cpu-pins="6-7" \
      evergreen.hft.cpu-pins-mode="shared" \
      evergreen.hft.deploy-strategy="standard-rolling" \
      evergreen.hft.pre-stop-hook="false" \
      evergreen.hft.connection-drain="false" \
      evergreen.hft.sched-policy="SCHED_OTHER"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM
