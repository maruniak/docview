from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    DOCUMENTS_DIR: Path = Path("/app/documents")
    PREVIEW_DIR: Path = Path("/app/previews")
    CONVERTED_FORMAT: str = "pdf"
    EXTERNAL_PORT: int = 40871  # Define external_port
    
    WINDOWS_SERVER_IP: str
    WINDOWS_SERVER_PORT: int
    API_PORT: int = 8000
    ACCESS_TOKEN: str
    AUTHENTICATION_ENABLED: bool    
    
    class Config:
        env_file = ".env"

settings = Settings()
