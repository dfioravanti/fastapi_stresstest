from contextlib import asynccontextmanager

from anyio import CapacityLimiter
from anyio.lowlevel import RunVar
from fastapi import FastAPI

from app.db.connection import (
    close_database_connection_pools,
    open_database_connection_pools,
)
from app.envs import MAX_NUMBER_THREADS


@asynccontextmanager
async def lifespan(app: FastAPI):
    RunVar("_default_thread_limiter").set(CapacityLimiter(MAX_NUMBER_THREADS))
    await open_database_connection_pools()
    yield
    await close_database_connection_pools()
