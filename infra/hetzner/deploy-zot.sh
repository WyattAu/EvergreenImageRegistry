#!/usr/bin/env bash
# =============================================================================
# EVERGREEN REGISTRY - Deploy Zot on Hetzner CX22
# =============================================================================
# Run on the Zot registry VM after provisioning.
# Usage: ssh root@<REGISTRY_IP> 'bash -s' < deploy-zot.sh
# =============================================================================

set -euo pipefail

ZOT_VERSION="v2.1.1"
ZOT_DIR="/opt/zot"
ZOT_CONFIG="$ZOT_DIR/config.json"
ZOT_DATA="/var/lib/zot"
ZOT_USER="zot"

echo "=== Deploying Zot Registry ==="

# Install dependencies
apt-get update -qq
apt-get install -y -qq curl nginx certbot python3-certbot-nginx

# Create zot user
id -u $ZOT_USER &>/dev/null || useradd -r -s /bin/false $ZOT_USER

# Create directories
mkdir -p "$ZOT_DIR" "$ZOT_DATA"
chown -R $ZOT_USER:$ZOT_USER "$ZOT_DIR" "$ZOT_DATA"

# Download Zot
echo "Downloading Zot $ZOT_VERSION..."
curl -sL "https://github.com/project-zot/zot/releases/download/${ZOT_VERSION}/zot-linux-amd64" \
    -o /usr/local/bin/zot
chmod +x /usr/local/bin/zot

# Generate Zot config
cat > "$ZOT_CONFIG" << 'ZOTCONFIG'
{
  "distSpecVersion": "1.1.1",
  "storage": {
    "rootDirectory": "/var/lib/zot",
    "gc": true,
    "gcInterval": "24h",
    "gcDelay": "1h"
  },
  "http": {
    "address": "127.0.0.1",
    "port": "5000",
    "realm": "Evergreen Registry",
    "auth": {
      "htpasswd": {
        "path": "/opt/zot/htpasswd"
      }
    },
    "accessControl": {
      "groups": {
        "admins": {
          "users": ["admin"]
        }
      },
      "repositories": {
        "**": {
          "defaultPolicy": ["read"],
          "admins": ["read", "create", "update", "delete"]
        }
      },
      "adminPolicy": {
        "users": ["admin"],
        "actions": ["read", "create", "update", "delete"]
      }
    }
  },
  "log": {
    "level": "info",
    "output": "/var/log/zot/zot.log"
  },
  "extensions": {
    "search": {
      "enable": true,
      "cve": {
        "updateInterval": "24h"
      }
    },
    "ui": {
      "enable": true
    },
    "metrics": {
      "enable": true,
      "prometheus": {
        "path": "/metrics"
      }
    }
  }
}
ZOTCONFIG

# Generate htpasswd (admin password will be set on first run)
echo "admin:\$2y\$10\$placeholder" > /opt/zot/htpasswd
echo "NOTE: Run 'htpasswd -B /opt/zot/htpasswd admin' to set admin password"

# Create systemd service
cat > /etc/systemd/system/zot.service << 'SYSTEMD'
[Unit]
Description=Zot OCI Registry
After=network.target

[Service]
Type=simple
User=zot
Group=zot
ExecStart=/usr/local/bin/zot serve /opt/zot/config.json
Restart=always
RestartSec=5
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
SYSTEMD

# Create log directory
mkdir -p /var/log/zot
chown $ZOT_USER:$ZOT_USER /var/log/zot

# Enable and start
systemctl daemon-reload
systemctl enable zot
systemctl start zot

echo ""
echo "=== Zot deployed ==="
echo "Listening on: http://127.0.0.1:5000"
echo "UI: http://127.0.0.1:5000/ui/"
echo "Metrics: http://127.0.0.1:5000/metrics"
echo ""
echo "Next steps:"
echo "1. Set admin password: htpasswd -B /opt/zot/htpasswd admin"
echo "2. Configure nginx reverse proxy"
echo "3. Set up Cloudflare Tunnel"
