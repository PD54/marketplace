from decimal import Decimal

import pytest

from app.database.dto.discount import DiscountDTO, DiscountStatus


@pytest.fixture
def discount_active() -> DiscountDTO:
    return DiscountDTO(
        status=DiscountStatus.active,
        percentage=Decimal("20.00"),
    )


@pytest.fixture
def discount_active_higher_percentage() -> DiscountDTO:
    return DiscountDTO(
        status=DiscountStatus.active,
        percentage=Decimal("25.00"),
    )


@pytest.fixture
def discount_finished_highest_percentage() -> DiscountDTO:
    return DiscountDTO(
        status=DiscountStatus.finished,
        percentage=Decimal("30.00"),
    )


@pytest.fixture
def discounts_list(
    discount_active: DiscountDTO,
    discount_active_higher_percentage: DiscountDTO,
    discount_finished_highest_percentage: DiscountDTO,
) -> list[DiscountDTO]:
    return [
        discount_active,
        discount_active_higher_percentage,
        discount_finished_highest_percentage,
    ]
