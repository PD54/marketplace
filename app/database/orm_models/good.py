from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from app.database.orm_models.base import BaseORM


class GoodORM(BaseORM):
    __tablename__ = "goods"

    sku_id: Mapped[UUID] = mapped_column(
        ForeignKey("sku.id", ondelete="CASCADE", onupdate="CASCADE"),
        index=True
    )
    stock: Mapped[str] = mapped_column(
        default="valid",
        server_default="valid"
    )
    reserved_state: Mapped[bool] = mapped_column(
        default=False,
        server_default="f"
    )
