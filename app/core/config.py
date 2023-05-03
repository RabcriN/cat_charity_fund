from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'QRKot'
    description: str = 'API для приложения QRKot'
    database_url: str = 'sqlite+aiosqlite'
    secret: str = 'SECRET'

    class Config:
        env_file = '.env'


settings = Settings()
