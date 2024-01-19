from datetime import datetime, timedelta

import jwt
from fastapi.security import HTTPBearer
from passlib.context import CryptContext
from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminUser, AuthProvider
from starlette_admin.exceptions import FormValidationError, LoginFailed

from src.settings import settings

users = {
    "dolphine": {
        "name": "Funny Dolphine Admin",
        "roles": ["read", "write", "update", "delete"],
    },
}


class ExpiredAccessToken(BaseException):
    pass


class InvalidAccessToken(BaseException):
    pass


class Authenticator:
    _algorithm = "HS256"
    _access_token_expires_minutes = 60

    auth_scheme = HTTPBearer()
    pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")
    _secret_key = settings.jwt_secret_key

    def validated_token_payload(self, access_token: str):
        try:
            payload = jwt.decode(
                access_token, key=self._secret_key, algorithms=[self._algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise ExpiredAccessToken
        except jwt.InvalidSignatureError:
            raise InvalidAccessToken

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(password, hashed_password)

    def create_access_token(self, username: str) -> str:
        to_encode = {
            "sub": {"username": username},
            "exp": datetime.utcnow()
            + timedelta(minutes=self._access_token_expires_minutes),
        }
        encoded_jwt = jwt.encode(to_encode, self._secret_key, algorithm=self._algorithm)
        return encoded_jwt

    async def authenticate_user(self, username: str, password: str):
        if not self.verify_password(password, settings.admin_password):
            return
        return {"username": username}


class ServiceAuthProvider(AuthProvider):
    _authenticator = Authenticator()

    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response:
        if len(username) < 3:
            raise FormValidationError(
                {"username": "Ensure username has at least 03 characters"}
            )

        if username in users and self._authenticator.verify_password(
            password, settings.admin_password
        ):
            token = self._authenticator.create_access_token(username)
            request.session.update({"token": token})
            return response

        raise LoginFailed("Invalid username or password")

    async def is_authenticated(self, request) -> bool:
        if "token" in request.session:
            try:
                payload = self._authenticator.validated_token_payload(
                    request.session["token"]
                )
            except ExpiredAccessToken:
                return False
            except InvalidAccessToken:
                return False

            request.state.user = users.get(payload["sub"]["username"])
            return True
        return False

    def get_admin_user(self, request: Request) -> AdminUser:
        user = request.state.user
        return AdminUser(username=user["name"])

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response
