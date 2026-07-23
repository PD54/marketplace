from app.database.repositories.base import BaseRepository
from app.database.dto.product import ProductDTO
from app.database.orm_models.product import ProductORM


class ProductRepository(BaseRepository[ProductDTO, ProductORM]):
    dto = ProductDTO
    orm_model = ProductORM
