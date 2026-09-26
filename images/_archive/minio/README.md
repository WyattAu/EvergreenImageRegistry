# MinIO (ARCHIVED)

Archived 2026-09-26.

Reason: MinIO removed public distribution. Docker Hub org returns 401
(locked), quay.io returns 401 for anonymous pulls (verified via the
registry API), ghcr mirror 403. No viable anonymous pull source exists
for any tag. Affects: minio, s3, mc, minio-mc, milvus-minio.

If MinIO reopens distribution or you accept authenticated pulls with a
robot account, un-archive and pin the source.
