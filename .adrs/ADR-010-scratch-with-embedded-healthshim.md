at runtime. Database and proxy images need health probes, metrics, and process management; but adding a shell violates
- No shell required in scratch images; pure binary orchestration
- Single binary entrypoint; no `--init` flag needed
- CLI exec adds latency (~10-100ms per check); acceptable for 30s probe intervals