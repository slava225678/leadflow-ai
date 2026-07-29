from app.core.logger import logger
from app.core.service_factory import ServiceFactory


class LeadWorker:
    """
    Фоновый обработчик лидов.

    Берет сервис из фабрики, запускает анализ лида и закрывает сессию.
    """

    def __init__(
        self,
        factory: ServiceFactory | None = None,
    ):
        self.factory = factory or ServiceFactory()

    def process(
        self,
        lead_id: int,
    ):
        """
        Обрабатывает лид в фоновом режиме.

        Инициирует создание сервиса, запускает анализ лида
        и гарантированно закрывает базу данных.
        """
        logger.info("Worker started for lead #%s", lead_id)
        service, db = self.factory.create_lead_service()
        try:
            service.analyze_lead(
                lead_id,
            )
        finally:
            db.close()
        logger.info("Worker finished for lead #%s", lead_id)
