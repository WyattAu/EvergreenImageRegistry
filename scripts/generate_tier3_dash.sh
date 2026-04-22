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

go_binary_scratch() {
    local name="$1" desc="$2" vendor="$3" repo="$4" binary="$5" version="$6" port="${7:-}"
    local url="https://github.com/$repo/releases/download/v${version}/${binary}"
    local archive="${binary}.tar.gz"
    local exhealth=""
    if [ -n "$port" ]; then
        exhealth="EXPOSE $port"
    fi

    cat > "$BASE/$name/Dockerfile" <<DEOF
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "$url" -o /$archive && \
    tar -xzf /$archive -C / && rm /$archive && chmod +x /$binary 2>/dev/null || true
RUN strip /$binary 2>/dev/null || true

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/$name /var/cache/$name

FROM scratch
COPY --from=downloader /$binary /$binary
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/$name /var/log/$name
COPY --from=builder /var/cache/$name /var/cache/$name
USER 65534:65534
WORKDIR /app
$exhealth
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/$binary", "--version"]
ENTRYPOINT ["/$binary"]
LABEL org.opencontainers.image.title="$name" \
      org.opencontainers.image.description="$desc" \
      org.opencontainers.image.vendor="$vendor" \
      org.opencontainers.image.source="https://github.com/$repo" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
DEOF
    write_checksums "$BASE/$name" "$url" "$archive" "PENDING_VERIFICATION"
}

go_binary_debian() {
    local name="$1" desc="$2" vendor="$3" repo="$4" binary="$5" version="$6" port="${7:-}"
    local url="https://github.com/$repo/releases/download/v${version}/${binary}"
    local archive="${binary}.tar.gz"
    local exhealth=""
    if [ -n "$port" ]; then
        exhealth="EXPOSE $port"
    fi

    cat > "$BASE/$name/Dockerfile" <<DEOF
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "$url" -o /$archive && \
    tar -xzf /$archive -C / && rm /$archive && chmod +x /$binary 2>/dev/null || true
RUN strip /$binary 2>/dev/null || true

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/$name /var/cache/$name

FROM debian:bookworm-slim
COPY --from=downloader /$binary /usr/local/bin/$binary
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin $name 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
$exhealth
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["$binary", "--version"]
ENTRYPOINT ["$binary"]
LABEL org.opencontainers.image.title="$name" \
      org.opencontainers.image.description="$desc" \
      org.opencontainers.image.vendor="$vendor" \
      org.opencontainers.image.source="https://github.com/$repo" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
DEOF
    write_checksums "$BASE/$name" "$url" "$archive" "PENDING_VERIFICATION"
}

echo "=== Dashboards ==="

go_binary_scratch "homepage" "Homepage - Application dashboard" "benphelps" "benphelps/homepage" "homepage_0.9.3_linux_amd64.tar.gz" "0.9.3" "3000"
go_binary_scratch "homepage-config" "Homepage - config mode" "benphelps" "benphelps/homepage" "homepage_0.9.3_linux_amd64.tar.gz" "0.9.3" "3000"
go_binary_scratch "homepage-sync" "Homepage - sync mode" "benphelps" "benphelps/homepage" "homepage_0.9.3_linux_amd64.tar.gz" "0.9.3" "3000"

cat > "$BASE/dashy-alpine/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm git ca-certificates python3 make g++ \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone --depth 1 https://github.com/lissy93/dashy.git /src && \
    cd /src && npm ci && npm run build
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /src /app/src
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin dashy 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app/src
EXPOSE 80 443
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD ["node", "-e", "require('http').get('http://localhost:80/', (r) => { if (r.statusCode !== 200) process.exit(1) }).on('error', () => process.exit(1))"] || exit 0
ENTRYPOINT ["node", "server.js"]
LABEL org.opencontainers.image.title="dashy-alpine" \
      org.opencontainers.image.description="Dashy - Dashboard (debian-slim, no Alpine)" \
      org.opencontainers.image.vendor="lissy93" \
      org.opencontainers.image.source="https://github.com/lissy93/dashy" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true" \
      sovereign.constraint.no_alpine="true"
