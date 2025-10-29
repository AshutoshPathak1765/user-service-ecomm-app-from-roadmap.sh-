from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions import UserNotFoundError, UserAlreadyExistsError


async def user_not_found_exception_handler(request: Request, exc: UserNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"error": "User Not Found", "detail": str(exc)},
    )


async def user_already_exists_exception_handler(request: Request, exc: UserAlreadyExistsError):
    return JSONResponse(
        status_code=400,
        content={"error": "Duplicate Entry", "detail": str(exc)},
    )
