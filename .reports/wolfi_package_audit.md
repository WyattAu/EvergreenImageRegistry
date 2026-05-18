# Wolfi Package Audit Report

**Generated**: Automated audit against wolfi APKINDEX

**Source**: `https://packages.wolfi.dev/os/x86_64/APKINDEX.tar.gz`

## Summary

| Metric | Value |
|--------|-------|
| Total unique packages | 474 |
| Valid (in wolfi) | 155 |
| Invalid (not in wolfi) | 319 |
| Valid percentage | 32.7% |
| Dockerfiles scanned | 979 |
| Dockerfiles with `apk add` | 519 |

## Invalid Packages

| Package | Category | Dockerfiles | Images |
|---------|----------|-------------|--------|
| `#` | unknown | 1 | gitea |
| `*)` | unknown | 3 | gitea, libsql, litestream |
| `+x` | unknown | 17 | caddy-alpine, dbmate, docker-clean, duplicati, forgejo... |
| `-` | unknown | 11 | automatic1111, bazarr, bazarr-subliminal, comfyui, docker-clean... |
| `2.5.0` | unknown | 1 | bundler |
| `65532:65532` | unknown | 76 | 389ds, akaunting, apache, athom, calibre-web... |
| `8.0` | unknown | 1 | duplicati |
| `?` | unknown | 1 | organizer |
| `@grafana/toolkit@__VAR__` | unknown | 1 | grafana-toolkit |
| `@worldsibu/convector-platform@__VAR__` | unknown | 1 | convector |
| `ARCH=$(case` | unknown | 2 | gitea, libsql |
| `AWS` | unknown | 1 | neptune |
| `Atlas` | unknown | 1 | objectrocket |
| `Based` | unknown | 1 | docker-clean |
| `CGO_ENABLED=0` | unknown | 1 | dotdns |
| `Docker` | unknown | 1 | docker-clean |
| `GOARCH=__VAR__` | unknown | 1 | dotdns |
| `GOOS=linux` | unknown | 1 | dotdns |
| `Gremlin/SPARQL` | unknown | 1 | neptune |
| `MongoDB` | unknown | 1 | objectrocket |
| `Neptune` | unknown | 1 | neptune |
| `Neptune-compatible` | unknown | 1 | neptune |
| `ObjectRocket-compatible` | unknown | 1 | objectrocket |
| `ObjectRocket/MongoDB` | unknown | 1 | objectrocket |
| `RediSearch,` | unknown | 1 | redismodules |
| `RedisJSON,` | unknown | 1 | redismodules |
| `RedisTimeSeries,` | unknown | 1 | redismodules |
| `SPARQLWrapper` | unknown | 1 | neptune |
| `SQL` | unknown | 1 | singlestore |
| `SingleStore-compatible` | unknown | 1 | singlestore |
| `TTS` | unknown | 2 | coqui-tts, tts |
| `a` | unknown | 3 | neptune, objectrocket, singlestore |
| `a2dismod` | unknown | 1 | apache |
| `accelerate` | unknown | 1 | stable-diffusion |
| `add` | unknown | 10 | faster-whisper, gitbucket, knot-resolver, mailtrain, mozilla-hubs... |
| `amd64)` | unknown | 3 | gitea, libsql, litestream |
| `apk` | unknown | 12 | faster-whisper, gitbucket, knot-resolver, mailtrain, milvus-minio... |
| `app` | unknown | 70 | airsonic, airsonic-advanced, automatic1111, bazarr, bazarr-subliminal... |
| `app:app` | unknown | 55 | automatic1111, bazarr, bazarr-subliminal, bundler, calibre... |
| `appuser` | unknown | 14 | cinny, debian-slim, element-web, element-x, fail2ban... |
| `appuser:appuser` | unknown | 4 | fail2ban, modsecurity, powerdns, softether |
| `arango` | unknown | 1 | arango |
| `arm64)` | unknown | 3 | gitea, libsql, litestream |
| `as` | unknown | 3 | neptune, objectrocket, singlestore |
| `athom` | unknown | 1 | athom |
| `autoindex` | unknown | 1 | apache |
| `available` | unknown | 7 | automatic1111, bazarr, bazarr-subliminal, comfyui, gallery3... |
| `backup` | unknown | 1 | gitlab-backup |
| `base` | unknown | 3 | neptune, objectrocket, singlestore |
| `build` | unknown | 1 | dotdns |
| `bundled:` | unknown | 1 | redismodules |
| `bundler` | unknown | 1 | bundler |
| `bzip2-libs` | unknown | 2 | onlyoffice-documentserver, onlyoffice-documentserver-ee |
| `calibre` | unknown | 4 | calibre, calibre-eb, calibre-server, calibre-web |
| `case` | unknown | 1 | litestream |
| `chartdb` | unknown | 1 | chartdb |
| `chroma` | unknown | 1 | chroma |
| `chroma:chroma` | unknown | 1 | chroma |
| `chromadb` | unknown | 1 | chroma |
| `chromadb==0.5.23` | unknown | 1 | chroma-all-minimal |
| `chromadb==__VAR__` | unknown | 1 | chroma |
| `cid` | unknown | 1 | docker-clean |
| `cleanup` | unknown | 1 | docker-clean |
| `client` | unknown | 2 | objectrocket, singlestore |
| `clone` | unknown | 8 | automatic1111, bazarr, bazarr-subliminal, comfyui, fail2ban-exporter... |
| `cloud` | unknown | 1 | objectrocket |
| `cmak` | unknown | 1 | kafka-manager |
| `codimd` | unknown | 1 | codimd |
| `commercial` | unknown | 1 | singlestore |
| `common` | unknown | 1 | docker-clean |
| `compatibility` | unknown | 2 | neptune, singlestore |
| `complement` | unknown | 1 | chat-relay |
| `conduit` | unknown | 1 | conduit-admin |
| `connect` | unknown | 1 | kafka-connect |
| `container:` | unknown | 1 | docker-clean |
| `convector` | unknown | 1 | convector |
| `crate` | unknown | 1 | crate |
| `created=$(docker` | unknown | 1 | docker-clean |
| `dagster` | unknown | 3 | dagster, dagster-daemon, dagster-logs |
| `dagster-webserver` | unknown | 1 | dagster |
| `dangling` | unknown | 1 | docker-clean |
| `database` | unknown | 2 | neptune, objectrocket |
| `deepspeed` | unknown | 1 | deepspeed |
| `del` | unknown | 2 | milvus-minio, sqlite-utils |
| `dendrite` | unknown | 1 | dendrite-pot |
| `derby` | unknown | 1 | derby |
| `development` | unknown | 3 | neptune, objectrocket, singlestore |
| `diffusers` | unknown | 2 | diffusers, stable-diffusion |
| `distributed` | unknown | 1 | singlestore |
| `do\n` | unknown | 1 | docker-clean |
| `docker-clean` | unknown | 1 | docker-clean |
| `dockerclean` | unknown | 1 | docker-clean |
| `dsp` | unknown | 1 | docker-socket-proxy |
| `edition` | unknown | 1 | singlestore |
| `ejdb` | unknown | 1 | ejdb |
| `endpoint` | unknown | 2 | neptune, objectrocket |
| `erpnext` | unknown | 1 | erpnext |
| `erpnext:erpnext` | unknown | 1 | erpnext |
| `esac` | unknown | 1 | litestream |
| `esac)` | unknown | 2 | gitea, libsql |
| `exited` | unknown | 1 | docker-clean |
| `fastapi==0.115.0` | unknown | 2 | immich-machine-learning, immich-ml |
| `faster-whisper` | unknown | 1 | faster-whisper |
| `fi` | unknown | 3 | caddy-alpine, cinny, keycloak |
| `fi\ndone\n\ndangling_images=$(docker` | unknown | 1 | docker-clean |
| `fileshare` | unknown | 1 | ol_fileshare |
| `firebird` | unknown | 1 | firebird |
| `fluentd` | unknown | 1 | fluentd |
| `for` | unknown | 3 | neptune, objectrocket, singlestore |
| `free` | unknown | 1 | singlestore |
| `from` | unknown | 1 | singlestore |
| `fstrm-libs` | unknown | 1 | powerdns-recursor |
| `fully` | unknown | 2 | neptune, objectrocket |
| `gitbucket` | unknown | 1 | gitbucket |
| `graph` | unknown | 1 | neptune |
| `graphdb` | unknown | 1 | graphdb-enterpriser |
| `graphile` | unknown | 1 | graphile |
| `graylog` | unknown | 1 | graylog |
| `gremlinpython` | unknown | 1 | neptune |
| `gremlinpython,` | unknown | 1 | neptune |
| `h2` | unknown | 1 | h2 |
| `hazelcast` | unknown | 1 | hazelcast |
| `hive` | unknown | 2 | hive, hive-metastore |
| `homeassistant` | unknown | 1 | homeassistant |
| `homeassistant:homeassistant` | unknown | 1 | homeassistant |
| `homekit` | unknown | 1 | homekit |
| `hts` | unknown | 1 | tvheadend |
| `hts:hts` | unknown | 1 | tvheadend |
| `hydrogen` | unknown | 1 | hydrogen |
| `if` | unknown | 4 | caddy-alpine, cinny, docker-clean, keycloak |
| `ignite` | unknown | 1 | ignite |
| `image` | unknown | 3 | neptune, objectrocket, singlestore |
| `images` | unknown | 1 | docker-clean |
| `immich` | unknown | 1 | immich |
| `immich:immich` | unknown | 1 | immich |
| `import` | unknown | 3 | neptune, objectrocket, singlestore |
| `in` | unknown | 6 | docker-clean, gitea, libsql, litestream, neptune... |
| `inspect` | unknown | 1 | docker-clean |
| `invokeai` | unknown | 1 | invokeai |
| `is` | unknown | 3 | neptune, objectrocket, singlestore |
| `janusgraph` | unknown | 1 | janusgraph |
| `java-21-default-jdk` | unknown | 3 | gitbucket, openhab, wolfi-jdk |
| `jenkins:jenkins` | unknown | 1 | jenkins |
| `jupyter` | unknown | 1 | jupyter-all |
| `jupyterlab` | unknown | 3 | jupyter-pytorch, jupyter-scikit, jupyter-tensorflow |
| `kibana` | unknown | 2 | kibana, kibana-oss |
| `knot` | unknown | 1 | knot-resolver |
| `knot-resolver` | unknown | 1 | knot-resolver |
| `knot-resolver-utils` | unknown | 1 | knot-resolver |
| `langchain` | unknown | 1 | langchain |
| `langserve` | unknown | 1 | langserve |
| `ldap` | unknown | 2 | ldap, openldap |
| `ldap:ldap` | unknown | 2 | ldap, openldap |
| `libcrypto1.1` | unknown | 1 | strongswan |
| `libcurl` | unknown | 7 | onlyoffice-communityserver, onlyoffice-controlpanel, onlyoffice-documentserver, onlyoffice-documentserver-ee, powerdns-api... |
| `libraries` | unknown | 1 | singlestore |
| `library` | unknown | 1 | objectrocket |
| `libtiff` | unknown | 2 | onlyoffice-documentserver, onlyoffice-documentserver-ee |
| `litellm` | unknown | 1 | litellm |
| `litellm[proxy]` | unknown | 1 | litellm-proxy |
| `local` | unknown | 1 | neptune |
| `main()` | unknown | 1 | dotdns |
| `main\nimport` | unknown | 1 | dotdns |
| `managed` | unknown | 2 | neptune, objectrocket |
| `mariadb-libs` | unknown | 1 | onlyoffice-communityserver |
| `matplotlib` | unknown | 1 | jupyter-scikit |
| `matrix-synapse==__VAR__` | unknown | 1 | chat-server |
| `maxbot==__VAR__` | unknown | 1 | maxbot |
| `meltano` | unknown | 1 | meltano |
| `memgraph` | unknown | 1 | memgraph |
| `modsec` | unknown | 1 | modsecurity-crs |
| `module` | unknown | 1 | redismodules |
| `modules` | unknown | 1 | redismodules |
| `mongodb` | unknown | 3 | mongodb-5, mongodb-7, mongodb-community |
| `mongosh` | unknown | 1 | mongodb-opsmanager |
| `mosquitto:mosquitto` | unknown | 1 | mqtt |
| `mythtv` | unknown | 1 | mythtv |
| `mythtv:mythtv` | unknown | 1 | mythtv |
| `neptune` | unknown | 1 | neptune |
| `newsboat` | unknown | 1 | newsboat |
| `newsboat:newsboat` | unknown | 1 | newsboat |
| `nheko` | unknown | 1 | nheko |
| `nifi` | unknown | 2 | apache-nifi, nifi-registry |
| `node` | unknown | 4 | logseq, n8n, typesense-js, uptime-kuma |
| `node:node` | unknown | 4 | logseq, n8n, typesense-js, uptime-kuma |
| `nogroup` | unknown | 13 | athom, docker-clean, homekit, r2c-bench, rblake... |
| `not` | unknown | 7 | automatic1111, bazarr, bazarr-subliminal, comfyui, gallery3... |
| `numpy==2.1.0` | unknown | 2 | immich-machine-learning, jupyter-scikit |
| `objectrocket` | unknown | 1 | objectrocket |
| `on` | unknown | 1 | docker-clean |
| `onnxruntime` | unknown | 2 | immich-machine-learning, immich-ml |
| `open-gpts` | unknown | 1 | opengpts |
| `openai-whisper` | unknown | 1 | whisper |
| `openhab` | unknown | 1 | openhab |
| `openjdk-21-jdk-headless` | unknown | 3 | gitbucket, openhab, wolfi-jdk |
| `openssl-libs` | unknown | 7 | onlyoffice-communityserver, onlyoffice-controlpanel, onlyoffice-documentserver, onlyoffice-documentserver-ee, powerdns-api... |
| `oracle` | unknown | 1 | oracledb-xe |
| `organizr` | unknown | 1 | organizer |
| `outline` | unknown | 1 | outline |
| `outline:outline` | unknown | 1 | outline |
| `oxidized` | unknown | 1 | oxidized |
| `pandas==2.2.0` | unknown | 1 | jupyter-scikit |
| `pgbouncer:pgbouncer` | unknown | 1 | pgbouncer |
| `pgpool` | unknown | 1 | pgpool-ii |
| `pgpool:pgpool` | unknown | 1 | pgpool-ii |
| `php-cli` | unknown | 2 | photoshow, rss2 |
| `php-json` | unknown | 3 | photoshow, roundcube, rss2 |
| `php-session` | unknown | 2 | photoshow, roundcube |
| `php-valkey` | unknown | 1 | cachet |
| `pillow==10.4.0` | unknown | 2 | immich-machine-learning, immich-ml |
| `pinecone-client` | unknown | 1 | pinecone |
| `pip3` | unknown | 4 | maxbot, neptune, objectrocket, singlestore |
| `pipefail\n#` | unknown | 1 | docker-clean |
| `placeholder` | unknown | 1 | organizer |
| `placeholder</h1` | unknown | 1 | cinny |
| `planka` | unknown | 1 | planka |
| `planka:planka` | unknown | 1 | planka |
| `postgraphile@__VAR__` | unknown | 1 | graphile |
| `postgresql-__VAR__-client` | unknown | 3 | postgres-backup, postgres-restore, postgresql-init |
| `postgresql-libs` | unknown | 3 | onlyoffice-communityserver, onlyoffice-documentserver, onlyoffice-documentserver-ee |
| `prefect` | unknown | 2 | prefect, prefect-server |
| `production` | unknown | 1 | singlestore |
| `provides` | unknown | 3 | neptune, objectrocket, singlestore |
| `ps` | unknown | 1 | docker-clean |
| `pulsar` | unknown | 2 | pulsar-functions, pulsar-proxy |
| `pymongo` | unknown | 1 | objectrocket |
| `pymysql` | unknown | 1 | singlestore |
| `pymysql,` | unknown | 1 | singlestore |
| `pymysql/sqlalchemy` | unknown | 1 | singlestore |
| `python` | unknown | 1 | meilisearch-python |
| `python:python` | unknown | 1 | meilisearch-python |
| `qbitmanage==4.2.0` | unknown | 1 | qbitmanage |
| `qbittorrent` | unknown | 2 | qbittorrent, qbittorrent-nox |
| `qbittorrent:qbittorrent` | unknown | 1 | qbittorrent |
| `questdb` | unknown | 1 | questdb |
| `r2c` | unknown | 1 | r2c-bench |
| `rabbitmq` | unknown | 7 | rabbitmq, rabbitmq-amqp, rabbitmq-delayed, rabbitmq-federation, rabbitmq-management... |
| `rabbitmq:rabbitmq` | unknown | 1 | rabbitmq |
| `rblake` | unknown | 1 | rblake |
| `redis` | unknown | 6 | argocd-redis, redis-cluster, redis-sentinel, redis-vert, redis7... |
| `redis:redis` | unknown | 1 | redis7 |
| `redisinsight` | unknown | 1 | redis-insight |
| `repo` | unknown | 7 | automatic1111, bazarr, bazarr-subliminal, comfyui, gallery3... |
| `repo-security` | unknown | 1 | repo-security |
| `repo-supervisor` | unknown | 1 | repo-supervisor |
| `requirements.txt` | unknown | 7 | automatic1111, bazarr, bazarr-subliminal, comfyui, gallery3... |
| `rmi` | unknown | 1 | docker-clean |
| `rmilter` | unknown | 1 | rmilter |
| `root:root` | unknown | 1 | sssd |
| `roundcube` | unknown | 1 | roundcube |
| `rss2email==3.15.1` | unknown | 1 | rss2email |
| `ruby-irb` | unknown | 1 | dependabot |
| `ruby-rdoc` | unknown | 1 | dependabot |
| `runner` | unknown | 2 | github-actions-minimal, github-actions-runner |
| `runner:runner` | unknown | 1 | github-actions-runner |
| `scikit-learn` | unknown | 2 | immich-machine-learning, jupyter-scikit |
| `scrapyd==1.5.0` | unknown | 1 | scrapyd |
| `script\n#` | unknown | 1 | docker-clean |
| `scylla` | unknown | 1 | scylladb |
| `searxng` | unknown | 1 | searxng |
| `searxng:searxng` | unknown | 1 | searxng |
| `secrets-scanner` | unknown | 1 | secrets-scanner |
| `secretz` | unknown | 1 | secretz |
| `shh` | unknown | 1 | shh |
| `sigal==2.3.0` | unknown | 1 | sigal |
| `singer-python` | unknown | 1 | singer |
| `singlestore` | unknown | 1 | singlestore |
| `sleep` | unknown | 5 | caddy-alpine, forgejo, grafana-toolkit, graphile, keycloak |
| `splunk` | unknown | 1 | splunk-forwarder |
| `sqlalchemy` | unknown | 1 | singlestore |
| `sqlalchemy,` | unknown | 1 | singlestore |
| `sqlite:sqlite` | unknown | 1 | sqlite |
| `stalwart` | unknown | 1 | stalwart-bitnami |
| `subliminal` | unknown | 1 | bazarr-subliminal |
| `synapse` | unknown | 1 | chat-server |
| `tensorboard` | unknown | 2 | tensor, tensorboard |
| `tensorboard==__VAR__` | unknown | 1 | tensor |
| `tensorflow` | unknown | 2 | jupyter-tensorflow, tensorflow |
| `the` | unknown | 1 | singlestore |
| `then` | unknown | 3 | caddy-alpine, cinny, keycloak |
| `then\n` | unknown | 1 | docker-clean |
| `this` | unknown | 3 | neptune, objectrocket, singlestore |
| `tigergraph` | unknown | 2 | tigergraph, tigergraph-ecosystem |
| `to` | unknown | 2 | neptune, objectrocket |
| `toolkit` | unknown | 1 | grafana-toolkit |
| `tools:` | unknown | 1 | neptune |
| `torch` | unknown | 4 | jupyter-pytorch, pytorch, text-generation-webui, transformers-gpu |
| `torchaudio` | unknown | 1 | pytorch |
| `torchvision` | unknown | 3 | jupyter-pytorch, pytorch, text-generation-webui |
| `transfer` | unknown | 1 | transferhelper |
| `transformers` | unknown | 3 | stable-diffusion, transformers, transformers-gpu |
| `transmission` | unknown | 1 | transmission |
| `transmission:transmission` | unknown | 1 | transmission |
| `true)\nfor` | unknown | 1 | docker-clean |
| `true)\nif` | unknown | 1 | docker-clean |
| `true\n` | unknown | 1 | docker-clean |
| `true\nfi\n\necho` | unknown | 1 | docker-clean |
| `user` | unknown | 1 | text-generation-webui |
| `user:user` | unknown | 1 | text-generation-webui |
| `usermod` | unknown | 1 | apache |
| `using` | unknown | 7 | automatic1111, bazarr, bazarr-subliminal, comfyui, gallery3... |
| `uvicorn==0.30.0` | unknown | 2 | immich-machine-learning, immich-ml |
| `v%s` | unknown | 6 | docker-clean, dotdns, keycloak, neptune, objectrocket... |
| `v1.5.2` | unknown | 2 | bazarr, bazarr-subliminal |
| `v1.9.3` | unknown | 2 | automatic1111, stable-diffusion-webui |
| `v3.0.0` | unknown | 1 | gallery3 |
| `v__VAR__` | unknown | 1 | text-generation-webui |
| `vecs` | unknown | 1 | vecs-db |
| `virtuoso` | unknown | 1 | virtuoso |
| `vlatest` | unknown | 1 | comfyui |
| `vllm` | unknown | 1 | vllm |
| `wandb` | unknown | 2 | wandb-server, weights-biases |
| `weaviate-client` | unknown | 1 | weaviate-python |
| `www-data` | unknown | 1 | apache |
| `xzf` | unknown | 5 | elasticsearch, elasticsearch-7, keycloak, neo4j, opensearch-dashboards |
| `your` | unknown | 3 | neptune, objectrocket, singlestore |
| `zigpy==0.60.0` | unknown | 4 | athom, homekit, zoe, zzh |
| `zoe` | unknown | 1 | zoe |
| `zzh` | unknown | 1 | zzh |

