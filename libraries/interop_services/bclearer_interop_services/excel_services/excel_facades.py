from pathlib import Path

import pandas as pd
from bclearer_interop_services.excel_services.object_model.excel_workbooks import (
    ExcelWorkbooks,
)


class ExcelFacades:
    def __init__(self, file_path):
        self.file_extension = Path(
            file_path,
        ).suffix.lower()

        self.workbook = ExcelWorkbooks(
            file_path,
            self.file_extension,
        )

    def read_cell(
        self,
        sheet_name,
        row_index,
        column_index,
    ):
        sheet = self.workbook.sheet(
            sheet_name,
        )
        cell = sheet.rows[
            row_index
        ].cells[column_index]
        return cell.value

    def read_sheet_to_dataframe(
        self,
        sheet_name: str,
        header_row_number: int = 0,
    ) -> pd.DataFrame:
        # Get the sheet from the workbook
        sheet = self.workbook.sheet(
            sheet_name,
        )

        # Convert the sheet rows into a list of lists (representing rows)
        sheet_dataframe = pd.DataFrame(
            [
                [
                    cell.value
                    for cell in row
                ]
                for row in sheet.rows
            ],
        )

        # Check if the header row exists and is valid (non-empty)
        if (
            header_row_number
            >= sheet_dataframe.shape[0]
        ):
            raise ValueError(
                f"Header row number {header_row_number} is out of range for the sheet '{sheet_name}'",
            )

        # Extract headers from the specified row
        headers = sheet_dataframe.iloc[
            header_row_number
        ]

        # Ensure no empty or duplicate headers
        if headers.isnull().any():
            raise ValueError(
                f"Header row contains null values in sheet '{sheet_name}'",
            )
        if headers.duplicated().any():
            raise ValueError(
                f"Header row contains duplicate values in sheet '{sheet_name}'",
            )

        # Set the DataFrame column headers
        sheet_dataframe.columns = (
            headers
        )

        # Drop the header row and any rows above it
        sheet_dataframe = sheet_dataframe.drop(
            index=list(
                range(
                    header_row_number
                    + 1,
                ),
            ),
        )

        # Reset the index after dropping the rows
        sheet_dataframe.reset_index(
            drop=True,
            inplace=True,
        )

        return sheet_dataframe

    def write_cell(
        self,
        sheet_name,
        row_index,
        column_index,
        value,
    ):
        sheet = self.workbook.sheet(
            sheet_name,
        )
        sheet.rows[row_index].cells[
            column_index
        ].value = value

    def update_cell(
        self,
        sheet_name,
        row_index,
        column_index,
        value,
    ):
        self.write_cell(
            sheet_name,
            row_index,
            column_index,
            value,
        )

    def save(self, file_path=None):
        if file_path is None:
            file_path = (
                self.workbook.file_path
            )

        self.workbook.save(file_path)
