from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Numeric

from app.models.base import BaseORM


class SkuORM(BaseORM):
    __tablename__ = "sku"

    base_price: Mapped[Decimal] = mapped_column(
        Numeric(precision=12, scale=2),
        nullable=False,
        default=Decimal("0.00"),
        server_default="0.00"
    )

    is_hidden: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
        server_default="f"
    )
