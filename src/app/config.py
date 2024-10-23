from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    auth: str = "/auth"
    page: str = "/page"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class DatabaseConfig(BaseModel):
    url: str
    echo: bool = False


class JWTConfig(BaseModel):
    secret_key: str = Field(..., description="JWT secret key")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 5


class NotionConfig(BaseModel):
    api_key: str = Field(..., description="API key for Notion integration")
    database_id: str = Field(..., description="Database ID for Notion")


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class Settings(BaseSettings):
    notion: NotionConfig
    db: DatabaseConfig
    jwt: JWTConfig
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="allow",
    )



settings = Settings()
