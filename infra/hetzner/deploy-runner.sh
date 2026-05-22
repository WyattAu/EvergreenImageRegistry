#!/usr/bin/env bash
# =============================================================================
# EVERGREEN REGISTRY - Deploy Gitea Act Runner on Hetzner CAX11 (ARM64)
# =============================================================================
# Run on the runner VM after provisioning.
# Usage: ssh root@<RUNNER_IP> 'bash -s' < deploy-runner.sh
# =============================================================================

set -euo pipefail

RUNNER_VERSION="v0.2.11"
RUNNER_DIR="/opt/act-runner"

echo "=== Deploying Gitea Act Runner ==="

# Install dependencies
apt-get update -qq
apt-get install -y -qq curl docker.io

# Enable Docker
systemctl enable docker
systemctl start docker

# Install act_runner
echo "Downloading act_runner $RUNNER_VERSION..."
curl -sL "https://gitea.com/gitea/act_runner/releases/download/${RUNNER_VERSION}/act_runner-linux-arm64" \
    -o /usr/local/bin/act_runner
chmod +x /usr/local/bin/act_runner

# Create runner directory
mkdir -p "$RUNNER_DIR"

# Register runner (requires GITHUB_RUNNER_TOKEN or GITEA_RUNNER_TOKEN)
# For GitHub Actions compatibility:
cat > "$RUNNER_DIR/config.yaml" << 'RUNNERCONFIG'
runner:
  file: .runner
  capacity: 2
  env_file: .env
  timeout: 360m
  shutdown_timeout: 30m

cache:
  enabled: true
  dir: ""
  host: ""
  port: 0

container:
  network: ""
  privileged: false
  options: ""
  workdir_parent: "/var/lib/act-runner"
  valid_volumes: []
  docker_host: ""

host:
  workdir_parent: "/var/lib/act-runner"
RUNNERCONFIG

echo ""
echo "=== Act Runner installed ==="
echo ""
echo "To register with GitHub:"
echo "  export RUNNER_TOKEN=<your-github-runner-token>"
echo "  act_runner register --instance https://github.com --token \$RUNNER_TOKEN --name evergreen-arm64 --labels arm64,linux-arm64"
echo ""
echo "To start:"
echo "  act_runner daemon --config $RUNNER_DIR/config.yaml"
echo ""
echo "For systemd service, create /etc/systemd/system/act-runner.service"
