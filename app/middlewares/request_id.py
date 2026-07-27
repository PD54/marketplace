from collections.abc import Callable, Awaitable
from uuid import uuid7

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.contexts import REQUEST_ID


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        REQUEST_ID.set(str(uuid7()))
        response = await call_next(request)
        return response