## Category Breakdown

| Category | Count | Examples |
|----------|-------|----------|
| debian-lib | 0 | — |
| debian-php | 0 | — |
| versioned | 0 | — |
| unknown | 319 | `#`, `*)`, `+x`, `-`, `2.5.0` |

## Per-Image Summary

### `389ds`

**Valid** (2): `ca-certificates`, `openldap`

**Invalid** (1): `65532:65532`

### `activemq`

**Valid** (2): `ca-certificates`, `openjdk-17-jre-base`

All packages valid.

### `adempiere`

**Valid** (1): `ca-certificates`

All packages valid.

### `airbyte`

**Valid** (1): `ca-certificates`

All packages valid.

### `airbyte-server`

**Valid** (1): `ca-certificates`

All packages valid.

### `airbyte-worker`

**Valid** (1): `ca-certificates`

All packages valid.

### `airsonic`

**Valid** (1): `ca-certificates`

**Invalid** (1): `app`

### `airsonic-advanced`

**Valid** (1): `ca-certificates`

**Invalid** (1): `app`

### `akaunting`

**Valid** (13): `ca-certificates`, `nginx`, `openssl`, `php`, `php-curl`, `php-fpm`, `php-intl`, `php-mbstring`, `php-mysqli`, `php-pdo`, `php-pdo_mysql`, `php-xml`, `zip`

