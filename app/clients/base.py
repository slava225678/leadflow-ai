from abc import ABC, abstractmethod

from app.schemas.ai import LeadAnalysis


class LLMClient(ABC):
    """
    Абстрактный клиент для анализа лидов.

    Реализации должны предоставлять метод analyze_lead.
    """

    @abstractmethod
    def analyze_lead(self, message: str) -> LeadAnalysis:
        """Analyze lead message."""
        raise NotImplementedError
