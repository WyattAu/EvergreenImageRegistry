| Tier 1 | `FROM scratch`                       | ~104  | CRITICAL; full profiles |
| Tier 1 | `FROM gcr.io/distroless/*`           | ~7    | CRITICAL; full profiles |
| Tier 2 | `FROM debian:bookworm-slim`          | ~87   | HIGH; standard profiles |
| Tier 2 | `FROM cgr.dev/chainguard/wolfi-base` | ~13   | HIGH; standard profiles |
| Tier 3 | Other/Official                       | ~12   | MEDIUM; baseline only   |
Stream A: Seccomp Profiles (T2.1.1); 20 hours, sequential per image type
Stream B: AppArmor Profiles (T2.1.2); 16 hours, sequential per image type
Stream C: Binary Hardening (T2.2.1, T2.2.2); 8 hours combined
Stream D: Capabilities (T2.2.3); 4 hours
Stream E: Size Enforcement (T2.3.1); 2 hours
| CLI tools (cosign, trivy, restic)      | Minimal; mostly read/write/exit                        | May need `execve` for subprocesses |
3. **Handle multi-binary archives**: Some tarballs contain multiple binaries; strip all executables:
         # Has shell: check directly
         # No shell: extract and check
This is informational only; oversized images are pushed to the registry.