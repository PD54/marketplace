from uuid import UUID

from sqlalchemy import select

from app.database.dto.posting_good import PostingGoodDTO, UpdatePostingGoodDTO
from app.database.orm_models.posting_good import PostingGoodORM
from app.database.repositories.base import BaseRepository


class PostingGoodRepository(
    BaseRepository[PostingGoodDTO, PostingGoodORM, UpdatePostingGoodDTO]
):
    dto = PostingGoodDTO
    orm_model = PostingGoodORM

    async def get_by_good_id(self, good_id: UUID) -> list[PostingGoodDTO]:
        res = await self.database.scalars(
            select(self.orm_model).where(self.orm_model.good_id == good_id)
        )
        return [self.dto.model_validate(posting_good) for posting_good in res]

    async def get_by_posting_id(
        self,
        posting_id: UUID,
    ) -> list[PostingGoodDTO]:
        res = await self.database.scalars(
            select(self.orm_model).where(
                self.orm_model.posting_id == posting_id
            )
        )
        return [self.dto.model_validate(posting_good) for posting_good in res]