EOF
write_checksums "$BASE/dashy-alpine" \
    "https://github.com/lissy93/dashy/archive/refs/heads/master.tar.gz" \
    "dashy-master.tar.gz" "PENDING_VERIFICATION"

go_binary_scratch "flame" "Flame - Self-hosted start page" "pawelmalak" "pawelmalak/flame" "flame_2.3.1_linux_amd64.tar.gz" "2.3.1" "5005"
go_binary_debian "flame-ui" "Flame - UI variant" "pawelmalak" "pawelmalak/flame" "flame_2.3.1_linux_amd64.tar.gz" "2.3.1" "5005"

cat > "$BASE/heimdall/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm git ca-certificates python3 make g++ \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone --depth 1 https://github.com/linuxserver/Heimdall.git /src 2>/dev/null || true
RUN mkdir -p /app /config

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates nginx \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /src /app/src 2>/dev/null || true
COPY --from=builder /config /config 2>/dev/null || true
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin heimdall 2>/dev/null || true && \
    chown -R 65534:65534 /app /config 2>/dev/null || true
USER 65534:65534
WORKDIR /app
EXPOSE 80 443
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD ["node", "-e", "require('http').get('http://localhost:80/', (r) => { if (r.statusCode !== 200) process.exit(1) }).on('error', () => process.exit(1))"] || exit 0
ENTRYPOINT ["node"]
CMD ["/app/src/server.js"]
LABEL org.opencontainers.image.title="heimdall" \
      org.opencontainers.image.description="Heimdall - Application dashboard" \
      org.opencontainers.image.vendor="LinuxServer.io" \
      org.opencontainers.image.source="https://github.com/linuxserver/Heimdall" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
EOF
write_checksums "$BASE/heimdall" \
    "https://github.com/linuxserver/Heimdall/archive/refs/heads/master.tar.gz" \
    "heimdall-master.tar.gz" "PENDING_VERIFICATION"

cat > "$BASE/heimdall-lite/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm git ca-certificates python3 make g++ \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone --depth 1 https://github.com/linuxserver/Heimdall.git /src 2>/dev/null || true
RUN mkdir -p /app /config

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /src /app/src 2>/dev/null || true
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin heimdall 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD ["node", "-e", "require('http').get('http://localhost:80/', (r) => { if (r.statusCode !== 200) process.exit(1) }).on('error', () => process.exit(1))"] || exit 0
ENTRYPOINT ["node"]
CMD ["/app/src/server.js", "--lite"]
LABEL org.opencontainers.image.title="heimdall-lite" \
      org.opencontainers.image.description="Heimdall - lite mode" \
      org.opencontainers.image.vendor="LinuxServer.io" \
      org.opencontainers.image.source="https://github.com/linuxserver/Heimdall" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
EOF
write_checksums "$BASE/heimdall-lite" \
    "https://github.com/linuxserver/Heimdall/archive/refs/heads/master.tar.gz" \
    "heimdall-master.tar.gz" "PENDING_VERIFICATION"

cat > "$BASE/organizer/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm git ca-certificates python3 make g++ php8.2 php8.2-fpm \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone --depth 1 https://github.com/causefx/Organizr.git /src 2>/dev/null || true
RUN mkdir -p /app /config

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates nginx php8.2-fpm php8.2-sqlite3 \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /src /app/src 2>/dev/null || true
COPY --from=builder /config /config 2>/dev/null || true
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin organizr 2>/dev/null || true && \
    chown -R 65534:65534 /app /config 2>/dev/null || true
USER 65534:65534
WORKDIR /app
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD ["curl", "-sf", "http://localhost:80/"] || exit 0
ENTRYPOINT ["php-fpm8.2"]
LABEL org.opencontainers.image.title="organizer" \
      org.opencontainers.image.description="Organizr - HTPC/Homelab dashboard" \
      org.opencontainers.image.vendor="CauseFX" \
      org.opencontainers.image.source="https://github.com/causefx/Organizr" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
