from app.database.repositories.base import BaseRepository
from app.database.dto.good import GoodDTO
from app.database.orm_models.good import GoodORM


class GoodRepository(BaseRepository[GoodDTO, GoodORM]):
    dto = GoodDTO
    orm_model = GoodORM
