import os

import pytest


@pytest.fixture(scope="session")
def data_input_folder_absolute_path():
    data_input_relative_path = (
        "../data/input"
    )
    base_path = os.path.dirname(
        os.path.abspath(__file__),
    )
    data_input_folder_absolute_path = os.path.normpath(
        os.path.join(
            base_path,
            data_input_relative_path,
        ),
    )
    return (
        data_input_folder_absolute_path
    )


@pytest.fixture(scope="session")
def configurations_folder():
    configurations_folder_relative_path = (
        "../configurations"
    )
    base_path = os.path.dirname(
        os.path.abspath(__file__),
    )
    configurations_folder_absolute_path = os.path.normpath(
        os.path.join(
            base_path,
            configurations_folder_relative_path,
        ),
    )
    return configurations_folder_absolute_path


@pytest.fixture(scope="session")
def log_folder():
    log_folder_relative_path = (
        "./data/logs"
    )

    return log_folder_relative_path


@pytest.fixture(scope="session")
def storage_interop_services_source_folder():
    storage_interop_services_source_folder_relative_path = (
        "./data/input"
    )

    return storage_interop_services_source_folder_relative_path


@pytest.fixture(scope="session")
def excel_file_name_and_path_xlsx():
    excel_file_path_relative_path = "./data/input/excel/cfi-20210507-current.xlsx"
    return excel_file_path_relative_path


@pytest.fixture(scope="session")
def excel_file_name_and_path_xls():
    excel_file_path_relative_path = "./data/input/excel/cfi-20210507-current.xls"
    return excel_file_path_relative_path


@pytest.fixture(scope="session")
def csv_file_name_and_path(
    data_input_folder_absolute_path,
):
    csv_file_path_relative_path = "delimited_text/cfi-20210507-current.csv"
    csv_file_absolute_path = os.path.join(
        data_input_folder_absolute_path,
        csv_file_path_relative_path,
    )
    return csv_file_absolute_path


@pytest.fixture(scope="session")
def csv_file_name_and_path_no_header(
    data_input_folder_absolute_path,
):
    csv_file_path_relative_path = "delimited_text/cfi-20210507-current_no_header.csv"
    csv_file_absolute_path = os.path.join(
        data_input_folder_absolute_path,
        csv_file_path_relative_path,
    )
    return csv_file_absolute_path