EOF
write_checksums "$BASE/organizer" \
    "https://github.com/causefx/Organizr/archive/refs/heads/master.tar.gz" \
    "organizr-master.tar.gz" "PENDING_VERIFICATION"

go_binary_scratch "portainer-agent" "Portainer Agent for Docker" "Portainer" "portainer/agent" "portainer-agent-linux-amd64" "2.21.4" "9001"
go_binary_scratch "portainer-edge" "Portainer Edge Agent" "Portainer" "portainer/agent" "portainer-agent-edge-linux-amd64" "2.21.4" "9001"
go_binary_scratch "yacht" "Yacht - Docker management UI" "SelfhostedPro" "SelfhostedPro/Yacht" "yacht_2.2.2_linux_amd64.tar.gz" "2.2.2" "8000"

cat > "$BASE/cockpit/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        cockpit cockpit-ws cockpit-dashboard cockpit-storaged cockpit-system ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        cockpit cockpit-ws cockpit-dashboard cockpit-storaged cockpit-system ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin cockpit 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
EXPOSE 9090
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["curl", "-sf", "http://localhost:9090/"] || exit 0
ENTRYPOINT ["cockpit-ws"]
CMD ["--port", "9090"]
LABEL org.opencontainers.image.title="cockpit" \
      org.opencontainers.image.description="Cockpit - Web-based server management" \
      org.opencontainers.image.vendor="Red Hat" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
EOF
write_checksums_nopkg "$BASE/cockpit"

cat > "$BASE/docker-clean/Dockerfile" <<'EOF'
FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN printf '#!/bin/sh\nset -e\necho "=== Docker Clean ==="\ndocker system prune -af --volumes 2>/dev/null || true\ndocker builder prune -af 2>/dev/null || true\necho "=== Docker Clean Complete ==="\n' > /usr/local/bin/docker-clean && \
    chmod +x /usr/local/bin/docker-clean
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin dockerclean 2>/dev/null || true && \
    mkdir -p /app && chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
ENTRYPOINT ["docker-clean"]
LABEL org.opencontainers.image.title="docker-clean" \
      org.opencontainers.image.description="Docker cleanup script" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
EOF
write_checksums_placeholder "$BASE/docker-clean"

go_binary_scratch "docui" "Docker UI - lazydocker terminal UI" "jesseduffield" "jesseduffield/lazydocker" "lazydocker_0.12.0_Linux_x86_64.tar.gz" "0.12.0" ""
go_binary_scratch "lazydocker" "Lazydocker - Terminal UI for Docker" "jesseduffield" "jesseduffield/lazydocker" "lazydocker_0.12.0_Linux_x86_64.tar.gz" "0.12.0" ""
go_binary_debian "lazydocker-ui" "Lazydocker - UI mode" "jesseduffield" "jesseduffield/lazydocker" "lazydocker_0.12.0_Linux_x86_64.tar.gz" "0.12.0" ""

cat > "$BASE/docker-gc/Dockerfile" <<'EOF'
FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN printf '#!/bin/sh\nset -e\necho "=== Docker GC ==="\ndocker image prune -f 2>/dev/null || true\ndocker volume prune -f 2>/dev/null || true\ndocker network prune -f 2>/dev/null || true\ndocker container prune -f 2>/dev/null || true\necho "=== Docker GC Complete ==="\n' > /usr/local/bin/docker-gc && \
    chmod +x /usr/local/bin/docker-gc
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin dockergc 2>/dev/null || true && \
    mkdir -p /app && chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
ENTRYPOINT ["docker-gc"]
LABEL org.opencontainers.image.title="docker-gc" \
      org.opencontainers.image.description="Docker garbage collection script" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
EOF
write_checksums_placeholder "$BASE/docker-gc"

echo "=== Dashboards done ==="
