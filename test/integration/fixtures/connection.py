import asyncio

import pytest
from pytest_mock_resources import PostgresConfig, create_postgres_fixture

from app import envs
from app.db.connection import (
    close_database_connection_pools,
    open_database_connection_pools,
)

mock_docker_database = create_postgres_fixture(scope="session")


@pytest.fixture(scope="session")
def pmr_postgres_config():
    return PostgresConfig(image="postgres:15", drivername="postgresql+psycopg")


@pytest.fixture(scope="session")
def setup_engine(mock_docker_database):
    uri_with_hidden_password = str(mock_docker_database.url)
    uri = uri_with_hidden_password.replace("***", mock_docker_database.url.password)
    envs.DB_URI = str(uri)

    asyncio.run(open_database_connection_pools(envs.DB_URI))
    yield
    asyncio.run(close_database_connection_pools())


@pytest.fixture()
def setup_tables(alembic_runner, setup_engine):
    alembic_runner.migrate_up_to("heads", return_current=False)
    yield
    alembic_runner.migrate_down_to("base")
