from test import test_directory_path

import pytest
from pytest_alembic.config import Config


@pytest.fixture
def alembic_config():
    """Override this fixture to configure the exact alembic context setup required."""
    return Config(
        config_options={
            "file": str(test_directory_path.parent / "alembic.ini"),
            "script_location": str(test_directory_path.parent / "alembic"),
        }
    )


# Here we need to pass the mock db because this function wants an engine not a session
# we need the setup_engine so that
@pytest.fixture()
def alembic_engine(mock_docker_database):
    return mock_docker_database
