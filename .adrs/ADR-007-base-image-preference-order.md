| 1        | `scratch`         | - | none  | none     | 0 MB    | Static binary, zero runtime deps      |
#### wolfi First: Including FIPS
| Jenkins    | 3    | scratch     | Static Go binary; even though Tier 3, scratch works |
| Grafana    | 3    | wolfi       | Needs glibc; falls to wolfi                         |
- Migration is not a sed replacement; different package managers, package names, paths
| ADR-003 | Debian multi-stage strategy (superseded; debian-slim now banned) |