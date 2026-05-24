# Evergreen Image Registry - Comprehensive Dockerfile Audit Report

**Generated:** 2026-05-19 **Scope:** All Dockerfiles in `images/` (excluding `_wip/`) **Total Images Audited:** 841

---

## 1. Summary Statistics

| Metric                       |   Count |       Pct |
| ---------------------------- | ------: | --------: |
| Total images                 |     841 |    100.0% |
| Multi-stage builds           |     651 |     77.4% |
| With ENTRYPOINT              |     801 |     95.2% |
| With real HEALTHCHECK        |     378 |     44.9% |
| HEALTHCHECK NONE             |     462 |     54.9% |
| Missing HEALTHCHECK entirely |       1 |      0.1% |
| With EXPOSE (app ports)      |     641 |     76.2% |
| With USER directive          |     836 |     99.4% |
| With STOPSIGNAL              |     837 |     99.5% |
| **Placeholder fallback**     | **337** | **40.1%** |
| True no-op placeholders      |       0 |      0.0% |
| Images with any issue        |     546 |     64.9% |
| Clean images (no issues)     |     295 |     35.1% |

---

## 2. Build Type Distribution

| Build Type      | Count |   Pct |
| --------------- | ----: | ----: |
| binary-download |   343 | 40.8% |
| repack          |   262 | 31.2% |
| pkg-install     |   175 | 20.8% |
| source-build    |    55 |  6.5% |
| unknown         |     6 |  0.7% |

---

## 3. Issue Distribution

| Issue                        | Count | Description                                                          |
| ---------------------------- | ----: | -------------------------------------------------------------------- |
| PLACEHOLDER_FALLBACK         |   337 | Creates `sleep infinity` placeholder when real binary download fails |
| NO_EXPOSE                    |   200 | No application EXPOSE ports (metrics port 9101 excluded)             |
| HEALTHCHECK_NONE_NON_SCRATCH |   130 | HEALTHCHECK NONE on non-scratch base image                           |
| NO_ENTRYPOINT                |    40 | No ENTRYPOINT instruction defined                                    |
| WRONG_BASE                   |    21 | glibc binary on musl-based base (wolfi/alpine/scratch)               |
| BLOATED                      |    18 | Final image stage contains build tools (gcc, make, etc.)             |
| MISSING_USER                 |     5 | No USER directive                                                    |
| NO_STOPSIGNAL                |     4 | No STOPSIGNAL directive                                              |
| NO_HEALTHCHECK               |     1 | No HEALTHCHECK instruction at all (not even NONE)                    |

---

## 4. Placeholder Fallback Images (CRITICAL)

**337 images** have a fallback that creates a dummy script with `sleep infinity` when the real binary download fails.
The build succeeds but the container does nothing useful.

These images will silently succeed at build time and sleep forever at runtime if the upstream release URL is wrong, the
version doesn't exist, or the download fails.

| #   | Image                             | Version                      | Build Type      |
| --- | --------------------------------- | ---------------------------- | --------------- |
| 1   | activemq                          | 5.18.3                       | binary-download |
| 2   | adguard-dns                       | 0.107.50                     | binary-download |
| 3   | adguardhome                       | 0.107.74                     | binary-download |
| 4   | adguardhome-lite                  | 0.107.50                     | binary-download |
| 5   | age                               | 1.3.1                        | binary-download |
| 6   | alertmanager                      | 0.27.0                       | binary-download |
| 7   | arango                            | 3.12.2                       | binary-download |
| 8   | arangodb                          | 3.12.4                       | binary-download |
| 9   | argo-cd                           | 3.4.2                        | binary-download |
| 10  | argo-rollouts                     | 1.9.0                        | binary-download |
| 11  | argocd-redis                      | 7.2.4                        | binary-download |
| 12  | auditbeat                         | 9.4.0                        | binary-download |
| 13  | authelia                          | 4.39.19                      | binary-download |
| 14  | authelia-lite                     | 4.39.19                      | binary-download |
| 15  | awslogs                           | 0.15.0                       | repack          |
| 16  | azurelogs                         | 1.2.0                        | repack          |
| 17  | badger                            | 4.2.0                        | source-build    |
| 18  | basic-auth-proxy                  | ?                            | source-build    |
| 19  | beancount                         | 2.3.6                        | repack          |
| 20  | betteruptime                      | 0.2.0                        | source-build    |
| 21  | bind                              | 9.21.21                      | binary-download |
| 22  | bind-exporter                     | 0.7.0                        | binary-download |
| 23  | blackbox-exporter                 | v0.26.0                      | binary-download |
| 24  | blocky                            | 0.29.0                       | binary-download |
| 25  | buildx                            | 0.33.0                       | binary-download |
| 26  | caddy                             | 2.11.3                       | binary-download |
| 27  | caddy-alpine                      | 2.8.4                        | binary-download |
| 28  | caddy-fileserver                  | 2.7.6                        | binary-download |
| 29  | caddy-reverseproxy                | 2.7.6                        | binary-download |
| 30  | caddy-wildcard                    | 2.7.6                        | binary-download |
| 31  | cadvisor                          | 0.49.1                       | repack          |
| 32  | cargo-audit                       | ?                            | source-build    |
| 33  | cassandra-operator                | 1.20.0                       | repack          |
| 34  | cayley                            | 0.7.7                        | source-build    |
| 35  | certificates                      | 1.6.5                        | binary-download |
| 36  | chartdb                           | v1.20.1                      | repack          |
| 37  | checkov                           | ?                            | repack          |
| 38  | checkov-k8s                       | ?                            | repack          |
| 39  | cloudflare-ddns                   | 1.16.2                       | binary-download |
| 40  | cloudflare-warrior                | 2026.5.0                     | binary-download |
| 41  | cloudflared                       | 2026.3.0                     | binary-download |
| 42  | cloudreve                         | 3.8.3                        | binary-download |
| 43  | cockroachdb                       | 24.3.0                       | binary-download |
| 44  | cockroachdb-exporter              | 23.2.3                       | binary-download |
| 45  | cockroachdb-sql                   | 23.2.3                       | binary-download |
| 46  | composer                          | 2.8.0                        | binary-download |
| 47  | conan-audit                       | ?                            | repack          |
| 48  | conduit                           | 0.4.0                        | repack          |
| 49  | conduit-admin                     | 0.4.0                        | repack          |
| 50  | consul                            | 1.18.1                       | binary-download |
| 51  | consul-exporter                   | 0.4.0                        | binary-download |
| 52  | consul-template                   | 0.37.0                       | binary-download |
| 53  | coredns                           | 1.12.0                       | binary-download |
| 54  | coredns-alpine                    | 1.11.1                       | binary-download |
| 55  | cors-proxy                        | ?                            | source-build    |
| 56  | cortex                            | 1.17.0                       | binary-download |
| 57  | cosign                            | 3.0.6                        | binary-download |
| 58  | cosign-verify                     | 3.0.6                        | binary-download |
| 59  | couchbase                         | ?                            | repack          |
| 60  | couchbase-operator                | 2.8.0                        | repack          |
| 61  | couchdb                           | 3.5.1                        | repack          |
| 62  | crane                             | 0.21.5                       | binary-download |
| 63  | crate                             | 5.9.0                        | binary-download |
| 64  | crawlergo                         | 0.4.4                        | binary-download |
| 65  | crdb-init                         | 23.2.3                       | binary-download |
| 66  | ct-log                            | 1.3.3                        | source-build    |
| 67  | dashy                             | 3.3.0                        | binary-download |
| 68  | dnsmasq                           | 2.90                         | binary-download |
| 69  | docui                             | ?                            | binary-download |
| 70  | dragonfly                         | 1.18.0                       | binary-download |
| 71  | dragonfly-client                  | 1.18.0                       | binary-download |
| 72  | duplicati                         | 2.1.0.1                      | binary-download |
| 73  | elasticsearch-8                   | 8.12.2                       | repack          |
| 74  | elasticsearch-exporter            | 1.7.0                        | repack          |
| 75  | erpnext-worker                    | 15                           | repack          |
| 76  | esphome                           | ?                            | repack          |
| 77  | esphome-daemon                    | ?                            | repack          |
| 78  | etcd                              | 3.6.10                       | binary-download |
| 79  | etcd-backup                       | 3.6.10                       | binary-download |
| 80  | etcd-empty                        | 3.6.10                       | binary-download |
| 81  | etcd-operator                     | 3.6.10                       | binary-download |
| 82  | falcosidekick                     | ?                            | binary-download |
| 83  | filebeat                          | 9.4.0                        | binary-download |
| 84  | filebrowser                       | v2.32.0                      | binary-download |
| 85  | filebrowser-alpine                | v2.32.0                      | binary-download |
| 86  | firefly-iii-importer              | 1.6.0                        | repack          |
| 87  | flux                              | 2.3.0                        | binary-download |
| 88  | flux2                             | 2.8.6                        | binary-download |
| 89  | fluxcd-helm                       | 2.8.6                        | binary-download |
| 90  | fluxcd-image                      | 2.8.6                        | binary-download |
| 91  | focalboard-server                 | 7.11.3                       | binary-download |
| 92  | forgejo                           | 12.0.3                       | repack          |
| 93  | fulcio                            | 1.8.5                        | binary-download |
| 94  | gcplogs                           | 3.10.0                       | repack          |
| 95  | ggshield                          | ?                            | repack          |
| 96  | gitguardian                       | ?                            | repack          |
| 97  | gitleaks                          | ?                            | binary-download |
| 98  | go-static                         | 1.22.10                      | binary-download |
| 99  | gogs                              | 0.13.0                       | binary-download |
| 100 | golang-alpine                     | 1.22.10                      | binary-download |
| 101 | golang-cache                      | 1.0.0                        | source-build    |
| 102 | gradle                            | 8.10.2                       | binary-download |
| 103 | grafana                           | 12.2.0                       | binary-download |
| 104 | grafana-dev                       | 10.4.1                       | binary-download |
| 105 | grafana-image-renderer            | 5.8.2                        | binary-download |
| 106 | grafana-lite                      | 10.4.1                       | binary-download |
| 107 | grafana-oss                       | 10.4.1                       | binary-download |
| 108 | grafana-toolkit                   | 10.4.1                       | binary-download |
| 109 | graphile                          | 4.14.0                       | pkg-install     |
| 110 | graylog-sidecar                   | 1.5.2                        | binary-download |
| 111 | grype                             | 0.80.0                       | binary-download |
| 112 | grype-alpine                      | ?                            | binary-download |
| 113 | hadolint                          | 2.14.0                       | binary-download |
| 114 | haproxy-exporter                  | 0.15.0                       | binary-download |
| 115 | hashicorp-vault                   | 1.18.1                       | binary-download |
| 116 | headscale                         | 0.16.0                       | binary-download |
| 117 | health-checks                     | 1.0.0                        | source-build    |
| 118 | healthcheck                       | 0.4.36                       | binary-download |
| 119 | heartbeat                         | 9.4.0                        | binary-download |
| 120 | helm                              | 3.15.1                       | binary-download |
| 121 | helmfile                          | 0.162.0                      | binary-download |
| 122 | helmsman                          | 4.0.5                        | binary-download |
| 123 | homebridge                        | ?                            | repack          |
| 124 | homebridge-camera                 | ?                            | repack          |
| 125 | ignite                            | 2.16.0                       | binary-download |
| 126 | immudb                            | 1.11.0                       | binary-download |
| 127 | influxdb-client                   | 2.7.5                        | binary-download |
| 128 | ipmi-exporter                     | 1.10.1                       | binary-download |
| 129 | it-tools                          | 2024.10.22-7ca5933           | binary-download |
| 130 | jaeger                            | 1.62.0                       | binary-download |
| 131 | jaeger-agent                      | 1.55.0                       | binary-download |
| 132 | jaeger-collector                  | 1.55.0                       | binary-download |
| 133 | jaeger-query                      | 1.55.0                       | binary-download |
| 134 | jenkins-agent                     | 3355.v388858a_47b_33         | binary-download |
| 135 | jenkins-executor                  | 3355.v388858a_47b_33         | binary-download |
| 136 | jenkins-plugin                    | 2.462.1                      | binary-download |
| 137 | journalbeat                       | 9.4.0                        | binary-download |
| 138 | k3d                               | 5.8.3                        | binary-download |
| 139 | k3d-proxy                         | 5.8.3                        | binary-download |
| 140 | k3s                               | 1.33.6+k3s1                  | binary-download |
| 141 | k3s-agent                         | 1.33.6+k3s1                  | binary-download |
| 142 | k3s-server                        | 1.33.6+k3s1                  | binary-download |
| 143 | kafka-exporter                    | 1.9.0                        | binary-download |
| 144 | kafka-ui                          | 0.7.2                        | binary-download |
| 145 | keycloak                          | 26.6.1                       | pkg-install     |
| 146 | keycloak-gatekeeper               | 9.1.1                        | binary-download |
| 147 | keycloak-init                     | 26.6.1                       | binary-download |
| 148 | keycloak-quarkus                  | 26.6.1                       | binary-download |
| 149 | kibana                            | 8.12.2                       | binary-download |
| 150 | kibana-oss                        | 8.12.2                       | binary-download |
| 151 | kube-apiserver                    | 1.30.1                       | binary-download |
| 152 | kube-bench                        | ?                            | binary-download |
| 153 | kube-controller                   | 1.30.1                       | binary-download |
| 154 | kube-hunter                       | ?                            | repack          |
| 155 | kube-proxy                        | 1.30.1                       | binary-download |
| 156 | kube-scheduler                    | 1.30.1                       | binary-download |
| 157 | kube-state-metrics                | 2.18.0                       | binary-download |
| 158 | kubectl                           | 1.30.1                       | binary-download |
| 159 | kubescape                         | ?                            | binary-download |
| 160 | kustomize                         | 5.4.1                        | binary-download |
| 161 | lazydocker                        | ?                            | binary-download |
| 162 | lazydocker-ui                     | ?                            | binary-download |
| 163 | linguist-go                       | 9.5.0                        | source-build    |
| 164 | llama-cpp-server                  | b5415                        | binary-download |
| 165 | llama.cpp                         | ${VERSION}                   | binary-download |
| 166 | localai                           | 4.1.3                        | binary-download |
| 167 | loki                              | 3.1.0                        | binary-download |
| 168 | loki-canary                       | 2.9.4                        | binary-download |
| 169 | loki-simple                       | 3.1.0                        | binary-download |
| 170 | mattermost                        | 11.6.2                       | binary-download |
| 171 | maven                             | 3.9.15                       | binary-download |
| 172 | mc                                | RELEASE.2025-04-08T16-46-15Z | binary-download |
| 173 | meilisearch                       | 1.42.1                       | binary-download |
| 174 | memcached-exporter                | 0.13.0                       | binary-download |
| 175 | meshbird                          | 2.3                          | source-build    |
| 176 | metricbeat                        | 9.4.0                        | binary-download |
| 177 | mimir                             | 2.10.0                       | binary-download |
| 178 | miniflux-21                       | 2.2.19                       | binary-download |
| 179 | minio                             | RELEASE.2025-10-15T17-29-55Z | binary-download |
| 180 | minio-operator                    | v6.0.4                       | binary-download |
| 181 | mongo-exporter                    | 0.40.0                       | repack          |
| 182 | mongodb-7                         | 7.0.9                        | binary-download |
| 183 | mongodb-community                 | 7.0.9                        | binary-download |
| 184 | mongodb-exporter                  | 0.13.0                       | repack          |
| 185 | mysql-8-exporter                  | 0.19.0                       | repack          |
| 186 | mysql-anonymizer                  | 0.10.0                       | repack          |
| 187 | mysql-exporter                    | 0.15.0                       | binary-download |
| 188 | mysqld-exporter                   | v0.16.0                      | binary-download |
| 189 | nats                              | 2.12.7                       | binary-download |
| 190 | navidrome                         | 0.52.5                       | binary-download |
| 191 | navidrome-sqlite                  | 0.52.5                       | binary-download |
| 192 | netbird                           | 0.70.5                       | binary-download |
| 193 | netmaker                          | 1.5.1                        | binary-download |
| 194 | nginx                             | 1.27.1                       | binary-download |
| 195 | nginx-exporter                    | 1.1.0                        | binary-download |
| 196 | nginx-ingress                     | 1.27.1                       | binary-download |
| 197 | nginx-ingress-controller          | 1.10.1                       | source-build    |
| 198 | nginx-stream                      | 1.27.1                       | binary-download |
| 199 | nginx-unprivileged                | 1.27.1                       | binary-download |
| 200 | node-alpine                       | 22.12.0                      | binary-download |
| 201 | node-distroless                   | 22.12.0                      | binary-download |
| 202 | node-exporter                     | 1.8.0                        | binary-download |
| 203 | oauth2-proxy                      | 7.12.0                       | binary-download |
| 204 | ollama                            | 0.21.0                       | binary-download |
| 205 | opensearch                        | 2.12.0                       | binary-download |
| 206 | openvpn-as                        | 2.12.1                       | binary-download |
| 207 | packetbeat                        | 9.4.0                        | binary-download |
| 208 | pairdrop                          | 1.11.2                       | binary-download |
| 209 | paperless-ngx                     | 2.20.14                      | repack          |
| 210 | perscache                         | 1.0.0                        | source-build    |
| 211 | pgbouncer-exporter                | 0.12.0                       | repack          |
| 212 | photoprism-bin                    | 260305-fad9d5395             | repack          |
| 213 | pi-hole                           | ?                            | binary-download |
| 214 | pihole-ftl                        | 5.18.2                       | binary-download |
| 215 | pinned-search                     | 0.1.0                        | source-build    |
| 216 | piper                             | 1.2.0                        | binary-download |
| 217 | portainer                         | 2.20.1                       | binary-download |
| 218 | postgres-exporter                 | 0.17.0                       | binary-download |
| 219 | postgresql-17                     | 17.2                         | repack          |
| 220 | postgresql-anonymizer             | 1.2.0                        | repack          |
| 221 | postgresql-exporter               | 0.15.0                       | binary-download |
| 222 | prometheus                        | 2.53.0                       | binary-download |
| 223 | prometheus-alertmanager           | 0.27.0                       | binary-download |
| 224 | prometheus-aws-exporter           | 0.65.0                       | binary-download |
| 225 | prometheus-blackbox-exporter      | 0.28.0                       | binary-download |
| 226 | prometheus-consul-exporter        | 0.13.0                       | binary-download |
| 227 | prometheus-elasticsearch-exporter | 1.10.0                       | binary-download |
| 228 | prometheus-haproxy-exporter       | 0.15.0                       | binary-download |
| 229 | prometheus-kafka-exporter         | 1.9.0                        | binary-download |
| 230 | prometheus-mysqld-exporter        | 0.19.0                       | binary-download |
| 231 | prometheus-nginx-exporter         | 1.1.0                        | binary-download |
| 232 | prometheus-node-exporter          | 1.8.0                        | binary-download |
| 233 | prometheus-postgres-exporter      | 0.19.1                       | binary-download |
| 234 | prometheus-pushgateway            | 1.8.0                        | binary-download |
| 235 | prometheus-snmp-exporter          | 0.30.1                       | binary-download |
| 236 | prometheus-statsd-exporter        | 0.29.0                       | binary-download |
| 237 | prometheus-x509-exporter          | 3.9.0                        | binary-download |
| 238 | promtail                          | 3.5.12                       | binary-download |
| 239 | promtail-agent                    | ${VERSION}                   | binary-download |
| 240 | prowlarr-develop                  | 2.3.6.5351                   | binary-download |
| 241 | qdrant                            | 1.17.1                       | binary-download |
| 242 | qdrant-cpu                        | 1.17.1                       | binary-download |
| 243 | questdb                           | 7.3.10                       | repack          |
| 244 | rabbitmq-exporter                 | 1.1.0                        | repack          |
| 245 | rabbitmq-management               | 3.13.1                       | binary-download |
| 246 | radarr-develop                    | 6.2.0.10390                  | binary-download |
| 247 | rclone                            | v1.69.1                      | binary-download |
| 248 | readarr                           | 0.4.18.2805                  | binary-download |
| 249 | redash                            | 10.0.0                       | repack          |
| 250 | redis-exporter                    | 1.68.0                       | binary-download |
| 251 | redismodules                      | 2.0.0                        | pkg-install     |
| 252 | rekor                             | 1.5.1                        | binary-download |
| 253 | restic                            | 0.17.3                       | binary-download |
| 254 | rmilter                           | 1.0.0                        | source-build    |
| 255 | rocketmq                          | 5.1.4                        | binary-download |
| 256 | rsyslog                           | 8.2312.0                     | repack          |
| 257 | s3                                | RELEASE.2025-10-15T17-29-55Z | binary-download |
| 258 | searx                             | ?                            | repack          |
| 259 | searxng-meta                      | ?                            | repack          |
| 260 | shield                            | 8.6.0                        | binary-download |
| 261 | snmp-exporter                     | 0.26.0                       | binary-download |
| 262 | snyk                              | 1.1300.0                     | binary-download |
| 263 | snyk-agent                        | 1.1300.0                     | binary-download |
| 264 | snyk-alpine                       | ?                            | binary-download |
| 265 | snyk-docker                       | ?                            | binary-download |
| 266 | snyk-monitor                      | ?                            | binary-download |
| 267 | sonarr-develop                    | 4.0.17.2953                  | binary-download |
| 268 | splunk-forwarder                  | 9.2.1                        | binary-download |
| 269 | statping-ng                       | 0.90.74                      | binary-download |
| 270 | step-acme                         | 0.30.2                       | binary-download |
| 271 | step-ca                           | 0.30.2                       | binary-download |
| 272 | step-certificates                 | 0.30.2                       | binary-download |
| 273 | step-cli                          | 0.30.2                       | binary-download |
| 274 | stirling-pdf                      | 2.10.0                       | binary-download |
| 275 | stirling-pdf-core                 | 2.10.0                       | binary-download |
| 276 | surrealdb                         | 3.0.5                        | binary-download |
| 277 | syft                              | 1.8.0                        | binary-download |
| 278 | syft-alpine                       | ?                            | binary-download |
| 279 | synapse                           | 1.152.1                      | repack          |
| 280 | syslog-ng                         | 4.8.1                        | repack          |
| 281 | taiga                             | 6.9.0                        | repack          |
| 282 | taiga-backend                     | 6.9.0                        | repack          |
| 283 | tailscale                         | 1.58.0                       | binary-download |
| 284 | tekton                            | 0.60.0                       | binary-download |
| 285 | tempo                             | 2.8.0                        | binary-download |
| 286 | thanos                            | 0.35.0                       | binary-download |
| 287 | thanos-bucket                     | ${VERSION}                   | binary-download |
| 288 | thanos-querier                    | ${VERSION}                   | binary-download |
| 289 | thanos-receive                    | 0.35.0                       | binary-download |
| 290 | thanos-rule                       | ${VERSION}                   | binary-download |
| 291 | thanos-store                      | 0.35.0                       | binary-download |
| 292 | traefik                           | 3.5.3                        | binary-download |
| 293 | traefik-cloud                     | 3.6.13                       | binary-download |
| 294 | traefik-crypto                    | 3.6.13                       | binary-download |
| 295 | traefik-dashboard                 | 3.6.13                       | binary-download |
| 296 | traefik-hub                       | 3.6.13                       | binary-download |
| 297 | traefik-metrics                   | 3.6.13                       | binary-download |
| 298 | traefik-mirror                    | 3.6.13                       | binary-download |
| 299 | traefik-plugin-auth               | 3.6.13                       | binary-download |
| 300 | traefik-plugin-csrf               | 3.6.13                       | binary-download |
| 301 | traefik-v2                        | 2.11.42                      | binary-download |
| 302 | traefik-wss                       | 3.6.13                       | binary-download |
| 303 | transfer.sh                       | ?                            | binary-download |
| 304 | trino                             | 435                          | repack          |
| 305 | trivy                             | 0.70.0                       | binary-download |
| 306 | trivy-alpine                      | ?                            | binary-download |
| 307 | trivy-iac                         | ?                            | binary-download |
| 308 | trivy-k8s                         | ?                            | binary-download |
| 309 | trivy-operator                    | 0.30.1                       | binary-download |
| 310 | truffelsh                         | ?                            | binary-download |
| 311 | trufflehog                        | ?                            | binary-download |
| 312 | truffleshog                       | ?                            | binary-download |
| 313 | ulogger                           | latest                       | source-build    |
| 314 | unbound                           | 1.20.0                       | source-build    |
| 315 | unbound-alpine                    | 1.19.3                       | source-build    |
| 316 | unbound-exporter                  | 0.6.0                        | binary-download |
| 317 | valkey-exporter                   | 1.58.0                       | binary-download |
| 318 | vault                             | 1.18.1                       | binary-download |
| 319 | vector                            | 0.39.0                       | binary-download |
| 320 | victoria-logs                     | v1.50.0                      | binary-download |
| 321 | victoriametrics                   | 1.142.0                      | binary-download |
| 322 | victoriametrics-cluster           | 1.97.0                       | binary-download |
| 323 | vikunja                           | 2.3.0                        | repack          |
| 324 | vikunja-api                       | 2.3.0                        | binary-download |
| 325 | vikunja-redis                     | 2.3.0                        | binary-download |
| 326 | vm-agent                          | 1.140.0                      | binary-download |
| 327 | vmalert                           | 1.142.0                      | binary-download |
| 328 | watchtower                        | 1.7.1                        | binary-download |
| 329 | whisparr                          | 2.2.0-develop.115            | binary-download |
| 330 | whoogle                           | 1.2.4                        | repack          |
| 331 | whoogle-search                    | ?                            | repack          |
| 332 | wireguard                         | 1.0.20250521                 | source-build    |
| 333 | wireguard-ui                      | 0.5.4                        | binary-download |
| 334 | yarr                              | 2.4.0                        | repack          |
| 335 | zfs-exporter                      | 0.0.12                       | binary-download |
| 336 | zipline                           | ?                            | source-build    |
| 337 | zitadel                           | 4.13.1                       | binary-download |

