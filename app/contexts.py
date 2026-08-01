from contextvars import ContextVar

REQUEST_ID: ContextVar[str | None] = ContextVar("REQUEST_ID", default=None)
