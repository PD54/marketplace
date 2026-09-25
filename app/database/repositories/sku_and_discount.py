from uuid import UUID

from sqlalchemy import select

from app.database.dto.sku_and_discount import (
    SkuAndDiscountDTO,
    UpdateSkuAndDiscountDTO,
)
from app.database.orm_models.sku_and_discount import SkuAndDiscountORM
from app.database.repositories.base import BaseRepository


class SkuAndDiscountRepository(
    BaseRepository[
        SkuAndDiscountDTO,
        SkuAndDiscountORM,
        UpdateSkuAndDiscountDTO,
    ]
):
    dto = SkuAndDiscountDTO
    orm_model = SkuAndDiscountORM

    async def get_by_sku_id(self, sku_id: UUID) -> list[SkuAndDiscountDTO]:
        result = await self.database.scalars(
            select(self.orm_model).where(self.orm_model.sku_id == sku_id)
        )
        return [self.dto.model_validate(obj) for obj in result]

    async def get_by_discount_id(
        self,
        discount_id: UUID,
    ) -> list[SkuAndDiscountDTO]:
        result = await self.database.scalars(
            select(self.orm_model).where(
                self.orm_model.discount_id == discount_id
            )
        )
        return [self.dto.model_validate(obj) for obj in result]