---

## 5. HEALTHCHECK Analysis

| Type     | Count |   Pct |
| -------- | ----: | ----: |
| none     |   462 | 54.9% |
| http/tcp |   348 | 41.4% |
| native   |    25 |  3.0% |
| generic  |     5 |  0.6% |
| missing  |     1 |  0.1% |

### HEALTHCHECK NONE on non-scratch images (130)

These images use `HEALTHCHECK NONE` but have a non-scratch base that could support health checks:

| Image                      | Base Image                                  |
| -------------------------- | ------------------------------------------- |
| 389ds                      | cgr.dev/chainguard/wolfi-base               |
| activemq                   | cgr.dev/chainguard/wolfi-base               |
| adempiere                  | cgr.dev/chainguard/wolfi-base               |
| akaunting                  | cgr.dev/chainguard/wolfi-base               |
| alpine-static              | cgr.dev/chainguard/static                   |
| apache-ofbiz               | cgr.dev/chainguard/wolfi-base               |
| awslogs                    | registry.access.redhat.com/ubi9/ubi-minimal |
| azurelogs                  | registry.access.redhat.com/ubi9/ubi-minimal |
| basic-auth-proxy           | cgr.dev/chainguard/wolfi-base               |
| beancount                  | registry.access.redhat.com/ubi9/ubi-minimal |
| busybox                    | cgr.dev/chainguard/wolfi-base               |
| caddy-alpine               | cgr.dev/chainguard/wolfi-base               |
| collabora                  | cgr.dev/chainguard/wolfi-base               |
| collabora-online           | cgr.dev/chainguard/wolfi-base               |
| collabora-online-code      | cgr.dev/chainguard/wolfi-base               |
| cors-proxy                 | cgr.dev/chainguard/wolfi-base               |
| couchbase                  | cgr.dev/chainguard/wolfi-base               |
| couchdb                    | cgr.dev/chainguard/wolfi-base               |
| cryptpad                   | cgr.dev/chainguard/wolfi-base               |
| distroless                 | gcr.io/distroless/static-debian12           |
| dnsdist                    | cgr.dev/chainguard/wolfi-base               |
| docker-socket-proxy        | cgr.dev/chainguard/wolfi-base               |
| dolibarr                   | cgr.dev/chainguard/wolfi-base               |
| duplicati                  | cgr.dev/chainguard/wolfi-base               |
| egroupware                 | cgr.dev/chainguard/wolfi-base               |
| emby                       | cgr.dev/chainguard/wolfi-base               |
| espocrm                    | cgr.dev/chainguard/wolfi-base               |
| firefly-iii-importer       | registry.access.redhat.com/ubi9/ubi-minimal |
| focalboard-server          | cgr.dev/chainguard/wolfi-base               |
| forgejo                    | cgr.dev/chainguard/wolfi-base               |
| freeipa-client             | cgr.dev/chainguard/wolfi-base               |
| frontaccounting            | cgr.dev/chainguard/wolfi-base               |
| gcplogs                    | registry.access.redhat.com/ubi9/ubi-minimal |
| gnucash                    | cgr.dev/chainguard/wolfi-base               |
| grafana-image-renderer     | cgr.dev/chainguard/wolfi-base               |
| graylog                    | cgr.dev/chainguard/wolfi-base               |
| grisbi                     | cgr.dev/chainguard/wolfi-base               |
| headscale-ui               | gcr.io/distroless/static-debian12           |
| idempiere                  | cgr.dev/chainguard/wolfi-base               |
| invoice-ninja              | cgr.dev/chainguard/wolfi-base               |
| invoice-ninja-api          | cgr.dev/chainguard/wolfi-base               |
| jellyfin                   | cgr.dev/chainguard/wolfi-base               |
| jellyfin-server            | cgr.dev/chainguard/wolfi-base               |
| kafka-connect              | cgr.dev/chainguard/wolfi-base               |
| keycloak                   | cgr.dev/chainguard/wolfi-base               |
| keycloak-init              | cgr.dev/chainguard/wolfi-base               |
| keycloak-quarkus           | cgr.dev/chainguard/wolfi-base               |
| kibana                     | cgr.dev/chainguard/wolfi-base               |
| kibana-oss                 | cgr.dev/chainguard/wolfi-base               |
| kmymoney                   | cgr.dev/chainguard/wolfi-base               |
| libreoffice                | cgr.dev/chainguard/wolfi-base               |
| libreoffice-headless       | cgr.dev/chainguard/wolfi-base               |
| lidarr                     | cgr.dev/chainguard/wolfi-base               |
| logstash                   | cgr.dev/chainguard/wolfi-base               |
| logstash-oss               | cgr.dev/chainguard/wolfi-base               |
| matrix-hookshot            | cgr.dev/chainguard/wolfi-base               |
| maxbot                     | cgr.dev/chainguard/wolfi-base               |
| milvus-minio               | cgr.dev/chainguard/wolfi-base               |
| musl                       | cgr.dev/chainguard/static                   |
| netmaker-ui                | gcr.io/distroless/static-debian12           |
| nextcloud                  | cgr.dev/chainguard/wolfi-base               |
| nextcloud-alpine           | cgr.dev/chainguard/wolfi-base               |
| nextcloud-external         | cgr.dev/chainguard/wolfi-base               |
| nextcloud-imaging          | cgr.dev/chainguard/wolfi-base               |
| nextcloud-nginx            | cgr.dev/chainguard/wolfi-base               |
| node-distroless            | gcr.io/distroless/nodejs22-debian12         |
| ocserv                     | cgr.dev/chainguard/wolfi-base               |
| onlyoffice-communityserver | cgr.dev/chainguard/wolfi-base               |
| onlyoffice-controlpanel    | cgr.dev/chainguard/wolfi-base               |
| openhab                    | cgr.dev/chainguard/wolfi-base               |
| openldap-backup            | cgr.dev/chainguard/wolfi-base               |
| openldap-lambda            | cgr.dev/chainguard/wolfi-base               |
| openproject                | cgr.dev/chainguard/wolfi-base               |
| opensearch                 | cgr.dev/chainguard/wolfi-base               |
| openvpn-as                 | cgr.dev/chainguard/wolfi-base               |
| photoshow                  | cgr.dev/chainguard/wolfi-base               |
| pi-hole                    | cgr.dev/chainguard/wolfi-base               |
| plex                       | cgr.dev/chainguard/wolfi-base               |
| postgres                   | cgr.dev/chainguard/wolfi-base               |
| pptpd                      | cgr.dev/chainguard/wolfi-base               |
| prowlarr                   | cgr.dev/chainguard/wolfi-base               |
| pulsar-functions           | cgr.dev/chainguard/wolfi-base               |
| pulsar-proxy               | cgr.dev/chainguard/wolfi-base               |
| pydio                      | cgr.dev/chainguard/wolfi-base               |
| radarr                     | cgr.dev/chainguard/wolfi-base               |
| rclone-browser             | cgr.dev/chainguard/wolfi-base               |
| redis-vert                 | cgr.dev/chainguard/wolfi-base               |
| redis7                     | cgr.dev/chainguard/wolfi-base               |
| redmine                    | cgr.dev/chainguard/wolfi-base               |
| renovate                   | cgr.dev/chainguard/wolfi-base               |
| renovatebot                | cgr.dev/chainguard/wolfi-base               |
| rocketmq                   | cgr.dev/chainguard/wolfi-base               |
| rss2                       | cgr.dev/chainguard/wolfi-base               |
| rsyslog                    | cgr.dev/chainguard/wolfi-base               |
| sentry                     | cgr.dev/chainguard/wolfi-base               |
| sentry-cron                | cgr.dev/chainguard/wolfi-base               |
| sentry-worker              | cgr.dev/chainguard/wolfi-base               |
| skrooge                    | cgr.dev/chainguard/wolfi-base               |
| smartdns                   | cgr.dev/chainguard/wolfi-base               |
| snyk                       | cgr.dev/chainguard/wolfi-base               |
| snyk-agent                 | cgr.dev/chainguard/wolfi-base               |
| sonarr                     | cgr.dev/chainguard/wolfi-base               |
| splunk-forwarder           | cgr.dev/chainguard/wolfi-base               |
| sql-ledger                 | cgr.dev/chainguard/wolfi-base               |
| sqlcipher                  | cgr.dev/chainguard/wolfi-base               |
| sqlite-browser             | cgr.dev/chainguard/wolfi-base               |
| sqlite-utils               | cgr.dev/chainguard/wolfi-base               |
| stirling-pdf               | cgr.dev/chainguard/wolfi-base               |
| stirling-pdf-core          | cgr.dev/chainguard/wolfi-base               |
| suitecrm                   | cgr.dev/chainguard/wolfi-base               |
| synapse                    | registry.access.redhat.com/ubi9/ubi-minimal |
| syslog-ng                  | cgr.dev/chainguard/wolfi-base               |
| taiga                      | registry.access.redhat.com/ubi9/ubi-minimal |
| taiga-backend              | registry.access.redhat.com/ubi9/ubi-minimal |
| taiga-front                | cgr.dev/chainguard/wolfi-base               |
| taiga-protected            | registry.access.redhat.com/ubi9/ubi-minimal |
| tautulli                   | registry.access.redhat.com/ubi9/ubi-minimal |
| tautulli-py                | registry.access.redhat.com/ubi9/ubi-minimal |
| tig                        | cgr.dev/chainguard/wolfi-base               |
| unbound-alpine             | cgr.dev/chainguard/wolfi-base               |
| unoconv                    | cgr.dev/chainguard/wolfi-base               |
| vaultwarden-mysql          | cgr.dev/chainguard/wolfi-base               |
| vaultwarden-postgres       | cgr.dev/chainguard/wolfi-base               |
| vpn-controller             | cgr.dev/chainguard/wolfi-base               |
| vtigercrm                  | cgr.dev/chainguard/wolfi-base               |
| wg-quick                   | cgr.dev/chainguard/wolfi-base               |
| wolfi-gcc                  | cgr.dev/chainguard/wolfi-base               |
| wolfi-jdk                  | cgr.dev/chainguard/wolfi-base               |
| wolfi-node                 | cgr.dev/chainguard/wolfi-base               |
| wolfi-python               | cgr.dev/chainguard/wolfi-base               |

---

## 6. Base Image Distribution

| Base Image                                  | Count |   Pct |
| ------------------------------------------- | ----: | ----: |
| cgr.dev/chainguard/wolfi-base               |   455 | 54.1% |
| scratch                                     |   333 | 39.6% |
| registry.access.redhat.com/ubi9/ubi-minimal |    34 |  4.0% |
| debian                                      |    13 |  1.5% |
| gcr.io/distroless/static-debian12           |     3 |  0.4% |
| cgr.dev/chainguard/static                   |     2 |  0.2% |
| gcr.io/distroless/nodejs22-debian12         |     1 |  0.1% |

### Potential WRONG_BASE images (21)

glibc indicators found on musl-based base images:

| Image             | Final Base                    |
| ----------------- | ----------------------------- |
| jellyfin          | cgr.dev/chainguard/wolfi-base |
| jellyfin-server   | cgr.dev/chainguard/wolfi-base |
| lidarr            | cgr.dev/chainguard/wolfi-base |
| mongodb-7         | cgr.dev/chainguard/wolfi-base |
| mongodb-community | cgr.dev/chainguard/wolfi-base |
| mysql-8           | cgr.dev/chainguard/wolfi-base |
| mysql-backup      | cgr.dev/chainguard/wolfi-base |
| mysql-init        | cgr.dev/chainguard/wolfi-base |
| mysql-restore     | cgr.dev/chainguard/wolfi-base |
| pihole-ftl        | scratch                       |
| postgres-backup   | cgr.dev/chainguard/wolfi-base |
| postgres-restore  | cgr.dev/chainguard/wolfi-base |
| postgresql-17     | cgr.dev/chainguard/wolfi-base |
| postgresql-init   | cgr.dev/chainguard/wolfi-base |
| prowlarr          | cgr.dev/chainguard/wolfi-base |
| radarr            | cgr.dev/chainguard/wolfi-base |
| shield            | scratch                       |
| sonarr            | cgr.dev/chainguard/wolfi-base |
| sonic             | scratch                       |
| wolfi-gcc         | cgr.dev/chainguard/wolfi-base |
| zeromq            | cgr.dev/chainguard/wolfi-base |

---

## 7. Per-Image Audit Table

