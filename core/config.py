from datetime import timedelta
from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent
DB_PATH = Path(BASE_DIR / "store_pc.db")


class DbSettings(BaseModel):
    url: str = f"sqlite+aiosqlite:///{DB_PATH}"
    echo: bool = False


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt_private_key.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt_public_key.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15


class Settings(BaseSettings):
    api_v1_prefix: str = '/api/v1'
    alembic_prefix: str = '/alembic'
    db: DbSettings = DbSettings()
    auth_JWT: AuthJWT = AuthJWT()


settings = Settings()