**Invalid** (1): `65532:65532`

### `alpine`

**Valid** (2): `ca-certificates`, `tzdata`

All packages valid.

### `apache`

**Valid** (3): `apache2`, `ca-certificates`, `tzdata`

**Invalid** (5): `65532:65532`, `a2dismod`, `autoindex`, `usermod`, `www-data`

### `apache-nifi`

**Valid** (1): `ca-certificates`

**Invalid** (1): `nifi`

### `apache-ofbiz`

**Valid** (1): `ca-certificates`

All packages valid.

### `appsmith`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `appsmith-editor`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `appsmith-nginx`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `arango`

**Valid** (2): `ca-certificates`, `libstdc++`

**Invalid** (1): `arango`

### `argocd-redis`

**Valid** (1): `ca-certificates`

**Invalid** (1): `redis`

### `arm64`

**Valid** (2): `ca-certificates`, `tzdata`

All packages valid.

### `athom`

**Valid** (1): `ca-certificates`

**Invalid** (4): `65532:65532`, `athom`, `nogroup`, `zigpy==0.60.0`

### `audiobookshelf`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `audiobookshelf-opds`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `authentik`

**Valid** (7): `build-base`, `ca-certificates`, `libffi-dev`, `libpq`, `libxml2-dev`, `libxslt-dev`, `openssl-dev`

All packages valid.

### `authentik-geoip`

**Valid** (2): `ca-certificates`, `libpq`

All packages valid.

### `authentik-proxy`

**Valid** (2): `ca-certificates`, `libpq`

All packages valid.

### `authentik-worker`

**Valid** (7): `build-base`, `ca-certificates`, `libffi-dev`, `libpq`, `libxml2-dev`, `libxslt-dev`, `openssl-dev`

All packages valid.

### `automatic1111`

**Valid** (2): `build-base`, `ca-certificates`

**Invalid** (10): `-`, `app`, `app:app`, `available`, `clone`, `not`, `repo`, `requirements.txt`, `using`, `v1.9.3`

### `basic-auth-proxy`

**Valid** (4): `apache2`, `ca-certificates`, `libpcre2-8-0`, `zlib`

All packages valid.

### `bazarr`

**Valid** (2): `build-base`, `ca-certificates`

**Invalid** (10): `-`, `app`, `app:app`, `available`, `clone`, `not`, `repo`, `requirements.txt`, `using`, `v1.5.2`

### `bazarr-subliminal`

**Valid** (2): `build-base`, `ca-certificates`

**Invalid** (11): `-`, `app`, `app:app`, `available`, `clone`, `not`, `repo`, `requirements.txt`, `subliminal`, `using`, `v1.5.2`

### `browserless`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `browserless-chrome`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `browserless-edge`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `budibase`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `budibase-worker`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `buildah`

**Valid** (2): `ca-certificates`, `containers-common`

All packages valid.

### `bundler`

**Valid** (4): `build-base`, `ca-certificates`, `ruby`, `ruby-dev`

**Invalid** (4): `2.5.0`, `app`, `app:app`, `bundler`

### `busybox`

**Valid** (1): `ca-certificates`

All packages valid.

### `cachet`

**Valid** (13): `ca-certificates`, `nginx`, `php-bcmath`, `php-curl`, `php-fpm`, `php-gd`, `php-mbstring`, `php-mysqli`, `php-pdo_mysql`, `php-pdo_sqlite`, `php-pgsql`, `php-xml`, `php-zip`

**Invalid** (1): `php-valkey`

### `caddy-alpine`

**Valid** (2): `ca-certificates`, `libcap`

**Invalid** (5): `+x`, `fi`, `if`, `sleep`, `then`

### `calibre`

**Valid** (2): `ca-certificates`, `xdg-utils`

**Invalid** (3): `app`, `app:app`, `calibre`

### `calibre-eb`

**Valid** (1): `ca-certificates`

**Invalid** (3): `app`, `app:app`, `calibre`

### `calibre-server`

**Valid** (1): `ca-certificates`

**Invalid** (3): `app`, `app:app`, `calibre`

### `calibre-web`

**Valid** (1): `ca-certificates`

**Invalid** (2): `65532:65532`, `calibre`

### `cargo-audit`

**Valid** (1): `ca-certificates`

All packages valid.

### `chartdb`

**Valid** (1): `ca-certificates`

**Invalid** (1): `chartdb`

### `chat-relay`

**Valid** (1): `ca-certificates`

**Invalid** (1): `complement`

### `chat-server`

**Valid** (4): `build-base`, `ca-certificates`, `py3-pip`, `python3`

**Invalid** (3): `65532:65532`, `matrix-synapse==__VAR__`, `synapse`

### `chevereto`

**Valid** (10): `php`, `php-curl`, `php-fpm`, `php-gd`, `php-mbstring`, `php-mysqli`, `php-pdo_mysql`, `php-pdo_sqlite`, `php-xml`, `php-zip`

All packages valid.

### `chkrootkit`

**Valid** (1): `ca-certificates`

All packages valid.

### `chroma`

**Valid** (2): `build-base`, `ca-certificates`

**Invalid** (4): `chroma`, `chroma:chroma`, `chromadb`, `chromadb==__VAR__`

### `chroma-all-minimal`

**Valid** (1): `ca-certificates`

**Invalid** (3): `app`, `app:app`, `chromadb==0.5.23`

### `cinny`

**Valid** (1): `ca-certificates`

**Invalid** (5): `appuser`, `fi`, `if`, `placeholder</h1`, `then`

### `clamav`

**Valid** (3): `ca-certificates`, `clamav`, `clamav-daemon`

All packages valid.

### `clamav-daemon`

**Valid** (4): `ca-certificates`, `clamav`, `clamav-daemon`, `freshclam`

All packages valid.

### `cockpit`

**Valid** (1): `ca-certificates`

All packages valid.

### `codimd`

**Valid** (3): `ca-certificates`, `nodejs-20`, `python3`

**Invalid** (1): `codimd`

### `collabora-online`

**Valid** (2): `ca-certificates`, `gnupg`

**Invalid** (1): `65532:65532`

### `collabora-online-code`

**Valid** (2): `ca-certificates`, `gnupg`

**Invalid** (1): `65532:65532`

### `comfyui`

**Valid** (2): `build-base`, `ca-certificates`

**Invalid** (10): `-`, `app`, `app:app`, `available`, `clone`, `not`, `repo`, `requirements.txt`, `using`, `vlatest`

### `composer-audit`

**Valid** (6): `ca-certificates`, `php`, `php-curl`, `php-mbstring`, `php-xml`, `unzip`

All packages valid.

### `conduit-admin`

**Valid** (2): `ca-certificates`, `sqlite-libs`

**Invalid** (1): `conduit`

### `convector`

**Valid** (2): `ca-certificates`, `nodejs-20`

**Invalid** (3): `65532:65532`, `@worldsibu/convector-platform@__VAR__`, `convector`

### `coqui-tts`

**Valid** (1): `ca-certificates`

**Invalid** (3): `TTS`, `app`, `app:app`

### `cors-proxy`

**Valid** (3): `ca-certificates`, `libpcre2-8-0`, `zlib`

All packages valid.

### `couchbase`

**Valid** (3): `libstdc++`, `procps`, `zlib`

All packages valid.

### `couchdb`

**Valid** (2): `couchdb`, `procps`

All packages valid.

### `couchdb-sync`

**Valid** (1): `procps`

All packages valid.

### `courier-authlib`

**Valid** (1): `ca-certificates`

All packages valid.

### `courier-imap`

**Valid** (1): `ca-certificates`

All packages valid.

### `crate`

**Valid** (2): `ca-certificates`, `python3`

**Invalid** (1): `crate`

### `cryptpad`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `cyberchef`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `cyberchef-node`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `dagster`

**Valid** (1): `ca-certificates`

**Invalid** (4): `app`, `app:app`, `dagster`, `dagster-webserver`

### `dagster-daemon`

**Valid** (1): `ca-certificates`

**Invalid** (3): `app`, `app:app`, `dagster`

### `dagster-logs`

**Valid** (1): `ca-certificates`

**Invalid** (3): `app`, `app:app`, `dagster`

### `dashy-alpine`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `dbmate`

**Valid** (1): `ca-certificates`

**Invalid** (1): `+x`

### `debian-slim`

**Valid** (3): `ca-certificates`, `dumb-init`, `tzdata`

**Invalid** (1): `appuser`

### `deepspeed`

**Valid** (1): `ca-certificates`

**Invalid** (3): `app`, `app:app`, `deepspeed`

### `dendrite-pot`

**Valid** (1): `ca-certificates`

**Invalid** (1): `dendrite`

### `dependabot`

**Valid** (11): `ca-certificates`, `gmp`, `gnupg`, `libffi`, `mpdecimal`, `ncurses`, `nodejs`, `readline`, `ruby`, `yaml`, `zlib`

**Invalid** (2): `ruby-irb`, `ruby-rdoc`

### `derby`

**Valid** (1): `ca-certificates`

**Invalid** (1): `derby`

### `diffusers`

**Valid** (1): `ca-certificates`

**Invalid** (3): `app`, `app:app`, `diffusers`

### `dnsdist`

**Valid** (1): `ca-certificates`

All packages valid.

### `dnsmasq-full`

**Valid** (1): `ca-certificates`

All packages valid.

### `docker-bench`

**Valid** (1): `ca-certificates`

All packages valid.

### `docker-clean`

**Valid** (3): `ca-certificates`, `docker`, `docker-cli`

**Invalid** (32): `+x`, `-`, `65532:65532`, `Based`, `Docker`, `cid`, `cleanup`, `common`, `container:`, `created=$(docker`, `dangling`, `do\n`, `docker-clean`, `dockerclean`, `exited`, `fi\ndone\n\ndangling_images=$(docker`, `if`, `images`, `in`, `inspect`, `nogroup`, `on`, `pipefail\n#`, `ps`, `rmi`, `script\n#`, `then\n`, `true)\nfor`, `true)\nif`, `true\n`, `true\nfi\n\necho`, `v%s`

### `docker-gc`

**Valid** (2): `ca-certificates`, `docker-cli`

All packages valid.

### `docker-socket-proxy`

**Valid** (2): `ca-certificates`, `haproxy`

**Invalid** (2): `65532:65532`, `dsp`

### `dockerfile-lint`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `dolibarr`

**Valid** (15): `ca-certificates`, `json-c`, `nginx`, `openssl`, `php`, `php-curl`, `php-fpm`, `php-gd`, `php-intl`, `php-mbstring`, `php-mysqli`, `php-pdo`, `php-pdo_mysql`, `php-xml`, `zip`

**Invalid** (1): `65532:65532`

### `dotdns`

**Valid** (2): `ca-certificates`, `go`

**Invalid** (7): `CGO_ENABLED=0`, `GOARCH=__VAR__`, `GOOS=linux`, `build`, `main()`, `main\nimport`, `v%s`

### `dovecot`

**Valid** (1): `ca-certificates`

All packages valid.

### `dovecot-lda`

**Valid** (1): `ca-certificates`

All packages valid.

### `dovecot-pop3`

**Valid** (1): `ca-certificates`

All packages valid.

### `druid`

**Valid** (3): `ca-certificates`, `druid`, `python3`

All packages valid.

### `duplicati`

**Valid** (2): `ca-certificates`, `dotnet`

**Invalid** (2): `+x`, `8.0`

### `egroupware`

**Valid** (15): `ca-certificates`, `json-c`, `nginx`, `openssl`, `php`, `php-curl`, `php-fpm`, `php-gd`, `php-intl`, `php-mbstring`, `php-mysqli`, `php-pdo`, `php-pdo_mysql`, `php-xml`, `zip`

