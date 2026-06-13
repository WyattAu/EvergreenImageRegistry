# SSRF Protection Guide

## Overview

Server-Side Request Forgery (SSRF) allows an attacker to make outbound HTTP requests from a container to unintended destinations. In the context of hardened container images, SSRF can be used to:

- Access cloud metadata endpoints (169.254.169.254 on AWS/GCP/Azure)
- Scan internal networks and services
- Pivot to internal APIs not exposed externally
- Exfiltrate data via DNS/HTTP channels
- Exploit internal services that lack authentication

## Threat Model for Container Images

Evergreen images that make outbound HTTP requests are particularly susceptible:

| Image       | Attack Vector                              | Risk                                 |
| ----------- | ------------------------------------------ | ------------------------------------ |
| prometheus  | Malicious scrape targets in config         | Internal network enumeration         |
| grafana     | User-configured data source URLs           | Metadata endpoint access             |
| trivy       | Malicious registry URLs in CI              | Credential exfiltration              |
| keycloak    | OIDC endpoint configuration                | Token theft via redirect             |
| alertmanager| Webhook receiver URLs                      | Internal service abuse               |
| webhook     | Outgoing HTTP hook URLs                    | Full SSRF chain                      |

## Network Namespace Isolation

### Docker

Restrict outbound connectivity at the network level:

```bash
# Create an isolated network with no outbound routing
docker network create \
  --driver bridge \
  --opt com.docker.network.bridge.enable_icc=false \
  --opt com.docker.network.bridge.enable_ip_masquerade=false \
  --subnet 172.28.0.0/16 \
  evergreen-isolated

# Run with isolated network + explicit outbound network
docker run --network evergreen-isolated prometheus:latest
```

### Kubernetes NetworkPolicy

Deny all egress by default, then allow only specific destinations:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all-egress
  namespace: monitoring
spec:
  podSelector:
    matchLabels:
      evergreen.image/tier: critical
  policyTypes:
    - Egress
  egress: []
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-prometheus-scrape
  namespace: monitoring
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/name: prometheus
  policyTypes:
    - Egress
  egress:
    - to:
        - namespaceSelector:
            matchLabels:
              name: monitoring
        - namespaceSelector:
            matchLabels:
              name: ingress
      ports:
        - protocol: TCP
          port: 9090
        - protocol: TCP
          port: 9100
```

## DNS Restrictions

Prevent resolution of internal/cloud hostnames:

### CoreDNS Blocklist (Kubernetes)

```yaml
# ConfigMap override for CoreDNS
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns-custom
  namespace: kube-system
data:
  ssrf-block.server: |
    metadata.google.internal:53 {
      errors
      cache 30
      reload
      fallthrough
      # Block all queries for cloud metadata
      template ANY ANY metadata.google.internal {
        rcode NXDOMAIN
      }
    }
    metadata.aws.internal:53 {
      errors
      cache 30
      reload
      fallthrough
      template ANY ANY metadata.aws.internal {
        rcode NXDOMAIN
      }
    }
```

### /etc/hosts Override (Docker)

```dockerfile
# Block cloud metadata endpoints at the hosts file level
COPY <<EOF /etc/hosts.block
0.0.0.0 metadata.google.internal
0.0.0.0 metadata.goog
0.0.0.0 169.254.169.254
0.0.0.0 instance-data.ec2.internal
::1 metadata.google.internal
::1 metadata.goog
::1 169.254.169.254
EOF

ENTRYPOINT ["sh", "-c", "cat /etc/hosts.block >> /etc/hosts && exec /binary"]
```

## Outbound Connection Allowlisting

### iptables

```bash
# Drop all outbound by default
iptables -P OUTPUT DROP

# Allow established connections
iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow DNS to specific resolvers only
iptables -A OUTPUT -p udp --dport 53 -d 1.1.1.1 -j ACCEPT
iptables -A OUTPUT -p udp --dport 53 -d 8.8.8.8 -j ACCEPT

# Allow HTTPS to specific registries (for trivy)
iptables -A OUTPUT -p tcp --dport 443 -d ghcr.io -j ACCEPT
iptables -A OUTPUT -p tcp --dport 443 -d registry-1.docker.io -j ACCEPT

