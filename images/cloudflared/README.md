# Cloudflared - Evergreen Hardened Image

## Image Information

| Attribute | Value |
|-----------|-------|
| Image | `cloudflared` |
| Base | `scratch` |
| Binary Source | Official static (Cloudflare) |
| Version | 2026.3.0 |
| Architecture | amd64, arm64 |
| Size | ~30MB |
| Classification | Tier 1 - Network Tunnel |

## What is Cloudflared?

Cloudflared is the client daemon for Cloudflare Tunnels, providing secure outbound connections to Cloudflare's edge without opening inbound ports.

---

## Constraint Compliance Checklist

| ID | Constraint | Status | Notes |
|----|-----------|--------|-------|
| C001 | Non-root (USER 65532) | PASS | |
| C002 | Read-only filesystem | PASS | Runtime flag |
| C003 | No shell in image | PASS | |
| C004 | No package manager | PASS | |
| C005 | Static binary | PASS | |
| C006 | Stripped symbols | PASS | |
| C010 | Health check | PASS | NONE (tunnel-managed) |
| C011 | Signal handling | PASS | |
| C012 | No embedded secrets | PASS | |
| C013 | OCI compliant | PASS | |

---

## Usage

```bash
docker run -d \
  --name cloudflared \
  cloudflared tunnel --no-autoupdate run <tunnel-name>
```

---

## Sources

- Binary: https://github.com/cloudflare/cloudflared/releases
- Documentation: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/

---

**END OF README**
