import json

from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.responses import JSONResponse

from src.web.factory import create_app

app = create_app()


@app.exception_handler(RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):  # noqa
    if not isinstance(exc, RequestValidationError):
        exc_json = json.loads(exc.json())
    else:
        exc_json = exc.errors()

    response = {"errors": []}
    for error in exc_json:
        try:
            response["errors"].append({error["loc"][-1]: f"{error['msg']}"})
        except IndexError:
            response["errors"].append(
                {"error": f"This shouldn't be happening. Response {error['msg']}"}
            )

    return JSONResponse(response, status_code=422)
