import time

import docker
import pytest
from bclearer_interop_services.document_store_services.mongo_db_service.mongo_db_wrapper import (
    MongoDBWrapper,
)
from pymongo.errors import (
    ConnectionFailure,
)


@pytest.fixture(scope="session")
def mongodb_container():
    client = docker.from_env()

    # Pull and run a MongoDB container
    container = client.containers.run(
        "mongo:latest",
        ports={"27017/tcp": 27017},
        detach=True,
        name="test-mongodb",
        remove=True,
    )

    # Wait for MongoDB to become available
    time.sleep(
        5
    )  # Adjust this depending on how long it takes to start the container

    # Check connection until it's ready
    mongo_uri = (
        "mongodb://localhost:27017"
    )
    db_name = "test_db"
    wrapper = MongoDBWrapper(
        uri=mongo_uri,
        database_name=db_name,
    )

    for _ in range(10):
        try:
            # Check if MongoDB is ready
            wrapper.client.admin.command(
                "ping"
            )
            break
        except ConnectionFailure:
            time.sleep(2)

    yield wrapper

    # Teardown: Stop the container after the tests are done
    container.stop()
