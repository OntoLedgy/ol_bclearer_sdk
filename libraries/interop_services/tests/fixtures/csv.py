import pytest


@pytest.fixture(scope="module")
def csv_file():
    input_csv_file_path = r"libraries/interop_services/tests/data/input/delimited_text/cfi-20210507-current_no_header.csv"
    return input_csv_file_path
