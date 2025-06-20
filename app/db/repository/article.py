from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.article import Article

class ArticleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def __add__(self, url: str, content: str, parent_id: int=None) -> Article:
        existing_article = await self.session.execute(select(Article).where(Article.url == url))
        if existing_article.scalar():
            return {"error": "Article with this URL already exists."}

        if parent_id is None:
            parent_id = None
        article = Article(url=url, content=content, parent_id=parent_id)
        self.session.add(article)
        await self.session.commit()
        await self.session.refresh(article)
        return article

    async def __get__(self, article_id: int) -> Article | None:
        result = await self.session.execute(select(Article).where(Article.id == article_id))
        return result.scalar_one_or_none()

    async def __get_by_url__(self, url: str) -> Article | None:
        result = await self.session.execute(select(Article).where(Article.url == url))
        return result.scalar_one_or_none()