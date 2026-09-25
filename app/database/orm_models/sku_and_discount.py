from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.orm_models import BaseORM


class SkuAndDiscountORM(BaseORM):
    __tablename__ = "sku_and_discounts"

    sku_id: Mapped[UUID] = mapped_column(
        ForeignKey("sku.id", onupdate="CASCADE", ondelete="CASCADE"),
        index=True,
    )
    discount_id: Mapped[UUID] = mapped_column(
        ForeignKey("discounts.id", onupdate="CASCADE", ondelete="CASCADE"),
        index=True,
    )
