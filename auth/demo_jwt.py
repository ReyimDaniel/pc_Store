import profile

from jwt import InvalidTokenError
from fastapi import APIRouter, Depends, HTTPException, Form, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer

from models.user import UserSchema
from auth import service_jwt as auth_service
from auth.token_model import TokenInfo

router = APIRouter(prefix="/auth", tags=["auth"])

# http_bearer = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/jwt/auth/login")

daniel = UserSchema(
    username="daniel",
    password=auth_service.hash_password("qwerty"),
    email="danil@mail.ru",
    active=True
)

alex = UserSchema(
    username="alex",
    password=auth_service.hash_password("always"),
    active=True
)
users_db: dict[str, UserSchema] = {
    daniel.username: daniel,
    alex.username: alex,
}


def validate_auth_user_login(username: str = Form(),
                             password: str = Form(),
                             ):
    unauth_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    if not (user := users_db.get(username)):
        raise unauth_exception
    if auth_service.validate_password(password=password, hashed_password=user.password):
        return user
    if not user.active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return user


def get_current_token_payload(
        # credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        token: str = Depends(oauth2_scheme),
) -> UserSchema:
    # token = credentials.credentials
    try:
        payload = auth_service.decode_jwt_token(token=token)
        print(f"payload: {payload}")
    except InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token error: {e}")
    return payload


def get_current_auth_user(
        payload: dict = Depends(get_current_token_payload)
) -> UserSchema:
    username: str | None = payload.get("sub")
    if user := users_db.get(username):
        return user
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def get_current_active_auth_user(user: UserSchema = Depends(get_current_auth_user)):
    if user.active:
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User must be active")


@router.post("/login")
def auth_user_issue_jwt(user: UserSchema = Depends(validate_auth_user_login)):
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }
    access_token = auth_service.encode_jwt_token(jwt_payload)
    return TokenInfo(
        access_token=access_token,
        token_type="Bearer"
    )


@router.get("/users/me/")
def auth_user_check_self_info(payload: dict = Depends(get_current_token_payload),
                              user: UserSchema = Depends(get_current_active_auth_user),
                              ):
    iat = payload.get("iat")
    return {
        "username": user.username,
        "email": user.email,
        "logged_in": iat,
    }
