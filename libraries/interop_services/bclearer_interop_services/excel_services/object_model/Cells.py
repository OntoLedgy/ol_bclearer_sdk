from openpyxl.cell.cell import Cell as OpenpyxlCell


class Cells:
    def __init__(
        self,
        cell: OpenpyxlCell,
    ):
        self.cell = cell

    @property
    def value(self):
        return self.cell.value

    @value.setter
    def value(self, value):
        self.cell.value = value

    @property
    def coordinate(self):
        return self.cell.coordinate
