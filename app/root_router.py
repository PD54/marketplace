from fastapi import APIRouter

from app.controllers.acceptance_controller import router as acceptance_router
from app.controllers.discount_api import router as discount_router
from app.controllers.sku_controller import router as sku_router

all_routers = [
    sku_router,
    acceptance_router,
    discount_router,
]

root_router = APIRouter()

for router in all_routers:
    root_router.include_router(router)
