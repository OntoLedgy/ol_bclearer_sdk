import pytest
from bclearer_interop_services.relational_database_services.DatabaseFactory import \
    DatabaseFactory
from storage_interop_services_source.code.configuration_managers.configuration_loader import \
    load_configuration


@pytest.fixture(scope="module")
def db_connection_postgresql():
    db_type = "postgresql"
    configuration = load_configuration(
        "../../configurations/postgresql_configuration.json",
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
