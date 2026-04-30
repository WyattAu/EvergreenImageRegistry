ARG BUILD_DATE


FROM scratch
USER 65532:65532
LABEL org.opencontainers.image.title="wave" \
      sovereign.image.tier="2" \
      sovereign.image.category="business-finance" \
      sovereign.image.note="Placeholder image. SaaS-only product."

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="none"
EXPOSE 9101
STOPSIGNAL SIGTERM
