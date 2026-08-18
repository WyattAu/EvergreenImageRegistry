# Evergreenctl Fuzz Testing

Fuzz targets for finding edge cases and panics in critical parsing code.

## Targets

| Target | What it fuzzes |
|--------|---------------|
| `fuzz_dockerfile_parsing` | All 14 Dockerfile extraction functions |
| `fuzz_manifest_parsing` | TOML manifest deserialization |
| `fuzz_version_comparison` | Semver comparison and version safety checks |
| `fuzz_constraint_validation` | Policy constraint engine with random inputs |

## Prerequisites

```bash
cargo install cargo-fuzz
```

## Running

```bash
# Run all fuzz targets (10 minutes each)
cargo fuzz run fuzz_dockerfile_parsing -- -max_total_time=600
cargo fuzz run fuzz_manifest_parsing -- -max_total_time=600
cargo fuzz run fuzz_version_comparison -- -max_total_time=600
cargo fuzz run fuzz_constraint_validation -- -max_total_time=600

# Run with more iterations
cargo fuzz run fuzz_dockerfile_parsing -- -max_total_time=3600

# Run specific target with custom config
cargo fuzz run fuzz_dockerfile_parsing -- -rss_limit_mb=4096 -max_len=4096
```

## Interpreting Results

- **Panics**: Any panic indicates a bug that must be fixed
- **Timeouts**: May indicate ReDoS or excessive computation
- **OOM**: Increase `rss_limit_mb` or reduce `max_len`

## Regression corpus

Fuzz corpora are stored in `fuzz/artifacts/`. To add a regression test:

```bash
# Minimize a failing input
cargo fuzz tmin fuzz_dockerfile_parsing <crash-file>

# Then add it to the unit tests in evergreenctl/src/
```
