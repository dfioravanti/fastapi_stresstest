from contextlib import asynccontextmanager
from typing import AsyncContextManager, Optional

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

from app.envs import DB_MAX_OVERFLOW, DB_POOL_SIZE, DB_URI

_db_engine: Optional[AsyncEngine]


async def open_database_connection_pools(db_uri=DB_URI):
    global _db_engine

    _db_engine = create_async_engine(
        db_uri,
        pool_size=DB_POOL_SIZE,
        max_overflow=DB_MAX_OVERFLOW,
        pool_recycle=3600,
        pool_pre_ping=True,
    )


async def close_database_connection_pools():
    global _db_engine

    if _db_engine:
        await _db_engine.dispose()


async def get_db_conn() -> AsyncEngine:
    if _db_engine is None:
        raise ValueError("Impossible to connect to database since the connection pool is not initialised")
    return _db_engine


@asynccontextmanager
async def get_db_sess() -> AsyncContextManager[AsyncSession]:
    session = AsyncSession(bind=_db_engine, autocommit=False, autoflush=False)

    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
