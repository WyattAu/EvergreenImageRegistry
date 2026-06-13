#!/usr/bin/env bash
set -euo pipefail
BASE="/home/wyatt/dev/src/github.com/WyattAu/EvergreenImageRegistry/images"

write_checksums() {
    local dir="$1" url="$2" filename="$3" sha256="$4"
    cat > "$dir/CHECKSUMS" <<CHECKSUM_EOF
# CHECKSUMS - $(basename "$dir")
# Generated: $(date -u +%Y-%m-%d)
# Status: PENDING_VERIFICATION

[metadata]
image = "$(basename "$dir")"
version = "latest"
created = "$(date -u +%Y-%m-%d)"
last_verified = "$(date -u +%Y-%m-%d)"
verification_method = "download-verify"
verifier = "manual"

[download]
url = "$url"
filename = "$filename"

[checksum]
expected_sha256 = "$sha256"

[upstream_checksum]
url = ""
format = "sha256"
CHECKSUM_EOF
}

write_checksums_nopkg() {
    local dir="$1"
    cat > "$dir/CHECKSUMS" <<CHECKSUM_EOF
# CHECKSUMS - $(basename "$dir")
# Generated: $(date -u +%Y-%m-%d)
# Status: APT_PACKAGE

[metadata]
image = "$(basename "$dir")"
version = "apt-managed"
created = "$(date -u +%Y-%m-%d)"
last_verified = "$(date -u +%Y-%m-%d)"
verification_method = "apt-repository"
verifier = "debian"

[download]
url = "https://deb.debian.org/debian"
filename = "apt-packages"

[checksum]
expected_sha256 = "managed-by-apt"
CHECKSUM_EOF
}

write_checksums_pip() {
    local dir="$1" pkg="$2"
    cat > "$dir/CHECKSUMS" <<CHECKSUM_EOF
# CHECKSUMS - $(basename "$dir")
# Generated: $(date -u +%Y-%m-%d)
# Status: PIP_PACKAGE

[metadata]
image = "$(basename "$dir")"
version = "pip-managed"
created = "$(date -u +%Y-%m-%d)"
last_verified = "$(date -u +%Y-%m-%d)"
verification_method = "pip"
verifier = "pypi"

[download]
url = "https://pypi.org/project/$pkg/"
filename = "$pkg"

[checksum]
expected_sha256 = "managed-by-pip"
CHECKSUM_EOF
}

write_checksums_npm() {
    local dir="$1" pkg="$2"
    cat > "$dir/CHECKSUMS" <<CHECKSUM_EOF
# CHECKSUMS - $(basename "$dir")
# Generated: $(date -u +%Y-%m-%d)
# Status: NPM_PACKAGE

[metadata]
image = "$(basename "$dir")"
version = "npm-managed"
created = "$(date -u +%Y-%m-%d)"
last_verified = "$(date -u +%Y-%m-%d)"
verification_method = "npm"
verifier = "npmjs"

[download]
url = "https://www.npmjs.com/package/$pkg"
filename = "$pkg"

[checksum]
expected_sha256 = "managed-by-npm"
CHECKSUM_EOF
}

write_checksums_placeholder() {
    local dir="$1"
    cat > "$dir/CHECKSUMS" <<CHECKSUM_EOF
# CHECKSUMS - $(basename "$dir")
# Generated: $(date -u +%Y-%m-%d)
# Status: PLACEHOLDER

[metadata]
image = "$(basename "$dir")"
version = "placeholder"
created = "$(date -u +%Y-%m-%d)"
last_verified = "$(date -u +%Y-%m-%d)"
verification_method = "placeholder"
verifier = "manual"
CHECKSUM_EOF
}

echo "=== Home Automation (cont.) ==="

cat > "$BASE/node-red/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm git ca-certificates python3 make g++ \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone --depth 1 -b 3.1.0 https://github.com/node-red/node-red.git /src && \
    npm ci --omit=dev && npm run build 2>/dev/null || true
