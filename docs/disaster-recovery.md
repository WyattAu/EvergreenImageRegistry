# Disaster Recovery Procedures

## Overview

This document covers disaster recovery procedures for the Evergreen Image Registry, including rollback, backup
restoration, full rebuilds, and emergency contacts.

## 1. Rollback Procedures for Bad Image Pushes

### 1.1 Immediate Rollback (Registry Level)

If a bad image is pushed to GHCR, immediately deprecate the tag:

```bash
# Identify the bad image and tag
BAD_IMAGE="ghcr.io/wyattau/evergreenimageregistry/<image>:<bad-tag>"
GOOD_TAG="v28.0.0"  # Last known good version

# Pull the last known good version
docker pull "${GOOD_TAG}"

# Re-tag and push as the current version
docker tag "${GOOD_TAG}" "ghcr.io/wyattau/evergreenimageregistry/<image>:latest"
docker push "ghcr.io/wyattau/evergreenimageregistry/<image>:latest"
```

### 1.2 Git Rollback (Source Level)

Revert the commit that introduced the bad image:

```bash
# Find the commit that introduced the change
git log --oneline -- images/<bad-image>/

# Revert the specific commit
git revert <commit-hash>

# Push the revert
git push origin main
```

### 1.3 CI/CD Pipeline Rollback

If the nightly build produced bad images, disable the workflow and rebuild:

```bash
# Temporarily disable nightly builds
gh workflow disable build-nightly.yml

# Manually trigger a build with the last good SHA
gh workflow run build-on-demand.yml \
  --field tag=<last-good-sha> \
  --field images=<image-list>
```

## 2. Backup Restoration (Shim Backup System)

### 2.1 Backup Overview

The evergreen shim provides backup capabilities for stateful images (databases, caches). Key environment variables:

| Variable                     | Description               | Default     |
| ---------------------------- | ------------------------- | ----------- |
| `SHIM_BACKUP_ENABLED`        | Enable/disable backups    | `false`     |
| `SHIM_BACKUP_SCHEDULE`       | Cron schedule for backups | `0 2 * * *` |
| `SHIM_BACKUP_RETENTION_DAYS` | Days to keep backups      | `7`         |
| `SHIM_BACKUP_OUTPUT_DIR`     | Backup output directory   | `/backups`  |
| `SHIM_BACKUP_DB_HOST`        | Database host             | `localhost` |
| `SHIM_BACKUP_DB_PORT`        | Database port             | `5432`      |

### 2.2 Restoring PostgreSQL from Backup

```bash
# List available backups
ls -la /backups/postgresql-17/

# Restore from a specific backup
docker exec -it <container> /usr/local/bin/shim backup restore \
  --backup-file /backups/postgresql-17/backup-20260601-020000.sql.gz \
  --db-name mydb

# Manual restore with pg_restore
docker exec -it <container> pg_restore -U postgres -d mydb /backups/backup.sql
```

### 2.3 Restoring Redis/Valkey from RDB

```bash
# Stop the container
docker stop <redis-container>

# Copy RDB file
docker cp <redis-container>:/data/dump.rdb ./dump.rdb

# Restore RDB file
docker cp ./dump.rdb <redis-container>:/data/dump.rdb

# Start the container
docker start <redis-container>
```

### 2.4 Restoring Kafka Data

```bash
# Kafka topics are stored in /opt/kafka/data
# Restore from backup
docker cp /backups/kafka/<backup-date>/ <kafka-container>:/opt/kafka/data/

# Verify topic data
docker exec -it <kafka-container> /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 --list
```

## 3. Rebuilding All Images from Source

### 3.1 Full Rebuild (Local)

```bash
# Build all images locally
for image in images/*/; do
  name=$(basename "$image")
  [[ "$name" == _* ]] && continue
  echo "Building ${name}..."
  docker build -t "evergreen-${name}" "${image}"
done
```

### 3.2 Full Rebuild (CI/CD)

Trigger a full nightly build:

