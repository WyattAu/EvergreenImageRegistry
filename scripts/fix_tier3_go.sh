#!/usr/bin/env bash
set -euo pipefail
BASE="/home/wyatt/dev/src/github.com/WyattAu/EvergreenImageRegistry/images"

fix_go_scratch() {
    local name="$1" desc="$2" vendor="$3" repo="$4" archive="$5" binary="$6" version="$7"
    local url="https://github.com/$repo/releases/download/v${version}/${archive}"
    cat > "$BASE/$name/Dockerfile" <<DEOF
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "$url" -o /$archive && \
    tar -xzf /$archive -C / && rm /$archive && chmod +x /$binary
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
}

fix_go_debian() {
    local name="$1" desc="$2" vendor="$3" repo="$4" archive="$5" binary="$6" version="$7"
    local url="https://github.com/$repo/releases/download/v${version}/${archive}"
    cat > "$BASE/$name/Dockerfile" <<DEOF
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "$url" -o /$archive && \
    tar -xzf /$archive -C / && rm /$archive && chmod +x /$binary
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
}

fix_go_scratch "trivy-alpine" "Trivy - vulnerability scanner (no Alpine)" "Aqua Security" "aquasecurity/trivy" "trivy_0.58.2_linux-amd64.tar.gz" "trivy" "0.58.2"
fix_go_debian "trivy-k8s" "Trivy - Kubernetes operator" "Aqua Security" "aquasecurity/trivy" "trivy_0.58.2_linux-amd64.tar.gz" "trivy" "0.58.2"
fix_go_debian "trivy-iac" "Trivy - IaC scanner" "Aqua Security" "aquasecurity/trivy" "trivy_0.58.2_linux-amd64.tar.gz" "trivy" "0.58.2"
fix_go_scratch "grype-alpine" "Grype - vulnerability scanner (no Alpine)" "Anchore" "anchore/grype" "grype_0.80.0_linux_amd64.tar.gz" "grype" "0.80.0"
fix_go_scratch "syft-alpine" "Syft - SBOM scanner (no Alpine)" "Anchore" "anchore/syft" "syft_1.11.0_linux_amd64.tar.gz" "syft" "1.11.0"
fix_go_scratch "govulncheck" "Go vulnerability checker" "golang" "golang/vuln" "govulncheck_1.1.0_linux_amd64.tar.gz" "govulncheck" "1.1.0"
fix_go_scratch "trufflehog" "TruffleHog - secret scanner" "trufflesecurity" "trufflesecurity/trufflehog" "trufflehog_3.82.2_linux_amd64.tar.gz" "trufflehog" "3.82.2"
fix_go_scratch "truffleshog" "TruffleHog - secret scanner (alias)" "trufflesecurity" "trufflesecurity/trufflehog" "trufflehog_3.82.2_linux_amd64.tar.gz" "trufflehog" "3.82.2"
fix_go_scratch "truffelsh" "TruffleHog - secret scanner (alias)" "trufflesecurity" "trufflesecurity/trufflehog" "trufflehog_3.82.2_linux_amd64.tar.gz" "trufflehog" "3.82.2"
fix_go_scratch "gitleaks" "Gitleaks - secret scanner" "gitleaks" "gitleaks/gitleaks" "gitleaks_8.21.2_linux_x64.tar.gz" "gitleaks" "8.21.2"
fix_go_scratch "kube-bench" "Kubernetes CIS benchmark" "aquasecurity" "aquasecurity/kube-bench" "kube-bench_0.8.0_linux_amd64.tar.gz" "kube-bench" "0.8.0"
fix_go_scratch "falcosidekick" "Falcosidekick - Falco webhook" "falcosecurity" "falcosecurity/falcosidekick" "falcosidekick_2.28.0_linux_amd64.tar.gz" "falcosidekick" "2.28.0"

fix_go_scratch "portainer-agent" "Portainer Agent for Docker" "Portainer" "portainer/agent" "portainer-agent-linux-amd64" "portainer-agent" "2.21.4"
fix_go_scratch "portainer-edge" "Portainer Edge Agent" "Portainer" "portainer/agent" "portainer-agent-edge-linux-amd64" "portainer-edge-agent" "2.21.4"

fix_go_scratch "docui" "Docker UI - lazydocker terminal UI" "jesseduffield" "jesseduffield/lazydocker" "lazydocker_0.12.0_Linux_x86_64.tar.gz" "lazydocker" "0.12.0"
fix_go_scratch "lazydocker" "Lazydocker - Terminal UI for Docker" "jesseduffield" "jesseduffield/lazydocker" "lazydocker_0.12.0_Linux_x86_64.tar.gz" "lazydocker" "0.12.0"

fix_go_debian "yacht" "Yacht - Docker management UI" "SelfhostedPro" "SelfhostedPro/Yacht" "yacht_2.2.2_linux_amd64.tar.gz" "yacht" "2.2.2"
fix_go_debian "lazydocker-ui" "Lazydocker - UI mode" "jesseduffield" "jesseduffield/lazydocker" "lazydocker_0.12.0_Linux_x86_64.tar.gz" "lazydocker" "0.12.0"

fix_go_debian "kubescape" "Kubescape - Kubernetes security" "kubescape" "kubescape/kubescape" "kubescape-ubuntu-latest-amd64" "kubescape" "3.0.3"
fix_go_debian "kubescape-operator" "Kubescape - operator mode" "kubescape" "kubescape/kubescape" "kubescape-ubuntu-latest-amd64" "kubescape" "3.0.3"

echo "=== Fixed all broken Go tar.gz Dockerfiles ==="
