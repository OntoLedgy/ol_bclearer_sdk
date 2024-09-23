from bclearer_interop_services.excel_services.ExcelFacade import ExcelFacade
from bclearer_interop_services.dataframe_service.dataframe_helper import drop_empty_columns
import pytest
import pandas as pd

class TestExcelInteropServices():

    @pytest.fixture(autouse=True)
    def setup_method(self,excel_file_name_and_path_xlsx):
        self.excel_file_name_and_path_xls = r"D:\S\bclearer_projects\bank_transactions\bank_transactions\code\tests\data\collect\santander_current_account_20240817.xls"

    def test_excel_interop_reading_xlsx(self,excel_file_name_and_path_xlsx):
        sheet_name = "Categories"

        try:
            excel_facade = ExcelFacade(excel_file_name_and_path_xlsx)
            print(f"Successfully initialized ExcelFacade with file: {excel_file_name_and_path_xlsx}")

            cfi_categories = excel_facade.workbook.sheet(sheet_name)
            assert cfi_categories is not None, \
                f"Sheet {sheet_name} not found in the workbook."

            cfi_categories_dataframe = cfi_categories.read_to_dataframe()
            print(f"DataFrame successfully read from the {sheet_name} sheet:")

            assert isinstance(cfi_categories_dataframe, pd.DataFrame),\
                "The result is not a DataFrame object."

            print(cfi_categories_dataframe)

            assert cfi_categories_dataframe.shape == (14, 5), \
                "DataFrame does not have the expected shape (14, 5)."

            assert not cfi_categories_dataframe.empty, \
                "DataFrame is empty."

            print(f"DataFrame shape: {cfi_categories_dataframe.shape}")

            assert cfi_categories_dataframe.iloc[0]['Code'] == 'E', \
                "First row 'Code' column value is not 'E' as expected."

        except Exception as e:
            pytest.fail(f"An error occurred during the test: {str(e)}")

    def test_excel_interop_reading_xls(self,excel_file_name_and_path_xls):
        sheet_name = "Categories"

        try:
            excel_facade = ExcelFacade(excel_file_name_and_path_xls)
            print(f"Successfully initialized ExcelFacade with file: {excel_file_name_and_path_xls}")

            cfi_categories = excel_facade.workbook.sheet(sheet_name)
            assert cfi_categories is not None, \
                f"Sheet {sheet_name} not found in the workbook."

            cfi_categories_dataframe = cfi_categories.read_to_dataframe()
            print(f"DataFrame successfully read from the {sheet_name} sheet:")

            assert isinstance(cfi_categories_dataframe, pd.DataFrame),\
                "The result is not a DataFrame object."

            print(cfi_categories_dataframe)

            assert cfi_categories_dataframe.shape == (14, 5), \
                "DataFrame does not have the expected shape (14, 5)."

            assert not cfi_categories_dataframe.empty, \
                "DataFrame is empty."

            print(f"DataFrame shape: {cfi_categories_dataframe.shape}")

            assert cfi_categories_dataframe.iloc[0]['Code'] == 'E', \
                "First row 'Code' column value is not 'E' as expected."

        except Exception as e:
            pytest.fail(f"An error occurred during the test: {str(e)}")
