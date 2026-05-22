#!/usr/bin/env bash
# =============================================================================
# EVERGREEN REGISTRY - Hetzner Infrastructure Provisioning
# =============================================================================
# Prerequisites:
#   - hcloud CLI installed (https://github.com/hetznercloud/cli)
#   - HCLOUD_TOKEN set in environment
#   - SSH public key at ~/.ssh/id_ed25519.pub
#
# Creates:
#   - CX22 (amd64) for Zot registry
#   - CAX11 (arm64) for Gitea Act Runner
#   - Object Storage for image layers
#   - Firewall rules
#   - Cloudflare Tunnel integration
# =============================================================================

set -euo pipefail

SSH_KEY_FILE="${SSH_KEY_FILE:-$HOME/.ssh/id_ed25519.pub}"
REGION="${REGION:-fsn1}"  # Frankfurt
SSH_KEY_NAME="evergreen-admin"

echo "=== Evergreen Hetzner Provisioning ==="
echo "Region: $REGION"
echo ""

# Verify prerequisites
if [ -z "${HCLOUD_TOKEN:-}" ]; then
    echo "ERROR: HCLOUD_TOKEN not set"
    echo "Create token at: https://console.hetzner.cloud/ -> Security -> API Tokens"
    echo "Required permissions: Read & Write for Servers, Volumes, Networks, Firewalls, SSH Keys"
    exit 1
fi

if [ ! -f "$SSH_KEY_FILE" ]; then
    echo "ERROR: SSH key not found at $SSH_KEY_FILE"
    exit 1
fi

# Create context
hcloud context create evergreen 2>/dev/null || hcloud context use evergreen

# Upload SSH key
echo "--- Uploading SSH key ---"
hcloud ssh-key create --name "$SSH_KEY_NAME" --public-key-from-file "$SSH_KEY_FILE" 2>/dev/null || \
    echo "SSH key already exists (ok)"

# Create firewall
echo "--- Creating firewall ---"
hcloud firewall create --name evergreen-registry --rules-file=- << 'EOF' 2>/dev/null || echo "Firewall exists (ok)"
[
  {"direction":"in","protocol":"tcp","port":22,"source_ips":["0.0.0.0/0","::/0"],"description":"SSH"},
  {"direction":"in","protocol":"tcp","port":443,"source_ips":["0.0.0.0/0","::/0"],"description":"HTTPS"},
  {"direction":"in","protocol":"tcp","port":80,"source_ips":["0.0.0.0/0","::/0"],"description":"HTTP"},
  {"direction":"in","protocol":"tcp","port":5000,"source_ips":["0.0.0.0/0","::/0"],"description":"Zot Registry"},
  {"direction":"in","protocol":"icmp","source_ips":["0.0.0.0/0","::/0"],"description":"ICMP"}
]
EOF

# Create CX22 for Zot registry
echo "--- Creating Zot registry VM (CX22) ---"
REGISTRY_ID=$(hcloud server create \
    --name evergreen-registry \
    --type cx22 \
    --image debian-12 \
    --location "$REGION" \
    --ssh-key "$SSH_KEY_NAME" \
    --firewall evergreen-registry \
    --output-format=json 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin)['server']['id'])" 2>/dev/null || echo "exists")

if [ "$REGISTRY_ID" = "exists" ]; then
    echo "Registry VM already exists"
    REGISTRY_IP=$(hcloud server ip evergreen-registry)
else
    echo "Created registry VM: $REGISTRY_ID"
    REGISTRY_IP=$(hcloud server ip evergreen-registry)
fi
echo "Registry IP: $REGISTRY_IP"

# Create CAX11 for CI runner (ARM64)
echo "--- Creating CI runner VM (CAX11 ARM64) ---"
RUNNER_ID=$(hcloud server create \
    --name evergreen-runner \
    --type cax11 \
    --image debian-12 \
    --location "$REGION" \
    --ssh-key "$SSH_KEY_NAME" \
    --firewall evergreen-registry \
    --output-format=json 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin)['server']['id'])" 2>/dev/null || echo "exists")

if [ "$RUNNER_ID" = "exists" ]; then
    echo "Runner VM already exists"
    RUNNER_IP=$(hcloud server ip evergreen-runner)
else
    echo "Created runner VM: $RUNNER_ID"
    RUNNER_IP=$(hcloud server ip evergreen-runner)
fi
echo "Runner IP: $RUNNER_IP"

echo ""
echo "=== Provisioning Complete ==="
echo "Registry (CX22): $REGISTRY_IP"
echo "Runner (CAX11): $RUNNER_IP"
echo ""
echo "Next steps:"
echo "1. ssh root@$REGISTRY_IP  # Deploy Zot"
echo "2. ssh root@$RUNNER_IP    # Deploy Gitea Act Runner"
echo "3. Configure Cloudflare Tunnel"
