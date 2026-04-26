from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from app.database.dto.base import BaseDTO
from app.database.orm_models.base import BaseORM


class BaseRepository[DTO: BaseDTO, ORMModel: BaseORM]:
    dto: type[DTO]
    orm_model: type[ORMModel]

    def __init__(self, database: AsyncSession):
        self.database = database

    async def get_by_id(self, entity_id: UUID) -> DTO | None:
        res = await self.database.get(self.orm_model, entity_id)
        if not res:
            return None
        return self.dto.model_validate(res)
    
    async def create(self, data: DTO) -> DTO:
        result = await self.database.scalars(
            insert(self.orm_model)
            .values(data.model_dump())
            .returning(self.orm_model)
        )
        return self.dto.model_validate(result.one())
