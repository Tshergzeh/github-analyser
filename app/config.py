from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    personal_access_token: str
    redis_host: str
    redis_port: int
    redis_username: str
    redis_password: str
    cache_ttl: int

    class Config:
        env_file = ".env"

settings = Settings() # type: ignore