| Base image         | Minimal         | Updated          | CIS: prefer updated; **Implemented via universal preference order (ADR-007)** |
| CVE tolerance      | 0 critical      | Updated priority | NIST: 0 critical; **C007: Zero Critical/High CVEs**                           |
| Privilege dropping | Recommended     | Required         | Use most restrictive: CIS; **C001: Non-root UID 65532**                       |
| Static linking | Yes          | Recommended    | Both: preferred; **C005**               |
| Debug symbols  | No           | Explicit       | Both: stripped; **C006**                |
**Resolution:** **Eliminated tier-based mapping entirely.** See ADR-007; universal preference order applies to all
- scratch: No shell (enforced; no OS)
- wolfi: BusyBox ash present (acceptable; needed for entrypoint scripts)
- UBI micro/minimal/standard: bash present (acceptable; needed for entrypoint and debugging)