import time

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.v1.leads import router as lead_router
from app.core.config import settings
from app.core.logger import logger
from app.db.session import get_db
from app.exceptions.lead import LeadNotFoundError

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)


@app.middleware("http")
async def log_requests(
    request: Request,
    call_next,
):
    start = time.perf_counter()

    try:
        response = await call_next(request)
        return response

    finally:
        duration = time.perf_counter() - start

        logger.info(
            "%s %s (%.3fs)",
            request.method,
            request.url.path,
            duration,
        )


@app.get("/")
async def health():
    return {
        "status": "ok",
        "app": settings.app_name,
    }


@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"database": "ok"}


@app.exception_handler(LeadNotFoundError)
async def lead_not_found_handler(
    request: Request,
    exc: LeadNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={"detail": f"Lead {exc.lead_id} not found"},
    )


app.include_router(lead_router)