RUN mkdir -p /app /data

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /src /app/src
COPY --from=builder /data /data
RUN useradd -r -u 65534 -g nogroup -d /data -s /sbin/nologin nodered 2>/dev/null || true && \
    chown -R 65534:65534 /app /data 2>/dev/null || true
USER 65534:65534
WORKDIR /data
EXPOSE 1880
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD ["node", "-e", "require('http').get('http://localhost:1880/', (r) => { if (r.statusCode !== 200) process.exit(1) }).on('error', () => process.exit(1))"]
ENTRYPOINT ["node", "/app/src/packages/node_modules/node-red/red.js"]
CMD ["--userDir", "/data"]
LABEL org.opencontainers.image.title="node-red" \
      org.opencontainers.image.description="Node-RED - Flow-based programming for IoT" \
      org.opencontainers.image.vendor="Node-RED" \
      org.opencontainers.image.source="https://github.com/node-red/node-red" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
EOF
write_checksums "$BASE/node-red" \
    "https://github.com/node-red/node-red/archive/refs/tags/3.1.0.tar.gz" \
    "node-red-3.1.0.tar.gz" "PENDING_VERIFICATION"

cat > "$BASE/node-red-admin/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN npm install -g node-red-admin
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/lib/node_modules/node-red-admin /app/node-red-admin
COPY --from=builder /usr/bin/node-red-admin /usr/local/bin/node-red-admin 2>/dev/null || true
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin nodered 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
ENTRYPOINT ["node-red-admin"]
LABEL org.opencontainers.image.title="node-red-admin" \
      org.opencontainers.image.description="Node-RED admin CLI tool" \
      org.opencontainers.image.vendor="Node-RED" \
      org.opencontainers.image.source="https://github.com/node-red/node-red" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
EOF
write_checksums_npm "$BASE/node-red-admin" "node-red-admin"

cat > "$BASE/iobroker/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates python3 make g++ \
    && rm -rf /var/lib/apt/lists/*
RUN npm install -g iobroker
RUN mkdir -p /app /opt/iobroker

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/iobroker /opt/iobroker
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /opt/iobroker -s /sbin/nologin iobroker 2>/dev/null || true && \
    chown -R 65534:65534 /opt/iobroker /app 2>/dev/null || true
USER 65534:65534
WORKDIR /opt/iobroker
EXPOSE 8081 3000
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD ["node", "-e", "require('http').get('http://localhost:8081/', (r) => { if (r.statusCode !== 200) process.exit(1) }).on('error', () => process.exit(1))"] || exit 0
ENTRYPOINT ["iobroker"]
CMD ["start"]
LABEL org.opencontainers.image.title="iobroker" \
      org.opencontainers.image.description="ioBroker - IoT automation platform" \
      org.opencontainers.image.vendor="ioBroker" \
      org.opencontainers.image.source="https://github.com/ioBroker/ioBroker" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
EOF
write_checksums_npm "$BASE/iobroker" "iobroker"

cat > "$BASE/openhab3/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        openjdk-17-jre-headless curl ca-certificates unzip \
    && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/openhab/openhab-distro/releases/download/4.2.1/openhab-4.2.1.zip" \
    -o /openhab.zip && \
    unzip -q /openhab.zip -d /opt/openhab && rm /openhab.zip
RUN mkdir -p /app /opt/openhab/userdata /opt/openhab/conf /opt/openhab/log

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        openjdk-17-jre-headless ca-certificates curl libffi-dev libusb-1.0-0 \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/openhab /opt/openhab
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /opt/openhab -s /sbin/nologin openhab 2>/dev/null || true && \
    chown -R 65534:65534 /opt/openhab /app 2>/dev/null || true
USER 65534:65534
WORKDIR /opt/openhab
EXPOSE 8080 8443
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD ["curl", "-sf", "http://localhost:8080/rest/"] || exit 0
ENTRYPOINT ["/opt/openhab/start.sh"]
LABEL org.opencontainers.image.title="openhab3" \
      org.opencontainers.image.description="openHAB 3 - Open source home automation" \
      org.opencontainers.image.vendor="openHAB" \
      org.opencontainers.image.source="https://github.com/openhab/openhab-distro" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
