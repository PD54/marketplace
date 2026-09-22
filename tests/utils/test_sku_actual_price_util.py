from decimal import Decimal

import pytest

from app.database.dto.discount import DiscountDTO
from app.database.dto.sku import SkuDTO
from app.utils.sku_actual_price import calculate_sku_actual_price


def test_many_active_discounts_success(
    sku: SkuDTO,
    discount_active: DiscountDTO,
    discount_active_higher_percentage: DiscountDTO,
):
    active_discounts = [
        discount_active,
        discount_active_higher_percentage,
    ]

    actual_price = calculate_sku_actual_price(
        sku=sku,
        active_discounts=active_discounts,
    )

    assert actual_price == Decimal("3750")


def test_no_active_discounts_success(
    sku: SkuDTO,
):
    actual_price = calculate_sku_actual_price(
        sku=sku,
        active_discounts=[],
    )

    assert actual_price == sku.base_price


def test_zero_discount_success(
    sku: SkuDTO,
):
    zero_discount = DiscountDTO(
        percentage=Decimal("0"),
    )

    actual_price = calculate_sku_actual_price(
        sku=sku,
        active_discounts=[zero_discount],
    )

    assert actual_price == sku.base_price


def test_fractional_discount_success(
    sku: SkuDTO,
):
    fractional_discount = DiscountDTO(
        percentage=Decimal("17.93"),
    )

    actual_price = calculate_sku_actual_price(
        sku=sku,
        active_discounts=[fractional_discount],
    )

    assert actual_price == Decimal("4103.50")


@pytest.mark.parametrize(
    ("base_price", "discount_percentage", "expected_actual_price"),
    [
        # Третья цифра меньше 5, округление вниз (3662.1831 -> 3662.18)
        (Decimal("5493.00"), Decimal("33.33"), Decimal("3662.18")),
        # Третья цифра больше 5, округление вниз (2428.349 -> 2428.35)
        (Decimal("2867.00"), Decimal("15.30"), Decimal("2428.35")),
        # Третья цифра 5, вторая нечётная,
        # банковское округление, вверх (8631.875 -> 8631.88)
        (Decimal("9865.00"), Decimal("12.50"), Decimal("8631.88")),
        # Третья цифра 5, вторая чётная,
        # банковское округление, вниз (8447.465 -> 8447.46)
        (Decimal("9997.00"), Decimal("15.50"), Decimal("8447.46")),
    ],
)
def test_correct_rounding_success(
    sku: SkuDTO,
    base_price: Decimal,
    discount_percentage: Decimal,
    expected_actual_price: Decimal,
):
    sku.base_price = base_price
    discount = DiscountDTO(
        percentage=discount_percentage,
    )

    actual_price = calculate_sku_actual_price(
        sku=sku,
        active_discounts=[discount],
    )

    assert actual_price == expected_actual_price
