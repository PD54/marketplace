from enum import StrEnum

from pydantic import Field

from app.database.dto.base import BaseDTO, UpdateBaseDTO


class PostingStatus(StrEnum):
    in_item_pick = "in_item_pick"
    sent = "sent"
    cancelled = "cancelled"


class PostingDTO(BaseDTO):
    status: PostingStatus = Field(
        PostingStatus.in_item_pick,
        description="Status of the posting",
    )


class UpdatePostingDTO(UpdateBaseDTO):
    status: PostingStatus | None = Field(
        None,
        description="Status of the posting",
    )
