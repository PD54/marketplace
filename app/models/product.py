import uuid

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Index

from app.models.base import Base
from app.models.stock_enum import Stock


class Product(Base):
    __tablename__ = "products"

    sku_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("sku.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )
    stock: Mapped[Stock] = mapped_column(
        nullable=False,
        default=Stock.not_found,
        server_default=Stock.not_found
    )
    reserved_state: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
        server_default="f"
    )

    __table_args__ = (Index("idx_products_sku_id", "sku_id"),)