**Invalid** (1): `65532:65532`

### `ejdb`

**Valid** (2): `ca-certificates`, `libstdc++`

**Invalid** (1): `ejdb`

### `elasticsearch`

**Valid** (1): `ca-certificates`

**Invalid** (1): `xzf`

### `elasticsearch-7`

**Valid** (1): `ca-certificates`

**Invalid** (1): `xzf`

### `elasticsearch-8`

**Valid** (1): `ca-certificates`

All packages valid.

### `elasticsearch-curator`

**Valid** (1): `ca-certificates`

All packages valid.

### `element-web`

**Valid** (1): `ca-certificates`

**Invalid** (1): `appuser`

### `element-x`

**Valid** (1): `ca-certificates`

**Invalid** (1): `appuser`

### `emby`

**Valid** (4): `ca-certificates`, `fontconfig`, `freetype`, `glib`

All packages valid.

### `emby-server`

**Valid** (4): `ca-certificates`, `fontconfig`, `freetype`, `glib`

All packages valid.

### `emqx`

**Valid** (2): `ca-certificates`, `procps`

All packages valid.

### `emqx-ee`

**Valid** (2): `ca-certificates`, `procps`

All packages valid.

### `eqonomize`

**Valid** (1): `ca-certificates`

All packages valid.

### `erpnext`

**Valid** (1): `ca-certificates`

**Invalid** (2): `erpnext`, `erpnext:erpnext`

### `espocrm`

**Valid** (15): `ca-certificates`, `json-c`, `nginx`, `openssl`, `php`, `php-curl`, `php-fpm`, `php-gd`, `php-intl`, `php-mbstring`, `php-mysqli`, `php-pdo`, `php-pdo_mysql`, `php-xml`, `zip`

**Invalid** (1): `65532:65532`

### `fail2ban`

**Valid** (1): `ca-certificates`

**Invalid** (2): `appuser`, `appuser:appuser`

### `fail2ban-exporter`

**Invalid** (1): `clone`

### `falco`

**Valid** (1): `ca-certificates`

All packages valid.

### `falco-rules`

**Valid** (1): `ca-certificates`

All packages valid.

### `faster-whisper`

**Valid** (3): `ca-certificates`, `py3-pip`, `python3`

**Invalid** (5): `add`, `apk`, `app`, `app:app`, `faster-whisper`

### `firebird`

**Valid** (1): `ca-certificates`

**Invalid** (2): `65532:65532`, `firebird`

### `firefly-iii`

**Valid** (8): `php`, `php-curl`, `php-fpm`, `php-mbstring`, `php-mysqli`, `php-pdo_mysql`, `php-xml`, `php-zip`

All packages valid.

### `fluent-bit`

**Valid** (1): `ca-certificates`

All packages valid.

### `fluentd`

**Valid** (4): `ca-certificates`, `libffi-dev`, `tzdata`, `yaml`

**Invalid** (1): `fluentd`

### `focalboard-server`

**Valid** (1): `ca-certificates`

All packages valid.

### `forgejo`

**Valid** (1): `ca-certificates`

**Invalid** (2): `+x`, `sleep`

### `freeipa-client`

**Valid** (1): `ca-certificates`

**Invalid** (1): `65532:65532`

### `freshclam`

**Valid** (2): `ca-certificates`, `clamav-freshclam`

All packages valid.

### `freshrss`

**Valid** (6): `php`, `php-curl`, `php-fpm`, `php-mbstring`, `php-xml`, `php-zip`

All packages valid.

### `freshrss-minimal`

**Valid** (10): `php`, `php-curl`, `php-fpm`, `php-intl`, `php-mbstring`, `php-mysqli`, `php-pdo_mysql`, `php-pdo_sqlite`, `php-xml`, `php-zip`

All packages valid.

### `frontaccounting`

**Valid** (13): `ca-certificates`, `nginx`, `openssl`, `php`, `php-curl`, `php-fpm`, `php-intl`, `php-mbstring`, `php-mysqli`, `php-pdo`, `php-pdo_mysql`, `php-xml`, `zip`

**Invalid** (1): `65532:65532`

### `gallery3`

**Valid** (2): `build-base`, `ca-certificates`

**Invalid** (10): `-`, `app`, `app:app`, `available`, `clone`, `not`, `repo`, `requirements.txt`, `using`, `v3.0.0`

### `gem-audit`

**Valid** (2): `ca-certificates`, `ruby`

All packages valid.

### `git-secrets`

**Valid** (1): `ca-certificates`

All packages valid.

### `gitbucket`

**Valid** (1): `ca-certificates`

**Invalid** (6): `65532:65532`, `add`, `apk`, `gitbucket`, `java-21-default-jdk`, `openjdk-21-jdk-headless`

### `gitea`

**Valid** (1): `ca-certificates`

**Invalid** (8): `#`, `*)`, `+x`, `ARCH=$(case`, `amd64)`, `arm64)`, `esac)`, `in`

### `github-actions-minimal`

**Valid** (2): `ca-certificates`, `nodejs-20`

**Invalid** (1): `runner`

### `github-actions-runner`

**Valid** (1): `ca-certificates`

**Invalid** (2): `runner`, `runner:runner`

### `gitlab-backup`

**Valid** (3): `ca-certificates`, `openssh-client`, `ruby`

**Invalid** (2): `65532:65532`, `backup`

### `gitlab-ce`

**Valid** (4): `ca-certificates`, `gnupg`, `openssh-client`, `postfix`

All packages valid.

### `gitlab-ee`

**Valid** (4): `ca-certificates`, `gnupg`, `openssh-client`, `postfix`

All packages valid.

### `gitlab-geo`

**Valid** (4): `ca-certificates`, `gnupg`, `openssh-client`, `postgresql-client`

All packages valid.

### `gnucash`

**Valid** (1): `ca-certificates`

**Invalid** (1): `65532:65532`

### `golang`

**Valid** (1): `ca-certificates`

All packages valid.

### `gradle`

**Valid** (1): `ca-certificates`

All packages valid.

### `grafana`

**Valid** (3): `ca-certificates`, `fontconfig`, `tzdata`

All packages valid.

### `grafana-image-renderer`

**Valid** (1): `ca-certificates`

All packages valid.

### `grafana-toolkit`

**Valid** (2): `ca-certificates`, `nodejs-20`

**Invalid** (5): `+x`, `65532:65532`, `@grafana/toolkit@__VAR__`, `sleep`, `toolkit`

### `graphdb-enterpriser`

**Valid** (1): `ca-certificates`

**Invalid** (1): `graphdb`

### `graphile`

**Valid** (2): `ca-certificates`, `nodejs-20`

**Invalid** (5): `+x`, `65532:65532`, `graphile`, `postgraphile@__VAR__`, `sleep`

### `graylog`

**Valid** (1): `ca-certificates`

**Invalid** (1): `graylog`

### `grisbi`

**Valid** (1): `ca-certificates`

**Invalid** (1): `65532:65532`

### `h2`

**Valid** (1): `ca-certificates`

**Invalid** (1): `h2`

### `hackmd`

**Valid** (3): `ca-certificates`, `nodejs-20`, `python3`

All packages valid.

### `haproxy`

**Valid** (2): `ca-certificates`, `haproxy`

All packages valid.

### `haproxy-dev`

**Valid** (2): `ca-certificates`, `haproxy`

All packages valid.

### `haproxy-lb`

**Valid** (2): `ca-certificates`, `haproxy`

All packages valid.

### `hazelcast`

**Valid** (1): `ca-certificates`

**Invalid** (2): `65532:65532`, `hazelcast`

### `hedgedoc`

**Valid** (3): `ca-certificates`, `nodejs-20`, `python3`

All packages valid.

### `hedgedoc-legacy`

**Valid** (3): `ca-certificates`, `nodejs-20`, `python3`

All packages valid.

### `heimdall`

**Valid** (3): `ca-certificates`, `nginx`, `nodejs-20`

All packages valid.

### `heimdall-lite`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `hive`

**Valid** (1): `ca-certificates`

**Invalid** (1): `hive`

### `hive-metastore`

**Valid** (1): `ca-certificates`

**Invalid** (1): `hive`

### `homeassistant`

**Valid** (2): `ca-certificates`, `python3`

**Invalid** (2): `homeassistant`, `homeassistant:homeassistant`

### `homebridge`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `homebridge-camera`

**Valid** (3): `ca-certificates`, `ffmpeg`, `nodejs-20`

All packages valid.

### `homekit`

**Valid** (1): `ca-certificates`

**Invalid** (4): `65532:65532`, `homekit`, `nogroup`, `zigpy==0.60.0`

### `hydrogen`

**Valid** (1): `ca-certificates`

**Invalid** (1): `hydrogen`

### `idempiere`

**Valid** (1): `ca-certificates`

All packages valid.

### `ignite`

**Valid** (1): `ca-certificates`

**Invalid** (1): `ignite`

### `immich`

**Valid** (3): `ca-certificates`, `ffmpeg`, `nodejs-20`

**Invalid** (2): `immich`, `immich:immich`

### `immich-machine-learning`

**Valid** (1): `ca-certificates`

**Invalid** (8): `app`, `app:app`, `fastapi==0.115.0`, `numpy==2.1.0`, `onnxruntime`, `pillow==10.4.0`, `scikit-learn`, `uvicorn==0.30.0`

### `immich-microservices`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `immich-ml`

**Valid** (1): `ca-certificates`

**Invalid** (6): `app`, `app:app`, `fastapi==0.115.0`, `onnxruntime`, `pillow==10.4.0`, `uvicorn==0.30.0`

### `immich-server`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `invoice-ninja`

**Valid** (14): `ca-certificates`, `nginx`, `openssl`, `php`, `php-curl`, `php-fpm`, `php-gd`, `php-intl`, `php-mbstring`, `php-mysqli`, `php-pdo`, `php-pdo_mysql`, `php-xml`, `zip`

**Invalid** (1): `65532:65532`

### `invoice-ninja-api`

**Valid** (14): `ca-certificates`, `nginx`, `openssl`, `php`, `php-curl`, `php-fpm`, `php-gd`, `php-intl`, `php-mbstring`, `php-mysqli`, `php-pdo`, `php-pdo_mysql`, `php-xml`, `zip`

**Invalid** (1): `65532:65532`

### `invokeai`

**Valid** (1): `ca-certificates`

**Invalid** (3): `app`, `app:app`, `invokeai`

### `iobroker`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `it-tools-legacy`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `janusgraph`

**Valid** (1): `ca-certificates`

**Invalid** (1): `janusgraph`

### `jellyfin`

**Valid** (7): `ca-certificates`, `icu-libs`, `jellyfin`, `krb5-libs`, `libgcc`, `libstdc++`, `zlib`

All packages valid.

### `jellyfin-ffmpeg`

**Valid** (3): `ca-certificates`, `freetype`, `zlib`

All packages valid.

### `jellyfin-server`

**Valid** (7): `ca-certificates`, `icu-libs`, `jellyfin`, `krb5-libs`, `libgcc`, `libstdc++`, `zlib`

All packages valid.

### `jenkins`

**Valid** (3): `ca-certificates`, `jenkins`, `openjdk-17-jre-base`

**Invalid** (1): `jenkins:jenkins`

### `jenkins-agent`

**Valid** (1): `ca-certificates`

All packages valid.

### `jenkins-executor`

**Valid** (1): `ca-certificates`

All packages valid.

### `jenkins-plugin`

**Valid** (1): `ca-certificates`

All packages valid.

### `jitsu`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `jupyter-all`

**Valid** (1): `ca-certificates`

**Invalid** (3): `app`, `app:app`, `jupyter`

### `jupyter-pytorch`

**Valid** (1): `ca-certificates`

