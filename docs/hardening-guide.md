# Note: No USER override: inherit upstream's user model
- [ ] **Build succeeds**; `docker build` completes without error
- [ ] **Non-root user**; `docker inspect --format '{{.Config.User}}'` returns non-root UID
- [ ] **No shell**; `docker run --rm --entrypoint "" <img> sh -c "echo test"` fails
- [ ] **Health check works**; Container starts and HEALTHCHECK passes within start-period
- [ ] **Metrics available**; `curl http://localhost:9101/metrics` returns data (if shim enabled)
- [ ] **App functional**; Application-specific test passes (HTTP, TCP, DB query)
- [ ] **Signed**; `cosign verify` succeeds
- [ ] **SBOM exists**; `cosign verify-attestation --type spdxjson` succeeds