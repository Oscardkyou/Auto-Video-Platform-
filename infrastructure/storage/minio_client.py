from __future__ import annotations

from datetime import timedelta

from minio import Minio
from minio.commonconfig import Tags
from minio.error import S3Error

from config.settings import settings


def get_minio_client() -> Minio:
    endpoint = settings.storage.endpoint_url.replace("http://", "").replace("https://", "")
    secure = settings.storage.endpoint_url.startswith("https://")
    return Minio(
        endpoint,
        access_key=settings.storage.access_key,
        secret_key=settings.storage.secret_key,
        secure=secure,
    )


def ensure_bucket_exists(bucket: str) -> None:
    client = get_minio_client()
    found = client.bucket_exists(bucket)
    if not found:
        client.make_bucket(bucket)


def create_presigned_put(
    *,
    bucket: str,
    object_key: str,
    expires: timedelta = timedelta(minutes=15),
    content_type: str | None = None,
) -> str:
    client = get_minio_client()
    params = {"response-content-type": content_type} if content_type else None
    return client.presigned_put_object(bucket, object_key, expires=expires, response_headers=params)


def create_presigned_get(
    *,
    bucket: str,
    object_key: str,
    expires: timedelta = timedelta(minutes=60),
) -> str:
    client = get_minio_client()
    return client.presigned_get_object(bucket, object_key, expires=expires)
