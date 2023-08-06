# pylint: disable=unused-import,wildcard-import
# noinspection PyUnresolvedReferences

# These are tests defined in pytest-alembic that help with preventing accidental errors with alembic

from pytest_alembic.tests import (
    test_model_definitions_match_ddl,
    test_single_head_revision,
    test_up_down_consistency,
    test_upgrade,
)