from fastapi import APIRouter
from sqlalchemy import text

from app.api.deps import DbSession
from app.core.config import get_settings
from app.schemas.auth import HealthStatus

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthStatus)
def health(db: DbSession) -> HealthStatus:
    settings = get_settings()
    try:
        db.execute(text("SELECT 1"))
        database = "ok"
        status_text = "ok"
    except Exception:
        database = "unavailable"
        status_text = "degraded"
    return HealthStatus(status=status_text, app=settings.app_name, database=database)