**Invalid** (5): `app`, `app:app`, `jupyterlab`, `torch`, `torchvision`

### `jupyter-scikit`

**Valid** (1): `ca-certificates`

**Invalid** (7): `app`, `app:app`, `jupyterlab`, `matplotlib`, `numpy==2.1.0`, `pandas==2.2.0`, `scikit-learn`

### `jupyter-tensorflow`

**Valid** (1): `ca-certificates`

**Invalid** (4): `app`, `app:app`, `jupyterlab`, `tensorflow`

### `kafka`

**Valid** (2): `ca-certificates`, `kafka`

All packages valid.

### `kafka-connect`

**Valid** (1): `ca-certificates`

**Invalid** (1): `connect`

### `kafka-manager`

**Valid** (1): `ca-certificates`

**Invalid** (1): `cmak`

### `kaniko`

**Valid** (2): `ca-certificates`, `kaniko`

All packages valid.

### `keycloak`

**Valid** (2): `ca-certificates`, `keycloak`

**Invalid** (8): `+x`, `65532:65532`, `fi`, `if`, `sleep`, `then`, `v%s`, `xzf`

### `keycloak-init`

**Valid** (1): `ca-certificates`

All packages valid.

### `keycloak-quarkus`

**Valid** (1): `ca-certificates`

All packages valid.

### `kibana`

**Valid** (1): `ca-certificates`

**Invalid** (1): `kibana`

### `kibana-oss`

**Valid** (1): `ca-certificates`

**Invalid** (1): `kibana`

### `kmymoney`

**Valid** (1): `ca-certificates`

**Invalid** (1): `65532:65532`

### `knot-resolver`

**Valid** (2): `bind-tools`, `ca-certificates`

**Invalid** (6): `65532:65532`, `add`, `apk`, `knot`, `knot-resolver`, `knot-resolver-utils`

### `koel`

**Valid** (11): `php`, `php-bcmath`, `php-curl`, `php-fpm`, `php-gd`, `php-mbstring`, `php-mysqli`, `php-pdo_mysql`, `php-pdo_sqlite`, `php-xml`, `php-zip`

All packages valid.

### `koel-next`

**Valid** (11): `php`, `php-bcmath`, `php-curl`, `php-fpm`, `php-gd`, `php-mbstring`, `php-mysqli`, `php-pdo_mysql`, `php-pdo_sqlite`, `php-xml`, `php-zip`

All packages valid.

### `koken`

**Valid** (9): `php`, `php-curl`, `php-fpm`, `php-gd`, `php-mbstring`, `php-mysqli`, `php-pdo_mysql`, `php-xml`, `php-zip`

All packages valid.

### `kopano`

**Valid** (10): `php`, `php-curl`, `php-fpm`, `php-gd`, `php-mbstring`, `php-mysqli`, `php-pdo_mysql`, `php-soap`, `php-xml`, `php-zip`

All packages valid.

### `kube-apiserver`

**Valid** (1): `ca-certificates`

All packages valid.

### `kube-controller`

**Valid** (1): `ca-certificates`

All packages valid.

### `kube-proxy`

**Valid** (2): `ca-certificates`, `iptables`

All packages valid.

### `kube-scheduler`

**Valid** (1): `ca-certificates`

All packages valid.

### `langchain`

**Valid** (1): `ca-certificates`

**Invalid** (3): `app`, `app:app`, `langchain`

### `langserve`

**Valid** (1): `ca-certificates`

**Invalid** (3): `app`, `app:app`, `langserve`

### `ldap`

**Valid** (1): `ca-certificates`

**Invalid** (2): `ldap`, `ldap:ldap`

### `ldap-account-manager`

**Valid** (6): `ca-certificates`, `php-curl`, `php-fpm`, `php-ldap`, `php-mbstring`, `php-xml`

All packages valid.

### `ldapbrowser`

**Valid** (1): `ca-certificates`

All packages valid.

### `ledger`

**Valid** (1): `ca-certificates`

All packages valid.

### `libreoffice`

**Valid** (1): `ca-certificates`

**Invalid** (1): `65532:65532`

### `libreoffice-headless`

**Valid** (1): `ca-certificates`

**Invalid** (1): `65532:65532`

### `libsql`

**Valid** (4): `ca-certificates`, `libgcc`, `tzdata`, `xz`

**Invalid** (6): `*)`, `ARCH=$(case`, `amd64)`, `arm64)`, `esac)`, `in`

### `lidarr`

**Valid** (6): `ca-certificates`, `icu-libs`, `krb5-libs`, `libgcc`, `libstdc++`, `zlib`

**Invalid** (1): `app`

### `linguist`

**Valid** (2): `ca-certificates`, `ruby`

All packages valid.

### `litellm`

**Valid** (1): `ca-certificates`

**Invalid** (3): `app`, `app:app`, `litellm`

### `litellm-proxy`

**Valid** (1): `ca-certificates`

**Invalid** (3): `app`, `app:app`, `litellm[proxy]`

### `litestream`

**Valid** (1): `ca-certificates`

**Invalid** (6): `*)`, `amd64)`, `arm64)`, `case`, `esac`, `in`

### `localai-loadbalancer`

**Valid** (1): `ca-certificates`

All packages valid.

### `logseq`

**Valid** (2): `ca-certificates`, `nodejs-20`

**Invalid** (2): `node`, `node:node`

### `logstash`

**Valid** (2): `ca-certificates`, `logstash`

All packages valid.

### `logstash-oss`

**Valid** (2): `ca-certificates`, `logstash`

All packages valid.

### `lychee`

**Valid** (11): `php`, `php-curl`, `php-exif`, `php-fpm`, `php-gd`, `php-mbstring`, `php-mysqli`, `php-pdo_mysql`, `php-pdo_sqlite`, `php-xml`, `php-zip`

All packages valid.

### `lynis`

**Valid** (1): `ca-certificates`

All packages valid.

### `mailtrain`

**Valid** (2): `ca-certificates`, `nodejs-20`

**Invalid** (3): `add`, `apk`, `appuser`

### `maldet`

**Valid** (3): `ca-certificates`, `clamav-daemon`, `inotify-tools`

All packages valid.

### `mariadb`

**Valid** (1): `ca-certificates`

All packages valid.

### `mariadb-10`

**Valid** (2): `ca-certificates`, `mysql`

**Invalid** (1): `65532:65532`

### `mariadb-11`

**Valid** (2): `ca-certificates`, `mysql`

**Invalid** (1): `65532:65532`

### `mariadb-galera`

**Valid** (5): `ca-certificates`, `mariadb-backup`, `mysql`, `rsync`, `socat`

**Invalid** (1): `65532:65532`

### `matrix-hookshot`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `mattermost`

**Valid** (2): `ca-certificates`, `tzdata`

All packages valid.

### `mattermost-bridge`

**Valid** (1): `ca-certificates`

**Invalid** (1): `appuser`

### `maven`

**Valid** (1): `ca-certificates`

All packages valid.

### `maxbot`

**Valid** (3): `ca-certificates`, `py3-pip`, `python3`

**Invalid** (4): `65532:65532`, `app`, `maxbot==__VAR__`, `pip3`

### `meilisearch-python`

**Valid** (1): `ca-certificates`

**Invalid** (2): `python`, `python:python`

### `meltano`

**Valid** (1): `ca-certificates`

**Invalid** (3): `app`, `app:app`, `meltano`

### `memcached`

**Valid** (2): `ca-certificates`, `memcached`

All packages valid.

### `memgraph`

**Valid** (2): `ca-certificates`, `python3`

**Invalid** (1): `memgraph`

### `milvus`

**Valid** (1): `ca-certificates`

All packages valid.

### `milvus-etcd`

**Valid** (2): `ca-certificates`, `etcd`

All packages valid.

### `milvus-minio`

**Valid** (1): `ca-certificates`

**Invalid** (3): `+x`, `apk`, `del`

### `mlflow`

**Valid** (2): `ca-certificates`, `mlflow`

**Invalid** (2): `app`, `app:app`

### `mlflow-server`

**Valid** (2): `ca-certificates`, `mlflow`

**Invalid** (2): `app`, `app:app`

### `mlflow-tracking`

**Valid** (2): `ca-certificates`, `mlflow`

**Invalid** (2): `app`, `app:app`

### `modsecurity`

**Valid** (2): `apache2`, `ca-certificates`

**Invalid** (2): `appuser`, `appuser:appuser`

### `modsecurity-crs`

**Valid** (2): `ca-certificates`, `libxml2-dev`

**Invalid** (1): `modsec`

### `mongodb`

**Valid** (1): `ca-certificates`

All packages valid.

### `mongodb-5`

**Valid** (1): `ca-certificates`

**Invalid** (2): `65532:65532`, `mongodb`

### `mongodb-6`

**Valid** (1): `ca-certificates`

All packages valid.

### `mongodb-7`

**Valid** (1): `ca-certificates`

**Invalid** (2): `65532:65532`, `mongodb`

### `mongodb-community`

**Valid** (1): `ca-certificates`

**Invalid** (2): `65532:65532`, `mongodb`

### `mongodb-opsmanager`

**Valid** (1): `ca-certificates`

**Invalid** (1): `mongosh`

### `mosquito`

**Valid** (2): `ca-certificates`, `mosquitto-clients`

All packages valid.

### `mosquitto`

**Valid** (2): `ca-certificates`, `mosquitto`

All packages valid.

### `mosquitto-dev`

**Valid** (3): `ca-certificates`, `mosquitto`, `mosquitto-clients`

All packages valid.

### `mozilla-hubs`

**Valid** (2): `ca-certificates`, `nodejs-20`

**Invalid** (3): `add`, `apk`, `appuser`

### `mqtt`

**Valid** (2): `ca-certificates`, `mosquitto`

**Invalid** (1): `mosquitto:mosquitto`

### `mysql`

**Valid** (1): `ca-certificates`

All packages valid.

### `mysql-8`

**Valid** (3): `ca-certificates`, `gnupg`, `psmisc`

All packages valid.

### `mysql-anonymizer`

**Valid** (1): `ca-certificates`

All packages valid.

### `mysql-backup`

**Valid** (1): `ca-certificates`

All packages valid.

### `mysql-init`

**Valid** (1): `ca-certificates`

All packages valid.

### `mysql-restore`

**Valid** (1): `ca-certificates`

All packages valid.

### `mythtv`

**Valid** (1): `ca-certificates`

**Invalid** (2): `mythtv`, `mythtv:mythtv`

### `n8n`

**Valid** (2): `ca-certificates`, `nodejs-20`

**Invalid** (2): `node`, `node:node`

### `n8n-nodes`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `n8n-webhook`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `neo4j`

**Valid** (1): `ca-certificates`

**Invalid** (1): `xzf`

### `neptune`

**Valid** (3): `ca-certificates`, `py3-pip`, `python3`

**Invalid** (34): `+x`, `-`, `65532:65532`, `AWS`, `Gremlin/SPARQL`, `Neptune`, `Neptune-compatible`, `SPARQLWrapper`, `a`, `as`, `base`, `compatibility`, `database`, `development`, `endpoint`, `for`, `fully`, `graph`, `gremlinpython`, `gremlinpython,`, `image`, `import`, `in`, `is`, `local`, `managed`, `neptune`, `pip3`, `provides`, `this`, `to`, `tools:`, `v%s`, `your`

### `newsboat`

**Valid** (1): `ca-certificates`

**Invalid** (2): `newsboat`, `newsboat:newsboat`

### `nextcloud`

**Valid** (13): `ca-certificates`, `nginx`, `php`, `php-curl`, `php-fpm`, `php-gd`, `php-intl`, `php-mbstring`, `php-mysqli`, `php-pdo_mysql`, `php-xml`, `sqlite-libs`, `zip`

**Invalid** (1): `65532:65532`

### `nextcloud-alpine`

