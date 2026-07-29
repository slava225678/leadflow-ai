from app.clients.base import LLMClient
from app.schemas.ai import LeadAnalysis, LeadPriority


class FakeLLMClient(LLMClient):
    def __init__(
        self,
        response: LeadAnalysis | None = None,
        should_fail: bool = False,
    ):
        self.calls = 0
        self.should_fail = should_fail
        self.response = response or LeadAnalysis(
            summary="Fake summary",
            priority=LeadPriority.HIGH,
            budget=100000,
        )

    def analyze_lead(self, message: str) -> LeadAnalysis:
        self.calls += 1
        if self.should_fail:
            raise RuntimeError("LLM unavailable")
        return self.response
