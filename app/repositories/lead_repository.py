from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Lead


class LeadRepository:
    """
    Обеспечивает доступ к данным лидов в базе.

    Содержит методы создания, сохранения и выборки лидов.
    """

    def __init__(self, db: Session):
        self.db = db

    def save(self, lead: Lead) -> Lead:
        self.db.add(lead)
        self.db.commit()
        self.db.refresh(lead)
        return lead

    def create(self, lead: Lead) -> Lead:
        return self.save(lead)

    def get_by_id(self, lead_id: int) -> Lead | None:
        return self.db.get(Lead, lead_id)

    def get_all(self) -> list[Lead]:
        stmt = select(Lead)

        return self.db.scalars(stmt).all()  # type: ignore
