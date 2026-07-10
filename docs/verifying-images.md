# Verifying Evergreen Images

All Evergreen Image Registry images are signed, attested, and verifiable using Sigstore (cosign).

## Prerequisites

Install cosign:

```bash
# macOS
brew install cosign

# Linux
curl -sLO "https://github.com/sigstore/cosign/releases/latest/download/cosign-linux-amd64"
chmod +x cosign-linux-amd64
sudo mv cosign-linux-amd64 /usr/local/bin/cosign
```

## Verify Image Signature

Every image is signed using keyless signing (Sigstore OIDC via GitHub Actions):

```bash
cosign verify ghcr.io/wyattau/evergreenimageregistry/redis:latest \
  --certificate-identity-regexp "https://github.com/WyattAu/EvergreenImageRegistry/" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com"
```

## Verify SPDX SBOM Attestation

```bash
cosign verify-attestation ghcr.io/wyattau/evergreenimageregistry/redis:latest \
  --type spdxjson \
  --certificate-identity-regexp "https://github.com/WyattAu/EvergreenImageRegistry/" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com"
```

## Verify CycloneDX SBOM Attestation

```bash
cosign verify-attestation ghcr.io/wyattau/evergreenimageregistry/redis:latest \
  --type cyclonedx \
  --certificate-identity-regexp "https://github.com/WyattAu/EvergreenImageRegistry/" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com"
```

## Verify SLSA Provenance Attestation

```bash
cosign verify-attestation ghcr.io/wyattau/evergreenimageregistry/redis:latest \
  --type slsaprovenance \
  --certificate-identity-regexp "https://github.com/WyattAu/EvergreenImageRegistry/" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com"
```

## Download SBOM

```bash
# Download SPDX SBOM
cosign download attestation ghcr.io/wyattau/evergreenimageregistry/redis:latest \
  | jq -r .payload | base64 -d | jq

# Or use syft to generate a local SBOM
syft ghcr.io/wyattau/evergreenimageregistry/redis:latest
```

## Supply Chain Summary

| Artifact        | Method                           | How to Verify                                     |
| --------------- | -------------------------------- | ------------------------------------------------- |
| Image signature | Cosign keyless (Sigstore)        | `cosign verify`                                   |
| SPDX SBOM       | Syft + cosign attest             | `cosign verify-attestation --type spdxjson`       |
| CycloneDX SBOM  | Syft + cosign attest             | `cosign verify-attestation --type cyclonedx`      |
| SLSA provenance | Custom predicate + cosign attest | `cosign verify-attestation --type slsaprovenance` |
