from app.database.dto.discount import DiscountDTO, UpdateDiscountDTO
from app.database.orm_models.discount import DiscountORM
from app.database.repositories.base import BaseRepository


class DiscountRepository(
    BaseRepository[DiscountDTO, DiscountORM, UpdateDiscountDTO]
):
    dto = DiscountDTO
    orm_model = DiscountORM
