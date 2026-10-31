| A; LinuxServer.io    | 6     | Third-party Alpine-based images with no alternative upstream  | lidarr, prowlarr, radarr, sonarr            |
| B; Official upstream | 5     | Vendor-maintained images with opaque build systems            | drone, gitlab-ce, jellyfin, openhab, pulsar |
| C; Internal/custom   | 2     | Custom images with unclear provenance requiring investigation | milvus-etcd, milvus-minio                   |
| D; Migratable        | 3     | Images that CAN be migrated to compliant base images          | oxidized, python-alpine, python-slim        |
**Category A; LinuxServer.io (Accepted Exception)**
**Category B; Official upstream (Accepted Exception)**
**Category C; Internal/custom (Under Investigation)**
**Category D; Migratable (Migrate Immediately)**
- No exception required; these images comply with ADR-007 post-migration