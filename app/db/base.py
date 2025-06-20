from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncAttrs
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core import config

postgresCfg = config.new().PostgresConfig

db_url = (f"postgresql+asyncpg://{postgresCfg.POSTGRES_USER}:{postgresCfg.POSTGRES_PASSWORD}"
          f"@{postgresCfg.POSTGRES_HOST}:{postgresCfg.POSTGRES_PORT}"
          f"/{postgresCfg.POSTGRES_DB}")
engine = create_async_engine(db_url, echo=True, future=True)
SessionLocal = sessionmaker(
        bind=engine,
        class_= AsyncSession,
        expire_on_commit=False
)
Base = declarative_base(cls=AsyncAttrs)


async def get_session():
    async with SessionLocal() as session:
        yield session
