| `/livez`  | Liveness; process is alive | 200 OK / 503 Error  |
| `/readyz` | Readiness; accepting traffic| 200 OK / 503 Error  |
| `/startupz`| Startup; initialized       | 200 OK / 503 Error  |
| `HEALTH_CMD`   | YES      |;       | CLI command for liveness check                   |