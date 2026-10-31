| `/metrics`  | Prometheus/OpenMetrics text format | - | 200 + metrics body |
| `/livez`    | Liveness; process is alive        | `livenessProbe`  | 200 if alive       |
| `/readyz`   | Readiness; accepting traffic      | `readinessProbe` | 200 if ready       |
| `/startupz` | Startup; initialization complete  | `startupProbe`   | 200 if started     |
- 9090 is Prometheus server default; confusion risk