from uuid import UUID

from sqlalchemy import select

from app.database.dto.good import GoodDTO, GoodStock, UpdateGoodDTO
from app.database.orm_models.good import GoodORM
from app.database.repositories.base import BaseRepository


class GoodRepository(BaseRepository[GoodDTO, GoodORM, UpdateGoodDTO]):
    dto = GoodDTO
    orm_model = GoodORM

    async def grab_avail_by_sku_and_stock(
        self,
        sku_id: UUID,
        stock: GoodStock,
    ) -> GoodDTO | None:
        result = await self.database.scalars(
            select(self.orm_model)
            .where(
                self.orm_model.sku_id == sku_id,
                self.orm_model.stock == stock,
                self.orm_model.reserved_state.is_(False),
            )
            .limit(1)
            .with_for_update()
        )

        obj = result.one_or_none()
        return GoodDTO.model_validate(obj) if obj else None
