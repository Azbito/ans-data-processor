from fastapi.responses import JSONResponse
from fastapi import HTTPException
from repositories.analytics import AnalyticsRepository


class AnalyticsController:
    @staticmethod
    def get_top_expenses_quarterly() -> JSONResponse:
        try:
            results = AnalyticsRepository.get_top_expenses_by_period(period='quarterly')
            return JSONResponse(content=results)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_top_expenses_yearly() -> JSONResponse:
        try:
            results = AnalyticsRepository.get_top_expenses_by_period(period='yearly')
            return JSONResponse(content=results)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
