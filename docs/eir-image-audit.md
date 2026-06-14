# EIR Image Audit — Stub vs Functional

**Date:** 2026-06-14
**Auditor:** Nexus (automated)
**Method:** Dockerfile analysis for SIS-critical images

## Summary

| Category | Count | Impact |
|----------|-------|--------|
| FUNCTIONAL | 6 | Ready for SIS migration |
| STUB (shim path mismatch) | 5 | Quick fix possible |
| STUB (missing app code) | 5 | Needs implementation |
| STUB (syntax error) | 2 | Quick fix possible |

## Functional Images (Ready for Migration)

| Image | Build Type | Notes |
|-------|-----------|-------|
| redis | source-build | Static linked, shim.toml present |
| synapse | repack | From matrixdotorg/synapse, needs /data/homeserver.yaml |
| ntfy | binary-download | SHA256 verified per-arch |
| taiga-back | repack | From taigaio/taiga-back, gunicorn |
| taiga-event | repack | From taigaio/taiga-event, node |
| forgejo-runner | binary-download | Double `-c` flag bug in CMD (works but needs fix) |

## Stub Images (Need Fixes)

### Shim Path Mismatch (ENTRYPOINT uses `/shim`, COPY to `/usr/local/bin/shim`)

| Image | Also Missing App? | Fix Effort |
|-------|-------------------|------------|
| element-web | Yes (no nginx) | Medium |
| mariadb | No (binaries present) | **Low** — fix path + remove duplicate `-c` |
| immich | Yes (no app code) | High |
| taiga-front | Yes (no nginx, syntax err) | Medium |
| freshrss | Yes (no app code, no web server) | High |

### Missing Application Code (Binary/runtime only, no app)

| Image | What's Missing |
|-------|---------------|
| rabbitmq | `rabbitmq-server` never installed/copied |
| akaunting | No Akaunting PHP application code |
| immich | `/usr/src/app/dist/main.js` not copied |
| immich-ml | No app code, no CMD |
| paperless-ngx | No app, references s6-svscan (not installed) |

### Syntax Errors

| Image | Error |
|-------|-------|
| taiga-front | `ENTRYPOINT` has extra `]]` |
| taiga-protected | `ENTRYPOINT` has extra `]]`, runs nginx (should be Python) |

## Root Cause Analysis

### Pattern 1: Shim Path Mismatch
**Cause:** Dockerfile template generates ENTRYPOINT with `/shim` (correct for scratch) but wolfi-based images copy shim to `/usr/local/bin/shim`. The HEALTHCHECK line correctly uses `/usr/local/bin/shim`, proving the file knows the right path — ENTRYPOINT was not updated to match.

**Systemic Fix:** Audit all wolfi-base images with `COPY --from=shim /shim /usr/local/bin/shim` and verify ENTRYPOINT matches.

### Pattern 2: Missing App Code
**Cause:** Images generated from templates that set up the runtime environment (PHP, Node, Python) but never COPY the actual application from upstream. This matches the "pkg-install" build type pattern where the generator installs packages but doesn't fetch the app.

**Systemic Fix:** For each missing-app stub, add a `FROM upstream` stage and COPY the application code.

## Recommended Fix Priority

1. **Quick wins** (shim path fix, no other issues):
   - mariadb (fix path + remove duplicate `-c`)

2. **Medium effort** (add nginx + fix path):
   - element-web
   - taiga-front

3. **High effort** (add app code + web server):
   - freshrss
   - akaunting
   - immich
   - immich-ml
   - paperless-ngx
   - rabbitmq
