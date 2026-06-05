# =============================================================================
# Evergreen Image Registry - Unified Makefile
# =============================================================================
# Usage: make help

SHELL := /bin/bash
.DEFAULT_GOAL := help

# ---- lint ----
.PHONY: lint
lint: ## Run hadolint + ruff + shellcheck on changed files
	@echo "=== Linting changed files ==="
	@CHANGED_DOCKERFILES=$$(git diff --name-only --diff-filter=ACM HEAD 2>/dev/null | grep 'Dockerfile$$' || true); \
	CHANGED_PY=$$(git diff --name-only --diff-filter=ACM HEAD 2>/dev/null | grep '\.py$$' || true); \
	CHANGED_SH=$$(git diff --name-only --diff-filter=ACM HEAD 2>/dev/null | grep '\.sh$$' || true); \
	EXIT_CODE=0; \
	if [ -n "$$CHANGED_DOCKERFILES" ] && command -v hadolint >/dev/null 2>&1; then \
		echo "--- hadolint ---"; \
		for f in $$CHANGED_DOCKERFILES; do echo "  $$f"; done; \
		echo "$$CHANGED_DOCKERFILES" | xargs hadolint || EXIT_CODE=1; \
	fi; \
	if [ -n "$$CHANGED_PY" ] && command -v ruff >/dev/null 2>&1; then \
		echo "--- ruff ---"; \
		echo "$$CHANGED_PY" | xargs ruff check || EXIT_CODE=1; \
	fi; \
	if [ -n "$$CHANGED_SH" ] && command -v shellcheck >/dev/null 2>&1; then \
		echo "--- shellcheck ---"; \
		echo "$$CHANGED_SH" | xargs shellcheck || EXIT_CODE=1; \
	fi; \
	if [ -z "$$CHANGED_DOCKERFILES" ] && [ -z "$$CHANGED_PY" ] && [ -z "$$CHANGED_SH" ]; then \
		echo "No changed files to lint"; \
	fi; \
	exit $$EXIT_CODE

# ---- test ----
.PHONY: test
test: ## Run pre-push-gate.sh
	@echo "=== Running pre-push quality gate ==="
	@bash scripts/pre-push-gate.sh

# ---- verify ----
.PHONY: verify
verify: ## Run evergreenctl verify on all images
	@echo "=== Verifying all images ==="
	@for dir in images/*/; do \
		if [ -f "$${dir}manifest.toml" ]; then \
			echo "  verify: $$dir"; \
			evergreenctl verify "$$dir" 2>&1 || true; \
		fi; \
	done

# ---- drift ----
.PHONY: drift
drift: ## Run evergreenctl drift on all images
	@echo "=== Checking drift for all images ==="
	@for dir in images/*/; do \
		if [ -f "$${dir}manifest.toml" ] && [ -f "$${dir}Dockerfile" ]; then \
			echo "  drift: $$dir"; \
			evergreenctl drift "$$dir" 2>&1 || true; \
		fi; \
	done

# ---- build ----
IMG ?=
.PHONY: build
build: ## Build a single image locally (IMG=name)
	@if [ -z "$(IMG)" ]; then \
		echo "Usage: make build IMG=<image-name>"; \
		echo "Example: make build IMG=nginx"; \
		exit 1; \
	fi
	@if [ ! -f "images/$(IMG)/Dockerfile" ]; then \
		echo "Error: images/$(IMG)/Dockerfile not found"; \
		exit 1; \
	fi
	@echo "=== Building $(IMG) ==="
	@docker build -t "evergreen-$(IMG)" "images/$(IMG)/"