**Valid** (13): `ca-certificates`, `nginx`, `php`, `php-curl`, `php-fpm`, `php-gd`, `php-intl`, `php-mbstring`, `php-mysqli`, `php-pdo_mysql`, `php-xml`, `sqlite-libs`, `zip`

**Invalid** (1): `65532:65532`

### `nextcloud-external`

**Valid** (13): `ca-certificates`, `nginx`, `php`, `php-curl`, `php-fpm`, `php-gd`, `php-intl`, `php-mbstring`, `php-mysqli`, `php-pdo_mysql`, `php-xml`, `sqlite-libs`, `zip`

**Invalid** (1): `65532:65532`

### `nextcloud-imaging`

**Valid** (13): `ca-certificates`, `nginx`, `php`, `php-curl`, `php-fpm`, `php-gd`, `php-intl`, `php-mbstring`, `php-mysqli`, `php-pdo_mysql`, `php-xml`, `sqlite-libs`, `zip`

**Invalid** (1): `65532:65532`

### `nextcloud-nginx`

**Valid** (13): `ca-certificates`, `nginx`, `php`, `php-curl`, `php-fpm`, `php-gd`, `php-intl`, `php-mbstring`, `php-mysqli`, `php-pdo_mysql`, `php-xml`, `sqlite-libs`, `zip`

**Invalid** (1): `65532:65532`

### `nginx-alpine`

**Valid** (1): `ca-certificates`

All packages valid.

### `nginx-cache`

**Valid** (1): `ca-certificates`

All packages valid.

### `nginx-modsec`

**Valid** (3): `ca-certificates`, `libxml2`, `nginx`

**Invalid** (1): `65532:65532`

### `nheko`

**Valid** (2): `ca-certificates`, `glib`

**Invalid** (1): `nheko`

### `nifi-registry`

**Valid** (1): `ca-certificates`

**Invalid** (1): `nifi`

### `node`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `node-red`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `node-red-admin`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `npm-audit`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `objectrocket`

**Valid** (3): `ca-certificates`, `py3-pip`, `python3`

**Invalid** (31): `+x`, `-`, `65532:65532`, `Atlas`, `MongoDB`, `ObjectRocket-compatible`, `ObjectRocket/MongoDB`, `a`, `as`, `base`, `client`, `cloud`, `database`, `development`, `endpoint`, `for`, `fully`, `image`, `import`, `in`, `is`, `library`, `managed`, `objectrocket`, `pip3`, `provides`, `pymongo`, `this`, `to`, `v%s`, `your`

### `ocserv`

**Valid** (1): `ca-certificates`

All packages valid.

### `ol_fileshare`

**Valid** (2): `ca-certificates`, `tzdata`

**Invalid** (2): `65532:65532`, `fileshare`

### `onlyoffice-communityserver`

**Valid** (10): `ca-certificates`, `fontconfig`, `freetype`, `libgcc`, `libjpeg-turbo`, `libpng`, `libstdc++`, `libxml2`, `libxslt`, `tzdata`

**Invalid** (4): `libcurl`, `mariadb-libs`, `openssl-libs`, `postgresql-libs`

### `onlyoffice-controlpanel`

**Valid** (10): `ca-certificates`, `fontconfig`, `freetype`, `libgcc`, `libjpeg-turbo`, `libpng`, `libstdc++`, `libxml2`, `libxslt`, `tzdata`

**Invalid** (2): `libcurl`, `openssl-libs`

### `onlyoffice-documentserver`

**Valid** (15): `ca-certificates`, `fontconfig`, `freetype`, `glib`, `graphite2`, `harfbuzz`, `libgcc`, `libjpeg-turbo`, `libpng`, `libstdc++`, `libwebp`, `libxml2`, `libxslt`, `tzdata`, `zlib`

**Invalid** (5): `bzip2-libs`, `libcurl`, `libtiff`, `openssl-libs`, `postgresql-libs`

### `onlyoffice-documentserver-ee`

**Valid** (15): `ca-certificates`, `fontconfig`, `freetype`, `glib`, `graphite2`, `harfbuzz`, `libgcc`, `libjpeg-turbo`, `libpng`, `libstdc++`, `libwebp`, `libxml2`, `libxslt`, `tzdata`, `zlib`

**Invalid** (5): `bzip2-libs`, `libcurl`, `libtiff`, `openssl-libs`, `postgresql-libs`

### `open-webui`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `open-webui-api`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `opengpts`

**Valid** (1): `ca-certificates`

**Invalid** (3): `app`, `app:app`, `open-gpts`

### `openhab`

**Valid** (1): `ca-certificates`

**Invalid** (5): `add`, `apk`, `java-21-default-jdk`, `openhab`, `openjdk-21-jdk-headless`

### `openhab3`

**Valid** (2): `ca-certificates`, `libffi-dev`

All packages valid.

### `openjdk`

**Valid** (3): `ca-certificates`, `fontconfig`, `freetype`

All packages valid.

### `openjdk-alpine`

**Valid** (1): `ca-certificates`

All packages valid.

### `openjre`

**Valid** (3): `ca-certificates`, `dumb-init`, `tzdata`

All packages valid.

### `openldap`

**Valid** (1): `ca-certificates`

**Invalid** (2): `ldap`, `ldap:ldap`

### `openldap-backup`

**Valid** (2): `ca-certificates`, `coreutils`

**Invalid** (1): `65532:65532`

### `openldap-lambda`

**Valid** (1): `ca-certificates`

**Invalid** (1): `65532:65532`

### `openproject`

**Valid** (3): `ca-certificates`, `libpq`, `sqlite-libs`

**Invalid** (1): `65532:65532`

### `openscap`

**Valid** (2): `ca-certificates`, `scap-security-guide`

All packages valid.

### `opensearch`

**Valid** (2): `ca-certificates`, `gosu`

All packages valid.

### `opensearch-dashboards`

**Valid** (1): `ca-certificates`

**Invalid** (1): `xzf`

### `openvpn`

**Valid** (2): `ca-certificates`, `openvpn`

**Invalid** (1): `appuser`

### `openvpn-as`

**Valid** (7): `ca-certificates`, `iproute2`, `iptables`, `kmod`, `liblz4-1`, `net-tools`, `python3`

All packages valid.

### `oracledb-xe`

**Valid** (3): `bc`, `ca-certificates`, `netcat-openbsd`

**Invalid** (1): `oracle`

### `organizer`

**Valid** (6): `ca-certificates`, `nginx`, `php-fpm`, `php-mbstring`, `php-pdo_sqlite`, `php-xml`

**Invalid** (4): `65532:65532`, `?`, `organizr`, `placeholder`

### `outline`

**Valid** (3): `ca-certificates`, `nodejs-20`, `postgresql-client`

**Invalid** (2): `outline`, `outline:outline`

### `oxidized`

**Valid** (3): `ca-certificates`, `openssh`, `ruby`

**Invalid** (1): `oxidized`

### `pairdrop-server`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `pgbouncer`

**Valid** (2): `ca-certificates`, `pgbouncer`

**Invalid** (1): `pgbouncer:pgbouncer`

### `pgpool-ii`

**Valid** (1): `ca-certificates`

**Invalid** (2): `pgpool`, `pgpool:pgpool`

### `photoprism`

**Valid** (1): `ca-certificates`

All packages valid.

### `photoprism-frontend`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `photoshow`

**Valid** (6): `ca-certificates`, `php`, `php-curl`, `php-gd`, `php-mbstring`, `php-xml`

**Invalid** (5): `65532:65532`, `app`, `php-cli`, `php-json`, `php-session`

### `php`

**Valid** (5): `php`, `php-curl`, `php-mbstring`, `php-xml`, `php-zip`

All packages valid.

### `php-apache`

**Valid** (8): `apache2`, `php-8.4`, `php-8.4-curl`, `php-8.4-mbstring`, `php-8.4-mysqli`, `php-8.4-pdo_mysql`, `php-8.4-xml`, `php-8.4-zip`

All packages valid.

### `php-fpm`

**Valid** (6): `php`, `php-curl`, `php-fpm`, `php-mbstring`, `php-xml`, `php-zip`

All packages valid.

### `pi-hole`

**Valid** (4): `ca-certificates`, `iproute2`, `iptables`, `procps`

All packages valid.

### `pinecone`

**Valid** (1): `ca-certificates`

**Invalid** (3): `app`, `app:app`, `pinecone-client`

### `piwigo`

**Valid** (8): `php`, `php-curl`, `php-fpm`, `php-mbstring`, `php-mysqli`, `php-pdo_mysql`, `php-xml`, `php-zip`

All packages valid.

### `planka`

**Valid** (2): `ca-certificates`, `nodejs-20`

**Invalid** (2): `planka`, `planka:planka`

### `plex`

**Valid** (5): `ca-certificates`, `expat`, `fontconfig`, `freetype`, `glib`

All packages valid.

### `plex-media-server`

**Valid** (5): `ca-certificates`, `expat`, `fontconfig`, `freetype`, `glib`

All packages valid.

### `pm2`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `postfix`

**Valid** (2): `ca-certificates`, `postfix`

All packages valid.

### `postfix-constrained`

**Valid** (2): `ca-certificates`, `postfix`

All packages valid.

### `postfix-relay`

**Valid** (2): `ca-certificates`, `postfix`

All packages valid.

### `postgis`

**Valid** (2): `ca-certificates`, `postgis`

All packages valid.

### `postgres`

**Valid** (2): `ca-certificates`, `postgresql-17`

All packages valid.

### `postgres-backup`

**Valid** (1): `ca-certificates`

**Invalid** (1): `postgresql-__VAR__-client`

### `postgres-restore`

**Valid** (1): `ca-certificates`

**Invalid** (1): `postgresql-__VAR__-client`

### `postgresql`

**Valid** (2): `ca-certificates`, `postgresql-17`

All packages valid.

### `postgresql-14`

**Valid** (2): `ca-certificates`, `postgresql-14`

All packages valid.

### `postgresql-15`

**Valid** (2): `ca-certificates`, `postgresql-15`

All packages valid.

### `postgresql-16`

**Valid** (2): `ca-certificates`, `postgresql-16`

All packages valid.

### `postgresql-17`

**Valid** (4): `ca-certificates`, `gnupg`, `liblz4-1`, `libzstd1`

All packages valid.

### `postgresql-anonymizer`

**Valid** (3): `ca-certificates`, `libpq`, `postgresql-client`

All packages valid.

### `postgresql-init`

**Valid** (1): `ca-certificates`

**Invalid** (1): `postgresql-__VAR__-client`

### `postgrey`

**Valid** (2): `ca-certificates`, `postfix`

All packages valid.

### `powerdns`

**Valid** (1): `ca-certificates`

**Invalid** (2): `appuser`, `appuser:appuser`

### `powerdns-api`

**Valid** (8): `boost`, `ca-certificates`, `libgcc`, `libstdc++`, `libxml2`, `lua5.4-libs`, `protobuf`, `sqlite-libs`

**Invalid** (2): `libcurl`, `openssl-libs`

### `powerdns-recursor`

**Valid** (7): `boost`, `ca-certificates`, `libgcc`, `libstdc++`, `lua5.4-libs`, `net-snmp-libs`, `protobuf`

**Invalid** (3): `fstrm-libs`, `libcurl`, `openssl-libs`

### `pptpd`

**Valid** (2): `ca-certificates`, `libstdc++`

All packages valid.

### `prefect`

**Valid** (3): `ca-certificates`, `py3-pip`, `python3`

**Invalid** (5): `add`, `apk`, `app`, `app:app`, `prefect`

### `prefect-server`

**Valid** (3): `ca-certificates`, `py3-pip`, `python3`

**Invalid** (5): `add`, `apk`, `app`, `app:app`, `prefect`

### `privatebin`

