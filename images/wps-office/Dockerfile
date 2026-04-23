ARG BUILD_DATE


FROM scratch
LABEL org.opencontainers.image.title="wps-office" \
      org.opencontainers.image.description="WPS Office (proprietary)" \
      sovereign.image.tier="2" \
      sovereign.image.category="document-management" \
      sovereign.image.note="Proprietary software. No open-source container image available."

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="none"
EXPOSE 9101
STOPSIGNAL SIGTERM
