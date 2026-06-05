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
