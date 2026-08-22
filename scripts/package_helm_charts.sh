#!/bin/bash
# Package Helm charts for OCI registry publishing
# Usage: ./package_helm_charts.sh [oci://registry/repo]
#
# This script:
# 1. Discovers all Helm charts under charts/
# 2. Packages them as .tgz archives
# 3. Optionally pushes to an OCI registry (e.g., oci://ghcr.io/wyattau/helm-charts)

set -euo pipefail

OCI_REGISTRY="${1:-}"
CHARTS_DIR="charts"
PACKAGE_DIR="charts/packages"

echo "=== Evergreen Helm Chart Packager ==="
echo ""

# Find all charts
if [ ! -d "$CHARTS_DIR" ]; then
    echo "ERROR: $CHARTS_DIR/ not found. Run generate_helm_charts.sh first."
    exit 1
fi

CHARTS=$(find "$CHARTS_DIR" -name "Chart.yaml" -not -path "*/charts/*" | sort)
CHART_COUNT=$(echo "$CHARTS" | wc -l)

echo "Found $CHART_COUNT charts"
echo ""

# Create package directory
mkdir -p "$PACKAGE_DIR"

# Package each chart
PACKAGED=0
FAILED=0

for chart_yaml in $CHARTS; do
    chart_dir=$(dirname "$chart_yaml")
    chart_name=$(basename "$chart_dir")
    
    echo -n "  $chart_name: "
    
    # Package
    if helm package "$chart_dir" --destination "$PACKAGE_DIR" > /dev/null 2>&1; then
        PACKAGED=$((PACKAGED + 1))
        echo "✅ packaged"
    else
        FAILED=$((FAILED + 1))
        echo "❌ failed"
    fi
done

echo ""
echo "=== Package Results ==="
echo "PACKAGED: $PACKAGED"
echo "FAILED: $FAILED"

# Push to OCI registry if specified
if [ -n "$OCI_REGISTRY" ]; then
    echo ""
    echo "=== Pushing to $OCI_REGISTRY ==="
    
    PUSHED=0
    PUSH_FAILED=0
    
    for tgz in "$PACKAGE_DIR"/*.tgz; do
        [ -f "$tgz" ] || continue
        chart_name=$(basename "$tgz" | sed 's/-[0-9].*//')
        
        echo -n "  $chart_name: "
        
        if helm push "$tgz" "$OCI_REGISTRY" > /dev/null 2>&1; then
            PUSHED=$((PUSHED + 1))
            echo "✅ pushed"
        else
            PUSH_FAILED=$((PUSH_FAILED + 1))
            echo "❌ failed"
        fi
    done
    
    echo ""
    echo "=== Push Results ==="
    echo "PUSHED: $PUSHED"
    echo "FAILED: $PUSH_FAILED"
fi

echo ""
echo "=== Done ==="
echo "Packages: $PACKAGE_DIR/"
ls -la "$PACKAGE_DIR"/*.tgz 2>/dev/null | wc -l
echo "chart packages created"
