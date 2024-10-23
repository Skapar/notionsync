from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000

class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    auth: str = "/auth"
    page: str = "/page"

class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()

class NotionConfig(BaseModel):
    API_KEY: str
    DATABASE_ID: str

class Settings(BaseSettings):
    url: str
    echo: bool = False
    secret_key: str
    API_KEY: str
    DATABASE_ID: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    # notion: NotionConfig


settings = Settings()
# print(settings.notion.API_KEY)
