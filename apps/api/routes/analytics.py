from fastapi import APIRouter
from controllers.analytics import AnalyticsController

router = APIRouter()
analytics_controller = AnalyticsController()

@router.get("/analytics/expenses/quarterly")
async def get_top_expenses_quarterly():
    return analytics_controller.get_top_expenses_quarterly()

@router.get("/analytics/expenses/yearly")
async def get_top_expenses_yearly():
    return analytics_controller.get_top_expenses_yearly()
