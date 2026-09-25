from decimal import Decimal

from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.database.orm_models import BaseORM


class DiscountORM(BaseORM):
    __tablename__ = "discounts"

    status: Mapped[str] = mapped_column(
        default="active",
        server_default="active",
    )
    percentage: Mapped[Decimal] = mapped_column(
        Numeric(precision=5, scale=2),
        default=Decimal("0.00"),
        server_default="0.00",
    )
