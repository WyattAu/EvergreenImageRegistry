#!/usr/bin/env bash
# =============================================================================
# Install EIR Metrics Exporter as a systemd service
# =============================================================================
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
INSTALL_DIR="/opt/evergreen-image-registry"
SERVICE_NAME="eir-metrics"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

echo "=== Installing EIR Metrics Exporter ==="

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Error: Must run as root (sudo)"
    exit 1
fi

# Create service user
if ! id -u eir-metrics >/dev/null 2>&1; then
    echo "Creating eir-metrics user..."
    useradd --system --no-create-home --shell /usr/sbin/nologin eir-metrics
fi

# Install files
echo "Installing to ${INSTALL_DIR}..."
mkdir -p "$INSTALL_DIR"
cp "$REPO_ROOT/scripts/export_metrics.py" "$INSTALL_DIR/"
cp "$REPO_ROOT/monitoring/eir-metrics.service" "$SERVICE_FILE"

# Create symlinks for images directory
if [ ! -L "$INSTALL_DIR/images" ]; then
    ln -sf "$REPO_ROOT/images" "$INSTALL_DIR/images"
fi

# Create symlinks for compliance directory
if [ ! -L "$INSTALL_DIR/compliance" ]; then
    ln -sf "$REPO_ROOT/compliance" "$INSTALL_DIR/compliance"
fi

# Create symlinks for workflows directory
if [ ! -L "$INSTALL_DIR/.github" ]; then
    ln -sf "$REPO_ROOT/.github" "$INSTALL_DIR/.github"
fi

# Set permissions
chown -R eir-metrics:eir-metrics "$INSTALL_DIR"
chmod +x "$INSTALL_DIR/export_metrics.py"

# Reload and enable
echo "Enabling service..."
systemctl daemon-reload
systemctl enable "$SERVICE_NAME"
systemctl start "$SERVICE_NAME"

echo ""
echo "=== Installation Complete ==="
echo "Service: ${SERVICE_NAME}"
echo "Endpoint: http://localhost:9120/metrics"
echo "Health: http://localhost:9120/health"
echo ""
echo "Commands:"
echo "  systemctl status $SERVICE_NAME    # Check status"
echo "  systemctl restart $SERVICE_NAME   # Restart"
echo "  journalctl -u $SERVICE_NAME -f    # View logs"
echo "  curl http://localhost:9120/metrics # Test metrics"
