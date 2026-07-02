# X86_64 unknown linux musl

Evergreen Rust static build base for x86_64-unknown-linux-musl target

| Attribute | Value |
|-----------|-------|
| Version | unknown |
| Tier | 3 |
| Base Image | cgr.dev/chainguard/static:latest |
| Architecture | amd64 |
| Health Check | none |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/x86_64-unknown-linux-musl:unknown
```

## Security

- Non-root by default
- HEALTHCHECK disabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
