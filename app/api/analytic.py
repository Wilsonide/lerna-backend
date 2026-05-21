from fastapi import APIRouter

from app.core.deps import DBSession
from app.services.analytic_service import analytics_service

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/revenue")
async def revenue(session: DBSession):
    return {"revenue": await analytics_service.total_revenue(session)}


@router.get("/sales")
async def sales(session: DBSession):
    return {"sales": await analytics_service.total_sales(session)}


@router.get("/best-books")
async def best_books(session: DBSession):
    return await analytics_service.best_selling_books(session)


@router.get("/dashboard")
async def dashboard(session: DBSession):
    return await analytics_service.dashboard_summary(session)
