# pgrust

PostgreSQL 18.3 rewritten in Rust — wire- and SQL-compatible drop-in for
the official postgres image. **EXPERIMENTAL: v0.4-beta is not
production-ready**; the upstream targets production readiness in 2027.

- Upstream: https://github.com/malisper/pgrust (6.2k★, AGPL-3.0)
- Image: `ghcr.io/wyattau/pgrust:v0.4-beta` (mirrors upstream
  `malisper/pgrust:v0.4-beta`, multi-arch amd64+arm64)
- Extensions built in upstream: pgvector, pg_cron, pg_stat_statements,
  pg_trgm, hstore, pgcrypto, postgres_fdw and most of contrib. No C
  extension ABI — other Postgres extensions do not work.

## Deployed posture

Sandbox/evaluation only: non-critical, replayable workloads. Do not point
production services at it. Re-evaluate at the upstream's
production-readiness milestone with an evidence gate: independent
durability tests (the 13 failing recovery tests), non-Graviton
performance, and the fuzzing track record.

## Quick start

```bash
docker run -d --name pgrust \
  -e POSTGRES_PASSWORD=secret \
  -p 5433:5432 \
  ghcr.io/wyattau/pgrust:v0.4-beta
psql -h localhost -p 5433 -U postgres
```

## Known upstream gaps (2026-11)

- 13/47 crash-recovery tests failing (durability is the headline gap)
- SQLsmith found segfaults within days (planner invariants)
- Independent pgbench: ~1/9 vanilla TPS at v0.2; OOM under load reported
- The 1,600×/3,000× analytics claims are self-reported on Graviton4
