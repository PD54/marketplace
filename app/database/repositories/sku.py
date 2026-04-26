from app.database.repositories.base import BaseRepository
from app.database.dto.sku import SkuDTO
from app.database.orm_models.sku import SkuORM


class SkuRepository(BaseRepository[SkuDTO, SkuORM]):
    dto = SkuDTO
    orm_model = SkuORM
