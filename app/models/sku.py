from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

class Sku(Base):
    __tablename__ = "sku"

    base_price: Mapped[float] = mapped_column(
        nullable=False,
        default=0.00,
        server_default="0.00"
    )

    is_hidden: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
        server_default="f"
    )
