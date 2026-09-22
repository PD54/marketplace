import logging
from decimal import Decimal

from app.database.dto.discount import DiscountDTO
from app.database.dto.sku import SkuDTO

logger = logging.getLogger(__name__)


def calculate_sku_actual_price(
    sku: SkuDTO,
    active_discounts: list[DiscountDTO],
) -> Decimal:
    logger.info(f"Расчёт актуальной цены для SKU с id {sku.id}")
    if not active_discounts:
        logger.info("Активных скидок нет, актуальная цена равна базовой")
        return sku.base_price

    max_discount = max(
        active_discounts, key=lambda discount: discount.percentage
    )
    logger.info(
        f"Максимальная скидка имеет id {max_discount.id};"
        f" процент {max_discount.percentage}"
    )
    price_multiplier = 1 - max_discount.percentage / 100
    actual_price = round(sku.base_price * price_multiplier, 2)
    logger.info(f"Актуальная цена с максимальной скидкой: {actual_price}")

    return actual_price
