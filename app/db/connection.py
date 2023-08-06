from typing import Optional, ContextManager

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from contextlib import contextmanager, asynccontextmanager

from app.envs import DB_URI

_db_engine: Optional[Engine]


def _open_database_connection_pools():
    global _db_engine

    _db_engine = create_engine(
        DB_URI,
        pool_recycle=3600,
        pool_pre_ping=True,
    )


def _close_database_connection_pools():
    global _db_engine

    if _db_engine:
        _db_engine.dispose()


@asynccontextmanager
async def lifespan(app: FastAPI):
    _open_database_connection_pools()
    yield
    _close_database_connection_pools()


def get_db_conn() -> Engine:
    if _db_engine is None:
        raise ValueError("Impossible to connect to database since the connection pool is not initialised")
    return _db_engine


@contextmanager
def get_db_sess() -> ContextManager[Session]:
    session = Session(bind=_db_engine, autocommit=False, autoflush=False)

    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
