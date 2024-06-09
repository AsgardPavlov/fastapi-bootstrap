from datetime import datetime
from typing import AsyncGenerator

from sqlalchemy import TIMESTAMP, create_engine
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Session,
    mapped_column,
    sessionmaker,
)

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

SYNC_SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
ASYNC_SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# https://stackoverflow.com/questions/55457069/how-to-fix-operationalerror-psycopg2-operationalerror-server-closed-the-conn
sync_engine = create_engine(
    SYNC_SQLALCHEMY_DATABASE_URL,
    pool_size=10,
    max_overflow=2,
    pool_recycle=300,
    pool_pre_ping=True,
    pool_use_lifo=True,
)
async_engine = create_async_engine(ASYNC_SQLALCHEMY_DATABASE_URL)

async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=sync_engine, future=True
)
DbSession = Session(sync_engine)


class Base(DeclarativeBase):
    created_at = mapped_column(TIMESTAMP, default=datetime.utcnow)
    updated_at = mapped_column(
        TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    pass


# DB Utilities
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def create_db_and_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
