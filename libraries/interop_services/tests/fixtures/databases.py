import pytest
from bclearer_core.configuration_managers.configuration_loader import (
    load_configuration,
)
from bclearer_interop_services.relational_database_services.DatabaseFactory import (
    DatabaseFactory,
)


@pytest.fixture(scope="module")
def db_connection_postgresql():
    db_type = "postgresql"
    configuration = load_configuration(
        "./configurations/db_connection_postgresql.json",
    )
    db = DatabaseFactory.get_database(
        db_type,
        host=configuration["host"],
        database=configuration[
            "database"
        ],
        user=configuration["user"],
        password=configuration[
            "password"
        ],
    )
    db.connect()
    yield db
    db.disconnect()
