from fastapi import FastAPI

from app.controllers import sku_controller

app = FastAPI(title="Marketplace API")
app.include_router(sku_controller.router)


@app.get('/')
async def home() -> str:
    return "API is working."
