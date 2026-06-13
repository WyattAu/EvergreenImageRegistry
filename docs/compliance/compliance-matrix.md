# Evergreen Image Registry - Compliance Matrix

## Overview

This matrix maps each critical EIR image to applicable compliance standards, including FIPS 140-2/140-3, seccomp
profiles, AppArmor profiles, and implementation status.

**Legend:**

- ✅ Implemented
- 🔄 In Progress
- 📋 Planned
- ❌ Not Applicable / Requires Upstream
- ⚠️ Partial

## Critical Images Compliance Matrix

### Databases

| Image         | FIPS 140-3         | Seccomp            | AppArmor   | CIS        | STIG       | Notes                                                 |
| ------------- | ------------------ | ------------------ | ---------- | ---------- | ---------- | ----------------------------------------------------- |
| postgres      | 📋 Planned         | ✅ database.json   | 📋 Planned | 📋 Planned | 📋 Planned | OpenSSL FIPS provider; needs `OPENSSL_CONF` config    |
| mysql         | 📋 Planned         | ✅ database.json   | 📋 Planned | 📋 Planned | 📋 Planned | Requires source rebuild with FIPS OpenSSL             |
| redis         | 📋 Planned         | ✅ database.json   | 📋 Planned | 📋 Planned | 📋 Planned | `BUILD_TLS=yes` with FIPS OpenSSL                     |
| mongodb       | ⚠️ Enterprise only | ✅ database.json   | 📋 Planned | 📋 Planned | 📋 Planned | Enterprise FIPS certified; community rebuild needed   |
| cockroachdb   | 📋 Planned         | ✅ database.json   | 📋 Planned | 📋 Planned | 📋 Planned | Go BoringCrypto; cannot use scratch base              |
| valkey        | 📋 Planned         | ✅ database.json   | 📋 Planned | 📋 Planned | 📋 Planned | Redis fork; same FIPS approach                        |
| scylladb      | ❌ Not achievable  | ✅ database.json   | 📋 Planned | ❌ N/A     | ❌ N/A     | C++ Seastar framework; requires upstream FIPS support |
| tidb          | 📋 Planned         | ✅ database.json   | 📋 Planned | 📋 Planned | 📋 Planned | Go BoringCrypto; needs glibc base                     |
| mariadb       | 📋 Planned         | ✅ database.json   | 📋 Planned | 📋 Planned | 📋 Planned | MySQL fork; same FIPS approach                        |
| opensearch    | 📋 Planned         | ✅ networking.json | 📋 Planned | 📋 Planned | 📋 Planned | Java-based; needs BouncyCastle FIPS                   |
| elasticsearch | 📋 Planned         | ✅ networking.json | 📋 Planned | 📋 Planned | 📋 Planned | Java-based; needs BouncyCastle FIPS                   |

### Authentication & Identity

| Image        | FIPS 140-3        | Seccomp         | AppArmor   | CIS        | STIG       | Notes                                               |
| ------------ | ----------------- | --------------- | ---------- | ---------- | ---------- | --------------------------------------------------- |
| keycloak     | 📋 Planned        | ✅ default.json | 📋 Planned | 📋 Planned | 📋 Planned | Java Quarkus FIPS; `-Dquarkus.ssl.native-fips=true` |
| dex          | 📋 Planned        | ✅ minimal.json | 📋 Planned | 📋 Planned | 📋 Planned | Go BoringCrypto; switch from scratch                |
| vaultwarden  | ❌ Not applicable | ✅ default.json | 📋 Planned | 📋 Planned | 📋 Planned | Rust binary; depends on upstream vaultwarden FIPS   |
| oauth2-proxy | 📋 Planned        | ✅ default.json | 📋 Planned | 📋 Planned | 📋 Planned | Go BoringCrypto                                     |
| kanidm       | 📋 Planned        | ✅ default.json | 📋 Planned | 📋 Planned | 📋 Planned | Rust; needs OPENSSL_NO_VENDOR=1                     |
| authelia     | 📋 Planned        | ✅ default.json | 📋 Planned | 📋 Planned | 📋 Planned | Go BoringCrypto                                     |

