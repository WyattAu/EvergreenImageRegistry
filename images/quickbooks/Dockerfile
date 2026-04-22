ARG VERSION=placeholder
ARG BUILD_DATE

FROM scratch
LABEL org.opencontainers.image.title="quickbooks" \
      org.opencontainers.image.version="placeholder" \
      org.opencontainers.image.description="QuickBooks (proprietary)" \
      sovereign.image.tier="2" \
      sovereign.image.category="business-finance" \
      sovereign.image.status="placeholder" \
      sovereign.image.note="Proprietary software. No open-source container image available."

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="none"
EXPOSE 9101
STOPSIGNAL SIGTERM
