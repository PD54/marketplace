import uuid

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from app.database.orm_models.base import BaseORM


class ProductORM(BaseORM):
    __tablename__ = "products"

    sku_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("sku.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True
    )
    stock: Mapped[str] = mapped_column(
        nullable=False,
        default="valid",
        server_default="valid"
    )
    reserved_state: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
        server_default="f"
    )
