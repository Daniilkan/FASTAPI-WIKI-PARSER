from app.core import config
from app.services.parser import parse_article, parse_links, clean_urls
from app.services.summary import get_summary
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.repository.article import ArticleRepository
from app.db.repository.summary import SummaryRepository
from app.db.base import get_session
import uvicorn
from pydantic import BaseModel

app = FastAPI()
cfg = config.new()

class ArticleCreate(BaseModel):
    url: str

# curl -X POST http://host:port/articles/ \
#   -H "Content-Type: application/json" \
#   -d '{
#         "url": "https://example.com",
#       }'
@app.post("/articles/")
async def create_article(
    article: ArticleCreate,
    session: AsyncSession = Depends(get_session)
):
    content = parse_article(article.url)
    article_repo = ArticleRepository(session)
    if await article_repo.__get_by_url__(article.url):
        return {"error": "Article already exists"}
    article = await article_repo.__add__(article.url, content)

    summary_text = get_summary(article.content, cfg.AI_KEY)
    summary_repo = SummaryRepository(session)
    summary = await summary_repo.__add__(article.id, summary_text)

    urls = clean_urls(parse_links(article.url))[:5]
    for url in urls:
        await article_repo.__add__(url, parse_article(url), parent_id=article.id)

    await session.commit()
    return {"id": article.id, "url": article.url, "content": content, "summary": summary.summary}

# curl -X GET http://host:port/articles/
@app.get("/articles/{article_id}")
async def get_article(
    article_id: int,
    session: AsyncSession = Depends(get_session)
):
    repo = ArticleRepository(session)
    article = await repo.__get__(article_id)
    if not article:
        return {"error": "Not found"}
    return {
        "id": article.id,
        "title": article.title,
        "url": article.url,
        "content": article.content
    }

@app.get("/summaries/{article_id}")
async def get_summary_by_article(
    article_id: int,
    session: AsyncSession = Depends(get_session)
):
    summary_repo = SummaryRepository(session)
    summary = await summary_repo.__get__(article_id)
    if not summary:
        return {"error": "Summary not found"}
    return {
        "article_id": summary.article_id,
        "summary": summary.summary
    }

if __name__ == "__main__":
    uvicorn.run(app, host=cfg.APP_HOST, port=int(cfg.APP_PORT))