from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.summary import Summary

class SummaryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def __add__(self, article_id: int, summary: str) -> Summary:
        summary = Summary(article_id=article_id, summary=summary)
        self.session.add(summary)
        await self.session.commit()
        await self.session.refresh(summary)
        return summary

    async def __get__(self, article_id: int) -> Summary | None:
        result = await self.session.execute(select(Summary).where(Summary.article_id == article_id))
        return result.scalar_one_or_none()