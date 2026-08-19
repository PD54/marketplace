from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.orm_models.base import BaseORM


class TaskORM(BaseORM):
    __tablename__ = "tasks"

    status: Mapped[str] = mapped_column(
        default="in_work",
        server_default="in_work"
    )
    task_type: Mapped[str] = mapped_column()
    posting_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("postings.id", ondelete="CASCADE", onupdate="CASCADE"),
        index=True
    )
    acceptance_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("acceptances.id", ondelete="CASCADE", onupdate="CASCADE"),
        index=True
    )
    good_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("goods.id", ondelete="CASCADE", onupdate="CASCADE"),
        index=True
    )
    sku_id: Mapped[UUID] = mapped_column(
        ForeignKey("sku.id", ondelete="CASCADE", onupdate="CASCADE"),
        index=True
    )
    stock: Mapped[str] = mapped_column()
    count: Mapped[int] = mapped_column()
