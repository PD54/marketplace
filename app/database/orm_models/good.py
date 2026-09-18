from decimal import Decimal
from uuid import UUID

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.database.orm_models.base import BaseORM


class GoodORM(BaseORM):
    __tablename__ = "goods"

    sku_id: Mapped[UUID] = mapped_column(
        ForeignKey("sku.id", ondelete="CASCADE", onupdate="CASCADE"),
        index=True,
    )
    stock: Mapped[str] = mapped_column(
        default="valid",
        server_default="valid",
    )
    reserved_state: Mapped[bool] = mapped_column(
        default=False,
        server_default="f",
    )
    discount_percentage: Mapped[Decimal] = mapped_column(
        Numeric(precision=5, scale=2),
        server_default="0.00",
    )
