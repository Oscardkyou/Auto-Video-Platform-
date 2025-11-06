from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class TemporalSettings(BaseSettings):
    hostname: str = Field(default="temporal", description="Temporal server host")
    port: int = Field(default=7233, description="Temporal server RPC порт")
    namespace: str = Field(default="default", description="Temporal namespace")

    model_config = SettingsConfigDict(env_prefix="TEMPORAL_", env_file_encoding="utf-8")


class DatabaseSettings(BaseSettings):
    url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@postgres:5432/auto_video",
        description="Строка подключения к основной БД",
    )

    model_config = SettingsConfigDict(env_prefix="DB_", env_file_encoding="utf-8")


class StorageSettings(BaseSettings):
    endpoint_url: str = Field(default="http://minio:9000")
    access_key: str = Field(default="minioadmin")
    secret_key: str = Field(default="minioadmin")
    bucket_assets: str = Field(default="assets")

    model_config = SettingsConfigDict(env_prefix="STORAGE_", env_file_encoding="utf-8")


class ExternalAPISettings(BaseSettings):
    meta_app_id: str | None = Field(default=None)
    meta_app_secret: str | None = Field(default=None)
    youtube_api_key: str | None = Field(default=None)
    tiktok_client_id: str | None = Field(default=None)

    model_config = SettingsConfigDict(env_prefix="EXT_", env_file_encoding="utf-8")


class SecuritySettings(BaseSettings):
    secret_key: str = Field(default="dev-secret-key")
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=60)

    model_config = SettingsConfigDict(env_prefix="AUTH_", env_file_encoding="utf-8")


class DemoUserSettings(BaseSettings):
    admin_email: str = Field(default="admin@example.com")
    admin_password: str = Field(default="admin123")

    model_config = SettingsConfigDict(env_prefix="DEMO_", env_file_encoding="utf-8")


class AppSettings(BaseSettings):
    environment: str = Field(default="local")
    log_level: str = Field(default="INFO")

    temporal: TemporalSettings = TemporalSettings()
    database: DatabaseSettings = DatabaseSettings()
    storage: StorageSettings = StorageSettings()
    external_api: ExternalAPISettings = ExternalAPISettings()
    security: SecuritySettings = SecuritySettings()
    demo_user: DemoUserSettings = DemoUserSettings()

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="APP_",
        extra="ignore",
    )


settings = AppSettings()
