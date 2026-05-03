
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        mosquitto ca-certificates ; rm -rf /var/lib/apt/lists/* || true

RUN mkdir -p /app /var/log/mosquitto /var/lib/mosquitto 2>/dev/null || true
RUN printf 'listener 1883\nallow_anonymous false\npersistence false\nlog_dest stderr\n' > /app/mosquitto.conf


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache mosquitto ca-certificates || true
COPY --from=builder /app /app
COPY --from=builder /var/log/mosquitto /var/log/mosquitto
COPY --from=builder /var/lib/mosquitto /var/lib/mosquitto
RUN addgroup -S -g 2 nogroup >/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /bin/false mosquitto 2>/dev/null || true && \
    chown -R 65532:65532 /app /var/log/mosquitto /var/lib/mosquitto 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 1883 9001

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:1883/ || exit 1
ENTRYPOINT ["mosquitto"]
CMD ["-c", "/app/mosquitto.conf"]
LABEL org.opencontainers.image.title="mosquitto" \
      org.opencontainers.image.description="Eclipse Mosquitto MQTT broker" \
      org.opencontainers.image.vendor="Eclipse" \
      org.opencontainers.image.source="https://github.com/eclipse/mosquitto" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM
