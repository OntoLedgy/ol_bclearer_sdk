CREATE INDEX index_name_for_column FOR (column:Column) ON (column.column_uuids);
CREATE INDEX index_name_for_row FOR (row:Row) ON (row.row_uuids);
CREATE INDEX index_name_for_cell_value FOR (cv:CellValue) ON (cv.uuid);
CREATE INDEX index_name_for_cell_type FOR (celltype:CellType) ON (celltype.cell_type_uuids);
CREATE INDEX index_name_for_physical_quantity FOR (physicalquantity:PhysicalQuantity) ON (physicalquantity.physical_quantity_uuids);
CREATE INDEX index_name_for_standard_unit_of_measure FOR (standard_unit_of_measure:StandardUnitOfMeasure) ON (standard_unit_of_measure.standard_unit_of_measure_uuids);
CREATE INDEX index_name_for_property_type FOR (property_type:PropertyType) ON (property_type.property_type_uuids);
