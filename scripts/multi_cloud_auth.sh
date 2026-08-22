#!/usr/bin/env bash
# =============================================================================
# Evergreen Image Registry — Multi-Cloud Authentication
# =============================================================================
# Configures authentication for pulling EIR images from GHCR across
# AWS, GCP, and Azure cloud providers.
#
# Features:
#   - AWS IAM Roles for Service Accounts (IRSA)
#   - GCP Workload Identity
#   - Azure Workload Identity Federation
#   - Docker credential helper setup
#
# Usage:
#   ./scripts/multi_cloud_auth.sh --provider aws
#   ./scripts/multi_cloud_auth.sh --provider gcp
#   ./scripts/multi_cloud_auth.sh --provider azure
#   ./scripts/multi_cloud_auth.sh --verify
# =============================================================================

set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'
NC='\033[0m'

PROVIDER=""
VERIFY=false
REGISTRY="ghcr.io"
REPO_OWNER="wyattau"

log_info()  { echo -e "${CYAN}[INFO]${NC} $1"; }
log_ok()    { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

while [ $# -gt 0 ]; do
    case "$1" in
        --provider) PROVIDER="$2"; shift 2 ;;
        --verify)   VERIFY=true; shift ;;
        --help)     head -25 "$0" | tail -23; exit 0 ;;
        *)          log_error "Unknown: $1"; exit 1 ;;
    esac
done

# ---- AWS IRSA Configuration ----
configure_aws() {
    log_info "Configuring AWS IAM Roles for Service Accounts (IRSA)"

    # Check for AWS environment
    if [ -z "${AWS_ROLE_ARN:-}" ]; then
        log_warn "AWS_ROLE_ARN not set. Ensure IRSA is configured."
        log_info "Required:"
        log_info "  1. Create IAM role with GHCR read permissions"
        log_info "  2. Associate role with Kubernetes service account"
        log_info "  3. Set AWS_ROLE_ARN environment variable"
    fi

    # Install docker-credential-ecr-login (works with GHCR too)
    if ! command -v docker-credential-ecr-login &>/dev/null; then
        log_info "Installing docker credential helper..."
        ARCH=$(uname -m)
        case "$ARCH" in
            x86_64) ARCH="amd64" ;;
            aarch64) ARCH="arm64" ;;
        esac
        curl -sL "https://amazon-ecr-credential-helper-releases.s3.us-east-2.amazonaws.com/0.7.1/linux-${ARCH}/docker-credential-ecr-login" \
            -o /usr/local/bin/docker-credential-ecr-login
        chmod +x /usr/local/bin/docker-credential-ecr-login
    fi

    # Configure Docker credential store
    mkdir -p ~/.docker
    cat > ~/.docker/config.json << EOF
{
  "credsStore": "ecr-login",
  "auths": {
    "${REGISTRY}": {}
  }
}
EOF

    log_ok "AWS IRSA configured"
    log_info "Pull with: docker pull ${REGISTRY}/${REPO_OWNER}/<image>:latest"
}

# ---- GCP Workload Identity Configuration ----
configure_gcp() {
    log_info "Configuring GCP Workload Identity"

    # Check for GCP environment
    if [ -z "${GOOGLE_APPLICATION_CREDENTIALS:-}" ] && [ -z "${GCP_PROJECT:-}" ]; then
        log_warn "GCP credentials not detected."
        log_info "Required:"
        log_info "  1. Enable Workload Identity on GKE cluster"
        log_info "  2. Create GCP service account with GHCR read access"
        log_info "  3. Bind K8s SA to GCP SA via workload identity"
    fi

    # Install docker-credential-gcr
    if ! command -v docker-credential-gcr &>/dev/null; then
        log_info "Installing GCR credential helper..."
        curl -sL "https://github.com/GoogleCloudPlatform/docker-credential-gcr/releases/download/v2.0.11/docker-credential-gcr_linux_amd64" \
            -o /usr/local/bin/docker-credential-gcr
        chmod +x /usr/local/bin/docker-credential-gcr
    fi

    # Configure Docker for GHCR via GCP
    gcr configure-docker --registries="${REGISTRY}"

    log_ok "GCP Workload Identity configured"
    log_info "Pull with: docker pull ${REGISTRY}/${REPO_OWNER}/<image>:latest"
}

# ---- Azure Workload Identity Configuration ----
configure_azure() {
    log_info "Configuring Azure Workload Identity"

    # Check for Azure environment
    if [ -z "${AZURE_CLIENT_ID:-}" ] && [ -z "${AZURE_TENANT_ID:-}" ]; then
        log_warn "Azure credentials not detected."
        log_info "Required:"
        log_info "  1. Enable Workload Identity on AKS cluster"
        log_info "  2. Create Azure AD app registration"
        log_info "  3. Federate with Kubernetes service account"
    fi

    # Install docker-credential-azure
    if ! command -v docker-credential-acr-env &>/dev/null; then
        log_info "Installing ACR credential helper..."
        ARCH=$(uname -m)
        case "$ARCH" in
            x86_64) ARCH="amd64" ;;
            aarch64) ARCH="arm64" ;;
        esac
        curl -sL "https://github.com/Azure/acr-docker-credential-helper/releases/latest/download/docker-credential-acr-linux-${ARCH}" \
            -o /usr/local/bin/docker-credential-acr-env
        chmod +x /usr/local/bin/docker-credential-acr-env
    fi

    log_ok "Azure Workload Identity configured"
    log_info "Pull with: docker pull ${REGISTRY}/${REPO_OWNER}/<image>:latest"
}

# ---- Verify Authentication ----
verify_auth() {
    log_info "Verifying GHCR authentication..."

    # Test pull
    TEST_IMAGE="${REGISTRY}/${REPO_OWNER}/evergreenimageregistry/redis:latest"

    if docker manifest inspect "$TEST_IMAGE" >/dev/null 2>&1; then
        log_ok "Authentication successful — can pull from GHCR"
    else
        log_warn "Cannot pull from GHCR — authentication may not be configured"
        log_info "Try: docker login ${REGISTRY}"
    fi

    # Check credential helpers
    log_info "Installed credential helpers:"
    for helper in docker-credential-ecr-login docker-credential-gcr docker-credential-acr-env; do
        if command -v "$helper" &>/dev/null; then
            echo "  ✅ $helper"
        else
            echo "  ❌ $helper (not installed)"
        fi
    done
}

# ---- Main ----
if [ "$VERIFY" = true ]; then
    verify_auth
    exit 0
fi

case "$PROVIDER" in
    aws)    configure_aws ;;
    gcp)    configure_gcp ;;
    azure)  configure_azure ;;
    "")     log_error "Specify --provider (aws|gcp|azure) or --verify"; exit 1 ;;
    *)      log_error "Unknown provider: $PROVIDER"; exit 1 ;;
esac
