# Reproducible Builds

This document describes the reproducibility guarantees and workflows for the Evergreen Image Registry.

## Overview

Reproducible builds produce bit-for-bit identical output when given the same source inputs. This registry supports
reproducibility through two mechanisms:

1. **Digest pinning** — base images are referenced by immutable SHA256 digests
2. **Deterministic timestamps** — `SOURCE_DATE_EPOCH` normalises build dates

## Verifying a Build is Reproducible

Build the same commit twice and compare layer digests:

```bash
# Build once
docker buildx build --platform linux/amd64 \
  -t test:v1 \
  --output type=docker,dest=/tmp/v1.tar \
  images/<image>/

# Build again (different machine or time)
docker buildx build --platform linux/amd64 \
  -t test:v2 \
  --output type=docker,dest=/tmp/v2.tar \
  images/<image>/

# Compare
docker load -i /tmp/v1.tar
docker load -i /tmp/v2.tar
docker inspect test:v1 --format '{{json .RootFS.Layers}}' > /tmp/layers1.json
docker inspect test:v2 --format '{{json .RootFS.Layers}}' > /tmp/layers2.json
diff /tmp/layers1.json /tmp/layers2.json
```

If the diff is empty, the build is reproducible.

## Digest Pinning Workflow

Base images referenced by mutable tags (e.g. `wolfi-base:latest`) can change over time, breaking reproducibility. The
`scripts/pin_digests.sh` script resolves tags to SHA256 digests.

### Audit (read-only)

```bash
./scripts/pin_digests.sh
```

Outputs CSV with columns: `image_name, from_line, current_ref, pinned_digest, status`.

### Pin digests in-place

```bash
./scripts/pin_digests.sh --update
```

Modifies Dockerfiles, replacing tags like `wolfi-base:latest` with `wolfi-base:latest@sha256:abcd...`.

### Resolution backends

The script tries, in order:

1. `docker manifest inspect`
2. `skopeo inspect`
3. Docker Registry API v2 via `curl`

At least one of `docker`, `skopeo`, or `curl` must be available.

## SOURCE_DATE_EPOCH

The build pipeline sets `SOURCE_DATE_EPOCH` from the repository push timestamp:

```yaml
env:
  SOURCE_DATE_EPOCH: ${{ github.event.repository.pushed_at }}
```

This causes `GNU date`, `tar`, `zip`, and other tools to use a deterministic timestamp instead of the current wall-clock
time. BuildKit also honours this variable, so layer metadata is consistent across rebuilds.

### Local usage

When building locally and you want reproducible timestamps:

```bash
export SOURCE_DATE_EPOCH=$(git log -1 --format=%ct)
docker buildx build -t myimage:local ./images/<image>/
```

## Known Non-Reproducible Sources

Some images cannot be fully bit-reproducible due to design choices:

| Source                  | Reason                                                                                                         |
| ----------------------- | -------------------------------------------------------------------------------------------------------------- |
| Dynamic `VERSION` ARG   | Downloaded binary version depends on runtime variable; pinning the version arg is required for reproducibility |
| `curl` without checksum | Downloaded artefacts may change if the upstream URL serves different content                                   |
| Go module proxy         | Module dependencies may be updated; use `go.mod` with explicit versions                                        |
| `ARG GITHUB_TOKEN`      | Token-based downloads may hit rate limits and fail intermittently                                              |

### Mitigations

- Always pin `VERSION` ARGs to a specific release
- Verify checksums after downloads (SHA256)
- Pin base images with digests via `scripts/pin_digests.sh`
- Use `SOURCE_DATE_EPOCH` for deterministic timestamps
