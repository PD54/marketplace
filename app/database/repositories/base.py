from uuid import UUID

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dto.base import BaseDTO
from app.database.orm_models.base import BaseORM


class BaseRepository[DTO: BaseDTO, ORMModel: BaseORM]:
    dto: type[DTO]
    orm_model: type[ORMModel]

    def __init__(self, database: AsyncSession):
        self.database = database

    async def get_by_id(self, entity_id: UUID) -> DTO | None:
        result = await self.database.get(self.orm_model, entity_id)
        if not result:
            return None
        return self.dto.model_validate(result)

    async def create(self, data: DTO) -> DTO:
        result = await self.database.scalars(
            insert(self.orm_model)
            .values(data.model_dump())
            .returning(self.orm_model)
        )
        return self.dto.model_validate(result.one())

    async def bulk_create(self, list_of_dto: list[DTO]) -> list[DTO]:
        if not list_of_dto:
            return []

        result = await self.database.scalars(
            insert(self.orm_model)
            .values([dto.model_dump() for dto in list_of_dto])
            .returning(self.orm_model)
        )
        return [self.dto.model_validate(obj) for obj in result]
