import logging
from decimal import Decimal

from app.database.dto.acceptance import AcceptanceDTO
from app.database.dto.sku import SkuDTO
from app.database.dto.task import TaskDTO, TaskType
from app.database.repositories.acceptance import AcceptanceRepository
from app.database.repositories.sku import SkuRepository
from app.database.repositories.task import TaskRepository
from app.services.acceptance.dto.create_acceptance import (
    CreateAcceptanceInputDTO,
    CreateAcceptanceItemInputDTO,
    CreateAcceptanceOutputDTO,
)

logger = logging.getLogger(__name__)


class CreateAcceptanceService:
    def __init__(
        self,
        acceptance_repo: AcceptanceRepository,
        sku_repo: SkuRepository,
        task_repo: TaskRepository,
    ):
        self.acceptance_repo = acceptance_repo
        self.sku_repo = sku_repo
        self.task_repo = task_repo

    async def create_acceptance(
        self,
        input_dto: CreateAcceptanceInputDTO,
    ) -> CreateAcceptanceOutputDTO:
        items_sorted_by_id = sorted(
            input_dto.items_to_accept,
            key=lambda x: x.sku_id,
        )
        logger.info("SKU отсортированы по id")

        acceptance = await self.acceptance_repo.create(AcceptanceDTO())
        logger.info(f"Создана приёмка с id {acceptance.id}")

        for item in items_sorted_by_id:
            task = await self.process_item(item=item, acceptance=acceptance)
            logger.info(f"Создана задача на размещение с id {task.id}")

        return CreateAcceptanceOutputDTO.model_validate(acceptance)

    async def process_item(
        self,
        item: CreateAcceptanceItemInputDTO,
        acceptance: AcceptanceDTO,
    ) -> TaskDTO:
        logger.info(f"Обработка SKU с id {item.sku_id}")
        sku_to_create = SkuDTO(
            id=item.sku_id,
            base_price=Decimal("0.00"),
            is_hidden=False,
        )
        sku = await self.sku_repo.create_or_do_nothing(sku_to_create)
        if sku:
            logger.info(f"Создана SKU с id {item.sku_id}")
        else:
            logger.info(f"SKU с id {item.sku_id} уже существует")

        task = await self.task_repo.create(
            TaskDTO(
                task_type=TaskType.placing,
                acceptance_id=acceptance.id,
                sku_id=item.sku_id,
                stock=item.stock,
                count=item.count,
            )
        )
        return task
