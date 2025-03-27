from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent
DB_PATH = Path(BASE_DIR / "store_pc.db")


class DbSettings(BaseModel):
    url: str = f"sqlite+aiosqlite:///{DB_PATH}"
    echo: bool = False


class Settings(BaseSettings):
    api_v1_prefix: str = '/api/v1'
    alembic_prefix: str = '/alembic'
    db: DbSettings = DbSettings()


settings = Settings()
