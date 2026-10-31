images need health probes, metrics, and process management; but adding a shell violates Pillar I (Security &
3. Not the entrypoint; additional process orchestration needed
- `tokio`; async runtime
- `axum`; HTTP server (~50KB)
- `prometheus-client`; metrics format
- `nix`; signal handling, process management
- `serde`; config parsing from env vars
**No shell required**; pure binary orchestration.
- CLI exec adds latency (~10-100ms per check); acceptable for 30s probe intervals