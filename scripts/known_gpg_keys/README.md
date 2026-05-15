# Known GPG Keys

This directory stores pre-fetched GPG public keys for projects whose releases are tracked by EvergreenImageRegistry.
These keys are used by `populate_checksums.py` (Layer 2: GPG signature verification) to verify detached signatures on
release artifacts.

## Adding a New Key

1. **Fetch the key from the project's official website** — not from a keyserver. Example sources:
   - `https://etcd.io/docs/latest/op-guide/security/`
   - `https://prometheus.io/docs/prometheus/latest/getting_started/`
   - Project GitHub `KEYS` or `SECURITY` files

2. **Export the ASCII-armored public key:**

   ```bash
   gpg --armor --export <KEY_ID> > scripts/known_gpg_keys/<project>.asc
   ```

3. **Verify the key fingerprint** matches what the project publishes.

## File Format

Each key file is named `{project}.asc` where `{project}` is the lowercase project name (e.g. `etcd.asc`,
`prometheus.asc`, `containerd.asc`).

## Importing Keys (for local verification)

```bash
gpg --import scripts/known_gpg_keys/<project>.asc
```

Or import all keys at once:

```bash
for key in scripts/known_gpg_keys/*.asc; do
    gpg --import "$key"
done
```

## Security Notes

- Keys **must** be fetched from the project's official website or official documentation. Do not rely solely on
  keyservers, as keyserver lookups are not authenticated.
- Review key fingerprints against project documentation before committing.
- This directory is committed to the repository so that CI can verify signatures without network access to keyservers.
- If a project rotates its signing key, update the `.asc` file here and verify the new fingerprint.
