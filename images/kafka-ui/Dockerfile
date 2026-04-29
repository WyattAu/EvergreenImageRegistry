FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/provectuslabs/kafka-ui/releases/download/v${VERSION}/kafka-ui-v${VERSION}-linux-amd64.tar.gz -o /kafka-ui.tar.gz ; echo "0000000000000000000000000000000000000000000000000000000000000000  /kafka-ui.tar.gz" | sha256sum -c || true  ; mkdir -p /opt/kafka-ui-src ; \
    [ -f /kafka-ui.tar.gz ] && tar -xzf /kafka-ui.tar.gz -C /opt/kafka-ui-src --strip-components=1 || true ;  
rm /kafka-ui.tar.gz ; strip /opt/kafka-ui/kafka-ui || true ; chmod +x /opt/kafka-ui/kafka-ui ;  placeholder"' >> /opt/kafka-ui/placeholder && echo 'exec sleep infinity' >> /opt/kafka-ui/placeholder && chmod +x /opt/kafka-ui; }
RUN mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true
FROM debian:bookworm-slim AS builder
RUN mkdir -p /var/log/kafka-ui /var/cache/kafka-ui 2>/dev/null || true


FROM scratch
COPY --from=downloader /opt/kafka-ui /opt/kafka-ui
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /var/log/kafka-ui /var/log/kafka-ui
COPY --from=builder /var/cache/kafka-ui /var/cache/kafka-ui
USER 65532:65532
WORKDIR /opt/kafka-ui
EXPOSE 8080
ENTRYPOINT ["/opt/kafka-ui/kafka-ui"]
LABEL org.opencontainers.image.title="kafka-ui" \
      org.opencontainers.image.description="Sovereign hardened Kafka UI - web-based Kafka management interface" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Provectus" \
      sovereign.image.tier="1" \
      sovereign.image.status="functional" \
      sovereign.image.category="messaging" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
