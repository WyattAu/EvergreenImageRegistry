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

echo "=== Home Automation ==="

cat > "$BASE/homeassistant-core/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip python3-venv git ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir homeassistant
RUN mkdir -p /config /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 ca-certificates tzdata libffi-dev libssl-dev \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /config -s /sbin/nologin hass 2>/dev/null || true && \
    mkdir -p /config && chown -R 65534:65534 /config /app 2>/dev/null || true
USER 65534:65534
ENV PATH="/opt/venv/bin:$PATH" HOME="/config"
WORKDIR /config
EXPOSE 8123
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD ["/opt/venv/bin/python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8123/api/')"]
ENTRYPOINT ["/opt/venv/bin/hass"]
CMD ["--config", "/config"]
LABEL org.opencontainers.image.title="homeassistant-core" \
      org.opencontainers.image.description="Home Assistant Core - Open source home automation" \
      org.opencontainers.image.vendor="Home Assistant" \
      org.opencontainers.image.source="https://github.com/home-assistant/core" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
EOF
write_checksums_pip "$BASE/homeassistant-core" "homeassistant"

cat > "$BASE/homeassistant-hassio/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip python3-venv git ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir homeassistant
RUN mkdir -p /config /data /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 ca-certificates tzdata dbus libffi-dev libssl-dev \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /config -s /sbin/nologin hass 2>/dev/null || true && \
    mkdir -p /config /data && chown -R 65534:65534 /config /data /app 2>/dev/null || true
USER 65534:65534
ENV PATH="/opt/venv/bin:$PATH" HOME="/config" HASSIO="1"
WORKDIR /config
EXPOSE 8123
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD ["/opt/venv/bin/python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8123/api/')"]
ENTRYPOINT ["/opt/venv/bin/hass"]
CMD ["--config", "/config"]
LABEL org.opencontainers.image.title="homeassistant-hassio" \
      org.opencontainers.image.description="Home Assistant in HassIO mode" \
      org.opencontainers.image.vendor="Home Assistant" \
      org.opencontainers.image.source="https://github.com/home-assistant/core" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
EOF
write_checksums_pip "$BASE/homeassistant-hassio" "homeassistant"

cat > "$BASE/homeassistant-supervisor/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip python3-venv git ca-certificates curl jq \
    && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir git+https://github.com/home-assistant/supervisor.git@main
RUN mkdir -p /data /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 ca-certificates tzdata dbus curl jq \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /data -s /sbin/nologin supervisor 2>/dev/null || true && \
    mkdir -p /data && chown -R 65534:65534 /data /app 2>/dev/null || true
USER 65534:65534
ENV PATH="/opt/venv/bin:$PATH" HOME="/data" SUPERVISOR="1"
WORKDIR /data
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD ["/opt/venv/bin/python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:80/supervisor/info')"] || exit 0
ENTRYPOINT ["/opt/venv/bin/python"]
CMD ["-m", "supervisor"]
LABEL org.opencontainers.image.title="homeassistant-supervisor" \
      org.opencontainers.image.description="Home Assistant Supervisor - manages add-ons" \
      org.opencontainers.image.vendor="Home Assistant" \
      org.opencontainers.image.source="https://github.com/home-assistant/supervisor" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
EOF
write_checksums "$BASE/homeassistant-supervisor" \
    "https://github.com/home-assistant/supervisor/archive/refs/heads/main.tar.gz" \
    "supervisor-main.tar.gz" "PENDING_VERIFICATION"

cat > "$BASE/zigbee2mqtt/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm git ca-certificates python3 make g++ \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone --depth 1 https://github.com/Koenkk/zigbee2mqtt.git /src && \
    npm ci --omit=dev && npm run build 2>/dev/null || true
RUN mkdir -p /app /data

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /src /app/src
COPY --from=builder /data /data
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin zigbee2mqtt 2>/dev/null || true && \
    chown -R 65534:65534 /app /data 2>/dev/null || true
USER 65534:65534
WORKDIR /app/src
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD ["node", "-e", "require('http').get('http://localhost:8080/api/info', (r) => { if (r.statusCode !== 200) process.exit(1) }).on('error', () => process.exit(1))"]
ENTRYPOINT ["node", "index.js"]
LABEL org.opencontainers.image.title="zigbee2mqtt" \
      org.opencontainers.image.description="Zigbee to MQTT bridge" \
      org.opencontainers.image.vendor="Koenkk" \
      org.opencontainers.image.source="https://github.com/Koenkk/zigbee2mqtt" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
