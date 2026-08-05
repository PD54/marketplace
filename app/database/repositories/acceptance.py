from app.database.dto.acceptance import AcceptanceDTO
from app.database.orm_models.acceptance import AcceptanceORM
from app.database.repositories.base import BaseRepository


class AcceptanceRepository(BaseRepository[AcceptanceDTO, AcceptanceORM]):
    dto = AcceptanceDTO
    orm_model = AcceptanceORM
