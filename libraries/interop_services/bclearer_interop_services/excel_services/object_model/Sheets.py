import pandas as pd
from bclearer_interop_services.excel_services.object_model.Cells import Cells
from bclearer_interop_services.excel_services.object_model.Columns import Columns
from bclearer_interop_services.excel_services.object_model.Ranges import Ranges
from bclearer_interop_services.excel_services.object_model.Rows import Rows
from openpyxl.worksheet.worksheet import Worksheet as OpenpyxlWorksheet


class Sheets:
    def __init__(
        self,
        sheet: OpenpyxlWorksheet,
    ):
        self.sheet = sheet

    def cell(self, row: int, col: int):
        return Cells(
            self.sheet.cell(
                row=row,
                column=col,
            ),
        )

    def row(self, index: int):
        return Rows(self.sheet, index)

    def column(self, index: int):
        return Columns(
            self.sheet,
            index,
        )

    def range(
        self,
        min_row: int,
        min_col: int,
        max_row: int,
        max_col: int,
    ):
        return Ranges(
            self.sheet,
            min_row,
            min_col,
            max_row,
            max_col,
        )

    def read_to_dataframe(
        self,
        header_row_number: int = 1,
    ) -> pd.DataFrame:
        data = [[cell.value for cell in row] for row in self.sheet.rows]

        if not data:
            return pd.DataFrame()  # Return an empty DataFrame if there is no data

        # Convert to 0-based index for internal processing
        header_index = header_row_number - 1

        # Check for potential empty or merged rows
        while header_index < len(
            data,
        ) and not any(
            data[header_index],
        ):
            header_index += 1  # Skip empty rows

        # Ensure we are within bounds
        if header_index >= len(data):
            raise ValueError(
                f"header_row_number {header_row_number} (adjusted to {header_index + 1}) is out of range.",
            )

        # Set headers from the identified row
        headers = data[header_index]

        # Exclude rows above the identified header row
        data = data[header_index + 1 :]

        # Create the DataFrame with the identified headers and data below
        return pd.DataFrame(
            data,
            columns=headers,
        )


# TODO - retire these sheets

# import pandas as pd
# import os

# class Sheets:
#     def __init__(
#         self,
#         file_name_and_path,
#         sheet_name):

#         if file_name_and_path.lower().endswith(".csv"):

#             self.sheet_data_dataframe = self.load_csv(file_name_and_path)
#             self.sheet_name = os.path.basename(file_name_and_path)

#         else:
#             self.sheet_data_dataframe = self.load_excel(file_name_and_path,sheet_name)

#     def load_csv(self,file_name_and_path) -> pd.DataFrame:

#         self.sheet_name = file_name_and_path

#         sheet_data_dataframe = pd.read_csv(os.path.join(file_name_and_path, sheet_data_dataframe), encoding='latin-1')

#         return sheet_data_dataframe

#     def load_excel(self,file_name_and_path,sheet_name) -> pd.DataFrame:
#         pass