**Valid** (6): `php`, `php-curl`, `php-fpm`, `php-mbstring`, `php-xml`, `php-zip`

All packages valid.

### `privatebin-nginx`

**Valid** (8): `ca-certificates`, `nginx`, `php`, `php-curl`, `php-fpm`, `php-gd`, `php-mbstring`, `php-xml`

All packages valid.

### `prowlarr`

**Valid** (6): `ca-certificates`, `icu-libs`, `krb5-libs`, `libgcc`, `libstdc++`, `zlib`

**Invalid** (1): `app`

### `prowlarr-develop`

**Valid** (1): `ca-certificates`

**Invalid** (1): `app`

### `pulsar-functions`

**Valid** (1): `ca-certificates`

**Invalid** (1): `pulsar`

### `pulsar-proxy`

**Valid** (1): `ca-certificates`

**Invalid** (1): `pulsar`

### `pydio`

**Valid** (14): `ca-certificates`, `json-c`, `nginx`, `php`, `php-curl`, `php-fpm`, `php-gd`, `php-intl`, `php-mbstring`, `php-mysqli`, `php-pdo_mysql`, `php-xml`, `sqlite-libs`, `zip`

**Invalid** (1): `65532:65532`

### `python`

**Valid** (1): `ca-certificates`

All packages valid.

### `python-alpine`

**Valid** (1): `python3`

All packages valid.

### `python-slim`

**Valid** (1): `python3`

All packages valid.

### `pytorch`

**Valid** (1): `ca-certificates`

**Invalid** (5): `app`, `app:app`, `torch`, `torchaudio`, `torchvision`

### `qbitmanage`

**Valid** (1): `ca-certificates`

**Invalid** (3): `app`, `app:app`, `qbitmanage==4.2.0`

### `qbittorrent`

**Valid** (1): `ca-certificates`

**Invalid** (2): `qbittorrent`, `qbittorrent:qbittorrent`

### `qbittorrent-nox`

**Valid** (1): `ca-certificates`

**Invalid** (1): `qbittorrent`

### `questdb`

**Valid** (1): `ca-certificates`

**Invalid** (1): `questdb`

### `r2c-bench`

**Valid** (2): `ca-certificates`, `python3`

**Invalid** (3): `65532:65532`, `nogroup`, `r2c`

### `rabbitmq`

**Valid** (1): `ca-certificates`

**Invalid** (2): `rabbitmq`, `rabbitmq:rabbitmq`

### `rabbitmq-amqp`

**Valid** (1): `ca-certificates`

**Invalid** (1): `rabbitmq`

### `rabbitmq-delayed`

**Valid** (1): `ca-certificates`

**Invalid** (1): `rabbitmq`

### `rabbitmq-federation`

**Valid** (1): `ca-certificates`

**Invalid** (1): `rabbitmq`

### `rabbitmq-management`

**Valid** (1): `ca-certificates`

**Invalid** (1): `rabbitmq`

### `rabbitmq-mqtt`

**Valid** (1): `ca-certificates`

**Invalid** (1): `rabbitmq`

### `rabbitmq-stomp`

**Valid** (1): `ca-certificates`

**Invalid** (1): `rabbitmq`

### `radarr`

**Valid** (6): `ca-certificates`, `icu-libs`, `krb5-libs`, `libgcc`, `libstdc++`, `zlib`

**Invalid** (1): `app`

### `radarr-develop`

**Valid** (1): `ca-certificates`

**Invalid** (1): `app`

### `rainloop`

**Valid** (1): `ca-certificates`

**Invalid** (1): `appuser`

### `rblake`

**Valid** (2): `ca-certificates`, `python3`

**Invalid** (3): `65532:65532`, `nogroup`, `rblake`

### `rclone-browser`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `readarr`

**Valid** (1): `ca-certificates`

**Invalid** (1): `app`

### `redash`

**Valid** (2): `ca-certificates`, `libpq`

All packages valid.

### `redis`

**Valid** (1): `ca-certificates`

All packages valid.

### `redis-6`

**Valid** (1): `ca-certificates`

All packages valid.

### `redis-7`

**Valid** (1): `ca-certificates`

All packages valid.

### `redis-cluster`

**Valid** (1): `ca-certificates`

**Invalid** (1): `redis`

### `redis-insight`

**Valid** (4): `ca-certificates`, `fontconfig`, `freetype`, `glib`

**Invalid** (1): `redisinsight`

### `redis-sentinel`

**Valid** (1): `ca-certificates`

**Invalid** (1): `redis`

### `redis-vert`

**Valid** (1): `ca-certificates`

**Invalid** (1): `redis`

### `redis7`

**Valid** (1): `ca-certificates`

**Invalid** (2): `redis`, `redis:redis`

### `redismodules`

**Valid** (2): `ca-certificates`, `valkey`

**Invalid** (9): `+x`, `65532:65532`, `RediSearch,`, `RedisJSON,`, `RedisTimeSeries,`, `bundled:`, `module`, `modules`, `redis`

### `redmine`

**Valid** (3): `ca-certificates`, `libpq`, `sqlite-libs`

**Invalid** (1): `65532:65532`

### `renovate`

**Valid** (1): `ca-certificates`

All packages valid.

### `renovatebot`

**Valid** (1): `ca-certificates`

All packages valid.

### `repo-security`

**Valid** (2): `ca-certificates`, `python3`

**Invalid** (3): `65532:65532`, `nogroup`, `repo-security`

### `repo-supervisor`

**Valid** (2): `ca-certificates`, `python3`

**Invalid** (3): `65532:65532`, `nogroup`, `repo-supervisor`

### `rkhunter`

**Valid** (1): `ca-certificates`

All packages valid.

### `rmilter`

**Valid** (2): `ca-certificates`, `libpcre2-8-0`

**Invalid** (1): `rmilter`

### `rocketmq`

**Valid** (2): `ca-certificates`, `openjdk-17-jre-base`

All packages valid.

### `roundcube`

**Valid** (9): `ca-certificates`, `php`, `php-curl`, `php-dom`, `php-fpm`, `php-iconv`, `php-intl`, `php-mbstring`, `php-xml`

**Invalid** (3): `php-json`, `php-session`, `roundcube`

### `rowy`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `rspamd`

**Valid** (2): `ca-certificates`, `rspamd`

All packages valid.

### `rss2`

**Valid** (8): `ca-certificates`, `php`, `php-curl`, `php-dom`, `php-iconv`, `php-mbstring`, `php-simplexml`, `php-xml`

**Invalid** (4): `65532:65532`, `app`, `php-cli`, `php-json`

### `rss2email`

**Valid** (1): `ca-certificates`

**Invalid** (3): `app`, `app:app`, `rss2email==3.15.1`

### `rsyslog`

**Valid** (2): `ca-certificates`, `rsyslog`

All packages valid.

### `ruby`

**Valid** (2): `ca-certificates`, `ruby`

All packages valid.

### `rust`

**Valid** (2): `ca-certificates`, `rust`

All packages valid.

### `sbt`

**Valid** (1): `ca-certificates`

All packages valid.

### `scap-workbench`

**Valid** (1): `ca-certificates`

All packages valid.

### `scrapyd`

**Valid** (1): `ca-certificates`

**Invalid** (3): `app`, `app:app`, `scrapyd==1.5.0`

### `scratch`

**Valid** (1): `ca-certificates`

All packages valid.

### `scylladb`

**Valid** (4): `ca-certificates`, `libxml2-utils`, `python3`, `systemd`

**Invalid** (1): `scylla`

### `searxng`

**Valid** (2): `ca-certificates`, `py3-lxml`

**Invalid** (2): `searxng`, `searxng:searxng`

### `secrets-scanner`

**Valid** (2): `ca-certificates`, `python3`

**Invalid** (3): `65532:65532`, `nogroup`, `secrets-scanner`

### `secretz`

**Valid** (2): `ca-certificates`, `python3`

**Invalid** (3): `65532:65532`, `nogroup`, `secretz`

### `sentry`

**Valid** (6): `ca-certificates`, `libffi`, `libpq`, `libxml2`, `libxslt`, `openssl`

All packages valid.

### `sentry-cron`

**Valid** (6): `ca-certificates`, `libffi`, `libpq`, `libxml2`, `libxslt`, `openssl`

All packages valid.

### `sentry-worker`

**Valid** (6): `ca-certificates`, `libffi`, `libpq`, `libxml2`, `libxslt`, `openssl`

All packages valid.

### `shh`

**Valid** (2): `ca-certificates`, `python3`

**Invalid** (3): `65532:65532`, `nogroup`, `shh`

### `sigal`

**Valid** (1): `ca-certificates`

**Invalid** (3): `app`, `app:app`, `sigal==2.3.0`

### `singer`

**Valid** (1): `ca-certificates`

**Invalid** (3): `app`, `app:app`, `singer-python`

### `singlestore`

**Valid** (4): `ca-certificates`, `mariadb-client`, `py3-pip`, `python3`

**Invalid** (34): `+x`, `-`, `65532:65532`, `SQL`, `SingleStore-compatible`, `a`, `as`, `base`, `client`, `commercial`, `compatibility`, `development`, `distributed`, `edition`, `for`, `free`, `from`, `image`, `import`, `is`, `libraries`, `pip3`, `production`, `provides`, `pymysql`, `pymysql,`, `pymysql/sqlalchemy`, `singlestore`, `sqlalchemy`, `sqlalchemy,`, `the`, `this`, `v%s`, `your`

### `skrooge`

**Valid** (1): `ca-certificates`

**Invalid** (1): `65532:65532`

### `smartdns`

**Valid** (1): `ca-certificates`

All packages valid.

### `snyk`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `snyk-agent`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `softether`

**Valid** (2): `build-base`, `ca-certificates`

**Invalid** (2): `appuser`, `appuser:appuser`

### `sonarr`

**Valid** (6): `ca-certificates`, `icu-libs`, `krb5-libs`, `libgcc`, `libstdc++`, `zlib`

**Invalid** (1): `app`

### `sonarr-develop`

**Valid** (1): `ca-certificates`

**Invalid** (1): `app`

### `source-control`

**Valid** (3): `ca-certificates`, `tzdata`, `xz`

**Invalid** (1): `+x`

### `spamassassin`

**Valid** (1): `ca-certificates`

All packages valid.

### `splunk-forwarder`

**Valid** (1): `ca-certificates`

**Invalid** (1): `splunk`

### `sql-ledger`

**Valid** (3): `apache2`, `ca-certificates`, `perl`

**Invalid** (1): `65532:65532`

### `sqlcipher`

**Valid** (1): `ca-certificates`

All packages valid.

### `sqlite`

**Valid** (3): `ca-certificates`, `sqlite`, `sqlite-libs`

**Invalid** (1): `sqlite:sqlite`

### `sqlite-browser`

**Valid** (2): `ca-certificates`, `sqlite-libs`

All packages valid.

### `sqlite-utils`

**Valid** (5): `ca-certificates`, `py3-pip`, `python3`, `sqlite`, `tzdata`

**Invalid** (3): `65532:65532`, `apk`, `del`

### `sqlpad`

**Valid** (1): `ca-certificates`

All packages valid.

### `sqlpage`

**Valid** (3): `ca-certificates`, `libgcc`, `tzdata`

All packages valid.

### `sssd`

**Valid** (2): `ca-certificates`, `tzdata`

**Invalid** (1): `root:root`

### `stable-diffusion`

**Valid** (1): `ca-certificates`

**Invalid** (5): `accelerate`, `app`, `app:app`, `diffusers`, `transformers`

### `stable-diffusion-webui`

**Valid** (2): `build-base`, `ca-certificates`

**Invalid** (10): `-`, `app`, `app:app`, `available`, `clone`, `not`, `repo`, `requirements.txt`, `using`, `v1.9.3`