```bash
# Via GitHub CLI
gh workflow run build-nightly.yml --field tier=all --field sign=true

# Via GitHub Actions UI
# Navigate to Actions > Nightly Full Rebuild > Run workflow
```

### 3.3 Rebuilding Specific Tiers

```bash
# Critical tier only (databases, proxies, CI tools)
gh workflow run build-nightly.yml --field tier=critical

# Standard tier
gh workflow run build-nightly.yml --field tier=standard

# Community tier
gh workflow run build-nightly.yml --field tier=community
```

### 3.4 Rebuilding a Single Image

```bash
# Via GitHub CLI
gh workflow run build-on-demand.yml --field images=nginx

# Via Docker directly
docker build -t ghcr.io/wyattau/evergreenimageregistry/nginx:local images/nginx/
```

## 4. Emergency Contact Procedures

### 4.1 Severity Levels

| Level             | Description                           | Response Time     | Example                        |
| ----------------- | ------------------------------------- | ----------------- | ------------------------------ |
| **P0 - Critical** | Registry down, all images unavailable | Immediate         | GHCR outage, compromised image |
| **P1 - High**     | Single critical image broken          | < 1 hour          | PostgreSQL build failure       |
| **P2 - Medium**   | Non-critical image broken             | < 4 hours         | Monitoring image build failure |
| **P3 - Low**      | Cosmetic or documentation issue       | Next business day | Label inconsistency            |

### 4.2 Contact Chain

1. **Primary Maintainer**: WyattAu (repository owner)
2. **Security Team**: Report via GitHub Security Advisories
3. **Infrastructure**: Check GitHub Actions status at https://www.githubstatus.com/

### 4.3 Communication Channels

- **GitHub Issues**: For non-urgent bugs and feature requests
- **GitHub Security Advisories**: For security vulnerabilities
- **GitHub Discussions**: For questions and community support
- **Repository README**: For emergency procedures and status

### 4.4 Incident Response Checklist

1. **Identify** the scope of the issue (single image, tier, or all)
2. **Contain** by disabling affected workflows if needed
3. **Communicate** status via GitHub Issues/Security Advisories
4. **Remediate** using rollback or rebuild procedures
5. **Verify** with `evergreenctl verify` and pre-push gate
6. **Document** the incident in a post-mortem

## 5. Recovery Time & Recovery Point Objectives

### 5.1 RTO (Recovery Time Objective)

| Scenario                | Target RTO   | Method                               |
| ----------------------- | ------------ | ------------------------------------ |
| Single image failure    | < 5 minutes  | Rebuild with `build-on-demand`       |
| Tier failure (critical) | < 30 minutes | Rebuild tier with `build-nightly`    |
| Full registry failure   | < 2 hours    | Full rebuild with `build-nightly`    |
| GHCR outage             | < 1 hour     | Wait for GHCR recovery, then rebuild |

### 5.2 RPO (Recovery Point Objective)

| Scenario             | Target RPO | Backup Method                      |
| -------------------- | ---------- | ---------------------------------- |
| PostgreSQL data      | < 24 hours | SHIM_BACKUP_SCHEDULE (daily)       |
| Redis/Valkey data    | < 1 hour   | RDB snapshots + AOF                |
| Kafka data           | < 1 hour   | Topic replication + snapshots      |
| Image configurations | 0 (Git)    | Git history is the source of truth |

### 5.3 Verification After Recovery

```bash
# Verify all images
evergreenctl verify images/

# Check for drift
evergreenctl drift images/

# Run pre-push gate
bash .github/workflows/pre-push-gate.sh

# Verify specific image
evergreenctl verify images/postgresql-17/
```

## 6. Prevention Measures

- **Pre-commit hooks**: 9 hooks validate Dockerfiles before commit
- **Pre-push gate**: 11 quality checks before pushing
- **Nightly scans**: `nightly-scan.yml` and `daily-security-scan.yml`
- **SBOM generation**: Every image gets an SPDX 2.3 SBOM
- **Cosign signing**: Critical images are signed with Sigstore
- **SLSA provenance**: Build provenance attestations for supply chain security