### Networking & Proxy

| Image     | FIPS 140-3             | Seccomp            | AppArmor   | CIS        | STIG       | Notes                                                     |
| --------- | ---------------------- | ------------------ | ---------- | ---------- | ---------- | --------------------------------------------------------- |
| envoy     | ✅ Official FIPS build | ✅ networking.json | 📋 Planned | 📋 Planned | 📋 Planned | BoringSSL BoringCrypto built-in; use official FIPS binary |
| nginx     | 📋 Planned             | ✅ networking.json | 📋 Planned | 📋 Planned | 📋 Planned | OpenSSL FIPS provider; `--with-openssl` build flag        |
| traefik   | 📋 Planned             | ✅ networking.json | 📋 Planned | 📋 Planned | 📋 Planned | Go BoringCrypto                                           |
| coredns   | 📋 Planned             | ✅ networking.json | 📋 Planned | 📋 Planned | 📋 Planned | Go BoringCrypto                                           |
| consul    | ⚠️ Enterprise only     | ✅ networking.json | 📋 Planned | 📋 Planned | 📋 Planned | Enterprise FIPS certified; community rebuild possible     |
| haproxy   | 📋 Planned             | ✅ networking.json | 📋 Planned | 📋 Planned | 📋 Planned | C; OpenSSL FIPS provider needed                           |
| wireguard | ❌ Not applicable      | ✅ networking.json | 📋 Planned | 📋 Planned | 📋 Planned | Kernel crypto; no userspace FIPS module                   |

### Cryptography & Certificates

| Image        | FIPS 140-3         | Seccomp         | AppArmor   | CIS        | STIG       | Notes                                                       |
| ------------ | ------------------ | --------------- | ---------- | ---------- | ---------- | ----------------------------------------------------------- |
| vault        | ⚠️ Enterprise only | ✅ minimal.json | 📋 Planned | 📋 Planned | 📋 Planned | Enterprise FIPS certified; community BoringCrypto available |
| step-ca      | 📋 Planned         | ✅ default.json | 📋 Planned | 📋 Planned | 📋 Planned | Go BoringCrypto                                             |
| cosign       | 📋 Planned         | ✅ minimal.json | 📋 Planned | 📋 Planned | 📋 Planned | Go BoringCrypto                                             |
| fulcio       | 📋 Planned         | ✅ minimal.json | 📋 Planned | 📋 Planned | 📋 Planned | Go BoringCrypto                                             |
| rekor        | 📋 Planned         | ✅ minimal.json | 📋 Planned | 📋 Planned | 📋 Planned | Go BoringCrypto                                             |
| cert-manager | 📋 Planned         | ✅ default.json | 📋 Planned | 📋 Planned | 📋 Planned | Go BoringCrypto                                             |

### Monitoring & Observability

| Image                        | FIPS 140-3 | Seccomp         | AppArmor   | CIS        | STIG       | Notes                     |
| ---------------------------- | ---------- | --------------- | ---------- | ---------- | ---------- | ------------------------- |
| prometheus                   | 📋 Planned | ✅ default.json | 📋 Planned | 📋 Planned | 📋 Planned | Go BoringCrypto           |
| grafana                      | 📋 Planned | ✅ default.json | 📋 Planned | 📋 Planned | 📋 Planned | Go BoringCrypto (backend) |
| alertmanager                 | 📋 Planned | ✅ default.json | 📋 Planned | 📋 Planned | 📋 Planned | Go BoringCrypto           |
| loki                         | 📋 Planned | ✅ default.json | 📋 Planned | 📋 Planned | 📋 Planned | Go BoringCrypto           |
| tempo                        | 📋 Planned | ✅ default.json | 📋 Planned | 📋 Planned | 📋 Planned | Go BoringCrypto           |
| thanos                       | 📋 Planned | ✅ default.json | 📋 Planned | 📋 Planned | 📋 Planned | Go BoringCrypto           |
| node-exporter                | 📋 Planned | ✅ minimal.json | 📋 Planned | 📋 Planned | 📋 Planned | Go BoringCrypto           |
| cadvisor                     | 📋 Planned | ✅ default.json | 📋 Planned | 📋 Planned | 📋 Planned | Go BoringCrypto           |
| redis-exporter               | 📋 Planned | ✅ default.json | 📋 Planned | 📋 Planned | 📋 Planned | Go BoringCrypto           |
| postgres-exporter            | 📋 Planned | ✅ default.json | 📋 Planned | 📋 Planned | 📋 Planned | Go BoringCrypto           |
| prometheus-blackbox-exporter | 📋 Planned | ✅ default.json | 📋 Planned | 📋 Planned | 📋 Planned | Go BoringCrypto           |

