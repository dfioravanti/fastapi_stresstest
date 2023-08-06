from typing import AsyncIterable, Optional, Annotated, ContextManager

from fastapi import Depends, FastAPI
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from contextlib import contextmanager

from app.envs import DB_URI

_db_conn: Optional[Engine]


def _open_database_connection_pools():
    global _db_conn
    _db_conn = create_engine(DB_URI)


def _close_database_connection_pools():
    global _db_conn
    if _db_conn:
        _db_conn.dispose()


def set_up_postgres(app: FastAPI):
    app.add_event_handler("startup", _open_database_connection_pools)
    app.add_event_handler("shutdown", _close_database_connection_pools)


def get_db_conn() -> Engine:
    if _db_conn is None:
        raise ValueError("Impossible to connect to database since the connection pool is not initialised")
    return _db_conn


# This is the part that replaces sessionmaker
@contextmanager
def get_db_sess() -> ContextManager[Session]:
    sess = Session(bind=get_db_conn())

    try:
        yield sess
    finally:
        sess.close()
