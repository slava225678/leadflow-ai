from app.clients.base import LLMClient
from app.core.logger import logger
from app.db.models import Lead, LeadStatus
from app.exceptions.lead import LeadNotFoundError
from app.repositories.lead_repository import LeadRepository
from app.schemas.lead import LeadCreate


class LeadService:
    """
    Координирует бизнес-логику для обработки лидов.

    Создает лидов, возвращает их, инициирует анализ
    через LLM и обновляет статус сущности.
    """

    def __init__(
        self,
        repository: LeadRepository,
        llm: LLMClient,
    ):
        self.repository = repository
        self.llm = llm

    def create_lead(self, data: LeadCreate) -> Lead:
        logger.info("Creating lead")
        lead = Lead(
            name=data.name,
            phone=data.phone,
            email=data.email,
            message=data.message,
            status=LeadStatus.NEW,
        )
        lead = self.repository.create(lead)
        logger.info("Lead #%s created", lead.id)
        return lead

    def analyze_lead(self, lead_id: int) -> Lead:
        """
        Выполняет анализ лида и обновляет его статус.

        Ищет лид по идентификатору, ставит статус PROCESSING,
        запрашивает анализ у LLM и сохраняет результаты.
        При ошибке помечает лид как FAILED.
        """
        lead = self.repository.get_by_id(lead_id)
        if lead is None:
            raise LeadNotFoundError(lead_id)
        logger.info("Analyzing lead #%s", lead.id)
        lead.status = LeadStatus.PROCESSING
        self.repository.save(lead)
        try:
            analysis = self.llm.analyze_lead(lead.message)
            lead.summary = analysis.summary
            lead.priority = analysis.priority.value
            lead.budget = analysis.budget
            lead.analysis_json = analysis.model_dump()
            lead.status = LeadStatus.COMPLETED
        except Exception as exc:
            logger.exception(
                "Failed to analyze lead #%s: %s",
                lead.id,
                exc,
            )
            lead.status = LeadStatus.FAILED
        finally:
            self.repository.save(lead)
        return lead

    def get_leads(self):
        return self.repository.get_all()

    def get_lead(self, lead_id: int) -> Lead:
        logger.info("Fetching lead %s", lead_id)
        lead = self.repository.get_by_id(lead_id)
        if lead is None:
            logger.warning("Lead %s not found", lead_id)
            raise LeadNotFoundError(lead_id)
        return lead
