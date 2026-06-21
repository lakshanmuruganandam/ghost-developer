from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Ghost Developer"
    environment: str = "production"
    github_token: str = "placeholder_token"
    llm_api_key: str = "placeholder_key"
    repo_path: str = "/tmp/repo"
    
    class Config:
        env_file = ".env"

settings = Settings()
