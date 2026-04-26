from fastapi import FastAPI

from app.root_router import root_router

app = FastAPI(title="Marketplace API")
app.include_router(root_router)