### CI/CD & DevOps

| Image              | FIPS 140-3 | Seccomp         | AppArmor   | CIS        | STIG       | Notes                         |
| ------------------ | ---------- | --------------- | ---------- | ---------- | ---------- | ----------------------------- |
| jenkins            | 📋 Planned | ✅ default.json | 📋 Planned | 📋 Planned | 📋 Planned | Java-based; BouncyCastle FIPS |
| drone              | 📋 Planned | ✅ default.json | 📋 Planned | 📋 Planned | 📋 Planned | Go BoringCrypto               |
| argo-cd            | 📋 Planned | ✅ default.json | 📋 Planned | 📋 Planned | 📋 Planned | Go BoringCrypto               |
| tekton             | 📋 Planned | ✅ default.json | 📋 Planned | 📋 Planned | 📋 Planned | Go BoringCrypto               |
| forgejo            | 📋 Planned | ✅ default.json | 📋 Planned | 📋 Planned | 📋 Planned | Go BoringCrypto               |
| forgejo-runner-k8s | 📋 Planned | ✅ default.json | 📋 Planned | 📋 Planned | 📋 Planned | Go BoringCrypto               |
| kaniko             | 📋 Planned | ✅ default.json | 📋 Planned | 📋 Planned | 📋 Planned | Go BoringCrypto               |

### Messaging & Queues

| Image    | FIPS 140-3         | Seccomp         | AppArmor   | CIS        | STIG       | Notes                                     |
| -------- | ------------------ | --------------- | ---------- | ---------- | ---------- | ----------------------------------------- |
| nats     | 📋 Planned         | ✅ default.json | 📋 Planned | 📋 Planned | 📋 Planned | Go BoringCrypto                           |
| rabbitmq | 📋 Planned         | ✅ default.json | 📋 Planned | 📋 Planned | 📋 Planned | Erlang/OTP; OpenSSL FIPS                  |
| kafka    | ⚠️ Enterprise only | ✅ default.json | 📋 Planned | 📋 Planned | 📋 Planned | Java; Confluent Enterprise FIPS available |
| activemq | 📋 Planned         | ✅ default.json | 📋 Planned | 📋 Planned | 📋 Planned | Java; BouncyCastle FIPS                   |

### Security Scanning

| Image       | FIPS 140-3        | Seccomp         | AppArmor   | CIS        | STIG       | Notes                                          |
| ----------- | ----------------- | --------------- | ---------- | ---------- | ---------- | ---------------------------------------------- |
| trivy       | 📋 Planned        | ✅ minimal.json | 📋 Planned | 📋 Planned | 📋 Planned | Go BoringCrypto                                |
| falco       | ❌ Not achievable | ✅ default.json | 📋 Planned | 📋 Planned | 📋 Planned | C++ with kernel module; requires upstream FIPS |
| kubescape   | 📋 Planned        | ✅ minimal.json | 📋 Planned | 📋 Planned | 📋 Planned | Go BoringCrypto                                |
| vaultwarden | ❌ Not applicable | ✅ default.json | 📋 Planned | 📋 Planned | 📋 Planned | Rust; depends on upstream                      |

### Storage & Backup

