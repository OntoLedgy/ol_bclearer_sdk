import pytest


@pytest.fixture(scope="session")
def app_runner_method():
    print("hello")


@pytest.fixture(scope="session")
def test_message():
    return "hello"
