# UNBOUND-EXPORTER - ARCHIVED
# The prometheus-community/unbound_exporter repo has been removed.
# No maintained alternative is available.
# See: https://github.com/prometheus-community/unbound_exporter

FROM scratch
USER 65532:65532
LABEL org.opencontainers.image.title="unbound-exporter" \
      sovereign.image.status="archived" \
      sovereign.image.note="Upstream repo removed, no maintained alternative available"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="none"
EXPOSE 9101
STOPSIGNAL SIGTERM
