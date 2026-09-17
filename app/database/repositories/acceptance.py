from app.database.dto.acceptance import AcceptanceDTO, UpdateAcceptanceDTO
from app.database.orm_models.acceptance import AcceptanceORM
from app.database.repositories.base import BaseRepository


class AcceptanceRepository(
    BaseRepository[AcceptanceDTO, AcceptanceORM, UpdateAcceptanceDTO]
):
    dto = AcceptanceDTO
    orm_model = AcceptanceORM
