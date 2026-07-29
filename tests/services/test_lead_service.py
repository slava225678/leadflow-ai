import pytest

from app.db.models import LeadStatus
from app.exceptions.lead import LeadNotFoundError
from app.repositories.lead_repository import LeadRepository
from app.schemas.ai import LeadPriority
from app.services.lead_service import LeadService
from tests.fakes.fake_llm import FakeLLMClient


def test_create_lead_sets_status_new(lead_data, db_session):
    repository = LeadRepository(db_session)
    llm = FakeLLMClient()
    service = LeadService(
        repository,
        llm,
    )
    created = service.create_lead(lead_data)

    assert created.id is not None
    assert created.status == LeadStatus.NEW
    assert created.summary is None
    assert created.priority is None
    assert created.budget is None
    assert created.analysis_json is None


def test_analyze_lead_completes_successfully(db_session, lead_data):
    repository = LeadRepository(db_session)
    llm = FakeLLMClient()
    service = LeadService(
        repository,
        llm,
    )
    created = service.create_lead(lead_data)
    updated = service.analyze_lead(created.id)

    assert updated.status == LeadStatus.COMPLETED
    assert updated.summary == "Fake summary"
    assert updated.priority == LeadPriority.HIGH
    assert updated.budget == 100000
    assert updated.analysis_json == {
        "summary": "Fake summary",
        "priority": "HIGH",
        "budget": 100000,
    }
    assert llm.calls == 1


def test_analyze_nonexistent_lead_raises_error(db_session):
    repository = LeadRepository(db_session)
    service = LeadService(
        repository,
        FakeLLMClient(),
    )

    with pytest.raises(LeadNotFoundError):
        service.analyze_lead(999)


def test_analyze_lead_marks_failed_on_llm_error(db_session, lead_data):
    repository = LeadRepository(db_session)
    service = LeadService(
        repository,
        FakeLLMClient(should_fail=True),
    )

    created = service.create_lead(lead_data)
    updated = service.analyze_lead(created.id)

    assert updated.status == LeadStatus.FAILED
    assert updated.summary is None
    assert updated.priority is None
    assert updated.budget is None
