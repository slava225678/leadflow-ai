from fastapi import APIRouter, BackgroundTasks, Depends

from app.core.dependencies import get_lead_service, get_lead_worker
from app.schemas.lead import LeadCreate, LeadResponse
from app.services.lead_service import LeadService
from app.workers.lead_worker import LeadWorker

router = APIRouter(
    prefix="/leads",
    tags=["Leads"],
)


@router.post("", response_model=LeadResponse)
def create_lead(
    lead: LeadCreate,
    background_tasks: BackgroundTasks,
    service: LeadService = Depends(get_lead_service),
    worker: LeadWorker = Depends(get_lead_worker),
):
    created = service.create_lead(lead)

    background_tasks.add_task(
        worker.process,
        created.id,
    )

    return LeadResponse.model_validate(created)


@router.get("", response_model=list[LeadResponse])
def get_leads(
    service: LeadService = Depends(get_lead_service),
):
    return [LeadResponse.model_validate(item) for item in service.get_leads()]


@router.get("/{lead_id}", response_model=LeadResponse)
def get_lead(
    lead_id: int,
    service: LeadService = Depends(get_lead_service),
):
    lead = service.get_lead(lead_id)

    return LeadResponse.model_validate(lead)
