class LeadNotFoundError(Exception):
    def __init__(self, lead_id: int):
        self.lead_id = lead_id
        super().__init__(f"Lead with ID {lead_id} not found")