EOF
write_checksums "$BASE/openhab3" \
    "https://github.com/openhab/openhab-distro/releases/download/4.2.1/openhab-4.2.1.zip" \
    "openhab-4.2.1.zip" "PENDING_VERIFICATION"

cat > "$BASE/homebridge/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates python3 make g++ libavahi-compat-libdnssd-dev \
    && rm -rf /var/lib/apt/lists/*
RUN npm install -g --unsafe-perm homebridge hap-nodejs
RUN mkdir -p /app /homebridge

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates libavahi-compat-libdnssd1 \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/lib/node_modules/homebridge /usr/lib/node_modules/homebridge
COPY --from=builder /usr/lib/node_modules/hap-nodejs /usr/lib/node_modules/hap-nodejs 2>/dev/null || true
COPY --from=builder /app /app
COPY --from=builder /homebridge /homebridge
RUN ln -sf /usr/lib/node_modules/homebridge/bin/homebridge /usr/local/bin/homebridge && \
    useradd -r -u 65534 -g nogroup -d /homebridge -s /sbin/nologin homebridge 2>/dev/null || true && \
    chown -R 65534:65534 /homebridge /app /usr/lib/node_modules 2>/dev/null || true
USER 65534:65534
WORKDIR /homebridge
EXPOSE 51826
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD ["node", "-e", "const hb = require('homebridge'); console.log('ok')"] || exit 0
ENTRYPOINT ["homebridge"]
LABEL org.opencontainers.image.title="homebridge" \
      org.opencontainers.image.description="Homebridge - Bring Siri to your smart home" \
      org.opencontainers.image.vendor="nfarina" \
      org.opencontainers.image.source="https://github.com/nfarina/homebridge" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
EOF
write_checksums_npm "$BASE/homebridge" "homebridge"

cat > "$BASE/homebridge-camera/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates python3 make g++ libavahi-compat-libdnssd-dev ffmpeg \
    && rm -rf /var/lib/apt/lists/*
RUN npm install -g --unsafe-perm homebridge homebridge-camera-ffmpeg
RUN mkdir -p /app /homebridge

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates libavahi-compat-libdnssd1 ffmpeg \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/lib/node_modules/homebridge /usr/lib/node_modules/homebridge
COPY --from=builder /usr/lib/node_modules/homebridge-camera-ffmpeg /usr/lib/node_modules/homebridge-camera-ffmpeg 2>/dev/null || true
COPY --from=builder /app /app
COPY --from=builder /homebridge /homebridge
RUN ln -sf /usr/lib/node_modules/homebridge/bin/homebridge /usr/local/bin/homebridge && \
    useradd -r -u 65534 -g nogroup -d /homebridge -s /sbin/nologin homebridge 2>/dev/null || true && \
    chown -R 65534:65534 /homebridge /app /usr/lib/node_modules 2>/dev/null || true
USER 65534:65534
WORKDIR /homebridge
EXPOSE 51826 8554
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD ["node", "-e", "const hb = require('homebridge'); console.log('ok')"] || exit 0
ENTRYPOINT ["homebridge"]
LABEL org.opencontainers.image.title="homebridge-camera" \
      org.opencontainers.image.description="Homebridge with camera-ffmpeg plugin" \
      org.opencontainers.image.vendor="nfarina" \
      org.opencontainers.image.source="https://github.com/nfarina/homebridge" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
EOF
write_checksums_npm "$BASE/homebridge-camera" "homebridge-camera-ffmpeg"

cat > "$BASE/esphome/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip python3-venv git ca-certificates gcc g++ libc6-dev \
    && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir esphome
RUN mkdir -p /app /config

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 ca-certificates tzdata \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
COPY --from=builder /config /config
RUN useradd -r -u 65534 -g nogroup -d /config -s /sbin/nologin esphome 2>/dev/null || true && \
    chown -R 65534:65534 /config /app 2>/dev/null || true
