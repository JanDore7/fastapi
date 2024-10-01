import os

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_NAME : str
    DB_HOST : str
    DB_PORT : int
    DB_USER : str
    DB_PASSWORD : str

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), '..', '.env'),
        extra='ignore'
    )

settings = Settings()


if __name__ == '__main__':
    print(settings.DB_URL)
