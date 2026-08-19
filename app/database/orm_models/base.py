from uuid import UUID, uuid7
from datetime import datetime, UTC

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import func, DateTime


class BaseORM(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid7,
        server_default=func.uuidv7()
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        server_default=func.now(),
        onupdate=func.now()
    )
