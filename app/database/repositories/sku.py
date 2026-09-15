from sqlalchemy.dialects.postgresql import insert

from app.database.dto.sku import SkuDTO, UpdateSkuDTO
from app.database.orm_models.sku import SkuORM
from app.database.repositories.base import BaseRepository


class SkuRepository(BaseRepository[SkuDTO, SkuORM, UpdateSkuDTO]):
    dto = SkuDTO
    orm_model = SkuORM

    async def create_or_do_nothing(self, sku_dto: SkuDTO) -> SkuDTO | None:
        res = await self.database.scalars(
            insert(self.orm_model)
            .values(sku_dto.model_dump())
            .on_conflict_do_nothing(index_elements=[self.orm_model.id])
            .returning(self.orm_model)
        )
        obj = res.one_or_none()
        return self.dto.model_validate(obj) if obj else None
