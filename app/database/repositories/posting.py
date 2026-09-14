from app.database.dto.posting import PostingDTO, UpdatePostingDTO
from app.database.orm_models import PostingORM
from app.database.repositories.base import BaseRepository


class PostingRepository(
    BaseRepository[PostingDTO, PostingORM, UpdatePostingDTO]
):
    dto = PostingDTO
    orm_model = PostingORM
