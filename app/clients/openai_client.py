from openai import OpenAI

from app.clients.base import LLMClient
from app.core.config import settings
from app.core.logger import logger
from app.schemas.ai import LeadAnalysis


class OpenAIClient(LLMClient):
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.openai_api_key,
        )

    def analyze_lead(
        self,
        message: str,
    ) -> LeadAnalysis:
        logger.info("Sending lead to OpenAI")
        completion = self.client.chat.completions.parse(
            model=settings.openai_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You analyze incoming sales leads."
                        " Return only structured information."
                    ),
                },
                {
                    "role": "user",
                    "content": message,
                },
            ],
            response_format=LeadAnalysis,
        )
        parsed = completion.choices[0].message.parsed
        logger.info("Lead analyzed successfully")
        return parsed
