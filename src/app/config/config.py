from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000

class Settings(BaseSettings):
    url: str
    echo: bool = False
    secret_key: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    
    run: RunConfig = RunConfig()


settings = Settings()
