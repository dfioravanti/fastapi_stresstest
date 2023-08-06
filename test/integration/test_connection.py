import pytest
from sqlalchemy import text

from app.db.connection import get_db_sess


@pytest.mark.asyncio
async def test_connection(setup_tables):
    async with get_db_sess() as session:
        await session.execute(text("SELECT 1;"))


@pytest.mark.asyncio
async def test_second_run_works(setup_tables):
    async with get_db_sess() as session:
        result = await session.execute(
            text("select count(*) from information_schema.tables  where table_schema = 'public';")
        )
        nb_table = result.scalar()
        assert nb_table > 1