# Allow Prometheus scrape targets (specific subnets only)
iptables -A OUTPUT -p tcp --dport 9090 -d 10.0.0.0/8 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 9100 -d 10.0.0.0/8 -j ACCEPT

# Allow loopback
iptables -A OUTPUT -o lo -j ACCEPT
```

### nftables

```nftables
table inet ssrf-protection {
  chain output {
    type filter hook output priority 0; policy drop;

    # Allow established
    ct state established,related accept

    # Allow loopback
    oif "lo" accept

    # Allow DNS to approved resolvers
    ip daddr { 1.1.1.1, 8.8.8.8 } udp dport 53 accept
    ip daddr { 1.1.1.1, 8.8.8.8 } tcp dport 53 accept

    # Allow HTTPS to approved destinations
    ip daddr 10.0.0.0/8 tcp dport { 443, 9090, 9100 } accept
    ip6 daddr fd00::/8 tcp dport { 443, 9090, 9100 } accept
  }
}
```

## Environment Variable Configuration

All Evergreen images that make outbound requests should support these environment variables:

| Variable                          | Description                                      | Example                         |
| --------------------------------- | ------------------------------------------------ | ------------------------------- |
| `EVERGREEN_ALLOWED_HOSTS`         | Comma-separated list of allowed hostnames         | `api.github.com,ghcr.io`        |
| `EVERGREEN_ALLOWED_CIDRS`         | Comma-separated list of allowed destination CIDRs | `10.0.0.0/8,172.16.0.0/12`     |
| `EVERGREEN_BLOCK_METADATA`        | Block cloud metadata endpoints (default: `true`)  | `true`                          |
| `EVERGREEN_DNS_SERVERS`           | Approved DNS resolvers                            | `1.1.1.1,8.8.8.8`              |
| `EVERGREEN_OUTBOUND_PORTS`        | Allowed destination ports                         | `443,9090,9100`                 |
| `EVERGREEN_PROXY`                 | Outbound HTTP proxy for all requests              | `http://proxy.internal:3128`    |
| `EVERGREEN_NO_PROXY`              | Destinations that bypass the proxy                | `localhost,127.0.0.1,10.0.0.0/8`|
| `EVERGREEN_REQUEST_TIMEOUT`       | Maximum outbound request duration                 | `30s`                           |
| `EVERGREEN_MAX_REDIRECTS`         | Maximum HTTP redirects allowed                    | `0`                             |
| `EVERGREEN_DISABLE_IPV6`          | Disable IPv6 for outbound connections             | `true`                          |

### Implementation Pattern

Go-based images should use the standard `net/http` client with a custom transport:

```go
package ssrf

import (
    "net"
    "net/http"
    "strings"
    "time"
)

var blockedNetworks = []struct {
    net  *net.IPNet
    name string
}{
    mustParseCIDR("169.254.0.0/16", "link-local"),
    mustParseCIDR("127.0.0.0/8", "loopback"),
    mustParseCIDR("::1/128", "loopback-v6"),
    mustParseCIDR("fd00::/8", "ULA-v6"),
    mustParseCIDR("fe80::/10", "link-local-v6"),
}

func SafeHTTPClient(timeout time.Duration) *http.Client {
    dialer := &net.Dialer{Timeout: timeout}
    transport := &http.Transport{
        DialContext: func(ctx interface{}, network, addr string) (net.Conn, error) {
            host, _, _ := net.SplitHostPort(addr)
            ips, err := net.LookupIP(host)
            if err != nil {
                return nil, err
            }
            for _, ip := range ips {
                for _, blocked := range blockedNetworks {
                    if blocked.net.Contains(ip) {
                        return nil, fmt.Errorf("ssrf: blocked %s (%s)", ip, blocked.name)
                    }
                }
            }
            return dialer.DialContext(ctx.(context.Context), network, addr)
        },
    }
    checkRedirect := func(req *http.Request, via []*http.Request) error {
        if len(via) >= 2 {
            return fmt.Errorf("ssrf: too many redirects")
        }
        return nil
    }
    return &http.Client{
        Transport:     transport,
        Timeout:       timeout,
        CheckRedirect: checkRedirect,
    }
}
```

