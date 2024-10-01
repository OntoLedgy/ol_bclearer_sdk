import pytest


@pytest.fixture(scope="module")
def csv_file():
    input_csv_file_path = r"X:\Planning\2024\Actuals\hsbc_61601261_20240726.csv"
    return input_csv_file_path
