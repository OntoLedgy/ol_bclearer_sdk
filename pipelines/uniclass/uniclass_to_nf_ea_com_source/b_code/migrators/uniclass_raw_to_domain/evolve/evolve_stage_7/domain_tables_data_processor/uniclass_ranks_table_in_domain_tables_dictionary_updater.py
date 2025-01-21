from pandas import DataFrame
from pipelines.uniclass.uniclass_to_nf_ea_com_source.b_code.configurations.common_constants.uniclass_bclearer_constants import (
    UNICLASS_2024_RANKS_TABLE_NAME,
)


def update_uniclass_ranks_table_in_domain_tables_dictionary(
    dictionary_of_dataframes: dict,
    dataframe: DataFrame,
) -> dict:
    dictionary_of_dataframes[
        UNICLASS_2024_RANKS_TABLE_NAME
    ] = dataframe

    return dictionary_of_dataframes
