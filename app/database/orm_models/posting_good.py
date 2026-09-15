from decimal import Decimal
from uuid import UUID

from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.database.orm_models import BaseORM


class PostingGoodORM(BaseORM):
    __tablename__ = "posting_goods"

    posting_id: Mapped[UUID] = mapped_column(
        ForeignKey("postings.id", onupdate="CASCADE", ondelete="CASCADE"),
        index=True,
    )
    good_id: Mapped[UUID] = mapped_column(
        ForeignKey("goods.id", onupdate="CASCADE", ondelete="CASCADE"),
        index=True,
    )
    good_sku_id: Mapped[UUID] = mapped_column(
        ForeignKey("sku.id", onupdate="CASCADE", ondelete="CASCADE"),
        index=True,
    )
    good_cost: Mapped[Decimal] = mapped_column()
    good_stock: Mapped[str] = mapped_column()
    cancel_reason: Mapped[str | None] = mapped_column()

    __table_args__ = (
        Index(
            "uix_posting_goods_good_id",
            "good_id",
            unique=True,
            postgresql_where=cancel_reason.is_(None),
        ),
    )
