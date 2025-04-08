from datetime import timedelta, datetime

import jwt
import bcrypt
from core.config import settings


def encode_jwt_token(payload, private_key: str = settings.auth_JWT.private_key_path.read_text(),
                     algorithm: str = settings.auth_JWT.algorithm,
                     expire_minutes: int = settings.auth_JWT.access_token_expire_minutes,
                     expire_delta: timedelta | None = None,
                     ):
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_delta:
        expire = now + expire_delta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(exp=expire, iat=now)
    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded


def decode_jwt_token(token: str | bytes, public_key: str = settings.auth_JWT.public_key_path.read_text(),
                     algorithm: str = settings.auth_JWT.algorithm):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password)
