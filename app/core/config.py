from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_env: str = "development"
    app_debug: bool = True
    log_level: str = "INFO"
    use_mock: bool = True

    # OpenStack
    os_auth_url: str = "http://localhost:5000/v3"
    os_username: str = "admin"
    os_password: str = "secret"
    os_project_name: str = "admin"
    os_user_domain_name: str = "Default"
    os_project_domain_name: str = "Default"

    class Config:
        env_file = ".env"

settings = Settings()