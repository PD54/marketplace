from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import update as sa_update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dto.base import BaseDTO, UpdateBaseDTO
from app.database.orm_models.base import BaseORM


class BaseRepository[
    DTO: BaseDTO,
    ORMModel: BaseORM,
    UpdateDTO: UpdateBaseDTO,
]:
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

    async def update(
        self,
        entity_id: UUID,
        update_dto: UpdateDTO,
    ) -> DTO | None:
        update_fields = update_dto.model_dump(exclude_unset=True)
        update_fields["updated_at"] = datetime.now(UTC)

        result = await self.database.scalars(
            sa_update(self.orm_model)
            .where(self.orm_model.id == entity_id)
            .values(update_fields)
            .returning(self.orm_model)
        )
        obj = result.one_or_none()
        return self.dto.model_validate(obj) if obj else None
