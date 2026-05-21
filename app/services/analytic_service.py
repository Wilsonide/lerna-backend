from app.repositories.analytic_repository import analytics_repository


class AnalyticsService:
    async def total_revenue(self, session):
        return await analytics_repository.get_total_revenue(session)

    async def total_sales(self, session):
        return await analytics_repository.get_total_sales(session)

    async def best_selling_books(self, session):
        return await analytics_repository.get_best_selling_books(session)

    async def dashboard_summary(self, session):
        revenue = await self.total_revenue(session)
        sales = await self.total_sales(session)
        best_books = await self.best_selling_books(session)

        return {
            "total_revenue": revenue,
            "total_sales": sales,
            "best_selling_books": best_books,
        }


analytics_service = AnalyticsService()