### `stalwart-bitnami`

**Valid** (1): `ca-certificates`

**Invalid** (2): `+x`, `stalwart`

### `standard`

**Valid** (1): `ca-certificates`

All packages valid.

### `stirling-pdf`

**Valid** (1): `ca-certificates`

All packages valid.

### `stirling-pdf-core`

**Valid** (1): `ca-certificates`

All packages valid.

### `strongswan`

**Valid** (7): `ca-certificates`, `gmp`, `iproute2`, `iptables`, `kmod`, `talloc`, `zlib`

**Invalid** (3): `libcrypto1.1`, `libcurl`, `openssl-libs`

### `subsonic`

**Valid** (1): `ca-certificates`

**Invalid** (1): `app`

### `suitecrm`

**Valid** (15): `ca-certificates`, `json-c`, `nginx`, `openssl`, `php`, `php-curl`, `php-fpm`, `php-gd`, `php-intl`, `php-mbstring`, `php-mysqli`, `php-pdo`, `php-pdo_mysql`, `php-xml`, `zip`

**Invalid** (1): `65532:65532`

### `synapse-admin`

**Valid** (2): `ca-certificates`, `nodejs-20`

**Invalid** (3): `add`, `apk`, `appuser`

### `syslog-ng`

**Valid** (1): `ca-certificates`

All packages valid.

### `taiga-front`

**Valid** (2): `ca-certificates`, `nginx`

All packages valid.

### `tasmota-js`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `tensor`

**Valid** (3): `ca-certificates`, `py3-pip`, `python3`

**Invalid** (3): `65532:65532`, `tensorboard`, `tensorboard==__VAR__`

### `tensorboard`

**Valid** (1): `ca-certificates`

**Invalid** (3): `app`, `app:app`, `tensorboard`

### `tensorflow`

**Valid** (1): `ca-certificates`

**Invalid** (3): `app`, `app:app`, `tensorflow`

### `text-gen-ui`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `text-generation-webui`

**Valid** (2): `build-base`, `ca-certificates`

**Invalid** (12): `-`, `available`, `clone`, `not`, `repo`, `requirements.txt`, `torch`, `torchvision`, `user`, `user:user`, `using`, `v__VAR__`

### `tig`

**Valid** (2): `ca-certificates`, `zlib`

All packages valid.

### `tigergraph`

**Valid** (3): `ca-certificates`, `libstdc++`, `python3`

**Invalid** (1): `tigergraph`

### `tigergraph-ecosystem`

**Valid** (3): `ca-certificates`, `libstdc++`, `python3`

**Invalid** (1): `tigergraph`

### `timescaledb`

**Valid** (1): `ca-certificates`

All packages valid.

### `tinytinyrss`

**Valid** (11): `php`, `php-curl`, `php-dom`, `php-fpm`, `php-mbstring`, `php-mysqli`, `php-pdo_mysql`, `php-pdo_sqlite`, `php-pgsql`, `php-xml`, `php-zip`

All packages valid.

### `tooljet`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `tooljet-client`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `tooljet-server`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `transferhelper`

**Valid** (1): `ca-certificates`

**Invalid** (3): `65532:65532`, `nogroup`, `transfer`

### `transformers`

**Valid** (1): `ca-certificates`

**Invalid** (3): `app`, `app:app`, `transformers`

### `transformers-gpu`

**Valid** (1): `ca-certificates`

**Invalid** (4): `app`, `app:app`, `torch`, `transformers`

### `transmission`

**Valid** (1): `ca-certificates`

**Invalid** (2): `transmission`, `transmission:transmission`

### `trino`

**Valid** (3): `ca-certificates`, `python3`, `trino`

All packages valid.

### `tt-rss`

**Valid** (11): `php`, `php-curl`, `php-dom`, `php-fpm`, `php-mbstring`, `php-mysqli`, `php-pdo_mysql`, `php-pdo_sqlite`, `php-pgsql`, `php-xml`, `php-zip`

All packages valid.

### `tts`

**Valid** (1): `ca-certificates`

**Invalid** (3): `TTS`, `app`, `app:app`

### `tvheadend`

**Valid** (1): `ca-certificates`

**Invalid** (2): `hts`, `hts:hts`

### `typesense-js`

**Valid** (2): `ca-certificates`, `nodejs-20`

**Invalid** (2): `node`, `node:node`

### `unbound-alpine`

**Valid** (2): `ca-certificates`, `expat`

All packages valid.

### `unoconv`

**Valid** (1): `ca-certificates`

**Invalid** (1): `65532:65532`

### `upstream`

**Valid** (1): `ca-certificates`

All packages valid.

### `uptime-kuma`

**Valid** (2): `ca-certificates`, `nodejs-20`

**Invalid** (2): `node`, `node:node`

### `valkey`

**Valid** (2): `ca-certificates`, `valkey`

All packages valid.

### `valkey-cluster`

**Valid** (1): `ca-certificates`

All packages valid.

### `vaultwarden-mysql`

**Valid** (1): `ca-certificates`

All packages valid.

### `vaultwarden-postgres`

**Valid** (2): `ca-certificates`, `libpq`

All packages valid.

### `vecs-db`

**Valid** (1): `ca-certificates`

**Invalid** (3): `app`, `app:app`, `vecs`

### `vernemq`

**Valid** (2): `ca-certificates`, `procps`

All packages valid.

### `virtuoso`

**Valid** (1): `ca-certificates`

**Invalid** (2): `65532:65532`, `virtuoso`

### `vllm`

**Valid** (1): `ca-certificates`

**Invalid** (3): `app`, `app:app`, `vllm`

### `vpn-controller`

**Valid** (4): `ca-certificates`, `iproute2`, `iptables`, `kmod`

All packages valid.

### `vtigercrm`

**Valid** (15): `ca-certificates`, `json-c`, `nginx`, `openssl`, `php`, `php-curl`, `php-fpm`, `php-gd`, `php-intl`, `php-mbstring`, `php-mysqli`, `php-pdo`, `php-pdo_mysql`, `php-xml`, `zip`

**Invalid** (1): `65532:65532`

### `wandb-server`

**Valid** (1): `ca-certificates`

**Invalid** (3): `app`, `app:app`, `wandb`

### `weaviate`

**Valid** (1): `ca-certificates`

**Invalid** (1): `+x`

### `weaviate-python`

**Valid** (1): `ca-certificates`

**Invalid** (3): `app`, `app:app`, `weaviate-client`

### `weights-biases`

**Valid** (1): `ca-certificates`

**Invalid** (3): `app`, `app:app`, `wandb`

### `wekan`

**Valid** (1): `ca-certificates`

All packages valid.

### `wg-quick`

**Valid** (5): `ca-certificates`, `iproute2`, `iptables`, `kmod`, `wireguard-tools`

All packages valid.

### `whisparr`

**Valid** (1): `ca-certificates`

**Invalid** (1): `app`

### `whisper`

**Valid** (1): `ca-certificates`

**Invalid** (3): `app`, `app:app`, `openai-whisper`

### `wolfi-gcc`

**Valid** (8): `autoconf`, `automake`, `bison`, `ca-certificates`, `flex`, `libtool`, `openssl-dev`, `zlib-dev`

All packages valid.

### `wolfi-jdk`

**Valid** (1): `ca-certificates`

**Invalid** (4): `add`, `apk`, `java-21-default-jdk`, `openjdk-21-jdk-headless`

### `wolfi-node`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `wolfi-python`

**Valid** (4): `build-base`, `ca-certificates`, `py3-pip`, `python3`

All packages valid.

### `x86_64-unknown-linux-musl`

**Valid** (1): `rust`

All packages valid.

### `yacy`

**Valid** (1): `ca-certificates`

All packages valid.

### `yarn`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `yarn-audit`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `zenphoto`

**Valid** (10): `php`, `php-curl`, `php-fpm`, `php-gd`, `php-mbstring`, `php-mysqli`, `php-pdo_mysql`, `php-pdo_sqlite`, `php-xml`, `php-zip`

All packages valid.

### `zeromq`

**Valid** (2): `ca-certificates`, `libstdc++`

All packages valid.

### `zerotier`

**Valid** (3): `ca-certificates`, `iproute2`, `libstdc++`

All packages valid.

### `zigbee2mqtt`

**Valid** (2): `ca-certificates`, `nodejs-20`

All packages valid.

### `zipkin`

**Valid** (2): `ca-certificates`, `tzdata`

All packages valid.

### `zipline`

**Valid** (3): `ca-certificates`, `nodejs-20`, `python3`

All packages valid.

### `zoe`

**Valid** (1): `ca-certificates`

**Invalid** (4): `65532:65532`, `nogroup`, `zigpy==0.60.0`, `zoe`

### `zzh`

**Valid** (1): `ca-certificates`

**Invalid** (4): `65532:65532`, `nogroup`, `zigpy==0.60.0`, `zzh`

## Full Valid Package List

`apache2`, `autoconf`, `automake`, `bc`, `bind-tools`, `bison`, `boost`, `build-base`, `ca-certificates`, `clamav`, `clamav-daemon`, `clamav-freshclam`, `containers-common`, `coreutils`, `couchdb`, `docker`, `docker-cli`, `dotnet`, `druid`, `dumb-init`, `etcd`, `expat`, `ffmpeg`, `flex`, `fontconfig`, `freetype`, `freshclam`, `glib`, `gmp`, `gnupg`, `go`, `gosu`, `graphite2`, `haproxy`, `harfbuzz`, `icu-libs`, `inotify-tools`, `iproute2`, `iptables`, `jellyfin`, `jenkins`, `json-c`, `kafka`, `kaniko`, `keycloak`, `kmod`, `krb5-libs`, `libcap`, `libffi`, `libffi-dev`, `libgcc`, `libjpeg-turbo`, `liblz4-1`, `libpcre2-8-0`, `libpng`, `libpq`, `libstdc++`, `libtool`, `libwebp`, `libxml2`, `libxml2-dev`, `libxml2-utils`, `libxslt`, `libxslt-dev`, `libzstd1`, `logstash`, `lua5.4-libs`, `mariadb-backup`, `mariadb-client`, `memcached`, `mlflow`, `mosquitto`, `mosquitto-clients`, `mpdecimal`, `mysql`, `ncurses`, `net-snmp-libs`, `net-tools`, `netcat-openbsd`, `nginx`, `nodejs`, `nodejs-20`, `openjdk-17-jre-base`, `openldap`, `openssh`, `openssh-client`, `openssl`, `openssl-dev`, `openvpn`, `perl`, `pgbouncer`, `php`, `php-8.4`, `php-8.4-curl`, `php-8.4-mbstring`, `php-8.4-mysqli`, `php-8.4-pdo_mysql`, `php-8.4-xml`, `php-8.4-zip`, `php-bcmath`, `php-curl`, `php-dom`, `php-exif`, `php-fpm`, `php-gd`, `php-iconv`, `php-intl`, `php-ldap`, `php-mbstring`, `php-mysqli`, `php-pdo`, `php-pdo_mysql`, `php-pdo_sqlite`, `php-pgsql`, `php-simplexml`, `php-soap`, `php-xml`, `php-zip`, `postfix`, `postgis`, `postgresql-14`, `postgresql-15`, `postgresql-16`, `postgresql-17`, `postgresql-client`, `procps`, `protobuf`, `psmisc`, `py3-lxml`, `py3-pip`, `python3`, `readline`, `rspamd`, `rsync`, `rsyslog`, `ruby`, `ruby-dev`, `rust`, `scap-security-guide`, `socat`, `sqlite`, `sqlite-libs`, `systemd`, `talloc`, `trino`, `tzdata`, `unzip`, `valkey`, `wireguard-tools`, `xdg-utils`, `xz`, `yaml`, `zip`, `zlib`, `zlib-dev`
