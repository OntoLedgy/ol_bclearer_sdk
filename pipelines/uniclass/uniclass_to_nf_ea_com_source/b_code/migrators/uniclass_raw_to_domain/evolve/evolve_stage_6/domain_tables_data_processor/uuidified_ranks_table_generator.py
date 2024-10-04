from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_uuidifier import (
    uuidify_dataframe,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.nf_domains.standard_object_table_column_types import (
    StandardObjectTableColumnTypes,
)
from pandas import DataFrame, read_csv


def get_uuidified_ranks_table(
    csv_file_path: str,
) -> DataFrame:
    ranks_table = read_csv(
        csv_file_path,
    )

    uuidified_ranks_table = uuidify_dataframe(
        dataframe=ranks_table,
        uuid_column_name=StandardObjectTableColumnTypes.NF_UUIDS.column_name,
    )

    return uuidified_ranks_table
