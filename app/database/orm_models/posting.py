from sqlalchemy.orm import Mapped, mapped_column

from app.database.orm_models import BaseORM


class PostingORM(BaseORM):
    __tablename__ = "postings"

    status: Mapped[str] = mapped_column(
        default="in_item_pick",
        server_default="in_item_pick",
    )
