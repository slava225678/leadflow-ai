from app.core.service_factory import ServiceFactory
from app.db.models import LeadStatus
from app.repositories.lead_repository import LeadRepository
from app.services.lead_service import LeadService
from tests.fakes.fake_llm import FakeLLMClient


class FakeServiceFactory(ServiceFactory):
    def __init__(self, db):
        self.db = db

    def create_lead_service(self):
        repository = LeadRepository(self.db)
        service = LeadService(
            repository=repository,
            llm=FakeLLMClient(),
        )
        return service, self.db


def test_create_lead(client, db_session, lead_data):
    response = client.post(
        "/leads",
        json=lead_data.model_dump(),
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == lead_data.name
    assert data["phone"] == lead_data.phone
    assert data["email"] == lead_data.email
    assert data["message"] == lead_data.message
    assert data["status"] == LeadStatus.NEW.value
    assert data["summary"] is None
    assert data["priority"] is None
    assert data["budget"] is None


def test_get_leads_returns_created_leads(client, lead_data):
    client.post(
        "/leads",
        json=lead_data.model_dump(),
    )
    response = client.get("/leads")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    lead = data[0]
    assert lead["name"] == lead_data.name
    assert lead["phone"] == lead_data.phone
    assert lead["email"] == lead_data.email
    assert lead["message"] == lead_data.message
    assert lead["status"] == LeadStatus.COMPLETED.value


def test_get_lead_by_id_returns_lead(client, lead_data):
    created = client.post(
        "/leads",
        json=lead_data.model_dump(),
    ).json()
    response = client.get(f"/leads/{created['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created["id"]
    assert data["name"] == lead_data.name
    assert data["phone"] == lead_data.phone
    assert data["email"] == lead_data.email
    assert data["message"] == lead_data.message
    assert data["status"] == LeadStatus.COMPLETED.value


def test_get_nonexistent_lead_returns_404(client):
    response = client.get("/leads/999")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Lead 999 not found",
    }


def test_create_lead_validation_error(client):
    response = client.post(
        "/leads",
        json={
            "name": "Ivan",
        },
    )
    assert response.status_code == 422
