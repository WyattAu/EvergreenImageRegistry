# Postgresql-patroni (ARCHIVED)

Archived 2026-09-09.

Reason: upstream `registry.opensource.zalan.do` was shut down by
Zalando; the image no longer resolves anywhere (ghcr mirrors 403,
docker.io 401). Not deployed in the SimpleInfrastructureStack.

To revive: Patroni publishes images at ghcr.io/patroni/patroni behind
auth; rewrite FROM once a public tag exists.
