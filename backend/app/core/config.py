import os
from typing import Optional
from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Car Color Studio"
    
    # CORS settings
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    
    # File storage settings
    UPLOAD_DIR: str = "uploads"
    MASK_DIR: str = "masks"
    ANALYSIS_DIR: str = "analyses"
    OUTPUT_DIR: str = "output"
    
    # External masking API settings
    MASKING_API_URL: Optional[str] = os.getenv("MASKING_API_URL", "https://6497-34-90-189-112.ngrok-free.app/")
    
    # Create necessary directories
    def initialize_directories(self):
        base_path = Path("storage")
        for dir_name in [self.UPLOAD_DIR, self.MASK_DIR, self.ANALYSIS_DIR, self.OUTPUT_DIR]:
            full_path = base_path / dir_name
            full_path.mkdir(parents=True, exist_ok=True)

settings = Settings()
