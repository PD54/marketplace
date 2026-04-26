from fastapi import FastAPI, Depends, HTTPException

from uuid import UUID
from collections.abc import AsyncGenerator
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import async_session
from app.models.product import Product

from app.pydantic_schemas.responses.get_item_info import getItemInfoResponse


app = FastAPI()


async def get_db() -> AsyncGenerator[AsyncSession]:
    async with async_session() as session:
        yield session


@app.get('/')
async def home() -> str:
    return "This is the homepage."


@app.get('/getItemInfo', response_model=getItemInfoResponse)
async def get_item_info(
    id: Optional[UUID] = None,
    database: AsyncSession = Depends(get_db)
) -> getItemInfoResponse:
    if id:
        product = await database.get(Product, id)
        if not product or product.stock == "not_found":
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    raise HTTPException(status_code=404, detail="No item id provided")