# ---- build-all ----
.PHONY: build-all
build-all: ## Build all images (requires Docker)
	@echo "=== Building all images ==="
	@EXIT_CODE=0; \
	for dir in images/*/; do \
		if [ -f "$${dir}Dockerfile" ]; then \
			NAME=$$(basename "$$dir"); \
			echo "  Building $$NAME ..."; \
			docker build -t "evergreen-$$NAME" "$$dir" || { echo "  FAILED: $$NAME"; EXIT_CODE=1; }; \
		fi; \
	done; \
	exit $$EXIT_CODE

# ---- sbom ----
.PHONY: sbom
sbom: ## Generate missing SBOMs
	@echo "=== Generating missing SBOMs ==="
	@SKIP_UNCHANGED=true scripts/generate_all_sboms.sh 2>/dev/null || \
		echo "No SBOM generation script found or no missing SBOMs"

# ---- audit ----
.PHONY: audit
audit: ## Run evergreenctl audit on all images
	@echo "=== Auditing all images ==="
	@evergreenctl audit images/ 2>&1 || echo "evergreenctl audit completed (or not installed)"

# ---- musl-check ----
.PHONY: musl-check
musl-check: ## Run musl rebuild check locally for a single image (IMG=name)
	@if [ -z "$(IMG)" ]; then \
		echo "Usage: make musl-check IMG=<image-name>"; \
		echo "Example: make musl-check IMG=vector"; \
		exit 1; \
	fi
	@if [ ! -f "images/$(IMG)/Dockerfile" ]; then \
		echo "Error: images/$(IMG)/Dockerfile not found"; \
		exit 1; \
	fi
	@echo "=== Musl Rebuild Check: $(IMG) ==="
	@IMAGE="$(IMG)"; \
	BUILD_TYPE="unknown"; \
	if grep -qE 'golang\.org/dl/|github\.com/.*releases/download.*linux.*amd64' "images/$$IMAGE/Dockerfile" 2>/dev/null; then \
		BUILD_TYPE="go"; \
	elif grep -qE 'rust-lang\.org/dist' "images/$$IMAGE/Dockerfile" 2>/dev/null; then \
		BUILD_TYPE="rust"; \
	fi; \
	echo "  Build type: $$BUILD_TYPE"; \
	if [ "$$BUILD_TYPE" = "unknown" ]; then \
		echo "  Skipping: not a Go/Rust binary-download image"; \
		exit 0; \
	fi; \
	if [ ! -f "images/$$IMAGE/Dockerfile.musl-src" ]; then \
		echo "  Generating musl Dockerfile..."; \
		if [ "$$BUILD_TYPE" = "go" ]; then \
			bash scripts/rebuild_go_musl.sh "$$IMAGE"; \
		else \
			bash scripts/rebuild_rust_musl.sh "$$IMAGE"; \
		fi; \
	fi; \
	if [ ! -f "images/$$IMAGE/Dockerfile.musl-src" ]; then \
		echo "  ERROR: Failed to generate musl Dockerfile"; \
		exit 1; \
	fi; \
	echo "  Building original image..."; \
	docker build -t "evergreen-$$IMAGE-glibc" "images/$$IMAGE/" || exit 1; \
	echo "  Building musl image..."; \
	docker build -t "evergreen-$$IMAGE-musl" -f "images/$$IMAGE/Dockerfile.musl-src" "images/$$IMAGE/" || exit 1; \
	ORIG_SIZE=$$(docker image inspect "evergreen-$$IMAGE-glibc" --format='{{.Size}}' 2>/dev/null); \
	MUSL_SIZE=$$(docker image inspect "evergreen-$$IMAGE-musl" --format='{{.Size}}' 2>/dev/null); \
	ORIG_MB=$$((ORIG_SIZE / 1024 / 1024)); \
	MUSL_MB=$$((MUSL_SIZE / 1024 / 1024)); \
	SAVED=$$((ORIG_SIZE - MUSL_SIZE)); \
	SAVINGS_PCT=$$(( (SAVED * 100) / ORIG_SIZE )); \
	echo ""; \
	echo "  Results:"; \
	echo "    Original: $${ORIG_MB} MB"; \
	echo "    Musl:     $${MUSL_MB} MB"; \
	echo "    Savings:  $${SAVINGS_PCT}%"; \
	if [ "$$SAVINGS_PCT" -ge 10 ]; then \
		echo "  -> Exceeds 10% threshold! PR candidate."; \
	else \
		echo "  -> Below 10% threshold."; \
	fi; \
	echo ""; \
	echo "  Verifying musl image..."; \
	docker run --rm "evergreen-$$IMAGE-musl" --version 2>&1 || true

# ---- help ----
.PHONY: help
help: ## List all targets
	@echo "Evergreen Image Registry - Available Targets"
	@echo "============================================"
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "Examples:"
	@echo "  make lint"
	@echo "  make build IMG=nginx"
	@echo "  make test"