| Image                             | Build Type      | Ph? | ENTRYPOINT                           | EXPOSE                     | HC       | Base               | User                  | Issues                              |
| --------------------------------- | --------------- | :-: | ------------------------------------ | -------------------------- | -------- | ------------------ | --------------------- | ----------------------------------- |
| 389ds                             | pkg-install     |     | /usr/sbin/slapd                      | 389,636                    | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| aarch64-unknown-linux-musl        | unknown         |     | NONE                                 | -                          | NONE     | scratch            | 65532:65532           | NO_ENTRYPOINT,NO_EXPOSE             |
| activemq                          | binary-download |  Y  | /opt/activemq/bin/activemq", "conso  | 61616,8161,5672,61613      | NONE     | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,HEALTHCHECK... |
| adempiere                         | repack          |     | java", "-jar", "/opt/adempiere/Adem  | 8080                       | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| adguard-dns                       | binary-download |  Y  | /AdGuardHome                         | 53,53                      | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| adguardhome-lite                  | binary-download |  Y  | /AdGuardHome                         | 53,53                      | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| adguardhome                       | binary-download |  Y  | /AdGuardHome                         | 53,3000                    | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| age                               | binary-download |  Y  | /usr/local/bin/age                   | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| airbyte-server                    | repack          |     | java", "-jar", "/app/server.jar      | 8000                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| airbyte-worker                    | repack          |     | java", "-jar", "/app/worker.jar      | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE                           |
| airbyte                           | repack          |     | java", "-jar", "/app/airbyte.jar     | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE                           |
| airsonic-advanced                 | binary-download |     | java", "-jar", "/app/airsonic-advan  | 4040                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| airsonic                          | binary-download |     | java", "-jar", "/app/airsonic.war    | 4040                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| akaunting                         | pkg-install     |     | php-fpm                              | 80,443                     | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| alertmanager                      | binary-download |  Y  | /alertmanager                        | 9093                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| alpine-static                     | unknown         |     | NONE                                 | -                          | NONE     | cgr.dev/chainguard | 65532:65532           | NO_ENTRYPOINT,NO_EXPOSE,HEALTHCH... |
| alpine                            | pkg-install     |     | NONE                                 | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_ENTRYPOINT,NO_EXPOSE             |
| amd64                             | unknown         |     | NONE                                 | -                          | NONE     | scratch            | 65532:65532           | NO_ENTRYPOINT,NO_EXPOSE             |
| apache-ofbiz                      | repack          |     | java", "-jar", "/opt/apache-ofbiz/a  | 8080                       | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| apache                            | pkg-install     |     | apache2ctl                           | 80,443                     | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| appsmith-editor                   | repack          |     | node                                 | 8080                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| appsmith-nginx                    | repack          |     | node                                 | 80                         | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| appsmith                          | repack          |     | node                                 | 8080                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| arango                            | binary-download |  Y  | /opt/arangodb/usr/sbin/arangod", "-  | 8529                       | http/tcp | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK                |
| arangodb-starter                  | repack          |     | /arangod", "--serverstarter          | 8529                       | NONE     | scratch            | 65532:65532           |                                     |
| arangodb                          | binary-download |  Y  | /arangod                             | 8529                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| argo-cd                           | binary-download |  Y  | /argocd                              | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| argo-rollouts                     | binary-download |  Y  | /kubectl-argo-rollouts               | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| argocd-application-controller     | binary-download |     | argocd-application-controller        | 8082                       | NONE     | scratch            | 65532:65532           |                                     |
| argocd-applicationset-controller  | binary-download |     | argocd-applicationset-controller     | 8082                       | NONE     | scratch            | 65532:65532           |                                     |
| argocd-notifications              | binary-download |     | argocd-notifications                 | 8082                       | NONE     | scratch            | 65532:65532           |                                     |
| argocd-redis                      | binary-download |  Y  | /usr/local/bin/redis                 | 6379                       | native   | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK                |
| argocd-repo-server                | binary-download |     | argocd-repo-server                   | 8081                       | NONE     | scratch            | 65532:65532           |                                     |
| argocd                            | binary-download |     | argocd                               | 8080                       | NONE     | scratch            | 65532:65532           |                                     |
| arm64                             | pkg-install     |     | NONE                                 | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_ENTRYPOINT,NO_EXPOSE             |
| athom                             | pkg-install     |     | NONE                                 | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_ENTRYPOINT,NO_EXPOSE             |
| audiobookshelf-opds               | repack          |     | node                                 | 13379                      | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| audiobookshelf                    | repack          |     | node                                 | 13378                      | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| auditbeat                         | binary-download |  Y  | /opt/auditbeat/auditbeat             | 5066                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| authelia-lite                     | binary-download |  Y  | /usr/local/bin/authelia              | 80,443                     | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| authelia                          | binary-download |  Y  | /authelia                            | 80,443                     | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| automatic1111                     | source-build    |     | python3", "/opt/automatic1111/launc  | 7860                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| awslogs                           | repack          |  Y  | awslogs                              | -                          | NONE     | registry.access.re | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE,H... |
| azurelogs                         | repack          |  Y  | python3", "-m", "azure.monitor.inge  | -                          | NONE     | registry.access.re | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE,H... |
| badger                            | source-build    |  Y  | /usr/local/bin/badger                | 8080                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| basic-auth-proxy                  | source-build    |  Y  | /opt/nginx/sbin/nginx                | 8080                       | NONE     | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,HEALTHCHECK... |
| bazarr-subliminal                 | source-build    |     | python3", "/opt/bazarr-subliminal/b  | 6768                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| bazarr                            | source-build    |     | python3", "/opt/bazarr/bazarr.py     | 6767                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| beancount                         | repack          |  Y  | python3", "-m", "beancount           | 8080                       | NONE     | registry.access.re | 65532:65532           | PLACEHOLDER_FALLBACK,HEALTHCHECK... |
| betteruptime                      | source-build    |  Y  | /betteruptime                        | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| bind-exporter                     | binary-download |  Y  | /bind_exporter                       | 9119                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| bind                              | binary-download |  Y  | /named                               | 53,953                     | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| blackbox-exporter                 | binary-download |  Y  | /blackbox_exporter                   | 9115                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| blocky                            | binary-download |  Y  | /blocky                              | 53,4000                    | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| browserless-chrome                | repack          |     | node                                 | 3000                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| browserless-edge                  | repack          |     | node                                 | 3000                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| browserless                       | repack          |     | node                                 | 3000                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| budibase-worker                   | repack          |     | node                                 | 10001                      | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| budibase                          | repack          |     | node                                 | 10000                      | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| buildah                           | repack          |     | buildah                              | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE                           |
| buildkit                          | binary-download |     | buildkitd                            | 1234                       | NONE     | scratch            | 65532:65532           |                                     |
| buildx                            | binary-download |  Y  | /buildx                              | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| bundler                           | pkg-install     |     | bundle                               | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE                           |
| busybox                           | pkg-install     |     | /bin/busybox                         | -                          | NONE     | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE,HEALTHCHECK_NONE_NON_S... |
| caddy-alpine                      | binary-download |  Y  | /usr/local/bin/caddy                 | 80,443,443                 | NONE     | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,HEALTHCHECK... |
| caddy-fileserver                  | binary-download |  Y  | /caddy                               | 80,2019                    | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| caddy-reverseproxy                | binary-download |  Y  | /caddy                               | 80,443                     | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| caddy-wildcard                    | binary-download |  Y  | /caddy                               | 80,443                     | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| caddy                             | binary-download |  Y  | /caddy                               | 80,443,2019                | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| cadvisor                          | repack          |  Y  | /cadvisor                            | 8080                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| calibre-eb                        | pkg-install     |     | calibre-server                       | 8080                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| calibre-server                    | pkg-install     |     | calibre-server                       | 8080                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| calibre-web                       | pkg-install     |     | python                               | 8083                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| calibre                           | pkg-install     |     | python3                              | 8080                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| cargo-audit                       | source-build    |  Y  | cargo-audit                          | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| cassandra-operator                | repack          |  Y  | /usr/local/bin/cass-operator         | 8080,8443                  | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| cayley                            | source-build    |  Y  | /usr/local/bin/cayley                | 64210                      | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| certificates                      | binary-download |  Y  | /cfssl                               | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| chartdb                           | repack          |  Y  | java", "-jar", "/opt/chartdb/chartd  | 8080                       | http/tcp | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK                |
| chat-server                       | pkg-install     |     | synapse                              | 8008                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| checkov-k8s                       | repack          |  Y  | checkov                              | -                          | http/tcp | registry.access.re | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| checkov                           | repack          |  Y  | checkov                              | -                          | http/tcp | registry.access.re | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| chevereto                         | pkg-install     |     | php                                  | 80                         | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| chkrootkit                        | repack          |     | chkrootkit                           | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE                           |
| chroma-all-minimal                | pkg-install     |     | python3                              | 8000                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| chroma                            | pkg-install     |     | chroma                               | 8000                       | http/tcp | cgr.dev/chainguard | chroma                |                                     |
| cinny                             | repack          |     | httpd                                | 80                         | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| clamav-daemon                     | repack          |     | clamd                                | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE                           |
| clamav                            | repack          |     | clamd                                | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE                           |
| cloudflare-ddns                   | binary-download |  Y  | /cloudflare-ddns                     | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| cloudflare-warrior                | binary-download |  Y  | /cloudflared                         | 7844                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| cloudflared                       | binary-download |  Y  | /cloudflared                         | 7844                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| cloudreve                         | binary-download |  Y  | /cloudreve                           | 5212                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| cloudwatch-agent                  | repack          |     | /amazon-cloudwatch-agent             | 25888,12789                | NONE     | scratch            | 65532:65532           |                                     |
| cockpit                           | repack          |     | cockpit-ws                           | 9090                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| cockroachdb-exporter              | binary-download |  Y  | /cockroach                           | 8080                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| cockroachdb-sql                   | binary-download |  Y  | /usr/local/bin/cockroach             | 26257                      | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| cockroachdb                       | binary-download |  Y  | /usr/local/bin/cockroach             | 26257,8080                 | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| codimd                            | repack          |     | node                                 | 3000                       | http/tcp | cgr.dev/chainguard | 65532:65532           | BLOATED                             |
| collabora-online-code             | pkg-install     |     | /usr/bin/loolwsd                     | 9980                       | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| collabora-online                  | pkg-install     |     | /usr/bin/loolwsd                     | 9980                       | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| collabora                         | repack          |     | /usr/bin/loolwsd                     | 9980                       | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| comfyui                           | source-build    |     | python3", "/opt/comfyui/main.py", "  | 8188                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| composer-audit                    | binary-download |     | composer                             | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE                           |
| composer                          | binary-download |  Y  | /composer                            | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| conan-audit                       | repack          |  Y  | conan                                | -                          | http/tcp | registry.access.re | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| conduit-admin                     | repack          |  Y  | /usr/local/bin/conduit               | 6167                       | http/tcp | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK                |
| conduit                           | repack          |  Y  | /usr/local/bin/conduit               | 6167                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| consul-exporter                   | binary-download |  Y  | /consul_exporter                     | 9107                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| consul-template                   | binary-download |  Y  | /consul-template                     | 8500                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| consul                            | binary-download |  Y  | /consul                              | 8500                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| convector                         | pkg-install     |     | node                                 | 8008                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| coqui-tts                         | pkg-install     |     | python3                              | 5002                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| coredns-alpine                    | binary-download |  Y  | /coredns                             | 53,53                      | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| coredns                           | binary-download |  Y  | /coredns                             | 53                         | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| cors-proxy                        | source-build    |  Y  | /opt/nginx/sbin/nginx                | 8080                       | NONE     | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,HEALTHCHECK... |
| cortex                            | binary-download |  Y  | /cortex                              | 9009                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| cosign-verify                     | binary-download |  Y  | /cosign                              | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| cosign                            | binary-download |  Y  | /cosign                              | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| couchbase-operator                | repack          |  Y  | /usr/local/bin/couchbase-operator    | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| couchbase                         | repack          |  Y  | /opt/couchbase/bin/couchbase-server  | 8091                       | NONE     | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,HEALTHCHECK... |
| couchdb                           | repack          |  Y  | sh", "-c", "/opt/couchdb/bin/couchd  | 5984                       | NONE     | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,HEALTHCHECK... |
| courier-authlib                   | repack          |     | NONE                                 | 0                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_ENTRYPOINT                       |
| courier-imap                      | repack          |     | NONE                                 | 143,993                    | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_ENTRYPOINT                       |
| crane                             | binary-download |  Y  | /crane                               | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| crate                             | binary-download |  Y  | /opt/crate/bin/crate                 | 4200,5432                  | http/tcp | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,BLOATED        |
| crawlergo                         | binary-download |  Y  | /crawlergo                           | 0                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| crdb-init                         | binary-download |  Y  | /usr/local/bin/cockroach", "init     | 26257                      | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| crowdsec-agent                    | repack          |     | /crowdsec                            | 8080,6060                  | NONE     | scratch            | 65532:65532           |                                     |
| crowdsec-lapi                     | repack          |     | /crowdsec                            | 8080,6060                  | NONE     | scratch            | 65532:65532           |                                     |
| crowdsec                          | repack          |     | /crowdsec                            | 8080,6060                  | NONE     | scratch            | 65532:65532           |                                     |
| cryptpad                          | repack          |     | node                                 | 3000                       | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| ct-log                            | source-build    |  Y  | /ct-log                              | 6962                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| cyberchef-node                    | source-build    |     | node", "CyberChef.js                 | 3000                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| cyberchef                         | source-build    |     | node", "server.js                    | 8080                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| dagster-daemon                    | pkg-install     |     | dagster-daemon                       | 3000                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| dagster-logs                      | pkg-install     |     | dagster-logs                         | 3000                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| dagster                           | pkg-install     |     | dagster-webserver                    | 3000                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| dashy-alpine                      | source-build    |     | node", "server.js                    | 80,443                     | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| dashy                             | binary-download |  Y  | /dashy                               | 80                         | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| dbmate                            | repack          |     | /dbmate                              | -                          | NONE     | scratch            | 65532:65532           | NO_EXPOSE                           |
| debian-slim                       | pkg-install     |     | NONE                                 | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_ENTRYPOINT,NO_EXPOSE             |
| deepspeed                         | pkg-install     |     | python3                              | 8080                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| dendrite-monolith                 | repack          |     | /usr/local/bin/dendrite              | 8008                       | NONE     | scratch            | 65532:65532           |                                     |
| dendrite-pot                      | repack          |     | /usr/local/bin/dendrite              | 8008                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| dendrite                          | repack          |     | /usr/local/bin/dendrite              | 8008                       | NONE     | scratch            | 65532:65532           |                                     |
| derby                             | binary-download |     | java", "-jar", "/opt/derby/lib/derb  | 1527                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| dex                               | source-build    |     | /dex                                 | 5556                       | NONE     | scratch            | 65532:65532           |                                     |
| diffusers                         | pkg-install     |     | python3                              | 8000                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| distroless                        | unknown         |     | NONE                                 | -                          | NONE     | gcr.io/distroless/ | -                     | NO*ENTRYPOINT,NO_EXPOSE,MISSING*... |
| dnsdist                           | source-build    |     | /usr/local/bin/dnsdist               | 53,53                      | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| dnsmasq                           | binary-download |  Y  | /dnsmasq                             | 53                         | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| dnsvalidator                      | repack          |     | /opt/venv/bin/dnsvalidator           | 8080                       | http/tcp | registry.access.re | 65532:65532           |                                     |
| docker-bench                      | source-build    |     | sh                                   | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE                           |
| docker-clean                      | pkg-install     |     | docker-clean                         | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE                           |
| docker-gc                         | repack          |     | docker-gc                            | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE                           |
| docker-socket-proxy               | repack          |     | docker-entrypoint.sh                 | 2375                       | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| docui                             | binary-download |  Y  | /lazydocker                          | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| dolibarr                          | repack          |     | php-8.4-fpm                          | 80,443                     | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| dotdns                            | source-build    |     | /usr/local/bin/dotdns                | 53,8053                    | NONE     | scratch            | 65532:65532           |                                     |
| dovecot-lda                       | repack          |     | dovecot", "-F                        | 143,993                    | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| dovecot-pop3                      | repack          |     | dovecot", "-F                        | 110,995                    | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| dovecot                           | repack          |     | dovecot                              | 143,993,110,995,24         | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| dragonfly-client                  | binary-download |  Y  | /dfly                                | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| dragonfly                         | binary-download |  Y  | /dragonfly                           | 6379                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| drone-agent                       | repack          |     | /usr/local/bin/drone-agent           | 3000                       | NONE     | scratch            | 65532:65532           |                                     |
| drone-autoscaler                  | repack          |     | /usr/local/bin/drone-autoscaler      | 8080                       | NONE     | scratch            | 65532:65532           |                                     |
| drone-runner                      | repack          |     | /usr/local/bin/drone-runner-exec     | 3000                       | NONE     | scratch            | 65532:65532           |                                     |
| drone                             | repack          |     | /drone                               | 80                         | NONE     | scratch            | 65532:65532           |                                     |
| druid                             | repack          |     | /opt/druid/bin/start-druid           | 8088,8888,8280             | http/tcp | cgr.dev/chainguard | 65532:65532           | BLOATED                             |
| duckdb                            | binary-download |     | /usr/local/bin/duckdb                | 5432                       | NONE     | scratch            | 65532:65532           |                                     |
| duplicati                         | binary-download |  Y  | dotnet", "/opt/duplicati/Duplicati.  | 8200                       | NONE     | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,HEALTHCHECK... |
| egroupware                        | repack          |     | php-8.4-fpm                          | 80,443                     | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| elasticsearch-8                   | repack          |  Y  | /opt/elasticsearch/bin/elasticsearc  | 9200,9300                  | http/tcp | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK                |
| elasticsearch-curator             | repack          |     | curator                              | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE                           |
| elasticsearch-exporter            | repack          |  Y  | /elasticsearch_exporter              | 9114                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| elasticsearch                     | binary-download |     | sh", "-c", "elasticsearch            | 9200,9300                  | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| element-web                       | repack          |     | busybox", "httpd", "-f", "-p", "80"  | 80                         | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| element-x                         | repack          |     | busybox", "httpd", "-f", "-p", "80"  | 80                         | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| emby                              | repack          |     | /opt/emby-server/emby-server         | 8096,8920                  | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| emqx-ee                           | repack          |     | echo                                 | 1883,8083,8084,8883,18083  | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| emqx                              | binary-download |     | /opt/emqx/bin/emqx                   | 1883,8083,8084,8883,18083  | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| envoy-extras                      | binary-download |     | /usr/local/bin/envoy                 | 9901                       | NONE     | scratch            | 65532:65532           |                                     |
| envoy-grpc                        | binary-download |     | /usr/local/bin/envoy                 | 15001,15090                | NONE     | scratch            | 65532:65532           |                                     |
| envoy-init                        | binary-download |     | /usr/local/bin/envoy", "--mode", "i  | 9901                       | NONE     | scratch            | 65532:65532           |                                     |
| envoy-sidecar                     | binary-download |     | /usr/local/bin/envoy", "--mode", "s  | 15001                      | NONE     | scratch            | 65532:65532           |                                     |
| envoy                             | binary-download |     | /usr/local/bin/envoy                 | 9901                       | NONE     | scratch            | 65532:65532           |                                     |
| erpnext-worker                    | repack          |  Y  | bench                                | 8000,9000                  | http/tcp | registry.access.re | 65532:65532           | PLACEHOLDER_FALLBACK                |
| erpnext                           | pkg-install     |     | python3                              | 8000                       | http/tcp | cgr.dev/chainguard | erpnext               |                                     |
| espeasy                           | repack          |     | NONE                                 | -                          | http/tcp | registry.access.re | 65532:65532           | NO_ENTRYPOINT,NO_EXPOSE             |
| esphome-daemon                    | repack          |  Y  | esphome                              | 6053                       | http/tcp | registry.access.re | 65532:65532           | PLACEHOLDER_FALLBACK                |
| esphome                           | repack          |  Y  | esphome                              | 6052                       | http/tcp | registry.access.re | 65532:65532           | PLACEHOLDER_FALLBACK                |
| espocrm                           | repack          |     | php-8.4-fpm                          | 80,443                     | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| espurna                           | repack          |     | NONE                                 | -                          | http/tcp | registry.access.re | 65532:65532           | NO_ENTRYPOINT,NO_EXPOSE             |
| etcd-backup                       | binary-download |  Y  | /usr/local/bin/etcdctl               | 2379                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| etcd-empty                        | binary-download |  Y  | /etcd                                | 2379,2380                  | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| etcd-operator                     | binary-download |  Y  | /usr/local/bin/etcdctl               | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| etcd                              | binary-download |  Y  | /etcd                                | 2379,2380                  | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| fail2ban-exporter                 | source-build    |     | /fail2ban-exporter                   | 9191                       | NONE     | scratch            | 65532:65532           |                                     |
| fail2ban                          | pkg-install     |     | fail2ban                             | 22                         | http/tcp | cgr.dev/chainguard | appuser               |                                     |
| falco-rules                       | source-build    |     | cat                                  | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE                           |
| falco                             | binary-download |     | falco                                | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE                           |
| falcosidekick                     | binary-download |  Y  | /falcosidekick                       | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| ferretdb                          | binary-download |     | /usr/local/bin/ferretdb              | 27017,8080                 | NONE     | scratch            | 65532:65532           |                                     |
| filebeat                          | binary-download |  Y  | /opt/filebeat/filebeat               | 5066                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| filebrowser-alpine                | binary-download |  Y  | /filebrowser                         | 8080                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| filebrowser                       | binary-download |  Y  | /filebrowser                         | 8080                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| firebird                          | pkg-install     |     | firebird                             | 3050                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| firefly-iii-importer              | repack          |  Y  | python3", "-m", "firefly_iii         | 8080                       | NONE     | registry.access.re | 65532:65532           | PLACEHOLDER_FALLBACK,HEALTHCHECK... |
| firefly-iii                       | pkg-install     |     | php                                  | 80                         | http/tcp | cgr.dev/chainguard | www-data              |                                     |
| fluent-bit                        | repack          |     | fluent-bit                           | 2020                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| flux                              | binary-download |  Y  | /flux                                | 3030                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| flux2                             | binary-download |  Y  | /flux                                | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| fluxcd-helm                       | binary-download |  Y  | /flux", "bootstrap", "helm-release   | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| fluxcd-image                      | binary-download |  Y  | /flux", "bootstrap", "image-automat  | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| focalboard-server                 | binary-download |  Y  | /opt/focalboard/bin/focalboard-serv  | 8000                       | NONE     | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,HEALTHCHECK... |
| forgejo-runner                    | repack          |     | /usr/local/bin/forgejo-runner        | 8088                       | NONE     | scratch            | 65532:65532           |                                     |
| forgejo                           | repack          |  Y  | /usr/local/bin/forgejo               | 3000,22                    | NONE     | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,HEALTHCHECK... |
| freeipa-client                    | pkg-install     |     | /usr/bin/sssctl                      | -                          | NONE     | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE,HEALTHCHECK_NONE_NON_S... |
| freshclam                         | repack          |     | freshclam                            | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE                           |
| freshrss-minimal                  | pkg-install     |     | php                                  | 80                         | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| freshrss                          | pkg-install     |     | php                                  | 80                         | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| frontaccounting                   | repack          |     | php-8.4-fpm                          | 80,443                     | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| fulcio                            | binary-download |  Y  | /fulcio                              | 5555                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| gallery3                          | source-build    |     | python3", "/opt/gallery3/manage.py"  | 8000                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| gcplogs                           | repack          |  Y  | python3", "-m", "google.cloud.loggi  | -                          | NONE     | registry.access.re | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE,H... |
| gem-audit                         | repack          |     | bundler-audit                        | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE                           |
| ggshield                          | repack          |  Y  | ggshield                             | -                          | http/tcp | registry.access.re | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| git-secrets                       | binary-download |     | git-secrets                          | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE,BLOATED                   |
| gitea-actions                     | binary-download |     | gitea                                | 3000                       | NONE     | scratch            | 65532:65532           |                                     |
| gitea-editor                      | binary-download |     | gitea                                | 3000                       | NONE     | scratch            | 65532:65532           |                                     |
| gitea-secure                      | binary-download |     | gitea                                | 3000                       | NONE     | scratch            | 65532:65532           |                                     |
| gitea                             | repack          |     | /usr/local/bin/gitea                 | 3000,22                    | http/tcp | cgr.dev/chainguard | git                   |                                     |
| gitguardian                       | repack          |  Y  | ggshield                             | -                          | http/tcp | registry.access.re | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| github-actions-minimal            | binary-download |     | /app/runner/bin/Runner.Worker        | 8080                       | http/tcp | cgr.dev/chainguard | 65532:65532           | BLOATED                             |
| github-actions-runner             | pkg-install     |     | run.sh                               | -                          | http/tcp | cgr.dev/chainguard | runner                | NO_EXPOSE                           |
| gitlab-backup                     | source-build    |     | /usr/local/bin/backup                | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE,BLOATED                   |
| gitlab-ce                         | binary-download |     | /opt/gitlab/bin/gitlab               | 80,443,22                  | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| gitlab-ee                         | binary-download |     | /opt/gitlab/bin/gitlab               | 80,443,22                  | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| gitlab-geo                        | binary-download |     | /opt/gitlab/bin/gitlab-geo           | 80,443                     | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| gitlab-runner-alpine              | binary-download |     | gitlab-runner                        | 8093                       | NONE     | scratch            | 65532:65532           |                                     |
| gitlab-runner                     | binary-download |     | gitlab-runner                        | 8093                       | NONE     | scratch            | 65532:65532           |                                     |
| gitlab                            | repack          |     | NONE                                 | 80,22,443                  | NONE     | scratch            | git                   | NO_ENTRYPOINT                       |
| gitleaks                          | binary-download |  Y  | /gitleaks                            | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| gitserver                         | binary-download |     | /opt/gitserver/gitea                 | 80,22                      | NONE     | scratch            | 65532:65532           |                                     |
| gnucash                           | pkg-install     |     | gnucash                              | 8080                       | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| go-static                         | binary-download |  Y  | go                                   | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| gogs                              | binary-download |  Y  | gogs                                 | 3000                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| golang-alpine                     | binary-download |  Y  | go                                   | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| golang-cache                      | source-build    |  Y  | /usr/local/bin/go-1.23-cache         | 6379                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| golang                            | repack          |     | go                                   | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE                           |
| gotify                            | repack          |     | /usr/local/bin/gotify                | 8080                       | NONE     | scratch            | 65532:65532           |                                     |
| gradle                            | binary-download |  Y  | gradle                               | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| grafana-dev                       | binary-download |  Y  | /usr/local/bin/grafana-server        | 3000                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| grafana-image-renderer            | binary-download |  Y  | /opt/grafana-image-renderer/build/g  | 8081                       | NONE     | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,HEALTHCHECK... |
| grafana-lite                      | binary-download |  Y  | /grafana-server                      | 3000                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| grafana-operator                  | repack          |     | /usr/local/bin/grafana-operator      | -                          | NONE     | scratch            | 65532:65532           | NO_EXPOSE                           |
| grafana-oss                       | binary-download |  Y  | /grafana-server                      | 3000                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| grafana-toolkit                   | binary-download |  Y  | npx", "grafana-toolkit               | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE,B... |
| grafana                           | binary-download |  Y  | grafana-server                       | 3000                       | http/tcp | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK                |
| graphdb-enterpriser               | repack          |     | /opt/graphdb/bin/graphdb             | 7200                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| graphile                          | pkg-install     |  Y  | node", "/opt/graphile/cli.js         | 5000                       | http/tcp | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK                |
| graylog-sidecar                   | binary-download |  Y  | /opt/sidecar/collector_sidecar       | 8989                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| graylog                           | binary-download |     | /opt/graylog/bin/graylogctl          | 9000,12201,5044            | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| grisbi                            | pkg-install     |     | grisbi                               | 8080                       | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| grub                              | unknown         |     | NONE                                 | -                          | NONE     | scratch            | 65532:65532           | NO_ENTRYPOINT,NO_EXPOSE             |
| grype-alpine                      | binary-download |  Y  | /grype                               | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| grype                             | binary-download |  Y  | /grype                               | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| h2                                | binary-download |     | java", "-cp", "/opt/h2/h2.jar", "or  | 8082,9092                  | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| hackmd                            | pkg-install     |     | node", "app.js                       | 3000                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| hadolint                          | binary-download |  Y  | /hadolint                            | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| haproxy-dev                       | repack          |     | /usr/local/sbin/haproxy", "-f", "/d  | 8404                       | NONE     | scratch            | 65532:65532           |                                     |
| haproxy-exporter                  | binary-download |  Y  | /haproxy_exporter                    | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| haproxy-lb                        | repack          |     | /usr/local/sbin/haproxy", "-f", "/d  | 80,443                     | NONE     | scratch            | 65532:65532           |                                     |
| haproxy                           | repack          |     | /usr/local/sbin/haproxy              | 8404                       | NONE     | scratch            | 65532:65532           |                                     |
| hashicorp-vault                   | binary-download |  Y  | /vault                               | 8200,8201                  | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| hazelcast                         | binary-download |     | /opt/hazelcast/bin/hazelcast         | 5701,5702,5703,8080        | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| headscale-ui                      | binary-download |     | /app/fileserver                      | 8080                       | NONE     | gcr.io/distroless/ | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| headscale                         | binary-download |  Y  | /headscale                           | 8080,443                   | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| health-checks                     | source-build    |  Y  | /health-checks                       | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| health-shim                       | source-build    |     | /health-shim                         | -                          | -        | scratch            | 65532:65532           | NO_HEALTHCHECK,NO_EXPOSE            |
| healthcheck                       | binary-download |  Y  | /grpc_health_probe                   | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| heartbeat                         | binary-download |  Y  | /opt/heartbeat/heartbeat             | 5066                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| hedgedoc-legacy                   | pkg-install     |     | node", "app.js                       | 3000                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| hedgedoc                          | pkg-install     |     | node", "app.js                       | 3000                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| heimdall-lite                     | source-build    |     | node                                 | 80                         | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| heimdall                          | source-build    |     | node                                 | 80,443                     | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| helm                              | binary-download |  Y  | /helm                                | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| helmfile                          | binary-download |  Y  | /helmfile                            | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| helmsman                          | binary-download |  Y  | /helmsman                            | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| hledger                           | binary-download |     | /hledger                             | -                          | NONE     | scratch            | 65532:65532           | NO_EXPOSE                           |
| homeassistant-core                | pkg-install     |     | python", "-m", "homeassistant        | -                          | http/tcp | debian             | 65532:65532           | NO_EXPOSE                           |
| homeassistant-hassio              | pkg-install     |     | python", "-m", "homeassistant        | -                          | http/tcp | debian             | 65532:65532           | NO_EXPOSE                           |
| homeassistant-supervisor          | pkg-install     |     | python", "-m", "homeassistant-assis  | -                          | http/tcp | debian             | 65532:65532           | NO_EXPOSE                           |
| homeassistant                     | pkg-install     |     | python3                              | 8123                       | http/tcp | cgr.dev/chainguard | homeassistant         |                                     |
| homebridge-camera                 | repack          |  Y  | homebridge                           | 51826,8554                 | http/tcp | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,BLOATED        |
| homebridge                        | repack          |  Y  | homebridge                           | 51826                      | http/tcp | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,BLOATED        |
| homekit                           | pkg-install     |     | NONE                                 | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_ENTRYPOINT,NO_EXPOSE             |
| homepage-config                   | repack          |     | homepage                             | 3000                       | NONE     | scratch            | 65532:65532           |                                     |
| homepage-sync                     | repack          |     | homepage                             | 3000                       | NONE     | scratch            | 65532:65532           |                                     |
| homepage                          | repack          |     | /app/homepage                        | 3000                       | NONE     | scratch            | 65532:65532           |                                     |
| hydrogen                          | binary-download |     | busybox", "httpd", "-f", "-p", "808  | 8080                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| idempiere                         | repack          |     | java", "-jar", "/opt/idempiere/idem  | 8080                       | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| ignite                            | binary-download |  Y  | /opt/ignite/bin/ignite.sh            | 10800,11211,47100,47500    | http/tcp | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK                |
| immich-machine-learning           | pkg-install     |     | python3                              | 3003                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| immich-microservices              | repack          |     | node                                 | 3002                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| immich-ml                         | pkg-install     |     | python3                              | 3003                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| immich-server                     | repack          |     | node                                 | 3001                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| immich                            | pkg-install     |     | node                                 | 2283                       | http/tcp | cgr.dev/chainguard | immich                |                                     |
| immudb                            | binary-download |  Y  | /usr/local/bin/immudb                | 3322,9497                  | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| influxdb-2                        | repack          |     | /influxd                             | 8086                       | NONE     | scratch            | 65532:65532           |                                     |
| influxdb-client                   | binary-download |  Y  | /influx                              | 8086                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| influxdb                          | repack          |     | /influxd                             | 8086                       | NONE     | scratch            | 65532:65532           |                                     |
| invoice-ninja-api                 | repack          |     | php-8.4-fpm                          | 80,443                     | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| invoice-ninja                     | repack          |     | php-8.4-fpm                          | 80,443                     | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| invokeai                          | pkg-install     |     | python3                              | 9090                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| iobroker                          | repack          |     | iobroker                             | 8081,3000                  | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| ipmi-exporter                     | binary-download |  Y  | /ipmi_exporter                       | 9290                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| it-tools-legacy                   | source-build    |     | node", "server.js                    | 8080                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| it-tools                          | binary-download |  Y  | /it-tools                            | 80                         | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| jaeger-agent                      | binary-download |  Y  | /jaeger-agent                        | 5775                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| jaeger-collector                  | binary-download |  Y  | /jaeger-collector                    | 14267                      | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| jaeger-query                      | binary-download |  Y  | /jaeger-query                        | 16686                      | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| jaeger                            | binary-download |  Y  | /jaeger-agent                        | 5775,6831,6832             | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| janusgraph                        | binary-download |     | /opt/janusgraph/bin/gremlin.sh       | 8182                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| jellyfin-server                   | binary-download |     | /app/jellyfin                        | 8096                       | NONE     | cgr.dev/chainguard | 65532:65532           | WRONG*BASE,HEALTHCHECK_NONE_NON*... |
| jellyfin                          | binary-download |     | /app/jellyfin                        | 8096                       | NONE     | cgr.dev/chainguard | 65532:65532           | WRONG*BASE,HEALTHCHECK_NONE_NON*... |
| jenkins-agent                     | binary-download |  Y  | java", "-jar", "/app/agent.jar       | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| jenkins-executor                  | binary-download |  Y  | java", "-jar", "/app/agent.jar", "-  | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| jenkins-plugin                    | binary-download |  Y  | java", "-jar", "/app/jenkins.war     | 8080                       | http/tcp | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK                |
| jenkins                           | pkg-install     |     | jenkins                              | 8080                       | http/tcp | cgr.dev/chainguard | jenkins               |                                     |
| jitsu                             | repack          |     | node                                 | 8000                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| journalbeat                       | binary-download |  Y  | /opt/journalbeat/journalbeat         | 5066                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| jupyter-all                       | pkg-install     |     | jupyter                              | 8888                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| jupyter-pytorch                   | pkg-install     |     | jupyter-lab                          | 8888                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| jupyter-scikit                    | pkg-install     |     | jupyter-lab                          | 8888                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| jupyter-tensorflow                | pkg-install     |     | jupyter-lab                          | 8888                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| k3d-proxy                         | binary-download |  Y  | /k3d", "proxy                        | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| k3d                               | binary-download |  Y  | /k3d                                 | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| k3s-agent                         | binary-download |  Y  | /k3s", "agent                        | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| k3s-server                        | binary-download |  Y  | /k3s", "server                       | 6443                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| k3s                               | binary-download |  Y  | /k3s                                 | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| kafka-connect                     | binary-download |     | /opt/kafka/bin/connect-distributed.  | 8083                       | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| kafka-exporter                    | binary-download |  Y  | /kafka_exporter                      | 9308                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| kafka-ui                          | binary-download |  Y  | /opt/kafka-ui/kafka-ui               | 8080                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| kafka                             | binary-download |     | sh", "-c", "/opt/kafka/bin/kafka-se  | 9092                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| keycloak-gatekeeper               | binary-download |  Y  | /keycloak-gatekeeper                 | 8080                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| keycloak-init                     | binary-download |  Y  | /opt/keycloak/bin/kc.sh              | 8080,8443                  | NONE     | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,HEALTHCHECK... |
| keycloak-quarkus                  | binary-download |  Y  | /opt/keycloak/bin/kc.sh              | 8080,8443                  | NONE     | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,HEALTHCHECK... |
| keycloak                          | pkg-install     |  Y  | /opt/keycloak/bin/kc.sh              | 8080,8443                  | NONE     | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,HEALTHCHECK... |
| kibana-oss                        | binary-download |  Y  | /opt/kibana/bin/kibana               | 5601                       | NONE     | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,HEALTHCHECK... |
| kibana                            | binary-download |  Y  | /opt/kibana/bin/kibana               | 5601                       | NONE     | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,HEALTHCHECK... |
| kmymoney                          | pkg-install     |     | kmymoney                             | 8080                       | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| knot-resolver                     | pkg-install     |     | kresd                                | 53,53                      | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| koel-next                         | pkg-install     |     | php                                  | 80                         | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| koel                              | pkg-install     |     | php                                  | 80                         | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| koken                             | pkg-install     |     | php                                  | 80                         | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| kopano                            | pkg-install     |     | php                                  | 80                         | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| kube-apiserver                    | binary-download |  Y  | kube-apiserver                       | 6443                       | http/tcp | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK                |
| kube-bench                        | binary-download |  Y  | /kube-bench                          | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| kube-controller                   | binary-download |  Y  | kube-controller-manager              | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| kube-hunter                       | repack          |  Y  | kube-hunter                          | -                          | http/tcp | registry.access.re | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| kube-proxy                        | binary-download |  Y  | kube-proxy                           | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| kube-scheduler                    | binary-download |  Y  | kube-scheduler                       | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| kube-state-metrics                | binary-download |  Y  | /kube-state-metrics                  | 8080                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| kubectl                           | binary-download |  Y  | /kubectl                             | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| kubescape                         | binary-download |  Y  | /kubescape                           | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| kustomize                         | binary-download |  Y  | /kustomize                           | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| langchain                         | pkg-install     |     | python3                              | 8000                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| langserve                         | pkg-install     |     | python3                              | 8000                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| lazydocker-ui                     | binary-download |  Y  | /lazydocker                          | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| lazydocker                        | binary-download |  Y  | /lazydocker                          | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| ldap-account-manager              | repack          |     | php-fpm                              | 8080                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| ldap                              | pkg-install     |     | slapd                                | 389,636                    | http/tcp | cgr.dev/chainguard | ldap                  |                                     |
| libreoffice-headless              | pkg-install     |     | libreoffice                          | 8080                       | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| libreoffice                       | pkg-install     |     | libreoffice                          | 8080                       | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| libsql                            | binary-download |     | /opt/libsql/libsql-server            | 8080                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| lidarr                            | binary-download |     | /app/Lidarr                          | 8686                       | NONE     | cgr.dev/chainguard | 65532:65532           | WRONG*BASE,HEALTHCHECK_NONE_NON*... |
| linguist-go                       | source-build    |  Y  | /linguist                            | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| linguist                          | source-build    |     | linguist                             | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE                           |
| litellm-proxy                     | pkg-install     |     | litellm                              | 4000                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| litellm                           | pkg-install     |     | python3                              | 4000                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| llama-cpp-server                  | binary-download |  Y  | /llama-server                        | 8080                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| llama.cpp                         | binary-download |  Y  | /llama-server                        | 8080                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| localai                           | binary-download |  Y  | /localai                             | 8080                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| logseq                            | pkg-install     |     | node                                 | 3000                       | http/tcp | cgr.dev/chainguard | node                  |                                     |
| logstash-oss                      | binary-download |     | /opt/logstash/bin/logstash           | 5044,9600                  | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| logstash                          | binary-download |     | /opt/logstash/bin/logstash           | 5044,9600                  | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| loki-canary                       | binary-download |  Y  | /loki-canary                         | 3500                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| loki-simple                       | binary-download |  Y  | /loki", "-config.file=/etc/loki/sim  | 3100                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| loki                              | binary-download |  Y  | /loki                                | 3100                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| lychee                            | pkg-install     |     | php                                  | 80                         | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| lynis                             | source-build    |     | /app/src/lynis                       | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE                           |
| maddy                             | repack          |     | /usr/local/bin/maddy                 | 25,143,465,587,993,995     | NONE     | scratch            | 65532:65532           |                                     |
| mailhog                           | repack          |     | /usr/local/bin/MailHog               | 8025,1025                  | NONE     | scratch            | 65532:65532           |                                     |
| mailu                             | repack          |     | python", "-m", "mailu                | 8080                       | http/tcp | registry.access.re | 65532:65532           |                                     |
| maldet                            | repack          |     | /opt/maldet/maldet                   | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE                           |
| mariadb-10                        | binary-download |     | mariadbd                             | 3306                       | native   | cgr.dev/chainguard | 65532:65532           |                                     |
| mariadb-11                        | binary-download |     | /usr/local/bin/docker-entrypoint.sh  | 3306                       | native   | cgr.dev/chainguard | 65532:65532           |                                     |
| mariadb-galera                    | binary-download |     | mariadbd", "--wsrep_new_cluster      | 3306,4567,4568,4444        | native   | cgr.dev/chainguard | 65532:65532           |                                     |
| mariadb-operator                  | repack          |     | /usr/local/bin/mariadb-operator      | 8080,8443                  | NONE     | scratch            | 65532:65532           |                                     |
| mariadb                           | repack          |     | sh", "-c", "mariadbd                 | 3306                       | native   | cgr.dev/chainguard | 65532:65532           |                                     |
| matrix-hookshot                   | binary-download |     | node                                 | 9993                       | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| mattermost-bridge                 | repack          |     | /app/plugin/server                   | 8065                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| mattermost-operator               | repack          |     | /usr/local/bin/mattermost-kubernete  | 8080                       | NONE     | scratch            | 65532:65532           |                                     |
| mattermost                        | binary-download |  Y  | /opt/mattermost/bin/mattermost       | 8065                       | http/tcp | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK                |
| maven                             | binary-download |  Y  | mvn                                  | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| maxbot                            | pkg-install     |     | maxbot                               | -                          | NONE     | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE,HEALTHCHECK_NONE_NON_S... |
| mc                                | binary-download |  Y  | /mc                                  | 0                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| meilisearch-python                | pkg-install     |     | python                               | 7700                       | http/tcp | cgr.dev/chainguard | python                |                                     |
| meilisearch                       | binary-download |  Y  | /meilisearch                         | 7700                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| meltano                           | pkg-install     |     | meltano                              | 5000                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| memcached-exporter                | binary-download |  Y  | /memcached_exporter                  | 9150                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| memcached                         | repack          |     | memcached                            | 11211                      | native   | cgr.dev/chainguard | 65532:65532           |                                     |
| memgraph                          | repack          |     | /opt/memgraph/bin/memgraph", "--dat  | 7687,7444                  | http/tcp | cgr.dev/chainguard | 65532:65532           | BLOATED                             |
| meshbird                          | source-build    |  Y  | /meshbird                            | 10500,10500                | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| metricbeat                        | binary-download |  Y  | /opt/metricbeat/metricbeat           | 5066                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| milvus-etcd                       | pkg-install     |     | etcd                                 | 2379,2380                  | generic  | cgr.dev/chainguard | 65532:65532           |                                     |
| milvus-minio                      | binary-download |     | /usr/local/bin/minio                 | 9000                       | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| milvus                            | repack          |     | /opt/milvus/bin/milvus               | 19530                      | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| mimir                             | binary-download |  Y  | /mimir                               | 8080                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| miniflux-2                        | repack          |     | /miniflux                            | 8080                       | NONE     | scratch            | 65532:65532           |                                     |
| miniflux-21                       | binary-download |  Y  | /miniflux                            | 8080                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| miniflux                          | repack          |     | /miniflux                            | 8080                       | NONE     | scratch            | 65532:65532           |                                     |
| minio-console                     | repack          |     | /minio                               | 9000,9090                  | NONE     | scratch            | 65532:65532           |                                     |
| minio-operator                    | binary-download |  Y  | /minio-operator                      | 4455                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| minio                             | binary-download |  Y  | /minio                               | 9000,9001                  | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| mlflow-server                     | pkg-install     |     | mlflow                               | 5000                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| mlflow-tracking                   | pkg-install     |     | mlflow                               | 5000                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| mlflow                            | pkg-install     |     | mlflow                               | 5000                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| modsecurity-crs                   | source-build    |     | /usr/sbin/apache2", "-D", "FOREGROU  | 80,443                     | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| modsecurity                       | pkg-install     |     | apache2                              | 80                         | http/tcp | cgr.dev/chainguard | appuser               |                                     |
| mongo-exporter                    | repack          |  Y  | /mongodb_exporter                    | 9216                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| mongodb-5                         | repack          |     | mongod                               | 27017                      | native   | cgr.dev/chainguard | 65532:65532           |                                     |
| mongodb-6                         | repack          |     | mongod                               | 27017                      | native   | cgr.dev/chainguard | 65532:65532           |                                     |
| mongodb-7                         | binary-download |  Y  | mongod                               | 27017                      | native   | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,WRONG_BASE     |
| mongodb-community                 | binary-download |  Y  | mongod                               | 27017                      | native   | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,WRONG_BASE     |
| mongodb-exporter                  | repack          |  Y  | /mongodb_exporter                    | 9216                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| mongodb-opsmanager                | repack          |     | /opt/mongosh/bin/mongosh             | 27017                      | native   | cgr.dev/chainguard | 65532:65532           |                                     |
| mongodb                           | repack          |     | sh", "-c", "mongod                   | 27017                      | native   | cgr.dev/chainguard | 65532:65532           |                                     |
| mosquito                          | repack          |     | mosquitto_pub                        | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE                           |
| mosquitto-dev                     | repack          |     | mosquitto                            | 1883,9001                  | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| mosquitto                         | repack          |     | mosquitto                            | 1883,9001                  | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| mqtt                              | pkg-install     |     | mosquitto                            | 1883,9001                  | http/tcp | cgr.dev/chainguard | mosquitto             |                                     |
| musl                              | unknown         |     | NONE                                 | -                          | NONE     | cgr.dev/chainguard | 65532:65532           | NO_ENTRYPOINT,NO_EXPOSE,HEALTHCH... |
| mysql-8-exporter                  | repack          |  Y  | /mysqld_exporter                     | 9104                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| mysql-8                           | repack          |     | mysqld                               | 3306,33060                 | native   | cgr.dev/chainguard | 65532:65532           | WRONG_BASE                          |
| mysql-anonymizer                  | repack          |  Y  | python3", "/app/anonymize.py         | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| mysql-backup                      | repack          |     | /app/backup.sh                       | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE,WRONG_BASE                |
| mysql-exporter                    | binary-download |  Y  | /mysqld_exporter                     | 9104                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| mysql-init                        | repack          |     | /app/init.sh                         | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE,WRONG_BASE                |
| mysql-restore                     | repack          |     | /app/restore.sh                      | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE,WRONG_BASE                |
| mysql                             | repack          |     | sh", "-c", "mariadbd                 | 3306                       | native   | cgr.dev/chainguard | 65532:65532           |                                     |
| mysqld-exporter                   | binary-download |  Y  | /mysqld_exporter                     | 9104                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| mythtv                            | pkg-install     |     | mythbackend                          | 6543                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| n8n-nodes                         | repack          |     | node                                 | 5679                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| n8n-webhook                       | repack          |     | node                                 | 5678                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| n8n                               | pkg-install     |     | node                                 | 5678                       | http/tcp | cgr.dev/chainguard | node                  |                                     |
| nats                              | binary-download |  Y  | /nats-server                         | 4222,8222                  | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| navidrome-sqlite                  | binary-download |  Y  | /navidrome                           | 4533                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| navidrome                         | binary-download |  Y  | /navidrome                           | 4533                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| neo4j                             | binary-download |     | neo4j                                | 7474,7687                  | http/tcp | cgr.dev/chainguard | neo4j                 |                                     |
| neptune                           | pkg-install     |     | /app/neptune                         | 8182,8443                  | http/tcp | cgr.dev/chainguard | 65532:65532           | BLOATED                             |
| netbird                           | binary-download |  Y  | /netbird                             | 443,80                     | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| netclient                         | repack          |     | /netclient                           | 443                        | NONE     | scratch            | 65532:65532           |                                     |
| netmaker-ui                       | repack          |     | sleep", "infinity                    | 8080                       | NONE     | gcr.io/distroless/ | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| netmaker                          | binary-download |  Y  | /netmaker                            | 443,8080                   | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| newsboat                          | pkg-install     |     | newsboat                             | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE                           |
| nextcloud-alpine                  | repack          |     | php-8.4-fpm                          | 80,443                     | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| nextcloud-external                | repack          |     | php-8.4-fpm                          | 80,443                     | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| nextcloud-imaging                 | repack          |     | php-8.4-fpm                          | 80,443                     | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| nextcloud-nginx                   | repack          |     | php-8.4-fpm                          | 80,443                     | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| nextcloud-ocis                    | repack          |     | /nextcloud-ocis                      | 9200                       | NONE     | scratch            | 65532:65532           |                                     |
| nextcloud                         | binary-download |     | php-8.4-fpm                          | 80,443                     | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| nginx-exporter                    | binary-download |  Y  | /nginx_exporter                      | 9113                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| nginx-ingress-controller          | source-build    |  Y  | /nginx-ingress-controller            | 80,443,8443                | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| nginx-ingress                     | binary-download |  Y  | /nginx                               | 80,443                     | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| nginx-modsec                      | pkg-install     |     | nginx                                | 80,443                     | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| nginx-stream                      | binary-download |  Y  | /nginx                               | 80,443                     | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| nginx-unprivileged                | binary-download |  Y  | /nginx                               | 8080,8443                  | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| nginx                             | binary-download |  Y  | /nginx                               | 80,443                     | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| nifi-registry                     | repack          |     | /opt/nifi-registry/bin/nifi-registr  | 18080                      | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| node-alpine                       | binary-download |  Y  | node                                 | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| node-distroless                   | binary-download |  Y  | node                                 | -                          | NONE     | gcr.io/distroless/ | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE,H... |
| node-exporter                     | binary-download |  Y  | /node_exporter                       | 9100                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| node-red                          | source-build    |     | node", "/app/src/packages/node_modu  | 1880                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| node                              | repack          |     | node                                 | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE                           |
| npm-audit                         | repack          |     | npm                                  | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE                           |
| ntfy                              | repack          |     | /usr/local/bin/ntfy                  | 80                         | NONE     | scratch            | 65532:65532           |                                     |
| oauth2-proxy                      | binary-download |  Y  | /oauth2-proxy                        | 80,443                     | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| objectrocket                      | pkg-install     |     | /app/objectrocket                    | 27017                      | http/tcp | cgr.dev/chainguard | 65532:65532           | BLOATED                             |
| ocis                              | binary-download |     | /ocis                                | 9200                       | NONE     | scratch            | 65532:65532           |                                     |
| ocserv                            | repack          |     | /usr/sbin/ocserv                     | 443,443                    | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| ol_fileshare                      | pkg-install     |     | NONE                                 | 445,139                    | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_ENTRYPOINT                       |
| ollama                            | binary-download |  Y  | /ollama                              | 11434                      | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| onlyoffice-communityserver        | repack          |     | /opt/onlyoffice/onlyoffice-enterpri  | 80,443                     | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| onlyoffice-controlpanel           | repack          |     | /opt/onlyoffice/controlpanel/start.  | 80,443                     | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| open-webui-api                    | repack          |     | node                                 | 8080                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| open-webui                        | repack          |     | node                                 | 8080                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| opengpts                          | pkg-install     |     | python3                              | 8000                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| openhab                           | binary-download |     | /openhab/start.sh                    | 8080,8443                  | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| openjdk-alpine                    | binary-download |     | java                                 | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE                           |
| openjdk                           | binary-download |     | java                                 | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE                           |
| openjre                           | binary-download |     | NONE                                 | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_ENTRYPOINT,NO_EXPOSE             |
| openldap-backup                   | pkg-install     |     | /usr/sbin/slapcat                    | -                          | NONE     | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE,HEALTHCHECK_NONE_NON_S... |
| openldap-lambda                   | pkg-install     |     | /usr/bin/ldapsearch                  | -                          | NONE     | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE,HEALTHCHECK_NONE_NON_S... |
| openldap                          | pkg-install     |     | slapd                                | 389,636                    | http/tcp | cgr.dev/chainguard | ldap                  |                                     |
| openproject                       | pkg-install     |     | bundle", "exec", "rails", "server",  | 3000                       | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| opensearch-dashboards             | binary-download |     | opensearch-dashboards                | 5601                       | http/tcp | cgr.dev/chainguard | opensearch-dashboards |                                     |
| opensearch-operator               | repack          |     | /usr/local/bin/opensearch-operator   | 8080,8443                  | NONE     | scratch            | 65532:65532           |                                     |
| opensearch                        | binary-download |  Y  | sh", "-c", "/opt/opensearch/bin/ope  | 9200,9300                  | NONE     | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,HEALTHCHECK... |
| openvpn-as                        | binary-download |  Y  | /usr/local/openvpn_as/scripts/ovpn-  | 443,943,1194,9453          | NONE     | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,BLOATED,HEA... |
| openvpn                           | repack          |     | /usr/local/bin/openvpn               | 1194                       | http/tcp | cgr.dev/chainguard | appuser               |                                     |
| organizer                         | pkg-install     |     | php-fpm83                            | 80                         | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| outline                           | pkg-install     |     | node                                 | 3000                       | http/tcp | cgr.dev/chainguard | outline               |                                     |
| oxidized                          | pkg-install     |     | sleep", "infinity                    | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE                           |
| packetbeat                        | binary-download |  Y  | /opt/packetbeat/packetbeat           | 5066                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| pairdrop-server                   | source-build    |     | node", "server.js                    | 3000                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| pairdrop                          | binary-download |  Y  | /pairdrop                            | 80                         | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| paperless-ngx-gotenberg           | pkg-install     |     | python", "-m", "paperless-ngx        | -                          | http/tcp | debian             | 65532:65532           | NO_EXPOSE                           |
| paperless-ngx-ocr                 | pkg-install     |     | python", "-m", "paperless-ngx        | -                          | http/tcp | debian             | 65532:65532           | NO_EXPOSE                           |
| paperless-ngx-tika                | pkg-install     |     | python", "-m", "paperless-ngx        | -                          | http/tcp | debian             | 65532:65532           | NO_EXPOSE                           |
| paperless-ngx                     | repack          |  Y  | paperless                            | 8000                       | http/tcp | registry.access.re | 65532:65532           | PLACEHOLDER_FALLBACK                |
| pdfarranger                       | pkg-install     |     | python", "-m", "pdfarranger          | -                          | http/tcp | debian             | 65532:65532           | NO_EXPOSE                           |
| pdfmixer                          | pkg-install     |     | python", "-m", "pdfmixer             | -                          | http/tcp | debian             | 65532:65532           | NO_EXPOSE                           |
| perscache                         | source-build    |  Y  | /usr/local/bin/perscache             | 8429                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| pgbouncer-exporter                | repack          |  Y  | /pgbouncer_exporter                  | 9127                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| pgbouncer                         | pkg-install     |     | pgbouncer                            | 6432                       | http/tcp | cgr.dev/chainguard | pgbouncer             |                                     |
| pgpool-ii                         | pkg-install     |     | pgpool                               | 9999                       | http/tcp | cgr.dev/chainguard | pgpool                |                                     |
| photoprism-bin                    | repack          |  Y  | /photoprism                          | 2282                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| photoprism-frontend               | repack          |     | node                                 | 2283                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| photoprism                        | repack          |     | /opt/photoprism                      | 2282                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| photoshow                         | binary-download |     | php", "-S", "0.0.0.0:8080", "-t", "  | 8080                       | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| photoview                         | repack          |     | /photoview                           | 80                         | NONE     | scratch            | 65532:65532           |                                     |
| php-apache                        | pkg-install     |     | apache2ctl                           | 80                         | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| php-fpm                           | pkg-install     |     | php-fpm                              | 9000                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| php                               | pkg-install     |     | php                                  | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE                           |
| pi-hole                           | binary-download |  Y  | /usr/local/bin/pihole                | 53,53                      | NONE     | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,HEALTHCHECK... |
| pihole-ftl                        | binary-download |  Y  | /pihole-FTL                          | 53,53                      | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,WRONG_BASE     |
| pinecone                          | pkg-install     |     | python3                              | 8080                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| pinned-search                     | source-build    |  Y  | /usr/local/bin/pinned-search         | 8080                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| piper                             | binary-download |  Y  | /piper                               | 6666                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| piwigo                            | pkg-install     |     | php                                  | 80                         | http/tcp | cgr.dev/chainguard | www-data              |                                     |
| planka                            | pkg-install     |     | node                                 | 3000                       | http/tcp | cgr.dev/chainguard | planka                |                                     |
| plex                              | repack          |     | /usr/lib/plexmediaserver/Plex Media  | 32400                      | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| pm2                               | repack          |     | node                                 | 0                          | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| portainer                         | binary-download |  Y  | /portainer                           | 9000                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| postfix-constrained               | repack          |     | postfix", "-c", "/etc/postfix", "st  | 25                         | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| postfix-relay                     | repack          |     | postfix", "-c", "/etc/postfix", "st  | 25,587                     | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| postfix                           | repack          |     | postfix                              | 25                         | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| postgis                           | repack          |     | postgres                             | 5432                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| postgres-backup                   | repack          |     | /app/backup.sh                       | -                          | http/tcp | cgr.dev/chainguard | is                    | NO_EXPOSE,WRONG_BASE                |
| postgres-exporter                 | binary-download |  Y  | /postgres_exporter                   | 9187                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| postgres-operator                 | repack          |     | /usr/local/bin/postgres-operator     | 8080,8443                  | NONE     | scratch            | 65532:65532           |                                     |
| postgres-restore                  | repack          |     | /app/restore.sh                      | -                          | http/tcp | cgr.dev/chainguard | is                    | NO_EXPOSE,WRONG_BASE                |
| postgres                          | repack          |     | postgres                             | 5432                       | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| postgresql-14                     | repack          |     | postgres                             | 5432                       | native   | cgr.dev/chainguard | 65532:65532           |                                     |
| postgresql-15                     | repack          |     | postgres                             | 5432                       | native   | cgr.dev/chainguard | 65532:65532           |                                     |
| postgresql-16                     | repack          |     | postgres                             | 5432                       | native   | cgr.dev/chainguard | 65532:65532           |                                     |
| postgresql-17                     | repack          |  Y  | /usr/local/bin/docker-entrypoint.sh  | 5432                       | native   | cgr.dev/chainguard | 5432:5432             | PLACEHOLDER_FALLBACK,WRONG_BASE     |
| postgresql-anonymizer             | repack          |  Y  | python3", "-m", "postgresql_anonymi  | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| postgresql-exporter               | binary-download |  Y  | /postgres_exporter                   | 9187                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| postgresql-init                   | repack          |     | /app/init.sh                         | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE,WRONG_BASE                |
| postgresql-patroni                | repack          |     | python3", "-m", "patroni             | 8008,5432                  | native   | registry.access.re | 65532:65532           |                                     |
| postgresql                        | repack          |     | sh", "-c", "postgres                 | 5432                       | native   | cgr.dev/chainguard | 65532:65532           |                                     |
| postgrey                          | repack          |     | postgrey                             | 10023                      | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| powerdns                          | pkg-install     |     | pdns                                 | 53,8081                    | http/tcp | cgr.dev/chainguard | appuser               |                                     |
| pptpd                             | repack          |     | /usr/sbin/pptpd                      | 1723                       | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| privatebin-nginx                  | source-build    |     | php-8.4-fpm                          | 80                         | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| privatebin                        | pkg-install     |     | php                                  | 80                         | http/tcp | cgr.dev/chainguard | www-data              |                                     |
| prometheus-alertmanager           | binary-download |  Y  | /alertmanager                        | 9093                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| prometheus-aws-exporter           | binary-download |  Y  | /yace                                | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| prometheus-blackbox-exporter      | binary-download |  Y  | /blackbox_exporter                   | 9115                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| prometheus-consul-exporter        | binary-download |  Y  | /consul_exporter                     | 9107                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| prometheus-elasticsearch-exporter | binary-download |  Y  | /elasticsearch_exporter              | 9214                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| prometheus-haproxy-exporter       | binary-download |  Y  | /haproxy_exporter                    | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| prometheus-kafka-exporter         | binary-download |  Y  | /kafka_exporter                      | 9308                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| prometheus-mysqld-exporter        | binary-download |  Y  | /mysqld_exporter                     | 9104                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| prometheus-nginx-exporter         | binary-download |  Y  | /nginx-prometheus-exporter           | 9113                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| prometheus-node-exporter          | binary-download |  Y  | /node_exporter                       | 9100                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| prometheus-operator               | repack          |     | /usr/local/bin/prometheus-operator   | -                          | NONE     | scratch            | 65532:65532           | NO_EXPOSE                           |
| prometheus-postgres-exporter      | binary-download |  Y  | /postgres_exporter                   | 9187                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| prometheus-pushgateway            | binary-download |  Y  | /pushgateway                         | 9091                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| prometheus-snmp-exporter          | binary-download |  Y  | /snmp_exporter                       | 9116                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| prometheus-statsd-exporter        | binary-download |  Y  | /statsd_exporter                     | 9102,9125                  | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| prometheus-x509-exporter          | binary-download |  Y  | /x509-certificate-exporter           | 9793                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| prometheus                        | binary-download |  Y  | /prometheus                          | 9090                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| promtail-agent                    | binary-download |  Y  | /usr/bin/promtail                    | 9080,3100                  | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| promtail                          | binary-download |  Y  | /usr/bin/promtail                    | 9080,3100                  | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| promxy                            | repack          |     | /promxy                              | 8082                       | NONE     | scratch            | 65532:65532           |                                     |
| prowlarr-develop                  | binary-download |  Y  | /app/Prowlarr                        | 9696                       | http/tcp | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK                |
| prowlarr                          | binary-download |     | /app/Prowlarr                        | 9696                       | NONE     | cgr.dev/chainguard | 65532:65532           | WRONG*BASE,HEALTHCHECK_NONE_NON*... |
| pulsar-functions                  | binary-download |     | /opt/pulsar/bin/pulsar               | 8080                       | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| pulsar-proxy                      | binary-download |     | /opt/pulsar/bin/pulsar               | 6650,8080                  | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| pulsar                            | repack          |     | NONE                                 | 6650,8080                  | NONE     | scratch            | pulsar                | NO_ENTRYPOINT                       |
| pydio                             | repack          |     | php-8.4-fpm                          | 80,443                     | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| python-alpine                     | pkg-install     |     | sleep", "infinity                    | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE                           |
| python-slim                       | pkg-install     |     | sleep", "infinity                    | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE                           |
| python                            | repack          |     | python3                              | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE                           |
| pytorch                           | pkg-install     |     | python3                              | 8080                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| qbitmanage                        | pkg-install     |     | python3                              | 8080                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| qbittorrent                       | pkg-install     |     | qbittorrent-nox                      | 8080                       | http/tcp | cgr.dev/chainguard | qbittorrent           |                                     |
| qdrant-cpu                        | binary-download |  Y  | /qdrant                              | 6333                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| qdrant                            | binary-download |  Y  | /qdrant                              | 6333,6334                  | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| questdb-python                    | repack          |     | python", "-m", "questdb              | -                          | http/tcp | registry.access.re | 65532:65532           | NO_EXPOSE                           |
| questdb                           | repack          |  Y  | /opt/questdb/bin/questdb.sh", "star  | 9000,8812,9009             | http/tcp | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK                |
| r2c-bench                         | pkg-install     |     | python3                              | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE                           |
| rabbitmq-exporter                 | repack          |  Y  | /rabbitmq_exporter                   | 9090                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| rabbitmq-management               | binary-download |  Y  | rabbitmq-server                      | 5672,15672,15692           | generic  | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK                |
| rabbitmq                          | repack          |     | /usr/local/bin/docker-entrypoint.sh  | 5672,15672                 | generic  | cgr.dev/chainguard | 65532:65532           |                                     |
| radarr-develop                    | binary-download |  Y  | /app/Radarr                          | 7878                       | http/tcp | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK                |
| radarr                            | binary-download |     | /app/Radarr                          | 7878                       | NONE     | cgr.dev/chainguard | 65532:65532           | WRONG*BASE,HEALTHCHECK_NONE_NON*... |
| rainloop                          | repack          |     | httpd                                | 8888                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| rblake                            | pkg-install     |     | python3                              | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE                           |
| rclone-browser                    | repack          |     | node                                 | 8080                       | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| rclone                            | binary-download |  Y  | /rclone                              | 5572                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| readarr                           | binary-download |  Y  | /app/Readarr                         | 8787                       | http/tcp | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK                |
| redash                            | repack          |  Y  | redash", "server                     | 5000                       | http/tcp | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK                |
| redis-6                           | repack          |     | redis                                | 6379                       | native   | cgr.dev/chainguard | 65532:65532           |                                     |
| redis-7                           | repack          |     | /usr/local/bin/docker-entrypoint.sh  | 6379                       | native   | cgr.dev/chainguard | 65532:65532           |                                     |
| redis-cluster                     | binary-download |     | /usr/local/bin/redis", "--cluster-e  | 6379,16379                 | native   | cgr.dev/chainguard | 65532:65532           |                                     |
| redis-exporter                    | binary-download |  Y  | /redis_exporter                      | 9121                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| redis-insight                     | binary-download |     | /opt/redisinsight/redisinsight       | 8001                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| redis-sentinel                    | binary-download |     | /usr/local/bin/redis", "--sentinel   | 26379                      | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| redis-vert                        | pkg-install     |     | redis-server                         | 6379                       | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| redis                             | repack          |     | sh", "-c", "redis                    | 6379                       | native   | cgr.dev/chainguard | 65532:65532           |                                     |
| redis7                            | pkg-install     |     | redis                                | 6379                       | NONE     | cgr.dev/chainguard | redis:redis           | HEALTHCHECK_NONE_NON_SCRATCH        |
| redismodules                      | pkg-install     |  Y  | redis-server                         | 6379                       | native   | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK                |
| redmine                           | pkg-install     |     | bundle", "exec", "rails", "server",  | 3000                       | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| rekor                             | binary-download |  Y  | /rekor-server                        | 3000                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| renovate                          | repack          |     | renovate                             | -                          | NONE     | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE,HEALTHCHECK_NONE_NON_S... |
| renovatebot                       | repack          |     | renovate                             | -                          | NONE     | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE,HEALTHCHECK_NONE_NON_S... |
| repo-security                     | pkg-install     |     | NONE                                 | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_ENTRYPOINT,NO_EXPOSE             |
| repo-supervisor                   | pkg-install     |     | NONE                                 | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_ENTRYPOINT,NO_EXPOSE             |
| restic                            | binary-download |  Y  | /restic                              | 8000                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| rkhunter                          | repack          |     | rkhunter                             | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE                           |
| rmilter                           | source-build    |  Y  | /usr/local/bin/rmilter               | 6379                       | http/tcp | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK                |
| rocketmq                          | binary-download |  Y  | /opt/rocketmq/bin/mqnamesrv          | 9876,10911,10909           | NONE     | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,HEALTHCHECK... |
| roundcube                         | repack          |     | php-fpm83                            | 8888                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| rowy                              | repack          |     | node                                 | 3000                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| rqlite                            | binary-download |     | /usr/local/bin/rqlited               | 4001,4002                  | NONE     | scratch            | 65532:65532           |                                     |
| rspamd                            | repack          |     | rspamd                               | 11333,11334                | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| rss2                              | binary-download |     | php", "-S", "0.0.0.0:8080", "-t", "  | 8080                       | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| rss2email                         | pkg-install     |     | r2e                                  | 8080                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| rsyslog                           | repack          |  Y  | /usr/sbin/rsyslogd                   | 514,514                    | NONE     | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,HEALTHCHECK... |
| ruby                              | repack          |     | ruby                                 | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE                           |
| rust-static-arm                   | repack          |     | /opt/rust/bin/rustc                  | -                          | NONE     | scratch            | 65532:65532           | NO_EXPOSE                           |
| rust-static                       | repack          |     | /opt/rust/bin/rustc                  | -                          | NONE     | scratch            | 65532:65532           | NO_EXPOSE                           |
| rust                              | repack          |     | rust                                 | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE                           |
| s3                                | binary-download |  Y  | /s3-server                           | 9000,9001                  | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| sbt                               | binary-download |     | sbt                                  | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE                           |
| scrapyd                           | pkg-install     |     | scrapyd                              | 6800                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| scratch-base                      | repack          |     | NONE                                 | -                          | NONE     | scratch            | 65532:65532           | NO_ENTRYPOINT,NO_EXPOSE             |
| scratch                           | pkg-install     |     | NONE                                 | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_ENTRYPOINT,NO_EXPOSE             |
| scylladb                          | repack          |     | /usr/bin/scylla                      | 9042,9160,10000            | generic  | cgr.dev/chainguard | 65532:65532           | BLOATED                             |
| seafile-pro                       | pkg-install     |     | python", "-m", "seafile-pro          | -                          | http/tcp | debian             | 65532:65532           | NO_EXPOSE                           |
| seafile                           | pkg-install     |     | python", "-m", "seafile              | -                          | http/tcp | debian             | 65532:65532           | NO_EXPOSE                           |
| searx                             | repack          |  Y  | searx-run                            | 8888                       | http/tcp | registry.access.re | 65532:65532           | PLACEHOLDER_FALLBACK                |
| searxng-meta                      | repack          |  Y  | searxng-meta                         | 8888                       | http/tcp | registry.access.re | 65532:65532           | PLACEHOLDER_FALLBACK                |
| searxng                           | pkg-install     |     | python                               | 8080                       | http/tcp | cgr.dev/chainguard | searxng               |                                     |
| secrets-scanner                   | pkg-install     |     | NONE                                 | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_ENTRYPOINT,NO_EXPOSE             |
| secretz                           | pkg-install     |     | NONE                                 | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_ENTRYPOINT,NO_EXPOSE             |
| sentry-cron                       | repack          |     | sentry                               | 9000                       | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| sentry-worker                     | repack          |     | sentry                               | 9000                       | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| sentry                            | repack          |     | sentry                               | 9000                       | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| shh                               | pkg-install     |     | NONE                                 | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_ENTRYPOINT,NO_EXPOSE             |
| shield                            | binary-download |  Y  | /shield                              | 8443                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,WRONG_BASE     |
| sigal                             | pkg-install     |     | python3                              | 8000                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| singer                            | pkg-install     |     | python3                              | 8080                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| singlestore                       | pkg-install     |     | /app/singlestore                     | 3306,8080                  | http/tcp | cgr.dev/chainguard | 65532:65532           | BLOATED                             |
| skrooge                           | pkg-install     |     | skrooge                              | 8080                       | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| smartdns                          | source-build    |     | /usr/local/bin/smartdns              | 53,53                      | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| snmp-exporter                     | binary-download |  Y  | /snmp_exporter                       | 9116                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| snyk-agent                        | binary-download |  Y  | /usr/local/bin/snyk                  | -                          | NONE     | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE,H... |
| snyk-alpine                       | binary-download |  Y  | /snyk-alpine                         | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| snyk-docker                       | binary-download |  Y  | /snyk-docker                         | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| snyk-monitor                      | binary-download |  Y  | /snyk-monitor                        | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| snyk                              | binary-download |  Y  | /usr/local/bin/snyk                  | -                          | NONE     | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE,H... |
| softether                         | pkg-install     |     | vpnserver                            | 443,992,1194,500,4500,5555 | http/tcp | cgr.dev/chainguard | appuser               |                                     |
| sonarr-develop                    | binary-download |  Y  | /app/Sonarr                          | 8989                       | http/tcp | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK                |
| sonarr                            | binary-download |     | /app/Sonarr                          | 8989                       | NONE     | cgr.dev/chainguard | 65532:65532           | WRONG*BASE,HEALTHCHECK_NONE_NON*... |
| sonic                             | repack          |     | /sonic                               | 1491                       | NONE     | scratch            | 65532:65532           | WRONG_BASE                          |
| source-control                    | repack          |     | /usr/local/bin/gitea                 | 3000,22                    | http/tcp | cgr.dev/chainguard | 65532:65532           | BLOATED                             |
| spamassassin                      | repack          |     | spamassassin                         | 783                        | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| splunk-forwarder                  | binary-download |  Y  | /opt/splunkforwarder/bin/splunk      | 8089,9997                  | NONE     | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,HEALTHCHECK... |
| sql-ledger                        | pkg-install     |     | httpd", "-D", "FOREGROUND            | 80                         | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| sqlcipher                         | binary-download |     | /usr/local/bin/sqlcipher             | -                          | NONE     | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE,HEALTHCHECK_NONE_NON_S... |
| sqlite-browser                    | repack          |     | /usr/local/bin/sqlitebrowser         | -                          | NONE     | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE,HEALTHCHECK_NONE_NON_S... |
| sqlite-utils                      | pkg-install     |     | sqlite-utils                         | -                          | NONE     | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE,HEALTHCHECK_NONE_NON_S... |
| sqlite                            | pkg-install     |     | sqlite-libs                          | -                          | http/tcp | cgr.dev/chainguard | sqlite                | NO_EXPOSE                           |
| sqlpage                           | binary-download |     | /opt/sqlpage/sqlpage                 | 8080                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| sssd                              | pkg-install     |     | NONE                                 | 0                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_ENTRYPOINT                       |
| stable-diffusion-webui            | source-build    |     | python3", "/opt/stable-diffusion-we  | 7860                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| stable-diffusion                  | pkg-install     |     | python3                              | 7860                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| stalwart-bitnami                  | repack          |     | /usr/local/bin/stalwart              | 25,143,465,587,993         | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| stalwart                          | repack          |     | /usr/local/bin/stalwart              | 25,143,465,587,993         | NONE     | scratch            | 65532:65532           |                                     |
| standard                          | pkg-install     |     | NONE                                 | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_ENTRYPOINT,NO_EXPOSE             |
| static-c                          | repack          |     | NONE                                 | -                          | NONE     | scratch            | 65532:65532           | NO_ENTRYPOINT,NO_EXPOSE             |
| statping-ng                       | binary-download |  Y  | /statping                            | 8080                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| step-acme                         | binary-download |  Y  | /step-ca                             | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| step-ca                           | binary-download |  Y  | /step-ca                             | 9000                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| step-certificates                 | binary-download |  Y  | /step-ca                             | 9000                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| step-cli                          | binary-download |  Y  | /step                                | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| stirling-pdf-core                 | binary-download |  Y  | /opt/stirling-pdf-core/stirling-pdf  | 8080                       | NONE     | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,HEALTHCHECK... |
| stirling-pdf                      | binary-download |  Y  | /opt/stirling-pdf/stirling-pdf       | 8080                       | NONE     | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,HEALTHCHECK... |
| streamlink                        | pkg-install     |     | python", "-m", "streamlink           | -                          | http/tcp | debian             | 65532:65532           | NO_EXPOSE                           |
| subsonic                          | binary-download |     | java", "-jar", "/app/subsonic.war    | 4040                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| suitecrm                          | repack          |     | php-8.4-fpm                          | 80,443                     | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| surrealdb-python                  | repack          |     | python3", "-m", "surrealdb           | -                          | http/tcp | registry.access.re | 65532:65532           | NO_EXPOSE                           |
| surrealdb                         | binary-download |  Y  | /surreal                             | 8000,8001                  | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| syft-alpine                       | binary-download |  Y  | /syft                                | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| syft                              | binary-download |  Y  | /syft                                | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| synapse-media                     | pkg-install     |     | python3", "-m", "synapse.app.media\_ | 8008                       | http/tcp | debian             | 65532:65532           |                                     |
| synapse                           | repack          |  Y  | python3", "-m", "synapse.app.homese  | 8008,8448                  | NONE     | registry.access.re | 65532:65532           | PLACEHOLDER_FALLBACK,HEALTHCHECK... |
| syslog-ng                         | repack          |  Y  | /usr/sbin/syslog-ng                  | 514,514                    | NONE     | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,HEALTHCHECK... |
| taiga-backend                     | repack          |  Y  | python", "-m", "taiga                | 8000                       | NONE     | registry.access.re | 65532:65532           | PLACEHOLDER_FALLBACK,HEALTHCHECK... |
| taiga-front                       | source-build    |     | nginx", "-g", "daemon off;           | 80,443                     | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| taiga-protected                   | repack          |     | /venv/bin/python", "-m", "taiga_pro  | 8003                       | NONE     | registry.access.re | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| taiga                             | repack          |  Y  | python", "-m", "taiga_events         | 8888                       | NONE     | registry.access.re | 65532:65532           | PLACEHOLDER_FALLBACK,HEALTHCHECK... |
| tailscale                         | binary-download |  Y  | /tailscaled                          | 41641                      | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| tasmota                           | repack          |     | NONE                                 | -                          | http/tcp | registry.access.re | 65532:65532           | NO_ENTRYPOINT,NO_EXPOSE             |
| tautulli-py                       | source-build    |     | python3", "/opt/tautulli/Tautulli.p  | 8181                       | NONE     | registry.access.re | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| tautulli                          | source-build    |     | python3", "/opt/tautulli/Tautulli.p  | 8181                       | NONE     | registry.access.re | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| tekton                            | binary-download |  Y  | /tekton                              | 9090                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| telegraf                          | binary-download |     | /usr/bin/telegraf                    | 8125,8092,8094             | NONE     | scratch            | 65532:65532           |                                     |
| tempo                             | binary-download |  Y  | /tempo                               | 3200                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| tensor                            | pkg-install     |     | tensorboard                          | 6006                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| tensorboard                       | pkg-install     |     | tensorboard                          | 6006                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| tensorflow                        | pkg-install     |     | python3                              | 8080                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| text-gen-ui                       | repack          |     | node                                 | 7860                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| text-generation-webui             | source-build    |     | python3", "/opt/text-generation-web  | 7860                       | http/tcp | cgr.dev/chainguard | user                  |                                     |
| thanos-bucket                     | binary-download |  Y  | /thanos                              | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| thanos-querier                    | binary-download |  Y  | /thanos                              | 10902                      | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| thanos-receive                    | binary-download |  Y  | /thanos                              | 10902                      | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| thanos-rule                       | binary-download |  Y  | /thanos                              | 10902                      | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| thanos-store                      | binary-download |  Y  | /thanos                              | 10902                      | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| thanos                            | binary-download |  Y  | /thanos                              | 10902                      | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| tig                               | binary-download |     | /usr/local/bin/tig                   | -                          | NONE     | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE,BLOATED,HEALTHCHECK_NO... |
| timescaledb                       | repack          |     | postgres                             | 5432                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| tinytinyrss                       | pkg-install     |     | php                                  | 80                         | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| tooljet-client                    | repack          |     | node                                 | 8080                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| tooljet-server                    | repack          |     | node                                 | 3000                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| tooljet                           | repack          |     | node                                 | 8080                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| traefik-cloud                     | binary-download |  Y  | /traefik                             | 80,443,8080                | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| traefik-crypto                    | binary-download |  Y  | /traefik                             | 80,443                     | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| traefik-dashboard                 | binary-download |  Y  | /traefik                             | 8080                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| traefik-hub                       | binary-download |  Y  | /traefik                             | 80,443                     | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| traefik-metrics                   | binary-download |  Y  | /traefik                             | 8080                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| traefik-mirror                    | binary-download |  Y  | /traefik                             | 80,443                     | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| traefik-plugin-auth               | binary-download |  Y  | /traefik                             | 80                         | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| traefik-plugin-csrf               | binary-download |  Y  | /traefik                             | 80                         | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| traefik-v2                        | binary-download |  Y  | /traefik                             | 80,443,8080                | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| traefik-wss                       | binary-download |  Y  | /traefik                             | 80,443                     | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| traefik                           | binary-download |  Y  | /traefik                             | 80,443,8080                | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| transfer.sh                       | binary-download |  Y  | /transfer.sh                         | 8080                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| transferhelper                    | pkg-install     |     | echo                                 | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_EXPOSE                           |
| transformers-gpu                  | pkg-install     |     | python3                              | 8000                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| transformers                      | pkg-install     |     | python3                              | 8000                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| transmission                      | pkg-install     |     | transmission-daemon                  | 9091                       | http/tcp | cgr.dev/chainguard | transmission          |                                     |
| trino                             | repack          |  Y  | /opt/trino/bin/launcher", "run       | 8080                       | http/tcp | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,BLOATED        |
| trivy-alpine                      | binary-download |  Y  | /trivy                               | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| trivy-iac                         | binary-download |  Y  | /trivy                               | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| trivy-k8s                         | binary-download |  Y  | /trivy                               | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| trivy-operator                    | binary-download |  Y  | /trivy-operator                      | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| trivy                             | binary-download |  Y  | /trivy                               | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| truffelsh                         | binary-download |  Y  | /trufflehog                          | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| trufflehog                        | binary-download |  Y  | /trufflehog                          | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| truffleshog                       | binary-download |  Y  | /trufflehog                          | -                          | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK,NO_EXPOSE      |
| tryton                            | pkg-install     |     | python", "-m", "trytond              | -                          | http/tcp | debian             | 65532:65532           | NO_EXPOSE                           |
| tt-rss                            | pkg-install     |     | php                                  | 80                         | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| tts                               | pkg-install     |     | python3                              | 5002                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| tvheadend                         | pkg-install     |     | tvheadend                            | 9981                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| typesense-js                      | pkg-install     |     | node                                 | 8108                       | http/tcp | cgr.dev/chainguard | node                  |                                     |
| ulogger                           | source-build    |  Y  | ulogger                              | 8080                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| unbound-alpine                    | source-build    |  Y  | /usr/sbin/unbound                    | 53,53                      | NONE     | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK,HEALTHCHECK... |
| unbound-exporter                  | binary-download |  Y  | /unbound_exporter                    | 9167                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| unbound                           | source-build    |  Y  | /unbound                             | 53                         | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| unoconv                           | pkg-install     |     | unoconv                              | 8080                       | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| upstream                          | pkg-install     |     | NONE                                 | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_ENTRYPOINT,NO_EXPOSE             |
| uptime-kuma                       | pkg-install     |     | node                                 | 3001                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| valkey-cluster                    | repack          |     | ["valkey",                           | 6379,16379                 | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| valkey-exporter                   | binary-download |  Y  | /valkey-exporter                     | 9121                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| valkey                            | pkg-install     |     | sh", "-c", "valkey                   | 6379                       | generic  | cgr.dev/chainguard | 65532:65532           |                                     |
| vault-csi-provider                | repack          |     | /usr/local/bin/vault-csi-provider    | -                          | NONE     | scratch            | 65532:65532           | NO_EXPOSE                           |
| vault-secrets-operator            | repack          |     | /usr/local/bin/vault-secrets-operat  | -                          | NONE     | scratch            | 65532:65532           | NO_EXPOSE                           |
| vault-secrets                     | repack          |     | /vault-secrets-operator              | 8080,8443                  | NONE     | scratch            | 65532:65532           |                                     |
| vault                             | binary-download |  Y  | /vault                               | 8200,8201                  | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| vaultwarden-alpine                | repack          |     | /vaultwarden                         | 8080                       | NONE     | scratch            | 65532:65532           |                                     |
| vaultwarden-mysql                 | repack          |     | /usr/local/bin/vaultwarden           | 8080                       | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| vaultwarden-postgres              | repack          |     | /usr/local/bin/vaultwarden           | 8080                       | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| vaultwarden-sqlite                | repack          |     | /vaultwarden                         | 8080                       | NONE     | scratch            | 65532:65532           |                                     |
| vaultwarden                       | repack          |     | /vaultwarden                         | 8080                       | NONE     | scratch            | 65532:65532           |                                     |
| vecs-db                           | pkg-install     |     | python3                              | 8080                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| vector-init                       | binary-download |     | /usr/bin/vector                      | 8686                       | NONE     | scratch            | 65532:65532           |                                     |
| vector                            | binary-download |  Y  | /vector                              | 9001                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| vernemq                           | repack          |     | echo                                 | 1883,4369,44053,8080       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| victoria-logs                     | binary-download |  Y  | /victoria-logs-prod                  | 9428                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| victoriametrics-cluster           | binary-download |  Y  | /vmstorage                           | 8480                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| victoriametrics                   | binary-download |  Y  | /victoria-metrics                    | 8428                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| vikunja-api                       | binary-download |  Y  | /vikunja                             | 3456                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| vikunja-redis                     | binary-download |  Y  | /vikunja                             | 3456                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| vikunja                           | repack          |  Y  | /vikunja                             | 3456                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| virtuoso                          | binary-download |     | virtuoso-t", "-f", "-c", "/etc/virt  | 1111,8890                  | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| vllm                              | pkg-install     |     | python3                              | 8000                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| vm-agent                          | binary-download |  Y  | /vmagent                             | 8429                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| vmalert                           | binary-download |  Y  | /vmalert-prod                        | 8880                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| vpn-controller                    | binary-download |     | /app/vpn-controller                  | 51820,51820                | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| vtigercrm                         | repack          |     | php-8.4-fpm                          | 80,443                     | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| wandb-server                      | pkg-install     |     | wandb                                | 8080                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| watchtower                        | binary-download |  Y  | /watchtower                          | 8080                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| weaviate-python                   | pkg-install     |     | python3                              | 8080                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| weaviate                          | pkg-install     |     | /opt/weaviate                        | 8080                       | http/tcp | cgr.dev/chainguard | weaviate              |                                     |
| weights-biases                    | pkg-install     |     | python3                              | 8080                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| wg-quick                          | repack          |     | /usr/bin/wg-quick                    | 51820                      | NONE     | cgr.dev/chainguard | 65532:65532           | HEALTHCHECK_NONE_NON_SCRATCH        |
| whisparr                          | binary-download |  Y  | /app/Whisparr                        | 6969                       | http/tcp | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK                |
| whisper                           | pkg-install     |     | python3                              | 8080                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| whoogle-search                    | repack          |  Y  | whoogle-search                       | 5000                       | http/tcp | registry.access.re | 65532:65532           | PLACEHOLDER_FALLBACK                |
| whoogle                           | repack          |  Y  | whoogle-search                       | 5000                       | http/tcp | registry.access.re | 65532:65532           | PLACEHOLDER_FALLBACK                |
| wireguard-ui                      | binary-download |  Y  | /wireguard-ui                        | 8080                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| wireguard                         | source-build    |  Y  | /wireguard-go                        | 51820                      | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| wled                              | repack          |     | NONE                                 | -                          | http/tcp | registry.access.re | 65532:65532           | NO_ENTRYPOINT,NO_EXPOSE             |
| wolfi-gcc                         | source-build    |     | NONE                                 | -                          | NONE     | cgr.dev/chainguard | -                     | NO*ENTRYPOINT,NO_EXPOSE,MISSING*... |
| wolfi-jdk                         | pkg-install     |     | NONE                                 | -                          | NONE     | cgr.dev/chainguard | -                     | NO*ENTRYPOINT,NO_EXPOSE,MISSING*... |
| wolfi-node                        | pkg-install     |     | NONE                                 | -                          | NONE     | cgr.dev/chainguard | -                     | NO*ENTRYPOINT,NO_EXPOSE,MISSING*... |
| wolfi-python                      | pkg-install     |     | NONE                                 | -                          | NONE     | cgr.dev/chainguard | -                     | NO*ENTRYPOINT,NO_EXPOSE,MISSING*... |
| woodpecker-agent                  | repack          |     | /usr/local/bin/woodpecker-agent      | 3000                       | NONE     | scratch            | 65532:65532           |                                     |
| woodpecker-ci                     | repack          |     | /usr/local/bin/woodpecker-server     | 8000                       | NONE     | scratch            | 65532:65532           |                                     |
| woodpecker-server                 | repack          |     | /usr/local/bin/woodpecker-server     | 8000                       | NONE     | scratch            | 65532:65532           |                                     |
| x86_64-unknown-linux-musl         | source-build    |     | NONE                                 | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_ENTRYPOINT,NO_EXPOSE             |
| yarn                              | repack          |     | node                                 | 0                          | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| yarr                              | repack          |  Y  | /yarr                                | 7070                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| zenphoto                          | pkg-install     |     | php                                  | 80                         | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| zeromq                            | source-build    |     | NONE                                 | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_ENTRYPOINT,NO_EXPOSE,WRONG_BASE  |
| zerotier                          | repack          |     | /usr/sbin/zerotier-one               | 9993                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| zfs-exporter                      | binary-download |  Y  | /zfs-exporter                        | 9134                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| zigbee2mqtt                       | source-build    |     | node", "index.js                     | 8080                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| zipkin                            | binary-download |     | java                                 | 9411                       | http/tcp | cgr.dev/chainguard | 65532:65532           |                                     |
| zipline                           | source-build    |  Y  | node", "server.js                    | 8080                       | http/tcp | cgr.dev/chainguard | 65532:65532           | PLACEHOLDER_FALLBACK                |
| zitadel                           | binary-download |  Y  | /zitadel                             | 8080                       | NONE     | scratch            | 65532:65532           | PLACEHOLDER_FALLBACK                |
| zoe                               | pkg-install     |     | NONE                                 | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_ENTRYPOINT,NO_EXPOSE             |
| zzh                               | pkg-install     |     | NONE                                 | -                          | http/tcp | cgr.dev/chainguard | 65532:65532           | NO_ENTRYPOINT,NO_EXPOSE             |

---

## 8. Detailed Findings by Issue Category

### PLACEHOLDER_FALLBACK (337 images)

- **activemq** (v5.18.3)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **adguard-dns** (v0.107.50)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **adguardhome** (v0.107.74)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **adguardhome-lite** (v0.107.50)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **age** (v1.3.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **alertmanager** (v0.27.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **arango** (v3.12.2)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **arangodb** (v3.12.4)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **argo-cd** (v3.4.2)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **argo-rollouts** (v1.9.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **argocd-redis** (v7.2.4)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **auditbeat** (v9.4.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **authelia** (v4.39.19)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **authelia-lite** (v4.39.19)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **awslogs** (v0.15.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **azurelogs** (v1.2.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **badger** (v4.2.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **basic-auth-proxy**
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **beancount** (v2.3.6)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **betteruptime** (v0.2.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **bind** (v9.21.21)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **bind-exporter** (v0.7.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **blackbox-exporter** (vv0.26.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **blocky** (v0.29.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **buildx** (v0.33.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **caddy** (v2.11.3)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **caddy-alpine** (v2.8.4)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **caddy-fileserver** (v2.7.6)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **caddy-reverseproxy** (v2.7.6)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **caddy-wildcard** (v2.7.6)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **cadvisor** (v0.49.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **cargo-audit**
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **cassandra-operator** (v1.20.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **cayley** (v0.7.7)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **certificates** (v1.6.5)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **chartdb** (vv1.20.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **checkov**
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **checkov-k8s**
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **cloudflare-ddns** (v1.16.2)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **cloudflare-warrior** (v2026.5.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **cloudflared** (v2026.3.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **cloudreve** (v3.8.3)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **cockroachdb** (v24.3.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **cockroachdb-exporter** (v23.2.3)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **cockroachdb-sql** (v23.2.3)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **composer** (v2.8.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **conan-audit**
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **conduit** (v0.4.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **conduit-admin** (v0.4.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **consul** (v1.18.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **consul-exporter** (v0.4.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **consul-template** (v0.37.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **coredns** (v1.12.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **coredns-alpine** (v1.11.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **cors-proxy**
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **cortex** (v1.17.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **cosign** (v3.0.6)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **cosign-verify** (v3.0.6)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **couchbase**
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **couchbase-operator** (v2.8.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **couchdb** (v3.5.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **crane** (v0.21.5)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **crate** (v5.9.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **crawlergo** (v0.4.4)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **crdb-init** (v23.2.3)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **ct-log** (v1.3.3)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **dashy** (v3.3.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **dnsmasq** (v2.90)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **docui**
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **dragonfly** (v1.18.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **dragonfly-client** (v1.18.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **duplicati** (v2.1.0.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **elasticsearch-8** (v8.12.2)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **elasticsearch-exporter** (v1.7.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **erpnext-worker** (v15)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **esphome**
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **esphome-daemon**
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **etcd** (v3.6.10)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **etcd-backup** (v3.6.10)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **etcd-empty** (v3.6.10)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **etcd-operator** (v3.6.10)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **falcosidekick**
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **filebeat** (v9.4.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **filebrowser** (vv2.32.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **filebrowser-alpine** (vv2.32.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **firefly-iii-importer** (v1.6.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **flux** (v2.3.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **flux2** (v2.8.6)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **fluxcd-helm** (v2.8.6)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **fluxcd-image** (v2.8.6)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **focalboard-server** (v7.11.3)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **forgejo** (v12.0.3)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **fulcio** (v1.8.5)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **gcplogs** (v3.10.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **ggshield**
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **gitguardian**
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **gitleaks**
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **go-static** (v1.22.10)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **gogs** (v0.13.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **golang-alpine** (v1.22.10)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **golang-cache** (v1.0.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **gradle** (v8.10.2)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **grafana** (v12.2.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **grafana-dev** (v10.4.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **grafana-image-renderer** (v5.8.2)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **grafana-lite** (v10.4.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **grafana-oss** (v10.4.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **grafana-toolkit** (v10.4.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **graphile** (v4.14.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **graylog-sidecar** (v1.5.2)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **grype** (v0.80.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **grype-alpine**
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **hadolint** (v2.14.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **haproxy-exporter** (v0.15.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **hashicorp-vault** (v1.18.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **headscale** (v0.16.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **health-checks** (v1.0.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **healthcheck** (v0.4.36)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **heartbeat** (v9.4.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **helm** (v3.15.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **helmfile** (v0.162.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **helmsman** (v4.0.5)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **homebridge**
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **homebridge-camera**
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **ignite** (v2.16.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **immudb** (v1.11.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **influxdb-client** (v2.7.5)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **ipmi-exporter** (v1.10.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **it-tools** (v2024.10.22-7ca5933)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **jaeger** (v1.62.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **jaeger-agent** (v1.55.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **jaeger-collector** (v1.55.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **jaeger-query** (v1.55.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **jenkins-agent** (v3355.v388858a_47b_33)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **jenkins-executor** (v3355.v388858a_47b_33)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **jenkins-plugin** (v2.462.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **journalbeat** (v9.4.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **k3d** (v5.8.3)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **k3d-proxy** (v5.8.3)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **k3s** (v1.33.6+k3s1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **k3s-agent** (v1.33.6+k3s1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **k3s-server** (v1.33.6+k3s1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **kafka-exporter** (v1.9.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **kafka-ui** (v0.7.2)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **keycloak** (v26.6.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **keycloak-gatekeeper** (v9.1.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **keycloak-init** (v26.6.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **keycloak-quarkus** (v26.6.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **kibana** (v8.12.2)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **kibana-oss** (v8.12.2)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **kube-apiserver** (v1.30.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **kube-bench**
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **kube-controller** (v1.30.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **kube-hunter**
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **kube-proxy** (v1.30.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **kube-scheduler** (v1.30.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **kube-state-metrics** (v2.18.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **kubectl** (v1.30.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **kubescape**
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **kustomize** (v5.4.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **lazydocker**
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **lazydocker-ui**
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **linguist-go** (v9.5.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **llama-cpp-server** (vb5415)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **llama.cpp** (v${VERSION})
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **localai** (v4.1.3)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **loki** (v3.1.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **loki-canary** (v2.9.4)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **loki-simple** (v3.1.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **mattermost** (v11.6.2)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **maven** (v3.9.15)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **mc** (vRELEASE.2025-04-08T16-46-15Z)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **meilisearch** (v1.42.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **memcached-exporter** (v0.13.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **meshbird** (v2.3)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **metricbeat** (v9.4.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **mimir** (v2.10.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **miniflux-21** (v2.2.19)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **minio** (vRELEASE.2025-10-15T17-29-55Z)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **minio-operator** (vv6.0.4)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **mongo-exporter** (v0.40.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **mongodb-7** (v7.0.9)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **mongodb-community** (v7.0.9)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **mongodb-exporter** (v0.13.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **mysql-8-exporter** (v0.19.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **mysql-anonymizer** (v0.10.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **mysql-exporter** (v0.15.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **mysqld-exporter** (vv0.16.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **nats** (v2.12.7)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **navidrome** (v0.52.5)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **navidrome-sqlite** (v0.52.5)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **netbird** (v0.70.5)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **netmaker** (v1.5.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **nginx** (v1.27.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **nginx-exporter** (v1.1.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **nginx-ingress** (v1.27.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **nginx-ingress-controller** (v1.10.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **nginx-stream** (v1.27.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **nginx-unprivileged** (v1.27.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **node-alpine** (v22.12.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **node-distroless** (v22.12.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **node-exporter** (v1.8.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **oauth2-proxy** (v7.12.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **ollama** (v0.21.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **opensearch** (v2.12.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **openvpn-as** (v2.12.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **packetbeat** (v9.4.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **pairdrop** (v1.11.2)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **paperless-ngx** (v2.20.14)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **perscache** (v1.0.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **pgbouncer-exporter** (v0.12.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **photoprism-bin** (v260305-fad9d5395)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **pi-hole**
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **pihole-ftl** (v5.18.2)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **pinned-search** (v0.1.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **piper** (v1.2.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **portainer** (v2.20.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **postgres-exporter** (v0.17.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **postgresql-17** (v17.2)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **postgresql-anonymizer** (v1.2.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **postgresql-exporter** (v0.15.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **prometheus** (v2.53.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **prometheus-alertmanager** (v0.27.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **prometheus-aws-exporter** (v0.65.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **prometheus-blackbox-exporter** (v0.28.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **prometheus-consul-exporter** (v0.13.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **prometheus-elasticsearch-exporter** (v1.10.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **prometheus-haproxy-exporter** (v0.15.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **prometheus-kafka-exporter** (v1.9.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **prometheus-mysqld-exporter** (v0.19.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **prometheus-nginx-exporter** (v1.1.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **prometheus-node-exporter** (v1.8.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **prometheus-postgres-exporter** (v0.19.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **prometheus-pushgateway** (v1.8.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **prometheus-snmp-exporter** (v0.30.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **prometheus-statsd-exporter** (v0.29.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **prometheus-x509-exporter** (v3.9.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **promtail** (v3.5.12)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **promtail-agent** (v${VERSION})
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **prowlarr-develop** (v2.3.6.5351)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **qdrant** (v1.17.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **qdrant-cpu** (v1.17.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **questdb** (v7.3.10)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **rabbitmq-exporter** (v1.1.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **rabbitmq-management** (v3.13.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **radarr-develop** (v6.2.0.10390)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **rclone** (vv1.69.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **readarr** (v0.4.18.2805)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **redash** (v10.0.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **redis-exporter** (v1.68.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **redismodules** (v2.0.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **rekor** (v1.5.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **restic** (v0.17.3)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **rmilter** (v1.0.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **rocketmq** (v5.1.4)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **rsyslog** (v8.2312.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **s3** (vRELEASE.2025-10-15T17-29-55Z)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **searx**
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **searxng-meta**
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **shield** (v8.6.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **snmp-exporter** (v0.26.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **snyk** (v1.1300.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **snyk-agent** (v1.1300.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **snyk-alpine**
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **snyk-docker**
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **snyk-monitor**
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **sonarr-develop** (v4.0.17.2953)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **splunk-forwarder** (v9.2.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **statping-ng** (v0.90.74)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **step-acme** (v0.30.2)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **step-ca** (v0.30.2)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **step-certificates** (v0.30.2)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **step-cli** (v0.30.2)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **stirling-pdf** (v2.10.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **stirling-pdf-core** (v2.10.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **surrealdb** (v3.0.5)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **syft** (v1.8.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **syft-alpine**
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **synapse** (v1.152.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **syslog-ng** (v4.8.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **taiga** (v6.9.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **taiga-backend** (v6.9.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **tailscale** (v1.58.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **tekton** (v0.60.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **tempo** (v2.8.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **thanos** (v0.35.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **thanos-bucket** (v${VERSION})
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **thanos-querier** (v${VERSION})
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **thanos-receive** (v0.35.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **thanos-rule** (v${VERSION})
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **thanos-store** (v0.35.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **traefik** (v3.5.3)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **traefik-cloud** (v3.6.13)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **traefik-crypto** (v3.6.13)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **traefik-dashboard** (v3.6.13)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **traefik-hub** (v3.6.13)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **traefik-metrics** (v3.6.13)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **traefik-mirror** (v3.6.13)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **traefik-plugin-auth** (v3.6.13)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **traefik-plugin-csrf** (v3.6.13)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **traefik-v2** (v2.11.42)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **traefik-wss** (v3.6.13)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **transfer.sh**
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **trino** (v435)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **trivy** (v0.70.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **trivy-alpine**
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **trivy-iac**
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **trivy-k8s**
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **trivy-operator** (v0.30.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **truffelsh**
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **trufflehog**
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **truffleshog**
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **ulogger** (vlatest)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **unbound** (v1.20.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **unbound-alpine** (v1.19.3)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **unbound-exporter** (v0.6.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **valkey-exporter** (v1.58.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **vault** (v1.18.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **vector** (v0.39.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **victoria-logs** (vv1.50.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **victoriametrics** (v1.142.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **victoriametrics-cluster** (v1.97.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **vikunja** (v2.3.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **vikunja-api** (v2.3.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **vikunja-redis** (v2.3.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **vm-agent** (v1.140.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **vmalert** (v1.142.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **watchtower** (v1.7.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **whisparr** (v2.2.0-develop.115)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **whoogle** (v1.2.4)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **whoogle-search**
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **wireguard** (v1.0.20250521)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **wireguard-ui** (v0.5.4)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **yarr** (v2.4.0)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **zfs-exporter** (v0.0.12)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **zipline**
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails
- **zitadel** (v4.13.1)
  - Has fallback pattern: creates placeholder script with `sleep infinity` on download failure
  - Fix: Remove the `|| true` / fallback pattern; let the build fail explicitly if download fails

### NO_ENTRYPOINT (40 images)

- **aarch64-unknown-linux-musl**
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary
- **alpine**
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary
- **alpine-static**
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary
- **amd64**
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary
- **arm64**
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary
- **athom**
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary
- **courier-authlib** (v0.71.4)
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary
- **courier-imap** (v5.1.4)
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary
- **debian-slim**
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary
- **distroless**
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary
- **espeasy**
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary
- **espurna**
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary
- **gitlab** (v17.6.0)
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary
- **grub**
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary
- **homekit**
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary
- **musl**
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary
- **ol_fileshare**
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary
- **openjre**
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary
- **pulsar** (v3.3.0)
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary
- **repo-security**
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary
- **repo-supervisor**
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary
- **scratch**
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary
- **scratch-base**
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary
- **secrets-scanner**
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary
- **secretz**
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary
- **shh**
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary
- **sssd**
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary
- **standard**
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary
- **static-c**
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary
- **tasmota**
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary
- **upstream**
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary
- **wled**
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary
- **wolfi-gcc**
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary
- **wolfi-jdk**
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary
- **wolfi-node**
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary
- **wolfi-python**
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary
- **x86_64-unknown-linux-musl**
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary
- **zeromq** (v4.3.5)
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary
- **zoe**
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary
- **zzh**
  - No ENTRYPOINT defined
  - Fix: Add ENTRYPOINT pointing to the application binary

### NO_HEALTHCHECK (1 images)

- **health-shim** (v1.0.0)
  - No HEALTHCHECK instruction
  - Fix: Add HEALTHCHECK with wget/curl to localhost or native health check command

### NO_EXPOSE (200 images)

- **aarch64-unknown-linux-musl**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **age** (v1.3.1)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **airbyte** (v0.65.22)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **airbyte-worker** (v0.65.22)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **alpine**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **alpine-static**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **amd64**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **argo-cd** (v3.4.2)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **argo-rollouts** (v1.9.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **arm64**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **athom**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **awslogs** (v0.15.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **azurelogs** (v1.2.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **betteruptime** (v0.2.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **buildah** (vv1.43.1)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **buildx** (v0.33.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **bundler** (v2.5.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **busybox** (v1.37.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **cargo-audit**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **certificates** (v1.6.5)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **checkov**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **checkov-k8s**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **chkrootkit**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **clamav**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **clamav-daemon**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **cloudflare-ddns** (v1.16.2)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **composer** (v2.8.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **composer-audit**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **conan-audit**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **cosign** (v3.0.6)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **cosign-verify** (v3.0.6)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **couchbase-operator** (v2.8.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **crane** (v0.21.5)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **dbmate** (v2.33.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **debian-slim**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **distroless**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **docker-bench**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **docker-clean** (v0.3.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **docker-gc** (v0.3.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **docui**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **dragonfly-client** (v1.18.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **elasticsearch-curator** (v5.8.3)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **espeasy**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **espurna**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **etcd-operator** (v3.6.10)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **falco**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **falco-rules**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **falcosidekick**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **flux2** (v2.8.6)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **fluxcd-helm** (v2.8.6)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **fluxcd-image** (v2.8.6)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **freeipa-client**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **freshclam**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **gcplogs** (v3.10.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **gem-audit**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **ggshield**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **git-secrets**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **gitguardian**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **github-actions-runner** (v2.316.1)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **gitlab-backup** (v4.6.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **gitleaks**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **go-static** (v1.22.10)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **golang** (v1.22.3)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **golang-alpine** (v1.22.10)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **gradle** (v8.10.2)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **grafana-operator** (v5.22.2)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **grafana-toolkit** (v10.4.1)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **grub**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **grype** (v0.80.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **grype-alpine**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **hadolint** (v2.14.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **haproxy-exporter** (v0.15.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **health-checks** (v1.0.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **health-shim** (v1.0.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **healthcheck** (v0.4.36)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **helm** (v3.15.1)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **helmfile** (v0.162.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **helmsman** (v4.0.5)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **hledger** (v1.52)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **homeassistant-core**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **homeassistant-hassio**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **homeassistant-supervisor**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **homekit**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **jenkins-agent** (v3355.v388858a_47b_33)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **jenkins-executor** (v3355.v388858a_47b_33)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **k3d** (v5.8.3)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **k3d-proxy** (v5.8.3)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **k3s** (v1.33.6+k3s1)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **k3s-agent** (v1.33.6+k3s1)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **kube-bench**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **kube-controller** (v1.30.1)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **kube-hunter**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **kube-proxy** (v1.30.1)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **kube-scheduler** (v1.30.1)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **kubectl** (v1.30.1)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **kubescape**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **kustomize** (v5.4.1)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **lazydocker**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **lazydocker-ui**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **linguist**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **linguist-go** (v9.5.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **lynis**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **maldet**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **maven** (v3.9.15)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **maxbot** (v0.3.0b2)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **mosquito**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **musl**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **mysql-anonymizer** (v0.10.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **mysql-backup** (v8.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **mysql-init** (v8.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **mysql-restore** (v8.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **newsboat** (v2.30)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **node** (v20.12.2)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **node-alpine** (v22.12.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **node-distroless** (v22.12.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **npm-audit**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **openjdk** (v21.0.3)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **openjdk-alpine** (v21-slim)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **openjre**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **openldap-backup**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **openldap-lambda**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **oxidized** (v0.30.1)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **paperless-ngx-gotenberg** (v2.14.4)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **paperless-ngx-ocr** (v2.14.4)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **paperless-ngx-tika** (v2.14.4)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **pdfarranger** (v1.12.2)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **pdfmixer** (v0.7.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **php** (v8.3)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **postgres-backup** (v17)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **postgres-restore** (v17)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **postgresql-anonymizer** (v1.2.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **postgresql-init** (v17)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **prometheus-aws-exporter** (v0.65.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **prometheus-haproxy-exporter** (v0.15.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **prometheus-operator** (v0.90.1)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **python** (v3.12.3)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **python-alpine** (v3.12)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **python-slim** (v3.12)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **questdb-python**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **r2c-bench**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **rblake**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **renovate** (v43.150.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **renovatebot** (v43.150.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **repo-security**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **repo-supervisor**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **rkhunter**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **ruby** (v3.3.1)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **rust** (v1.78.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **rust-static** (v1.78.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **rust-static-arm** (v1.78.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **sbt** (v1.12.10)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **scratch**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **scratch-base**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **seafile** (v11.0.14)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **seafile-pro** (v11.0.14)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **secrets-scanner**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **secretz**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **shh**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **snyk** (v1.1300.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **snyk-agent** (v1.1300.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **snyk-alpine**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **snyk-docker**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **snyk-monitor**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **sqlcipher** (v4.5.6)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **sqlite** (v3.45.1)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **sqlite-browser**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **sqlite-utils** (v3.39)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **standard**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **static-c**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **step-acme** (v0.30.2)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **step-cli** (v0.30.2)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **streamlink** (v7.0.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **surrealdb-python** (v1.0.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **syft** (v1.8.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **syft-alpine**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **tasmota**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **thanos-bucket** (v${VERSION})
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **tig** (v2.5.8)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **transferhelper**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **trivy** (v0.70.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **trivy-alpine**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **trivy-iac**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **trivy-k8s**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **trivy-operator** (v0.30.1)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **truffelsh**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **trufflehog**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **truffleshog**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **tryton** (v7.2.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **upstream**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **vault-csi-provider** (v1.7.1)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **vault-secrets-operator** (v1.4.0)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **wled**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **wolfi-gcc**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **wolfi-jdk**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **wolfi-node**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **wolfi-python**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **x86_64-unknown-linux-musl**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **zeromq** (v4.3.5)
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **zoe**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port
- **zzh**
  - No application EXPOSE ports (only metrics 9101 or none)
  - Fix: Add EXPOSE for the application's default port

### MISSING_USER (5 images)

- **distroless**
  - No USER directive
  - Fix: Add `USER 65532:65532` before ENTRYPOINT
- **wolfi-gcc**
  - No USER directive
  - Fix: Add `USER 65532:65532` before ENTRYPOINT
- **wolfi-jdk**
  - No USER directive
  - Fix: Add `USER 65532:65532` before ENTRYPOINT
- **wolfi-node**
  - No USER directive
  - Fix: Add `USER 65532:65532` before ENTRYPOINT
- **wolfi-python**
  - No USER directive
  - Fix: Add `USER 65532:65532` before ENTRYPOINT

### BLOATED (18 images)

- **codimd** (v2.6.1)
  - Final image stage contains build tools
  - Fix: Use multi-stage build; move build tools to builder stage
- **crate** (v5.9.0)
  - Final image stage contains build tools
  - Fix: Use multi-stage build; move build tools to builder stage
- **druid** (v37.0.0)
  - Final image stage contains build tools
  - Fix: Use multi-stage build; move build tools to builder stage
- **git-secrets**
  - Final image stage contains build tools
  - Fix: Use multi-stage build; move build tools to builder stage
- **github-actions-minimal** (v2.334.0)
  - Final image stage contains build tools
  - Fix: Use multi-stage build; move build tools to builder stage
- **gitlab-backup** (v4.6.0)
  - Final image stage contains build tools
  - Fix: Use multi-stage build; move build tools to builder stage
- **grafana-toolkit** (v10.4.1)
  - Final image stage contains build tools
  - Fix: Use multi-stage build; move build tools to builder stage
- **homebridge**
  - Final image stage contains build tools
  - Fix: Use multi-stage build; move build tools to builder stage
- **homebridge-camera**
  - Final image stage contains build tools
  - Fix: Use multi-stage build; move build tools to builder stage
- **memgraph** (v3.9.0)
  - Final image stage contains build tools
  - Fix: Use multi-stage build; move build tools to builder stage
- **neptune** (v1.2.0)
  - Final image stage contains build tools
  - Fix: Use multi-stage build; move build tools to builder stage
- **objectrocket** (v1.0.0)
  - Final image stage contains build tools
  - Fix: Use multi-stage build; move build tools to builder stage
- **openvpn-as** (v2.12.1)
  - Final image stage contains build tools
  - Fix: Use multi-stage build; move build tools to builder stage
- **scylladb** (v5.4.6)
  - Final image stage contains build tools
  - Fix: Use multi-stage build; move build tools to builder stage
- **singlestore** (v8.5.0)
  - Final image stage contains build tools
  - Fix: Use multi-stage build; move build tools to builder stage
- **source-control** (v1.22.0)
  - Final image stage contains build tools
  - Fix: Use multi-stage build; move build tools to builder stage
- **tig** (v2.5.8)
  - Final image stage contains build tools
  - Fix: Use multi-stage build; move build tools to builder stage
- **trino** (v435)
  - Final image stage contains build tools
  - Fix: Use multi-stage build; move build tools to builder stage

### NO_STOPSIGNAL (4 images)

- **wolfi-gcc**
  - No STOPSIGNAL directive
  - Fix: Add `STOPSIGNAL SIGTERM`
- **wolfi-jdk**
  - No STOPSIGNAL directive
  - Fix: Add `STOPSIGNAL SIGTERM`
- **wolfi-node**
  - No STOPSIGNAL directive
  - Fix: Add `STOPSIGNAL SIGTERM`
- **wolfi-python**
  - No STOPSIGNAL directive
  - Fix: Add `STOPSIGNAL SIGTERM`

### WRONG_BASE (21 images)

- **jellyfin** (v10.11.8)
  - glibc indicators found on musl base (cgr.dev/chainguard/wolfi-base)
  - Fix: Switch to debian-slim or UBI base image for glibc compatibility
- **jellyfin-server** (v10.11.8)
  - glibc indicators found on musl base (cgr.dev/chainguard/wolfi-base)
  - Fix: Switch to debian-slim or UBI base image for glibc compatibility
- **lidarr** (v3.1.0.4875)
  - glibc indicators found on musl base (cgr.dev/chainguard/wolfi-base)
  - Fix: Switch to debian-slim or UBI base image for glibc compatibility
- **mongodb-7** (v7.0.9)
  - glibc indicators found on musl base (cgr.dev/chainguard/wolfi-base)
  - Fix: Switch to debian-slim or UBI base image for glibc compatibility
- **mongodb-community** (v7.0.9)
  - glibc indicators found on musl base (cgr.dev/chainguard/wolfi-base)
  - Fix: Switch to debian-slim or UBI base image for glibc compatibility
- **mysql-8** (v8.0.39)
  - glibc indicators found on musl base (cgr.dev/chainguard/wolfi-base)
  - Fix: Switch to debian-slim or UBI base image for glibc compatibility
- **mysql-backup** (v8.0)
  - glibc indicators found on musl base (cgr.dev/chainguard/wolfi-base)
  - Fix: Switch to debian-slim or UBI base image for glibc compatibility
- **mysql-init** (v8.0)
  - glibc indicators found on musl base (cgr.dev/chainguard/wolfi-base)
  - Fix: Switch to debian-slim or UBI base image for glibc compatibility
- **mysql-restore** (v8.0)
  - glibc indicators found on musl base (cgr.dev/chainguard/wolfi-base)
  - Fix: Switch to debian-slim or UBI base image for glibc compatibility
- **pihole-ftl** (v5.18.2)
  - glibc indicators found on musl base (scratch)
  - Fix: Switch to debian-slim or UBI base image for glibc compatibility
- **postgres-backup** (v17)
  - glibc indicators found on musl base (cgr.dev/chainguard/wolfi-base)
  - Fix: Switch to debian-slim or UBI base image for glibc compatibility
- **postgres-restore** (v17)
  - glibc indicators found on musl base (cgr.dev/chainguard/wolfi-base)
  - Fix: Switch to debian-slim or UBI base image for glibc compatibility
- **postgresql-17** (v17.2)
  - glibc indicators found on musl base (cgr.dev/chainguard/wolfi-base)
  - Fix: Switch to debian-slim or UBI base image for glibc compatibility
- **postgresql-init** (v17)
  - glibc indicators found on musl base (cgr.dev/chainguard/wolfi-base)
  - Fix: Switch to debian-slim or UBI base image for glibc compatibility
- **prowlarr** (v2.3.5.5327)
  - glibc indicators found on musl base (cgr.dev/chainguard/wolfi-base)
  - Fix: Switch to debian-slim or UBI base image for glibc compatibility
- **radarr** (v6.1.1.10360)
  - glibc indicators found on musl base (cgr.dev/chainguard/wolfi-base)
  - Fix: Switch to debian-slim or UBI base image for glibc compatibility
- **shield** (v8.6.0)
  - glibc indicators found on musl base (scratch)
  - Fix: Switch to debian-slim or UBI base image for glibc compatibility
- **sonarr** (v4.0.17.2952)
  - glibc indicators found on musl base (cgr.dev/chainguard/wolfi-base)
  - Fix: Switch to debian-slim or UBI base image for glibc compatibility
- **sonic** (vv1.4.9)
  - glibc indicators found on musl base (scratch)
  - Fix: Switch to debian-slim or UBI base image for glibc compatibility
- **wolfi-gcc**
  - glibc indicators found on musl base (cgr.dev/chainguard/wolfi-base)
  - Fix: Switch to debian-slim or UBI base image for glibc compatibility
- **zeromq** (v4.3.5)
  - glibc indicators found on musl base (cgr.dev/chainguard/wolfi-base)
  - Fix: Switch to debian-slim or UBI base image for glibc compatibility

### HEALTHCHECK_NONE_NON_SCRATCH (130 images)

- **389ds**
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **activemq** (v5.18.3)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **adempiere** (v3.9.4)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **akaunting** (v3.1.21-v)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **alpine-static**
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/static)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **apache-ofbiz** (v24.09.05)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **awslogs** (v0.15.0)
  - HEALTHCHECK NONE on non-scratch base (registry.access.redhat.com/ubi9/ubi-minimal)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **azurelogs** (v1.2.0)
  - HEALTHCHECK NONE on non-scratch base (registry.access.redhat.com/ubi9/ubi-minimal)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **basic-auth-proxy**
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **beancount** (v2.3.6)
  - HEALTHCHECK NONE on non-scratch base (registry.access.redhat.com/ubi9/ubi-minimal)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **busybox** (v1.37.0)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **caddy-alpine** (v2.8.4)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **collabora** (v25.04.9.4.1)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **collabora-online** (v24.04.10.2)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **collabora-online-code** (v24.04.10.2)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **cors-proxy**
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **couchbase**
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **couchdb** (v3.5.1)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **cryptpad**
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **distroless**
  - HEALTHCHECK NONE on non-scratch base (gcr.io/distroless/static-debian12)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **dnsdist** (v1.9.4)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **docker-socket-proxy** (vv0.4.2)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **dolibarr** (v23.0.2)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **duplicati** (v2.1.0.1)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **egroupware** (v23.1.20240608)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **emby** (v4.9.3.0)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **espocrm** (v8.3.2)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **firefly-iii-importer** (v1.6.0)
  - HEALTHCHECK NONE on non-scratch base (registry.access.redhat.com/ubi9/ubi-minimal)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **focalboard-server** (v7.11.3)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **forgejo** (v12.0.3)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **freeipa-client**
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **frontaccounting** (v2.4.14)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **gcplogs** (v3.10.0)
  - HEALTHCHECK NONE on non-scratch base (registry.access.redhat.com/ubi9/ubi-minimal)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **gnucash** (v5.6)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **grafana-image-renderer** (v5.8.2)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **graylog** (v5.1.5)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **grisbi** (v2.0.5)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **headscale-ui** (v2026.03.17)
  - HEALTHCHECK NONE on non-scratch base (gcr.io/distroless/static-debian12)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **idempiere** (vv2.0)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **invoice-ninja** (v5.13.19)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **invoice-ninja-api** (v5.13.19)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **jellyfin** (v10.11.8)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **jellyfin-server** (v10.11.8)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **kafka-connect** (v3.6.1)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **keycloak** (v26.6.1)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **keycloak-init** (v26.6.1)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **keycloak-quarkus** (v26.6.1)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **kibana** (v8.12.2)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **kibana-oss** (v8.12.2)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **kmymoney** (v5.1.4)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **libreoffice** (v24.8.2)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **libreoffice-headless** (v24.8.2)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **lidarr** (v3.1.0.4875)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **logstash** (v8.12.2)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **logstash-oss** (v8.12.2)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **matrix-hookshot** (v7.3.2)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **maxbot** (v0.3.0b2)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **milvus-minio** (v2024.11.07)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **musl**
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/static)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **netmaker-ui** (vv1.5.1)
  - HEALTHCHECK NONE on non-scratch base (gcr.io/distroless/static-debian12)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **nextcloud** (v30.0.5)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **nextcloud-alpine** (v30.0.5)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **nextcloud-external** (v30.0.5)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **nextcloud-imaging** (v30.0.5)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **nextcloud-nginx** (v30.0.5)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **node-distroless** (v22.12.0)
  - HEALTHCHECK NONE on non-scratch base (gcr.io/distroless/nodejs22-debian12)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **ocserv** (v1.3.0)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **onlyoffice-communityserver** (v12.5.2)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **onlyoffice-controlpanel** (v12.5.2)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **openhab** (v5.2.0.M3)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **openldap-backup**
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **openldap-lambda**
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **openproject** (v14.0.5)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **opensearch** (v2.12.0)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **openvpn-as** (v2.12.1)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **photoshow** (vv2)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **pi-hole**
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **plex** (v1.41.3.9292)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **postgres** (v17.6)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **pptpd** (v1.10.0)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **prowlarr** (v2.3.5.5327)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **pulsar-functions** (v3.2.0)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **pulsar-proxy** (v3.2.0)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **pydio** (v8.2.5)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **radarr** (v6.1.1.10360)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **rclone-browser**
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **redis-vert** (v7.4.2)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **redis7** (v7.4.1)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **redmine** (v6.0.3)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **renovate** (v43.150.0)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **renovatebot** (v43.150.0)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **rocketmq** (v5.1.4)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **rss2** (v2025-08-05)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **rsyslog** (v8.2312.0)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **sentry** (vnightly)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **sentry-cron** (vnightly)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **sentry-worker** (vnightly)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **skrooge** (v2.31.0)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **smartdns** (vRelease48)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **snyk** (v1.1300.0)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **snyk-agent** (v1.1300.0)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **sonarr** (v4.0.17.2952)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **splunk-forwarder** (v9.2.1)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **sql-ledger** (v2.8.38)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **sqlcipher** (v4.5.6)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **sqlite-browser**
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **sqlite-utils** (v3.39)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **stirling-pdf** (v2.10.0)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **stirling-pdf-core** (v2.10.0)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **suitecrm** (v8.9.3)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **synapse** (v1.152.1)
  - HEALTHCHECK NONE on non-scratch base (registry.access.redhat.com/ubi9/ubi-minimal)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **syslog-ng** (v4.8.1)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **taiga** (v6.9.0)
  - HEALTHCHECK NONE on non-scratch base (registry.access.redhat.com/ubi9/ubi-minimal)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **taiga-backend** (v6.9.0)
  - HEALTHCHECK NONE on non-scratch base (registry.access.redhat.com/ubi9/ubi-minimal)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **taiga-front** (v6.8.2)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **taiga-protected** (v6.9.0)
  - HEALTHCHECK NONE on non-scratch base (registry.access.redhat.com/ubi9/ubi-minimal)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **tautulli** (v2.14.5)
  - HEALTHCHECK NONE on non-scratch base (registry.access.redhat.com/ubi9/ubi-minimal)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **tautulli-py** (v2.14.5)
  - HEALTHCHECK NONE on non-scratch base (registry.access.redhat.com/ubi9/ubi-minimal)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **tig** (v2.5.8)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **unbound-alpine** (v1.19.3)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **unoconv** (v0.8)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **vaultwarden-mysql** (v1.35.8)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **vaultwarden-postgres** (v1.35.8)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **vpn-controller** (v1.0.20210914)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **vtigercrm** (v8.3.0)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **wg-quick** (v1.0.20210914)
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **wolfi-gcc**
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **wolfi-jdk**
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **wolfi-node**
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images
- **wolfi-python**
  - HEALTHCHECK NONE on non-scratch base (cgr.dev/chainguard/wolfi-base)
  - Fix: Add a real HEALTHCHECK or use HEALTHCHECK NONE only on scratch images

---

## 9. Clean Images (No Issues Detected)

**295 images** have no detected issues:

| Image                            | Build Type      | Base            | EP                        | EXPOSE                     | HC       |
| -------------------------------- | --------------- | --------------- | ------------------------- | -------------------------- | -------- |
| airbyte-server                   | repack          | cgr.dev/chaingu | java", "-jar", "/app/serv | 8000                       | http/tcp |
| airsonic-advanced                | binary-download | cgr.dev/chaingu | java", "-jar", "/app/airs | 4040                       | http/tcp |
| airsonic                         | binary-download | cgr.dev/chaingu | java", "-jar", "/app/airs | 4040                       | http/tcp |
| apache                           | pkg-install     | cgr.dev/chaingu | apache2ctl                | 80,443                     | http/tcp |
| appsmith-editor                  | repack          | cgr.dev/chaingu | node                      | 8080                       | http/tcp |
| appsmith-nginx                   | repack          | cgr.dev/chaingu | node                      | 80                         | http/tcp |
| appsmith                         | repack          | cgr.dev/chaingu | node                      | 8080                       | http/tcp |
| arangodb-starter                 | repack          | scratch         | /arangod", "--serverstart | 8529                       | NONE     |
| argocd-application-controller    | binary-download | scratch         | argocd-application-contro | 8082                       | NONE     |
| argocd-applicationset-controller | binary-download | scratch         | argocd-applicationset-con | 8082                       | NONE     |
| argocd-notifications             | binary-download | scratch         | argocd-notifications      | 8082                       | NONE     |
| argocd-repo-server               | binary-download | scratch         | argocd-repo-server        | 8081                       | NONE     |
| argocd                           | binary-download | scratch         | argocd                    | 8080                       | NONE     |
| audiobookshelf-opds              | repack          | cgr.dev/chaingu | node                      | 13379                      | http/tcp |
| audiobookshelf                   | repack          | cgr.dev/chaingu | node                      | 13378                      | http/tcp |
| automatic1111                    | source-build    | cgr.dev/chaingu | python3", "/opt/automatic | 7860                       | http/tcp |
| bazarr-subliminal                | source-build    | cgr.dev/chaingu | python3", "/opt/bazarr-su | 6768                       | http/tcp |
| bazarr                           | source-build    | cgr.dev/chaingu | python3", "/opt/bazarr/ba | 6767                       | http/tcp |
| browserless-chrome               | repack          | cgr.dev/chaingu | node                      | 3000                       | http/tcp |
| browserless-edge                 | repack          | cgr.dev/chaingu | node                      | 3000                       | http/tcp |
| browserless                      | repack          | cgr.dev/chaingu | node                      | 3000                       | http/tcp |
| budibase-worker                  | repack          | cgr.dev/chaingu | node                      | 10001                      | http/tcp |
| budibase                         | repack          | cgr.dev/chaingu | node                      | 10000                      | http/tcp |
| buildkit                         | binary-download | scratch         | buildkitd                 | 1234                       | NONE     |
| calibre-eb                       | pkg-install     | cgr.dev/chaingu | calibre-server            | 8080                       | http/tcp |
| calibre-server                   | pkg-install     | cgr.dev/chaingu | calibre-server            | 8080                       | http/tcp |
| calibre-web                      | pkg-install     | cgr.dev/chaingu | python                    | 8083                       | http/tcp |
| calibre                          | pkg-install     | cgr.dev/chaingu | python3                   | 8080                       | http/tcp |
| chat-server                      | pkg-install     | cgr.dev/chaingu | synapse                   | 8008                       | http/tcp |
| chevereto                        | pkg-install     | cgr.dev/chaingu | php                       | 80                         | http/tcp |
| chroma-all-minimal               | pkg-install     | cgr.dev/chaingu | python3                   | 8000                       | http/tcp |
| chroma                           | pkg-install     | cgr.dev/chaingu | chroma                    | 8000                       | http/tcp |
| cinny                            | repack          | cgr.dev/chaingu | httpd                     | 80                         | http/tcp |
| cloudwatch-agent                 | repack          | scratch         | /amazon-cloudwatch-agent  | 25888,12789                | NONE     |
| cockpit                          | repack          | cgr.dev/chaingu | cockpit-ws                | 9090                       | http/tcp |
| comfyui                          | source-build    | cgr.dev/chaingu | python3", "/opt/comfyui/m | 8188                       | http/tcp |
| convector                        | pkg-install     | cgr.dev/chaingu | node                      | 8008                       | http/tcp |
| coqui-tts                        | pkg-install     | cgr.dev/chaingu | python3                   | 5002                       | http/tcp |
| crowdsec-agent                   | repack          | scratch         | /crowdsec                 | 8080,6060                  | NONE     |
| crowdsec-lapi                    | repack          | scratch         | /crowdsec                 | 8080,6060                  | NONE     |
| crowdsec                         | repack          | scratch         | /crowdsec                 | 8080,6060                  | NONE     |
| cyberchef-node                   | source-build    | cgr.dev/chaingu | node", "CyberChef.js      | 3000                       | http/tcp |
| cyberchef                        | source-build    | cgr.dev/chaingu | node", "server.js         | 8080                       | http/tcp |
| dagster-daemon                   | pkg-install     | cgr.dev/chaingu | dagster-daemon            | 3000                       | http/tcp |
| dagster-logs                     | pkg-install     | cgr.dev/chaingu | dagster-logs              | 3000                       | http/tcp |
| dagster                          | pkg-install     | cgr.dev/chaingu | dagster-webserver         | 3000                       | http/tcp |
| dashy-alpine                     | source-build    | cgr.dev/chaingu | node", "server.js         | 80,443                     | http/tcp |
| deepspeed                        | pkg-install     | cgr.dev/chaingu | python3                   | 8080                       | http/tcp |
| dendrite-monolith                | repack          | scratch         | /usr/local/bin/dendrite   | 8008                       | NONE     |
| dendrite-pot                     | repack          | cgr.dev/chaingu | /usr/local/bin/dendrite   | 8008                       | http/tcp |
| dendrite                         | repack          | scratch         | /usr/local/bin/dendrite   | 8008                       | NONE     |
| derby                            | binary-download | cgr.dev/chaingu | java", "-jar", "/opt/derb | 1527                       | http/tcp |
| dex                              | source-build    | scratch         | /dex                      | 5556                       | NONE     |
| diffusers                        | pkg-install     | cgr.dev/chaingu | python3                   | 8000                       | http/tcp |
| dnsvalidator                     | repack          | registry.access | /opt/venv/bin/dnsvalidato | 8080                       | http/tcp |
| dotdns                           | source-build    | scratch         | /usr/local/bin/dotdns     | 53,8053                    | NONE     |
| dovecot-lda                      | repack          | cgr.dev/chaingu | dovecot", "-F             | 143,993                    | http/tcp |
| dovecot-pop3                     | repack          | cgr.dev/chaingu | dovecot", "-F             | 110,995                    | http/tcp |
| dovecot                          | repack          | cgr.dev/chaingu | dovecot                   | 143,993,110,995,24         | http/tcp |
| drone-agent                      | repack          | scratch         | /usr/local/bin/drone-agen | 3000                       | NONE     |
| drone-autoscaler                 | repack          | scratch         | /usr/local/bin/drone-auto | 8080                       | NONE     |
| drone-runner                     | repack          | scratch         | /usr/local/bin/drone-runn | 3000                       | NONE     |
| drone                            | repack          | scratch         | /drone                    | 80                         | NONE     |
| duckdb                           | binary-download | scratch         | /usr/local/bin/duckdb     | 5432                       | NONE     |
| elasticsearch                    | binary-download | cgr.dev/chaingu | sh", "-c", "elasticsearch | 9200,9300                  | http/tcp |
| element-web                      | repack          | cgr.dev/chaingu | busybox", "httpd", "-f",  | 80                         | http/tcp |
| element-x                        | repack          | cgr.dev/chaingu | busybox", "httpd", "-f",  | 80                         | http/tcp |
| emqx-ee                          | repack          | cgr.dev/chaingu | echo                      | 1883,8083,8084,8883,18083  | http/tcp |
| emqx                             | binary-download | cgr.dev/chaingu | /opt/emqx/bin/emqx        | 1883,8083,8084,8883,18083  | http/tcp |
| envoy-extras                     | binary-download | scratch         | /usr/local/bin/envoy      | 9901                       | NONE     |
| envoy-grpc                       | binary-download | scratch         | /usr/local/bin/envoy      | 15001,15090                | NONE     |
| envoy-init                       | binary-download | scratch         | /usr/local/bin/envoy", "- | 9901                       | NONE     |
| envoy-sidecar                    | binary-download | scratch         | /usr/local/bin/envoy", "- | 15001                      | NONE     |
| envoy                            | binary-download | scratch         | /usr/local/bin/envoy      | 9901                       | NONE     |
| erpnext                          | pkg-install     | cgr.dev/chaingu | python3                   | 8000                       | http/tcp |
| fail2ban-exporter                | source-build    | scratch         | /fail2ban-exporter        | 9191                       | NONE     |
| fail2ban                         | pkg-install     | cgr.dev/chaingu | fail2ban                  | 22                         | http/tcp |
| ferretdb                         | binary-download | scratch         | /usr/local/bin/ferretdb   | 27017,8080                 | NONE     |
| firebird                         | pkg-install     | cgr.dev/chaingu | firebird                  | 3050                       | http/tcp |
| firefly-iii                      | pkg-install     | cgr.dev/chaingu | php                       | 80                         | http/tcp |
| fluent-bit                       | repack          | cgr.dev/chaingu | fluent-bit                | 2020                       | http/tcp |
| forgejo-runner                   | repack          | scratch         | /usr/local/bin/forgejo-ru | 8088                       | NONE     |
| freshrss-minimal                 | pkg-install     | cgr.dev/chaingu | php                       | 80                         | http/tcp |
| freshrss                         | pkg-install     | cgr.dev/chaingu | php                       | 80                         | http/tcp |
| gallery3                         | source-build    | cgr.dev/chaingu | python3", "/opt/gallery3/ | 8000                       | http/tcp |
| gitea-actions                    | binary-download | scratch         | gitea                     | 3000                       | NONE     |
| gitea-editor                     | binary-download | scratch         | gitea                     | 3000                       | NONE     |
| gitea-secure                     | binary-download | scratch         | gitea                     | 3000                       | NONE     |
| gitea                            | repack          | cgr.dev/chaingu | /usr/local/bin/gitea      | 3000,22                    | http/tcp |
| gitlab-ce                        | binary-download | cgr.dev/chaingu | /opt/gitlab/bin/gitlab    | 80,443,22                  | http/tcp |
| gitlab-ee                        | binary-download | cgr.dev/chaingu | /opt/gitlab/bin/gitlab    | 80,443,22                  | http/tcp |
| gitlab-geo                       | binary-download | cgr.dev/chaingu | /opt/gitlab/bin/gitlab-ge | 80,443                     | http/tcp |
| gitlab-runner-alpine             | binary-download | scratch         | gitlab-runner             | 8093                       | NONE     |
| gitlab-runner                    | binary-download | scratch         | gitlab-runner             | 8093                       | NONE     |
| gitserver                        | binary-download | scratch         | /opt/gitserver/gitea      | 80,22                      | NONE     |
| gotify                           | repack          | scratch         | /usr/local/bin/gotify     | 8080                       | NONE     |
| graphdb-enterpriser              | repack          | cgr.dev/chaingu | /opt/graphdb/bin/graphdb  | 7200                       | http/tcp |
| h2                               | binary-download | cgr.dev/chaingu | java", "-cp", "/opt/h2/h2 | 8082,9092                  | http/tcp |
| hackmd                           | pkg-install     | cgr.dev/chaingu | node", "app.js            | 3000                       | http/tcp |
| haproxy-dev                      | repack          | scratch         | /usr/local/sbin/haproxy", | 8404                       | NONE     |
| haproxy-lb                       | repack          | scratch         | /usr/local/sbin/haproxy", | 80,443                     | NONE     |
| haproxy                          | repack          | scratch         | /usr/local/sbin/haproxy   | 8404                       | NONE     |
| hazelcast                        | binary-download | cgr.dev/chaingu | /opt/hazelcast/bin/hazelc | 5701,5702,5703,8080        | http/tcp |
| hedgedoc-legacy                  | pkg-install     | cgr.dev/chaingu | node", "app.js            | 3000                       | http/tcp |
| hedgedoc                         | pkg-install     | cgr.dev/chaingu | node", "app.js            | 3000                       | http/tcp |
| heimdall-lite                    | source-build    | cgr.dev/chaingu | node                      | 80                         | http/tcp |
| heimdall                         | source-build    | cgr.dev/chaingu | node                      | 80,443                     | http/tcp |
| homeassistant                    | pkg-install     | cgr.dev/chaingu | python3                   | 8123                       | http/tcp |
| homepage-config                  | repack          | scratch         | homepage                  | 3000                       | NONE     |
| homepage-sync                    | repack          | scratch         | homepage                  | 3000                       | NONE     |
| homepage                         | repack          | scratch         | /app/homepage             | 3000                       | NONE     |
| hydrogen                         | binary-download | cgr.dev/chaingu | busybox", "httpd", "-f",  | 8080                       | http/tcp |
| immich-machine-learning          | pkg-install     | cgr.dev/chaingu | python3                   | 3003                       | http/tcp |
| immich-microservices             | repack          | cgr.dev/chaingu | node                      | 3002                       | http/tcp |
| immich-ml                        | pkg-install     | cgr.dev/chaingu | python3                   | 3003                       | http/tcp |
| immich-server                    | repack          | cgr.dev/chaingu | node                      | 3001                       | http/tcp |
| immich                           | pkg-install     | cgr.dev/chaingu | node                      | 2283                       | http/tcp |
| influxdb-2                       | repack          | scratch         | /influxd                  | 8086                       | NONE     |
| influxdb                         | repack          | scratch         | /influxd                  | 8086                       | NONE     |
| invokeai                         | pkg-install     | cgr.dev/chaingu | python3                   | 9090                       | http/tcp |
| iobroker                         | repack          | cgr.dev/chaingu | iobroker                  | 8081,3000                  | http/tcp |
| it-tools-legacy                  | source-build    | cgr.dev/chaingu | node", "server.js         | 8080                       | http/tcp |
| janusgraph                       | binary-download | cgr.dev/chaingu | /opt/janusgraph/bin/greml | 8182                       | http/tcp |
| jenkins                          | pkg-install     | cgr.dev/chaingu | jenkins                   | 8080                       | http/tcp |
| jitsu                            | repack          | cgr.dev/chaingu | node                      | 8000                       | http/tcp |
| jupyter-all                      | pkg-install     | cgr.dev/chaingu | jupyter                   | 8888                       | http/tcp |
| jupyter-pytorch                  | pkg-install     | cgr.dev/chaingu | jupyter-lab               | 8888                       | http/tcp |
| jupyter-scikit                   | pkg-install     | cgr.dev/chaingu | jupyter-lab               | 8888                       | http/tcp |
| jupyter-tensorflow               | pkg-install     | cgr.dev/chaingu | jupyter-lab               | 8888                       | http/tcp |
| kafka                            | binary-download | cgr.dev/chaingu | sh", "-c", "/opt/kafka/bi | 9092                       | http/tcp |
| knot-resolver                    | pkg-install     | cgr.dev/chaingu | kresd                     | 53,53                      | http/tcp |
| koel-next                        | pkg-install     | cgr.dev/chaingu | php                       | 80                         | http/tcp |
| koel                             | pkg-install     | cgr.dev/chaingu | php                       | 80                         | http/tcp |
| koken                            | pkg-install     | cgr.dev/chaingu | php                       | 80                         | http/tcp |
| kopano                           | pkg-install     | cgr.dev/chaingu | php                       | 80                         | http/tcp |
| langchain                        | pkg-install     | cgr.dev/chaingu | python3                   | 8000                       | http/tcp |
| langserve                        | pkg-install     | cgr.dev/chaingu | python3                   | 8000                       | http/tcp |
| ldap-account-manager             | repack          | cgr.dev/chaingu | php-fpm                   | 8080                       | http/tcp |
| ldap                             | pkg-install     | cgr.dev/chaingu | slapd                     | 389,636                    | http/tcp |
| libsql                           | binary-download | cgr.dev/chaingu | /opt/libsql/libsql-server | 8080                       | http/tcp |
| litellm-proxy                    | pkg-install     | cgr.dev/chaingu | litellm                   | 4000                       | http/tcp |
| litellm                          | pkg-install     | cgr.dev/chaingu | python3                   | 4000                       | http/tcp |
| logseq                           | pkg-install     | cgr.dev/chaingu | node                      | 3000                       | http/tcp |
| lychee                           | pkg-install     | cgr.dev/chaingu | php                       | 80                         | http/tcp |
| maddy                            | repack          | scratch         | /usr/local/bin/maddy      | 25,143,465,587,993,995     | NONE     |
| mailhog                          | repack          | scratch         | /usr/local/bin/MailHog    | 8025,1025                  | NONE     |
| mailu                            | repack          | registry.access | python", "-m", "mailu     | 8080                       | http/tcp |
| mariadb-10                       | binary-download | cgr.dev/chaingu | mariadbd                  | 3306                       | native   |
| mariadb-11                       | binary-download | cgr.dev/chaingu | /usr/local/bin/docker-ent | 3306                       | native   |
| mariadb-galera                   | binary-download | cgr.dev/chaingu | mariadbd", "--wsrep_new_c | 3306,4567,4568,4444        | native   |
| mariadb-operator                 | repack          | scratch         | /usr/local/bin/mariadb-op | 8080,8443                  | NONE     |
| mariadb                          | repack          | cgr.dev/chaingu | sh", "-c", "mariadbd      | 3306                       | native   |
| mattermost-bridge                | repack          | cgr.dev/chaingu | /app/plugin/server        | 8065                       | http/tcp |
| mattermost-operator              | repack          | scratch         | /usr/local/bin/mattermost | 8080                       | NONE     |
| meilisearch-python               | pkg-install     | cgr.dev/chaingu | python                    | 7700                       | http/tcp |
| meltano                          | pkg-install     | cgr.dev/chaingu | meltano                   | 5000                       | http/tcp |
| memcached                        | repack          | cgr.dev/chaingu | memcached                 | 11211                      | native   |
| milvus-etcd                      | pkg-install     | cgr.dev/chaingu | etcd                      | 2379,2380                  | generic  |
| milvus                           | repack          | cgr.dev/chaingu | /opt/milvus/bin/milvus    | 19530                      | http/tcp |
| miniflux-2                       | repack          | scratch         | /miniflux                 | 8080                       | NONE     |
| miniflux                         | repack          | scratch         | /miniflux                 | 8080                       | NONE     |
| minio-console                    | repack          | scratch         | /minio                    | 9000,9090                  | NONE     |
| mlflow-server                    | pkg-install     | cgr.dev/chaingu | mlflow                    | 5000                       | http/tcp |
| mlflow-tracking                  | pkg-install     | cgr.dev/chaingu | mlflow                    | 5000                       | http/tcp |
| mlflow                           | pkg-install     | cgr.dev/chaingu | mlflow                    | 5000                       | http/tcp |
| modsecurity-crs                  | source-build    | cgr.dev/chaingu | /usr/sbin/apache2", "-D", | 80,443                     | http/tcp |
| modsecurity                      | pkg-install     | cgr.dev/chaingu | apache2                   | 80                         | http/tcp |
| mongodb-5                        | repack          | cgr.dev/chaingu | mongod                    | 27017                      | native   |
| mongodb-6                        | repack          | cgr.dev/chaingu | mongod                    | 27017                      | native   |
| mongodb-opsmanager               | repack          | cgr.dev/chaingu | /opt/mongosh/bin/mongosh  | 27017                      | native   |
| mongodb                          | repack          | cgr.dev/chaingu | sh", "-c", "mongod        | 27017                      | native   |
| mosquitto-dev                    | repack          | cgr.dev/chaingu | mosquitto                 | 1883,9001                  | http/tcp |
| mosquitto                        | repack          | cgr.dev/chaingu | mosquitto                 | 1883,9001                  | http/tcp |
| mqtt                             | pkg-install     | cgr.dev/chaingu | mosquitto                 | 1883,9001                  | http/tcp |
| mysql                            | repack          | cgr.dev/chaingu | sh", "-c", "mariadbd      | 3306                       | native   |
| mythtv                           | pkg-install     | cgr.dev/chaingu | mythbackend               | 6543                       | http/tcp |
| n8n-nodes                        | repack          | cgr.dev/chaingu | node                      | 5679                       | http/tcp |
| n8n-webhook                      | repack          | cgr.dev/chaingu | node                      | 5678                       | http/tcp |
| n8n                              | pkg-install     | cgr.dev/chaingu | node                      | 5678                       | http/tcp |
| neo4j                            | binary-download | cgr.dev/chaingu | neo4j                     | 7474,7687                  | http/tcp |
| netclient                        | repack          | scratch         | /netclient                | 443                        | NONE     |
| nextcloud-ocis                   | repack          | scratch         | /nextcloud-ocis           | 9200                       | NONE     |
| nginx-modsec                     | pkg-install     | cgr.dev/chaingu | nginx                     | 80,443                     | http/tcp |
| nifi-registry                    | repack          | cgr.dev/chaingu | /opt/nifi-registry/bin/ni | 18080                      | http/tcp |
| node-red                         | source-build    | cgr.dev/chaingu | node", "/app/src/packages | 1880                       | http/tcp |
| ntfy                             | repack          | scratch         | /usr/local/bin/ntfy       | 80                         | NONE     |
| ocis                             | binary-download | scratch         | /ocis                     | 9200                       | NONE     |
| open-webui-api                   | repack          | cgr.dev/chaingu | node                      | 8080                       | http/tcp |
| open-webui                       | repack          | cgr.dev/chaingu | node                      | 8080                       | http/tcp |
| opengpts                         | pkg-install     | cgr.dev/chaingu | python3                   | 8000                       | http/tcp |
| openldap                         | pkg-install     | cgr.dev/chaingu | slapd                     | 389,636                    | http/tcp |
| opensearch-dashboards            | binary-download | cgr.dev/chaingu | opensearch-dashboards     | 5601                       | http/tcp |
| opensearch-operator              | repack          | scratch         | /usr/local/bin/opensearch | 8080,8443                  | NONE     |
| openvpn                          | repack          | cgr.dev/chaingu | /usr/local/bin/openvpn    | 1194                       | http/tcp |
| organizer                        | pkg-install     | cgr.dev/chaingu | php-fpm83                 | 80                         | http/tcp |
| outline                          | pkg-install     | cgr.dev/chaingu | node                      | 3000                       | http/tcp |
| pairdrop-server                  | source-build    | cgr.dev/chaingu | node", "server.js         | 3000                       | http/tcp |
| pgbouncer                        | pkg-install     | cgr.dev/chaingu | pgbouncer                 | 6432                       | http/tcp |
| pgpool-ii                        | pkg-install     | cgr.dev/chaingu | pgpool                    | 9999                       | http/tcp |
| photoprism-frontend              | repack          | cgr.dev/chaingu | node                      | 2283                       | http/tcp |
| photoprism                       | repack          | cgr.dev/chaingu | /opt/photoprism           | 2282                       | http/tcp |
| photoview                        | repack          | scratch         | /photoview                | 80                         | NONE     |
| php-apache                       | pkg-install     | cgr.dev/chaingu | apache2ctl                | 80                         | http/tcp |
| php-fpm                          | pkg-install     | cgr.dev/chaingu | php-fpm                   | 9000                       | http/tcp |
| pinecone                         | pkg-install     | cgr.dev/chaingu | python3                   | 8080                       | http/tcp |
| piwigo                           | pkg-install     | cgr.dev/chaingu | php                       | 80                         | http/tcp |
| planka                           | pkg-install     | cgr.dev/chaingu | node                      | 3000                       | http/tcp |
| pm2                              | repack          | cgr.dev/chaingu | node                      | 0                          | http/tcp |
| postfix-constrained              | repack          | cgr.dev/chaingu | postfix", "-c", "/etc/pos | 25                         | http/tcp |
| postfix-relay                    | repack          | cgr.dev/chaingu | postfix", "-c", "/etc/pos | 25,587                     | http/tcp |
| postfix                          | repack          | cgr.dev/chaingu | postfix                   | 25                         | http/tcp |
| postgis                          | repack          | cgr.dev/chaingu | postgres                  | 5432                       | http/tcp |
| postgres-operator                | repack          | scratch         | /usr/local/bin/postgres-o | 8080,8443                  | NONE     |
| postgresql-14                    | repack          | cgr.dev/chaingu | postgres                  | 5432                       | native   |
| postgresql-15                    | repack          | cgr.dev/chaingu | postgres                  | 5432                       | native   |
| postgresql-16                    | repack          | cgr.dev/chaingu | postgres                  | 5432                       | native   |
| postgresql-patroni               | repack          | registry.access | python3", "-m", "patroni  | 8008,5432                  | native   |
| postgresql                       | repack          | cgr.dev/chaingu | sh", "-c", "postgres      | 5432                       | native   |
| postgrey                         | repack          | cgr.dev/chaingu | postgrey                  | 10023                      | http/tcp |
| powerdns                         | pkg-install     | cgr.dev/chaingu | pdns                      | 53,8081                    | http/tcp |
| privatebin-nginx                 | source-build    | cgr.dev/chaingu | php-8.4-fpm               | 80                         | http/tcp |
| privatebin                       | pkg-install     | cgr.dev/chaingu | php                       | 80                         | http/tcp |
| promxy                           | repack          | scratch         | /promxy                   | 8082                       | NONE     |
| pytorch                          | pkg-install     | cgr.dev/chaingu | python3                   | 8080                       | http/tcp |
| qbitmanage                       | pkg-install     | cgr.dev/chaingu | python3                   | 8080                       | http/tcp |
| qbittorrent                      | pkg-install     | cgr.dev/chaingu | qbittorrent-nox           | 8080                       | http/tcp |
| rabbitmq                         | repack          | cgr.dev/chaingu | /usr/local/bin/docker-ent | 5672,15672                 | generic  |
| rainloop                         | repack          | cgr.dev/chaingu | httpd                     | 8888                       | http/tcp |
| redis-6                          | repack          | cgr.dev/chaingu | redis                     | 6379                       | native   |
| redis-7                          | repack          | cgr.dev/chaingu | /usr/local/bin/docker-ent | 6379                       | native   |
| redis-cluster                    | binary-download | cgr.dev/chaingu | /usr/local/bin/redis", "- | 6379,16379                 | native   |
| redis-insight                    | binary-download | cgr.dev/chaingu | /opt/redisinsight/redisin | 8001                       | http/tcp |
| redis-sentinel                   | binary-download | cgr.dev/chaingu | /usr/local/bin/redis", "- | 26379                      | http/tcp |
| redis                            | repack          | cgr.dev/chaingu | sh", "-c", "redis         | 6379                       | native   |
| roundcube                        | repack          | cgr.dev/chaingu | php-fpm83                 | 8888                       | http/tcp |
| rowy                             | repack          | cgr.dev/chaingu | node                      | 3000                       | http/tcp |
| rqlite                           | binary-download | scratch         | /usr/local/bin/rqlited    | 4001,4002                  | NONE     |
| rspamd                           | repack          | cgr.dev/chaingu | rspamd                    | 11333,11334                | http/tcp |
| rss2email                        | pkg-install     | cgr.dev/chaingu | r2e                       | 8080                       | http/tcp |
| scrapyd                          | pkg-install     | cgr.dev/chaingu | scrapyd                   | 6800                       | http/tcp |
| searxng                          | pkg-install     | cgr.dev/chaingu | python                    | 8080                       | http/tcp |
| sigal                            | pkg-install     | cgr.dev/chaingu | python3                   | 8000                       | http/tcp |
| singer                           | pkg-install     | cgr.dev/chaingu | python3                   | 8080                       | http/tcp |
| softether                        | pkg-install     | cgr.dev/chaingu | vpnserver                 | 443,992,1194,500,4500,5555 | http/tcp |
| spamassassin                     | repack          | cgr.dev/chaingu | spamassassin              | 783                        | http/tcp |
| sqlpage                          | binary-download | cgr.dev/chaingu | /opt/sqlpage/sqlpage      | 8080                       | http/tcp |
| stable-diffusion-webui           | source-build    | cgr.dev/chaingu | python3", "/opt/stable-di | 7860                       | http/tcp |
| stable-diffusion                 | pkg-install     | cgr.dev/chaingu | python3                   | 7860                       | http/tcp |
| stalwart-bitnami                 | repack          | cgr.dev/chaingu | /usr/local/bin/stalwart   | 25,143,465,587,993         | http/tcp |
| stalwart                         | repack          | scratch         | /usr/local/bin/stalwart   | 25,143,465,587,993         | NONE     |
| subsonic                         | binary-download | cgr.dev/chaingu | java", "-jar", "/app/subs | 4040                       | http/tcp |
| synapse-media                    | pkg-install     | debian          | python3", "-m", "synapse. | 8008                       | http/tcp |
| telegraf                         | binary-download | scratch         | /usr/bin/telegraf         | 8125,8092,8094             | NONE     |
| tensor                           | pkg-install     | cgr.dev/chaingu | tensorboard               | 6006                       | http/tcp |
| tensorboard                      | pkg-install     | cgr.dev/chaingu | tensorboard               | 6006                       | http/tcp |
| tensorflow                       | pkg-install     | cgr.dev/chaingu | python3                   | 8080                       | http/tcp |
| text-gen-ui                      | repack          | cgr.dev/chaingu | node                      | 7860                       | http/tcp |
| text-generation-webui            | source-build    | cgr.dev/chaingu | python3", "/opt/text-gene | 7860                       | http/tcp |
| timescaledb                      | repack          | cgr.dev/chaingu | postgres                  | 5432                       | http/tcp |
| tinytinyrss                      | pkg-install     | cgr.dev/chaingu | php                       | 80                         | http/tcp |
| tooljet-client                   | repack          | cgr.dev/chaingu | node                      | 8080                       | http/tcp |
| tooljet-server                   | repack          | cgr.dev/chaingu | node                      | 3000                       | http/tcp |
| tooljet                          | repack          | cgr.dev/chaingu | node                      | 8080                       | http/tcp |
| transformers-gpu                 | pkg-install     | cgr.dev/chaingu | python3                   | 8000                       | http/tcp |
| transformers                     | pkg-install     | cgr.dev/chaingu | python3                   | 8000                       | http/tcp |
| transmission                     | pkg-install     | cgr.dev/chaingu | transmission-daemon       | 9091                       | http/tcp |
| tt-rss                           | pkg-install     | cgr.dev/chaingu | php                       | 80                         | http/tcp |
| tts                              | pkg-install     | cgr.dev/chaingu | python3                   | 5002                       | http/tcp |
| tvheadend                        | pkg-install     | cgr.dev/chaingu | tvheadend                 | 9981                       | http/tcp |
| typesense-js                     | pkg-install     | cgr.dev/chaingu | node                      | 8108                       | http/tcp |
| uptime-kuma                      | pkg-install     | cgr.dev/chaingu | node                      | 3001                       | http/tcp |
| valkey-cluster                   | repack          | cgr.dev/chaingu | ["valkey",                | 6379,16379                 | http/tcp |
| valkey                           | pkg-install     | cgr.dev/chaingu | sh", "-c", "valkey        | 6379                       | generic  |
| vault-secrets                    | repack          | scratch         | /vault-secrets-operator   | 8080,8443                  | NONE     |
| vaultwarden-alpine               | repack          | scratch         | /vaultwarden              | 8080                       | NONE     |
| vaultwarden-sqlite               | repack          | scratch         | /vaultwarden              | 8080                       | NONE     |
| vaultwarden                      | repack          | scratch         | /vaultwarden              | 8080                       | NONE     |
| vecs-db                          | pkg-install     | cgr.dev/chaingu | python3                   | 8080                       | http/tcp |
| vector-init                      | binary-download | scratch         | /usr/bin/vector           | 8686                       | NONE     |
| vernemq                          | repack          | cgr.dev/chaingu | echo                      | 1883,4369,44053,8080       | http/tcp |
| virtuoso                         | binary-download | cgr.dev/chaingu | virtuoso-t", "-f", "-c",  | 1111,8890                  | http/tcp |
| vllm                             | pkg-install     | cgr.dev/chaingu | python3                   | 8000                       | http/tcp |
| wandb-server                     | pkg-install     | cgr.dev/chaingu | wandb                     | 8080                       | http/tcp |
| weaviate-python                  | pkg-install     | cgr.dev/chaingu | python3                   | 8080                       | http/tcp |
| weaviate                         | pkg-install     | cgr.dev/chaingu | /opt/weaviate             | 8080                       | http/tcp |
| weights-biases                   | pkg-install     | cgr.dev/chaingu | python3                   | 8080                       | http/tcp |
| whisper                          | pkg-install     | cgr.dev/chaingu | python3                   | 8080                       | http/tcp |
| woodpecker-agent                 | repack          | scratch         | /usr/local/bin/woodpecker | 3000                       | NONE     |
| woodpecker-ci                    | repack          | scratch         | /usr/local/bin/woodpecker | 8000                       | NONE     |
| woodpecker-server                | repack          | scratch         | /usr/local/bin/woodpecker | 8000                       | NONE     |
| yarn                             | repack          | cgr.dev/chaingu | node                      | 0                          | http/tcp |
| zenphoto                         | pkg-install     | cgr.dev/chaingu | php                       | 80                         | http/tcp |
| zerotier                         | repack          | cgr.dev/chaingu | /usr/sbin/zerotier-one    | 9993                       | http/tcp |
| zigbee2mqtt                      | source-build    | cgr.dev/chaingu | node", "index.js          | 8080                       | http/tcp |
| zipkin                           | binary-download | cgr.dev/chaingu | java                      | 9411                       | http/tcp |
