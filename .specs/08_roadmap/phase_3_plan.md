Stream A: Database Tests (T3.1.1); 16 hours
Stream B: Proxy Tests (T3.1.2); 12 hours
Stream C: Adversarial Tests (T3.1.3); 16 hours
Stream D: Layer Analysis (T3.2.1); 4 hours
Stream E: Startup Benchmarking (T3.2.2); 4 hours
Stream F: Test Config Expansion (T3.1.4); 8 hours
Current functional tests only check that a binary responds to `--version` or `-v`. For databases, this is insufficient -
| postgresql  | `postgres`     | 5432  | RDBMS       | HIGH; needs initdb, data directory |
| postgres    | `postgres`     | 5432  | RDBMS       | HIGH; same as postgresql           |
| mysql       | `mariadbd`     | 3306  | RDBMS       | HIGH; needs data directory         |
| mariadb     | `mariadbd`     | 3306  | RDBMS       | HIGH; same as mysql                |
| mongodb     | `mongod`       | 27017 | Document DB | HIGH; needs data directory         |
| redis       | `redis-server` | 6379  | Key-value   | MEDIUM; in-memory                  |
| redis7      | `redis-server` | 6379  | Key-value   | MEDIUM; in-memory                  |
| sqlite      | `sqlite3`      | N/A   | Embedded    | LOW; file-based                    |
| dragonfly   | `dragonfly`    | 6379  | Key-value   | MEDIUM; Redis-compatible           |
| cockroachdb | `cockroach`    | 26257 | RDBMS       | HIGH; distributed                  |
| memcached   | `memcached`    | 11211 | Key-value   | LOW; simple get/set                |
    # SQLite is embedded: test basic query
        # Not a fail: setuid in scratch images is expected for the main binary
        # This is a warning, not a fail: network restrictions are runtime policy
    # /proc/self/maps: reveals memory layout
    # /proc/1/environ: reveals environment variables of PID 1
5. **CI integration**: Add adversarial test job (may be slow; run in parallel):
   - Variant images (nginx vs nginx-unprivileged; same binary, different ports)