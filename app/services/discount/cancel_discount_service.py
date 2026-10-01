import logging

from app.database.dto.discount import DiscountStatus, UpdateDiscountDTO
from app.database.repositories.discount import DiscountRepository
from app.services.discount.dto.cancel_discount import CancelDiscountInputDTO
from app.services.discount.exceptions import DiscountNotFoundError

logger = logging.getLogger(__name__)


class CancelDiscountService:
    def __init__(
        self,
        discount_repo: DiscountRepository,
    ):
        self.discount_repo = discount_repo

    async def cancel_discount(
        self,
        input_dto: CancelDiscountInputDTO,
    ) -> None:
        logger.info(f"Завершение скидки с id {input_dto.id}")

        discount = await self.discount_repo.get_by_id(input_dto.id)
        if not discount:
            logger.error(f"Скидка с id {input_dto.id} не найдена в БД")
            raise DiscountNotFoundError()

        if discount.status == DiscountStatus.finished:
            logger.info(f"Скидка с id {input_dto.id} уже завершена")
            return

        await self.discount_repo.update(
            entity_id=input_dto.id,
            update_dto=UpdateDiscountDTO(
                status=DiscountStatus.finished,
            ),
        )
        logger.info(
            f"Статус скидки с id {input_dto.id}"
            f" изменён на {DiscountStatus.finished}"
        )
