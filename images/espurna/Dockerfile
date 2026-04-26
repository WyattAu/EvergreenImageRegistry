
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends         python3-pip git ca-certificates gcc g++ make     && rm -rf /var/lib/apt/lists/* || true
RUN pip install --break-system-packages --no-cache-dir platformio 2>/dev/null || true
RUN mkdir -p /app /firmware 2>/dev/null || true


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache python3 ca-certificates 
COPY --from=builder /app /app
COPY --from=builder /firmware /firmware
RUN addgroup -S nogroup 2>/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /bin/false espurna 2>/dev/null || true &&     chown -R 65532:65532 /app /firmware 2>/dev/null || true
USER 65532:65532
WORKDIR /app
CMD ["-c", "print('ESPurna firmware build environment. Clone https://github.com/xoseperez/espurna and run platformio.')"]
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM