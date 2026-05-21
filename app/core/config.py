from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7
    smtp_user: str
    cloudinary_cloud_name: str
    cloudinary_api_key: str
    cloudinary_api_secret: str
    smtp_password: str
    domain: str = "https://lerna-backend.vercel.app"
    frontend_url: str = "https://lerna-frontend.vercel.app"
    secret_key: str = "supersecretkeythatisatleast32chars!"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
