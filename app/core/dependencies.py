from fastapi import Depends

from app.core.service_factory import ServiceFactory
from app.workers.lead_worker import LeadWorker


def get_service_factory():
    return ServiceFactory()


def get_lead_service(
    factory: ServiceFactory = Depends(get_service_factory),
):
    service, db = factory.create_lead_service()

    try:
        yield service
    finally:
        db.close()


def get_lead_worker(
    factory: ServiceFactory = Depends(get_service_factory),
):
    return LeadWorker(factory)
