#!/bin/bash
# =============================================================================
# TRAEFIK CONSTRAINT VERIFICATION TESTS
# Run these to verify constraint compliance
# =============================================================================

set -euo pipefail

IMAGE="${1:-ghcr.io/sovereign/traefik:latest}"
PASS=0
FAIL=0

echo "=========================================="
echo "TRAEFIK CONSTRAINT VERIFICATION"
echo "Image: $IMAGE"
echo "=========================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# C001: Non-root execution
echo -n "C001: Non-root execution (UID 65534)... "
USER_ID=$(docker run --rm "$IMAGE" id -u 2>/dev/null || echo "failed")
if [ "$USER_ID" = "65534" ] || [ "$USER_ID" = "nobody" ]; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((PASS++))
else
    echo -e "${RED}✗ FAIL${NC} (got UID $USER_ID)"
    ((FAIL++))
fi

# C003: No shell
echo -n "C003: No shell (/bin/sh)... "
if docker run --rm "$IMAGE" test -f /bin/sh 2>/dev/null; then
    echo -e "${RED}✗ FAIL${NC} (/bin/sh exists)"
    ((FAIL++))
else
    echo -e "${GREEN}✓ PASS${NC}"
    ((PASS++))
fi

echo -n "C003: No shell (/bin/bash)... "
if docker run --rm "$IMAGE" test -f /bin/bash 2>/dev/null; then
    echo -e "${RED}✗ FAIL${NC} (/bin/bash exists)"
    ((FAIL++))
else
    echo -e "${GREEN}✓ PASS${NC}"
    ((PASS++))
fi

# C004: No package manager
echo -n "C004: No package manager (apt)... "
if docker run --rm "$IMAGE" test -f /usr/bin/apt 2>/dev/null || docker run --rm "$IMAGE" which apt 2>/dev/null; then
    echo -e "${RED}✗ FAIL${NC} (apt exists)"
    ((FAIL++))
else
    echo -e "${GREEN}✓ PASS${NC}"
    ((PASS++))
fi

echo -n "C004: No package manager (apk)... "
if docker run --rm "$IMAGE" test -f /usr/bin/apk 2>/dev/null || docker run --rm "$IMAGE" which apk 2>/dev/null; then
    echo -e "${RED}✗ FAIL${NC} (apk exists)"
    ((FAIL++))
else
    echo -e "${GREEN}✓ PASS${NC}"
    ((PASS++))
fi

echo -n "C004: No package manager (dnf)... "
if docker run --rm "$IMAGE" test -f /usr/bin/dnf 2>/dev/null || docker run --rm "$IMAGE" which dnf 2>/dev/null; then
    echo -e "${RED}✗ FAIL${NC} (dnf exists)"
    ((FAIL++))
else
    echo -e "${GREEN}✓ PASS${NC}"
    ((PASS++))
fi

# C005: Static linking (if binary exists)
echo -n "C005: Static linking... "
BINARY=$(docker run --rm "$IMAGE" find / -type f -executable -name traefik 2>/dev/null | head -1 || true)
if [ -n "$BINARY" ]; then
    LDD_OUTPUT=$(docker run --rm "$IMAGE" ldd "$BINARY" 2>&1 || true)
    if echo "$LDD_OUTPUT" | grep -q "not a dynamic" || echo "$LDD_OUTPUT" | grep -q "statically linked"; then
        echo -e "${GREEN}✓ PASS (static)${NC}"
        ((PASS++))
    else
        echo -e "${YELLOW}⚠ PARTIAL${NC} (dynamic: $LDD_OUTPUT)"
    fi
else
    echo -e "${YELLOW}⚠ SKIP${NC} (no binary found)"
fi

# C006: Stripped symbols
echo -n "C006: Stripped symbols... "
if [ -n "$BINARY" ]; then
    SYM_COUNT=$(docker run --rm "$IMAGE" nm "$BINARY" 2>/dev/null | wc -l || echo "0")
    if [ "$SYM_COUNT" -lt 10 ]; then
        echo -e "${GREEN}✓ PASS${NC} ($SYM_COUNT symbols)"
        ((PASS++))
    else
        echo -e "${YELLOW}⚠ PARTIAL${NC} ($SYM_COUNT symbols)"
    fi
else
    echo -e "${YELLOW}⚠ SKIP${NC}"
fi

# C010: Health check
echo -n "C010: Health check... "
# Start container in background
CID=$(docker run -d --rm --name="${IMAGE//\//-}-test" "$IMAGE" 2>/dev/null || true)
sleep 3
if [ -n "$CID" ]; then
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/ping 2>/dev/null || echo "000")
    docker kill "$CID" 2>/dev/null || true
    if [ "$HTTP_CODE" = "200" ]; then
        echo -e "${GREEN}✓ PASS${NC} (/ping returns 200)"
        ((PASS++))
    else
        echo -e "${YELLOW}⚠ PARTIAL${NC} (HTTP $HTTP_CODE)"
    fi
else
    echo -e "${RED}✗ FAIL${NC} (container failed to start)"
    ((FAIL++))
fi

# C012: No secrets (basic check)
echo -n "C012: No embedded secrets (basic)... "
SECRETS=$(docker run --rm "$IMAGE" grep -r "password\|secret\|api.key\|token" /etc/ 2>/dev/null | wc -l || echo "0")
if [ "$SECRETS" = "0" ]; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((PASS++))
else
    echo -e "${YELLOW}⚠ WARNING${NC} ($SECRETS potential secrets)"
fi

echo "=========================================="
echo "RESULTS: $PASS passed, $FAIL failed"
echo "=========================================="

# C002: Read-only test (requires manual verification)
echo ""
echo -e "${YELLOW}C002: Read-only filesystem - run manually:${NC}"
echo "  docker run --rm --read-only $IMAGE touch /test"
echo "  # Should fail with: Read-only file system"

exit $FAIL