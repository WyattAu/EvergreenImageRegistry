FROM malisper/pgrust:v0.4-beta

LABEL org.opencontainers.image.title="pgrust" \
      org.opencontainers.image.description="PostgreSQL 18.3 rewritten in Rust - wire-compatible drop-in (EXPERIMENTAL: not production-ready, upstream targets production in 2027)" \
      org.opencontainers.image.source="https://github.com/malisper/pgrust" \
      org.opencontainers.image.licenses="AGPL-3.0" \
      evergreen.image.tier="community" \
      evergreen.constraint.experimental="true" \
      evergreen.upstream.repo="malisper/pgrust" \
      evergreen.upstream.version="v0.4-beta"

EXPOSE 5432
VOLUME /var/lib/postgresql/data

# The upstream image keeps the official postgres image's entrypoint and
# environment-variable layout (POSTGRES_PASSWORD/USER/DB, init scripts),
# so it drops into existing compose files unchanged.
