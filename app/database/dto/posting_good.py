from decimal import Decimal
from enum import StrEnum
from uuid import UUID

from pydantic import Field

from app.database.dto.base import BaseDTO, UpdateBaseDTO
from app.database.dto.good import GoodStock


class PostingGoodCancelReason(StrEnum):
    good_not_found = "good_not_found"
    good_defected = "good_defected"
    task_cancelled = "task_cancelled"


class PostingGoodDTO(BaseDTO):
    posting_id: UUID = Field(
        description="Id of the posting",
    )
    good_id: UUID = Field(
        description="Id of the good",
    )
    good_sku_id: UUID = Field(
        description="Id of the sku that the good belongs to",
    )
    good_cost: Decimal = Field(
        description="Cost of the good",
    )
    good_stock: GoodStock = Field(
        description="Stock status of the good",
    )
    cancel_reason: PostingGoodCancelReason | None = Field(
        None,
        description="Cancellation reason for the good",
    )


class UpdatePostingGoodDTO(UpdateBaseDTO):
    posting_id: UUID | None = Field(
        None,
        description="Id of the posting",
    )
    good_id: UUID | None = Field(
        None,
        description="Id of the good",
    )
    good_sku_id: UUID | None = Field(
        None,
        description="Id of the sku that the good belongs to",
    )
    good_cost: Decimal | None = Field(
        None,
        description="Cost of the good",
    )
    good_stock: GoodStock | None = Field(
        None,
        description="Stock status of the good",
    )
    cancel_reason: PostingGoodCancelReason | None = Field(
        None,
        description="Cancellation reason for the good",
    )