| Image    | FIPS 140-3 | Seccomp         | AppArmor   | CIS        | STIG       | Notes           |
| -------- | ---------- | --------------- | ---------- | ---------- | ---------- | --------------- |
| minio    | 📋 Planned | ✅ default.json | 📋 Planned | 📋 Planned | 📋 Planned | Go BoringCrypto |
| restic   | 📋 Planned | ✅ minimal.json | 📋 Planned | 📋 Planned | 📋 Planned | Go BoringCrypto |
| longhorn | 📋 Planned | ✅ default.json | 📋 Planned | 📋 Planned | 📋 Planned | Go BoringCrypto |

### Web & Applications

| Image       | FIPS 140-3 | Seccomp         | AppArmor   | CIS        | STIG       | Notes                       |
| ----------- | ---------- | --------------- | ---------- | ---------- | ---------- | --------------------------- |
| homepage    | 📋 Planned | ✅ default.json | 📋 Planned | 📋 Planned | 📋 Planned | Node.js; Node.js FIPS mode  |
| freshrss    | 📋 Planned | ✅ default.json | 📋 Planned | 📋 Planned | 📋 Planned | PHP; OpenSSL FIPS           |
| calibre-web | 📋 Planned | ✅ default.json | 📋 Planned | 📋 Planned | 📋 Planned | Python; pyOpenSSL FIPS      |
| immich      | 📋 Planned | ✅ default.json | 📋 Planned | 📋 Planned | 📋 Planned | Go/TypeScript; mixed crypto |
| akaunting   | 📋 Planned | ✅ default.json | 📋 Planned | 📋 Planned | 📋 Planned | PHP; OpenSSL FIPS           |

## Summary Statistics

### FIPS 140-3 Status

| Status                                | Count | Percentage |
| ------------------------------------- | ----- | ---------- |
| ✅ Implemented (Official FIPS)        | 1     | ~1%        |
| 📋 Planned (Achievable)               | 75    | ~80%       |
| ⚠️ Enterprise Only                    | 4     | ~4%        |
| ❌ Not Achievable (Requires Upstream) | 5     | ~5%        |
| ❌ Not Applicable                     | 3     | ~3%        |
| 🔄 In Progress                        | 5     | ~5%        |

### Seccomp Profile Distribution

| Profile         | Images Using |
| --------------- | ------------ |
| default.json    | 55           |
| database.json   | 11           |
| networking.json | 10           |
| minimal.json    | 14           |

### AppArmor Profile Status

| Status         | Count |
| -------------- | ----- |
| ✅ Implemented | 0     |
| 📋 Planned     | 95    |

## Implementation Roadmap

### Phase 1: Foundation (Current)

- ✅ Seccomp profiles created for all image categories
- ✅ FIPS 140-3 documentation published
- ✅ Compliance matrix established

### Phase 2: Seccomp Rollout

- Add seccomp profiles to all critical image Dockerfiles
- Add seccomp profile validation to CI pipeline
- Add seccomp compliance checks to pre-commit hooks

### Phase 3: AppArmor Profiles

- Implement default AppArmor profile for all images
- Implement minimal profile for scratch-based images
- Implement docker-socket-proxy profile for proxy images

### Phase 4: FIPS Variants

- Build FIPS variants for Tier 1 critical images (postgres, redis, nginx, envoy, vault)
- Add FIPS variant testing to CI/CD pipeline
- Publish FIPS variant tags alongside standard tags

### Phase 5: CIS/STIG Compliance

- Map CIS Docker Benchmark to EIR images
- Implement STIG hardening for critical infrastructure images
- Add compliance scanning to nightly CI

## References

- [FIPS 140-3 Implementation Guide](./fips-140-3.md)
- [Seccomp Profiles](../../security/seccomp/)
- [AppArmor Profiles](../../security/apparmor/)
- [CIS Docker Benchmark](https://www.cisecurity.org/benchmark/docker)
- [NIST FIPS 140-3](https://csrc.nist.gov/projects/cryptographic-module-validation-program)
- [NIST SP 800-123](https://csrc.nist.gov/publications/detail/sp/800-123/final) - Guide to General Server Security
