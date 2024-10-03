import random
import time

import docker
import pytest
from bclearer_interop_services.relational_database_services.DatabaseFactory import (
    DatabaseFactory,
)
from faker import Faker

# Initialize Faker for generating random data
fake = Faker()


@pytest.fixture(scope="session")
def postgres_docker():
    """Spin up a PostgreSQL container using Docker and return a PostgresqlFacade instance."""
    client = docker.from_env()

    # Pull and run a PostgreSQL container
    container = client.containers.run(
        "postgres:13",
        # Postgres version
        name="test_postgres_db",
        environment={
            "POSTGRES_USER": "test_user",
            "POSTGRES_PASSWORD": "test_password",
            "POSTGRES_DB": "test_db",
        },
        ports={"5432/tcp": 5432},
        detach=True,
    )

    # Allow the container to start and initialize the database
    time.sleep(5)

    # Use DatabaseFactory to get the PostgresqlFacade
    try:
        db_instance = DatabaseFactory.get_database(
            db_type="postgresql",
            host="localhost",
            database="test_db",
            user="test_user",
            password="test_password",
        )

        # Connect to the database
        db_instance.connect()

        # Create the transactions table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS transactions (
            id SERIAL PRIMARY KEY,
            transaction_date DATE,
            amount DECIMAL(10, 2),
            description TEXT
        );
        """
        db_instance.execute_query(
            create_table_query
        )

        # Insert random data into the transactions table
        for _ in range(
            10
        ):  # Insert 10 rows of random data
            insert_query = """
            INSERT INTO transactions (transaction_date, amount, description)
            VALUES (%s, %s, %s);
            """
            db_instance.execute_query(
                insert_query,
                (
                    fake.date_this_year(),  # Random date within this year
                    round(
                        random.uniform(
                            10.0, 1000.0
                        ),
                        2,
                    ),  # Random amount
                    fake.sentence(),  # Random description
                ),
            )

        yield db_instance

    finally:
        # Clean up the container
        container.stop()
        container.remove()
