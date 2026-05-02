from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = 'Restaurant Ops Dashboard'
    database_url: str = 'sqlite:///./app.db'
    backend_cors_origins: str = 'http://localhost:3000'
    email_host: str = 'imap.gmail.com'
    email_port: int = 993
    email_user: str = ''
    email_password: str = ''
    email_folder: str = 'INBOX'
    email_processed_folder: str = 'Processed'
    email_error_folder: str = 'Errors'
    uploads_dir: str = 'uploads'

    class Config:
        env_file = '.env'

settings = Settings()
