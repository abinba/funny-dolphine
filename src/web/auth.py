from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminUser, AuthProvider
from starlette_admin.exceptions import FormValidationError, LoginFailed

from src.core.auth import Authenticator
from src.core.exceptions import ExpiredAccessToken, InvalidAccessToken
from src.settings import settings

users = {
    "dolphine": {
        "name": "Funny Dolphine Admin",
        "roles": ["read", "write", "update", "delete"],
    },
}


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
