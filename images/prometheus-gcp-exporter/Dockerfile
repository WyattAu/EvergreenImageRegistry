ARG VERSION=v0.16.7
ARG TARGETARCH

FROM gcr.io/google-containers/prometheus-to-sd:${VERSION} AS upstream

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/prometheus-gcp-exporter /var/cache/prometheus-gcp-exporter 2>/dev/null || true


FROM scratch
COPY --from=upstream /prometheus-to-sd /stackdriver-prometheus-sidecar
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/prometheus-gcp-exporter /var/log/prometheus-gcp-exporter
COPY --from=builder /var/cache/prometheus-gcp-exporter /var/cache/prometheus-gcp-exporter

WORKDIR /app

EXPOSE 9090
EXPOSE 9101

LABEL org.opencontainers.image.title="prometheus-gcp-exporter" org.opencontainers.image.version="0.10.0" org.opencontainers.image.vendor="Google Cloud Platform" org.opencontainers.image.description="Stackdriver Prometheus sidecar for GCP metrics" evergreen.image.tier="1" evergreen.constraint.nonroot="true" evergreen.constraint.scratch="true" evergreen.hft.signal-handling="native" evergreen.hft.shutdown-timeout="3s" evergreen.hft.init-system="none" evergreen.hft.startup-timeout="3000ms" evergreen.hft.cpu-pins="4-5" evergreen.hft.cpu-pins-mode="exclusive" evergreen.hft.deploy-strategy="hft-stateful" evergreen.hft.pre-stop-hook="true" evergreen.hft.pre-stop-delay="5s" evergreen.hft.connection-drain="true" evergreen.hft.sched-policy="SCHED_OTHER" \
      org.opencontainers.image.source="https://github.com/GoogleCloudPlatform/prometheus-to-sd"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK NONE
ENTRYPOINT ["/stackdriver-prometheus-sidecar"]
