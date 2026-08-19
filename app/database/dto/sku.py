from decimal import Decimal

from pydantic import Field

from app.database.dto.base import BaseDTO


class SkuDTO(BaseDTO):
    base_price: Decimal = Field(
        description="Base price of the SKU",
    )
    is_hidden: bool = Field(
        False,
        description="Flag that tells if this SKU is hidden",
    )