## Per-Image Guidance

### Prometheus

Prometheus scrapes user-defined targets, making it a high-risk SSRF vector.

**Mitigations:**

1. Restrict scrape targets to known subnets via `--web.enable-remote-write-receiver=false`
2. Use `--storage.tsdb.retention.time` to limit exposure window
3. Set `EVERGREEN_ALLOWED_CIDRS` to scrape target subnets only
4. Block metadata endpoint access at the network level

```yaml
# prometheus.yml - restrict scrape targets
global:
  scrape_interval: 15s
  scrape_timeout: 10s

scrape_configs:
  - job_name: 'evergreen'
    static_configs:
      - targets:
          - '10.0.1.10:9090'
          - '10.0.1.11:9100'
    metric_relabel_configs:
      - source_labels: [__address__]
        regex: '10\.0\.1\.\d+:\d+'
        action: keep
```

### Grafana

Users configure data source URLs, enabling SSRF through the UI.

**Mitigations:**

1. Set `GF_SECURITY_DATA_SOURCE_PROXY_WHITELIST` to allowed data source hosts
2. Disable `GF_AUTH_ANONYMOUS_ENABLED` to prevent unauthenticated SSRF
3. Use `GF_DATABASE_URL` with internal-only addresses
4. Set `GF_SERVER_ENABLE_GZIP=true` to reduce request smuggling risk

```ini
[security]
data_source_proxy_whitelist = prometheus.monitoring.svc:9090,loki.logging.svc:3100

[auth]
disable_login_form = false
disable_signout_menu = false

[panels]
disable_sanitize_html = true
```

### Trivy

Trivy fetches vulnerability databases and registry manifests, making registry URL manipulation an SSRF vector.

**Mitigations:**

1. Pin `TRIVY_DB_REPOSITORY` to approved registries only
2. Set `TRIVY_REGISTRY_TOKEN` via sealed secrets, not environment
3. Disable `TRIVY_SKIP_UPDATE` only in air-gapped environments
4. Use `TRIVY_INSECURE=false` to enforce TLS

```bash
TRIVY_DB_REPOSITORY=ghcr.io/aquasecurity/trivy-db
TRIVY_JAVA_DB_REPOSITORY=ghcr.io/aquasecurity/trivy-java-db
TRIVY_INSECURE=false
TRIVY_SKIP_DB_UPDATE=false
TRIVY_SKIP_JAVA_DB_UPDATE=false
```

### Keycloak

OIDC endpoint configuration and identity provider URLs are SSRF vectors.

**Mitigations:**

1. Restrict `KC_PROXY` to edge mode only
2. Pin `KC_HOSTNAME` to prevent redirect-based SSRF
3. Set `KC_SPI_HOSTNAME_DEFAULT_PROVIDER=fixed` to prevent dynamic hostname resolution
4. Block metadata endpoint access at the network level

```bash
KC_HOSTNAME=auth.example.com
KC_HOSTNAME_STRICT=true
KC_HOSTNAME_STRICT_HTTPS=true
KC_SPI_HOSTNAME_DEFAULT_PROVIDER=fixed
KC_HTTP_ENABLED=false
KC_PROXY=edge
```

## Verification

### Test SSRF Protection

```bash
# Verify metadata endpoint is blocked
docker run --rm evergreen/prometheus:latest \
  wget -q -O - http://169.254.169.254/latest/meta-data/ && echo "FAIL" || echo "PASS"

# Verify internal DNS is blocked
docker run --rm evergreen/grafana:latest \
  nslookup metadata.google.internal && echo "FAIL" || echo "PASS"

# Verify outbound allowlist works
docker run --rm evergreen/trivy:latest \
  wget -q -O - https://unauthorized-host.example.com && echo "FAIL" || echo "PASS"
```

### Verify with evergreenctl

```bash
evergreenctl verify --check ssrf images/prometheus/
evergreenctl audit --security ssrf images/
```
