from app.database.dto.good import GoodDTO
from app.database.orm_models.good import GoodORM
from app.database.repositories.base import BaseRepository


class GoodRepository(BaseRepository[GoodDTO, GoodORM]):
    dto = GoodDTO
    orm_model = GoodORM
