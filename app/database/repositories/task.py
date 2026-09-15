from uuid import UUID

from sqlalchemy import select

from app.database.dto.task import TaskDTO, UpdateTaskDTO
from app.database.orm_models.task import TaskORM
from app.database.repositories.base import BaseRepository


class TaskRepository(BaseRepository[TaskDTO, TaskORM, UpdateTaskDTO]):
    dto = TaskDTO
    orm_model = TaskORM

    async def get_by_acceptance_id(
        self,
        acceptance_id: UUID,
    ) -> list[TaskDTO]:
        result = await self.database.scalars(
            select(self.orm_model).where(
                self.orm_model.acceptance_id == acceptance_id
            )
        )
        return [self.dto.model_validate(task) for task in result]

    async def get_by_good_id(self, good_id: UUID) -> list[TaskDTO]:
        result = await self.database.scalars(
            select(self.orm_model).where(self.orm_model.good_id == good_id)
        )
        return [self.dto.model_validate(task) for task in result]
