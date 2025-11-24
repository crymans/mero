from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


class Settings(ConfigBase):
    model_config = SettingsConfigDict() 

    DATABASE_URL: str
    BOT_TOKEN: str
    JWT_TOKEN: str


settings = Settings()
