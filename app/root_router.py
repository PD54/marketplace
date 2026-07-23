from fastapi import APIRouter

from app.controllers.sku_controller import router as sku_router

all_routers = [
    sku_router,
]

root_router = APIRouter()

for router in all_routers:
    root_router.include_router(router)
