from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    personal_access_token: str

    class Config:
        env_file = ".env"

settings = Settings() # type: ignore