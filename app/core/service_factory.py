from collections.abc import Callable

from app.clients.base import LLMClient
from app.clients.openai_client import OpenAIClient
from app.db.session import create_session
from app.repositories.lead_repository import LeadRepository
from app.services.lead_service import LeadService


class ServiceFactory:
    """
    Фабрика, создающая зависимости для обработки лидов.

    Собирает объект сервиса, репозитория и клиент LLM.
    """

    def __init__(
        self,
        db_factory: Callable = create_session,
        llm_factory: Callable[[], LLMClient] = OpenAIClient,
    ):
        self.db_factory = db_factory
        self.llm_factory = llm_factory

    def create_lead_service(self):
        """
        Создает и возвращает сервис для работы с лидами.

        Метод инкапсулирует создание сессии, репозитория и LLM-клиента.
        """
        db = self.db_factory()

        repository = LeadRepository(db)
        llm = self.llm_factory()

        service = LeadService(repository=repository, llm=llm)

        return service, db