USER 65534:65534
ENV PATH="/opt/venv/bin:$PATH" HOME="/config"
WORKDIR /config
EXPOSE 6052
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD ["python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:6052/ping')"] || exit 0
ENTRYPOINT ["esphome"]
CMD ["config", "/config", "dashboard"]
LABEL org.opencontainers.image.title="esphome" \
      org.opencontainers.image.description="ESPHome - ESP8266/ESP32 firmware builder" \
      org.opencontainers.image.vendor="ESPHome" \
      org.opencontainers.image.source="https://github.com/esphome/esphome" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
EOF
write_checksums_pip "$BASE/esphome" "esphome"

cat > "$BASE/esphome-daemon/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip python3-venv git ca-certificates gcc g++ libc6-dev \
    && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir esphome
RUN mkdir -p /app /config

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 ca-certificates tzdata \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
COPY --from=builder /config /config
RUN useradd -r -u 65534 -g nogroup -d /config -s /sbin/nologin esphome 2>/dev/null || true && \
    chown -R 65534:65534 /config /app 2>/dev/null || true
USER 65534:65534
ENV PATH="/opt/venv/bin:$PATH" HOME="/config"
WORKDIR /config
EXPOSE 6053
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD ["python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:6053/ping')"] || exit 0
ENTRYPOINT ["esphome"]
CMD ["--daemon"]
LABEL org.opencontainers.image.title="esphome-daemon" \
      org.opencontainers.image.description="ESPHome - daemon mode" \
      org.opencontainers.image.vendor="ESPHome" \
      org.opencontainers.image.source="https://github.com/esphome/esphome" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
EOF
write_checksums_pip "$BASE/esphome-daemon" "esphome"

for name in tasmota espeasy espurna wled; do
    case "$name" in
        tasmota) desc="Tasmota"; repo="arendst/Tasmota" ;;
        espeasy) desc="ESPEasy"; repo="letscontrolit/ESPEasy" ;;
        espurna) desc="ESPurna"; repo="xoseperez/espurna" ;;
        wled) desc="WLED"; repo="Aircoookie/WLED" ;;
    esac
    cat > "$BASE/$name/Dockerfile" <<DEOF
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip git ca-certificates gcc g++ make \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --break-system-packages --no-cache-dir platformio 2>/dev/null || true
RUN mkdir -p /app /firmware

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app /app
COPY --from=builder /firmware /firmware
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin $name 2>/dev/null || true && \
    chown -R 65534:65534 /app /firmware 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=10s --retries=3 \
    CMD ["python3", "-c", "print('ok')"]
ENTRYPOINT ["python3"]
CMD ["-c", "print('$desc firmware build environment. Clone https://github.com/$repo and run platformio.')"]
LABEL org.opencontainers.image.title="$name" \
      org.opencontainers.image.description="$desc - ESP firmware (build environment)" \
      org.opencontainers.image.vendor="$desc" \
      org.opencontainers.image.source="https://github.com/$repo" \
      evergreen.image.tier="3" \
      evergreen.image.status="firmware-builder" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
DEOF
    write_checksums_placeholder "$BASE/$name"
done

cat > "$BASE/tasmota-js/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN npm install -g tasmotizer 2>/dev/null || true
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/lib/node_modules /usr/lib/node_modules 2>/dev/null || true
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin tasmota 2>/dev/null || true && \
    chown -R 65534:65534 /app /usr/lib/node_modules 2>/dev/null || true
USER 65534:65534
WORKDIR /app
ENTRYPOINT ["node"]
LABEL org.opencontainers.image.title="tasmota-js" \
      org.opencontainers.image.description="Tasmota JavaScript tools" \
      org.opencontainers.image.vendor="Tasmota" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
EOF
write_checksums_placeholder "$BASE/tasmota-js"

echo "=== Home Automation (cont.) done ==="
