import os

import pytest
from bclearer_interop_services.excel_services.excel_facades import (
    ExcelFacades,
)
from pandas import DataFrame


class TestExcelInteropServices:
    @pytest.fixture(autouse=True)
    def setup_method(
        self,
        excel_file_name_and_path_xlsx,
    ):
        self.sheet_name = "Categories"

    def test_excel_interop_reading_xlsx(
        self,
        excel_file_name_and_path_xlsx,
    ):

        try:
            excel_facade = ExcelFacades(
                excel_file_name_and_path_xlsx,
            )
            print(
                f"Successfully initialized ExcelFacade with file: {excel_file_name_and_path_xlsx}",
            )

            cfi_categories = excel_facade.workbook.sheet(
                self.sheet_name,
            )
            assert (
                cfi_categories
                is not None
            ), f"Sheet {sheet_name} not found in the workbook."

            cfi_categories_dataframe = excel_facade.read_sheet_to_dataframe(
                sheet_name=sheet_name
            )
            print(
                f"DataFrame successfully read from the {sheet_name} sheet:",
            )

            assert isinstance(
                cfi_categories_dataframe,
                DataFrame,
            ), "The result is not a DataFrame object."

            print(
                cfi_categories_dataframe,
            )

            assert (
                cfi_categories_dataframe.shape
                == (
                    14,
                    5,
                )
            ), "DataFrame does not have the expected shape (14, 5)."

            assert (
                not cfi_categories_dataframe.empty
            ), "DataFrame is empty."

            print(
                f"DataFrame shape: {cfi_categories_dataframe.shape}",
            )

            assert (
                cfi_categories_dataframe.iloc[
                    0
                ][
                    "Code"
                ]
                == "E"
            ), "First row 'Code' column value is not 'E' as expected."

        except Exception as e:
            pytest.fail(
                f"An error occurred during the test: {e!s}",
            )

    def test_excel_interop_reading_xls(
        self,
        excel_file_name_and_path_xls,
    ):
        sheet_name = "Categories"

        try:
            excel_facade = ExcelFacades(
                excel_file_name_and_path_xls,
            )
            print(
                f"Successfully initialized ExcelFacade with file: {excel_file_name_and_path_xls}",
            )

            cfi_categories = excel_facade.workbook.sheet(
                sheet_name,
            )
            assert (
                cfi_categories
                is not None
            ), f"Sheet {sheet_name} not found in the workbook."

            cfi_categories_dataframe = (
                cfi_categories.read_to_dataframe()
            )
            print(
                f"DataFrame successfully read from the {sheet_name} sheet:",
            )

            assert isinstance(
                cfi_categories_dataframe,
                DataFrame,
            ), "The result is not a DataFrame object."

            print(
                cfi_categories_dataframe,
            )

            assert (
                cfi_categories_dataframe.shape
                == (
                    14,
                    5,
                )
            ), "DataFrame does not have the expected shape (14, 5)."

            assert (
                not cfi_categories_dataframe.empty
            ), "DataFrame is empty."

            print(
                f"DataFrame shape: {cfi_categories_dataframe.shape}",
            )

            assert (
                cfi_categories_dataframe.iloc[
                    0
                ][
                    "Code"
                ]
                == "E"
            ), "First row 'Code' column value is not 'E' as expected."

        except Exception as e:
            pytest.fail(
                f"An error occurred during the test: {e!s}",
            )

    # TODO: need to add more fine grained tests
    def test_excel_interop_reading_ranges(
        self,
        excel_file_name_and_path_xlsx,
    ):
        sheet_name = "ESXXXX"

        try:
            excel_facade = ExcelFacades(
                excel_file_name_and_path_xlsx,
            )
            print(
                f"Successfully initialized ExcelFacade with file: {excel_file_name_and_path_xlsx}",
            )

            cfi_categories = excel_facade.workbook.sheet(
                sheet_name
            )

        except Exception as e:
            pytest.fail(
                f"An error occurred during the test: {e!s}",
            )

    def test_excel_interop_reading_cells(
        self,
    ):
        pass

    def test_excel_interop_reading_cells(
        self,
        excel_file_name_and_path_xlsx,
        data_output_folder_absolute_path,
    ):
        target_output_file_path = os.path.join(
            data_output_folder_absolute_path,
            "excel/test_output.xlsx",
        )
        test_string = (
            "Testing Excel Writting"
        )
        try:

            excel_facade = ExcelFacades(
                excel_file_name_and_path_xlsx,
            )

            print(
                f"Successfully initialized ExcelFacade with file: {excel_file_name_and_path_xlsx}",
            )

            excel_facade.write_cell(
                sheet_name=self.sheet_name,
                row_index=10,
                column_index=10,
                value=test_string,
            )

            excel_facade.save(
                file_path=os.path.join(
                    data_output_folder_absolute_path,
                    target_output_file_path,
                ),
            )

            output_excel_facade = ExcelFacades(
                target_output_file_path,
            )

            written_cell_value = output_excel_facade.read_cell(
                sheet_name=self.sheet_name,
                row_index=10,
                column_index=10,
            )

            assert (
                written_cell_value,
                test_string,
            )

        except Exception as e:
            pytest.fail(
                f"An error occurred during the test: {e!s}",
            )