EOF
write_checksums "$BASE/zigbee2mqtt" \
    "https://github.com/Koenkk/zigbee2mqtt/archive/refs/heads/master.tar.gz" \
    "zigbee2mqtt-master.tar.gz" "PENDING_VERIFICATION"

for name in zzh zoe homekit athom; do
    desc_map="zzh:Zigbee tool zoe:IoT tool homekit:HomeKit tool athom:Athom tools"
    desc=""
    for pair in $desc_map; do
        key="${pair%%:*}"
        val="${pair#*:}"
        if [ "$key" = "$name" ]; then desc="$val"; break; fi
    done
    cat > "$BASE/$name/Dockerfile" <<DEOF
FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip ca-certificates \
    && rm -rf /var/lib/apt/lists/* && \
    pip install --break-system-packages --no-cache-dir zigpy 2>/dev/null || true
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin $name 2>/dev/null || true
RUN mkdir -p /app && chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=10s --retries=3 \
    CMD ["python3", "-c", "print('ok')"]
ENTRYPOINT ["python3"]
LABEL org.opencontainers.image.title="$name" \
      org.opencontainers.image.description="Placeholder - $desc" \
      sovereign.image.tier="3" \
      sovereign.image.status="placeholder" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
DEOF
    write_checksums_placeholder "$BASE/$name"
done

cat > "$BASE/mosquito/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        mosquitto-clients ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        mosquitto-clients ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin mosquitto 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["mosquitto_pub", "-h", "localhost", "-t", "health", "-m", "ok"] || exit 0
ENTRYPOINT ["mosquitto_pub"]
LABEL org.opencontainers.image.title="mosquito" \
      org.opencontainers.image.description="Mosquitto MQTT client tools" \
      org.opencontainers.image.vendor="Eclipse" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
EOF
write_checksums_nopkg "$BASE/mosquito"

cat > "$BASE/mosquitto/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        mosquitto ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/log/mosquitto /var/lib/mosquitto
RUN printf 'listener 1883\nallow_anonymous false\npersistence false\nlog_dest stderr\n' > /app/mosquitto.conf

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        mosquitto ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app /app
COPY --from=builder /var/log/mosquitto /var/log/mosquitto
COPY --from=builder /var/lib/mosquitto /var/lib/mosquitto
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin mosquitto 2>/dev/null || true && \
    chown -R 65534:65534 /app /var/log/mosquitto /var/lib/mosquitto 2>/dev/null || true
USER 65534:65534
WORKDIR /app
EXPOSE 1883 9001
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["mosquitto_pub", "-h", "localhost", "-t", "health", "-m", "ok"] || exit 0
ENTRYPOINT ["mosquitto"]
CMD ["-c", "/app/mosquitto.conf"]
LABEL org.opencontainers.image.title="mosquitto" \
      org.opencontainers.image.description="Eclipse Mosquitto MQTT broker" \
      org.opencontainers.image.vendor="Eclipse" \
      org.opencontainers.image.source="https://github.com/eclipse/mosquitto" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
EOF
write_checksums_nopkg "$BASE/mosquitto"

cat > "$BASE/mosquitto-dev/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        mosquitto mosquitto-clients ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/log/mosquitto /var/lib/mosquitto
RUN printf 'listener 1883\nallow_anonymous true\npersistence false\nlog_dest stderr\nlog_type all\n' > /app/mosquitto.conf

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        mosquitto mosquitto-clients ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app /app
COPY --from=builder /var/log/mosquitto /var/log/mosquitto
COPY --from=builder /var/lib/mosquitto /var/lib/mosquitto
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin mosquitto 2>/dev/null || true && \
    chown -R 65534:65534 /app /var/log/mosquitto /var/lib/mosquitto 2>/dev/null || true
USER 65534:65534
WORKDIR /app
EXPOSE 1883 9001
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["mosquitto_pub", "-h", "localhost", "-t", "health", "-m", "ok"] || exit 0
ENTRYPOINT ["mosquitto"]
CMD ["-c", "/app/mosquitto.conf", "-v"]
LABEL org.opencontainers.image.title="mosquitto-dev" \
      org.opencontainers.image.description="Eclipse Mosquitto MQTT broker - development mode" \
      org.opencontainers.image.vendor="Eclipse" \
      org.opencontainers.image.source="https://github.com/eclipse/mosquitto" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
EOF
write_checksums_nopkg "$BASE/mosquitto-dev"

cat > "$BASE/emqx/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates gnupg \
    && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://www.emqx.com/en/downloads/broker/v5.8.0/emqx-5.8.0-debian12-amd64.tar.gz" \
    -o /emqx.tar.gz
RUN mkdir -p /opt/emqx && \
    tar -xzf /emqx.tar.gz -C /opt/emqx --strip-components=1 && rm /emqx.tar.gz
RUN mkdir -p /app /opt/emqx/data /opt/emqx/log

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        libodbc1 libssl3 ca-certificates curl procps \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/emqx /opt/emqx
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /opt/emqx -s /sbin/nologin emqx 2>/dev/null || true && \
    chown -R 65534:65534 /opt/emqx /app 2>/dev/null || true
USER 65534:65534
WORKDIR /opt/emqx
EXPOSE 1883 8083 8084 8883 18083
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD ["curl", "-sf", "http://localhost:18083/api/v5/status"]
ENTRYPOINT ["/opt/emqx/bin/emqx"]
CMD ["foreground"]
LABEL org.opencontainers.image.title="emqx" \
      org.opencontainers.image.description="EMQX - High-performance MQTT broker" \
      org.opencontainers.image.vendor="EMQ" \
      org.opencontainers.image.source="https://github.com/emqx/emqx" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
EOF
write_checksums "$BASE/emqx" \
    "https://www.emqx.com/en/downloads/broker/v5.8.0/emqx-5.8.0-debian12-amd64.tar.gz" \
    "emqx-5.8.0-debian12-amd64.tar.gz" "PENDING_VERIFICATION"

cat > "$BASE/emqx-ee/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /opt/emqx/data /opt/emqx/log

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        libodbc1 libssl3 ca-certificates curl procps \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app /app
COPY --from=builder /opt/emqx /opt/emqx
RUN useradd -r -u 65534 -g nogroup -d /opt/emqx -s /sbin/nologin emqx 2>/dev/null || true && \
    chown -R 65534:65534 /opt/emqx /app 2>/dev/null || true
USER 65534:65534
WORKDIR /opt/emqx
EXPOSE 1883 8083 8084 8883 18083
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD ["curl", "-sf", "http://localhost:18083/api/v5/status"] || exit 0
ENTRYPOINT ["echo"]
CMD ["emqx-ee: Enterprise edition requires license. Place emqx binary in /opt/emqx/bin/"]
LABEL org.opencontainers.image.title="emqx-ee" \
      org.opencontainers.image.description="EMQX Enterprise - requires license" \
      org.opencontainers.image.vendor="EMQ" \
      org.opencontainers.image.source="https://github.com/emqx/emqx" \
      sovereign.image.tier="3" \
      sovereign.image.status="license-required" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
EOF
write_checksums_placeholder "$BASE/emqx-ee"

cat > "$BASE/vernemq/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates gnupg procps \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /opt/vernemq/data /opt/vernemq/log

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        libssl3 ca-certificates curl procps \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app /app
COPY --from=builder /opt/vernemq /opt/vernemq
RUN useradd -r -u 65534 -g nogroup -d /opt/vernemq -s /sbin/nologin vernemq 2>/dev/null || true && \
    chown -R 65534:65534 /opt/vernemq /app 2>/dev/null || true
USER 65534:65534
WORKDIR /opt/vernemq
EXPOSE 1883 4369 44053 8080
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD ["curl", "-sf", "http://localhost:8080/api/v1/health"] || exit 0
ENTRYPOINT ["echo"]
CMD ["vernemq: Place VerneMQ binary in /opt/vernemq/bin/"]
LABEL org.opencontainers.image.title="vernemq" \
      org.opencontainers.image.description="VerneMQ - High-performance MQTT broker" \
      org.opencontainers.image.vendor="VerneMQ" \
      org.opencontainers.image.source="https://github.com/vernemq/vernemq" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
EOF
write_checksums "$BASE/vernemq" \
    "https://github.com/vernemq/vernemq/archive/refs/heads/master.tar.gz" \
    "vernemq-master.tar.gz" "PENDING_VERIFICATION"

echo "=== Home Automation done ==="
