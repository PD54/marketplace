from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Numeric

from app.database.orm_models.base import BaseORM


class SkuORM(BaseORM):
    __tablename__ = "sku"

    base_price: Mapped[Decimal] = mapped_column(
        Numeric(precision=12, scale=2)
    )

    is_hidden: Mapped[bool] = mapped_column(
        default=False,
        server_default="f"
    )
