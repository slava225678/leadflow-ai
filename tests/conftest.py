import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.dependencies import get_service_factory
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.schemas.lead import LeadCreate
from tests.api.test_leads import FakeServiceFactory

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    def override_service_factory():
        return FakeServiceFactory(db_session)

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_service_factory] = override_service_factory

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def lead_data():
    return LeadCreate(
        name="Ivan",
        phone="+79999999999",
        email="ivan@test.ru",
        message="Нужен сайт за 100000 рублей",
    )
