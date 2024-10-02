from bclearer_interop_services.excel_services.object_model.Cells import Cells
from openpyxl.worksheet.worksheet import Worksheet as OpenpyxlWorksheet


class Rows:
    def __init__(
        self,
        sheet: OpenpyxlWorksheet,
        index: int,
    ):
        self.sheet = sheet
        self.index = index

    def __getitem__(
        self,
        col_index: int,
    ):
        return Cells(
            self.sheet.cell(
                row=self.index,
                column=col_index,
            ),
        )

    def __iter__(self):
        for cell in self.sheet[
            self.index
        ]:
            yield Cells(cell)
