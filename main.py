from fastapi import FastAPI

from app.config.logging_config import setup_logging
from app.root_router import root_router
from app.middlewares.request_id import RequestIdMiddleware

setup_logging()

app = FastAPI(title="Marketplace API")

app.add_middleware(RequestIdMiddleware)
app.include_router(root_router)
